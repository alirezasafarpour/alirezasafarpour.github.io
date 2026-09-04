#!/usr/bin/env python3
"""Build the grammar course JSON from the authored Python modules.

    cd tools && python3 build_grammar.py

Writes data/grammar.a0.json … grammar.b1.json and refuses to write anything if
the curriculum does not check out — a broken exercise should never reach a
learner.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "grammar"))
OUT = os.path.join(HERE, "..", "data")

import _kit  # noqa: E402

# Importing the content modules registers everything with the kit.
import a0  # noqa: E402,F401
import a1  # noqa: E402,F401
import a1b  # noqa: E402,F401
import a2  # noqa: E402,F401
import a2b  # noqa: E402,F401
import b1  # noqa: E402,F401
import b1b  # noqa: E402,F401
import extra  # noqa: E402,F401  (audit additions)

LEVELS = ["A0", "A1", "A2", "B1"]


def audit(parts):
    """Sanity checks that span the whole course, not just one lesson."""
    notes = []
    seen_lessons = set()
    seen_modules = set()
    concept_ids = {c["id"] for p in parts for c in p["concepts"]}
    taught = set()

    for part in parts:
        for m in part["modules"]:
            if m["id"] in seen_modules:
                notes.append(f"duplicate module id {m['id']}")
            seen_modules.add(m["id"])
        for l in part["lessons"]:
            if l["id"] in seen_lessons:
                notes.append(f"duplicate lesson id {l['id']}")
            seen_lessons.add(l["id"])
            taught.update(l["concepts"])
            for cid in l["concepts"]:
                if cid not in concept_ids:
                    notes.append(f"{l['id']}: concept {cid} is not registered")
            # Every lesson should give the learner something to do at each of
            # the three difficulty shapes: recognise, build, produce.
            modes = {e["mode"] for e in l["exercises"]}
            if "choice" not in modes:
                notes.append(f"{l['id']}: no recognition (choice) exercise")
            if not ({"input", "build"} & modes):
                notes.append(f"{l['id']}: nothing the learner has to produce")
            for e in l["exercises"]:
                if e["mode"] == "choice" and e["a"] not in e.get("options", []):
                    notes.append(f"{l['id']}: choice answer not in options: {e['q']!r}")
                if e["mode"] == "build":
                    tiles = sorted(e.get("tiles", []))
                    if tiles != sorted(e["a"].split()):
                        notes.append(f"{l['id']}: build tiles do not match answer: {e['a']!r}")
                if not e.get("why"):
                    notes.append(f"{l['id']}: exercise without explanation: {e['q']!r}")
                if len(e.get("options", [])) > 4:
                    notes.append(f"{l['id']}: more than four options: {e['q']!r}")

    for cid in concept_ids - taught:
        notes.append(f"concept {cid} is never taught by a lesson")
    return notes


def stats(parts):
    lessons = [l for p in parts for l in p["lessons"]]
    exercises = [e for l in lessons for e in l["exercises"]]
    kinds = {}
    for e in exercises:
        kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    return {
        "modules": sum(len(p["modules"]) for p in parts),
        "lessons": len(lessons),
        "concepts": sum(len(p["concepts"]) for p in parts),
        "exercises": len(exercises),
        "examples": sum(len(l["examples"]) for l in lessons),
        "contrasts": sum(len(l["contrast"]) for l in lessons),
        "kinds": dict(sorted(kinds.items(), key=lambda kv: -kv[1])),
    }


def main():
    parts = [_kit.dump(level) for level in LEVELS]
    problems = _kit.problems() + audit(parts)

    if problems:
        print(f"{len(problems)} problem(s) — nothing written:\n")
        for p in problems[:60]:
            print("  -", p)
        if len(problems) > 60:
            print(f"  … and {len(problems) - 60} more")
        return 1

    os.makedirs(OUT, exist_ok=True)
    for part in parts:
        path = os.path.join(OUT, f"grammar.{part['level'].lower()}.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(part, fh, ensure_ascii=False, separators=(",", ":"))
        size = os.path.getsize(path) / 1024
        print(f"{os.path.basename(path):24s} "
              f"{len(part['modules']):2d} modules  "
              f"{len(part['lessons']):3d} lessons  "
              f"{sum(len(l['exercises']) for l in part['lessons']):4d} exercises  "
              f"{size:6.1f} kB")

    s = stats(parts)
    print("\ntotal: {modules} modules · {lessons} lessons · {concepts} concepts · "
          "{exercises} exercises · {examples} examples · {contrasts} mistake pairs".format(**s))
    print("exercise kinds:", ", ".join(f"{k}×{v}" for k, v in s["kinds"].items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
