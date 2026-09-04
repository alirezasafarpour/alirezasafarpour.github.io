/* The grammar course: curriculum loading, concept mastery and session queues.
 *
 * Grammar is deliberately its own engine sitting beside the vocabulary one.
 * They share the SRS maths, the store and the sync row, but nothing else: a
 * grammar concept is not a word, it is mastered by *demonstrating* it across
 * different exercise types on different days, so it needs its own rules.
 */

import { store } from './store.js';
import * as SRS from './srs.js';
import { shuffle, clamp, dayKey, normalizeAnswer } from './util.js';

export const LEVELS = [
  { id: 'A0', label: 'A0', name: 'Eerste woorden', fa: 'شروع از صفر' },
  { id: 'A1', label: 'A1', name: 'Basis', fa: 'پایه' },
  { id: 'A2', label: 'A2', name: 'Dagelijks gebruik', fa: 'زندگی روزمره' },
  { id: 'B1', label: 'B1', name: 'Zelfstandig', fa: 'مستقل' },
];

const BASE = new URL('../../../data/', import.meta.url);
const FILES = LEVELS.map((l) => `grammar.${l.id.toLowerCase()}.json`);

export const gdb = {
  modules: [],
  lessons: [],
  concepts: [],
  byLesson: new Map(),
  byModule: new Map(),      // moduleId -> lessons[]
  byConcept: new Map(),     // conceptId -> concept
  conceptLessons: new Map(),// conceptId -> lessons[] that teach it
  byLevel: new Map(),       // level -> modules[]
  loadErrors: [],
};

/* ---------- loading ---------- */

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

export async function loadGrammar() {
  gdb.modules = []; gdb.lessons = []; gdb.concepts = []; gdb.loadErrors = [];
  gdb.byLesson.clear(); gdb.byModule.clear(); gdb.byConcept.clear();
  gdb.conceptLessons.clear(); gdb.byLevel.clear();

  const parts = await Promise.all(FILES.map((f) => loadJSON(f).catch((err) => {
    gdb.loadErrors.push({ file: f, message: String(err.message || err) });
    return null;
  })));

  for (const part of parts) {
    if (!part) continue;
    for (const c of part.concepts || []) { gdb.concepts.push(c); gdb.byConcept.set(c.id, c); }
    for (const m of part.modules || []) gdb.modules.push(m);
    for (const l of part.lessons || []) { gdb.lessons.push(l); gdb.byLesson.set(l.id, l); }
  }

  // Curriculum order is level order, then the order modules were authored in.
  const levelRank = new Map(LEVELS.map((l, i) => [l.id, i]));
  gdb.modules.sort((a, b) => (levelRank.get(a.level) ?? 9) - (levelRank.get(b.level) ?? 9));

  for (const m of gdb.modules) {
    const lessons = (m.lessons || []).map((id) => gdb.byLesson.get(id)).filter(Boolean);
    gdb.byModule.set(m.id, lessons);
    if (!gdb.byLevel.has(m.level)) gdb.byLevel.set(m.level, []);
    gdb.byLevel.get(m.level).push(m);
  }

  for (const l of gdb.lessons) {
    for (const cid of l.concepts || []) {
      if (!gdb.conceptLessons.has(cid)) gdb.conceptLessons.set(cid, []);
      gdb.conceptLessons.get(cid).push(l);
    }
  }
  return gdb;
}

export const lesson = (id) => gdb.byLesson.get(id) || null;
export const module_ = (id) => gdb.modules.find((m) => m.id === id) || null;
export const concept = (id) => gdb.byConcept.get(id) || null;
export const moduleLessons = (id) => gdb.byModule.get(id) || [];
export const levelModules = (level) => gdb.byLevel.get(level) || [];
export const loaded = () => gdb.lessons.length > 0;

/** Every lesson in curriculum order — the spine the whole course walks along. */
export function orderedLessons() {
  const out = [];
  for (const m of gdb.modules) out.push(...moduleLessons(m.id));
  return out;
}

export function moduleOf(lessonId) {
  const l = lesson(lessonId);
  return l ? module_(l.module) : null;
}

/* ---------- concept mastery ---------- */

