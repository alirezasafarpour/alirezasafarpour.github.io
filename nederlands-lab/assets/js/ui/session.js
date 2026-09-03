/* The study session runner.
 *
 * One full-screen surface hosts every exercise type. The queue is built by
 * data.buildQueue(); this file only decides how a question looks, what counts
 * as correct, and what happens next. A word answered wrongly is re-queued a few
 * cards later so it gets a second chance inside the same session — on top of
 * the SRS bringing it back sooner on later days.
 */

import { el, mount, clear, icon, ICONS, shuffle, normalizeAnswer, editDistance, pct, toast, clamp } from '../core/util.js';
import { store } from '../core/store.js';
import * as SRS from '../core/srs.js';
import * as DATA from '../core/data.js';
import * as audio from '../core/audio.js';
import { glossify, exampleBlock, speakButton, wordFacts, stageDots, fa } from './components.js';

const EX_LABEL = {
  intro: 'Nieuw woord',
  mc: 'Kies de betekenis',
  mcRev: 'Kies het Nederlandse woord',
  type: 'Typ het Nederlandse woord',
  blank: 'Vul het woord in',
  flash: 'Flashcard',
  listen: 'Luister en typ',
};

let current = null;

export function isActive() { return !!current; }
export function abort() { current?.close(true); }

export function startSession(kind, opts = {}) {
  const queue = DATA.buildQueue(kind, opts);
  if (!queue.length) {
    toast('Geen woorden voor deze oefening — kies een andere modus of les.', 'bad');
    return false;
  }
  current?.close(true);
  current = new Session(kind, queue, opts);
  current.mount();
  return true;
}

class Session {
  constructor(kind, queue, opts) {
    this.kind = kind;
    this.opts = opts;
    this.queue = queue;
    this.pos = 0;
    this.total = queue.length;
    this.right = 0;
    this.wrong = 0;
    this.answeredIds = new Set();
    this.startedAt = Date.now();
    this.repeats = 0;
    this.root = el('div.study', { role: 'dialog', 'aria-modal': 'true', 'aria-label': 'Oefensessie' });
    this.onKey = this.handleKey.bind(this);
  }

  mount() {
    document.body.append(this.root);
    document.body.style.overflow = 'hidden';
    addEventListener('keydown', this.onKey);
    this.render();
  }

  close(silent = false) {
    removeEventListener('keydown', this.onKey);
    audio.stop();
    this.root.remove();
    document.body.style.overflow = '';
    store.addTime(Date.now() - this.startedAt);
    store.save();
    if (current === this) current = null;
    if (!silent) document.dispatchEvent(new CustomEvent('session:done'));
  }

  /* ---------- chrome ---------- */

  render() {
    const item = this.queue[this.pos];
    if (!item) return this.renderFinish();
    const w = DATA.word(item.id);
    if (!w) { this.pos += 1; return this.render(); }

    const bar = el('div.bar', {}, el('i'));
    bar.firstChild.style.width = `${pct(this.pos, this.total)}%`;

    const top = el('div.study-top', {},
      el('button.icon-btn', {
        type: 'button', 'aria-label': 'Sessie sluiten',
        html: icon(ICONS.x, 17), onclick: () => this.confirmExit(),
      }),
      bar,
      el('span.study-count', { text: `${Math.min(this.pos + 1, this.total)}/${this.total}` }),
      el('div.study-score', {},
        el('span.score-pill.ok', { text: String(this.right) }),
        el('span.score-pill.no', { text: String(this.wrong) })));

    this.body = el('div.study-body');
    this.foot = el('div.study-foot');
    mount(this.root, top, this.body, this.foot);

    this.inner = el('div.study-inner');
    this.body.append(this.inner);
    this.renderQuestion(w, item);
  }

  confirmExit() {
    if (this.pos === 0 || this.pos >= this.total) return this.close();
    this.close();
  }

