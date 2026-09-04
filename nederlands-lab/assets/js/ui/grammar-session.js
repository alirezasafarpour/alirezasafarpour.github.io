/* The grammar lesson runner.
 *
 * A lesson is not a page of theory followed by a quiz. It is one flow:
 * notice the pattern → read one short rule → see real sentences → practise,
 * with the common-mistake card dropped in halfway and the "when do Dutch
 * people actually say this" card just before the end.
 *
 * A wrong answer is where the teaching happens: it says why, shows the right
 * shape, and puts the question back a few cards later.
 */

import { el, mount, clear, icon, ICONS, shuffle, toast, clamp, pct } from '../core/util.js';
import { store } from '../core/store.js';
import * as SRS from '../core/srs.js';
import * as G from '../core/grammar.js';
import { glossify, fa, speakButton } from './components.js';

let current = null;

export function isActive() { return !!current; }
export function abortGrammar() { current?.close(true); }

/**
 * Start a lesson (kind 'lesson') or a drill of loose exercises
 * (kind 'review' | 'mixed' | 'concept').
 */
export function startGrammar(kind, opts = {}) {
  let items = [];
  let lesson = null;

  if (kind === 'lesson') {
    lesson = G.lesson(opts.lesson);
    if (!lesson) { toast('Deze les bestaat niet.', 'bad'); return false; }
    items = buildLessonFlow(lesson);
    store.gStartLesson(lesson.id, lesson.level);
  } else if (kind === 'concept') {
    items = G.reviewQueue({ size: opts.size || 12, conceptId: opts.concept });
  } else if (kind === 'mixed') {
    items = G.mixedQueue(opts.size || 15);
  } else {
    items = G.reviewQueue({ size: opts.size || 15, level: opts.level || '' });
  }

  if (!items.length) {
    toast(kind === 'review'
      ? 'Nog niets te herhalen — doe eerst een grammaticales.'
      : 'Geen oefeningen gevonden.', 'bad');
    return false;
  }

  current?.close(true);
  current = new GrammarSession(kind, items, { ...opts, lesson });
  current.mount();
  return true;
}

/**
 * Discover → rule → examples → recognise → (mistakes) → build → produce →
 * (usage) → done. The authored exercises are already ordered easy-to-hard, so
 * the flow only has to decide where the two teaching cards land.
 */
function buildLessonFlow(l) {
  const ex = G.lessonQueue(l.id);
  const cut = Math.max(2, Math.round(ex.length * 0.45));
  return [
    { card: 'discover', lesson: l },
    { card: 'rule', lesson: l },
    { card: 'examples', lesson: l },
    ...ex.slice(0, cut),
    ...(l.contrast?.length ? [{ card: 'contrast', lesson: l }] : []),
    ...ex.slice(cut),
    ...(l.usage ? [{ card: 'usage', lesson: l }] : []),
  ];
}

const isCard = (item) => !!item && !!item.card;

class GrammarSession {
  constructor(kind, queue, opts) {
    this.kind = kind;
    this.opts = opts;
    this.lesson = opts.lesson || null;
    this.queue = queue;
    this.pos = 0;
    this.right = 0;
    this.wrong = 0;
    this.repeats = 0;
    this.startedAt = Date.now();
    this.root = el('div.study.study-grammar', {
      role: 'dialog', 'aria-modal': 'true', 'aria-label': 'Grammaticales',
    });
    this.onKey = this.handleKey.bind(this);
  }

  get exerciseCount() { return this.queue.filter((i) => !isCard(i)).length; }

  mount() {
    document.body.append(this.root);
    document.body.style.overflow = 'hidden';
    addEventListener('keydown', this.onKey);
    this.render();
  }

  close(silent = false) {
    removeEventListener('keydown', this.onKey);
    this.root.remove();
    document.body.style.overflow = '';
    if (current === this) current = null;
    store.addTime(Date.now() - this.startedAt);
    store.save();
    if (!silent) document.dispatchEvent(new CustomEvent('grammar:done'));
  }

  /* ---------- chrome ---------- */

