/* Dutch text-to-speech via the Web Speech API.
 *
 * Voice lists load asynchronously and differ per platform, so we resolve the
 * best available Dutch voice lazily and fall back to any nl-* voice, then to
 * the platform default. When no speech synthesis exists at all, speak() is a
 * no-op and `available` stays false so the UI can hide listening exercises.
 */

const synth = typeof speechSynthesis !== 'undefined' ? speechSynthesis : null;

let voices = [];
let resolved = null;
let warmed = false;

function refreshVoices() {
  if (!synth) return;
  voices = synth.getVoices() || [];
  resolved = null;
}

if (synth) {
  refreshVoices();
  synth.addEventListener?.('voiceschanged', refreshVoices);
}

export const available = !!synth;

export function dutchVoices() {
  if (!voices.length) refreshVoices();
  return voices.filter((v) => /^nl(-|_|$)/i.test(v.lang || ''));
}

export function allVoices() {
  if (!voices.length) refreshVoices();
  return voices;
}

function pickVoice(preferredURI) {
  if (!synth) return null;
  if (preferredURI) {
    const exact = allVoices().find((v) => v.voiceURI === preferredURI);
    if (exact) return exact;
  }
  if (resolved) return resolved;
  const nl = dutchVoices();
  // Prefer nl-NL over nl-BE, and a local voice over a network one.
  const score = (v) => (/nl[-_]NL/i.test(v.lang) ? 2 : 0) + (v.localService ? 1 : 0);
  resolved = nl.sort((a, b) => score(b) - score(a))[0] || null;
  return resolved;
}

export function hasDutchVoice() { return !!pickVoice(); }

/**
 * Speak Dutch text. Returns a promise that settles when playback ends, so the
 * caller can show a playing state without guessing at timing.
 */
export function speak(text, opts = {}) {
  if (!synth || !text) return Promise.resolve(false);
  try {
    synth.cancel();
    // Safari needs one primed utterance before it will speak reliably.
    if (!warmed) { warmed = true; try { synth.resume(); } catch { /* ignore */ } }

    const u = new SpeechSynthesisUtterance(String(text));
    const voice = pickVoice(opts.voiceURI);
    if (voice) u.voice = voice;
    u.lang = (voice && voice.lang) || 'nl-NL';
    u.rate = Math.max(0.5, Math.min(1.4, opts.rate || 0.92));
    u.pitch = opts.pitch || 1;

    return new Promise((resolve) => {
      let done = false;
      const finish = (ok) => { if (!done) { done = true; resolve(ok); } };
      u.onend = () => finish(true);
      u.onerror = () => finish(false);
      // Long utterances can silently stall on some platforms; cap the wait.
      setTimeout(() => finish(true), 1200 + String(text).length * 90);
      synth.speak(u);
    });
  } catch {
    return Promise.resolve(false);
  }
}

export function stop() { try { synth && synth.cancel(); } catch { /* ignore */ } }