/**
 * Mastery is earned, not visited. A concept counts as mastered only when the
 * learner has answered it right enough times, at a decent accuracy, spread over
 * more than one day — the SRS stage alone would let a single lucky streak in
 * one sitting look like knowledge.
 */
export const MASTERY = { correct: 6, accuracy: 0.8, days: 2, stage: 4 };

export function conceptStats(id) {
  const c = store.gConcept(id);
  if (!c || !c.r) {
    return { seen: false, r: 0, c: 0, w: 0, accuracy: 0, stage: 0, days: 0, strength: 0, mastered: false, due: 0, weak: false };
  }
  const accuracy = c.c / c.r;
  const days = (c.days || []).length;
  const mastered = c.c >= MASTERY.correct && accuracy >= MASTERY.accuracy
    && days >= MASTERY.days && (c.s || 0) >= MASTERY.stage;
  return {
    seen: true,
    r: c.r, c: c.c, w: c.w || 0,
    accuracy, stage: c.s || 0, days,
    strength: strengthOf(c, mastered),
    mastered,
    due: c.due || 0,
    weak: isWeak(c),
  };
}

/** 0-100: how solid this concept looks right now. */
function strengthOf(c, mastered) {
  if (!c || !c.r) return 0;
  const acc = c.c / c.r;
  const stage = Math.min(c.s || 0, 5) / 5;
  const volume = Math.min(c.c, MASTERY.correct) / MASTERY.correct;
  const spread = Math.min((c.days || []).length, MASTERY.days) / MASTERY.days;
  const raw = stage * 0.3 + acc * 0.34 + volume * 0.22 + spread * 0.14;
  return clamp(Math.round(raw * 100), 0, mastered ? 100 : 96);
}

/** A concept the learner keeps getting wrong — what "weak topics" is built on. */
function isWeak(c) {
  if (!c || c.r < 2) return false;
  const acc = c.c / c.r;
  return acc < 0.7 || (c.l || 0) >= 2 || (c.e || 2.5) <= 1.8;
}

export function isConceptDue(id, now = Date.now()) {
  const c = store.gConcept(id);
  return !!c && c.r > 0 && (c.due || 0) <= now;
}

/* ---------- lesson state ---------- */

export const PASS_MARK = 80;

export function lessonState(id) {
  const rec = store.gLesson(id) || null;
  const l = lesson(id);
  const concepts = (l?.concepts || []).map(conceptStats);
  const started = !!rec?.started;
  const done = !!rec?.done;
  const mastered = concepts.length > 0 && concepts.every((c) => c.mastered);
  const strength = concepts.length
    ? Math.round(concepts.reduce((s, c) => s + c.strength, 0) / concepts.length)
    : 0;
  return {
    started, done, mastered, strength,
    best: rec?.best || 0, last: rec?.last || 0, tries: rec?.tries || 0,
    due: (l?.concepts || []).some((cid) => isConceptDue(cid)),
  };
}

export function moduleProgress(moduleId) {
  const lessons = moduleLessons(moduleId);
  let done = 0, mastered = 0, strength = 0;
  for (const l of lessons) {
    const st = lessonState(l.id);
    if (st.done) done += 1;
    if (st.mastered) mastered += 1;
    strength += st.strength;
  }
  return {
    total: lessons.length, done, mastered,
    strength: lessons.length ? Math.round(strength / lessons.length) : 0,
    pct: lessons.length ? Math.round((done / lessons.length) * 100) : 0,
  };
}

export function levelProgress(level) {
  const mods = levelModules(level);
  let total = 0, done = 0, mastered = 0;
  for (const m of mods) {
    const p = moduleProgress(m.id);
    total += p.total; done += p.done; mastered += p.mastered;
  }
  return { modules: mods.length, total, done, mastered, pct: total ? Math.round((done / total) * 100) : 0 };
}

export function overallProgress() {
  let total = 0, done = 0, mastered = 0, started = 0;
  for (const l of gdb.lessons) {
    total += 1;
    const st = lessonState(l.id);
    if (st.done) done += 1;
    if (st.mastered) mastered += 1;
    if (st.started) started += 1;
  }
  const concepts = gdb.concepts.length;
  let conceptsMastered = 0, conceptsSeen = 0;
  for (const c of gdb.concepts) {
    const s = conceptStats(c.id);
    if (s.seen) conceptsSeen += 1;
    if (s.mastered) conceptsMastered += 1;
  }
  const gm = store.grammar.meta || {};
  return {
    lessons: total, done, mastered, started,
    concepts, conceptsSeen, conceptsMastered,
    pct: total ? Math.round((done / total) * 100) : 0,
    answers: gm.answers || 0,
    correct: gm.correct || 0,
    accuracy: gm.answers ? Math.round((gm.correct / gm.answers) * 100) : 0,
    due: dueConcepts().length,
  };
}

