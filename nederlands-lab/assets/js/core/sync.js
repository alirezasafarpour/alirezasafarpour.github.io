/* Accounts and cross-device sync, backed by Supabase.
 *
 * Talks to the Supabase Auth and PostgREST endpoints directly — no SDK, no CDN
 * script, nothing to keep in step. The project URL and anon key are public by
 * design (row-level security is what protects the data), and are configurable
 * in-app so no keys have to live in the repository.
 *
 * Sync model: one JSONB row per user holding the whole progress state. On every
 * sync we pull the remote row, merge it with local state (per-word timestamps,
 * see store.mergeStates) and push the result back. That makes studying offline
 * on one device and continuing on another safe in both directions.
 */

import { store } from './store.js';

const CFG_KEY = 'nl-lab:supabase';
const SESSION_KEY = 'nl-lab:session';
const TABLE = 'user_state';
const AUTO_MS = 90_000;

export const state = {
  configured: false,
  user: null,
  status: 'off',      // off | idle | pending | ok | error
  lastSync: 0,
  lastError: '',
};

const listeners = new Set();
export function onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); }
function emit() { for (const fn of listeners) { try { fn(state); } catch { /* listener errors are not sync errors */ } } }

function setStatus(status, error = '') {
  state.status = status;
  state.lastError = error;
  emit();
}

/* ---------- configuration ---------- */

function readJSON(key) {
  try { const v = localStorage.getItem(key); return v ? JSON.parse(v) : null; } catch { return null; }
}
function writeJSON(key, value) {
  try {
    if (value == null) localStorage.removeItem(key);
    else localStorage.setItem(key, JSON.stringify(value));
  } catch { /* private mode: sync stays session-only */ }
}

let cfg = null;
let session = null;
let timer = null;
let inFlight = null;

export function getConfig() { return cfg ? { ...cfg } : null; }

export function configure(url, anonKey) {
  const clean = String(url || '').trim().replace(/\/+$/, '');
  const key = String(anonKey || '').trim();
  if (!clean || !key) throw new Error('Vul zowel de project-URL als de anon key in.');
  if (!/^https:\/\/[\w.-]+/.test(clean)) throw new Error('De project-URL moet met https:// beginnen.');
  cfg = { url: clean, key };
  writeJSON(CFG_KEY, cfg);
  state.configured = true;
  setStatus(session ? 'idle' : 'off');
}

export function clearConfig() {
  cfg = null; session = null;
  writeJSON(CFG_KEY, null); writeJSON(SESSION_KEY, null);
  state.configured = false; state.user = null;
  stopAuto();
  setStatus('off');
}

/* ---------- low-level requests ---------- */

