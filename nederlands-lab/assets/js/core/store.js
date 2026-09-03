/* Progress store.
 *
 * Offline-first: everything lives in memory, is persisted to IndexedDB (with a
 * localStorage mirror as a last-resort backup) and is pushed to Supabase by
 * sync.js when an account is connected. Nothing is ever only in localStorage.
 */

import { dayKey, dayStart, daysBetween, DAY, clamp, pct } from './util.js';
import * as SRS from './srs.js';

const DB_NAME = 'nederlands-lab';
const DB_VERSION = 1;
const STORE_KV = 'kv';
const STORE_DATA = 'datasets';
const STATE_KEY = 'state';
const MIRROR_KEY = 'nl-lab:mirror';
const SCHEMA = 2;

export const DEFAULT_SETTINGS = {
  theme: 'auto',
  direction: 'nl-fa',        // prompt language for mixed sessions
  sessionSize: 20,
  newPerSession: 8,
  autoSpeak: false,
  speakRate: 0.92,
  voiceURI: '',
  showEnglish: true,
  typingStrictness: 'lenient',
  gloss: true,
};

function freshState() {
  return {
    schema: SCHEMA,
    cards: {},               // wordId -> SRS card
    flags: {},               // wordId -> { fav: 1, hard: 1 }
    meta: {
      streak: 0, bestStreak: 0, lastDay: '', lastActivity: 0,
      answers: 0, correct: 0,
      position: {},          // book -> lesson number in progress
      lastBook: 'gb',
      daily: {},             // dayKey -> { a, c, n, ms }
      createdAt: Date.now(),
    },
    settings: { ...DEFAULT_SETTINGS },
    rev: 0,                  // bumped on every local mutation
    updatedAt: 0,
  };
}

/* ---------- IndexedDB ---------- */

let dbPromise = null;
function openDB() {
  if (dbPromise) return dbPromise;
  dbPromise = new Promise((resolve, reject) => {
    if (!('indexedDB' in globalThis)) return reject(new Error('no indexedDB'));
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE_KV)) db.createObjectStore(STORE_KV);
      if (!db.objectStoreNames.contains(STORE_DATA)) db.createObjectStore(STORE_DATA);
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  }).catch((err) => { dbPromise = null; throw err; });
  return dbPromise;
}

