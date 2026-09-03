/* Books, lesson lists and the lesson view.
 *
 * The lesson view is the Delftse methode in app form: read the text first with
 * the word list one tap away, then drill the words of that lesson.
 */

import { el, icon, ICONS, pct } from '../core/util.js';
import { store } from '../core/store.js';
import * as SRS from '../core/srs.js';
import * as DATA from '../core/data.js';
import { startSession } from './session.js';
import { progressBar, wordRow, emptyState, glossify, speakButton } from './components.js';
import { go } from '../main.js';

export function renderBooks(view) {
  const books = DATA.db.books;
  if (!books.length) {
    return view.append(emptyState('Geen boeken geladen', 'Controleer de databestanden in de map data/.'));
  }
  view.append(el('div.page-head', {}, el('h1', { text: 'Lessen' }),
    el('p', { text: 'Kies een boek en een les. Beide boeken volgen dezelfde methode.' })));

  const cards = books.map((b) => {
    const words = DATA.bookWords(b.id);
    const st = store.stats(words);
    const lessons = DATA.bookLessons(b.id);
    return el('section.card.book-card', {},
      el('div.book-head', {},
        el('div', {}, el('h3', { text: b.name }), el('p', { text: b.note })),
        el(`span.chip.chip-${b.tone}`, { text: `${lessons.length} lessen` })),
      progressBar(st.learned, st.total, b.tone),
      el('div.book-nums', {},
        el('div', {}, el('b', { text: `${st.learned}/${st.total}` }), 'geleerd'),
        el('div', {}, el('b', { text: String(st.mastered) }), 'beheerst'),
        el('div', {}, el('b', { text: String(DATA.counts(b.id).due) }), 'te herhalen')),
      el('button.btn.btn-primary.btn-block', {
        type: 'button', text: `Open ${b.short}`, onclick: () => go(`#/book/${b.id}`),
      }));
  });
  view.append(el('div.stack', {}, cards));
}

export function renderBook(view, bookId) {
  const book = DATA.db.books.find((b) => b.id === bookId);
  if (!book) return view.append(emptyState('Boek niet gevonden', 'Dit boek is niet geladen.'));

  const lessons = DATA.bookLessons(bookId);
  const cur = DATA.currentLesson(bookId);
  const st = store.stats(DATA.bookWords(bookId));

  view.append(el('div.page-head', {},
    el('h1', { text: book.name }),
    el('p', { text: `${book.note} · ${lessons.length} lessen · ${st.total} woorden · ${pct(st.learned, st.total)}% geleerd` })));

  view.append(el('div.row.wrap', { style: { marginBottom: '18px', gap: '8px' } },
    el('button.btn.btn-primary', {
      type: 'button', html: `${icon(ICONS.spark, 16)} Verder bij les ${cur}`,
      onclick: () => startSession('learn', { book: bookId, lesson: cur }),
    }),
    el('button.btn', { type: 'button', html: `${icon(ICONS.refresh, 16)} Herhalen`, onclick: () => startSession('review', { book: bookId }) }),
    el('button.btn', { type: 'button', text: 'Woorden zoeken', onclick: () => go(`#/browse?book=${bookId}`) })));

  const grid = el('div.lesson-grid', {}, lessons.map((l) => {
    const p = DATA.lessonProgress(bookId, l.n);
    const done = p.total > 0 && p.seen === p.total;
    return el('button.lesson-card', {
      type: 'button', dataset: { done: done ? '1' : '0' },
      onclick: () => go(`#/lesson/${bookId}/${l.n}`),
    },
      el('span.num', { text: `LES ${l.n}${l.n === cur ? ' · nu' : ''}` }),
      el('h4', { lang: 'nl', text: l.title }),
      progressBar(p.seen, p.total, book.tone),
      el('span.foot', {},
        el('span', { text: `${p.seen}/${p.total} woorden` }),
        el('span', { text: p.mastered ? `${p.mastered} beheerst` : '' })));
  }));
  view.append(grid);
}

