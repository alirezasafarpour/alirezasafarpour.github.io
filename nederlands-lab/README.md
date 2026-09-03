# Nederlands Lab

A Dutch vocabulary trainer for the two Delftse-methode books — **Het Groene Boek**
(deel 1) and **Tweede Ronde** (deel 2) — with Persian meanings, example sentences,
spaced repetition and cross-device sync.

Static site, no build step. Open `index.html` from any web server, or visit
`https://alirezasafarpour.github.io/nederlands-lab/`.

---

## The learning method

The Groen Boek / Delftse rhythm is the foundation, and Tweede Ronde is integrated
into the same flow rather than bolted on beside it. Every word climbs five stages:

| Stage | Name | What it means | Exercise |
|---|---|---|---|
| 0 | nieuw | not yet seen | — |
| 1 | kennismaking | met the word in context | intro card |
| 2 | herkennen | recognises the meaning | multiple choice NL → FA |
| 3 | oproepen | recognises the Dutch form | multiple choice FA → NL |
| 4 | toepassen | can produce and use it | typing / fill in the blank |
| 5 | beheerst | retained over long intervals | spaced review |

**Learn mode** follows the book's intensive rhythm: meet a batch of four new words,
then drill that same batch straight away — recognition first, then production —
before moving to the next batch. Due reviews are always cleared first so nothing
that is slipping gets buried behind new material.

A word answered wrongly comes back **three to five cards later in the same session**
and again sooner on later days; a word answered easily several times in a row
stretches out fast and stops competing for attention.

## Study modes

Learn · Review · Flashcards · Multiple choice (both directions) · Type the answer ·
Fill in the blank · Listening · Difficult words · Favourites, plus per-lesson practice
and "practise this search result" from the vocabulary browser.

## Example sentences

Every word carries up to three example sentences, ordered simple → everyday →
slightly more advanced, each tagged with where it came from:

- **uit het boek** — a sentence lifted from the book's own text for that word, or
  mined from the rest of the book's prose. Authentic Dutch, no invention.
- **voorbeeld** — a natural example sentence from the vocabulary dataset.

Persian support works on two levels: a full translation where one has been authored,
and **tap-to-gloss** on every sentence — tap any Dutch word and the Persian meaning
appears, resolved from the combined lexicon of both books (including common
inflections). That means no example sentence is ever left without Persian help.

## Progress and sync

Progress is never only in localStorage:

1. **IndexedDB** on the device (primary), with a localStorage mirror as a backup.
2. **Supabase** (optional) — one JSONB row per user, synced on sign-in, every
   90 seconds, on tab focus, and after every session.
3. **Export / import** JSON files from Settings → Back-up.

Merging is per-word by timestamp, so studying offline on your phone and then on your
laptop keeps both sides' work; only the same word touched on both devices resolves
last-write-wins.

Persisted: learned words, stage, ease, interval and due date, correct/wrong counts,
lapses, difficult and favourite flags, lesson position per book, daily statistics,
streak and last activity.

### Setting up sync

1. Create a free project at [supabase.com](https://supabase.com).
2. Open **SQL Editor → New query**, paste [`supabase/schema.sql`](supabase/schema.sql), run it.
3. In the app: **Instellingen → Supabase koppelen**, paste the **Project URL** and
   **anon public key** from *Project Settings → API*.
4. Create an account (email + password, or a magic link) and sign in on each device.

The anon key is meant to be public — row-level security in the schema is what keeps
each account's data private. Nothing is committed to this repository; the keys live
in the browser's localStorage per device.

If you use magic links, add `https://alirezasafarpour.github.io/nederlands-lab/` to
**Authentication → URL Configuration → Redirect URLs** in Supabase.

## Data

| File | Contents |
|---|---|
| `data/tr.words.json` | Tweede Ronde vocabulary, 2333 entries |
| `data/tr.lessons.json` | 45 lessons: titles, reading texts, gap-fill passages |
| `data/gb.words.json` | Het Groene Boek vocabulary |
| `data/gb.lessons.json` | Het Groene Boek lessons |

A book whose files are missing simply does not appear; the app still runs on the
other one.

### Word schema

```jsonc
{
  "id": "tr-0002",          // stable, used as the progress key — never renumber
  "book": "tr",             // "gb" | "tr"
  "lesson": 1,
  "term": "cursist",        // clean headword
  "printed": "cursist (de)",// only when the book prints it differently
  "article": "de",          // de | het
  "plural": "cursisten",
  "fa": "…",                // full Persian meaning
  "faShort": "…",           // short gloss for cards and lists
  "en": "student",
  "pos": "zelfstandig naamwoord",
  "cefr": "A2-B1",
  "freq": 4,                // 1-5 importance
  "speak": 3,               // 1-5 spoken value
  "tier": "USEFUL",         // ESSENTIAL | USEFUL | BOOK
  "lemma": "…", "equiv": "…", "prep": "…", "hint": "…",
  "verb": { "inf": "…", "pp": "…", "aux": "hebben" },
  "colloc": [], "combos": [], "syn": [], "ant": [],
  "ex": [ { "nl": "…", "fa": "…", "lvl": 1, "src": "book" } ]
}
```

`ex[].lvl` is 1 (simple) to 3 (advanced); `ex[].src` is `book`, `corpus`, `natural`
or `authored`. Only `id`, `book`, `lesson`, `term` and `fa` are required.

### Rebuilding the data

```
cd tools
python3 build_tr.py        # normalise source JSON + parse the lesson markdown
python3 build_examples.py  # mine example sentences, attach curated Persian
python3 build_gb.py        # normalise the Groen Boek dataset
```

Curated example sentences and their Persian translations live in
`tools/curated/examples.curated.json`, keyed by word id, and are merged in by
`build_examples.py` — so regenerating never loses hand-written work.

## Layout

```
index.html              app shell
sw.js                   offline cache (shell cache-first, data stale-while-revalidate)
assets/css/app.css      design system
assets/js/
  main.js               bootstrap + hash router
  core/util.js          DOM, text, bidi and date helpers
  core/store.js         IndexedDB progress store + merge logic
  core/srs.js           spaced repetition
  core/data.js          dataset loading, search, queue building
  core/sync.js          Supabase auth + sync (no SDK, direct REST)
  core/audio.js         Dutch text-to-speech
  ui/                   dashboard, books, browse, stats, settings, session, components
data/                   vocabulary and lesson JSON
supabase/schema.sql     database + row-level security
tools/                  Python data pipeline
```

## Notes

- Persian is rendered RTL with embedded Dutch isolated in `<bdi>`, so quotes and
  slashes around a Latin word stay where they belong. Dutch is always LTR.
- Listening exercises use the browser's speech synthesis. Install a Dutch system
  voice for good pronunciation; without one, the app falls back gracefully.
- Keyboard: `1`–`4` choose an option, `Enter` submits and advances, `Space` flips a
  flashcard, `Esc` leaves a session.