/** Concepts whose review has come round, hardest-hit first. */
export function dueConcepts(now = Date.now()) {
  const out = [];
  for (const c of gdb.concepts) {
    if (!isConceptDue(c.id, now)) continue;
    out.push({ concept: c, priority: SRS.priority(store.gConcept(c.id), now) });
  }
  out.sort((a, b) => b.priority - a.priority);
  return out.map((x) => x.concept);
}

export function weakConcepts(limit = 8) {
  const out = [];
  for (const c of gdb.concepts) {
    const s = conceptStats(c.id);
    if (s.seen && s.weak) out.push({ concept: c, stats: s });
  }
  out.sort((a, b) => a.stats.strength - b.stats.strength);
  return out.slice(0, limit);
}

export function recentConcepts(limit = 6) {
  const rows = [];
  for (const c of gdb.concepts) {
    const card = store.gConcept(c.id);
    if (card?.t) rows.push({ concept: c, t: card.t, stats: conceptStats(c.id) });
  }
  rows.sort((a, b) => b.t - a.t);
  return rows.slice(0, limit);
}

/**
 * Where to go next: the first lesson that is neither passed nor a level the
 * learner has clearly outgrown. Falls back to the very first lesson.
 */
export function nextLesson() {
  const all = orderedLessons();
  if (!all.length) return null;
  const pos = store.grammar.meta?.position;
  if (pos) {
    const cur = lesson(pos);
    if (cur && !lessonState(cur.id).done) return cur;
    // The lesson after the one last worked on, if there is one.
    const idx = all.findIndex((l) => l.id === pos);
    if (idx >= 0) {
      const rest = all.slice(idx + 1).find((l) => !lessonState(l.id).done);
      if (rest) return rest;
    }
  }
  return all.find((l) => !lessonState(l.id).done) || all[all.length - 1];
}

/* ---------- exercise queues ---------- */

/**
 * A lesson run: the authored exercises in their taught order (they are already
 * written easiest-first), with anything the learner is currently weak on from
 * *earlier* lessons folded in at the end as recycling.
 */
export function lessonQueue(lessonId, { recycle = true } = {}) {
  const l = lesson(lessonId);
  if (!l) return [];
  const items = (l.exercises || []).map((ex, i) => ({ ...ex, _i: i, lesson: l.id }));
  if (!recycle) return items;

  const earlier = earlierWeakItems(lessonId, 2);
  return items.concat(earlier);
}

/** Up to `n` exercises from earlier lessons the learner is shaky on. */
function earlierWeakItems(lessonId, n) {
  const all = orderedLessons();
  const idx = all.findIndex((l) => l.id === lessonId);
  if (idx <= 0 || n <= 0) return [];
  const pool = [];
  for (const prev of all.slice(0, idx)) {
    const st = lessonState(prev.id);
    if (!st.started) continue;
    const shaky = (prev.concepts || []).some((cid) => {
      const s = conceptStats(cid);
      return s.seen && (s.weak || !s.mastered);
    });
    if (!shaky) continue;
    for (const ex of prev.exercises || []) pool.push({ ...ex, lesson: prev.id, recycled: true });
  }
  return shuffle(pool).slice(0, n);
}

/**
 * The grammar review session: exercises drawn from whatever is due, weighted
 * toward the weakest concepts, pulled from every lesson that teaches them so a
 * concept is never reviewed with the exact same question every time.
 */
