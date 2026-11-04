# Mathipelago: The Number Islands (prototype v0.1)

A bilingual (English / Bahasa Melayu) maths adventure for ages 7 to 12. A free demo with 3 islands and 12 puzzles
is included; paid island packs are designed for but **not implemented** (no checkout exists in this build).
"Mathipelago" is a working name. Run a trademark search before launch.

## Play it on Windows (no installs needed)

1. Unzip the folder, for example to `C:\Games\mathipelago`.
2. Double-click **`index.html`**. It opens in your browser and works.
3. Optional: double-click **`Start-Game.bat`**. If Python is installed it starts a small local server and opens
   `http://localhost:8000/index.html`, which behaves like a real website.

Saves are stored per browser. A file opened from disk and the same game from `localhost` keep separate saves.

## Put it on your website (static hosting)

The demo needs no server code. Upload the whole folder (keep the structure) to any static host:
cPanel/shared hosting, Netlify, Cloudflare Pages, GitHub Pages, etc.

* Shared hosting: upload the folder contents to `public_html/maths/` with the file manager or FTP. Visit `https://yoursite.com/maths/`.
* Netlify / Cloudflare Pages: drag the folder into their "deploy" page.
* Embed inside an existing page: `<iframe src="/maths/index.html" title="Mathipelago" style="width:100%;height:85vh;border:0" allow="fullscreen"></iframe>`
  (a dedicated page is better on phones).
* Edit **`js/config.js`**: set `homeUrl` (the "Back to website" button), `supportEmail`, and later `checkoutPageUrl`.
* Serve over HTTPS. If you change files after launch, ask visitors to refresh (browsers cache scripts). Add `?v=2` to the script URLs in `index.html` to force updates.

## Folder map

```
index.html            page shell: loads everything in order
css/style.css         all styling and scene animations
js/config.js          the only file a site owner normally edits (public, never put secrets here)
js/core.js            DOM helper + cleanup scopes (prevents leaks)
js/i18n.js            translation engine           js/locales/en.js, ms.js   all interface text
js/storage.js         local save + sanitising      js/audio.js     synthesised sounds (no files)
js/art.js             all original SVG artwork     js/ui.js        dialogs
js/validators.js      maths checking (pure)        js/adaptive.js  difficulty rules
js/packs.js           what can be sold             js/entitlements.js  "does the player own this pack?"
js/levels/*.js        the 12 free levels (36 puzzles)
packs/*.js            20 premium TEST packs = 200 levels (600 puzzles), loaded only when devUnlockPremium is true
tools/mk/             Python generator that writes most of packs/*.js (see docs/CONTENT-GUIDE.md)
js/puzzles.js         how each puzzle type looks/plays
js/app.js, main.js    screens, navigation, start-up
tests/                run-tests.js (node), e2e.py + e2e_more.py (browser)
docs/                 CONTENT-GUIDE, ARCHITECTURE, TEST-REPORT, TRANSLATION-REVIEW, ROADMAP
```

## Running the tests (optional, for developers)

```
node tests/run-tests.js                      # content, language, adaptive, save, no-secrets checks
python -m http.server 8123                   # in one terminal, inside this folder
pip install playwright && playwright install chromium
python tests/e2e.py http://localhost:8123/index.html
python tests/e2e_more.py http://localhost:8123/index.html
python tests/e2e_premium.py http://localhost:8123/index.html   # premium test packs, pets, dashboard
```

## Testing the premium packs

This build ships **thirty premium test packs, 300 levels in all** (levels 13 to 312) on 30 extra islands: Crystal Caves, Floating Gardens,
Mechanical Forest, Hidden City, Clock Harbour, Spice Market, Decimal Dunes, Frost Peaks, Coral Reef, Star Station, Ember Volcano, Pirate Cove,
Jungle Canopy, Candy Kingdom, Dino Valley, Robot Factory, Sports Arena, Castle Keep, Rainbow Bridge, Carnival Night, Kampung Village, Night Market, Kite Fields, Train Station, Bakery Bay, Deep Ocean, Zoo Park, Toy Workshop, Treehouse Town and Lantern Festival. They are switched on by
one line in `js/config.js`: `devUnlockPremium: true`. A yellow **TEST MODE** banner shows while it is on. **This is not a purchase and not secure.**
Before you publish the game publicly, set it to `false`: the premium islands then stay locked, the `packs/` files are
never requested, and you should not upload the `packs/` folder to the public site at all (see `docs/ARCHITECTURE.md`).

**Honest note on the 300 levels:** levels 13 to 24 were written by hand; levels 25 to 312 were produced with a generator
(`tools/mk`) from templates. Every answer is computed and every puzzle is proven solvable by the automated tests, but the wording is
repetitive in places and **both the English and the Bahasa Melayu need a teacher's review** before anyone pays for them.

## Players, pals and the map (new)

* **Players (profiles):** the chip at the top left of the menu opens *Players*. Up to 6 players, each with their own stars, coins, pals and
  settings. New players pick a name and a friendly avatar. *Save backup file* downloads a small `.json` file; *Load backup file* adds it as a
  new player (nobody is ever overwritten). Everything stays in this browser on this device: there are no accounts. If you clear the
  browser's site data, the saves go too, so keep a backup file.
  A save from the earlier version is moved into Player 1 automatically.