  render() {
    if (this.pos >= this.queue.length) return this.renderFinish();
    const item = this.queue[this.pos];
    this.answered = false;
    this.current = item;

    const done = this.pos;
    const total = this.queue.length;
    mount(this.root,
      el('div.study-top', {},
        el('button.icon-btn', {
          type: 'button', 'aria-label': 'Sluiten', html: icon(ICONS.x, 17),
          onclick: () => this.close(),
        }),
        el('div.bar', {}, el('i', { style: { width: `${pct(done, total)}%` } })),
        el('span.study-count', { text: `${Math.min(done + 1, total)}/${total}` }),
        el('div.study-score', {},
          el('span.score-pill.ok', { text: String(this.right) }),
          el('span.score-pill.no', { text: String(this.wrong) }))),
      el('div.study-body', {}, this.inner = el('div.study-inner')),
      this.foot = el('div.study-foot'));

    if (isCard(item)) this.renderCard(item);
    else this.renderExercise(item);
  }

  setFoot(...nodes) { mount(this.foot, el('div.study-foot-inner', {}, nodes.filter(Boolean))); }

  kindLabel(text) { return el('div.q-kind', {}, el('span', { text })); }

  next() { this.pos += 1; this.render(); }

  handleKey(e) {
    if (e.key === 'Escape') return this.close();
    if (isCard(this.current) && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault(); return this.next();
    }
    if (this.answered && e.key === 'Enter') { e.preventDefault(); return this.next(); }
    if (!this.answered && this.optionButtons && /^[1-4]$/.test(e.key)) {
      const btn = this.optionButtons[Number(e.key) - 1];
      if (btn) { e.preventDefault(); btn.click(); }
    }
  }

  /* ---------- teaching cards ---------- */

  renderCard(item) {
    const l = item.lesson;
    const build = {
      discover: () => this.cardDiscover(l),
      rule: () => this.cardRule(l),
      examples: () => this.cardExamples(l),
      contrast: () => this.cardContrast(l),
      usage: () => this.cardUsage(l),
    }[item.card];
    build?.();
    this.setFoot(
      el('button.btn.btn-primary.btn-block', {
        type: 'button', html: `${item.card === 'usage' ? 'Verder' : 'Ik snap het'} ${icon(ICONS.arrow, 16)}`,
        onclick: () => this.next(),
      }),
      el('p.kbd-hint', { html: '<kbd>Enter</kbd> om verder te gaan' }));
  }

  /** Step 1: see the Dutch first and work out the pattern yourself. */
  cardDiscover(l) {
    const d = l.discover || {};
    const reveal = el('div.reveal', { hidden: true },
      fa('p.reveal-text', d.answerFa || ''));
    const btn = el('button.btn.btn-block', {
      type: 'button', text: 'Toon wat er gebeurt',
      onclick: () => { reveal.hidden = false; btn.hidden = true; },
    });

    mount(this.inner,
      this.kindLabel('Ontdek het patroon'),
      el('div.g-lines', {}, (d.lines || []).map((line) =>
        el('div.g-line', { lang: 'nl' }, glossify(line, null)))),
      fa('p.g-ask', d.fa || ''),
      btn, reveal);
  }

  /** Step 2: one short rule, plus the sentence shape drawn out. */
  cardRule(l) {
    const r = l.rule || {};
    mount(this.inner,
      this.kindLabel('De regel'),
      el('div.g-rule', {},
        el('div.g-rule-nl', { lang: 'nl', text: r.nl || '' }),
        fa('div.g-rule-fa', r.fa || ''),
        r.en ? el('div.g-rule-en', { text: r.en }) : null),
      l.pattern ? patternBlock(l.pattern) : null);
  }

  /** Step 3: real sentences, tappable for Persian word meanings. */
  cardExamples(l) {
    mount(this.inner,
      this.kindLabel('Zo klinkt het'),
      el('div.g-examples', {}, (l.examples || []).slice(0, 6).map((e) =>
        el('div.g-example', {},
          el('div.row', { style: { gap: '8px', alignItems: 'flex-start' } },
            el('div.g-ex-nl.grow', { lang: 'nl' }, glossify(e.nl, null)),
            speakButton(e.nl)),
          fa('div.g-ex-fa', e.fa || ''),
          e.note ? fa('div.g-ex-note', e.note) : null))));
  }

  /** Step 4: the mistakes Persian speakers actually make, side by side. */
  cardContrast(l) {
    mount(this.inner,
      this.kindLabel('Let op — veelgemaakte fout'),
      el('div.g-contrasts', {}, (l.contrast || []).map((c) =>
        el('div.g-contrast', {},
          el('div.g-bad', {}, el('span.g-mark', { text: '✕' }),
            el('span', { lang: 'nl', text: c.bad })),
          el('div.g-good', {}, el('span.g-mark', { text: '✓' }),
            el('span', { lang: 'nl', text: c.good })),
          fa('div.g-why', c.fa || '')))));
  }