export function reviewQueue({ size = 15, level = '', conceptId = '' } = {}) {
  const now = Date.now();
  let concepts = conceptId ? [concept(conceptId)].filter(Boolean) : dueConcepts(now);
  if (level) concepts = concepts.filter((c) => c.level === level);

  if (!concepts.length && !conceptId) {
    // Nothing strictly due: revisit the weakest practised concepts instead of
    // sending the learner away with an empty session.
    concepts = weakConcepts(size).map((w) => w.concept);
    if (level) concepts = concepts.filter((c) => c.level === level);
  }
  if (!concepts.length) {
    // Still nothing: recycle whatever has been practised at all.
    concepts = gdb.concepts.filter((c) => conceptStats(c.id).seen);
    if (level) concepts = concepts.filter((c) => c.level === level);
  }
  if (!concepts.length) return [];

  const items = [];
  const used = new Set();
  // Round-robin over concepts so a review session covers breadth before depth.
  for (let round = 0; items.length < size && round < 6; round++) {
    let added = 0;
    for (const c of concepts) {
      if (items.length >= size) break;
      const pool = exercisesFor(c.id).filter((ex) => !used.has(exKey(ex)));
      if (!pool.length) continue;
      const pick = pool[Math.floor(Math.random() * pool.length)];
      used.add(exKey(pick));
      items.push({ ...pick, review: true });
      added += 1;
    }
    if (!added) break;
  }
  return shuffle(items);
}

const exKey = (ex) => `${ex.lesson}:${ex.q}:${ex.a}`;

/** Every exercise in the course that practises one concept. */
export function exercisesFor(conceptId) {
  const out = [];
  for (const l of gdb.conceptLessons.get(conceptId) || []) {
    for (const ex of l.exercises || []) {
      if (!ex.concept || ex.concept === conceptId) out.push({ ...ex, lesson: l.id });
    }
  }
  return out;
}

/** A mixed cumulative drill across everything practised so far. */
export function mixedQueue(size = 15) {
  const practised = gdb.concepts.filter((c) => conceptStats(c.id).seen);
  if (!practised.length) return [];
  const pool = [];
  for (const c of practised) pool.push(...exercisesFor(c.id));
  return shuffle(pool).slice(0, size).map((ex) => ({ ...ex, review: true }));
}

/* ---------- grading ---------- */

/**
 * Grade one answer. Typed answers accept every listed alternative and tolerate
 * a single typo in longer sentences, because this is a grammar test, not a
 * spelling one — but the sentence still has to be the right shape.
 */
export function judge(ex, given) {
  const raw = String(given ?? '').trim();
  if (!raw) return { ok: false, empty: true };
  const accepted = acceptedAnswers(ex);
  const g = normalizeAnswer(raw);
  if (accepted.some((a) => normalizeAnswer(a) === g)) return { ok: true };

  if (ex.mode === 'input' && raw.length > 8) {
    for (const a of accepted) {
      const target = normalizeAnswer(a);
      if (typoDistance(g, target) <= (target.length >= 24 ? 2 : 1)) {
        return { ok: true, typo: true, target: a };
      }
    }
  }
  return { ok: false };
}

export function acceptedAnswers(ex) {
  const list = [ex.a, ...(ex.alt || [])].filter(Boolean);
  return list.length ? list : [''];
}

/** Levenshtein, only used to forgive one slip of the finger. */
function typoDistance(a, b) {
  if (a === b) return 0;
  if (Math.abs(a.length - b.length) > 3) return 99;
  let prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    for (let j = 1; j <= b.length; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    prev = cur;
  }
  return prev[b.length];
}

/* ---------- reference search ---------- */

/**
 * English names for the same things, so someone who learned grammar terms in
 * English still finds the rule. Searching "perfect tense" should not come back
 * empty just because the course calls it "perfectum".
 */
const ALIASES = {
  'perfect': 'perfectum', 'present perfect': 'perfectum',
  'past': 'verleden', 'past tense': 'imperfectum', 'simple past': 'imperfectum',
  'past participle': 'deelwoord', 'participle': 'deelwoord',
  'word order': 'woordvolgorde', 'order': 'woordvolgorde',
  'article': 'lidwoord', 'articles': 'lidwoord',
  'plural': 'meervoud', 'plurals': 'meervoud',
  'adjective': 'bijvoeglijk', 'adjectives': 'bijvoeglijk',
  'negation': 'ontkenning', 'negative': 'ontkenning',
  'pronoun': 'voornaamwoord', 'pronouns': 'voornaamwoord',
  'modal': 'modaal', 'modals': 'modaal',
  'separable': 'scheidbaar', 'reflexive': 'wederkerend',
  'passive': 'lijdende', 'conditional': 'conditioneel',
  'relative clause': 'betrekkelijke', 'subordinate': 'bijzin',
  'clause': 'bijzin', 'conjunction': 'voegwoord',
  'question': 'vraag', 'questions': 'vraag',
  'future': 'toekomst', 'imperative': 'gebiedende',
  'comparative': 'vergrotende', 'superlative': 'overtreffende',
  'diminutive': 'verkleinwoord', 'infinitive': 'infinitief',
  'tense': '', 'verb': 'werkwoord', 'verbs': 'werkwoord',
  'noun': 'naamwoord', 'nouns': 'naamwoord',
};

