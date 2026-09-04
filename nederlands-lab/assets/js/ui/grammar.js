/* The grammar section: dashboard, curriculum map, lesson pages and reference.
 *
 * The dashboard answers one question — what should I do right now? — and only
 * then shows the map. The reference is deliberately kept apart from the course:
 * it is for looking something up, not for working through.
 */

import { el, icon, ICONS, pct, debounce, relTime } from '../core/util.js';
import { store } from '../core/store.js';
import * as G from '../core/grammar.js';
import * as DATA from '../core/data.js';
import { fa, emptyState, progressBar, speakButton, glossify } from './components.js';
import { startGrammar, patternBlock } from './grammar-session.js';
import { startSession } from './session.js';
import { go } from '../main.js';

const LEVEL_TONE = { A0: 'gb', A1: 'accent', A2: 'tr', B1: 'warn' };

function levelChip(level, extra = '') {
  return el(`span.chip.g-level.g-level-${level}`, { text: extra ? `${level} · ${extra}` : level });
}

function statBox(value, label, tone) {
  return el('div.stat', { dataset: { tone: tone || '' } },
    el('b', { text: String(value) }), el('span', { text: label }));
}

function notLoaded(view) {
  view.append(emptyState(
    'De grammaticacursus kon niet geladen worden',
    'Controleer de bestanden in de map data/ (grammar.a0.json … grammar.b1.json) of ververs de pagina.',
    el('button.btn.btn-primary', { type: 'button', text: 'Opnieuw laden', onclick: () => location.reload() })));
}

/* ---------- dashboard ---------- */

