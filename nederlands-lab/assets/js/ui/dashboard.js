/* Dashboard: where the learner lands, and where the next action is obvious. */

import { el, icon, ICONS, pct, relTime } from '../core/util.js';
import { store } from '../core/store.js';
import * as DATA from '../core/data.js';
import { startSession } from './session.js';
import { progressBar, emptyState, wordRow } from './components.js';
import { go } from '../main.js';

function tile(label, sub, iconName, tone, onClick) {
  return el('button.tile', { type: 'button', dataset: { tone: tone || '' }, onclick: onClick },
    el('span.tile-ico', { html: icon(ICONS[iconName] || ICONS.play, 18) }),
    el('strong', { text: label }),
    el('small', { text: sub }));
}

function statBox(value, label, tone) {
  return el('div.stat', { dataset: { tone: tone || '' } },
    el('b', { text: String(value) }), el('span', { text: label }));
}

function bookPanel(book) {
  const words = DATA.bookWords(book.id);
  const st = store.stats(words);
  const cur = DATA.currentLesson(book.id);
  const lessons = DATA.bookLessons(book.id);
  const lesson = DATA.lesson(book.id, cur);
  const c = DATA.counts(book.id);

  return el('section.card.book-card', {},
    el('div.book-head', {},
      el('div', {},
        el('h3', { text: book.name }),
        el('p', { text: `${book.note} · ${lessons.length} lessen · ${words.length} woorden` })),
      el(`span.chip.chip-${book.tone}`, { text: `${pct(st.learned, st.total)}%` })),
    progressBar(st.learned, st.total, book.tone),
    el('div.book-nums', {},
      el('div', {}, el('b', { text: String(st.learned) }), 'geleerd'),
      el('div', {}, el('b', { text: String(st.mastered) }), 'beheerst'),
      el('div', {}, el('b', { text: String(c.due) }), 'te herhalen'),
      el('div', {}, el('b', { text: String(st.difficult) }), 'moeilijk')),
    el('div.row.wrap', { style: { gap: '8px' } },
      el('button.btn.btn-sm.btn-primary', {
        type: 'button', html: `${icon(ICONS.spark, 15)} Les ${cur ?? '—'} leren`,
        onclick: () => cur != null && startSession('learn', { book: book.id, lesson: cur }),
      }),
      el('button.btn.btn-sm', {
        type: 'button', text: 'Alle lessen',
        onclick: () => go(`#/book/${book.id}`),
      })),
    lesson ? el('p.muted', { style: { fontSize: '.82rem' }, text: `Huidige les: ${lesson.title}` }) : null);
}

