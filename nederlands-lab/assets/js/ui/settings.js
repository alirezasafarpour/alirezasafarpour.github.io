/* Settings: account and sync, study preferences, audio, backup. */

import { el, clear, toast, relTime, icon, ICONS } from '../core/util.js';
import { store, DEFAULT_SETTINGS } from '../core/store.js';
import * as sync from '../core/sync.js';
import * as audio from '../core/audio.js';
import * as DATA from '../core/data.js';
import { openSheet, closeSheet } from './components.js';

function switchRow(title, help, checked, onToggle) {
  const sw = el('button.switch', { type: 'button', role: 'switch', 'aria-checked': String(!!checked), 'aria-label': title });
  sw.addEventListener('click', () => {
    const next = sw.getAttribute('aria-checked') !== 'true';
    sw.setAttribute('aria-checked', String(next));
    onToggle(next);
  });
  return el('div.switch-row', {},
    el('div.txt', {}, el('strong', { text: title }), el('small', { text: help })), sw);
}

function numberRow(title, help, value, min, max, onChange) {
  const input = el('input.input', { type: 'number', value: String(value), min: String(min), max: String(max), style: { width: '92px', textAlign: 'center' } });
  input.addEventListener('change', () => {
    const v = Math.max(min, Math.min(max, Number(input.value) || value));
    input.value = String(v);
    onChange(v);
  });
  return el('div.switch-row', {},
    el('div.txt', {}, el('strong', { text: title }), el('small', { text: help })), input);
}

/* ---------- account ---------- */

function accountPanel() {
  const wrap = el('section.card');

  const paint = () => {
    clear(wrap);
    wrap.append(el('div.section-title', { text: 'Account & synchronisatie' }));

    if (!sync.state.configured) {
      wrap.append(
        el('p.muted', { style: { fontSize: '.88rem', marginBottom: '12px' },
          text: 'Koppel een gratis Supabase-project om je voortgang op telefoon, tablet en laptop automatisch gelijk te houden. Zonder koppeling blijft alles veilig op dit apparaat staan.' }),
        el('button.btn.btn-primary', { type: 'button', html: `${icon(ICONS.cloud, 16)} Supabase koppelen`, onclick: () => openConfigSheet(paint) }),
        el('p.help', { style: { marginTop: '10px' }, html: 'Stap 1: maak een project op supabase.com. Stap 2: voer <code>supabase/schema.sql</code> uit in de SQL Editor. Stap 3: plak hier de Project URL en de anon key.' }));
      return;
    }

    if (!sync.isSignedIn()) {
      wrap.append(authForm(paint));
      wrap.append(el('button.btn.btn-ghost.btn-sm', { type: 'button', style: { marginTop: '10px' }, text: 'Andere Supabase-instellingen', onclick: () => openConfigSheet(paint) }));
      return;
    }

    const s = sync.state;
    wrap.append(
      el('div.kv', {}, el('span.kv-k', { text: 'Ingelogd als' }), el('span.kv-v', { text: s.user.email || '—' })),
      el('div.kv', {}, el('span.kv-k', { text: 'Laatste synchronisatie' }), el('span.kv-v', { text: s.lastSync ? relTime(s.lastSync) : 'nog niet' })),
      el('div.kv', {}, el('span.kv-k', { text: 'Status' }), el('span.kv-v', { text: statusLabel(s) })),
      s.lastError ? el('div.callout.callout-warn', { style: { marginTop: '10px' }, text: s.lastError }) : null,
      el('div.row.wrap', { style: { marginTop: '14px', gap: '8px' } },
        el('button.btn.btn-sm.btn-primary', {
          type: 'button', html: `${icon(ICONS.refresh, 15)} Nu synchroniseren`,
          onclick: async (e) => { e.currentTarget.disabled = true; await sync.sync(); paint(); toast('Synchronisatie klaar', 'good'); },
        }),
        el('button.btn.btn-sm', { type: 'button', text: 'Uitloggen', onclick: async () => { await sync.signOut(); paint(); } })));
  };

  sync.onChange(() => { if (wrap.isConnected) paint(); });
  paint();
  return wrap;
}