  /** Step 5: when do Dutch people actually use this? */
  cardUsage(l) {
    mount(this.inner,
      this.kindLabel('Wanneer gebruik je dit?'),
      el('div.g-usage', {}, fa('p', l.usage || '')));
  }

  /* ---------- exercises ---------- */

  renderExercise(item) {
    this.optionButtons = null;
    this.input = null;
    const head = el('div.g-q-head', {},
      this.kindLabel(item.heading || 'Oefening'),
      item.recycled || item.review
        ? el('span.chip.chip-warn.g-recycle', { text: 'herhaling' }) : null);

    const context = item.context
      ? el('div.g-context', { lang: 'nl' }, glossify(item.context, null)) : null;
    const ask = item.qfa ? fa('p.g-ask-small', item.qfa) : null;

    if (item.mode === 'choice') this.exChoice(item, head, context, ask);
    else if (item.mode === 'build') this.exBuild(item, head, context, ask);
    else this.exInput(item, head, context, ask);
  }

  questionNode(item) {
    // Direction follows whichever script dominates, not merely whether Persian
    // appears at all: "Ik ga sporten. → (جمله را ... کن)" is a Dutch sentence
    // with a Persian instruction, and forcing the whole line RTL scrambles it.
    const persian = (item.q.match(/[؀-ۿ]/g) || []).length;
    const latin = (item.q.match(/[A-Za-zÀ-ÖØ-öø-ÿ]/g) || []).length;
    return persian > latin
      ? fa('div.g-question.g-question-fa', item.q)
      : el('div.g-question', { lang: 'nl', dir: 'ltr' }, glossify(item.q, null));
  }

  exChoice(item, head, context, ask) {
    const options = shuffle(item.options || []);
    const opts = el('div.opts');
    this.optionButtons = options.map((opt, i) => {
      const btn = el('button.opt', {
        type: 'button', dataset: { v: opt },
        onclick: () => this.answerChoice(item, opt),
      },
        el('span.key', { text: String(i + 1) }),
        el('span.opt-text', { lang: 'nl', text: opt }));
      opts.append(btn);
      return btn;
    });

    mount(this.inner, head, context, this.questionNode(item), ask, opts);
    this.setFoot(el('p.kbd-hint', { html: 'Kies met <kbd>1</kbd>–<kbd>4</kbd>' }));
  }

  answerChoice(item, picked) {
    if (this.answered) return;
    this.answered = true;
    const ok = picked === item.a;
    for (const btn of this.optionButtons) {
      btn.disabled = true;
      if (btn.dataset.v === item.a) btn.dataset.state = 'ok';
      else if (btn.dataset.v === picked) btn.dataset.state = 'no';
      else btn.dataset.state = 'dim';
    }
    this.commit(item, ok, { given: picked });
  }

  /** Tap the words into the right order — the word-order exercise. */
  exBuild(item, head, context, ask) {
    const pool = el('div.g-tiles');
    const line = el('div.g-build-line', { lang: 'nl' });
    const chosen = [];

    const paint = () => {
      clear(line);
      if (!chosen.length) line.append(el('span.g-placeholder', { text: 'tik de woorden aan…' }));
      chosen.forEach((word, i) => {
        line.append(el('button.g-tile.g-tile-set', {
          type: 'button', text: word, disabled: this.answered,
          onclick: () => { chosen.splice(i, 1); paint(); },
        }));
      });
      for (const btn of pool.children) {
        btn.disabled = this.answered || chosen.includes(btn.dataset.word)
          ? countOf(chosen, btn.dataset.word) >= countOf(item.tiles, btn.dataset.word)
          : false;
      }
      check.disabled = chosen.length !== (item.tiles || []).length;
    };

    for (const word of shuffle(item.tiles || [])) {
      pool.append(el('button.g-tile', {
        type: 'button', text: word, dataset: { word },
        onclick: () => { chosen.push(word); paint(); },
      }));
    }

    const check = el('button.btn.btn-primary.btn-block', {
      type: 'button', text: 'Controleer',
      onclick: () => this.checkBuild(item, chosen),
    });
    this.buildLine = line;

    mount(this.inner, head, context, this.questionNode(item), ask, line, pool);
    this.setFoot(check,
      el('button.btn.btn-ghost.btn-block.btn-sm', {
        type: 'button', text: 'Ik weet het niet',
        onclick: () => this.commit(item, false, { given: chosen.join(' ') }),
      }));
    paint();
  }

