"""Build the Groen Boek dataset from nederlands_lab_dataset_V2.json.

That file carries both books plus lesson texts, grammar cards and a shared
sentence pool. This script takes the Groen Boek half and emits it in the same
schema Tweede Ronde already uses, so every study mode works on both books
without knowing which one it is looking at.

It also writes back the two cross-book fields (lexemeId / senseId) onto the
Tweede Ronde words, which is what lets the app recognise that a word met in
Groen Boek is the same lexeme when it reappears in Tweede Ronde.

Usage:
    python3 build_gb.py [path/to/nederlands_lab_dataset_V2.json]

Outputs ../data/gb.words.json and ../data/gb.lessons.json.
"""
import json
import os
import re
import sys
import collections

import lib_text as T

SRC = "src/nederlands_lab_dataset_V2.json"
OUT = "../data"
CURATED = "curated/gb.examples.curated.json"
SENT_FA = "curated/sentences.fa.json"
RAW_OUT = "build/gb.words.raw.json"

# The dataset's short part-of-speech codes -> the Dutch labels the app shows.
POS = {
    "noun": "zelfstandig naamwoord",
    "verb": "werkwoord",
    "adjective": "bijvoeglijk naamwoord",
    "adverb": "bijwoord",
    "preposition": "voorzetsel",
    "pronoun": "voornaamwoord",
    "conjunction": "voegwoord",
    "numeral": "telwoord",
    "article": "lidwoord",
    "proper noun": "eigennaam",
    "interjection": "tussenwerpsel",
    "phrase": "uitdrukking",
    "other": "woord",
}

# Corpus counts run from 1 to ~1700; the app's freq field is a 1-5 priority.
FREQ_BANDS = ((100, 5), (30, 4), (10, 3), (3, 2))


def freq_band(n):
    try:
        n = int(n)
    except (TypeError, ValueError):
        return 3
    for threshold, band in FREQ_BANDS:
        if n >= threshold:
            return band
    return 1


def clean_text(s):
    """Strip the source's footnote marks; keep dialogue and emphasis markers."""
    return T.norm_ws((s or "").replace("°", ""))


def strip_marks(s):
    """Plain text with the book's *new word* emphasis removed."""
    return T.norm_ws(re.sub(r"\*(.+?)\*", r"\1", s or "").replace("°", ""))


def level_of(s):
    n = len(s)
    return 1 if n <= 55 else 2 if n <= 95 else 3


def usable(s):
    """True when a mined sentence reads as an ordinary, complete Dutch sentence."""
    if not (14 <= len(s) <= 165) or "_" in s or "*" in s:
        return False
    if not re.search(r"[.!?]$", s):
        return False
    if re.match(r"^\s*\d+[.)]", s):          # numbered exercise line
        return False
    return len(s.split()) >= 3


def load_curated():
    curated = json.load(open(CURATED, encoding="utf-8")) if os.path.exists(CURATED) else {}
    sent_fa = {}
    if os.path.exists(SENT_FA):
        for k, v in json.load(open(SENT_FA, encoding="utf-8")).items():
            if v and v.strip():
                sent_fa[T.fold(k)] = v.strip()
    return curated, sent_fa


