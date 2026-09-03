/* Shared UI pieces: sheets, word cards, example blocks, gloss popovers. */

import { el, mount, clear, icon, ICONS, splitTokens, splitBidi, dueLabel, pct } from '../core/util.js';
import { store } from '../core/store.js';
import * as SRS from '../core/srs.js';
import { glossFor, termRanges, BOOKS } from '../core/data.js';
import * as audio from '../core/audio.js';

/* ---------- sheets ---------- */

let activeSheet = null;

export function closeSheet() {
  const root = document.getElementById('sheetRoot');
  if (!root || root.hidden) return;
  root.hidden = true;
  clear(root);
  activeSheet = null;
  document.body.style.overflow = '';
}

export function openSheet(build, opts = {}) {
  const root = document.getElementById('sheetRoot');
  if (!root) return;
  const scrim = el('div.sheet-scrim', { onclick: closeSheet });
  const panel = el('div.sheet', { role: 'dialog', 'aria-modal': 'true', 'aria-label': opts.label || 'Details' },
    el('div.sheet-grip'));
  const body = typeof build === 'function' ? build(closeSheet) : build;
  panel.append(body);
  mount(root, scrim, panel);
  root.hidden = false;
  document.body.style.overflow = 'hidden';
  activeSheet = panel;
  panel.focus?.();
}

addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && activeSheet) { e.preventDefault(); closeSheet(); }
});

/* ---------- gloss popover ---------- */

let glossNode = null;
function hideGloss() { glossNode?.remove(); glossNode = null; document.querySelectorAll('.tok.on').forEach((n) => n.classList.remove('on')); }
addEventListener('pointerdown', (e) => { if (!e.target.closest?.('.tok')) hideGloss(); }, true);
addEventListener('scroll', hideGloss, true);

function showGloss(target, entry) {
  hideGloss();
  target.classList.add('on');
  const node = el('div.gloss-pop', {}, el('b', { text: entry.term }), faText(entry.fa || '—'));
  document.body.append(node);
  const r = target.getBoundingClientRect();
  const w = node.offsetWidth, h = node.offsetHeight;
  let left = r.left + r.width / 2 - w / 2;
  left = Math.max(8, Math.min(left, innerWidth - w - 8));
  let top = r.top - h - 8;
  if (top < 8) top = r.bottom + 8;
  node.style.left = `${left}px`;
  node.style.top = `${top}px`;
  glossNode = node;
}

/**
 * Render a Dutch sentence with the headword highlighted and every known word
 * tappable for its Persian meaning. This is what gives every example sentence
 * Persian support, whether or not it has a full authored translation.
 */
export function glossify(sentence, term, { gloss = true } = {}) {
  const frag = document.createDocumentFragment();
  const ranges = term ? termRanges(sentence, term) : [];
  const inTerm = (i) => ranges.some(([a, b]) => i >= a && i < b);

  let offset = 0;
  for (const [chunk, isWord] of splitTokens(sentence)) {
    const start = offset;
    offset += chunk.length;
    if (!isWord) { frag.append(document.createTextNode(chunk)); continue; }

    const highlighted = inTerm(start);
    const entry = gloss ? glossFor(chunk) : null;
    const node = el(highlighted ? 'mark' : 'span', {
      class: 'tok',
      dataset: { known: entry ? '1' : '0' },
      text: chunk,
    });
    if (entry) {
      node.title = entry.fa || '';
      node.addEventListener('click', (e) => { e.stopPropagation(); showGloss(node, entry); });
    }
    frag.append(node);
  }
  return frag;
}

/**
 * One line of a lesson text. The book italicises words that are new in this
 * lesson and marks them with asterisks in the source; those become <em> here,
 * and everything stays tappable for its Persian meaning.
 */
export function readingLine(text, { gloss = true } = {}) {
  const frag = document.createDocumentFragment();
  const raw = String(text ?? '');
  // A leading > or » is the book's speaker marker for the two voices.
  const speaker = /^\s*[>›»]/.test(raw) ? raw.trim()[0] : '';
  const body = speaker ? raw.replace(/^\s*[>›»]\s*/, '') : raw;
  if (speaker) frag.append(el('span.speaker', { text: speaker === '»' ? '»' : '\u203a' }));

  // The body is one inline run: the paragraph is a flex row only so the speaker
  // marker can sit in its own gutter, so the text itself must be a single item.
  const line = el('span.line-body');
  for (const part of body.split(/(\*[^*]+\*)/g)) {
    if (!part) continue;
    const marked = part.length > 2 && part.startsWith('*') && part.endsWith('*');
    const inner = marked ? part.slice(1, -1) : part;
    const node = marked ? el('em.nw') : line;
    node.append(glossify(inner, null, { gloss }));
    if (marked) line.append(node);
  }
  frag.append(line);
  return frag;
}

/**
 * Persian text node with any embedded Dutch isolated, so quotes and slashes
 * around a Latin word stay where the author put them.
 */
