# Architecture and decisions

## Technology decision

| Question | Answer |
|---|---|
| Engine | Plain HTML + CSS + JavaScript, with SVG artwork drawn in code. No framework, no build step. |
| Why | Puzzles here are tap/slide interfaces, not physics or sprite action. DOM + SVG gives accessible real buttons, crisp art at any size, tiny download (about 240 KB uncompressed, no images/fonts/audio files) and nothing to install or compile. |
| Phaser 3 | Strong for real-time sprite games, but adds about 1 MB, a canvas that must be made accessible by hand, and a build workflow. It would only pay off if you later add arcade-style mini-games. |
| Mobile performance | Few DOM nodes, CSS transforms only, no render loop (nothing runs when nothing moves), animations paused or disabled with reduced motion. Not yet measured on low-end phones. |
| Deployment | Any static host (see README). |
| Trade-offs | Hand-written vanilla JS needs discipline (done with small modules and tests). If the team grows, migrating screens to a framework is possible because content, validators and rules are separate from rendering. |

## What needs a backend (and what does not)

| Feature | Backend needed? |
|---|---|
| Free demo, language, adaptive difficulty, local progress | No |
| Selling premium packs | **Yes.** A browser can never be trusted to say "I paid". |
| Cross-device progress / accounts | Yes (optional, later) |
| Parent progress reports by email | Yes (optional, later) |

Why not just use a local flag: anyone can edit localStorage or read page files. So this build contains **no premium
data and no "owned" flag**. `js/entitlements.js` is the single door; its only provider (`free-only`) says "no" to every paid pack.

## Recommended production design for paid access (least expensive sensible)

1. **Checkout on your website, not in the game.** Use a hosted checkout from a payment provider that supports Malaysian ringgit and local methods
   (for example Stripe Checkout, or a Malaysian gateway such as Billplz/Toyyibpay). The game only links to that page. Card details never touch the game.
2. **Tiny backend**: one serverless function platform (Cloudflare Workers + D1/KV, or Netlify/Vercel functions + a small database). Roughly:
   * `POST /webhook`: the payment provider calls this after a *successful* payment; verify its signature with the secret key (kept only in server settings), then record `(customer, pack)` as owned.
   * `POST /login-link`: customer enters the purchase email, receives a one-time sign-in link (no passwords, no child data).
   * `GET /entitlements`: returns pack ids owned by the signed-in customer (session cookie `HttpOnly; Secure`).
   * `GET /packs/<id>.js`: returns the premium level file **only** if entitled. Store premium files outside the public folder.
3. **Game change**: add `ServerProvider` implementing `fetchOwned()` / `startCheckout()` (same interface as `FreeOnlyProvider`), call `MP.entitlements.setProvider(...)`, and load pack files after the check. The engine and puzzles do not change.
4. Cost: free tiers of these platforms cover early sales. The main running costs are payment fees and your domain.
5. Alternative with even less to maintain: sell a **downloadable/access code** through a store platform and verify codes with one serverless function. Still server-side, still no secrets in the browser.

Not done and not claimed: payment integration, accounts, webhooks, entitlement server. Nothing of this has been built or tested.

## Privacy and legal (needs a lawyer, not a claim of compliance)

* The prototype collects no personal data, has no accounts/ads/trackers/third-party requests, and keeps progress on the device. Tests check there are no network calls or external URLs.
* When you add purchases or accounts you will process at least an email and payment records. In Malaysia the **Personal Data Protection Act 2010** (as amended in 2024) likely applies to a commercial operator; children's data is treated with extra care in practice, and there are consent and notice duties, data-user obligations and cross-border transfer rules. Confirm with a Malaysian lawyer which duties apply to your setup, including whether you must register or appoint a data-protection officer, and what consent is needed from parents.
* Publish a plain-language privacy notice and terms before launch. The in-game "For grown-ups" text is a summary, **not** a legal notice.
* Check consumer rules for digital goods (refund policy, price display in RM, tax/SST position) and if you target other countries their child-privacy laws (for example COPPA in the US, GDPR-K in the EU/UK).
* Educational claims: this game has **not** been verified against the official KSSR/DSKP learning standards. Do not advertise curriculum compliance or score improvements until reviewed by a qualified teacher and, ideally, tested with children.

## Launch roadmap (practical order)

1. Playtest with 5 to 10 children aged 7 to 12 on real phones; watch where they hesitate. Fix.
2. Native-speaker teacher reviews every Malay text (`docs/TRANSLATION-REVIEW.md`) and the maths against KSSR.
3. Trademark search for "Mathipelago" (Malaysia MyIPO, plus target markets) and domain; pick the final name.
4. Test on real devices: low-end Android, iPhone Safari, tablet; screen reader pass; add a service worker for offline once content is stable.
5. Draft privacy notice + terms with a lawyer; decide payment provider.
6. Build the small backend above, then the first paid pack (Fractions & the Crystal Caves reuses the `tank` mechanic plus new ones).
7. Launch free demo first, collect feedback, then open sales.