export function renderLesson(view, bookId, n) {
  const book = DATA.db.books.find((b) => b.id === bookId);
  const lesson = DATA.lesson(bookId, n);
  if (!book || !lesson) return view.append(emptyState('Les niet gevonden', 'Deze les bestaat niet in dit boek.'));

  const words = DATA.lessonWords(bookId, n);
  const p = DATA.lessonProgress(bookId, n);
  store.setPosition(bookId, n);

  view.append(el('div.page-head', {},
    el('div.row', { style: { gap: '8px' } },
      el(`span.chip.chip-${book.tone}`, { text: book.short }),
      el('span.chip', { text: `les ${n}` }),
      lesson.page ? el('span.chip', { text: `p. ${lesson.page}` }) : null),
    el('h1', { lang: 'nl', text: lesson.title }),
    el('p', { text: `${words.length} woorden · ${p.seen} geoefend · ${p.mastered} beheerst` })));

  view.append(el('div.row.wrap', { style: { marginBottom: '18px', gap: '8px' } },
    el('button.btn.btn-primary', {
      type: 'button', html: `${icon(ICONS.spark, 16)} Leer deze les`,
      onclick: () => startSession('learn', { book: bookId, lesson: n }),
    }),
    el('button.btn', { type: 'button', html: `${icon(ICONS.cards, 16)} Oefen alles`, onclick: () => startSession('lesson', { book: bookId, lesson: n, size: Math.min(words.length, 40) }) }),
    el('button.btn', { type: 'button', html: `${icon(ICONS.gap, 16)} Invullen`, onclick: () => startSession('blank', { book: bookId, lesson: n }) })));

  /* tabs: text / words / exercises from the book */
  const hasText = (lesson.text || []).length > 0;
  const hasCloze = (lesson.cloze || []).length > 0;
  const panel = el('div');
  const tabDefs = [
    hasText ? ['tekst', 'Tekst'] : null,
    ['woorden', `Woorden (${words.length})`],
    hasCloze ? ['gaten', 'Gatentekst'] : null,
  ].filter(Boolean);

  const tabs = el('div.tabs', { role: 'tablist', style: { marginBottom: '16px' } });
  const paint = (key) => {
    for (const btn of tabs.children) btn.setAttribute('aria-selected', String(btn.dataset.k === key));
    if (key === 'tekst') renderText(panel, lesson);
    else if (key === 'gaten') renderCloze(panel, lesson);
    else renderWords(panel, words, bookId, n);
  };
  for (const [k, label] of tabDefs) {
    tabs.append(el('button', { type: 'button', role: 'tab', dataset: { k }, text: label, onclick: () => paint(k) }));
  }
  view.append(tabs, panel);
  paint(tabDefs[0][0]);

  /* neighbouring lessons */
  const lessons = DATA.bookLessons(bookId);
  const idx = lessons.findIndex((l) => l.n === n);
  const nav = el('div.row-between', { style: { marginTop: '26px', gap: '8px' } },
    idx > 0 ? el('button.btn.btn-sm', { type: 'button', text: `← Les ${lessons[idx - 1].n}`, onclick: () => go(`#/lesson/${bookId}/${lessons[idx - 1].n}`) }) : el('span'),
    idx < lessons.length - 1 ? el('button.btn.btn-sm', { type: 'button', text: `Les ${lessons[idx + 1].n} →`, onclick: () => go(`#/lesson/${bookId}/${lessons[idx + 1].n}`) }) : el('span'));
  view.append(nav);
}

/** The book text, with every known word tappable for its Persian meaning. */
function renderText(panel, lesson) {
  panel.replaceChildren();
  const body = el('div.reading');
  for (const para of lesson.text) {
    const p = el('p', { lang: 'nl' });
    p.append(glossify(para, null));
    body.append(p);
  }
  panel.append(
    el('div.callout.callout-info', { text: 'Tik op een woord voor de Perzische betekenis. Lees de tekst eerst helemaal door — dat is de kern van de Delftse methode.' }),
    el('section.card', { style: { marginTop: '14px' } }, body,
      el('div.row', { style: { marginTop: '16px' } },
        speakButton(lesson.text.join(' ').slice(0, 600)) || el('span'),
        el('span.muted', { style: { fontSize: '.8rem' }, text: 'Luister naar het begin van de tekst' }))));
}

/** The book's own gap-fill passage. */
function renderCloze(panel, lesson) {
  panel.replaceChildren();
  const body = el('div.reading');
  for (const para of lesson.cloze) {
    const p = el('p', { lang: 'nl' });
    p.append(glossify(para.replace(/_{3,}/g, ' ⎯⎯ '), null));
    body.append(p);
  }
  panel.append(
    el('div.callout.callout-warn', { text: 'De gatentekst uit het boek. Probeer hem hardop aan te vullen; de woorden staan in de woordenlijst van deze les.' }),
    el('section.card', { style: { marginTop: '14px' } }, body));
}

function renderWords(panel, words, bookId, n) {
  panel.replaceChildren();
  const groups = [
    ['Te herhalen', words.filter((w) => SRS.isDue(store.card(w.id)))],
    ['Bezig', words.filter((w) => { const c = store.card(w.id); return c && c.r && !SRS.isDue(c) && !SRS.isMastered(c); })],
    ['Nieuw', words.filter((w) => SRS.isNew(store.card(w.id)))],
    ['Beheerst', words.filter((w) => SRS.isMastered(store.card(w.id)))],
  ].filter(([, list]) => list.length);

  for (const [title, list] of groups) {
    panel.append(el('section', { style: { marginBottom: '20px' } },
      el('div.section-title', { text: `${title} · ${list.length}` }),
      el('div.mini-list', {}, list.map((w) => wordRow(w)))));
  }
  if (!groups.length) panel.append(emptyState('Geen woorden', 'Deze les heeft nog geen woordenlijst.'));
}
