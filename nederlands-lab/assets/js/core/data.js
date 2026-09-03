/* Dataset loading, indexing and session queue building.
 *
 * Both books share one schema, so every study mode works identically on
 * Het Groene Boek and Tweede Ronde. Books are described in BOOKS; a book whose
 * files are missing simply does not appear, so the app still runs.
 */

import { store } from './store.js';
import * as SRS from './srs.js';
import { shuffle, sample, tokenize, normalizeAnswer, uniqBy, clamp } from './util.js';

export const BOOKS = [
  { id: 'gb', name: 'Het Groene Boek', short: 'Groen Boek', tone: 'gb',
    note: 'Delftse methode, deel 1' },
  { id: 'tr', name: 'Tweede Ronde', short: 'Tweede Ronde', tone: 'tr',
    note: 'Delftse methode, deel 2' },
];

const BASE = new URL('../../../data/', import.meta.url);

export const db = {
  words: [],
  byId: new Map(),
  byBook: new Map(),        // bookId -> words[]
  lessons: new Map(),       // bookId -> lesson[]
  books: [],                // BOOKS entries that actually loaded
  lexicon: new Map(),       // normalized dutch token -> {term, fa}
  stems: new Map(),         // stem -> lexicon entry (for inflected forms)
  loadErrors: [],
};

async function loadJSON(name) {
  const url = new URL(name, BASE).href;
  const cacheKey = `file:${name}`;
  try {
    const res = await fetch(url, { cache: 'no-cache' });
    if (!res.ok) throw new Error(String(res.status));
    const json = await res.json();
    store.cacheDataset(cacheKey, json);
    return json;
  } catch (err) {
    const cached = await store.readDataset(cacheKey);
    if (cached) return cached;
    throw err;
  }
}

export async function loadData() {
  db.words = []; db.byId.clear(); db.byBook.clear(); db.lessons.clear();
  db.books = []; db.loadErrors = [];

  for (const book of BOOKS) {
    let words = null, meta = null;
    try {
      [words, meta] = await Promise.all([
        loadJSON(book.id + '.words.json'),
        loadJSON(book.id + '.lessons.json').catch(() => null),
      ]);
    } catch (err) {
      db.loadErrors.push({ book: book.id, message: String(err.message || err) });
      continue;
    }
    if (!Array.isArray(words) || !words.length) continue;

    for (const w of words) {
      w.book = book.id;
      if (!db.byId.has(w.id)) { db.byId.set(w.id, w); db.words.push(w); }
    }
    db.byBook.set(book.id, words);
    const lessons = (meta && meta.lessons ? meta.lessons : []).map((l) => ({ ...l, book: book.id }));
    if (!lessons.length) {
      // Derive a minimal lesson list when a book ships without lesson metadata.
      const seen = new Map();
      for (const w of words) {
        const n = w.lesson == null ? 0 : w.lesson;
        const rec = seen.get(n) || { book: book.id, n, title: 'Les ' + n, words: 0, text: [], cloze: [] };
        rec.words += 1; seen.set(n, rec);
      }
      lessons.push(...[...seen.values()].sort((a, b) => a.n - b.n));
    }
    db.lessons.set(book.id, lessons);
    db.books.push({
      ...book,
      name: (meta && meta.title) || book.name,
      note: (meta && meta.subtitle) || book.note,
    });
  }

  buildSearchKeys();
  buildLexicon();
  return db;
}

function buildSearchKeys() {
  for (const w of db.words) {
    w._k = [w.term, w.printed, w.en, w.lemma, w.equiv, (w.colloc || []).join(' ')]
      .filter(Boolean).join(' ').toLowerCase();
    w._fa = (w.fa || '') + ' ' + (w.faShort || '');
  }
}

/** Dutch -> Persian gloss lexicon, including a light stem index for inflections. */
function buildLexicon() {
  db.lexicon.clear(); db.stems.clear();
  for (const w of db.words) {
    const gloss = { term: w.term, fa: w.faShort || w.fa, id: w.id };
    const forms = [w.term, w.lemma, w.verb && w.verb.inf, w.plural].filter(Boolean);
    for (const form of forms) {
      for (const t of tokenize(form)) {
        const k = t.toLowerCase();
        if (!db.lexicon.has(k)) db.lexicon.set(k, gloss);
      }
    }
  }
  for (const [k, v] of db.lexicon) {
    const stem = k.replace(/(eren|en|te|de|s|e)$/, '');
    if (stem.length >= 4 && !db.stems.has(stem)) db.stems.set(stem, v);
  }
}

