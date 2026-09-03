# Data pipeline

Turns the certified source files into the JSON the app loads.

| Script | Purpose |
|---|---|
| `lib_text.py` | Dutch sentence splitting, punctuation folding, whole-word matching |
| `parse_master.py` | Parses the Tweede Ronde source markdown into per-lesson blocks |
| `build_tr.py` | Normalises the Tweede Ronde vocabulary + lessons |
| `build_examples.py` | Mines example sentences and merges curated Persian translations |
| `build_gb.py` | Normalises the Groen Boek dataset into the same schema |

Run in order: `build_tr.py` → `build_examples.py`, and `build_gb.py` independently.

`src/` holds the source files (large, not needed at runtime).
`curated/examples.curated.json` holds hand-written example sentences and Persian
translations keyed by word id; `build_examples.py` merges them in, so rebuilding
never discards them.