  setFoot(...nodes) { mount(this.foot, el('div.study-foot-inner', {}, nodes.filter(Boolean))); }

  kindLabel(ex) {
    return el('div.q-kind', {}, el('span', { text: EX_LABEL[ex] || '' }));
  }

  /* ---------- question dispatch ---------- */

  renderQuestion(w, item) {
    this.answered = false;
    this.currentWord = w;
    this.currentEx = item.ex;
    switch (item.ex) {
      case 'intro': return this.qIntro(w);
      case 'flash': return this.qFlash(w);
      case 'mc': return this.qChoice(w, 'nl2fa');
      case 'mcRev': return this.qChoice(w, 'fa2nl');
      case 'type': return this.qType(w, false);
      case 'listen': return this.qType(w, true);
      case 'blank': return this.qBlank(w);
      default: return this.qChoice(w, 'nl2fa');
    }
  }

  /* ---------- 1. intro (Learn mode first contact) ---------- */

  qIntro(w) {
    store.introduce(w.id);
    const prompt = el('div.prompt', {},
      el('div.row', { style: { gap: '10px', justifyContent: 'center' } },
        el('div.prompt-word', { lang: 'nl', html: (w.article ? `<span class="art">${w.article}</span> ` : '') + w.term }),
        speakButton(w.term)),
      fa('div.prompt-fa', w.fa || ''),
      store.settings.showEnglish && w.en ? el('div.prompt-hint', { text: w.en }) : null,
      el('div.prompt-meta', {}, wordFacts(w).slice(0, 4)));

    mount(this.inner,
      this.kindLabel('intro'),
      prompt,
      w.hint ? el('p.prompt-hint.center', { lang: 'nl', text: w.hint }) : null,
      el('div', {}, el('div.section-title', { text: 'Zo gebruik je het' }), exampleBlock(w, { limit: 3 })));

    if (store.settings.autoSpeak) audio.speak(w.term, { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI });

    this.setFoot(
      el('button.btn.btn-primary.btn-block', {
        type: 'button', html: `Ik snap het ${icon(ICONS.arrow, 16)}`,
        onclick: () => this.next(),
      }),
      el('p.kbd-hint', { html: '<kbd>Enter</kbd> om verder te gaan' }));
  }

  /* ---------- 2. flashcard ---------- */

  qFlash(w) {
    const front = el('div.prompt', {},
      el('div.row', { style: { gap: '10px', justifyContent: 'center' } },
        el('div.prompt-word', { lang: 'nl', html: (w.article ? `<span class="art">${w.article}</span> ` : '') + w.term },),
        speakButton(w.term)));
    mount(this.inner, this.kindLabel('flash'), front);

    const reveal = () => {
      const back = el('div.prompt', {},
        el('div.prompt-word', { lang: 'nl', html: (w.article ? `<span class="art">${w.article}</span> ` : '') + w.term }),
        fa('div.prompt-fa', w.fa || ''),
        store.settings.showEnglish && w.en ? el('div.prompt-hint', { text: w.en }) : null);
      mount(this.inner, this.kindLabel('flash'), back,
        el('div', {}, el('div.section-title', { text: 'Voorbeeldzinnen' }), exampleBlock(w, { limit: 2 })));
      this.setFoot(this.gradeRow((g) => this.commit(w, g > SRS.GRADE.AGAIN, g)));
      this.revealed = true;
    };
    this.revealFn = reveal;
    this.revealed = false;

    this.setFoot(
      el('button.btn.btn-primary.btn-block', { type: 'button', text: 'Toon betekenis', onclick: reveal }),
      el('p.kbd-hint', { html: '<kbd>Spatie</kbd> om om te draaien' }));
  }