export function renderGrammar(view) {
  if (!G.loaded()) return notLoaded(view);

  const p = G.overallProgress();
  const next = G.nextLesson();
  const due = G.dueConcepts();
  const weak = G.weakConcepts(6);
  const today = store.gTodayCount();

  view.append(el('div.page-head', {},
    el('h1', { text: 'Grammatica' }),
    el('p', { text: p.started
      ? `${p.done} van ${p.lessons} lessen afgerond · ${p.conceptsMastered} onderwerpen beheerst`
      : 'Van absolute beginner (A0) tot zelfstandig (B1), in kleine stappen.' })));

  /* hero: the single next action */
  const heroLine = due.length
    ? `${due.length} grammaticapunt${due.length === 1 ? '' : 'en'} klaar om te herhalen.`
    : next
      ? (G.lessonState(next.id).started
          ? `Verder met les: ${next.title}`
          : `Volgende les: ${next.title}`)
      : 'Je hebt de hele cursus doorlopen. Herhaal om het vast te houden.';

  const mod = next ? G.moduleOf(next.id) : null;
  view.append(el('section.hero.g-hero', {}, el('div.hero-body', {},
    el('span.hero-eyebrow', {
      text: today.answers ? `Vandaag ${today.answers} antwoorden` : 'Grammatica',
    }),
    el('h2', { text: next ? next.title : 'Grammatica' }),
    next ? fa('p.g-hero-fa', next.titleFa || '') : null,
    el('p.hero-sub', { text: heroLine }),
    el('div.hero-actions', {},
      due.length
        ? el('button.btn.btn-primary', {
            type: 'button', html: `${icon(ICONS.refresh, 16)} Herhalen (${due.length})`,
            onclick: () => startGrammar('review', {}),
          })
        : null,
      next
        ? el('button.btn' + (due.length ? '' : '.btn-primary'), {
            type: 'button', html: `${icon(ICONS.spark, 16)} ${G.lessonState(next.id).started ? 'Verder leren' : 'Start les'}`,
            onclick: () => go(`#/grammar/lesson/${next.id}`),
          })
        : null,
      p.conceptsSeen
        ? el('button.btn', { type: 'button', text: 'Gemengde oefening', onclick: () => startGrammar('mixed', {}) })
        : null,
      mod ? el('button.btn', { type: 'button', text: mod.title, onclick: () => go(`#/grammar/module/${mod.id}`) }) : null))));

  /* headline numbers */
  view.append(el('div.stat-grid', {},
    statBox(p.done, 'lessen af', 'accent'),
    statBox(p.conceptsMastered, 'beheerst', 'good'),
    statBox(due.length, 'te herhalen', due.length ? 'warn' : 'good'),
    statBox(p.answers ? `${p.accuracy}%` : '—', 'nauwkeurigheid',
      !p.answers ? '' : p.accuracy >= 75 ? 'good' : p.accuracy >= 50 ? 'warn' : 'bad')));

  /* per level */
  const levels = el('section.card', {},
    el('div.section-title', { text: 'Niveaus' }),
    el('div.g-levels', {}, G.LEVELS.map((lv) => {
      const lp = G.levelProgress(lv.id);
      if (!lp.total) return null;
      return el('button.g-level-row', {
        type: 'button', onclick: () => go(`#/grammar/level/${lv.id}`),
      },
        el('span.g-level-badge', { dataset: { lv: lv.id }, text: lv.id }),
        el('div.grow', {},
          el('div.row-between', {},
            el('strong', { text: lv.name }),
            el('span.muted', { style: { fontSize: '.8rem' }, text: `${lp.done}/${lp.total}` })),
          progressBar(lp.done, lp.total, LEVEL_TONE[lv.id] === 'accent' ? '' : LEVEL_TONE[lv.id]),
          fa('small.g-level-fa', lv.fa)));
    }).filter(Boolean)));
  view.append(levels);

  /* weak topics — the honest bit */
  if (weak.length) {
    view.append(el('section.card', {},
      el('div.section-title', { text: 'Waar je nog moeite mee hebt' }),
      el('div.g-weak-list', {}, weak.map(({ concept, stats }) =>
        el('button.g-weak', { type: 'button', onclick: () => startGrammar('concept', { concept: concept.id }) },
          el('div.grow', {},
            el('div.row', { style: { gap: '8px' } },
              levelChip(concept.level),
              el('strong', { text: concept.title })),
            fa('small', concept.summaryFa || concept.titleFa || '')),
          el('span.chip.chip-bad', { text: `${stats.strength}%` }))))));
  }

  /* recently practised */
  const recent = G.recentConcepts(5);
  if (recent.length) {
    view.append(el('section.card', {},
      el('div.section-title', { text: 'Onlangs geoefend' }),
      el('div.g-recent', {}, recent.map(({ concept, stats, t }) =>
        el('div.g-recent-row', {},
          el('div.grow', {},
            el('strong', { text: concept.title }),
            el('small.muted', { style: { display: 'block' }, text: relTime(t) })),
          el('span.chip' + (stats.mastered ? '.chip-good' : ''), {
            text: stats.mastered ? 'beheerst' : `${stats.strength}%`,
          }))))));
  }

  /* curriculum map + reference */
  view.append(el('section.card', {},
    el('div.section-title', { text: 'Cursus' }),
    el('div.tile-grid', {},
      el('button.tile', { type: 'button', onclick: () => go('#/grammar/curriculum') },
        el('span.tile-ico', { html: icon(ICONS.list, 18) }),
        el('strong', { text: 'Leerroute' }),
        el('small', { text: `${G.gdb.modules.length} modules · ${p.lessons} lessen` })),
      el('button.tile', { type: 'button', dataset: { tone: 'tr' }, onclick: () => go('#/grammar/ref') },
        el('span.tile-ico', { html: icon(ICONS.book, 18) }),
        el('strong', { text: 'Naslag' }),
        el('small', { text: 'Zoek een regel op' })),
      el('button.tile', { type: 'button', dataset: { tone: 'warn' }, onclick: () => startGrammar('mixed', {}) },
        el('span.tile-ico', { html: icon(ICONS.cards, 18) }),
        el('strong', { text: 'Gemengd' }),
        el('small', { text: 'Alles door elkaar' })))));
}

/* ---------- curriculum map ---------- */

export function renderCurriculum(view, level = '') {
  if (!G.loaded()) return notLoaded(view);
  const levels = level ? G.LEVELS.filter((l) => l.id === level) : G.LEVELS;

  view.append(el('div.page-head', {},
    el('h1', { text: level ? `Grammatica ${level}` : 'Leerroute' }),
    el('p', { text: level
      ? (G.LEVELS.find((l) => l.id === level)?.name || '')
      : 'De hele weg van A0 naar B1. Werk van boven naar beneden.' })));

  for (const lv of levels) {
    const mods = G.levelModules(lv.id);
    if (!mods.length) continue;
    const lp = G.levelProgress(lv.id);

    view.append(el('section.card.g-level-card', {},
      el('div.row-between', {},
        el('div.row', { style: { gap: '10px' } },
          el('span.g-level-badge', { dataset: { lv: lv.id }, text: lv.id }),
          el('div', {}, el('strong', { text: lv.name }), fa('small.block', lv.fa))),
        el('span.chip', { text: `${lp.done}/${lp.total}` })),
      progressBar(lp.done, lp.total, LEVEL_TONE[lv.id] === 'accent' ? '' : LEVEL_TONE[lv.id]),
      el('div.g-modules', {}, mods.map((m) => moduleRow(m)))));
  }
}

