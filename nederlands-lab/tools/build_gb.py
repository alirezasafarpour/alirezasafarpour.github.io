"""Normalise the Groen Boek dataset into the app's shared word schema.

Usage:
    python3 build_gb.py [path/to/nederlands_lab_dataset_V2.json]

The exported shape of that file is not fixed, so this script discovers it:
it finds the list of entries wherever it sits in the JSON, then maps each
entry's fields by name against the aliases below. Run it and read the report
it prints — it names every field it matched and every one it ignored, so a
mismatch is visible rather than silent.

Outputs ../data/gb.words.json and ../data/gb.lessons.json.
"""
import json
import os
import re
import sys
import collections

import lib_text as T

OUT = "../data"
DEFAULT_SRC = "src/nederlands_lab_dataset_V2.json"
CURATED = "curated/gb.examples.curated.json"
SENT_FA = "curated/sentences.fa.json"

# Field aliases, checked case-insensitively after stripping non-letters.
ALIASES = {
    "term":    ["dutch", "nl", "nederlands", "woord", "word", "term", "headword", "vocab", "front"],
    "fa":      ["persian", "fa", "farsi", "perzisch", "meaning", "translation", "betekenis", "back", "manaa", "معنی"],
    "faShort": ["persianshort", "fashort", "shortmeaning", "gloss"],
    "en":      ["english", "en", "engels", "translationen"],
    "lesson":  ["lesson", "les", "chapter", "hoofdstuk", "unit", "lessonnumber", "lesnummer", "lesid"],
    "pos":     ["pos", "partofspeech", "wordclass", "woordsoort", "type", "category"],
    "article": ["article", "lidwoord", "gender", "artikel"],
    "plural":  ["plural", "meervoud"],
    "hint":    ["hint", "note", "notes", "uitleg", "explanation", "opmerking", "simpledutch"],
    "cefr":    ["cefr", "level", "niveau"],
    "freq":    ["freq", "frequency", "importance", "frequentie"],
    "tier":    ["tier", "classification", "class", "priority"],
    "lemma":   ["lemma", "base", "stam", "infinitive"],
    "equiv":   ["equivalent", "equiv", "synoniem", "sameas"],
    "page":    ["page", "pagina", "bladzijde", "printedpage"],
    "id":      ["id", "entryid", "wordid", "key", "uid", "nr", "number", "index"],
}
EXAMPLE_KEYS = ["examples", "example", "voorbeelden", "voorbeeld", "sentences", "sentence",
                "zinnen", "zin", "samples", "usage", "exampleSentences"]
EX_NL_KEYS = ["nl", "dutch", "sentence", "text", "zin", "nederlands", "example", "front"]
EX_FA_KEYS = ["fa", "persian", "farsi", "translation", "vertaling", "meaning", "back"]

ARTICLE_RE = re.compile(r"^(.*?)\s*\((de|het)\)\s*$", re.I)
EQUIV_RE = re.compile(r"^(.*?)\s*=\s*(.+)$")


def norm_key(k):
    return re.sub(r"[^a-z؀-ۿ]", "", str(k).lower())


def find_entries(data):
    """Locate the list of word records anywhere in the loaded JSON."""
    if isinstance(data, list):
        return data, "$"
    if not isinstance(data, dict):
        return [], "?"
    # Prefer an obviously named key, else the longest list of dicts.
    named = ["entries", "words", "vocabulary", "items", "data", "records", "list", "woorden"]
    for key in named:
        for k, v in data.items():
            if norm_key(k) == norm_key(key) and isinstance(v, list) and v:
                return v, k
    best, best_key = [], "?"
    for k, v in data.items():
        if isinstance(v, list) and len(v) > len(best) and v and isinstance(v[0], dict):
            best, best_key = v, k
        elif isinstance(v, dict):
            sub, sub_key = find_entries(v)
            if len(sub) > len(best):
                best, best_key = sub, f"{k}.{sub_key}"
    return best, best_key