export function renderDashboard(view) {
  const books = DATA.db.books;
  if (!books.length) {
    return view.append(emptyState(
      'Geen woordenlijsten gevonden',
      'De databestanden konden niet geladen worden. Controleer de map data/ of ververs de pagina.',
      el('button.btn.btn-primary', { type: 'button', text: 'Opnieuw laden', onclick: () => location.reload() })));
  }

  const all = DATA.db.words;
  const st = store.stats(all);
  const today = store.todayStats();
  const c = DATA.counts(null);
  const lastBook = DATA.hasBook(store.meta.lastBook) ? store.meta.lastBook : DATA.defaultBook();
  const cur = DATA.currentLesson(lastBook);
  const curLesson = DATA.lesson(lastBook, cur);
  const bookName = DATA.db.books.find((b) => b.id === lastBook)?.short || '';

  /* hero: one obvious next action */
  const heroLine = c.due > 0
    ? `${c.due} ${c.due === 1 ? 'woord wacht' : 'woorden wachten'} op herhaling.`
    : store.meta.lastActivity
      ? `Alles herhaald. Ga verder met ${bookName} — les ${cur}.`
      : 'Begin bij les 1 en bouw je woordenschat op met de Delftse methode.';

  const hero = el('section.hero', {}, el('div.hero-body', {},
    el('span.hero-eyebrow', { text: store.meta.lastActivity ? `Laatst geoefend ${relTime(store.meta.lastActivity)}` : 'Welkom' }),
    el('h2', { text: curLesson ? `${bookName} · les ${cur} — ${curLesson.title}` : 'Nederlands Lab' }),
    el('p.hero-sub', { text: heroLine }),
    el('div.hero-actions', {},
      c.due > 0
        ? el('button.btn.btn-primary', { type: 'button', html: `${icon(ICONS.refresh, 16)} Herhalen (${c.due})`, onclick: () => startSession('review', {}) })
        : null,
      el('button.btn' + (c.due > 0 ? '' : '.btn-primary'), {
        type: 'button', html: `${icon(ICONS.spark, 16)} Verder leren`,
        onclick: () => startSession('learn', { book: lastBook, lesson: cur }),
      }),
      curLesson ? el('button.btn', { type: 'button', text: 'Bekijk de les', onclick: () => go(`#/lesson/${lastBook}/${cur}`) }) : null)));

  /* today + totals */
  const stats = el('div.stat-grid', {},
    statBox(c.due, 'te herhalen', c.due ? 'warn' : 'good'),
    statBox(st.learned, 'geleerd', 'accent'),
    statBox(st.mastered, 'beheerst', 'good'),
    statBox(st.answers ? `${st.accuracy}%` : '—', 'nauwkeurigheid',
      !st.answers ? '' : st.accuracy >= 75 ? 'good' : st.accuracy >= 50 ? 'warn' : 'bad'));

  const todayCard = el('section.card', {},
    el('div.section-title', { text: 'Vandaag' }),
    el('div.stat-grid', {},
      statBox(today.answers, 'beurten'),
      statBox(today.newWords, 'nieuwe woorden'),
      statBox(today.answers ? `${pct(today.correct, today.answers)}%` : '—', 'score vandaag',
        today.answers ? (pct(today.correct, today.answers) >= 70 ? 'good' : 'warn') : ''),
      statBox(store.meta.streak, 'dagen streak', store.meta.streak ? 'warn' : '')));

  /* practice modes */
  const modes = el('section', {},
    el('div.section-title', { text: 'Oefenen' }),
    el('div.tile-grid', {},
      tile('Leren', 'nieuwe woorden in fases', 'spark', 'accent', () => startSession('learn', { book: lastBook, lesson: cur })),
      tile('Herhalen', `${c.due} klaar voor vandaag`, 'refresh', '', () => startSession('review', {})),
      tile('Flashcards', 'zelf beoordelen', 'cards', '', () => startSession('flash', {})),
      tile('Meerkeuze', 'NL ↔ فارسی', 'list', '', () => startSession('mc', {})),
      tile('Typen', 'zelf produceren', 'pencil', '', () => startSession('type', {})),
      tile('Invullen', 'woord in een zin', 'gap', '', () => startSession('blank', {})),
      tile('Luisteren', 'uitspraak herkennen', 'ear', '', () => startSession('listen', {})),
      tile('Moeilijke woorden', `${c.hard} gemarkeerd`, 'flag', 'bad', () => startSession('hard', {})),
      tile('Favorieten', `${c.fav} bewaard`, 'star', 'warn', () => startSession('fav', {}))));

  /* per-book progress */
  const bookGrid = el('div.stack', {}, DATA.db.books.map(bookPanel));

  /* attention list */
  const weak = DATA.db.words
    .filter((w) => store.difficult(w.id))
    .sort((a, b) => (store.card(a.id)?.e || 3) - (store.card(b.id)?.e || 3))
    .slice(0, 6);
  const attention = weak.length
    ? el('section.card', {},
        el('div.row-between', { style: { marginBottom: '12px' } },
          el('div.section-title', { style: { marginBottom: 0 }, text: 'Vraagt aandacht' }),
          el('button.btn.btn-sm.btn-ghost', { type: 'button', text: 'Oefen deze', onclick: () => startSession('hard', {}) })),
        el('div.mini-list', {}, weak.map((w) => wordRow(w))))
    : null;

  view.append(el('div.stack', {}, hero, stats, todayCard, modes, bookGrid, attention));
}
