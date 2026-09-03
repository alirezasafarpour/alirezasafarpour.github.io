"""Merge numbered Persian translations back into curated/sentences.fa.json.

Reads `index|persian` lines on stdin, mapping each index against the batch that
fa_todo.py last emitted. Existing translations are never overwritten silently:
a repeat index updates the entry and is reported.
"""
import json, os, sys

SENT_FA = "curated/sentences.fa.json"
BATCH = "build/fa_batch.json"

batch = json.load(open(BATCH, encoding="utf-8"))
store = json.load(open(SENT_FA, encoding="utf-8")) if os.path.exists(SENT_FA) else {}

added = updated = skipped = 0
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    idx, _, fa = line.partition("|")
    fa = fa.strip()
    try:
        i = int(idx.strip())
    except ValueError:
        skipped += 1
        continue
    if not (1 <= i <= len(batch)) or not fa:
        skipped += 1
        continue
    key = batch[i - 1]
    if key in store and store[key] != fa:
        updated += 1
    elif key not in store:
        added += 1
    store[key] = fa

os.makedirs("curated", exist_ok=True)
json.dump(store, open(SENT_FA, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
print(f"added {added}, updated {updated}, skipped {skipped}; total stored {len(store)}")