/** Persian gloss for one Dutch token, tolerant of common inflections. */
export function glossFor(token) {
  const k = String(token || '').toLowerCase();
  if (!k) return null;
  const direct = db.lexicon.get(k);
  if (direct) return direct;
  for (const suffix of ['en', 'e', 's', 'de', 'te', 'n']) {
    if (k.endsWith(suffix)) {
      const hit = db.lexicon.get(k.slice(0, -suffix.length));
      if (hit) return hit;
    }
  }
  const stem = k.replace(/(eren|en|te|de|s|e)$/, '');
  return (stem.length >= 4 && db.stems.get(stem)) || null;
}

/* ---------- lookups ---------- */

export const word = (id) => db.byId.get(id);
export const bookWords = (bookId) => db.byBook.get(bookId) || [];
export const bookLessons = (bookId) => db.lessons.get(bookId) || [];
export const lessonWords = (bookId, n) => bookWords(bookId).filter((w) => w.lesson === n);
export const lesson = (bookId, n) => bookLessons(bookId).find((l) => l.n === n) || null;

export function hasBook(id) { return db.books.some((b) => b.id === id); }
export function defaultBook() { return (db.books[0] && db.books[0].id) || 'gb'; }

/* ---------- search ---------- */

export function search(query, filters = {}) {
  const q = String(query || '').trim().toLowerCase();
  const qFa = String(query || '').trim();
  const now = Date.now();
  let pool = filters.book ? bookWords(filters.book) : db.words;
  if (filters.lesson != null) pool = pool.filter((w) => w.lesson === filters.lesson);

  if (filters.status) {
    pool = pool.filter((w) => {
      const c = store.card(w.id);
      switch (filters.status) {
        case 'new': return SRS.isNew(c);
        case 'learning': return c && c.r > 0 && c.s < SRS.STAGE_MASTERED;
        case 'mastered': return SRS.isMastered(c);
        case 'difficult': return store.difficult(w.id);
        case 'favorite': return store.isFav(w.id);
        case 'due': return SRS.isDue(c, now);
        default: return true;
      }
    });
  }
  if (filters.cefr) pool = pool.filter((w) => (w.cefr || '').includes(filters.cefr));
  if (filters.tier) pool = pool.filter((w) => w.tier === filters.tier);

  if (!q) return pool;

  const scored = [];
  for (const w of pool) {
    let score = 0;
    const term = (w.term || '').toLowerCase();
    if (term === q) score = 100;
    else if (term.startsWith(q)) score = 70;
    else if (w._k.includes(q)) score = 40;
    if (!score && w._fa && w._fa.includes(qFa)) score = 35;
    if (score) scored.push([score - term.length * 0.01, w]);
  }
  scored.sort((a, b) => b[0] - a[0]);
  return scored.map((x) => x[1]);
}

/* ---------- exercise material ---------- */

const LETTER = 'A-Za-zÀ-ÖØ-öø-ÿ';

function wordRe(term, flags) {
  const body = String(term).trim().split(/\s+/)
    .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+');
  return new RegExp('(?<![' + LETTER + '])(' + body + ')(?![' + LETTER + '])', flags || 'i');
}

/** Examples usable as a gap-fill: the sentence must actually contain the word. */
export function clozeExamples(w) {
  if (w._cloze) return w._cloze;
  const out = [];
  let re;
  try { re = wordRe(w.term); } catch { w._cloze = out; return out; }
  for (const ex of w.ex || []) {
    const m = re.exec(ex.nl);
    if (m && ex.nl.length >= 18) out.push({ ...ex, match: m[1], index: m.index });
  }
  w._cloze = out;
  return out;
}

/** All match ranges of the headword inside a sentence, for highlighting. */
export function termRanges(sentence, term) {
  const out = [];
  let re;
  try { re = wordRe(term, 'gi'); } catch { return out; }
  const s = String(sentence);
  for (let m; (m = re.exec(s));) {
    out.push([m.index, m.index + m[1].length]);
    if (m.index === re.lastIndex) re.lastIndex += 1;
  }
  return out;
}

/**
 * Distractors for multiple choice: same book and nearby lesson first, then the
 * same part of speech, then anything, always with a different meaning.
 */
