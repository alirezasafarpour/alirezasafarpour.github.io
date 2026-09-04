"""Authoring helpers for the grammar course.

The course is written as Python literals rather than raw JSON so that every
lesson is checked as it is written: an exercise whose answer is not among its
own options, a lesson pointing at a concept that does not exist, a missing
Persian explanation — all of it fails the build instead of shipping.

Exercise shape
--------------
Every exercise has a semantic ``kind`` (what the learner is asked to do) and a
render ``mode`` (how the app draws it). Three renderers cover every kind:

    choice  one right answer among options   (mc, de/het, niet/geen, ...)
    input   the learner types the answer     (blank, conjugate, translate, ...)
    build   tap word tiles into a sentence   (word order, questions, bijzin)
"""

import re

LEVELS = ("A0", "A1", "A2", "B1")

# kind -> (renderer, Dutch heading shown above the question)
KINDS = {
    "mc":        ("choice", "Kies het juiste antwoord"),
    "dehet":     ("choice", "de of het?"),
    "nietgeen":  ("choice", "niet of geen?"),
    "pickorder": ("choice", "Welke zin klopt?"),
    "pick2":     ("choice", "Welke vorm past hier?"),
    "nl2fa":     ("choice", "Wat betekent deze zin?"),
    "dialogue":  ("choice", "Maak het gesprek af"),
    "scenario":  ("choice", "Wat zeg je?"),
    "fixmc":     ("choice", "Welke zin is fout?"),
    "blank":     ("input",  "Vul het juiste woord in"),
    "conjugate": ("input",  "Vervoeg het werkwoord"),
    "transform": ("input",  "Verander de zin"),
    "fa2nl":     ("input",  "Zeg het in het Nederlands"),
    "fix":       ("input",  "Verbeter de fout"),
    "type":      ("input",  "Typ de hele zin"),
    "order":     ("build",  "Zet in de goede volgorde"),
    "question":  ("build",  "Maak er een vraag van"),
    "subclause": ("build",  "Maak er een bijzin van"),
}

_PROBLEMS = []


def problem(msg):
    _PROBLEMS.append(msg)


def problems():
    return list(_PROBLEMS)


# ---------------------------------------------------------------- concepts

_CONCEPTS = {}


def concept(cid, title, title_fa, level, keywords=(), summary_fa=""):
    """Register one trackable grammar concept."""
    if cid in _CONCEPTS:
        problem(f"duplicate concept id: {cid}")
    if level not in LEVELS:
        problem(f"{cid}: unknown level {level}")
    _CONCEPTS[cid] = {
        "id": cid,
        "title": title,
        "titleFa": title_fa,
        "level": level,
        "keywords": list(keywords),
        "summaryFa": summary_fa,
    }
    return cid


def all_concepts():
    return list(_CONCEPTS.values())


# --------------------------------------------------------------- exercises


def _ex(kind, q, a, **kw):
    mode, heading = KINDS[kind]
    ex = {"kind": kind, "mode": mode, "heading": heading, "q": q, "a": a}
    for key in ("qfa", "why", "hint", "alt", "options", "tiles", "concept", "context", "fa"):
        v = kw.get(key)
        if v:
            ex[key] = v
    if not kw.get("why"):
        problem(f"exercise without Persian explanation: {q!r}")
    return ex


def mc(q, options, a, why, qfa="", concept=None, kind="mc", context="", fa=""):
    """One right answer among 2-4 options."""
    if a not in options:
        problem(f"{kind}: answer {a!r} is not one of its options ({q!r})")
    if len(options) < 2:
        problem(f"{kind}: needs at least two options ({q!r})")
    if len(set(options)) != len(options):
        problem(f"{kind}: duplicate options ({q!r})")
    return _ex(kind, q, a, options=list(options), why=why, qfa=qfa,
               concept=concept, context=context, fa=fa)


def dehet(q, a, why, qfa="", concept=None):
    return mc(q, ["de", "het"], a, why, qfa=qfa, concept=concept, kind="dehet")


def nietgeen(q, a, why, qfa="", concept=None):
    return mc(q, ["niet", "geen"], a, why, qfa=qfa, concept=concept, kind="nietgeen")


def pickorder(q, options, a, why, qfa="", concept=None):
    return mc(q, options, a, why, qfa=qfa, concept=concept, kind="pickorder")


def pick2(q, options, a, why, qfa="", concept=None):
    return mc(q, options, a, why, qfa=qfa, concept=concept, kind="pick2")


def dialogue(context, q, options, a, why, qfa="", concept=None):
    return mc(q, options, a, why, qfa=qfa, concept=concept, kind="dialogue", context=context)


def scenario(context, q, options, a, why, qfa="", concept=None):
    return mc(q, options, a, why, qfa=qfa, concept=concept, kind="scenario", context=context)


def typed(kind, q, a, why, alt=(), qfa="", hint="", concept=None, context=""):
    """Any exercise the learner answers by typing."""
    if not a:
        problem(f"{kind}: empty answer ({q!r})")
    return _ex(kind, q, a, alt=list(alt), why=why, qfa=qfa, hint=hint,
               concept=concept, context=context)


def blank(q, a, why, alt=(), qfa="", hint="", concept=None):
    if "___" not in q:
        problem(f"blank without a gap marker: {q!r}")
    return typed("blank", q, a, why, alt=alt, qfa=qfa, hint=hint, concept=concept)


def conjugate(q, a, why, alt=(), qfa="", hint="", concept=None):
    return typed("conjugate", q, a, why, alt=alt, qfa=qfa, hint=hint, concept=concept)


