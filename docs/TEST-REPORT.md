# Test report (v0.5.0)

Date of run: 22 Oct 2026. Environment: headless Chromium (Playwright) driven by scripts, plus Node 22. **No physical devices were used.**

## Executed and passed (3,467 checks, 0 failing in the final run)

**`node tests/run-tests.js`: 3,300 passed** (loads and validates all 312 levels: 12 free + 300 premium in 30 test packs, 33 islands, 936 puzzles each proven solvable by an independent solver; pals/buddy/history saving; profiles: migration of an old save, separate progress per player, 6-player limit, backup export/import, rejection of bad files, deletion rules; pal accessory/colour/nickname sanitising; all 14 accessories drawn)
* 12 levels, 3 islands, unique ids; every one of the 36 puzzles is proven solvable by an independent solver; correct answers are computed from the puzzle numbers.
* Every multi-step answer matches its calculation; validators reject wrong answers (wrong sum, repeated tile, wrong coin count, leading-zero number, non-equivalent fraction, etc.).
* All level text has English and Malay; numbers inside each EN/MS pair agree (one reviewed exception); UI locale files have identical keys and placeholders; every key used in code exists.
* Adaptive rules: start tier follows chosen rank; two clean solves raise a topic one step; 3+ mistakes or helper lowers one step and flags practice; a few mistakes change nothing; booster after two struggles; replay avoids the identical puzzle; help/friendlier thresholds; star rules.
* Save data: garbage, wrong types, out-of-range numbers, bad ids, unknown fields all sanitised; corrupt JSON kept for support; reset keeps language.
* No secrets, network calls, trackers or external URLs in shipped files; premium packs ship no level data; checkout reports "unavailable".

**`tests/e2e.py`: 24 passed** (now includes the name/avatar step of the intro). Starts the game at 360x640 touch, switches to Bahasa Melayu, persists after reload, plays all 12 levels in Malay through real taps (with a wrong attempt first on every second level), rewards saved, 12 companions, demo-complete screen, no console errors, no horizontal overflow.

**`tests/e2e_more.py`: 38 passed** (OS reduced-motion keeps the gentle mascot/sky motion, "Calmer" in Settings stops all of it) (run in free-only mode, as the public demo behaves).

**`tests/e2e_premium.py`: 68 passed** (the full run takes about 15 minutes because of the sweep; `SKIP_SWEEP=1` does a quick run). Free-only mode never requests `packs/` and keeps premium locked even with a hand-edited save; test mode loads 312 levels from 30 packs; the map shows 312 nodes and they read 1 to 312 in order; **music** (on by default, starts only after a tap, menu button and Settings on/off, volume slider scales and saves, off disables the slider); **motion** (menu clouds drift, mascot flies; map clouds drift, map mascot flies); **dashboard skills** (every skill listed with progress and rank) (left to right, rows bottom to top); **players**: greeting, add, switch, separate progress, reload keeps the active player, backup file download, restore as a new player, wrong file rejected, delete cancel/confirm; **pal customisation**: nickname, colour, found accessories (locked ones explain kindly and cost nothing, found ones are worn free), None, survives reload, nickname shown in the collection; the oval EN|BM button is wider than tall, its text fits and it switches language; no overlapping map buttons; all **300** premium levels solved through the UI (tier rotates friendly/standard/challenge by level; the unit tests prove all 600 puzzles solvable); Pal Park (pet reacts, treat costs 3 coins, play is free, too few coins is refused kindly, buddy saved and shown on menu and map, petting never changes coins); dashboard tiles, week chart, islands and skills; no overflow and 44px targets on the new screens at 4 sizes x 2 languages.
* All 36 free puzzles (12 levels x friendly/standard/challenge) solved through the real UI at their intended tier.
* Adaptive behaviour in the live game: friendlier offer after 3 wrong, "Show me how" so a child is never stuck, topic steps down then up, next level's tier follows; coins never reduced by mistakes.
* Hint, pause (Esc closes), double-tap reward protection, text-size / reduced-motion / sound settings, reset cancel and confirm, language switch keeps progress.
* Premium preview is labelled "Premium", states nothing was bought, shows "not available" with no checkout configured, pack not owned, no premium level data.
* Parents area (12 rows), collection (12), keyboard Tab focus and keyboard slider.
* 3 kinds of corrupt save do not crash; progress survives refresh.
* No horizontal overflow on all screens and 12 levels at 320x568, 360x640, 412x915, 768x1024, 1280x800 and 640x360, in both languages (plus 130% text at 320 px, Malay).
* All buttons at least 44 px at 360x640 and 320x568. OS "reduce motion" preference calms animation.

**Round 5 additions.** Unit tests (included in 3,300): a simulated sound engine (nothing before the first tap, a tap wakes it, iOS-style "interrupted" is resumed, music starts and stops, playing while suspended never throws); daily streak rules (rising rewards, 7-day week with the perfect-week bonus, double claim refused, missed day restarts, clock moved backwards never pays, month and year boundaries, garbage dates, save sanitising).
**`tests/e2e_round5.py`: 37 passed** in a real browser with autoplay blocked: the sound engine wakes on the first tap and again after the page was hidden and shown, and music plays; version number and "What's new" in Settings (English and Malay) and the menu note disappearing; the daily gift (button, 7 tiles, claim once, day 7 pays 150 coins, missed day restarts, survives reload, no sideways scroll at 320 and 390 px in both languages); finds (Party hat found on the 3rd finished level and announced, locked hats explain kindly, an older save is migrated, hat worn with one tap); the map path (dashed, curved, outlined, finished steps white, next step highlighted).