export function distractors(target, n = 3, field = 'fa') {
  const own = bookWords(target.book);
  const pool = own.length > n * 6 ? own : db.words;
  const valueOf = (w) => (field === 'fa' ? (w.faShort || w.fa) : w[field]);
  const answer = normalizeAnswer(valueOf(target) || '');
  const near = [], samePos = [], rest = [];
  for (const w of pool) {
    if (w.id === target.id) continue;
    const val = valueOf(w);
    if (!val) continue;
    if (normalizeAnswer(val) === answer) continue;
    if (Math.abs((w.lesson || 0) - (target.lesson || 0)) <= 2) near.push(w);
    else if (w.pos && w.pos === target.pos) samePos.push(w);
    else rest.push(w);
  }
  const picked = [];
  for (const bucket of [near, samePos, rest]) {
    if (picked.length >= n) break;
    picked.push(...sample(bucket, n - picked.length));
  }
  return uniqBy(picked, (w) => w.id).slice(0, n);
}

/* ---------- queue building ---------- */

export const MODES = {
  learn:  { label: 'Leren',             icon: 'spark' },
  review: { label: 'Herhalen',          icon: 'refresh' },
  flash:  { label: 'Flashcards',        icon: 'cards' },
  mc:     { label: 'Meerkeuze',         icon: 'list' },
  type:   { label: 'Typen',             icon: 'pencil' },
  blank:  { label: 'Invullen',          icon: 'gap' },
  listen: { label: 'Luisteren',         icon: 'ear' },
  hard:   { label: 'Moeilijke woorden', icon: 'flag' },
  fav:    { label: 'Favorieten',        icon: 'star' },
};

const MODE_EXERCISES = {
  learn: ['mc', 'mcRev', 'type', 'blank'],
  review: ['mc', 'mcRev', 'type', 'blank'],
  lesson: ['mc', 'mcRev', 'type', 'blank'],
  hard: ['mc', 'mcRev', 'type', 'blank'],
  fav: ['mc', 'mcRev', 'type', 'blank'],
};

/** Which exercise suits a card's current stage: the Delftse progression. */
export function exerciseForStage(w, card, allow) {
  const s = (card && card.s) || 0;
  const canCloze = clozeExamples(w).length > 0;
  let pick;
  if (s <= 1) pick = 'mc';                       // meet it, then recognise it
  else if (s === 2) pick = 'mcRev';              // recognise it the other way
  else if (s === 3) pick = 'type';               // produce it
  else pick = canCloze ? 'blank' : 'type';       // use it in context
  if (allow && !allow.includes(pick)) {
    pick = allow.find((a) => a !== 'blank' || canCloze) || 'mc';
  }
  if (pick === 'blank' && !canCloze) pick = 'type';
  return pick;
}

function poolFor(kind, opts) {
  const book = opts.book;
  const now = Date.now();
  // An explicit pool (e.g. the current search results) overrides everything.
  if (Array.isArray(opts.pool) && opts.pool.length) return opts.pool;
  const all = book ? bookWords(book) : db.words;
  switch (kind) {
    case 'hard': return all.filter((w) => store.difficult(w.id));
    case 'fav': return all.filter((w) => store.isFav(w.id));
    case 'review': return all.filter((w) => SRS.isDue(store.card(w.id), now));
    case 'lesson': return opts.lesson != null ? lessonWords(book, opts.lesson) : all;
    default: return all;
  }
}

/**
 * Build a study queue.
 *
 * Due reviews always come first so nothing that is slipping gets buried behind
 * new material: the single most important scheduling rule in the app.
 */
export function buildQueue(kind, opts = {}) {
  const now = Date.now();
  const size = clamp(opts.size || store.settings.sessionSize || 20, 4, 120);
  const newCap = clamp(opts.newPerSession == null ? store.settings.newPerSession : opts.newPerSession, 0, size);
  const allow = MODE_EXERCISES[kind] || null;

  const pool = poolFor(kind, opts);
  if (!pool.length) return [];

  const due = [], fresh = [], rest = [];
  for (const w of pool) {
    const c = store.card(w.id);
    if (SRS.isNew(c)) fresh.push(w);
    else if (SRS.isDue(c, now)) due.push(w);
    else rest.push(w);
  }
  due.sort((a, b) => SRS.priority(store.card(b.id), now) - SRS.priority(store.card(a.id), now));

  if (kind === 'learn') return learnQueue(due, fresh, rest, size, newCap);

  let picked;
  if (kind === 'review') {
    picked = due.slice(0, size);
    if (picked.length < size) {
      // Nothing due: pull the weakest seen words forward rather than stopping.
      picked.push(...rest
        .filter((w) => store.card(w.id))
        .sort((a, b) => SRS.strength(store.card(a.id)) - SRS.strength(store.card(b.id)))
        .slice(0, size - picked.length));
    }
  } else if (kind === 'lesson') {
    picked = [...due, ...fresh, ...shuffle(rest)].slice(0, size);
  } else {
    picked = shuffle([...due, ...shuffle(fresh).slice(0, newCap), ...rest]).slice(0, size);
    picked.sort((a, b) => SRS.priority(store.card(b.id), now) - SRS.priority(store.card(a.id), now));
  }

  const items = picked.map((w) => {
    const card = store.card(w.id);
    let ex;
    if (kind === 'flash') ex = 'flash';
    else if (kind === 'listen') ex = 'listen';
    else if (kind === 'mc') ex = Math.random() < 0.5 ? 'mc' : 'mcRev';
    else if (kind === 'type') ex = 'type';
    else if (kind === 'blank') ex = clozeExamples(w).length ? 'blank' : 'type';
    else if (kind === 'learn' && SRS.isNew(card)) ex = 'intro';
    else ex = exerciseForStage(w, card, allow);
    return { id: w.id, ex };
  });

  // Learn mode keeps its deliberate order; everything else gets de-clumped.
  return kind === 'learn' ? items : spreadExercises(items);
}

