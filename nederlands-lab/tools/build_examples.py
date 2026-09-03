"""Attach 2-3 example sentences to every word.

Sources, in order of authority:
  1. book    - a sentence from the lesson's own source paragraph
  2. corpus  - a different sentence mined from the whole book's prose
  3. natural - the dataset's model-authored natural example
  4. authored- hand-written examples from examples.curated.json (Persian included)

Persian translations come from examples.curated.json when present; every sentence
additionally gets a token-level gloss at runtime from the app's own lexicon.
"""
import json, re, os, collections
import lib_text as T
import parse_master as PM

DATA = "../data"
CURATED = "curated/examples.curated.json"
SENT_FA = "curated/sentences.fa.json"
RAW = "build/tr.words.raw.json"


# Markdown, grammar tables and exercise scaffolding leak into the prose blocks;
# none of it reads as a natural Dutch sentence, so it must not become an example.
ARTIFACTS = ("_____", "*", "`", " = ", "|", "->")


def usable(s):
    """True when a mined sentence reads as ordinary running Dutch."""
    if any(a in s for a in ARTIFACTS):
        return False
    if s.endswith(":") or s.endswith(";"):
        return False
    if s.count("-") >= 3 or s.count("?") >= 3:
        return False
    if not re.search(r"[.!?]$", s):
        return False
    # Needs a real clause, not a heading or a bare list of terms.
    return len(s.split()) >= 4 and s.count(",") <= 6


def build_corpus():
    """Every distinct prose sentence in the book, longest-first dedupe."""
    seen, sents = set(), []

    def add(par):
        for s in T.split_sentences((par or "").translate(T._FOLD)):
            s = T.norm_ws(s)
            if not (25 <= len(s) <= 165) or not usable(s):
                continue
            k = T.fold(s)
            if k in seen:
                continue
            seen.add(k)
            sents.append(s)

    for b in PM.parse("src/tweede_ronde_master.md"):
        if b["kind"] in ("text", "exercises", "grammar"):
            for p in PM.paragraphs(b["body"]):
                add(p)
    for w in json.load(open(RAW, encoding="utf-8")):
        add(w["_para"])
    return sents


def index_corpus(sents):
    """token -> sentence indices, so per-word lookup is O(hits) not O(corpus)."""
    idx = collections.defaultdict(list)
    for i, s in enumerate(sents):
        for tok in set(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", s.lower())):
            idx[tok].append(i)
    return idx


def candidates(word, sents, idx, limit=6):
    """Corpus sentences containing the word (or its lemma), shortest first."""
    forms = {word["term"]}
    if word.get("lemma"):
        forms.add(word["lemma"])
    if word.get("verb", {}).get("inf"):
        forms.add(word["verb"]["inf"])
    hits = set()
    for f in forms:
        toks = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+", f.lower())
        if not toks:
            continue
        pools = [set(idx.get(t, ())) for t in toks]
        for i in set.intersection(*pools) if pools else ():
            if T.contains_word(sents[i], f):
                hits.add(i)
    if len(hits) < 3:
        # Thin coverage: also accept inflected/derived forms sharing a long stem,
        # so the learner still sees the word family in real book Dutch.
        for f in forms:
            stem = re.sub(r"(en|te|de|e|s)$", "", f.lower())
            if len(stem) < 5 or " " in f:
                continue
            for tok, ids in idx.items():
                if tok.startswith(stem) and len(tok) - len(stem) <= 4:
                    hits.update(ids)
    out = sorted((sents[i] for i in hits), key=len)
    return out[:limit]


def level_of(s):
    """1 = simple, 2 = everyday, 3 = a bit more advanced."""
    n = len(s)
    if n <= 55:
        return 1
    return 2 if n <= 95 else 3


def assign(word, pool):
    """Pick up to three sentences spread across difficulty levels."""
    picked, used = [], set()
    for src, s in pool:
        k = T.fold(s)
        if not s or k in used:
            continue
        used.add(k)
        picked.append({"nl": s, "src": src, "lvl": level_of(s)})
    picked.sort(key=lambda e: (e["lvl"], len(e["nl"])))
    # Prefer one per level, then fill up to three by ascending difficulty.
    chosen, seen_lvl = [], set()
    for e in picked:
        if e["lvl"] not in seen_lvl:
            seen_lvl.add(e["lvl"])
            chosen.append(e)
    for e in picked:
        if len(chosen) >= 3:
            break
        if e not in chosen:
            chosen.append(e)
    chosen.sort(key=lambda e: (e["lvl"], len(e["nl"])))
    return chosen[:3]


def main():
    words = json.load(open(RAW, encoding="utf-8"))
    curated = {}
    if os.path.exists(CURATED):
        curated = json.load(open(CURATED, encoding="utf-8"))
    # Persian keyed by the Dutch sentence itself, so a sentence shared by several
    # words is translated once and reused everywhere it appears.
    sent_fa = {}
    if os.path.exists(SENT_FA):
        for k, v in json.load(open(SENT_FA, encoding="utf-8")).items():
            if v and v.strip():
                sent_fa[T.fold(k)] = v.strip()
    sents = build_corpus()
    idx = index_corpus(sents)
    print(f"corpus sentences: {len(sents)}")

    stats = collections.Counter()
    for w in words:
        pool = []
        own = T.find_sentence(w["_para"], w["term"])
        if own and usable(own):
            pool.append(("book", own))
        for s in candidates(w, sents, idx):
            if not own or T.fold(s) != T.fold(own):
                pool.append(("corpus", s))
        if w["_extra"] and usable(w["_extra"]):
            pool.append(("natural", w["_extra"]))
        for c in curated.get(w["id"], []):
            pool.insert(0, ("authored", c["nl"]))
        ex = assign(w, pool)
        # Attach curated Persian where the sentence matches one we authored.
        fa_by_nl = {T.fold(c["nl"]): c.get("fa", "") for c in curated.get(w["id"], [])}
        for e in ex:
            fa = fa_by_nl.get(T.fold(e["nl"])) or sent_fa.get(T.fold(e["nl"]))
            if fa:
                e["fa"] = fa
        w["ex"] = ex
        stats[len(ex)] += 1
        stats["fa"] += sum(1 for e in ex if e.get("fa"))
        for e in ex:
            stats["src:" + e["src"]] += 1
        w.pop("_para", None)
        w.pop("_extra", None)
        if w.get("printed") == w["term"]:
            del w["printed"]          # only keep the printed form when it differs
        if w.get("faShort") == w.get("fa"):
            del w["faShort"]

    json.dump(words, open(f"{DATA}/tr.words.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("examples per word:", {k: stats[k] for k in sorted(x for x in stats if isinstance(x, int))})
    print("by source:", {k: v for k, v in stats.items() if str(k).startswith("src:")})
    print("with Persian:", stats["fa"])
    print("size:", os.path.getsize(f"{DATA}/tr.words.json") // 1024, "KB")


if __name__ == "__main__":
    main()
