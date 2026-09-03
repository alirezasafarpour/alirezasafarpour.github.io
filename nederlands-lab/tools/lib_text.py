"""Shared text utilities for the Nederlands Lab data pipeline."""
import re
import unicodedata

# Dutch abbreviations whose full stop must not end a sentence.
ABBR = {
    "ca", "bijv", "bv", "enz", "etc", "nr", "blz", "dhr", "mevr", "mw", "dr", "drs",
    "ir", "ing", "mr", "prof", "o.a", "d.w.z", "m.a.w", "z.g", "t.o.v", "a.u.b",
    "jl", "e.d", "i.p.v", "n.a.v", "b.v", "St", "Sint", "km", "kg", "nl",
}
_SENT_SPLIT = re.compile(r"(?<=[.!?…])[\s ]+(?=[«“\"'(\[A-ZÀ-ÖØ-Þ0-9])")
_WS = re.compile(r"[\s ]+")

# Curly punctuation the source book uses -> straight equivalents for matching.
_FOLD = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", " ": " "})


def norm_ws(s):
    return _WS.sub(" ", (s or "").strip())


def fold(s):
    """Punctuation-folded, casefolded form used for matching only."""
    return norm_ws((s or "").translate(_FOLD)).casefold()


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if not unicodedata.combining(c))


def split_sentences(text):
    """Split a Dutch paragraph into sentences, respecting common abbreviations."""
    text = norm_ws(text)
    if not text:
        return []
    parts = _SENT_SPLIT.split(text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # Re-attach when the previous chunk ended on a known abbreviation.
        if out:
            tail = re.search(r"([A-Za-zÀ-ÿ.]+)\.$", out[-1])
            if tail and tail.group(1).strip(".") in ABBR:
                out[-1] = out[-1] + " " + p
                continue
        out.append(p)
    return out


_WORD_CHARS = "A-Za-zÀ-ÖØ-öø-ÿ"


def word_regex(surface):
    """Whole-word (or whole-phrase) regex for a Dutch surface form."""
    tokens = [re.escape(t) for t in re.split(r"[\s ]+", norm_ws(surface)) if t]
    if not tokens:
        return None
    body = r"[\s ]+".join(tokens)
    return re.compile(rf"(?<![{_WORD_CHARS}]){body}(?![{_WORD_CHARS}])", re.IGNORECASE)


def contains_word(haystack, surface):
    rx = word_regex(surface)
    if not rx:
        return False
    return bool(rx.search((haystack or "").translate(_FOLD)))


def find_sentence(paragraph, surface, max_len=190):
    """Pick the best single sentence from `paragraph` that contains `surface`.

    Prefers sentences that are complete, reasonably short and actually contain the
    word as a whole word. Returns None when nothing suitable is found.
    """
    sents = split_sentences((paragraph or "").translate(_FOLD))
    hits = [s for s in sents if contains_word(s, surface)]
    if not hits:
        return None
    # Shortest sentence that still reads as a full sentence wins.
    hits.sort(key=lambda s: (len(s) > max_len, len(s)))
    best = hits[0]
    return best if len(best) <= 320 else None