function moduleRow(m) {
  const mp = G.moduleProgress(m.id);
  return el('button.g-module', { type: 'button', onclick: () => go(`#/grammar/module/${m.id}`) },
    el('span.g-module-ico', { html: icon(ICONS[m.icon] || ICONS.book, 17) }),
    el('div.grow', {},
      el('div.row-between', {},
        el('strong', { text: m.title }),
        el('span.muted', { style: { fontSize: '.78rem' }, text: `${mp.done}/${mp.total}` })),
      fa('small.g-module-fa', m.goalFa || m.titleFa || '')),
    mp.done === mp.total && mp.total
      ? el('span.chip.chip-good', { text: '✓' })
      : el('span.chip', { text: `${mp.pct}%` }));
}

/* ---------- module page ---------- */

export function renderGrammarModule(view, moduleId) {
  if (!G.loaded()) return notLoaded(view);
  const m = G.module_(moduleId);
  if (!m) return view.append(emptyState('Module niet gevonden', 'Ga terug naar de leerroute.',
    el('button.btn.btn-primary', { type: 'button', text: 'Leerroute', onclick: () => go('#/grammar/curriculum') })));

  const lessons = G.moduleLessons(m.id);
  const mp = G.moduleProgress(m.id);

  view.append(el('div.page-head', {},
    el('div.row', { style: { gap: '8px' } }, levelChip(m.level), el('span.muted', { text: m.titleFa })),
    el('h1', { text: m.title }),
    fa('p.g-goal', m.goalFa || '')));

  view.append(el('section.card', {},
    el('div.row-between', {},
      el('div.section-title', { text: 'Voortgang' }),
      el('span.chip', { text: `${mp.done}/${mp.total} lessen` })),
    progressBar(mp.done, mp.total, LEVEL_TONE[m.level] === 'accent' ? '' : LEVEL_TONE[m.level]),
    el('div.g-lesson-list', {}, lessons.map((l) => lessonRow(l)))));
}

function lessonRow(l) {
  const st = G.lessonState(l.id);
  const mark = st.mastered ? '★' : st.done ? '✓' : st.started ? '·' : '';
  return el('button.g-lesson', {
    type: 'button', dataset: { state: st.mastered ? 'mastered' : st.done ? 'done' : st.started ? 'started' : '' },
    onclick: () => go(`#/grammar/lesson/${l.id}`),
  },
    el('span.g-lesson-mark', { text: mark || '' }),
    el('div.grow', {},
      el('strong', { text: l.title }),
      fa('small.g-lesson-fa', l.titleFa || '')),
    st.due ? el('span.chip.chip-warn', { text: 'herhalen' })
      : st.done ? el('span.chip.chip-good', { text: `${st.best}%` })
      : el('span.chip', { text: `${(l.exercises || []).length} oef.` }));
}

/* ---------- lesson page ---------- */