export function faText(text) {
  const frag = document.createDocumentFragment();
  for (const [chunk, isLatin] of splitBidi(text)) {
    frag.append(isLatin ? el('bdi', { lang: 'nl', dir: 'ltr', text: chunk }) : document.createTextNode(chunk));
  }
  return frag;
}

/** A Persian block element with bidi-safe content. */
export function fa(spec, text, props = {}) {
  const node = el(spec, { lang: 'fa', dir: 'rtl', ...props });
  node.append(faText(text || ''));
  return node;
}

/* ---------- small parts ---------- */

export const bookOf = (id) => BOOKS.find((b) => b.id === id) || BOOKS[0];

export function bookChip(bookId, extra = '') {
  const b = bookOf(bookId);
  return el(`span.chip.chip-${b.tone}`, { text: extra ? `${b.short} · ${extra}` : b.short });
}

export function progressBar(value, total, tone = '') {
  const bar = el(`div.bar${tone ? '.' + tone : ''}`, {}, el('i'));
  bar.firstChild.style.width = `${pct(value, total)}%`;
  return bar;
}

export function stageDots(card) {
  const s = card?.s || 0;
  return el('span.stage-dots', { title: SRS.STAGES[Math.min(s, 5)] },
    [0, 1, 2, 3, 4].map((i) => el('i', { class: i < s ? (SRS.isMastered(card) ? 'on mastered' : 'on') : '' })));
}

export function speakButton(text, opts = {}) {
  if (!audio.available) return null;
  const btn = el('button.speak-btn', {
    type: 'button', 'aria-label': 'Uitspreken', title: 'Uitspreken (nl)',
    html: icon(ICONS.volume, 16),
  });
  btn.addEventListener('click', async (e) => {
    e.stopPropagation();
    btn.dataset.playing = '1';
    await audio.speak(text, { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI, ...opts });
    delete btn.dataset.playing;
  });
  return btn;
}

/* ---------- examples ---------- */

const SRC_LABEL = { book: 'uit het boek', corpus: 'uit het boek', natural: 'voorbeeld', authored: 'voorbeeld' };
const LVL_LABEL = { 1: 'eenvoudig', 2: 'alledaags', 3: 'uitgebreider' };

export function exampleBlock(w, { limit = 3, gloss = store.settings.gloss } = {}) {
  const list = (w.ex || []).slice(0, limit);
  if (!list.length) return el('p.muted', { text: 'Nog geen voorbeeldzin voor dit woord.' });

  return el('div.ex-list', {}, list.map((ex) => {
    const nl = el('div.ex-nl', { lang: 'nl' });
    nl.append(glossify(ex.nl, w.term, { gloss }));
    const top = el('div.ex-top', {}, nl, speakButton(ex.nl));
    const parts = [top];
    if (ex.fa) parts.push(fa('div.ex-fa', ex.fa));
    parts.push(el('div.ex-foot', {},
      el('span.ex-tag', { text: `${LVL_LABEL[ex.lvl] || ''} · ${SRC_LABEL[ex.src] || ''}`.replace(/^ · | · $/, '') }),
      el('span.lvl-dots', {}, [1, 2, 3].map((i) => el('i', { class: i <= (ex.lvl || 1) ? 'on' : '' })))));
    return el('div.ex', {}, parts);
  }));
}

/* ---------- word detail ---------- */

// Both books grade their vocabulary, with slightly different bands.
const TIER_LABEL = {
  ESSENTIAL: ['kernwoord', 'chip-good'],
  HIGH: ['veel gebruikt', 'chip-good'],
  PROFESSIONAL: ['vakwoord', 'chip-warn'],
};

export function wordFacts(w) {
  const chips = [];
  if (w.article) chips.push(el('span.chip', { text: `${w.article} ${w.term}` }));
  if (w.plural) chips.push(el('span.chip', { text: `mv. ${w.plural}` }));
  if (w.verb?.inf && w.verb.inf !== w.term) chips.push(el('span.chip', { text: `inf. ${w.verb.inf}` }));
  if (w.verb?.p3) chips.push(el('span.chip', { text: `hij ${w.verb.p3}` }));
  if (w.verb?.past) chips.push(el('span.chip', { text: `verl. ${w.verb.past}` }));
  if (w.verb?.pp) chips.push(el('span.chip', { text: `volt. ${w.verb.pp}` }));
  if (w.verb?.aux) chips.push(el('span.chip', { text: `hulpww. ${w.verb.aux}` }));
  if (w.sep) chips.push(el('span.chip', { text: `scheidbaar: ${w.sep}` }));
  if (w.prep) chips.push(el('span.chip', { text: `+ ${w.prep}` }));
  if (w.pos) chips.push(el('span.chip', { text: w.pos }));
  if (w.cefr) chips.push(el('span.chip', { text: w.cefr }));
  if (TIER_LABEL[w.tier]) chips.push(el(`span.chip.${TIER_LABEL[w.tier][1]}`, { text: TIER_LABEL[w.tier][0] }));
  return chips;
}