function statusLabel(s) {
  return { ok: 'gesynchroniseerd', pending: 'bezig…', error: 'fout', idle: 'niet ingelogd', off: 'uit' }[s.status] || s.status;
}

function authForm(onDone) {
  const email = el('input.input', { type: 'email', placeholder: 'e-mailadres', autocomplete: 'email' });
  const pass = el('input.input', { type: 'password', placeholder: 'wachtwoord (min. 6 tekens)', autocomplete: 'current-password' });
  const msg = el('p.help');

  const run = async (fn, okText) => {
    msg.textContent = 'Bezig…';
    try {
      const res = await fn();
      msg.textContent = typeof res === 'string' ? res : okText;
      onDone();
    } catch (err) {
      msg.textContent = String(err.message || err);
    }
  };

  return el('div.stack', { style: { gap: '10px' } },
    el('div.field', {}, el('label', { text: 'E-mail' }), email),
    el('div.field', {}, el('label', { text: 'Wachtwoord' }), pass),
    el('div.row.wrap', { style: { gap: '8px' } },
      el('button.btn.btn-primary', { type: 'button', text: 'Inloggen', onclick: () => run(() => sync.signIn(email.value, pass.value), 'Ingelogd.') }),
      el('button.btn', {
        type: 'button', text: 'Account maken',
        onclick: () => run(async () => {
          const r = await sync.signUp(email.value, pass.value);
          return r.session ? 'Account gemaakt en ingelogd.' : 'Account gemaakt — bevestig je e-mail en log daarna in.';
        }, 'Account gemaakt.'),
      }),
      el('button.btn.btn-ghost', {
        type: 'button', text: 'Magic link',
        onclick: () => run(async () => { await sync.sendMagicLink(email.value); return 'Check je mail voor de inloglink.'; }),
      })),
    msg);
}

function openConfigSheet(onDone) {
  const cfg = sync.getConfig() || { url: '', key: '' };
  const url = el('input.input', { type: 'url', value: cfg.url, placeholder: 'https://xxxx.supabase.co' });
  const key = el('textarea.input', { rows: '3', placeholder: 'anon public key', style: { fontFamily: 'var(--font-mono)', fontSize: '.78rem' } });
  key.value = cfg.key;
  const msg = el('p.help');

  openSheet(() => el('div.stack', { style: { gap: '14px' } },
    el('h2', { style: { fontFamily: 'var(--font-display)', fontSize: '1.2rem' }, text: 'Supabase koppelen' }),
    el('div.callout.callout-info', { html: 'Maak een gratis project op <b>supabase.com</b>, open de SQL Editor en voer <code>supabase/schema.sql</code> uit dit project uit. Kopieer daarna Project URL en anon key uit <b>Project Settings → API</b>. Deze sleutels zijn bedoeld om publiek te zijn; row-level security beschermt je data.' }),
    el('div.field', {}, el('label', { text: 'Project URL' }), url),
    el('div.field', {}, el('label', { text: 'Anon public key' }), key),
    msg,
    el('div.row.wrap', { style: { gap: '8px' } },
      el('button.btn.btn-primary', {
        type: 'button', text: 'Opslaan',
        onclick: () => {
          try { sync.configure(url.value, key.value); closeSheet(); onDone(); toast('Supabase gekoppeld', 'good'); }
          catch (err) { msg.textContent = String(err.message || err); }
        },
      }),
      cfg.url ? el('button.btn.btn-danger', { type: 'button', text: 'Koppeling wissen', onclick: () => { sync.clearConfig(); closeSheet(); onDone(); } }) : null,
      el('button.btn.btn-ghost', { type: 'button', text: 'Annuleren', onclick: closeSheet }))),
    { label: 'Supabase koppelen' });
}

/* ---------- backup ---------- */