## Not verified (round 5)
* **Sound on real phones.** The fix follows known browser behaviour and is tested with a simulated engine and desktop Chromium. It has **not** been tried on a real iPhone or Android phone, where "sound sometimes not working" usually appears. Please test on your phone: open the game, tap once, lock the screen, unlock, tap again.
* The daily gift uses the device clock; a child can change the clock to claim again (acceptable for a coin trickle, but note it if coins ever have real value).
* Levels 213 to 312 are proven mathematically correct and solvable, not proven good teaching; they need a teacher's review in English and Bahasa Melayu.

## Not verified (round 3)
* The 188 generated levels (25 to 212) are proven **mathematically correct and solvable**, not proven **good teaching**: wording is template-based, difficulty progression within a pack is by design, not by testing with children, and Malay needs a teacher.
* Profiles live in one browser on one device (localStorage); clearing site data deletes them. Not tested on real phones, and file download/upload of backups is only tested in desktop Chromium.
* Visual checks of the map, chart labels, profile and dress-up screens were done by looking at headless screenshots at 360 px wide, not on real devices.

* The background music was heard by tests only as scheduled sound events (notes are created, the volume and on/off state change); nobody has judged whether the tune is pleasant, and volume balance on real phone speakers is untested.

## Failed during development and fixed
* The new menu music button squeezed the EN|BM oval so its text overflowed; the top row layout was fixed and re-tested at 320 to 768 px.
* Chart (bar) labels such as "Pink gems" and "Blue gems" ran into each other. Labels now wrap onto two lines and scale with the bar width.
* The map snaked back and forth, so level 13 14 15 appeared above 18 17 16. Levels now read left to right in every row; islands with more than 4 levels use at most 3 per row with more space.
* A test's "Main" button matched the new "Pemain" chip (substring match); the test now matches exactly.
* Multiplication tiles never settled for clicking because a CSS class name clashed with the spinning-gear animation. Renamed.
* Fraction-tank buttons were 33 px wide on a 320 px screen with 8 to 10 parts. Now wrap, minimum 44 px.
* Map header "Pals" label overflowed a round button. Now a normal small button.
* Several test-script mistakes (wrong expectations), corrected; none were game bugs.

## Fixed while building the new features
* The 6-level premium islands reused the 4-node map layout and markers overlapped. They now use a snake layout (test checks no overlap).
* Map header had too many buttons and truncated the title. It now has only "Pals".
* The last free level now continues into Crystal Caves in test mode; the main e2e run uses free-only mode to keep checking the real demo ending.

## Not verified (do not assume these work)
* The premium test puzzles' wording and difficulty have not been reviewed by a teacher.
* Pet animations were checked in headless Chromium only, not on real phones.
* Real phones and tablets (touch feel, iOS Safari quirks, low-end Android speed, battery). Performance has not been measured.
* Screen readers (NVDA, VoiceOver, TalkBack): labels, live regions and focus handling exist but have not been tried. Colour-contrast ratios were not measured with a tool.
* Sound on real devices (Web Audio is used; autoplay rules differ by browser). The game is fully playable with sound off.
* Drag-and-drop: none is needed. Every interaction is tap, slider or buttons (the brief's "tap alternative" is the only mode).
* Offline: no service worker, so offline use is not supported.
* Native-speaker review of Malay; maths content review by a teacher; alignment with the KSSR syllabus; testing with children; Firefox/Safari/Edge runs (only Chromium was run).
* Payments, accounts and secure entitlements: **not implemented**.

## Manual tests to do yourself
1. Open on your own phone (host it or send the folder), play levels 1 to 12 in both languages, rotate the screen mid-puzzle, and note anything awkward or too hard/easy.
2. Watch one child aged 7 to 8 and one aged 11 to 12 play without helping. Note where they get stuck or bored.
3. Turn off the phone's sound; switch on its "reduce motion" and big-text settings; replay.
4. Open it in Safari on iPhone and in Firefox; try keyboard-only on a laptop (Tab, Enter, arrow keys).
5. Close the tab mid-game and reopen: progress should be there; try a private window: the parents page should warn that saving is blocked if the browser forbids it.
6. Ask a Malay-speaking teacher to read every screen (`docs/TRANSLATION-REVIEW.md`).

## Known limitations
* Leaving a level mid-puzzle restarts that puzzle next time (completed levels are always saved). "Pause" keeps the puzzle in place.
* The decorative tick marks inside the fraction-tank picture are fixed and do not match every tank's part count; the numbered gauge below is the accurate one.
* The map fits exactly 4 levels per island; more needs a small layout change.
* Rank names, coin prices of hats and star rules are first guesses to tune after playtests.