* **Pals are customisable:** in *Pals* open **Dress up** to give a nickname, change the colour (10 choices) and wear accessories you have **found** (14 of them).
  Accessories are found by finishing levels, never bought. Found items can be worn by any pal. Collection and the map show pals the way you dressed them.
* **Map order:** levels are numbered 1 to 312. On every island they read left to right in rows, and the rows go from the bottom of the island to
  the top; islands stack upwards.

* **Music:** a playful, original background tune is made with the browser's own sound engine (no audio files). It starts after the first tap
  (browsers do not allow sound before that). Turn it on or off with the note button on the menu or in **Settings → Music**, and scale it with the
  **Music volume** slider (0 to 100%). It is a little softer while a puzzle is open. **Sound** (tap and reward effects) is a separate switch.
* **Lively front page and map:** clouds drift across the sky, the Nimbo mascot flies and the islands bob gently. If a device has "reduce motion"
  turned on, this gentle sky and mascot motion still plays; choosing **Calmer** in Settings → Animations stops all of it.
* **Skills you have learned:** the Progress Dashboard lists every skill with levels finished, stars and a rank (Not yet, Started, Skilled, Master).

Also: oval **EN | BM** switch, **Pal Park** (pet, treat, play with, and take a pal along), and a **Progress Dashboard**
(stars, week chart, island progress, skill strength, recent adventures).

## What this build is and is not

* **Is:** a complete playable demo; local-only progress; no accounts, ads, trackers or network requests.
* **Is not:** a store. There is no payment code. Premium levels are not part of the free bundle; the test packs are for testing only. See `docs/ARCHITECTURE.md`.
* **Not offline-capable:** there is no service worker yet. It works from a downloaded copy, but a hosted version needs the network on first load.
* **Not verified:** physical phones/tablets, screen readers, real children, Malay wording by a native teacher, or alignment with the official KSSR syllabus. See `docs/TEST-REPORT.md`.

## What is new in version 0.5.0

* **Version and update info:** *Settings* ends with an *About and updates* card: the version number and a "What's new" list (English and Bahasa Melayu),
  with earlier updates folded away. A returning player also sees a small green "New in 0.5.0" note on the menu until they open Settings.
  When you ship an update, change `MP.config.version` in `js/config.js` and add an entry at the top of `js/changelog.js`.
  The game has no network code, so it cannot update itself: players get the new version when the files on your site are replaced and the page is reloaded.
* **Sound fix:** browsers put the sound engine to sleep (a phone call, the lock screen, switching apps, or no tap yet). The game now wakes it on
  any tap, key press or return to the page, handles the iPhone "interrupted" state, and restarts the music beat cleanly instead of replaying
  a burst of notes. Tested with a simulated sound engine and in a real browser.
* **Daily gift (login streak):** a button on the menu pulses when today's gift is ready. Gifts grow each day of a 7-day week:
  5, 10, 15, 20, 30, 40 and 50 coins, and day 7 adds a **100-coin Perfect Week bonus**. Missing a day starts again at day 1 (kindly, no punishment).
  After day 7 a new week begins. It uses the device's calendar day; moving the clock backwards never pays twice. Change the amounts in `js/streak.js`.
* **100 more levels:** 10 new islands (levels 213 to 312), 312 levels in all.
* **Hats and collection are found:** finishing levels now unlocks them (the *Finish N levels* label shows what is needed): Nimbo hats at 5, 15, 40 and 80
  finished levels, and the 14 pal accessories from 3 up to 150. A "New find!" note appears on the level-complete card. Items already bought in
  an older save stay owned, and saves that already passed a milestone receive the items when the game opens. Coins are now for treats only.
* **Map path:** a simple dashed trail with a gentle S-curve between levels, outlined in dark so it reads on every island. Finished steps are white;
  the next step is yellow and its dashes march gently (stopped by "Calmer").

## What is new in version 0.6.0

* **Online friends (optional, off by default).** *Menu > Friends*. A grown-up answers a small sum to switch it on. Each player gets a 6-character friend code;
  type a friend's code to send a request, they accept, and then you see each other's nickname, avatar, stars, levels and buddy pal. **Cheer!** (once a day
  per friend) gives your friend 2 coins when they next open Friends. There is **no chat, no email, no real names, no location**. Nothing is sent until the
  switch is on; "Turn off" forgets the online identity on this device; backup files never carry it.
* **How it works:** only `js/friends.js` talks to the network, through nine small functions in a private `mathipelago` schema of the Supabase project named in `js/config.js` (`friends`).
  Set `friends.url` to `''` to remove the feature. Setup SQL is in `docs/friends-setup.sql` (already applied to the Daymark project) and **`docs/friends-delete-functions.sql`
  must still be run once** in the Supabase SQL Editor: it adds *decline request*, *remove friend* and *delete my online data*.
  Until you run it the screen cannot decline or remove friends.
* **Motion:** springy presses, sheet-style pop-ups, screens that ease in and staggered menu/list entrances. "Calmer" in Settings and the device's reduce-motion setting stop it.
* **Privacy note for publishing:** with friends on, the game is no longer fully offline for that player. Update your privacy text, and check the rules for children's data in the countries you sell in (for Malaysia, PDPA) before launch.

## v0.7.0
- Friends race dashboard (lanes ranked by stars, track shows levels finished).
- Settings gear at top right of the menu (replaces the language pill; language is in Settings).
- "Your player" and "Add player" sections collapse.
- Map animations pause when off-screen: about 360 running animations down to about 25, 11 to 23 fps at 6x CPU slowdown.