def transform(q, a, why, alt=(), qfa="", hint="", concept=None):
    return typed("transform", q, a, why, alt=alt, qfa=qfa, hint=hint, concept=concept)


def fa2nl(q, a, why, alt=(), hint="", concept=None):
    """Persian prompt, Dutch answer — the hardest and most useful drill."""
    return typed("fa2nl", q, a, why, alt=alt, hint=hint, concept=concept)


def fix(q, a, why, alt=(), qfa="", hint="", concept=None):
    return typed("fix", q, a, why, alt=alt, qfa=qfa, hint=hint, concept=concept)


def type_all(q, a, why, alt=(), qfa="", hint="", concept=None):
    return typed("type", q, a, why, alt=alt, qfa=qfa, hint=hint, concept=concept)


def _check_tiles(kind, tiles, a):
    """The tiles must be exactly the words of the answer, nothing more."""
    want = [t for t in re.split(r"\s+", a.strip()) if t]
    got = sorted(tiles)
    if sorted(want) != got:
        problem(f"{kind}: tiles {tiles} do not match the answer {a!r}")


def order(a, tiles=None, why="", qfa="", q="", concept=None, alt=()):
    tiles = tiles or _default_tiles(a)
    _check_tiles("order", tiles, a)
    return _ex("order", q or "Maak een goede Nederlandse zin.", a,
               tiles=list(tiles), why=why, qfa=qfa, concept=concept, alt=list(alt))


def question(a, tiles=None, why="", qfa="", q="", concept=None, alt=()):
    tiles = tiles or _default_tiles(a)
    _check_tiles("question", tiles, a)
    return _ex("question", q or "Maak een vraag.", a,
               tiles=list(tiles), why=why, qfa=qfa, concept=concept, alt=list(alt))


def subclause(a, tiles=None, why="", qfa="", q="", concept=None, alt=()):
    tiles = tiles or _default_tiles(a)
    _check_tiles("subclause", tiles, a)
    return _ex("subclause", q or "Maak er één zin van.", a,
               tiles=list(tiles), why=why, qfa=qfa, concept=concept, alt=list(alt))


def _default_tiles(a):
    return [t for t in re.split(r"\s+", a.strip()) if t]


# ----------------------------------------------------------------- lessons

_LESSONS = []
_MODULES = []


def lesson(lid, module, level, title, title_fa, concepts, discover, rule,
           pattern, examples, contrast, usage, exercises, minutes=6):
    """One lesson: discover -> rule -> pattern -> examples -> practice."""
    for cid in concepts:
        if cid not in _CONCEPTS:
            problem(f"{lid}: unknown concept {cid}")
    if not exercises:
        problem(f"{lid}: no exercises")
    if len(exercises) < 6:
        problem(f"{lid}: only {len(exercises)} exercises (want 6+)")
    kinds = {e["kind"] for e in exercises}
    if len(kinds) < 3:
        problem(f"{lid}: only {len(kinds)} exercise kinds — mix more")
    if not examples:
        problem(f"{lid}: no examples")
    for e in examples:
        if not e.get("fa"):
            problem(f"{lid}: example without Persian: {e.get('nl')!r}")
    for ex in exercises:
        cid = ex.get("concept")
        if cid and cid not in _CONCEPTS:
            problem(f"{lid}: exercise points at unknown concept {cid}")
        if cid and cid not in concepts:
            problem(f"{lid}: exercise concept {cid} is not taught by this lesson")
    rec = {
        "id": lid, "module": module, "level": level,
        "title": title, "titleFa": title_fa,
        "concepts": list(concepts), "minutes": minutes,
        "discover": discover, "rule": rule, "pattern": pattern,
        "examples": examples, "contrast": contrast, "usage": usage,
        "exercises": [dict(e, concept=e.get("concept") or concepts[0]) for e in exercises],
    }
    _LESSONS.append(rec)
    return lid


def module(mid, level, title, title_fa, goal_fa, lessons, icon="book"):
    for lid in lessons:
        if not any(l["id"] == lid for l in _LESSONS):
            problem(f"module {mid}: unknown lesson {lid}")
    _MODULES.append({
        "id": mid, "level": level, "title": title, "titleFa": title_fa,
        "goalFa": goal_fa, "lessons": list(lessons), "icon": icon,
    })
    return mid


def ex(nl, fa, note=""):
    """One example sentence with its Persian meaning."""
    rec = {"nl": nl, "fa": fa}
    if note:
        rec["note"] = note
    return rec


def wrong(bad, good, fa):
    """A mistake Persian speakers actually make, and the fix."""
    return {"bad": bad, "good": good, "fa": fa}


def pattern(parts, fa=""):
    """Visual sentence skeleton: a list of (text, role) slots."""
    return {"parts": [{"text": t, "role": r} for t, r in parts], "fa": fa}


def discover(lines, fa, answer_fa):
    """The noticing step: see real Dutch first, work out the rule, then read it."""
    return {"lines": list(lines), "fa": fa, "answerFa": answer_fa}


def rule(nl, fa, en=""):
    r = {"nl": nl, "fa": fa}
    if en:
        r["en"] = en
    return r


def dump(level):
    """Everything authored for one level, ready to be written as JSON."""
    lessons = [l for l in _LESSONS if l["level"] == level]
    modules = [m for m in _MODULES if m["level"] == level]
    concepts = [c for c in all_concepts() if c["level"] == level]
    lesson_ids = {l["id"] for l in lessons}
    claimed = {lid for m in modules for lid in m["lessons"]}
    for lid in lesson_ids - claimed:
        problem(f"lesson {lid} is in no module")
    return {"level": level, "modules": modules, "lessons": lessons, "concepts": concepts}