/**
 * The reference is a lookup, not a course: it searches rules, concepts and
 * lesson titles in Dutch, English and Persian.
 *
 * Short words are matched whole only — "er" has to find the lesson about *er*,
 * not every lesson containing "werkwoord" or "verleden".
 */
export function searchReference(query) {
  const raw = String(query || '').trim().toLowerCase();
  if (!raw) return [];

  const phrase = ALIASES[raw];
  const terms = (phrase !== undefined ? [phrase || raw] : raw.split(/\s+/))
    // An alias of '' marks a filler word ("tense", "form") — drop it entirely
    // rather than demanding the course use that English word.
    .filter((t) => ALIASES[t] !== '')
    .flatMap((t) => (ALIASES[t] ? [t, ALIASES[t]] : [t]))
    .filter(Boolean);
  if (!terms.length) return [];

  const rows = [];
  for (const l of gdb.lessons) {
    const hay = referenceText(l);
    let score = 0;
    let missed = false;
    // An aliased term counts if either the original or its translation hits.
    for (const t of terms) {
      const whole = new RegExp(`(^|[^\\p{L}\\p{M}])${escapeRe(t)}([^\\p{L}\\p{M}]|$)`, 'u').test(hay);
      const loose = t.length > 3 && hay.includes(t);
      if (!whole && !loose) {
        // Tolerate a miss when it is one half of an alias pair that did hit.
        const alias = ALIASES[t];
        if (alias && new RegExp(`(^|[^\\p{L}\\p{M}])${escapeRe(alias)}`, 'u').test(hay)) { score += 2; continue; }
        missed = true;
        break;
      }
      score += whole ? 3 : 1;
      if ((l.title || '').toLowerCase().includes(t)) score += 5;
      if ((l.titleFa || '').includes(t)) score += 5;
      if ((l.rule?.nl || '').toLowerCase().includes(t)) score += 2;
      for (const cid of l.concepts || []) {
        const c = concept(cid);
        if (!c) continue;
        if ((c.title || '').toLowerCase().includes(t)) score += 4;
        if ((c.keywords || []).some((k) => k.toLowerCase() === t)) score += 6;
      }
    }
    if (!missed && score > 0) rows.push({ lesson: l, score });
  }
  rows.sort((a, b) => b.score - a.score || a.lesson.id.localeCompare(b.lesson.id));
  return rows.map((r) => r.lesson);
}

const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

function referenceText(l) {
  if (l._ref) return l._ref;
  const parts = [
    l.title, l.titleFa, l.rule?.nl, l.rule?.fa, l.usage, l.discover?.fa,
    ...(l.concepts || []).flatMap((cid) => {
      const c = concept(cid);
      return c ? [c.title, c.titleFa, ...(c.keywords || [])] : [];
    }),
    ...(l.examples || []).flatMap((e) => [e.nl, e.fa]),
    ...(l.pattern?.parts || []).map((p) => p.text),
  ];
  l._ref = parts.filter(Boolean).join(' · ').toLowerCase();
  return l._ref;
}

/** Dutch words used in a lesson's examples — the bridge to the word trainer. */
export function lessonVocabulary(l) {
  const words = new Set();
  const add = (s) => {
    for (const m of String(s || '').match(/[A-Za-zÀ-ÖØ-öø-ÿ]+/g) || []) words.add(m.toLowerCase());
  };
  for (const e of l.examples || []) add(e.nl);
  for (const e of l.exercises || []) { add(e.a); add(e.q); }
  for (const c of l.contrast || []) add(c.good);
  return words;
}

export { dayKey };