/** Full word detail, used in the browse sheet and after answering a question. */
export function wordDetail(w, { showActions = true } = {}) {
  const card = store.card(w.id);
  const head = el('div.word-head', {},
    el('div.row', {},
      el('h2.word-term.grow', { lang: 'nl', html: (w.article ? `<span class="art">${w.article}</span> ` : '') + w.term }),
      speakButton(w.term)),
    w.printed && w.printed !== w.term ? el('div.word-en', { text: `in het boek: ${w.printed}` }) : null,
    fa('div.word-fa', w.fa || '—'),
    w.equiv ? el('div.word-en', { lang: 'nl', text: `= ${w.equiv}` }) : null,
    store.settings.showEnglish && w.en ? el('div.word-en', { text: w.en }) : null,
    el('div.word-facts', {}, wordFacts(w)));

  const parts = [head];
  if (w.hint) parts.push(el('p.prompt-hint', { lang: 'nl', text: w.hint }));

  parts.push(el('div', {}, el('div.section-title', { text: 'Voorbeeldzinnen' }), exampleBlock(w)));

  const extras = [];
  if (w.colloc?.length) extras.push(chipGroup('Combinaties', w.colloc));
  if (w.combos?.length) extras.push(chipGroup('Vaste patronen', w.combos));
  if (w.syn?.length) extras.push(chipGroup('Synoniemen', w.syn));
  if (w.ant?.length) extras.push(chipGroup('Tegenstellingen', w.ant));
  if (extras.length) parts.push(el('div.stack', { style: { gap: '12px' } }, extras));

  parts.push(statusRow(w, card));
  if (showActions) parts.push(actionRow(w));
  return el('div.word-detail', {}, parts);
}

function chipGroup(title, items) {
  return el('div', {},
    el('div.section-title', { text: title }),
    el('div.row.wrap', { style: { gap: '6px' } }, items.map((c) => el('span.chip', { lang: 'nl', text: c }))));
}

function statusRow(w, card) {
  const strength = SRS.strength(card);
  const rows = [
    ['Fase', SRS.STAGES[Math.min(card?.s || 0, 5)]],
    ['Geheugensterkte', `${strength}%`],
    ['Beurten', card?.r ? `${card.c}/${card.r} goed` : 'nog niet geoefend'],
    ['Volgende herhaling', card?.r ? dueLabel(card.due) : '—'],
    ['Les', `${bookOf(w.book).short} · les ${w.lesson}`],
  ];
  return el('div', {}, el('div.section-title', { text: 'Voortgang' }),
    rows.map(([k, v]) => el('div.kv', {}, el('span.kv-k', { text: k }), el('span.kv-v', { text: v }))));
}

function actionRow(w) {
  const fav = el('button.btn.btn-sm', { type: 'button' });
  const hard = el('button.btn.btn-sm', { type: 'button' });
  const paint = () => {
    fav.innerHTML = icon(ICONS.star, 15) + (store.isFav(w.id) ? ' Favoriet' : ' Favoriet maken');
    fav.classList.toggle('btn-primary', store.isFav(w.id));
    hard.innerHTML = icon(ICONS.flag, 15) + (store.isHard(w.id) ? ' Moeilijk' : ' Markeer moeilijk');
    hard.classList.toggle('btn-primary', store.isHard(w.id));
  };
  fav.addEventListener('click', () => { store.toggleFav(w.id); paint(); });
  hard.addEventListener('click', () => { store.toggleHard(w.id); paint(); });
  paint();
  return el('div.row.wrap', {}, fav, hard);
}

export function openWord(w) {
  openSheet(() => wordDetail(w), { label: w.term });
}

/* ---------- list rows ---------- */

export function wordRow(w, { onClick } = {}) {
  const card = store.card(w.id);
  const badges = [];
  if (store.isFav(w.id)) badges.push(el('span.chip.chip-warn', { text: '★' }));
  if (store.difficult(w.id)) badges.push(el('span.chip.chip-bad', { text: 'moeilijk' }));
  else if (SRS.isMastered(card)) badges.push(el('span.chip.chip-good', { text: 'beheerst' }));

  return el('button.mini', {
    type: 'button',
    onclick: () => (onClick ? onClick(w) : openWord(w)),
  },
    el('span', { style: { minWidth: '0', flex: '1' } },
      el('span.mini-term', { lang: 'nl', text: w.term }),
      el('span.mini-sub', { style: { display: 'block' }, text: `les ${w.lesson} · ${bookOf(w.book).short}` })),
    fa('span.mini-fa', w.faShort || w.fa || ''),
    el('span.mini-badge.row', { style: { gap: '5px' } }, badges, stageDots(card)));
}

export function emptyState(title, body, action) {
  return el('div.empty', {}, el('h3', { text: title }), el('p', { text: body }), action || null);
}

export function sectionCard(title, ...children) {
  return el('section.card', {}, title ? el('div.section-title', { text: title }) : null, ...children);
}