function backupPanel() {
  const fileInput = el('input', { type: 'file', accept: 'application/json', hidden: true });
  fileInput.addEventListener('change', async () => {
    const file = fileInput.files?.[0];
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      if (!data || typeof data !== 'object' || !data.cards) throw new Error('Dit bestand bevat geen voortgang.');
      store.applyRemote(data);
      toast('Voortgang samengevoegd', 'good');
      setTimeout(() => location.reload(), 700);
    } catch (err) {
      toast(String(err.message || err), 'bad');
    }
    fileInput.value = '';
  });

  return el('section.card', {},
    el('div.section-title', { text: 'Back-up' }),
    el('p.muted', { style: { fontSize: '.86rem', marginBottom: '12px' },
      text: 'Exporteer je voortgang als bestand, of voeg een eerdere export samen met wat er nu op dit apparaat staat.' }),
    el('div.row.wrap', { style: { gap: '8px' } },
      el('button.btn.btn-sm', {
        type: 'button', html: `${icon(ICONS.down, 15)} Exporteren`,
        onclick: () => {
          const blob = new Blob([JSON.stringify(store.export())], { type: 'application/json' });
          const a = el('a', { href: URL.createObjectURL(blob), download: `nederlands-lab-${new Date().toISOString().slice(0, 10)}.json` });
          document.body.append(a); a.click(); a.remove();
          setTimeout(() => URL.revokeObjectURL(a.href), 2000);
        },
      }),
      el('button.btn.btn-sm', { type: 'button', text: 'Importeren', onclick: () => fileInput.click() }),
      fileInput),
    el('div.row.wrap', { style: { marginTop: '14px' } },
      el('button.btn.btn-sm.btn-danger', {
        type: 'button', text: 'Alle voortgang wissen',
        onclick: () => openSheet(() => el('div.stack', {},
          el('h2', { style: { fontFamily: 'var(--font-display)', fontSize: '1.15rem' }, text: 'Voortgang wissen?' }),
          el('p.muted', { text: 'Dit verwijdert alle leerdata op dit apparaat. Als je bent ingelogd, wordt de lege staat bij de volgende synchronisatie ook naar de cloud geschreven.' }),
          el('div.row.wrap', { style: { gap: '8px' } },
            el('button.btn.btn-danger', { type: 'button', text: 'Ja, wissen', onclick: async () => { await store.reset(); closeSheet(); location.reload(); } }),
            el('button.btn', { type: 'button', text: 'Annuleren', onclick: closeSheet }))), { label: 'Bevestigen' }),
      })));
}

/* ---------- view ---------- */

