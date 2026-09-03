/* Spaced repetition.
 *
 * An SM-2 derivative tuned for vocabulary drilling in the Delftse rhythm:
 *  - a word climbs five learning stages before it enters long-interval review;
 *  - a wrong answer drops the stage and shortens the interval sharply, so the
 *    word comes back within the same session and again the next day;
 *  - a word answered easily several times in a row stretches out fast, so
 *    mastered vocabulary stops competing for attention.
 */

import { DAY, clamp, dayStart } from './util.js';

export const STAGES = ['nieuw', 'kennismaking', 'herkennen', 'oproepen', 'toepassen', 'beheerst'];
export const STAGE_NEW = 0;
export const STAGE_MASTERED = 5;

/** Learning-stage intervals in days before a card graduates to SM-2 spacing. */
const STEP_DAYS = [0, 0, 1, 2, 4];

export const GRADE = { AGAIN: 0, HARD: 1, GOOD: 2, EASY: 3 };

export function blank() {
  return { s: 0, e: 2.5, iv: 0, due: 0, r: 0, l: 0, c: 0, w: 0, last: 0, seen: 0, t: 0 };
}

/**
 * Apply one answer to a card record and return the updated copy.
 * `grade` is a GRADE value; `now` is injectable for tests.
 */
export function review(card, grade, now = Date.now()) {
  const c = { ...blank(), ...(card || {}) };
  const ok = grade > GRADE.AGAIN;

  c.r += 1;
  c.last = now;
  c.t = now;
  if (!c.seen) c.seen = now;
  if (ok) c.c += 1; else { c.w += 1; c.l += 1; }

  // Ease drifts the SM-2 way but is floored so a hard word never becomes unlearnable.
  const delta = { 0: -0.22, 1: -0.14, 2: 0, 3: 0.1 }[grade] ?? 0;
  c.e = clamp(+(c.e + delta).toFixed(3), 1.3, 2.9);

  if (!ok) {
    // Back one stage, minimum "herkennen" once the word has been introduced.
    c.s = c.s >= STAGE_MASTERED ? 3 : Math.max(1, c.s - 1);
    c.iv = 0;
    c.due = now;                      // same-session re-ask, handled by the queue
    return c;
  }

  if (c.s < STAGE_MASTERED - 1) {
    // Still climbing the learning stages.
    c.s = Math.min(STAGE_MASTERED - 1, c.s + (grade === GRADE.EASY ? 2 : 1));
    const step = STEP_DAYS[Math.min(c.s, STEP_DAYS.length - 1)];
    c.iv = step;
    c.due = step === 0 ? now : dayStart(now) + step * DAY;
    if (c.s >= STAGE_MASTERED - 1 && c.iv === 0) { c.iv = 1; c.due = dayStart(now) + DAY; }
    return c;
  }

  // Graduated: classic SM-2 growth, damped by past lapses.
  const lapsePenalty = 1 / (1 + Math.min(c.l, 6) * 0.18);
  const factor = grade === GRADE.HARD ? 1.2 : grade === GRADE.EASY ? c.e * 1.3 : c.e;
  const base = c.iv > 0 ? c.iv : 1;
  c.iv = clamp(Math.round(base * factor * lapsePenalty), 1, 365);
  c.s = STAGE_MASTERED;
  c.due = dayStart(now) + c.iv * DAY;
  return c;
}

/** A card the learner has answered wrong more than it deserves. */
export function isDifficult(card) {
  if (!card || !card.r) return false;
  const acc = card.c / card.r;
  return card.l >= 2 || (card.r >= 3 && acc < 0.6) || card.e <= 1.75;
}

export const isMastered = (card) => !!card && card.s >= STAGE_MASTERED && card.iv >= 21;
export const isDue = (card, now = Date.now()) => !!card && card.r > 0 && card.due <= now;
export const isNew = (card) => !card || !card.r;

/**
 * Priority for the review queue. Higher comes first.
 * Overdue, lapse-prone and low-ease cards float to the top, which is what makes
 * "words you got wrong show up more often" true in practice.
 */
export function priority(card, now = Date.now()) {
  if (!card || !card.r) return 0;
  const overdueDays = Math.max(0, (now - card.due) / DAY);
  const lapses = Math.min(card.l, 8) * 1.6;
  const weakness = (2.9 - card.e) * 2.2;
  const staleness = Math.min(overdueDays, 30) * 0.9;
  const masteredDamp = isMastered(card) ? -3.5 : 0;
  return 4 + lapses + weakness + staleness + masteredDamp;
}

/** Human-readable retention estimate used on the word detail sheet. */
export function strength(card) {
  if (!card || !card.r) return 0;
  const stageScore = Math.min(card.s, STAGE_MASTERED) / STAGE_MASTERED;
  const accuracy = card.c / card.r;
  const spacing = Math.min(card.iv, 60) / 60;
  return clamp(Math.round((stageScore * 0.45 + accuracy * 0.35 + spacing * 0.2) * 100), 0, 100);
}
