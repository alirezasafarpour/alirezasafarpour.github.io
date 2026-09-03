# Data pipeline

Turns the certified source files into the JSON the app loads.

| Script | Purpose |
|---|---|
| `lib_text.py` | Dutch sentence splitting, punctuation folding, whole-word matching |
| `parse_master.py` | Parses the Tweede Ronde source markdown into per-lesson blocks |
| `build_tr.py` | Normalises the Tweede Ronde vocabulary + lessons |
| `build_examples.py` | Mines example sentences and merges curated Persian translations |
| `build_gb.py` | Normalises the Groen Boek dataset into the same schema |
| `ex_todo.py` / `ex_add.py` | Batch workflow for authoring example sentences |
| `fa_todo.py` / `fa_add.py` | Batch workflow for Persian sentence translations |

Run in order: `build_tr.py` → `build_examples.py`, and `build_gb.py` independently.

## Importing the Groen Boek dataset

```
cp /path/to/nederlands_lab_dataset_V2.json src/
python3 build_gb.py
```

`build_gb.py` does not assume a fixed export shape. It finds the list of records
wherever it sits in the JSON, then matches each record's fields against the
aliases in `ALIASES` (checked at any nesting depth). Read the report it prints:
it names the key the entries were found under, the coverage of every mapped
field, and every source field it did **not** map — so add an alias if something
useful was skipped, rather than discovering the gap in the app.

Persian translations already in `curated/sentences.fa.json` are reused for any
Groen Boek sentence that matches, and hand-written Groen Boek examples live in
`curated/gb.examples.curated.json`.

`src/` holds the source files (large, not needed at runtime).
`curated/examples.curated.json` holds hand-written example sentences and Persian
translations keyed by word id; `build_examples.py` merges them in, so rebuilding
never discards them.