  gradeRow(onGrade) {
    const defs = [
      [SRS.GRADE.AGAIN, 'Opnieuw', 'nu weer'],
      [SRS.GRADE.HARD, 'Moeilijk', 'kort'],
      [SRS.GRADE.GOOD, 'Goed', 'normaal'],
      [SRS.GRADE.EASY, 'Makkelijk', 'lang'],
    ];
    return el('div.grade-row', {}, defs.map(([g, label, sub]) =>
      el('button.grade', { type: 'button', dataset: { g: String(g) }, onclick: () => onGrade(g) },
        label, el('small', { text: sub }))));
  }

  /* ---------- 3. multiple choice ---------- */

  qChoice(w, dir) {
    const nl2fa = dir === 'nl2fa';
    const options = shuffle([w, ...DATA.distractors(w, 3, nl2fa ? 'fa' : 'term')]);
    const label = (x) => (nl2fa ? (x.faShort || x.fa || '') : x.term);

    const prompt = nl2fa
      ? el('div.prompt', {},
          el('div.row', { style: { gap: '10px', justifyContent: 'center' } },
            el('div.prompt-word', { lang: 'nl', html: (w.article ? `<span class="art">${w.article}</span> ` : '') + w.term }),
            speakButton(w.term)))
      : el('div.prompt', {}, fa('div.prompt-fa', w.faShort || w.fa || ''));

    const opts = el('div.opts');
    this.optionButtons = options.map((opt, i) => {
      const btn = el(`button.opt${nl2fa ? '.fa' : ''}`, {
        type: 'button', dataset: { id: opt.id },
        onclick: () => this.answerChoice(w, opt, options),
      },
        el('span.key', { text: String(i + 1) }),
        nl2fa ? fa('span.opt-text', label(opt)) : el('span.opt-text', { lang: 'nl', text: label(opt) }));
      opts.append(btn);
      return btn;
    });

    mount(this.inner, this.kindLabel(nl2fa ? 'mc' : 'mcRev'), prompt, opts);
    this.setFoot(el('p.kbd-hint', { html: 'Kies met <kbd>1</kbd>–<kbd>4</kbd>' }));
    if (nl2fa && store.settings.autoSpeak) audio.speak(w.term, { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI });
  }

  answerChoice(w, picked, options) {
    if (this.answered) return;
    this.answered = true;
    const ok = picked.id === w.id;
    for (const btn of this.optionButtons) {
      btn.disabled = true;
      if (btn.dataset.id === w.id) btn.dataset.state = 'ok';
      else if (btn.dataset.id === picked.id) btn.dataset.state = 'no';
      else btn.dataset.state = 'dim';
    }
    this.commit(w, ok, ok ? SRS.GRADE.GOOD : SRS.GRADE.AGAIN);
  }

  /* ---------- 4. typing (and listening) ---------- */