def build_words(data, exs):
    """Normalise the Groen Boek vocabulary rows."""
    words, seen = [], {}
    for v in data["vocab"]:
        if v.get("b") != "GB":
            continue
        term = T.norm_ws(v.get("sf") or v.get("nl") or "")
        if not term:
            continue
        printed = T.norm_ws(v.get("nl") or "")

        w = {
            "id": "gb-" + str(v["nr"]).zfill(4),
            "book": "gb",
            "lesson": int(v.get("les") or 0),
            "term": term,
            "fa": T.norm_ws(v.get("fa") or ""),
            "en": T.norm_ws(v.get("en") or ""),
            "pos": POS.get(v.get("pos") or "", v.get("pos") or ""),
            "tier": (v.get("cls") or "USEFUL").upper(),
            "freq": freq_band(v.get("freq")),
        }
        w["speak"] = w["freq"]

        lemma = T.norm_ws(v.get("lm") or "")

        # Verb detail lives in `morph` for this book; `pp` is only a flag saying
        # the headword is itself a past participle, so it carries no form.
        verb = {}
        morph = v.get("morph") if isinstance(v.get("morph"), dict) else {}
        for dst, key in (("inf", "inf"), ("pp", "pp"), ("p3", "present3"),
                         ("past", "pastSg"), ("pastPl", "pastPl")):
            val = T.norm_ws(str(morph.get(key) or ""))
            if val:
                verb[dst] = val
        aux = morph.get("aux")
        if isinstance(aux, list) and aux:
            verb["aux"] = "/".join(T.norm_ws(str(a)) for a in aux if a)
        elif aux:
            verb["aux"] = T.norm_ws(str(aux))
        if v.get("pos") == "verb" and lemma and lemma != term:
            verb.setdefault("inf", lemma)

        for field, value in (
            ("printed", printed if printed and printed != term else None),
            ("article", (v.get("art") or "").lower() or None),
            ("lemma", lemma if lemma and lemma != term else None),
            ("hint", T.norm_ws(v.get("nlx") or "")),
            ("prep", T.norm_ws(v.get("prep") or "")),
            ("plural", T.norm_ws(str(morph.get("pl") or ""))),
            ("verb", verb or None),
            ("sep", T.norm_ws(str(v.get("sep") or "")) or None),
            ("lex", v.get("lexemeId")),
            ("sense", v.get("senseId")),
            ("page", v.get("pg")),
        ):
            if value:
                w[field] = value
        if w.get("article") not in ("de", "het", None):
            w.pop("article", None)

        for field, key in (("colloc", "col"), ("syn", "syn"), ("ant", "ant")):
            vals = [T.norm_ws(x) for x in (v.get(key) or []) if T.norm_ws(x)]
            vals = [x for x in vals if T.fold(x) != T.fold(term)]
            if vals:
                w[field] = vals[:4]

        # The book sentence this word was taken from (source index is 1-based).
        idx = v.get("ex")
        w["_book"] = ""
        if isinstance(idx, int) and 1 <= idx <= len(exs):
            w["_book"] = clean_text(exs[idx - 1])

        key = (T.fold(term), w["lesson"])
        if key in seen:
            continue
        seen[key] = w
        words.append(w)
    return words


def build_lessons(data, words):
    """Lesson metadata: reading text, gap-fill, questions, speaking, grammar."""
    grammar_by_lesson = collections.defaultdict(list)
    for g in data.get("grammar", []):
        if g.get("b") != "GB":
            continue
        for n in (g.get("les") if isinstance(g.get("les"), list) else [g.get("les")]):
            if isinstance(n, int):
                card = {"t": T.norm_ws(g.get("t") or ""), "md": g.get("md") or ""}
                if card not in grammar_by_lesson[n]:
                    grammar_by_lesson[n].append(card)

    counts = collections.Counter(w["lesson"] for w in words)
    lessons = []
    for l in sorted(data.get("gbLessons", []), key=lambda x: x.get("n") or 0):
        n = int(l.get("n") or 0)
        text = []
        for line in (l.get("text") or "").splitlines():
            line = clean_text(re.sub(r"^\(\d+\)\s*", "", line))   # drop the printed line numbers
            if strip_marks(line):
                text.append(line)

        cloze = []
        for t in l.get("test") or []:
            md = strip_marks(t.get("md") or "")
            if md:
                cloze.append(re.sub(r"_{2,}", "_____", md))

        pages = l.get("pg") or []
        lessons.append({
            "book": "gb",
            "n": n,
            "title": T.norm_ws(l.get("t") or f"Les {n}"),
            "page": pages[0] if pages else None,
            "words": counts.get(n, 0),
            "text": text,
            "cloze": cloze,
            "questions": [T.norm_ws(q.get("q") or "") for q in (l.get("q") or []) if q.get("q")],
            "speak": [strip_marks(s.get("line") or "") for s in (l.get("sp") or []) if s.get("line")],
            "kijk": [{"page": k.get("page"), "md": k.get("md") or ""} for k in (l.get("kijk") or []) if k.get("md")],
            "grammar": grammar_by_lesson.get(n, []),
        })
    return lessons