export function renderGrammarLesson(view, lessonId) {
  if (!G.loaded()) return notLoaded(view);
  const l = G.lesson(lessonId);
  if (!l) return view.append(emptyState('Les niet gevonden', 'Ga terug naar de leerroute.',
    el('button.btn.btn-primary', { type: 'button', text: 'Leerroute', onclick: () => go('#/grammar/curriculum') })));

  const m = G.module_(l.module);
  const st = G.lessonState(l.id);
  const concepts = (l.concepts || []).map((id) => ({ c: G.concept(id), s: G.conceptStats(id) }));

  view.append(el('div.page-head', {},
    el('div.row.wrap', { style: { gap: '8px' } },
      levelChip(l.level),
      m ? el('button.chip.chip-btn', { type: 'button', text: m.title, onclick: () => go(`#/grammar/module/${m.id}`) }) : null),
    el('h1', { text: l.title }),
    fa('p.g-goal', l.titleFa || '')));

  /* what this lesson is about, in one line, then straight to the button */
  view.append(el('section.card.g-start-card', {},
    el('div.g-rule', {},
      el('div.g-rule-nl', { lang: 'nl', text: l.rule?.nl || '' }),
      fa('div.g-rule-fa', l.rule?.fa || '')),
    el('div.hero-actions', {},
      el('button.btn.btn-primary', {
        type: 'button', html: `${icon(ICONS.play, 16)} ${st.started ? 'Opnieuw oefenen' : 'Start de les'}`,
        onclick: () => startGrammar('lesson', { lesson: l.id }),
      }),
      st.started ? el('button.btn', {
        type: 'button', text: 'Alleen de uitleg', onclick: () => go(`#/grammar/ref/${l.id}`),
      }) : null),
    st.tries ? el('p.muted', { style: { fontSize: '.82rem' },
      text: st.done
        ? `Afgerond · beste score ${st.best}%${st.mastered ? ' · beheerst' : ''}`
        : `${st.tries} poging${st.tries === 1 ? '' : 'en'} · beste score ${st.best}% (${G.PASS_MARK}% nodig)`,
    }) : null));

  /* the concepts this lesson is scored on */
  view.append(el('section.card', {},
    el('div.section-title', { text: 'Wat je hier leert' }),
    el('div.g-concept-list', {}, concepts.map(({ c, s }) => c ? el('div.g-concept-row', {},
      el('div.grow', {},
        el('strong', { text: c.title }),
        fa('small.block', c.summaryFa || c.titleFa || '')),
      el('div.bar.g-bar', {}, el('i', { style: { width: `${s.strength}%` } })),
      el('span.chip' + (s.mastered ? '.chip-good' : ''), {
        text: s.mastered ? 'beheerst' : s.seen ? `${s.strength}%` : 'nieuw',
      })) : null))));

  /* the bridge to the vocabulary trainer */
  const words = matchingWords(l);
  if (words.length >= 4) {
    view.append(el('section.card', {},
      el('div.row-between', {},
        el('div.section-title', { text: 'Woorden uit deze les' }),
        el('button.btn.btn-sm', {
          type: 'button', text: `Oefen ${words.length} woorden`,
          onclick: () => startSession('lesson', { pool: words, size: Math.min(words.length, 20) }),
        })),
      el('div.row.wrap', { style: { gap: '6px' } }, words.slice(0, 14).map((w) =>
        el('span.chip', { lang: 'nl', title: w.fa || '', text: w.term })))));
  }
}

/**
 * Dutch words used in this lesson that the vocabulary trainer already knows —
 * this is what makes grammar and vocabulary reinforce each other instead of
 * being two separate apps.
 */
function matchingWords(l) {
  const used = G.lessonVocabulary(l);
  const out = [];
  const seen = new Set();
  for (const w of DATA.db.words) {
    const key = String(w.term || '').toLowerCase();
    if (!used.has(key) || seen.has(key)) continue;
    seen.add(key);
    out.push(w);
    if (out.length >= 40) break;
  }
  return out;
}

/* ---------- reference ---------- */

export function renderGrammarReference(view, params) {
  if (!G.loaded()) return notLoaded(view);

  view.append(el('div.page-head', {},
    el('h1', { text: 'Naslag' }),
    el('p', { text: 'Zoek een regel op — bijvoorbeeld “niet geen”, “woordvolgorde”, “om te”, “er” of “perfectum”.' })));

  const results = el('div.g-ref-results');
  const input = el('input.input.g-search', {
    type: 'search', placeholder: 'Zoek een grammaticaregel…', 'aria-label': 'Zoek in de naslag',
    value: params?.get('q') || '',
  });

  const paint = (q) => {
    const hits = q.trim() ? G.searchReference(q) : [];
    results.replaceChildren();
    if (!q.trim()) {
      results.append(el('div.g-ref-hint', {},
        el('div.section-title', { text: 'Veelgezocht' }),
        el('div.row.wrap', { style: { gap: '6px' } },
          ['niet geen', 'woordvolgorde', 'om te', 'er', 'perfectum', 'de het', 'bijzin', 'zou'].map((t) =>
            el('button.chip.chip-btn', {
              type: 'button', text: t,
              onclick: () => { input.value = t; paint(t); },
            })))));
      return;
    }
    if (!hits.length) {
      results.append(el('p.muted', { text: `Niets gevonden voor “${q}”.` }));
      return;
    }
    results.append(el('p.muted', { style: { fontSize: '.82rem' }, text: `${hits.length} resultaten` }));
    for (const l of hits.slice(0, 25)) results.append(refRow(l));
  };

  const onInput = debounce(() => paint(input.value), 160);
  input.addEventListener('input', onInput);

  view.append(el('section.card', {}, input, results));
  paint(input.value);
}

function refRow(l) {
  return el('button.g-ref-row', { type: 'button', onclick: () => go(`#/grammar/ref/${l.id}`) },
    levelChip(l.level),
    el('div.grow', {},
      el('strong', { text: l.title }),
      el('div.g-ref-rule', { lang: 'nl', text: l.rule?.nl || '' }),
      fa('small.g-ref-fa', l.rule?.fa || '')),
    el('span.g-ref-arrow', { html: icon(ICONS.arrow, 15) }));
}