const LEARN_BATCH = 4;

/**
 * Learn mode follows the Delftse rhythm: meet a small batch of words, then
 * drill that same batch straight away — first recognition, then production —
 * before moving on. Words that are already due are cleared first.
 */
function learnQueue(due, fresh, rest, size, newCap) {
  const items = [];
  for (const w of due.slice(0, Math.max(0, size - newCap))) {
    items.push({ id: w.id, ex: exerciseForStage(w, store.card(w.id), MODE_EXERCISES.learn) });
  }

  const introduce = fresh.slice(0, Math.max(1, newCap));
  for (let i = 0; i < introduce.length; i += LEARN_BATCH) {
    const batch = introduce.slice(i, i + LEARN_BATCH);
    for (const w of batch) items.push({ id: w.id, ex: 'intro' });
    // Pass 1: recognise the meaning. Pass 2: produce the Dutch word.
    for (const w of shuffle(batch)) items.push({ id: w.id, ex: 'mc' });
    for (const w of shuffle(batch)) {
      items.push({ id: w.id, ex: clozeExamples(w).length && Math.random() < 0.4 ? 'blank' : 'mcRev' });
    }
  }

  // A short warm-down of already-known words keeps the session from ending cold.
  if (!introduce.length && !items.length) {
    for (const w of rest.slice(0, size)) {
      items.push({ id: w.id, ex: exerciseForStage(w, store.card(w.id), MODE_EXERCISES.learn) });
    }
  }
  return items;
}

/** Keep the queue varied so the same exercise type never runs many times over. */
function spreadExercises(items) {
  const buckets = new Map();
  for (const it of items) {
    if (!buckets.has(it.ex)) buckets.set(it.ex, []);
    buckets.get(it.ex).push(it);
  }
  const keys = [...buckets.keys()];
  const out = [];
  while (out.length < items.length) {
    let moved = false;
    for (const k of keys) {
      const b = buckets.get(k);
      if (b.length) { out.push(b.shift()); moved = true; }
    }
    if (!moved) break;
  }
  return out;
}

/** Counts used by the dashboard tiles. */
export function counts(bookId) {
  const now = Date.now();
  const pool = bookId ? bookWords(bookId) : db.words;
  let due = 0, fresh = 0, hard = 0, fav = 0;
  for (const w of pool) {
    const c = store.card(w.id);
    if (SRS.isNew(c)) fresh += 1;
    else if (SRS.isDue(c, now)) due += 1;
    if (store.difficult(w.id)) hard += 1;
    if (store.isFav(w.id)) fav += 1;
  }
  return { due, fresh, hard, fav, total: pool.length };
}

/** The lesson the learner should continue with in a book. */
export function currentLesson(bookId) {
  const saved = store.meta.position[bookId];
  const lessons = bookLessons(bookId);
  if (!lessons.length) return null;
  if (saved != null && lessons.some((l) => l.n === saved)) return saved;
  for (const l of lessons) {
    const words = lessonWords(bookId, l.n);
    const started = words.filter((w) => !SRS.isNew(store.card(w.id))).length;
    if (started < words.length) return l.n;
  }
  return lessons[lessons.length - 1].n;
}

export function lessonProgress(bookId, n) {
  const words = lessonWords(bookId, n);
  if (!words.length) return { total: 0, seen: 0, mastered: 0, pctSeen: 0 };
  let seen = 0, mastered = 0;
  for (const w of words) {
    const c = store.card(w.id);
    if (c && c.r) seen += 1;
    if (SRS.isMastered(c)) mastered += 1;
  }
  return { total: words.length, seen, mastered, pctSeen: Math.round((seen / words.length) * 100) };
}
