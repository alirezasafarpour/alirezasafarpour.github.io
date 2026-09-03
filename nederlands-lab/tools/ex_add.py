"""Merge authored example sentences into curated/examples.curated.json.

Reads `index|dutch|persian` lines on stdin, mapping the index against the batch
that ex_todo.py last emitted. Repeating an index adds a second sentence for that
word. Existing curated sentences for a word are kept; duplicates are ignored.
"""
import json, os, sys

CURATED = "curated/examples.curated.json"
BATCH = "build/ex_batch.json"

batch = json.load(open(BATCH, encoding="utf-8"))
store = json.load(open(CURATED, encoding="utf-8")) if os.path.exists(CURATED) else {}

added = skipped = dupes = 0
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 3:
        skipped += 1
        continue
    idx, nl, fa = parts[0], parts[1], parts[2]
    try:
        i = int(idx)
    except ValueError:
        skipped += 1
        continue
    if not (1 <= i <= len(batch)) or not nl or not fa:
        skipped += 1
        continue
    wid = batch[i - 1]["id"]
    bucket = store.setdefault(wid, [])
    if any(e["nl"].casefold() == nl.casefold() for e in bucket):
        dupes += 1
        continue
    bucket.append({"nl": nl, "fa": fa})
    added += 1

os.makedirs("curated", exist_ok=True)
json.dump(store, open(CURATED, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
print(f"added {added}, duplicates {dupes}, skipped {skipped}; words with curated examples: {len(store)}")
