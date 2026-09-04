/* Progress view: totals, accuracy, streak, activity and per-book breakdown. */

import { el, pct, dayKey, relTime } from '../core/util.js';
import { store } from '../core/store.js';
import * as SRS from '../core/srs.js';
import * as DATA from '../core/data.js';
import { progressBar, wordRow, emptyState } from './components.js';
import { startSession } from './session.js';
import { grammarStatsCard } from './grammar.js';

function donut(value, label) {
  const d = el('div.donut', {}, el('span', { text: `${value}%` }));
  d.style.setProperty('--p', String(value));
  return el('div.row', { style: { gap: '18px' } }, d,
    el('div', {}, el('div.section-title', { style: { marginBottom: '4px' }, text: label })));
}

function heatmap() {
  const days = store.history(91);
  const max = Math.max(10, ...days.map((d) => d.answers));
  const grid = el('div.heat', { role: 'img', 'aria-label': 'Activiteit van de laatste 13 weken' });
  for (const d of days) {
    const level = d.answers === 0 ? 0 : Math.min(4, Math.ceil((d.answers / max) * 4));
    grid.append(el('i', { dataset: { l: String(level) }, title: `${dayKey(d.ts)}: ${d.answers} beurten` }));
  }
  return grid;
}

export function renderStats(view) {
  const all = DATA.db.words;
  if (!all.length) return view.append(emptyState('Nog geen data', 'De woordenlijsten zijn niet geladen.'));

  const st = store.stats(all);
  const today = store.todayStats();

  view.append(el('div.page-head', {},
    el('h1', { text: 'Voortgang' }),
    el('p', { text: store.meta.lastActivity ? `Laatste activiteit ${relTime(store.meta.lastActivity)}` : 'Nog geen sessies afgerond.' })));

  const top = el('div.stat-grid', {},
    el('div.stat', { dataset: { tone: 'accent' } }, el('b', { text: String(st.learned) }), el('span', { text: 'woorden geleerd' })),
    el('div.stat', { dataset: { tone: 'good' } }, el('b', { text: String(st.mastered) }), el('span', { text: 'beheerst' })),
    el('div.stat', { dataset: { tone: 'bad' } }, el('b', { text: String(st.difficult) }), el('span', { text: 'moeilijk' })),
    el('div.stat', { dataset: { tone: 'warn' } }, el('b', { text: String(st.streak) }), el('span', { text: 'dagen streak' })));

  const accuracy = el('section.card', {},
    el('div.section-title', { text: 'Nauwkeurigheid' }),
    el('div.row.wrap', { style: { gap: '24px', alignItems: 'center' } },
      donut(st.accuracy, `${st.correct} van ${st.answers} beurten goed`),
      el('div.grow', {},
        el('div.kv', {}, el('span.kv-k', { text: 'Vandaag' }), el('span.kv-v', { text: `${today.correct}/${today.answers} · ${pct(today.correct, today.answers)}%` })),
        el('div.kv', {}, el('span.kv-k', { text: 'Nieuwe woorden vandaag' }), el('span.kv-v', { text: String(today.newWords) })),
        el('div.kv', {}, el('span.kv-k', { text: 'Studietijd vandaag' }), el('span.kv-v', { text: `${today.minutes} min` })),
        el('div.kv', {}, el('span.kv-k', { text: 'Langste streak' }), el('span.kv-v', { text: `${st.bestStreak} dagen` })))));

  const activity = el('section.card', {},
    el('div.section-title', { text: 'Activiteit — laatste 13 weken' }),
    heatmap());

  const books = el('div.stack', {}, DATA.db.books.map((b) => {
    const words = DATA.bookWords(b.id);
    const s = store.stats(words);
    const c = DATA.counts(b.id);
    return el('section.card', {},
      el('div.row-between', { style: { marginBottom: '10px' } },
        el('div.section-title', { style: { marginBottom: 0 }, text: b.name }),
        el(`span.chip.chip-${b.tone}`, { text: `${pct(s.learned, s.total)}%` })),
      progressBar(s.learned, s.total, b.tone),
      el('div.book-nums', { style: { marginTop: '12px' } },
        el('div', {}, el('b', { text: `${s.learned}/${s.total}` }), 'geleerd'),
        el('div', {}, el('b', { text: String(s.mastered) }), 'beheerst'),
        el('div', {}, el('b', { text: String(c.due) }), 'te herhalen'),
        el('div', {}, el('b', { text: String(s.fresh) }), 'nog nieuw')));
  }));

  /* upcoming reviews */
  const buckets = new Map();
  for (const w of all) {
    const c = store.card(w.id);
    if (!c || !c.r) continue;
    const k = Math.max(0, Math.round((c.due - Date.now()) / 86400000));
    if (k > 30) continue;
    buckets.set(k, (buckets.get(k) || 0) + 1);
  }
  const upcoming = [...buckets.entries()].sort((a, b) => a[0] - b[0]).slice(0, 8);
  const schedule = upcoming.length
    ? el('section.card', {},
        el('div.section-title', { text: 'Herhalingen komende dagen' }),
        upcoming.map(([d, n]) => el('div.kv', {},
          el('span.kv-k', { text: d === 0 ? 'Nu' : d === 1 ? 'Morgen' : `Over ${d} dagen` }),
          el('span.kv-v', { text: `${n} ${n === 1 ? 'woord' : 'woorden'}` }))))
    : null;

  const hard = all.filter((w) => store.difficult(w.id))
    .sort((a, b) => (store.card(a.id)?.e || 3) - (store.card(b.id)?.e || 3)).slice(0, 12);
  const hardCard = hard.length
    ? el('section.card', {},
        el('div.row-between', { style: { marginBottom: '12px' } },
          el('div.section-title', { style: { marginBottom: 0 }, text: `Moeilijke woorden · ${hard.length}` }),
          el('button.btn.btn-sm.btn-primary', { type: 'button', text: 'Oefen deze', onclick: () => startSession('hard', {}) })),
        el('div.mini-list', {}, hard.map((w) => wordRow(w))))
    : null;

  view.append(el('div.stack', {}, top, accuracy, activity, books, grammarStatsCard(), schedule, hardCard));
}
