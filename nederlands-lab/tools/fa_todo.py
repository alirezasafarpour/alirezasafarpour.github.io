"""Emit the next batch of example sentences that still need a Persian translation.

Sentences are ordered by the earliest lesson that uses them, so the front of the
book is completed first. The batch is written to build/fa_batch.json so fa_add.py
can map the numbered answers back to their sentences.
"""
import json, os, sys, collections
import lib_text as T

BOOK = os.environ.get("BOOK", "tr")
DATA = f"../data/{BOOK}.words.json"
SENT_FA = "curated/sentences.fa.json"
REJECT = "curated/rejected.json"
BATCH = "build/fa_batch.json"


def load_done():
    if not os.path.exists(SENT_FA):
        return {}
    return json.load(open(SENT_FA, encoding="utf-8"))


def pending():
    words = json.load(open(DATA, encoding="utf-8"))
    done = {T.fold(k) for k, v in load_done().items() if v and v.strip()}
    if os.path.exists(REJECT):
        done |= {T.fold(k) for k in json.load(open(REJECT, encoding="utf-8"))}
    first_use, users = {}, collections.Counter()
    for w in words:
        for e in w["ex"]:
            if e.get("fa"):
                done.add(T.fold(e["nl"]))   # already translated in the curated layer
                continue
            key = e["nl"]
            users[key] += 1
            prev = first_use.get(key)
            if prev is None or w["lesson"] < prev:
                first_use[key] = w["lesson"]
    todo = [s for s in first_use if T.fold(s) not in done]
    # Earliest lesson first; within a lesson, the most re-used sentences first.
    todo.sort(key=lambda s: (first_use[s], -users[s], len(s)))
    return todo, len(first_use), len(done)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    todo, total, done = pending()
    os.makedirs("build", exist_ok=True)
    # The whole pending list is written, not just the printed slice: a smaller
    # probe run must not renumber the batch a translation pass is working from.
    json.dump(todo, open(BATCH, "w", encoding="utf-8"), ensure_ascii=False)
    batch = todo[:n]
    print(f"# {done}/{total} sentences translated, {len(todo)} remaining. This batch: {len(batch)}")
    for i, s in enumerate(batch, 1):
        print(f"{i}|{s}")