def flatten(entry, prefix="", out=None, depth=0):
    """Flatten one nested record so aliases can match keys at any depth."""
    out = {} if out is None else out
    if depth > 3:
        return out
    example_keys = {norm_key(k) for k in EXAMPLE_KEYS}
    for k, v in entry.items():
        key = norm_key(k)
        if key in example_keys:
            continue
        if isinstance(v, dict):
            flatten(v, prefix + key, out, depth + 1)
        elif key not in out or out[key] in (None, "", []):
            out[key] = v
    return out


def pick(flat, field):
    for alias in ALIASES[field]:
        a = norm_key(alias)
        for k, v in flat.items():
            if k == a and v not in (None, "", [], {}):
                return v
    # Second pass: allow a distinctive alias as a suffix ("sourcedutch",
    # "learningpersian"). Short aliases are skipped: "en" would match "zinnen".
    for alias in ALIASES[field]:
        a = norm_key(alias)
        if len(a) < 5:
            continue
        for k, v in flat.items():
            if k.endswith(a) and v not in (None, "", [], {}):
                return v
    return None


def as_text(v):
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return T.norm_ws("؛ ".join(as_text(x) for x in v if x))
    if isinstance(v, dict):
        return T.norm_ws(" ".join(as_text(x) for x in v.values() if x))
    return T.norm_ws(str(v))


def read_examples(entry):
    """Collect example sentences in whatever shape the export used."""
    flat_raw = {norm_key(k): v for k, v in entry.items()}
    out = []
    for key in EXAMPLE_KEYS:
        v = flat_raw.get(norm_key(key))
        if not v:
            continue
        items = v if isinstance(v, list) else [v]
        for it in items:
            if isinstance(it, str):
                out.append({"nl": T.norm_ws(it), "fa": ""})
            elif isinstance(it, dict):
                low = {norm_key(k): val for k, val in it.items()}
                nl = next((as_text(low[k]) for k in map(norm_key, EX_NL_KEYS) if low.get(k)), "")
                fa = next((as_text(low[k]) for k in map(norm_key, EX_FA_KEYS) if low.get(k)), "")
                if nl:
                    out.append({"nl": nl, "fa": fa})
    seen, uniq = set(), []
    for e in out:
        k = T.fold(e["nl"])
        if e["nl"] and k not in seen:
            seen.add(k)
            uniq.append(e)
    return uniq


def make_id(raw, index):
    """Stable per-word id: the source id when it is usable, else the position."""
    s = re.sub(r"[^A-Za-z0-9_-]", "", as_text(raw))
    if not s:
        return str(index).zfill(4)
    return s.zfill(4) if s.isdigit() else s


def clean_surface(raw):
    s = T.norm_ws(raw)
    equiv = None
    m = EQUIV_RE.match(s)
    if m:
        s, equiv = T.norm_ws(m.group(1)), T.norm_ws(m.group(2))
    art = None
    m = ARTICLE_RE.match(s)
    if m:
        s, art = T.norm_ws(m.group(1)), m.group(2).lower()
    return s, art, equiv


def level_of(s):
    n = len(s)
    return 1 if n <= 55 else 2 if n <= 95 else 3


