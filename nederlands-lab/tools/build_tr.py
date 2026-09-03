"""Build the app-ready Tweede Ronde dataset from the certified source files.

Outputs (into ../data/):
  tr.words.json    - normalised vocabulary entries
  tr.lessons.json  - lesson metadata, reading texts and book cloze passages
"""
import json, re, os, collections
import lib_text as T
import parse_master as PM

SRC_JSON = "src/tweede_ronde_raw.json"
SRC_MD = "src/tweede_ronde_master.md"
OUT = "../data"

ARTICLE_RE = re.compile(r"^(.*?)\s*\((de|het)\)\s*$", re.I)
EQUIV_RE = re.compile(r"^(.*?)\s*=\s*(.+)$")
PLACEHOLDER_EXPL = "In deze les betekent dit ongeveer"

# Compact part-of-speech labels; the source uses long descriptive strings.
POS_MAP = {
    "lexical item (surface form)": "woord",
    "noun": "zelfstandig naamwoord",
    "adverb / discourse word": "bijwoord",
    "phrase / expression": "uitdrukking",
    "verb / infinitive-like form": "werkwoord",
    "verb": "werkwoord",
    "proper noun / name": "eigennaam",
    "fixed expression / equivalence": "vaste uitdrukking",
    "verb/prepositional expression": "werkwoord + voorzetsel",
    "adjective/formula": "bijvoeglijk naamwoord",
}


def clean_surface(raw):
    """Split the printed headword into (term, article, equivalence)."""
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


def short_persian(deep):
    """First clause of the deep Persian gloss, for compact cards."""
    s = T.norm_ws(deep)
    if not s:
        return ""
    head = re.split(r"[؛;]", s)[0]
    return head if len(head) <= 60 else T.norm_ws(re.split(r"[،,]", head)[0])


# The dataset fills unwritten example slots with instruction templates rather
# than sentences; these are not usable as example material.
PLACEHOLDER_STARTS = ("Gebruik", "Probeer", "Schrijf", "Maak een zin", "Bedenk")
PLACEHOLDER_MARKERS = (
    "korte, natuurlijke Nederlandse zin",
    "in een eigen antwoord te gebruiken",
    "in een zin over je eigen situatie",
    "te gebruiken.",
)


def is_placeholder(x):
    x = (x or "").strip()
    if not x:
        return True
    if x.startswith(PLACEHOLDER_STARTS):
        return True
    return any(m in x for m in PLACEHOLDER_MARKERS)


def build_words():
    raw = json.load(open(SRC_JSON, encoding="utf-8"))
    out, seen = [], {}
    for e in raw["entries"]:
        src, L = e["source"], e["learning"]
        term, art, equiv = clean_surface(src["dutch"])
        if not term:
            continue
        art = art or L.get("article")
        expl = L.get("simple_dutch_explanation") or ""
        if PLACEHOLDER_EXPL in expl:
            expl = ""
        plural = L.get("plural") or ""
        if "not applicable" in plural or "not source-derived" in plural:
            plural = ""
        vm = L.get("verb_morphology") or {}
        verb = None
        if vm.get("applicable"):
            aux = (vm.get("auxiliary") or "").split(" (")[0] or None
            verb = {k: v for k, v in (
                ("inf", vm.get("infinitive")),
                ("pp", vm.get("perfect_participle")),
                ("aux", aux),
            ) if v}
        colloc = [T.norm_ws(c) for c in (L.get("collocations") or []) if T.norm_ws(c)]
        combos = [T.norm_ws(c) for c in (L.get("common_combinations") or []) if T.norm_ws(c)]
        # Drop collocations that are just the headword repeated.
        colloc = [c for c in colloc if T.fold(c) != T.fold(term)]
        combos = [c for c in combos if T.fold(c) != T.fold(term) and "+" not in c]

        w = {
            "id": "tr-" + src["entry_id"].split("-")[1],
            "book": "tr",
            "lesson": src["lesson"],
            "term": term,
            "printed": T.norm_ws(src["dutch"]),
            "fa": T.norm_ws(L.get("persian_meaning_deep") or ""),
            "faShort": short_persian(L.get("persian_meaning_deep")),
            "en": T.norm_ws(src.get("english") or ""),
            "pos": POS_MAP.get(L.get("part_of_speech") or "", L.get("part_of_speech") or ""),
            "cefr": L.get("cefr_estimate") or "",
            "freq": L.get("frequency_importance_1_5") or 3,
            "speak": L.get("speaking_value_1_5") or 3,
            "tier": L.get("classification") or "USEFUL",
            "page": src.get("printed_page"),
        }
        for k, v in (("article", art), ("plural", plural), ("equiv", equiv), ("hint", expl),
                     ("lemma", L.get("lemma") if L.get("lemma") != term else None),
                     ("prep", L.get("fixed_preposition")), ("verb", verb)):
            if v:
                w[k] = v
        for k, v in (("colloc", colloc[:4]), ("syn", [T.norm_ws(s) for s in (L.get("synonyms") or [])][:4]),
                     ("ant", [T.norm_ws(s) for s in (L.get("antonyms") or [])][:3]),
                     ("combos", combos[:3])):
            if v:
                w[k] = v
        # Raw material for the example pipeline; consumed by build_examples.py.
        w["_para"] = T.norm_ws(L.get("source_example") or "")
        w["_extra"] = "" if is_placeholder(L.get("extra_natural_example")) else T.norm_ws(L["extra_natural_example"])

        key = (T.fold(term), src["lesson"])
        if key in seen:  # same word listed twice on one lesson's page
            prev = seen[key]
            if len(w["fa"]) > len(prev["fa"]):
                prev.update({k: v for k, v in w.items() if k != "id"})
            continue
        seen[key] = w
        out.append(w)
    return out


def build_lessons(words):
    blocks = PM.parse(SRC_MD)
    counts = collections.Counter(w["lesson"] for w in words)
    titles, pages = {}, {}
    for b in blocks:
        titles.setdefault(b["lesson"], b["title"])
        pages.setdefault(b["lesson"], b["page"])
    lessons = []
    for n in sorted(counts):
        texts, cloze = [], []
        for b in blocks:
            if b["lesson"] != n:
                continue
            paras = [p for p in PM.paragraphs(b["body"]) if len(p) > 40]
            if b["kind"] == "text":
                texts.extend(paras)
            elif b["kind"] == "cloze":
                cloze.extend(p for p in paras if "_____" in p)
        lessons.append({
            "book": "tr", "n": n,
            "title": titles.get(n, f"Les {n}"),
            "page": pages.get(n),
            "words": counts[n],
            "text": texts,
            "cloze": cloze,
        })
    return lessons


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs("build", exist_ok=True)
    words = build_words()
    lessons = build_lessons(words)
    json.dump(words, open("build/tr.words.raw.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"book": "tr", "title": "Tweede Ronde",
               "subtitle": "Nederlands voor buitenlanders — Delftse methode, deel 2",
               "lessons": lessons},
              open(f"{OUT}/tr.lessons.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(f"words: {len(words)}  lessons: {len(lessons)}")
    print("with article:", sum(1 for w in words if w.get("article")))
    print("with equiv:", sum(1 for w in words if w.get("equiv")))
    print("with hint:", sum(1 for w in words if w.get("hint")))
    print("with extra example:", sum(1 for w in words if w["_extra"]))
    print("reading paragraphs:", sum(len(l["text"]) for l in lessons))
    print("cloze paragraphs:", sum(len(l["cloze"]) for l in lessons))
    print("lessons missing text:", [l["n"] for l in lessons if not l["text"]])