  checkBuild(item, chosen) {
    if (this.answered) return;
    const given = chosen.join(' ');
    const verdict = G.judge(item, given);
    this.answered = true;
    this.buildLine.dataset.state = verdict.ok ? 'ok' : 'no';
    for (const btn of this.buildLine.children) btn.disabled = true;
    this.commit(item, verdict.ok, { given });
  }

  exInput(item, head, context, ask) {
    const input = el('input.answer-input', {
      type: 'text', lang: 'nl', autocomplete: 'off', autocapitalize: 'off',
      autocorrect: 'off', spellcheck: 'false',
      placeholder: item.kind === 'fa2nl' ? 'schrijf de Nederlandse zin…' : 'jouw antwoord…',
      'aria-label': 'Jouw antwoord',
    });
    this.input = input;
    input.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter') return;
      e.preventDefault();
      this.answered ? this.next() : this.checkInput(item);
    });

    mount(this.inner, head, context, this.questionNode(item), ask, input,
      item.hint ? fa('p.g-hint', item.hint) : null);
    this.setFoot(
      el('button.btn.btn-primary.btn-block', {
        type: 'button', text: 'Controleer', onclick: () => this.checkInput(item),
      }),
      el('button.btn.btn-ghost.btn-block.btn-sm', {
        type: 'button', text: 'Ik weet het niet',
        onclick: () => { if (!this.answered) { this.answered = true; input.disabled = true; this.commit(item, false, {}); } },
      }));
    setTimeout(() => input.focus({ preventScroll: true }), 30);
  }

  checkInput(item) {
    if (this.answered) return;
    if (!this.input.value.trim()) { this.input.focus(); return; }
    const verdict = G.judge(item, this.input.value);
    this.answered = true;
    this.input.disabled = true;
    this.input.dataset.state = verdict.ok ? 'ok' : 'no';
    this.commit(item, verdict.ok, { given: this.input.value.trim(), typo: verdict.typo });
  }

  /* ---------- grading and feedback ---------- */

  commit(item, ok, extra) {
    const conceptId = item.concept;
    if (conceptId) {
      store.gAnswer(conceptId, ok ? (extra.typo ? SRS.GRADE.HARD : SRS.GRADE.GOOD) : SRS.GRADE.AGAIN);
    }
    if (ok) this.right += 1; else { this.wrong += 1; this.requeue(item); }
    this.showVerdict(item, ok, extra);
  }

  /** A missed concept comes back a few cards later, in this same session. */
  requeue(item) {
    if (this.repeats >= 6) return;
    this.repeats += 1;
    const at = clamp(this.pos + 3 + Math.floor(Math.random() * 3), this.pos + 1, this.queue.length);
    this.queue.splice(at, 0, { ...item, recycled: true });
  }

  /**
   * The teaching moment. A wrong answer gets the reason, the correct shape and
   * one more real example — not just a red cross.
   */
  showVerdict(item, ok, extra) {
    const c = item.concept ? G.concept(item.concept) : null;
    const lesson = G.lesson(item.lesson);
    const another = ok ? null : anotherExample(lesson, item);

    const detail = el('div.verdict', { dataset: { v: ok ? 'ok' : 'no' } },
      el('div.verdict-head', {},
        el('span.mark', { html: icon(ok ? ICONS.check : ICONS.x, 15) }),
        ok ? (extra.typo ? 'Goed — let op de spelling' : 'Goed!') : 'Nog niet'),
      !ok && extra.given ? el('p.muted', { text: `jouw antwoord: ${extra.given}` }) : null,
      el('div.g-answer', { lang: 'nl' }, glossify(item.a, null)),
      item.why ? fa('div.g-why-box', item.why) : null,
      another ? el('div.g-more', {},
        el('div.section-title', { text: 'Nog een voorbeeld' }),
        el('div.g-ex-nl', { lang: 'nl' }, glossify(another.nl, null)),
        fa('div.g-ex-fa', another.fa || '')) : null,
      c ? el('div.row.wrap', { style: { gap: '6px' } },
        el('span.chip', { text: c.title }),
        el('span.chip.chip-' + (G.conceptStats(c.id).mastered ? 'good' : ''), {
          text: `${G.conceptStats(c.id).strength}% sterk`,
        })) : null);

    this.inner.append(detail);
    detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    this.setFoot(
      el('button.btn.btn-primary.btn-block', {
        type: 'button', html: `Volgende ${icon(ICONS.arrow, 16)}`, onclick: () => this.next(),
      }),
      el('p.kbd-hint', { html: '<kbd>Enter</kbd> voor de volgende' }));
  }

  /* ---------- finish ---------- */

  renderFinish() {
    const total = this.right + this.wrong;
    const score = total ? Math.round((this.right / total) * 100) : 0;
    const mins = Math.max(1, Math.round((Date.now() - this.startedAt) / 60000));

    let rec = null;
    if (this.kind === 'lesson' && this.lesson) {
      rec = store.gFinishLesson(this.lesson.id, score, G.PASS_MARK);
    }
    const passed = !rec ? score >= G.PASS_MARK : rec.best >= G.PASS_MARK;
    const headline = !total ? 'Les doorgelopen'
      : score >= 90 ? 'Uitstekend!'
      : score >= G.PASS_MARK ? 'Goed gedaan!'
      : 'Bijna — nog één ronde?';

    // Mastery is never granted for showing up: say plainly what is still needed.
    const concepts = (this.lesson?.concepts || []).map((id) => ({ c: G.concept(id), s: G.conceptStats(id) }));

    mount(this.root,
      el('div.study-top', {},
        el('button.icon-btn', {
          type: 'button', 'aria-label': 'Sluiten', html: icon(ICONS.x, 17),
          onclick: () => this.close(),
        }),
        el('div.bar', {}, el('i', { style: { width: '100%' } })),
        el('span.study-count', { text: 'klaar' })),
      el('div.study-body', {},
        el('div.study-inner.center', {},
          el('div.finish-emoji', { text: passed ? '🎯' : '💪' }),
          el('h2.finish-title', { text: headline }),
          this.lesson ? el('p.muted', { text: this.lesson.title }) : null,
          el('div.stat-grid', {},
            statBox(this.right, 'goed', 'good'),
            statBox(this.wrong, 'fout', this.wrong ? 'bad' : ''),
            statBox(total ? `${score}%` : '—', 'score',
              score >= G.PASS_MARK ? 'good' : score >= 50 ? 'warn' : 'bad')),
          this.kind === 'lesson' ? el('p.muted.finish-note', {
            text: passed
              ? `Les gehaald · ${mins} min`
              : `Je hebt ${G.PASS_MARK}% nodig om deze les af te ronden — probeer het nog een keer.`,
          }) : el('p.muted.finish-note', { text: `${mins} min geoefend` }),
          concepts.length ? el('div.g-concept-list', {}, concepts.map(({ c, s }) =>
            el('div.g-concept-row', {},
              el('div.grow', {},
                el('strong', { text: c.title }),
                fa('small', c.titleFa || '')),
              el('div.bar.g-bar', {}, el('i', { style: { width: `${s.strength}%` } })),
              el('span.chip' + (s.mastered ? '.chip-good' : ''), {
                text: s.mastered ? 'beheerst' : `${s.strength}%`,
              })))) : null)),
      el('div.study-foot', {},
        el('div.study-foot-inner', {},
          el('button.btn.btn-primary.btn-block', {
            type: 'button', text: passed ? 'Terug naar grammatica' : 'Nog een ronde',
            onclick: () => {
              const { kind, opts } = this;
              this.close();
              if (!passed) startGrammar(kind, opts);
            },
          }),
          el('button.btn.btn-block', {
            type: 'button', text: 'Afsluiten', onclick: () => this.close(),
          }))));
  }
}

/* ---------- helpers ---------- */

function statBox(value, label, tone) {
  return el('div.stat', { dataset: { tone: tone || '' } },
    el('b', { text: String(value) }), el('span', { text: label }));
}

function countOf(list, word) {
  return (list || []).filter((w) => w === word).length;
}

/** One more example of the same point, for the "you got it wrong" card. */
function anotherExample(lesson, item) {
  const pool = (lesson?.examples || []).filter((e) => e.nl && e.nl !== item.a);
  if (!pool.length) return null;
  return pool[Math.floor(Math.random() * pool.length)];
}

/** The sentence skeleton, drawn as coloured slots. */
export function patternBlock(p) {
  return el('div.g-pattern', {},
    el('div.g-pattern-row', {}, (p.parts || []).map((part) =>
      el('span.g-slot', { dataset: { role: part.role || '' }, lang: 'nl', text: part.text }))),
    p.fa ? fa('div.g-pattern-fa', p.fa) : null);
}