## Test unlock (what changed in this build)

`MP.config.devUnlockPremium = true` makes the app use `DevUnlockProvider` (js/entitlements.js). It reports every premium pack that has a
`testFile` as owned, then `loadOwnedPacks()` injects `<script src="packs/<id>.js">`. Everything still goes through `MP.entitlements.hasPack()`,
and `isUnlocked()` in `js/app.js` checks it before a premium level can open. A hand-edited save cannot unlock premium (covered by a test).

For production replace `DevUnlockProvider` with a `ServerProvider`: `fetchOwned()` asks your backend, and the backend serves `packs/<id>.js`
only to paying customers. Delete the `packs/` folder from the public site and set `devUnlockPremium: false`.

## Pals and dashboard data

Saved fields: `pals` (per pal `bond` 0..5, `fed`, `played`), `buddy` (a collected pal id) and `history` (last 40 finished runs: level id, stars,
mistakes, hints, day as YYYYMMDD). All are sanitised on load. Bond = floor((treats + plays) / 2), capped at 5. A treat costs 3 coins; petting and
playing are free and never give coins, so there is nothing to farm. The dashboard is computed from the save only; nothing leaves the device.

## Players (profiles) and pal customisation

Storage keys in the browser (`MP.config.storageKey` is the prefix, default `mathipelago.save`):
* `<prefix>.profiles` the list of players `{active, list:[{id,name,avatar}]}` (max 6)
* `<prefix>.p.<id>` one full save per player (same sanitised format as before plus `name`, `avatar`, `closet`)
* `<prefix>` the pre-profile save: read once and copied into player `p1`, then left alone as a harmless old copy.

Switching players saves the current one, then loads the other; there is no shared state besides the index. Backups are the player's save as JSON
(`{mathipelago:1, name, avatar, save}`); importing always creates a **new** player and runs the same `sanitize()`, so a hand-edited or foreign file
cannot crash the game or overwrite anyone. Names are stripped of `< > & "` and control characters and capped at 14 characters.
Pal customisation per pal: `acc` (`null` natural, `'none'`, or a bought accessory id), `tint` (0..11 or `null`), `nick` (max 12). `closet` lists bought
accessories (shared by all pals). `sanitize()` only keeps an `acc` that is in `closet`. None of this is a security boundary: it costs in-game coins only.
Players are separate **on one device and browser**; they are not accounts and do not sync. Deleting site data deletes the saves (hence the backup file).

## Background music

`js/audio.js` generates a looping tune (I - vi - IV - V in C major, 112 bpm: melody, bouncy bass, chord stabs, soft kick and hats) with Web Audio
oscillators scheduled about 0.35 s ahead by a timer. There are no audio files, so nothing is downloaded and nothing can be copied or licensed
from elsewhere. `MP.audio.setMusic(on, volume)`, `setDuck(true)` (softer on the puzzle screen) and `musicState()` are the whole API. The save holds
`music` (true/false) and `musicVol` (0..100). It is paused when the tab is hidden and starts only after the first tap (autoplay rules).

## Round 5 additions (v0.5.0)

* **Sound robustness (`js/audio.js`).** One capture-phase listener (pointer, touch, key, click) calls `wake()`: it creates the engine on the first tap, resumes it
  when it is `suspended` or iOS `interrupted`, plays a one-sample silent buffer (iOS only opens output after a real playback inside a gesture) and restarts the
  music timer. `onstatechange`, `visibilitychange`, `pageshow` and `focus` also resume it, but never while the page is hidden. When the engine comes back,
  the music clock restarts (`nextT`) so no backlog of notes plays at once. Sound effects try once more 120 ms later if the engine was still waking, then give up
  silently so nothing piles up. `MP.audio.state()` reports the engine state for tests.
* **Streak (`js/streak.js`).** Pure functions `status(st, today)` and `claim(st, today)` over `{day, last, best, weeks, total}` with local `YYYY-MM-DD` dates.
  `app.js` only wires them to the save (`streak`, sanitised in `storage.js`) and the screens (`SCREENS.streak`, the menu button).
* **Finds.** `HATS[].at` and `PAL_AT` in `app.js` are the finished-level thresholds; `awardFinds()` runs after every level completes and when the menu opens (this also migrates old saves).
* **Version info.** `MP.config.version` and `MP.changelog` (`js/changelog.js`); `seenVersion` in the save drives the small "new" note on the menu.
* **Map path.** Each step is a cubic S-curve built in `SCREENS.map` from two SVG paths (`.seg.under` outline, `.seg.top` dashes); styles in `css/style.css` (`.mappath`).
* **Content.** `tools/mk/p21.py` to `p30.py`, ten new islands wired in `js/packs.js`, `js/art.js` (backgrounds, island decorations, pal characters) and `tools/mk/build.py`.
