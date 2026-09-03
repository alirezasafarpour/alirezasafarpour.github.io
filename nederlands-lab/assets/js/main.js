/* Bootstrap and hash router. */

import { $, $$, clear, el, toast } from './core/util.js';
import { store } from './core/store.js';
import * as DATA from './core/data.js';
import * as sync from './core/sync.js';
import { renderDashboard } from './ui/dashboard.js';
import { renderBooks, renderBook, renderLesson } from './ui/books.js';
import { renderBrowse } from './ui/browse.js';
import { renderStats } from './ui/stats.js';
import { renderSettings, applyTheme } from './ui/settings.js';
import { closeSheet } from './ui/components.js';
import { isActive as sessionActive } from './ui/session.js';

export function go(hash) {
  if (location.hash === hash) render();
  else location.hash = hash;
}

/* ---------- routing ---------- */

function parseRoute() {
  const raw = location.hash.replace(/^#\/?/, '');
  const [pathPart, queryPart] = raw.split('?');
  const parts = pathPart.split('/').filter(Boolean);
  return { parts, params: new URLSearchParams(queryPart || '') };
}

const NAV_FOR = { '': 'home', book: 'books', lesson: 'books', browse: 'browse', stats: 'stats', settings: 'settings' };

function render() {
  const view = $('#view');
  if (!view) return;
  closeSheet();
  clear(view);

  const { parts, params } = parseRoute();
  const head = parts[0] || '';

  try {
    switch (head) {
      case '': renderDashboard(view); break;
      case 'books': renderBooks(view); break;
      case 'book': renderBook(view, parts[1]); break;
      case 'lesson': renderLesson(view, parts[1], Number(parts[2])); break;
      case 'browse': renderBrowse(view, params); break;
      case 'stats': renderStats(view); break;
      case 'settings': renderSettings(view); break;
      default: renderDashboard(view); break;
    }
  } catch (err) {
    console.error(err);
    view.append(el('div.empty', {},
      el('h3', { text: 'Er ging iets mis bij het tonen van deze pagina' }),
      el('p', { text: String(err.message || err) }),
      el('button.btn.btn-primary', { type: 'button', text: 'Terug naar start', onclick: () => go('#/') })));
  }

  const navKey = head === 'books' ? 'books' : (NAV_FOR[head] || 'home');
  for (const a of $$('[data-nav]')) a.classList.toggle('on', a.dataset.nav === navKey);
  view.scrollTop = 0;
  window.scrollTo({ top: 0 });
  paintChrome();
}

/* ---------- chrome ---------- */

function paintChrome() {
  const streak = store.meta.streak || 0;
  const chip = $('#streakChip');
  const count = $('#streakCount');
  if (count) count.textContent = String(streak);
  if (chip) chip.dataset.live = streak > 0 ? '1' : '0';
  const dot = $('#syncDot');
  if (dot) dot.dataset.state = sync.state.status;
}

function wireChrome() {
  $('#themeBtn')?.addEventListener('click', () => {
    const order = ['auto', 'light', 'dark'];
    const next = order[(order.indexOf(store.settings.theme) + 1) % order.length];
    store.updateSettings({ theme: next });
    applyTheme(next);
    toast(`Thema: ${{ auto: 'systeem', light: 'licht', dark: 'donker' }[next]}`);
  });

  $('#syncBtn')?.addEventListener('click', async () => {
    if (!sync.state.configured || !sync.isSignedIn()) return go('#/settings');
    await sync.sync();
    toast(sync.state.status === 'ok' ? 'Voortgang gesynchroniseerd' : (sync.state.lastError || 'Synchronisatie mislukt'),
      sync.state.status === 'ok' ? 'good' : 'bad');
  });

  $('#streakChip')?.addEventListener('click', () => go('#/stats'));

  sync.onChange(paintChrome);
  store.on('progress', paintChrome);
  document.addEventListener('session:done', () => { render(); sync.sync(); });
  document.addEventListener('route:refresh', render);
  addEventListener('hashchange', () => { if (!sessionActive()) render(); });
}

/* ---------- boot ---------- */

async function boot() {
  await store.init();
  applyTheme(store.settings.theme);

  try {
    await DATA.loadData();
  } catch (err) {
    console.error('dataset load failed', err);
  }

  $('#boot')?.remove();
  $('#app').hidden = false;

  wireChrome();
  render();

  // Sync runs after first paint so a slow network never blocks studying.
  sync.init().then(() => paintChrome()).catch(() => paintChrome());

  // isSecureContext covers https and localhost, where service workers are allowed.
  if ('serviceWorker' in navigator && isSecureContext) {
    navigator.serviceWorker.register(new URL('../../sw.js', import.meta.url)).catch(() => { /* offline cache is optional */ });
  }

  if (!DATA.db.books.length) {
    toast('Geen woordenlijsten gevonden — controleer de map data/.', 'bad');
  }
}

boot().catch((err) => {
  console.error(err);
  const boot = $('#boot');
  if (boot) {
    boot.innerHTML = '';
    boot.append(
      el('p.boot-text', { text: 'De app kon niet starten.' }),
      el('p.boot-text', { text: String(err.message || err) }),
      el('button.btn', { type: 'button', text: 'Opnieuw proberen', onclick: () => location.reload() }));
  }
});
