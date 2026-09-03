"""Parse the Tweede Ronde source master markdown into per-lesson content blocks.

The master file is organised as one `## Printed page N` section per scanned page.
Inside a section, `### ` sub-headings name the kind of content, which is far more
reliable than the page heading, so blocks are the unit we extract.
"""
import re
from lib_text import norm_ws

SECTION = re.compile(r"^## Printed pages? ([0-9–\-]+) — scans? ([0-9,\s–\-]+)\s*$", re.M)
HEADING = re.compile(r"^\*\*Les (\d+) — (.+?)\*\*\s*$", re.M)
SUBHEAD = re.compile(r"^### (.+?)\s*$", re.M)

# Sub-heading text -> content kind. Checked as ordered substring rules.
KIND_RULES = [
    ("source reference", "ref"),
    ("woordenlijst", "wordlist"),
    ("gatentekst", "cloze"),
    ("invuloefening", "cloze"),
    ("reading text", "text"),
    ("grammatica", "grammar"),
    ("grammar", "grammar"),
    ("visual content", "visual"),
    ("source figure", "visual"),
    ("exercises", "exercises"),
]


def classify(label, tail="", body=""):
    """Classify a block. `label` (### sub-heading) wins; otherwise fall back to the
    page heading tail, then to the shape of the body itself."""
    for source in (label, tail):
        low = (source or "").lower()
        for needle, kind in KIND_RULES:
            if needle in low:
                return kind
        if low and ("oefening" in low or "vragen" in low or "opdracht" in low):
            return "exercises"
        if low and ("plattegrond" in low or "kaart" in low or "formulier" in low):
            return "visual"
    rows = [ln for ln in body.splitlines() if ln.strip().startswith("|")]
    if len(rows) >= 4 and sum(ln.count("|") for ln in rows) / max(len(rows), 1) >= 5:
        return "wordlist"
    if body.count("_____") >= 5:
        return "cloze"
    if re.search(r"^\s*\d+\.\s", body, re.M) and body.count("?") >= 3:
        return "exercises"
    return "text"


def parse(path):
    """Yield {lesson, title, page, kind, label, body} blocks in source order."""
    raw = open(path, encoding="utf-8").read()
    blocks = []
    marks = list(SECTION.finditer(raw))
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(raw)
        section = raw[m.end():end]
        h = HEADING.search(section)
        if not h:
            continue
        lesson = int(h.group(1))
        bits = [b.strip() for b in re.split(r"\s+—\s+", h.group(2))]
        title, tail = bits[0], " ".join(bits[1:])
        page = m.group(1)
        rest = section[h.end():]
        subs = list(SUBHEAD.finditer(rest))
        spans = []
        if not subs or subs[0].start() > 0:
            lead = rest[:subs[0].start() if subs else len(rest)]
            spans.append(("", lead))
        for j, s in enumerate(subs):
            stop = subs[j + 1].start() if j + 1 < len(subs) else len(rest)
            spans.append((s.group(1), rest[s.end():stop]))
        for label, body in spans:
            lines = [ln for ln in body.splitlines() if not ln.startswith(">") and ln.strip() != "---"]
            text = "\n".join(lines).strip()
            if not text:
                continue
            blocks.append({
                "lesson": lesson, "title": title, "page": page,
                "kind": classify(label, tail, text), "label": label.strip(), "body": text,
            })
    return blocks


def paragraphs(body):
    """Prose paragraphs only: no tables, headings, list items or code fences."""
    out = []
    for block in re.split(r"\n\s*\n", body):
        b = block.strip()
        if not b or b.startswith("|") or b.startswith("#") or b.startswith("```"):
            continue
        if re.match(r"^\s*(\d+\.|[-*])\s", b):
            continue
        b = re.sub(r"\*\*(.+?)\*\*", r"\1", b)  # drop grammar bolding
        out.append(norm_ws(b))
    return out


if __name__ == "__main__":
    import collections, json
    bl = parse("src/tweede_ronde_master.md")
    print("blocks:", len(bl), "| lessons:", len({b['lesson'] for b in bl}))
    print("kinds:", collections.Counter(b["kind"] for b in bl).most_common())
    for k in ("text", "cloze"):
        tot = sum(len("".join(paragraphs(b["body"]))) for b in bl if b["kind"] == k)
        print(f"  {k}: {tot} prose chars over {sum(1 for b in bl if b['kind']==k)} blocks")
    t1 = [b for b in bl if b["lesson"] == 1 and b["kind"] == "text"]
    print("L1 text blocks:", [(b["label"], len(b["body"])) for b in t1])
    c1 = [b for b in bl if b["lesson"] == 3 and b["kind"] == "cloze"]
    print("L3 cloze sample:", json.dumps(paragraphs(c1[0]["body"])[:1], ensure_ascii=False)[:300] if c1 else None)
