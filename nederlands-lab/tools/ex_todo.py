"""Emit the next batch of words that still need example sentences.

One line per word: id | term | article | pos | persian | english | existing example.
Ordered by lesson so the front of the book is finished first, and within a
lesson by importance. The batch is written to build/ex_batch.json for ex_add.py.
"""
import json, os, sys

BOOK = os.environ.get("BOOK", "tr")
DATA = f"../data/{BOOK}.words.json"
CURATED = ("curated/examples.curated.json" if BOOK == "tr"
           else f"curated/{BOOK}.examples.curated.json")
BATCH = "build/ex_batch.json"
WANT = 2  # every word should end up with at least this many examples


def pending():
    words = json.load(open(DATA, encoding="utf-8"))
    curated = json.load(open(CURATED, encoding="utf-8")) if os.path.exists(CURATED) else {}
    todo = []
    for w in words:
        have = len(w.get("ex", [])) + len(curated.get(w["id"], []))
        if have < WANT:
            todo.append((w, WANT - have))
    todo.sort(key=lambda t: (t[0]["lesson"], -t[0]["freq"], t[0]["id"]))
    return todo, len(words)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    todo, total = pending()
    os.makedirs("build", exist_ok=True)
    batch = todo[:n]
    json.dump([{"id": w["id"], "need": k} for w, k in batch], open(BATCH, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"# {len(todo)} words still need examples (of {total}). This batch: {len(batch)}")
    print("# reply: <n>|<dutch>|<persian>   (one line per sentence; repeat n for a second sentence)")
    for i, (w, need) in enumerate(batch, 1):
        have = "; ".join(e["nl"] for e in w.get("ex", [])) or "-"
        art = w.get("article") or "-"
        fa = (w.get("faShort") or w.get("fa", ""))[:70]
        print(f'{i}|{w["term"]}|{art}|{w.get("pos","")}|{fa}|{w.get("en","")}|need {need}|have: {have}')