export function renderSettings(view) {
  const s = store.settings;

  view.append(el('div.page-head', {},
    el('h1', { text: 'Instellingen' }),
    el('p', { text: 'Sessies, uitspraak, account en back-up.' })));

  const study = el('section.card', {},
    el('div.section-title', { text: 'Studeren' }),
    numberRow('Woorden per sessie', 'Hoeveel vragen één ronde bevat.', s.sessionSize, 4, 60, (v) => store.updateSettings({ sessionSize: v })),
    numberRow('Nieuwe woorden per sessie', 'De rest van een ronde is herhaling.', s.newPerSession, 0, 30, (v) => store.updateSettings({ newPerSession: v })),
    switchRow('Engels tonen', 'Laat de Engelse vertaling uit het boek naast het Perzisch zien.', s.showEnglish, (v) => store.updateSettings({ showEnglish: v })),
    switchRow('Tik-vertaling in zinnen', 'Tik op een woord in een voorbeeldzin voor de Perzische betekenis.', s.gloss, (v) => store.updateSettings({ gloss: v })),
    switchRow('Streng spellen', 'Zonder dit telt één typefout nog als goed.', s.typingStrictness === 'strict',
      (v) => store.updateSettings({ typingStrictness: v ? 'strict' : 'lenient' })));

  const voices = audio.available ? audio.dutchVoices() : [];
  const voiceSelect = el('select.select', { 'aria-label': 'Stem' },
    el('option', { value: '', text: voices.length ? 'Automatisch (beste NL-stem)' : 'Geen Nederlandse stem gevonden' }),
    audio.allVoices().map((v) => el('option', { value: v.voiceURI, text: `${v.name} (${v.lang})`, selected: s.voiceURI === v.voiceURI })));
  voiceSelect.addEventListener('change', () => store.updateSettings({ voiceURI: voiceSelect.value }));

  const rate = el('input', { type: 'range', min: '0.6', max: '1.2', step: '0.02', value: String(s.speakRate), style: { width: '140px' } });
  rate.addEventListener('change', () => store.updateSettings({ speakRate: Number(rate.value) }));

  const audioCard = el('section.card', {},
    el('div.section-title', { text: 'Uitspraak' }),
    audio.available
      ? el('div', {},
          switchRow('Automatisch uitspreken', 'Spreek het woord uit zodra een kaart verschijnt.', s.autoSpeak, (v) => store.updateSettings({ autoSpeak: v })),
          el('div.switch-row', {}, el('div.txt', {}, el('strong', { text: 'Stem' }), el('small', { text: voices.length ? `${voices.length} Nederlandse stem(men) beschikbaar` : 'Installeer een Nederlandse stem in je systeeminstellingen voor de beste uitspraak.' })), voiceSelect),
          el('div.switch-row', {}, el('div.txt', {}, el('strong', { text: 'Spreeksnelheid' }), el('small', { text: 'Langzamer helpt bij luisteroefeningen.' })), rate),
          el('button.btn.btn-sm', { type: 'button', html: `${icon(ICONS.volume, 15)} Test`, onclick: () => audio.speak('Goedemorgen, ik oefen mijn Nederlands.', { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI }) }))
      : el('p.muted', { text: 'Deze browser ondersteunt geen spraaksynthese; luisteroefeningen zijn niet beschikbaar.' }));

  const dataCard = el('section.card', {},
    el('div.section-title', { text: 'Woordenlijsten' }),
    DATA.db.books.map((b) => el('div.kv', {},
      el('span.kv-k', { text: b.name }),
      el('span.kv-v', { text: `${DATA.bookWords(b.id).length} woorden · ${DATA.bookLessons(b.id).length} lessen` }))),
    DATA.db.loadErrors.map((e) => el('div.callout.callout-warn', { style: { marginTop: '10px' }, text: `${e.book}: ${e.message}` })),
    store.persistenceDegraded
      ? el('div.callout.callout-warn', { style: { marginTop: '10px' }, text: 'IndexedDB is niet beschikbaar in deze browser. Voortgang wordt alleen in localStorage bewaard — koppel een account om niets te verliezen.' })
      : null);

  const reset = el('section.card', {},
    el('div.section-title', { text: 'Weergave' }),
    el('div.row.wrap', { style: { gap: '8px' } },
      ['auto', 'licht', 'donker'].map((mode, i) => {
        const value = ['auto', 'light', 'dark'][i];
        return el('button.chip.chip-btn', {
          type: 'button', text: mode, 'aria-pressed': String(s.theme === value),
          onclick: () => { store.updateSettings({ theme: value }); applyTheme(value); renderSettingsRefresh(); },
        });
      })),
    el('button.btn.btn-sm.btn-ghost', { type: 'button', style: { marginTop: '12px' }, text: 'Standaardinstellingen herstellen', onclick: () => { store.updateSettings({ ...DEFAULT_SETTINGS }); location.reload(); } }));

  view.append(el('div.stack', {}, accountPanel(), study, audioCard, reset, backupPanel(), dataCard));
}

function renderSettingsRefresh() {
  document.dispatchEvent(new CustomEvent('route:refresh'));
}

export function applyTheme(mode) {
  const root = document.documentElement;
  if (mode === 'light' || mode === 'dark') root.setAttribute('data-theme', mode);
  else root.removeAttribute('data-theme');
}