async function idbGet(store, key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(store, 'readonly');
    const req = tx.objectStore(store).get(key);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function idbSet(store, key, value) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(store, 'readwrite');
    tx.objectStore(store).put(value, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

/* ---------- store ---------- */

class Store extends EventTarget {
  constructor() {
    super();
    this.state = freshState();
    this.ready = false;
    this._saveTimer = null;
    this._persistFailed = false;
  }

  async init() {
    let loaded = null;
    try {
      loaded = await idbGet(STORE_KV, STATE_KEY);
    } catch {
      this._persistFailed = true;
    }
    if (!loaded) loaded = this._readMirror();
    if (loaded) this.state = migrate(loaded);
    this.state.settings = { ...DEFAULT_SETTINGS, ...(this.state.settings || {}) };
    this.refreshStreak();
    this.ready = true;
    this.emit('ready');
    return this.state;
  }

  emit(type, detail) { this.dispatchEvent(new CustomEvent(type, { detail })); }
  on(type, fn) { this.addEventListener(type, fn); return () => this.removeEventListener(type, fn); }

  get settings() { return this.state.settings; }
  get meta() { return this.state.meta; }

  card(id) { return this.state.cards[id]; }
  flags(id) { return this.state.flags[id] || {}; }
  isFav(id) { return !!this.flags(id).fav; }
  isHard(id) { return !!this.flags(id).hard; }

  /** Marked difficult by hand, or judged difficult by the scheduler. */
  difficult(id) { return this.isHard(id) || SRS.isDifficult(this.card(id)); }

  /* ---------- mutations ---------- */

  /** Record one answer. Returns the updated card. */
  answer(id, grade, opts = {}) {
    const now = Date.now();
    const before = this.state.cards[id];
    const wasNew = SRS.isNew(before);
    const card = SRS.review(before, grade, now);
    this.state.cards[id] = card;

    const m = this.state.meta;
    if (!opts.silent) {
      m.answers += 1;
      if (grade > SRS.GRADE.AGAIN) m.correct += 1;
      const k = dayKey(now);
      const day = (m.daily[k] ||= { a: 0, c: 0, n: 0 });
      day.a += 1;
      if (grade > SRS.GRADE.AGAIN) day.c += 1;
      if (wasNew) day.n += 1;
    }
    m.lastActivity = now;
    this.refreshStreak(now);
    this.touch();
    this.emit('progress', { id, card });
    return card;
  }

  /** Introduce a word without grading it (Learn mode's first contact). */
  introduce(id) {
    const card = { ...SRS.blank(), ...(this.state.cards[id] || {}) };
    if (!card.seen) card.seen = Date.now();
    if (card.s < 1) card.s = 1;
    card.t = Date.now();
    this.state.cards[id] = card;
    this.touch();
    return card;
  }

  setFlag(id, key, value) {
    const f = { ...(this.state.flags[id] || {}) };
    if (value) f[key] = 1; else delete f[key];
    f.t = Date.now();
    if (Object.keys(f).length <= 1) delete this.state.flags[id];
    else this.state.flags[id] = f;
    this.touch();
    this.emit('flags', { id, key, value });
  }
  toggleFav(id) { const v = !this.isFav(id); this.setFlag(id, 'fav', v); return v; }
  toggleHard(id) { const v = !this.isHard(id); this.setFlag(id, 'hard', v); return v; }

  setPosition(book, lesson) {
    this.state.meta.position[book] = lesson;
    this.state.meta.lastBook = book;
    this.touch();
  }

  updateSettings(patch) {
    Object.assign(this.state.settings, patch);
    this.touch();
    this.emit('settings', patch);
  }

  /** Add session time to today's tally. */
  addTime(ms) {
    if (!(ms > 0)) return;
    const day = (this.state.meta.daily[dayKey()] ||= { a: 0, c: 0, n: 0 });
    day.ms = (day.ms || 0) + Math.round(ms);
    this.touch();
  }

  /* ---------- streak ---------- */

  refreshStreak(now = Date.now()) {
    const m = this.state.meta;
    const today = dayKey(now);
    const studiedToday = (m.daily[today]?.a || 0) > 0;
    if (m.lastDay === today) {
      if (studiedToday && m.streak === 0) m.streak = 1;
      return m.streak;
    }
    if (studiedToday) {
      const gap = m.lastDay ? daysBetween(new Date(m.lastDay + 'T00:00:00').getTime(), now) : 999;
      m.streak = gap === 1 ? m.streak + 1 : 1;
      m.lastDay = today;
      m.bestStreak = Math.max(m.bestStreak || 0, m.streak);
    } else if (m.lastDay) {
      // Streak survives today until midnight; it only breaks once a day is skipped.
      const gap = daysBetween(new Date(m.lastDay + 'T00:00:00').getTime(), now);
      if (gap > 1) m.streak = 0;
    }
    return m.streak;
  }

  /* ---------- derived stats ---------- */

  stats(words) {
    const now = Date.now();
    let learned = 0, mastered = 0, difficult = 0, due = 0, fresh = 0, seen = 0;
    for (const w of words) {
      const c = this.state.cards[w.id];
      if (!c || !c.r) { fresh += 1; continue; }
      seen += 1;
      if (c.s >= 2) learned += 1;
      if (SRS.isMastered(c)) mastered += 1;
      if (this.difficult(w.id)) difficult += 1;
      if (c.due <= now) due += 1;
    }
    const m = this.state.meta;
    return {
      total: words.length, learned, mastered, difficult, due, fresh, seen,
      accuracy: pct(m.correct, m.answers),
      answers: m.answers, correct: m.correct,
      streak: m.streak, bestStreak: m.bestStreak || 0,
    };
  }

  todayStats() {
    const d = this.state.meta.daily[dayKey()] || { a: 0, c: 0, n: 0 };
    return { answers: d.a, correct: d.c, newWords: d.n, minutes: Math.round((d.ms || 0) / 60000) };
  }

  /** Last `n` days of activity for the heatmap, oldest first. */
  history(n = 91) {
    const out = [];
    const start = dayStart() - (n - 1) * DAY;
    for (let i = 0; i < n; i++) {
      const ts = start + i * DAY;
      const d = this.state.meta.daily[dayKey(ts)];
      out.push({ ts, answers: d?.a || 0, correct: d?.c || 0 });
    }
    return out;
  }

  /* ---------- persistence ---------- */

  touch() {
    this.state.rev = (this.state.rev || 0) + 1;
    this.state.updatedAt = Date.now();
    this.scheduleSave();
    this.emit('dirty');
  }

  scheduleSave() {
    clearTimeout(this._saveTimer);
    this._saveTimer = setTimeout(() => this.save(), 500);
  }

  async save() {
    clearTimeout(this._saveTimer);
    try {
      await idbSet(STORE_KV, STATE_KEY, this.state);
      this._persistFailed = false;
    } catch {
      this._persistFailed = true;
    }
    this._writeMirror();
    this.emit('saved');
  }

  /** Compact localStorage mirror: enough to rebuild if IndexedDB is wiped. */
  _writeMirror() {
    try {
      localStorage.setItem(MIRROR_KEY, JSON.stringify(this.state));
    } catch {
      // Over quota: keep meta + settings only, cards live in IndexedDB/cloud.
      try {
        localStorage.setItem(MIRROR_KEY, JSON.stringify({
          schema: SCHEMA, cards: {}, flags: this.state.flags,
          meta: this.state.meta, settings: this.state.settings,
          rev: this.state.rev, updatedAt: this.state.updatedAt, partial: true,
        }));
      } catch { /* storage unavailable; IndexedDB and cloud still hold the data */ }
    }
  }

  _readMirror() {
    try {
      const raw = localStorage.getItem(MIRROR_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch { return null; }
  }

  get persistenceDegraded() { return this._persistFailed; }

  /* ---------- import / export / merge ---------- */

  export() {
    return { app: 'nederlands-lab', exportedAt: Date.now(), ...structuredClone(this.state) };
  }

  /** Replace local state with `incoming`, keeping whichever record is newer. */
  applyRemote(remote) {
    if (!remote) return false;
    const merged = mergeStates(this.state, migrate(remote));
    const changed = merged.rev !== this.state.rev || merged.updatedAt !== this.state.updatedAt;
    this.state = merged;
    this.state.settings = { ...DEFAULT_SETTINGS, ...(this.state.settings || {}) };
    this.refreshStreak();
    this.save();
    this.emit('merged');
    return changed;
  }

  async cacheDataset(key, value) { try { await idbSet(STORE_DATA, key, value); } catch { /* cache is optional */ } }
  async readDataset(key) { try { return await idbGet(STORE_DATA, key); } catch { return null; } }

  async reset() {
    this.state = freshState();
    await this.save();
    this.emit('merged');
  }
}

/* ---------- merging ---------- */

/**
 * Merge two states field by field. Cards and flags carry their own `t`
 * timestamp, so two devices that studied different words both keep their work;
 * only the same word touched on both devices resolves last-write-wins.
 */
export function mergeStates(a, b) {
  if (!a) return b;
  if (!b) return a;
  const out = freshState();
  out.cards = { ...a.cards };
  for (const [id, rc] of Object.entries(b.cards || {})) {
    const lc = out.cards[id];
    if (!lc) { out.cards[id] = rc; continue; }
    const lt = lc.t || lc.last || 0;
    const rt = rc.t || rc.last || 0;
    if (rt > lt) out.cards[id] = rc;
    else if (rt === lt && (rc.r || 0) > (lc.r || 0)) out.cards[id] = rc;
  }
  out.flags = { ...a.flags };
  for (const [id, rf] of Object.entries(b.flags || {})) {
    const lf = out.flags[id];
    if (!lf || (rf.t || 0) > (lf.t || 0)) out.flags[id] = rf;
  }

  const am = a.meta || {}, bm = b.meta || {};
  const daily = { ...(am.daily || {}) };
  for (const [k, d] of Object.entries(bm.daily || {})) {
    const cur = daily[k];
    // Same day on two devices: keep the fuller record rather than double-counting.
    if (!cur || (d.a || 0) > (cur.a || 0)) daily[k] = d;
  }
  const newer = (bm.lastActivity || 0) > (am.lastActivity || 0) ? bm : am;
  out.meta = {
    ...am, ...bm,
    daily,
    answers: Math.max(am.answers || 0, bm.answers || 0),
    correct: Math.max(am.correct || 0, bm.correct || 0),
    streak: Math.max(am.streak || 0, bm.streak || 0),
    bestStreak: Math.max(am.bestStreak || 0, bm.bestStreak || 0),
    lastActivity: Math.max(am.lastActivity || 0, bm.lastActivity || 0),
    position: { ...(am.position || {}), ...(bm.position || {}) },
    lastBook: newer.lastBook || am.lastBook || 'gb',
    createdAt: Math.min(am.createdAt || Date.now(), bm.createdAt || Date.now()),
  };
  out.settings = (b.updatedAt || 0) >= (a.updatedAt || 0)
    ? { ...a.settings, ...b.settings }
    : { ...b.settings, ...a.settings };
  out.rev = Math.max(a.rev || 0, b.rev || 0) + 1;
  out.updatedAt = Math.max(a.updatedAt || 0, b.updatedAt || 0);
  return out;
}

function migrate(s) {
  const out = { ...freshState(), ...s };
  out.cards = s.cards || {};
  out.flags = s.flags || {};
  out.meta = { ...freshState().meta, ...(s.meta || {}) };
  out.meta.daily = s.meta?.daily || {};
  out.meta.position = s.meta?.position || {};
  out.schema = SCHEMA;
  return out;
}

export const store = new Store();
export { SCHEMA, MIRROR_KEY };
