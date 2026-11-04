# Content guide: add questions, levels, translations and premium packs

All text a child sees is either in `js/locales/*.js` (interface) or inside the level files (story, puzzle prompts, hints).
Nothing needs changing in the engine for new content of an existing puzzle type.

## 1. Edit an existing question
Open `js/levels/meadow.js` (or forest/cove). Each level has `tiers: [friendly, standard, challenge]`.
Change numbers in `spec` and update `prompt`, `hint`, `explain` in **both** `en` and `ms`.
Answers are *computed* from `spec`, never typed in separately, so the question and answer cannot disagree.
Then run `node tests/run-tests.js`: it proves the puzzle is solvable and that numbers match between English and Malay.

## 2. Add a level
Copy a `MP.levels.register({...})` block (format documented at the top of `js/levels/registry.js`), then:
* new unique `id` (`m4-1`), next `order` number, `island`, `topic`, `skill`, `scene`, `npc`, a `critter` (collectible) and **three** authored tiers;
* add the skill name to both locale files as `skill.<skill>` (and `topic.<topic>` if new);
* the map has room for 4 levels per island. For more, change `NODE_X/NODE_Y` in `js/app.js`.

Puzzle types available: `numberline, balance, pattern, share, tiles, match, placeValue, digitArrange, coins, tank, shapes, chart, steps`.
Each has a spec shape shown in the existing levels. To add a **new type**: add a checker + solver in `js/validators.js`, a renderer in `js/puzzles.js`, and tests.

## 3. Add or change a translation
* Interface: edit `js/locales/en.js` and `js/locales/ms.js` together. The test fails if a key exists in only one.
* Placeholders like `{n}` must be identical in both languages (tested).
* New language (e.g. Chinese): copy `ms.js` to `zh.js`, translate, register with `MP.i18n.register('zh', …)`, add `'zh'` to `supported` in `js/i18n.js`, add the script to `index.html`, add a button in `langButtons()` (`js/app.js`), and add `zh` to every `{en, ms}` text object (the test lists any missing).
* Mark anything you are unsure about in `docs/TRANSLATION-REVIEW.md` for a native-speaker teacher.

## 4. Add a premium pack (design)
1. Describe it in `js/packs.js` (`free:false`) so it appears in previews.
2. Write its levels in a **separate file that is not in the free bundle** (e.g. `packs/crystal-caves.js`, same format with `pack:'crystal-caves'`).
3. In production your server delivers that file only to paying customers (see `docs/ARCHITECTURE.md`). The `ServerProvider` loads it, then registers the levels. Until that backend exists, do **not** put premium files on the public website: anything in the page's files can be copied.

## Premium packs (test format)

A premium pack is one JavaScript file in `packs/<pack-id>.js` that calls `MP.levels.register({...})` with exactly the same
level format as the free levels (see `packs/crystal-caves.js` for a complete example). To add a pack:
1. Add an entry to `js/packs.js` with `testFile: true`, a `levels` count and (for a new map island) an `island` object
   (`id`, `order`, `npc`, `pack`, `name`, `blurb`). The island `id` must also exist as a theme in `js/art.js` (`BG` backgrounds and the map `THEMES`).
2. Give the level `order` numbers that continue after the previous pack. Levels unlock in order and the map shows them 1, 2, 3 ... left to right,
   rows bottom to top (at most 3 per row on islands with more than 4 levels).
3. New `skill` names need `skill.<name>` in both locale files. Run `node tests/run-tests.js`: it loads `packs/` and validates every puzzle.

### The generator (`tools/mk`)
Levels 25 to 312 were written as Python modules (`p03.py` ... `p30.py`, plus the extra Crystal Caves and Floating Gardens levels in `p_extras.py`),
using helpers in `lib.py` (one per puzzle type: `tiles`, `balance`, `numberline`, `share`, `pattern`, `match`, `placevalue`, `coins`, `tank`,
`chart`, `steps`). The helpers **compute** answers and distractors and refuse impossible puzzles (an `assert` fires), so a typo cannot ship a
wrong answer. To regenerate: `python3 tools/mk/build.py` rewrites `packs/*.js` (do not hand-edit generated parts: they are overwritten).
Constraints of the puzzle types: `match` text is not translated, `share` needs 2 to 5 baskets and at most 30 items, `balance` never targets 0,
`steps` answers are checked against a `calc` expression, chart averages must be whole numbers.
Treat the generated wording as a first draft: it needs a teacher's review in English and Bahasa Melayu.