async function api(path, { method = 'GET', body, auth = true, headers = {} } = {}) {
  if (!cfg) throw new Error('Nog geen Supabase-project ingesteld.');
  const h = { apikey: cfg.key, 'Content-Type': 'application/json', ...headers };
  if (auth && session?.access_token) h.Authorization = `Bearer ${session.access_token}`;
  const res = await fetch(cfg.url + path, {
    method, headers: h, body: body == null ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  let json = null;
  try { json = text ? JSON.parse(text) : null; } catch { json = null; }
  if (!res.ok) {
    const msg = json?.error_description || json?.msg || json?.message || json?.error || `HTTP ${res.status}`;
    const err = new Error(msg);
    err.status = res.status;
    throw err;
  }
  return json;
}

function saveSession(s) {
  session = s;
  state.user = s?.user ? { id: s.user.id, email: s.user.email } : null;
  writeJSON(SESSION_KEY, s ? {
    access_token: s.access_token,
    refresh_token: s.refresh_token,
    expires_at: s.expires_at || Math.floor(Date.now() / 1000) + (s.expires_in || 3600),
    user: state.user,
  } : null);
  emit();
}

async function ensureFreshToken() {
  if (!session) return false;
  const exp = (session.expires_at || 0) * 1000;
  if (exp - Date.now() > 60_000) return true;
  if (!session.refresh_token) return false;
  try {
    const s = await api('/auth/v1/token?grant_type=refresh_token', {
      method: 'POST', auth: false, body: { refresh_token: session.refresh_token },
    });
    saveSession(s);
    return true;
  } catch {
    saveSession(null);
    return false;
  }
}

/* ---------- auth ---------- */

export async function signUp(email, password) {
  const s = await api('/auth/v1/signup', {
    method: 'POST', auth: false, body: { email, password },
  });
  // With email confirmation on, no session is returned until the link is used.
  if (s?.access_token) { saveSession(s); await sync({ force: true }); return { session: true }; }
  return { session: false };
}

export async function signIn(email, password) {
  const s = await api('/auth/v1/token?grant_type=password', {
    method: 'POST', auth: false, body: { email, password },
  });
  saveSession(s);
  await sync({ force: true });
  startAuto();
  return state.user;
}

/** Passwordless: Supabase mails a magic link back to this page. */
export async function sendMagicLink(email) {
  await api('/auth/v1/otp', {
    method: 'POST', auth: false,
    body: { email, create_user: true, email_redirect_to: location.href.split('#')[0] },
  });
}

export async function signOut() {
  try { if (session) await api('/auth/v1/logout', { method: 'POST' }); } catch { /* local sign-out still applies */ }
  saveSession(null);
  stopAuto();
  setStatus('idle');
}

/** Pick up tokens Supabase appends to the URL after a magic-link redirect. */
function consumeAuthRedirect() {
  const raw = location.hash.startsWith('#') ? location.hash.slice(1) : '';
  if (!raw.includes('access_token=')) return false;
  const p = new URLSearchParams(raw);
  const access_token = p.get('access_token');
  if (!access_token) return false;
  saveSession({
    access_token,
    refresh_token: p.get('refresh_token'),
    expires_at: Math.floor(Date.now() / 1000) + Number(p.get('expires_in') || 3600),
    user: null,
  });
  history.replaceState(null, '', location.pathname + location.search + '#/');
  return true;
}

async function fetchUser() {
  try {
    const u = await api('/auth/v1/user');
    if (u?.id) { state.user = { id: u.id, email: u.email }; writeJSON(SESSION_KEY, { ...session, user: state.user }); emit(); }
  } catch { /* token may be stale; sync will surface it */ }
}

/* ---------- sync ---------- */

/**
 * Pull, merge, push. Safe to call often: overlapping calls share one promise
 * and a failure leaves local state untouched.
 */
export async function sync(opts = {}) {
  if (!cfg || !session) { setStatus(cfg ? 'idle' : 'off'); return false; }
  if (inFlight) return inFlight;

  inFlight = (async () => {
    setStatus('pending');
    try {
      if (!(await ensureFreshToken())) throw new Error('Sessie verlopen — log opnieuw in.');
      if (!state.user?.id) await fetchUser();
      const uid = state.user?.id;
      if (!uid) throw new Error('Geen gebruiker gevonden.');

      const rows = await api(`/rest/v1/${TABLE}?user_id=eq.${uid}&select=state,updated_at`);
      const remote = Array.isArray(rows) && rows[0] ? rows[0].state : null;

      // applyRemote merges per-word by timestamp, so local work is never lost.
      if (remote) store.applyRemote(remote);

      const payload = {
        user_id: uid,
        state: store.state,
        updated_at: new Date().toISOString(),
      };
      await api(`/rest/v1/${TABLE}?on_conflict=user_id`, {
        method: 'POST', body: payload,
        headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
      });

      state.lastSync = Date.now();
      setStatus('ok');
      return true;
    } catch (err) {
      setStatus('error', String(err.message || err));
      return false;
    } finally {
      inFlight = null;
    }
  })();
  return inFlight;
}

function startAuto() {
  stopAuto();
  if (!cfg || !session) return;
  timer = setInterval(() => { if (!document.hidden) sync(); }, AUTO_MS);
}
function stopAuto() { clearInterval(timer); timer = null; }

/* ---------- boot ---------- */

export async function init() {
  cfg = readJSON(CFG_KEY);
  state.configured = !!cfg;

  const redirected = consumeAuthRedirect();
  if (!redirected) {
    const saved = readJSON(SESSION_KEY);
    if (saved?.access_token) { session = saved; state.user = saved.user || null; }
  }

  if (!cfg) { setStatus('off'); return state; }
  if (!session) { setStatus('idle'); return state; }

  setStatus('pending');
  await fetchUser();
  await sync();
  startAuto();

  // Sync when the tab comes back and before it goes away, so a device switch
  // never loses the last few answers.
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) sync();
    else if (store.state.updatedAt > state.lastSync) sync();
  });
  addEventListener('online', () => sync());
  addEventListener('pagehide', () => { try { store.save(); } catch { /* best effort */ } });

  return state;
}

export const isSignedIn = () => !!session && !!state.user;