def attach_examples(words, data, curated, sent_fa):
    """Give every word its book sentence plus sentences mined from the lessons."""
    # Sentence pool: the shared exs list plus every lesson's own sentences.
    pool, seen = [], set()
    for s in list(data.get("exs") or []) + [s for l in data.get("gbLessons", []) for s in (l.get("sents") or [])]:
        s = clean_text(s)
        if not usable(s):
            continue
        k = T.fold(s)
        if k in seen:
            continue
        seen.add(k)
        pool.append(s)

    index = collections.defaultdict(list)
    for i, s in enumerate(pool):
        for tok in set(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", s.lower())):
            index[tok].append(i)

    stats = collections.Counter()
    for w in words:
        cands = []
        if w["_book"]:
            cands.append(("book", w["_book"]))

        forms = {w["term"]}
        if w.get("lemma"):
            forms.add(w["lemma"])
        if w.get("verb", {}).get("inf"):
            forms.add(w["verb"]["inf"])
        hits = set()
        for f in forms:
            toks = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", f.lower())
            if not toks:
                continue
            pools = [set(index.get(t, ())) for t in toks]
            for i in (set.intersection(*pools) if pools else ()):
                if T.contains_word(pool[i], f):
                    hits.add(i)
        for s in sorted((pool[i] for i in hits), key=len)[:6]:
            cands.append(("corpus", s))

        for c in curated.get(w["id"], []):
            cands.insert(0, ("authored", c["nl"]))
        fa_by_nl = {T.fold(c["nl"]): c.get("fa", "") for c in curated.get(w["id"], [])}

        picked, used = [], set()
        for src, s in cands:
            k = T.fold(s)
            if not s or k in used:
                continue
            used.add(k)
            picked.append({"nl": s, "src": src, "lvl": level_of(s),
                           "fa": fa_by_nl.get(k) or sent_fa.get(k, "")})
        picked.sort(key=lambda e: (e["lvl"], len(e["nl"])))

        chosen, levels = [], set()
        for e in picked:
            if e["lvl"] not in levels:
                levels.add(e["lvl"])
                chosen.append(e)
        for e in picked:
            if len(chosen) >= 3:
                break
            if e not in chosen:
                chosen.append(e)
        chosen.sort(key=lambda e: (e["lvl"], len(e["nl"])))
        w["ex"] = chosen[:3]
        w.pop("_book", None)

        stats[len(w["ex"])] += 1
        stats["fa"] += sum(1 for e in w["ex"] if e["fa"])
        for e in w["ex"]:
            stats["src:" + e["src"]] += 1
    return stats, len(pool)


def enrich_tr(data):
    """Copy the cross-book lexeme ids onto the Tweede Ronde words."""
    path = f"{OUT}/tr.words.json"
    if not os.path.exists(path):
        return 0
    by_nr = {}
    for v in data["vocab"]:
        if v.get("b") == "TR":
            by_nr["tr-" + str(v["nr"]).zfill(4)] = v
    words = json.load(open(path, encoding="utf-8"))
    n = 0
    for w in words:
        v = by_nr.get(w["id"])
        if not v:
            continue
        for field, key in (("lex", "lexemeId"), ("sense", "senseId")):
            if v.get(key) and w.get(field) != v[key]:
                w[field] = v[key]
                n += 1
        lm = T.norm_ws(v.get("lm") or "")
        if lm and lm != w["term"] and not w.get("lemma"):
            w["lemma"] = lm
    json.dump(words, open(path, "w", encoding="utf-8"), ensure_ascii=False)
    return len(by_nr)


def main(src):
    data = json.load(open(src, encoding="utf-8"))
    exs = [clean_text(s) for s in (data.get("exs") or [])]
    curated, sent_fa = load_curated()

    words = build_words(data, exs)
    stats, pool_size = attach_examples(words, data, curated, sent_fa)
    lessons = build_lessons(data, words)

    os.makedirs(OUT, exist_ok=True)
    os.makedirs("build", exist_ok=True)
    json.dump(words, open(f"{OUT}/gb.words.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"book": "gb", "title": "Het Groene Boek",
               "subtitle": "Nederlands voor anderstaligen — Delftse methode, deel 1",
               "lessons": lessons},
              open(f"{OUT}/gb.lessons.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(words, open(RAW_OUT, "w", encoding="utf-8"), ensure_ascii=False)

    tr_linked = enrich_tr(data)

    print(f"words: {len(words)}   lessons: {len(lessons)}   sentence pool: {pool_size}")
    print("examples per word:", {k: stats[k] for k in sorted(x for x in stats if isinstance(x, int))})
    print("by source:", {k: v for k, v in stats.items() if str(k).startswith("src:")})
    print("with Persian:", stats["fa"], "/", sum(len(w["ex"]) for w in words))
    print("tier:", dict(collections.Counter(w["tier"] for w in words)))
    print("with article:", sum(1 for w in words if w.get("article")),
          "| with lemma:", sum(1 for w in words if w.get("lemma")),
          "| with lexeme id:", sum(1 for w in words if w.get("lex")))
    print("lesson content: texts",
          sum(len(l["text"]) for l in lessons), "| cloze", sum(len(l["cloze"]) for l in lessons),
          "| questions", sum(len(l["questions"]) for l in lessons),
          "| speaking", sum(len(l["speak"]) for l in lessons),
          "| grammar cards", sum(len(l["grammar"]) for l in lessons),
          "| kijk", sum(len(l["kijk"]) for l in lessons))
    print("TR words linked with lexeme ids:", tr_linked)
    print("size:", os.path.getsize(f"{OUT}/gb.words.json") // 1024, "KB words,",
          os.path.getsize(f"{OUT}/gb.lessons.json") // 1024, "KB lessons")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else SRC)