/** One rule, fully written out — the "look it up" view, with no exercises. */
export function renderGrammarRefLesson(view, lessonId) {
  if (!G.loaded()) return notLoaded(view);
  const l = G.lesson(lessonId);
  if (!l) return view.append(emptyState('Niet gevonden', 'Deze regel bestaat niet.',
    el('button.btn.btn-primary', { type: 'button', text: 'Naslag', onclick: () => go('#/grammar/ref') })));

  view.append(el('div.page-head', {},
    el('div.row.wrap', { style: { gap: '8px' } },
      levelChip(l.level),
      el('button.chip.chip-btn', { type: 'button', text: 'Naslag', onclick: () => go('#/grammar/ref') })),
    el('h1', { text: l.title }),
    fa('p.g-goal', l.titleFa || '')));

  view.append(el('section.card', {},
    el('div.g-rule', {},
      el('div.g-rule-nl', { lang: 'nl', text: l.rule?.nl || '' }),
      fa('div.g-rule-fa', l.rule?.fa || ''),
      l.rule?.en ? el('div.g-rule-en', { text: l.rule.en }) : null),
    l.pattern ? patternBlock(l.pattern) : null));

  if (l.examples?.length) {
    view.append(el('section.card', {},
      el('div.section-title', { text: 'Voorbeelden' }),
      el('div.g-examples', {}, l.examples.map((e) =>
        el('div.g-example', {},
          el('div.row', { style: { gap: '8px', alignItems: 'flex-start' } },
            el('div.g-ex-nl.grow', { lang: 'nl' }, glossify(e.nl, null)),
            speakButton(e.nl)),
          fa('div.g-ex-fa', e.fa || ''),
          e.note ? fa('div.g-ex-note', e.note) : null)))));
  }

  if (l.contrast?.length) {
    view.append(el('section.card', {},
      el('div.section-title', { text: 'Veelgemaakte fouten' }),
      el('div.g-contrasts', {}, l.contrast.map((c) =>
        el('div.g-contrast', {},
          el('div.g-bad', {}, el('span.g-mark', { text: '✕' }), el('span', { lang: 'nl', text: c.bad })),
          el('div.g-good', {}, el('span.g-mark', { text: '✓' }), el('span', { lang: 'nl', text: c.good })),
          fa('div.g-why', c.fa || ''))))));
  }

  if (l.usage) {
    view.append(el('section.card', {},
      el('div.section-title', { text: 'Wanneer gebruik je dit?' }),
      fa('p.g-usage-text', l.usage)));
  }

  view.append(el('section.card', {},
    el('div.hero-actions', {},
      el('button.btn.btn-primary', {
        type: 'button', html: `${icon(ICONS.play, 16)} Oefen deze regel`,
        onclick: () => startGrammar('lesson', { lesson: l.id }),
      }),
      el('button.btn', {
        type: 'button', text: 'Naar de les', onclick: () => go(`#/grammar/lesson/${l.id}`),
      }))));
}

/* ---------- stats block, reused by the Voortgang page ---------- */

export function grammarStatsCard() {
  if (!G.loaded()) return null;
  const p = G.overallProgress();
  if (!p.answers && !p.started) return null;

  return el('section.card', {},
    el('div.row-between', {},
      el('div.section-title', { text: 'Grammatica' }),
      el('button.btn.btn-sm.btn-ghost', { type: 'button', text: 'Openen', onclick: () => go('#/grammar') })),
    el('div.stat-grid', {},
      statBox(p.done, 'lessen af', 'accent'),
      statBox(p.conceptsMastered, 'beheerst', 'good'),
      statBox(p.due, 'te herhalen', p.due ? 'warn' : 'good'),
      statBox(p.answers ? `${p.accuracy}%` : '—', 'nauwkeurigheid')),
    el('div.g-levels-mini', {}, G.LEVELS.map((lv) => {
      const lp = G.levelProgress(lv.id);
      if (!lp.total) return null;
      return el('div.g-mini-row', {},
        el('span.g-level-badge.small', { dataset: { lv: lv.id }, text: lv.id }),
        el('div.bar.grow', {}, el('i', { style: { width: `${pct(lp.done, lp.total)}%` } })),
        el('span.muted', { style: { fontSize: '.75rem' }, text: `${lp.done}/${lp.total}` }));
    }).filter(Boolean)));
}