  qType(w, listening) {
    const prompt = listening
      ? el('div.prompt', {},
          el('button.btn.btn-primary', {
            type: 'button', html: `${icon(ICONS.volume, 18)} Speel af`,
            onclick: () => audio.speak(w.term, { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI }),
          }),
          el('p.prompt-hint', { text: 'Luister en typ wat je hoort.' }))
      : el('div.prompt', {},
          fa('div.prompt-fa', w.fa || ''),
          store.settings.showEnglish && w.en ? el('div.prompt-hint', { text: w.en }) : null,
          el('div.prompt-meta', {}, [
            w.pos ? el('span.chip', { text: w.pos }) : null,
            w.article ? el('span.chip', { text: `${w.article} …` }) : null,
          ].filter(Boolean)));

    const input = el('input.answer-input', {
      type: 'text', lang: 'nl', autocomplete: 'off', autocapitalize: 'off',
      autocorrect: 'off', spellcheck: 'false', placeholder: 'typ in het Nederlands…',
      'aria-label': 'Jouw antwoord',
    });
    this.input = input;

    mount(this.inner, this.kindLabel(listening ? 'listen' : 'type'), prompt, input);
    this.setFoot(
      el('button.btn.btn-primary.btn-block', { type: 'button', text: 'Controleer', onclick: () => this.checkTyped(w) }),
      el('button.btn.btn-ghost.btn-block.btn-sm', { type: 'button', text: 'Ik weet het niet', onclick: () => this.giveUp(w) }));

    setTimeout(() => input.focus({ preventScroll: true }), 30);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); this.answered ? this.next() : this.checkTyped(w); }
    });
    if (listening) setTimeout(() => audio.speak(w.term, { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI }), 250);
  }

  /** Accepts the headword, its printed form, lemma and infinitive. */
  acceptedAnswers(w) {
    const set = new Set();
    for (const v of [w.term, w.printed, w.lemma, w.verb?.inf, w.equiv]) {
      if (v) set.add(normalizeAnswer(v));
    }
    // "de/het woord" typed with its article is fine too.
    if (w.article) set.add(normalizeAnswer(`${w.article} ${w.term}`));
    set.delete('');
    return [...set];
  }

  judgeTyped(w, raw) {
    const given = normalizeAnswer(raw);
    if (!given) return { ok: false, close: false };
    const accepted = this.acceptedAnswers(w);
    if (accepted.includes(given)) return { ok: true, close: false };
    if (store.settings.typingStrictness === 'strict') return { ok: false, close: false };
    // Lenient: one typo in a word of 5+ letters still counts, two are "almost".
    for (const a of accepted) {
      const d = editDistance(given, a);
      const tol = a.length >= 8 ? 2 : a.length >= 5 ? 1 : 0;
      if (d <= tol) return { ok: true, close: true, target: a };
      if (d <= tol + 1) return { ok: false, close: true, target: a };
    }
    return { ok: false, close: false };
  }

  checkTyped(w) {
    if (this.answered) return;
    const verdict = this.judgeTyped(w, this.input.value);
    if (!this.input.value.trim()) { this.input.focus(); return; }
    this.answered = true;
    this.input.disabled = true;
    this.input.dataset.state = verdict.ok ? 'ok' : 'no';
    this.commit(w, verdict.ok, verdict.ok ? (verdict.close ? SRS.GRADE.HARD : SRS.GRADE.GOOD) : SRS.GRADE.AGAIN,
      { typo: verdict.ok && verdict.close, given: this.input.value.trim() });
  }

  giveUp(w) {
    if (this.answered) return;
    this.answered = true;
    if (this.input) { this.input.disabled = true; this.input.dataset.state = 'no'; }
    this.commit(w, false, SRS.GRADE.AGAIN);
  }

  /* ---------- 5. fill in the blank ---------- */

  qBlank(w) {
    const examples = DATA.clozeExamples(w);
    if (!examples.length) return this.qType(w, false);
    const ex = examples[Math.floor(Math.random() * examples.length)];

    const before = ex.nl.slice(0, ex.index);
    const after = ex.nl.slice(ex.index + ex.match.length);
    const gap = el('span.gap', { text: '?' });
    this.gapNode = gap;

    const sentence = el('div.cloze-sentence', { lang: 'nl' });
    sentence.append(glossify(before, null), gap, glossify(after, null));

    const input = el('input.answer-input', {
      type: 'text', lang: 'nl', autocomplete: 'off', autocapitalize: 'off',
      autocorrect: 'off', spellcheck: 'false', placeholder: 'welk woord past hier?',
      'aria-label': 'Ontbrekend woord',
    });
    this.input = input;
    input.addEventListener('input', () => { gap.textContent = input.value || '?'; gap.classList.toggle('filled', !!input.value); });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); this.answered ? this.next() : this.checkBlank(w, ex); }
    });

    mount(this.inner,
      this.kindLabel('blank'),
      el('div.prompt', {}, sentence),
      fa('div.prompt-fa.center', w.faShort || w.fa || ''),
      input);

    this.setFoot(
      el('button.btn.btn-primary.btn-block', { type: 'button', text: 'Controleer', onclick: () => this.checkBlank(w, ex) }),
      el('button.btn.btn-ghost.btn-block.btn-sm', { type: 'button', text: 'Ik weet het niet', onclick: () => this.giveUpBlank(w, ex) }));
    setTimeout(() => input.focus({ preventScroll: true }), 30);
  }

  checkBlank(w, ex) {
    if (this.answered) return;
    if (!this.input.value.trim()) { this.input.focus(); return; }
    const given = normalizeAnswer(this.input.value);
    const target = normalizeAnswer(ex.match);
    const tol = store.settings.typingStrictness === 'strict' ? 0 : target.length >= 6 ? 1 : 0;
    const ok = given === target || this.acceptedAnswers(w).includes(given) || editDistance(given, target) <= tol;
    this.answered = true;
    this.input.disabled = true;
    this.input.dataset.state = ok ? 'ok' : 'no';
    this.gapNode.textContent = ex.match;
    this.gapNode.className = `gap filled ${ok ? 'ok' : 'no'}`;
    this.commit(w, ok, ok ? SRS.GRADE.GOOD : SRS.GRADE.AGAIN, { given: this.input.value.trim() });
  }

  giveUpBlank(w, ex) {
    if (this.answered) return;
    this.answered = true;
    if (this.input) { this.input.disabled = true; this.input.dataset.state = 'no'; }
    this.gapNode.textContent = ex.match;
    this.gapNode.className = 'gap filled no';
    this.commit(w, false, SRS.GRADE.AGAIN);
  }

  /* ---------- verdict + advance ---------- */

  commit(w, ok, grade, extra = {}) {
    store.answer(w.id, grade);
    if (ok) this.right += 1; else this.wrong += 1;
    this.answeredIds.add(w.id);

    if (!ok) this.requeue(w.id);
    this.showVerdict(w, ok, extra);
  }

  /** Bring a missed word back later in this same session. */
  requeue(id) {
    if (this.repeats >= 12) return;
    this.repeats += 1;
    const card = store.card(id);
    const ex = DATA.exerciseForStage(DATA.word(id), card, ['mc', 'mcRev', 'type', 'blank']);
    const at = clamp(this.pos + 3 + Math.floor(Math.random() * 3), this.pos + 1, this.queue.length);
    this.queue.splice(at, 0, { id, ex, repeat: true });
    this.total = this.queue.length;
  }

  showVerdict(w, ok, extra) {
    const mark = el('span.mark', { html: icon(ok ? ICONS.check : ICONS.x, 15) });
    let headline = ok ? 'Goed!' : 'Nog niet';
    if (ok && extra.typo) headline = 'Goed — let op de spelling';

    const answerLine = el('div.row', { style: { gap: '10px', flexWrap: 'wrap' } },
      el('span.word-term', { lang: 'nl', style: { fontSize: '1.35rem' },
        html: (w.article ? `<span class="art">${w.article}</span> ` : '') + w.term }),
      speakButton(w.term));

    const detail = el('div.verdict', { dataset: { v: ok ? 'ok' : 'no' } },
      el('div.verdict-head', {}, mark, headline),
      answerLine,
      !ok && extra.given ? el('p.muted', { text: `jouw antwoord: ${extra.given}` }) : null,
      fa('div.word-fa', w.fa || ''),
      store.settings.showEnglish && w.en ? el('div.word-en', { text: w.en }) : null,
      exampleBlock(w, { limit: ok ? 1 : 2 }),
      el('div.row.wrap', { style: { gap: '6px' } },
        el('button.chip.chip-btn', {
          type: 'button', 'aria-pressed': String(store.isFav(w.id)), text: '★ favoriet',
          onclick: (e) => { const v = store.toggleFav(w.id); e.currentTarget.setAttribute('aria-pressed', String(v)); },
        }),
        el('button.chip.chip-btn', {
          type: 'button', 'aria-pressed': String(store.isHard(w.id)), text: '⚑ moeilijk',
          onclick: (e) => { const v = store.toggleHard(w.id); e.currentTarget.setAttribute('aria-pressed', String(v)); },
        }),
        stageDots(store.card(w.id))));

    this.inner.append(detail);
    detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    this.setFoot(
      el('button.btn.btn-primary.btn-block', {
        type: 'button', html: `Volgende ${icon(ICONS.arrow, 16)}`, onclick: () => this.next(),
      }),
      el('p.kbd-hint', { html: '<kbd>Enter</kbd> voor de volgende' }));
    if (!ok && store.settings.autoSpeak) audio.speak(w.term, { rate: store.settings.speakRate, voiceURI: store.settings.voiceURI });
  }

  next() {
    this.pos += 1;
    if (this.opts.book && this.opts.lesson != null) store.setPosition(this.opts.book, this.opts.lesson);
    this.render();
  }

  /* ---------- finish ---------- */

  renderFinish() {
    const total = this.right + this.wrong;
    const acc = pct(this.right, total);
    const mins = Math.max(1, Math.round((Date.now() - this.startedAt) / 60000));
    const praise = acc >= 90 ? 'Uitstekend!' : acc >= 70 ? 'Goed gedaan!' : acc >= 50 ? 'Op de goede weg.' : 'Blijf oefenen — herhaling werkt.';

    mount(this.root,
      el('div.study-top', {},
        el('button.icon-btn', { type: 'button', 'aria-label': 'Sluiten', html: icon(ICONS.x, 17), onclick: () => this.close() }),
        el('div.bar', {}, el('i', { style: { width: '100%' } })),
        el('span.study-count', { text: 'klaar' })),
      el('div.study-body', {},
        el('div.study-inner', {},
          el('div.finish', {},
            el('div.finish-mark', { text: acc >= 70 ? '🎉' : '💪' }),
            el('h2', { text: praise }),
            el('p.muted', { text: `${DATA.MODES[this.kind]?.label || 'Sessie'} afgerond` }),
            el('div.finish-stats', {},
              el('div.stat', { dataset: { tone: 'good' } }, el('b', { text: String(this.right) }), el('span', { text: 'goed' })),
              el('div.stat', { dataset: { tone: this.wrong ? 'bad' : '' } }, el('b', { text: String(this.wrong) }), el('span', { text: 'fout' })),
              el('div.stat', { dataset: { tone: 'accent' } }, el('b', { text: `${acc}%` }), el('span', { text: 'score' }))),
            el('p.muted', { text: `${total} beurten · ongeveer ${mins} min · streak ${store.meta.streak} 🔥` })))),
      el('div.study-foot', {},
        el('div.study-foot-inner', {},
          el('button.btn.btn-primary.btn-block', {
            type: 'button', text: 'Nog een ronde',
            onclick: () => { const k = this.kind, o = this.opts; this.close(true); startSession(k, o); },
          }),
          el('button.btn.btn-block', { type: 'button', text: 'Terug naar overzicht', onclick: () => this.close() }))));
  }

  /* ---------- keyboard ---------- */

  handleKey(e) {
    if (e.target.tagName === 'INPUT' && e.key !== 'Escape') return;
    if (e.key === 'Escape') { e.preventDefault(); return this.confirmExit(); }

    if (this.pos >= this.total) return;
    if (this.answered) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); this.next(); }
      return;
    }
    if (this.currentEx === 'intro' && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); return this.next(); }
    if (this.currentEx === 'flash') {
      if (!this.revealed && (e.key === ' ' || e.key === 'Enter')) { e.preventDefault(); return this.revealFn(); }
      if (this.revealed && '1234'.includes(e.key)) {
        e.preventDefault();
        return this.commit(this.currentWord, Number(e.key) > 1, Number(e.key) - 1);
      }
      return;
    }
    if (this.optionButtons && '1234'.includes(e.key)) {
      const btn = this.optionButtons[Number(e.key) - 1];
      if (btn && !btn.disabled) { e.preventDefault(); btn.click(); }
    }
  }
}
