/* Small DOM + formatting helpers shared by every view. */

export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

/** Create an element: el('div.card', {onclick}, child, child...) */
export function el(spec, props = null, ...kids) {
  const [tagPart, ...classes] = String(spec).split('.');
  const node = document.createElement(tagPart || 'div');
  if (classes.length) node.className = classes.join(' ');
  if (props) {
    for (const [k, v] of Object.entries(props)) {
      if (v == null || v === false) continue;
      if (k === 'class') node.className = [node.className, v].filter(Boolean).join(' ');
      else if (k === 'html') node.innerHTML = v;
      else if (k === 'text') node.textContent = v;
      else if (k === 'style' && typeof v === 'object') Object.assign(node.style, v);
      else if (k === 'dataset') Object.assign(node.dataset, v);
      else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
      else if (v === true) node.setAttribute(k, '');
      else node.setAttribute(k, v);
    }
  }
  for (const kid of kids.flat(3)) {
    if (kid == null || kid === false) continue;
    node.append(kid.nodeType ? kid : document.createTextNode(String(kid)));
  }
  return node;
}

export function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); return node; }
export function mount(node, ...kids) { clear(node).append(...kids.flat(3).filter(Boolean)); return node; }

export const escapeHtml = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

/* ---------- text ---------- */

/** Case/diacritic/punctuation-insensitive comparison key for typed answers. */
export function normalizeAnswer(s) {
  return String(s ?? '')
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[’'`´]/g, "'")
    .replace(/[^a-z0-9' ]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

/** Levenshtein distance, capped for speed — used for "almost right" feedback. */
export function editDistance(a, b) {
  if (a === b) return 0;
  if (!a.length) return b.length;
  if (!b.length) return a.length;
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

const WORD_RE = /[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’-][A-Za-zÀ-ÖØ-öø-ÿ]+)*/g;
export const tokenize = (s) => String(s ?? '').match(WORD_RE) || [];

/** Split a string into [text, isWord] runs so we can wrap words in spans. */
export function splitTokens(s) {
  const out = []; let last = 0; const str = String(s ?? '');
  WORD_RE.lastIndex = 0;
  for (let m; (m = WORD_RE.exec(str));) {
    if (m.index > last) out.push([str.slice(last, m.index), false]);
    out.push([m[0], true]);
    last = m.index + m[0].length;
  }
  if (last < str.length) out.push([str.slice(last), false]);
  return out;
}

/**
 * Persian text often quotes a Dutch word or phrase. Left to itself the browser
 * reorders the surrounding punctuation around those Latin runs, so quotes and
 * slashes end up on the wrong side. Splitting the string into RTL and LTR runs
 * lets the caller isolate each Latin run in its own <bdi>.
 */
const LATIN_WORD = "[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ0-9'\u2019\\-]*";
// A Latin run, optionally with the quotes that wrap it. Pulling the quotes into
// the isolated run is what keeps « » and " " on the correct side of the phrase.
const LATIN_RUN = new RegExp(
  '[\u00ab\u201c"]?' + LATIN_WORD + '(?:[ /]' + LATIN_WORD + ')*' + '[\u00bb\u201d"]?',
  'g');

export function splitBidi(text) {
  const str = String(text ?? '');
  const out = [];
  let last = 0;
  LATIN_RUN.lastIndex = 0;
  for (let m; (m = LATIN_RUN.exec(str));) {
    if (m.index > last) out.push([str.slice(last, m.index), false]);
    out.push([m[0], true]);
    last = m.index + m[0].length;
  }
  if (last < str.length) out.push([str.slice(last), false]);
  return out;
}

/* ---------- numbers, time ---------- */

export const clamp = (n, lo, hi) => Math.min(hi, Math.max(lo, n));
export const pct = (a, b) => (b > 0 ? Math.round((a / b) * 100) : 0);

export const DAY = 86400000;
/** Local calendar day key, so streaks follow the learner's clock, not UTC. */
export function dayKey(ts = Date.now()) {
  const d = new Date(ts);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
export function dayStart(ts = Date.now()) { const d = new Date(ts); d.setHours(0, 0, 0, 0); return d.getTime(); }
export function daysBetween(a, b) { return Math.round((dayStart(b) - dayStart(a)) / DAY); }

export function relTime(ts) {
  if (!ts) return '—';
  const diff = Date.now() - ts;
  if (diff < 60000) return 'zojuist';
  const mins = Math.round(diff / 60000);
  if (mins < 60) return `${mins} min geleden`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs} uur geleden`;
  const d = Math.round(hrs / 24);
  if (d === 1) return 'gisteren';
  if (d < 30) return `${d} dagen geleden`;
  return new Date(ts).toLocaleDateString('nl-NL', { day: 'numeric', month: 'short' });
}

export function dueLabel(due) {
  if (!due) return 'nieuw';
  const d = daysBetween(Date.now(), due);
  if (d <= 0) return 'nu';
  if (d === 1) return 'morgen';
  if (d < 30) return `over ${d} d`;
  return `over ${Math.round(d / 30)} mnd`;
}

/* ---------- collections ---------- */

export function shuffle(arr, rng = Math.random) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(rng() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}
export const sample = (arr, n) => shuffle(arr).slice(0, n);
export const uniqBy = (arr, key) => {
  const seen = new Set();
  return arr.filter((x) => { const k = key(x); if (seen.has(k)) return false; seen.add(k); return true; });
};

export function debounce(fn, ms = 220) {
  let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

/* ---------- misc ---------- */

export function toast(msg, kind = '') {
  const root = document.getElementById('toaster');
  if (!root) return;
  const node = el('div.toast', { dataset: { kind }, text: msg });
  root.append(node);
  setTimeout(() => {
    node.style.transition = 'opacity .25s, transform .25s';
    node.style.opacity = '0'; node.style.transform = 'translateY(6px)';
    setTimeout(() => node.remove(), 260);
  }, 2400);
}

export const icon = (paths, size = 18) =>
  `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${paths}</svg>`;

export const ICONS = {
  play: '<path d="M7 4.5v15l12-7.5z"/>',
  book: '<path d="M4 4h7v16H4zM13 4h7v16h-7z"/>',
  cards: '<rect x="3" y="6" width="13" height="14" rx="2.5"/><path d="M8 3h10a3 3 0 0 1 3 3v10"/>',
  list: '<path d="M8 6h13M8 12h13M8 18h13M3.5 6h.01M3.5 12h.01M3.5 18h.01"/>',
  pencil: '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
  gap: '<path d="M4 12h4M16 12h4"/><rect x="9" y="8" width="6" height="8" rx="1.5" stroke-dasharray="3 2"/>',
  ear: '<path d="M11 5a5 5 0 0 1 5 5c0 2.5-2 3.5-2 6a2.5 2.5 0 0 1-5 0"/><path d="M6 10a5 5 0 0 1 1.5-3.6"/>',
  volume: '<path d="M11 5 6.5 9H3v6h3.5L11 19z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/>',
  star: '<path d="m12 3.5 2.6 5.3 5.9.9-4.2 4.1 1 5.8-5.3-2.8-5.3 2.8 1-5.8L3.5 9.7l5.9-.9z"/>',
  flag: '<path d="M5 21V4.5M5 5h11l-1.5 3.5L16 12H5"/>',
  refresh: '<path d="M21 12a9 9 0 0 1-15.3 6.4M3 12a9 9 0 0 1 15.3-6.4"/><path d="M21 4v5h-5M3 20v-5h5"/>',
  check: '<path d="m5 13 4.5 4.5L19 7"/>',
  x: '<path d="M6 6l12 12M18 6L6 18"/>',
  arrow: '<path d="M5 12h13m-5.5-5.5L18 12l-5.5 5.5"/>',
  clock: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
  spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/>',
  target: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4"/><circle cx="12" cy="12" r="1"/>',
  fire: '<path d="M12 3s5 4.5 5 9a5 5 0 0 1-10 0c0-2 1-3.5 1-3.5S9 11 10.5 11 12 8 12 3z"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4.5 20a7.5 7.5 0 0 1 15 0"/>',
  cloud: '<path d="M7 18a4 4 0 0 1 .6-8 5.5 5.5 0 0 1 10.4 1.6A3.6 3.6 0 0 1 17.5 18z"/>',
  down: '<path d="M12 4v12m-5-5 5 5 5-5M4.5 20h15"/>',
};
