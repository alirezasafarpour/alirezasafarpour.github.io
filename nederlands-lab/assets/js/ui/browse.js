/* Vocabulary search with filters, in Dutch, English and Persian. */

import { el, icon, ICONS, debounce, clear } from '../core/util.js';
import * as DATA from '../core/data.js';
import { startSession } from './session.js';
import { wordRow, emptyState } from './components.js';

const STATUS_FILTERS = [
  ['', 'Alles'],
  ['due', 'Te herhalen'],
  ['new', 'Nieuw'],
  ['learning', 'Bezig'],
  ['difficult', 'Moeilijk'],
  ['favorite', 'Favoriet'],
  ['mastered', 'Beheerst'],
];

const PAGE = 60;

export function renderBrowse(view, params) {
  const state = {
    q: params.get('q') || '',
    book: params.get('book') || '',
    lesson: params.get('lesson') ? Number(params.get('lesson')) : null,
    status: params.get('status') || '',
    cefr: '',
    limit: PAGE,
  };

  view.append(el('div.page-head', {},
    el('h1', { text: 'Woorden' }),
    el('p', { text: 'Zoek in het Nederlands, Engels of Perzisch. Tik op een woord voor betekenis en voorbeelden.' })));

  /* search box */
  const input = el('input.input', {
    type: 'search', value: state.q, placeholder: 'zoek een woord, betekenis of معنی…',
    'aria-label': 'Zoeken', autocomplete: 'off',
  });
  const clearBtn = el('button.search-clear', { type: 'button', 'aria-label': 'Wissen', html: icon(ICONS.x, 15) });
  const searchWrap = el('div.search-wrap', {
    html: `<svg viewBox="0 0 24 24" fill="none" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>`,
  });
  searchWrap.append(input, clearBtn);

  /* filters */
  const bookRow = el('div.filter-row');
  const statusRow = el('div.filter-row');
  const results = el('div.mini-list');
  const meta = el('p.result-meta');
  const more = el('button.btn.btn-block', { type: 'button', text: 'Meer laden' });

  const paintFilters = () => {
    clear(bookRow); clear(statusRow);
    const books = [['', 'Beide boeken'], ...DATA.db.books.map((b) => [b.id, b.short])];
    for (const [id, label] of books) {
      bookRow.append(el('button.chip.chip-btn', {
        type: 'button', text: label, 'aria-pressed': String(state.book === id),
        onclick: () => { state.book = id; state.lesson = null; state.limit = PAGE; run(); },
      }));
    }
    if (state.book) {
      const lessons = DATA.bookLessons(state.book);
      const sel = el('select.select', { style: { maxWidth: '220px' }, 'aria-label': 'Les' },
        el('option', { value: '', text: 'Alle lessen' }),
        lessons.map((l) => el('option', { value: String(l.n), text: `Les ${l.n} — ${l.title}`, selected: state.lesson === l.n })));
      sel.addEventListener('change', () => { state.lesson = sel.value ? Number(sel.value) : null; state.limit = PAGE; run(); });
      bookRow.append(sel);
    }
    for (const [id, label] of STATUS_FILTERS) {
      statusRow.append(el('button.chip.chip-btn', {
        type: 'button', text: label, 'aria-pressed': String(state.status === id),
        onclick: () => { state.status = id; state.limit = PAGE; run(); },
      }));
    }
  };

  const run = () => {
    paintFilters();
    const hits = DATA.search(state.q, { book: state.book, lesson: state.lesson, status: state.status });
    meta.textContent = hits.length
      ? `${hits.length} ${hits.length === 1 ? 'woord' : 'woorden'}${state.q ? ` voor “${state.q}”` : ''}`
      : '';
    clear(results);
    if (!hits.length) {
      results.append(emptyState('Niets gevonden', 'Probeer een ander woord of zet een filter uit.'));
      more.hidden = true;
    } else {
      for (const w of hits.slice(0, state.limit)) results.append(wordRow(w));
      more.hidden = hits.length <= state.limit;
      more.onclick = () => { state.limit += PAGE; run(); };
    }
    practiceBtn.hidden = hits.length < 4;
    practiceBtn.onclick = () => startSession('lesson', {
      book: state.book || null,
      lesson: state.lesson,
      size: Math.min(hits.length, 30),
      pool: hits,
    });
    const url = new URL(location.href);
    url.hash = `#/browse?${new URLSearchParams(Object.fromEntries(
      Object.entries({ q: state.q, book: state.book, status: state.status, lesson: state.lesson ?? '' })
        .filter(([, v]) => v !== '' && v != null))).toString()}`;
    history.replaceState(null, '', url);
  };

  const practiceBtn = el('button.btn.btn-primary.btn-sm', { type: 'button', html: `${icon(ICONS.play, 15)} Oefen deze selectie` });

  input.addEventListener('input', debounce(() => { state.q = input.value; state.limit = PAGE; run(); }, 180));
  clearBtn.addEventListener('click', () => { input.value = ''; state.q = ''; state.limit = PAGE; run(); input.focus(); });

  view.append(el('div.stack', { style: { gap: '14px' } },
    searchWrap, bookRow, statusRow,
    el('div.row-between', {}, meta, practiceBtn),
    results, more));
  run();
}