def build(src):
    data = json.load(open(src, encoding="utf-8"))
    entries, where = find_entries(data)
    if not entries:
        raise SystemExit(f"No list of entries found in {src}. Top-level keys: "
                         f"{list(data)[:12] if isinstance(data, dict) else type(data)}")

    curated = json.load(open(CURATED, encoding="utf-8")) if os.path.exists(CURATED) else {}
    sent_fa = {}
    if os.path.exists(SENT_FA):
        for k, v in json.load(open(SENT_FA, encoding="utf-8")).items():
            if v and v.strip():
                sent_fa[T.fold(k)] = v.strip()

    words, seen = [], {}
    matched = collections.Counter()
    unmatched_keys = collections.Counter()
    known = {norm_key(a) for al in ALIASES.values() for a in al} | {norm_key(k) for k in EXAMPLE_KEYS}

    for i, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            continue
        flat = flatten(entry)
        for k in flat:
            if k not in known:
                unmatched_keys[k] += 1

        raw_term = as_text(pick(flat, "term"))
        if not raw_term:
            continue
        term, art, equiv = clean_surface(raw_term)
        if not term:
            continue

        fa = as_text(pick(flat, "fa"))
        lesson_raw = pick(flat, "lesson")
        try:
            lesson = int(re.sub(r"\D", "", str(lesson_raw)) or 0)
        except ValueError:
            lesson = 0

        w = {
            "id": "gb-" + make_id(pick(flat, "id"), i),
            "book": "gb",
            "lesson": lesson,
            "term": term,
            "fa": fa,
            "en": as_text(pick(flat, "en")),
            "pos": as_text(pick(flat, "pos")),
            "cefr": as_text(pick(flat, "cefr")),
            "tier": (as_text(pick(flat, "tier")) or "USEFUL").upper()[:12],
        }
        for field, value in (
            ("faShort", as_text(pick(flat, "faShort"))),
            ("article", (as_text(pick(flat, "article")) or art or "").lower() or None),
            ("plural", as_text(pick(flat, "plural"))),
            ("hint", as_text(pick(flat, "hint"))),
            ("lemma", as_text(pick(flat, "lemma"))),
            ("equiv", as_text(pick(flat, "equiv")) or equiv),
            ("printed", raw_term if raw_term != term else None),
        ):
            if value:
                w[field] = value
        if w.get("article") not in ("de", "het", None):
            w.pop("article", None)

        freq = pick(flat, "freq")
        try:
            w["freq"] = max(1, min(5, int(float(freq))))
        except (TypeError, ValueError):
            w["freq"] = 3
        w["speak"] = w["freq"]

        page = pick(flat, "page")
        if page not in (None, ""):
            w["page"] = as_text(page)

        ex = read_examples(entry) + curated.get(w["id"], [])
        for e in ex:
            if not e.get("fa"):
                e["fa"] = sent_fa.get(T.fold(e["nl"]), "")
            e["src"] = "book"
            e["lvl"] = level_of(e["nl"])
        ex.sort(key=lambda e: (e["lvl"], len(e["nl"])))
        w["ex"] = ex[:3]

        for field in ("term", "fa", "en", "ex", "lesson"):
            if w.get(field) not in (None, "", []):
                matched[field] += 1

        key = (T.fold(term), lesson)
        if key in seen:
            continue
        seen[key] = w
        words.append(w)

    counts = collections.Counter(w["lesson"] for w in words)
    lessons = [{"book": "gb", "n": n, "title": f"Les {n}" if n else "Overig",
                "words": counts[n], "text": [], "cloze": []}
               for n in sorted(counts)]

    os.makedirs(OUT, exist_ok=True)
    json.dump(words, open(f"{OUT}/gb.words.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"book": "gb", "title": "Het Groene Boek",
               "subtitle": "Nederlands voor buitenlanders — Delftse methode, deel 1",
               "lessons": lessons},
              open(f"{OUT}/gb.lessons.json", "w", encoding="utf-8"), ensure_ascii=False)

    print(f"source: {src}")
    print(f"entries found at key: {where}  ({len(entries)} records)")
    print(f"words written: {len(words)}   lessons: {len(lessons)}")
    print("field coverage:", {k: matched[k] for k in ("term", "fa", "en", "lesson", "ex")})
    print("with examples:", sum(1 for w in words if w["ex"]),
          "| example slots:", sum(len(w["ex"]) for w in words),
          "| with Persian:", sum(1 for w in words for e in w["ex"] if e.get("fa")))
    print("with article:", sum(1 for w in words if w.get("article")))
    if unmatched_keys:
        print("unmapped source fields (add an alias if any of these matter):")
        for k, n in unmatched_keys.most_common(15):
            print(f"   {k}  ({n})")
    thin = [w for w in words if len(w["ex"]) < 2]
    if thin:
        print(f"words with fewer than 2 examples: {len(thin)} "
              f"(author them into {CURATED} with ex_todo/ex_add)")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC)
