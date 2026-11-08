/*
 * Node unit tests (no browser needed):   node tests/run-tests.js
 * Checks content quality (every puzzle solvable, both languages complete, numbers agree between
 * languages), adaptive-difficulty rules, save-data sanitising and that no secrets ship in the bundle.
 */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..');

// minimal browser-like sandbox
const store = {};
const sandbox = {
  console, Math, JSON, Object, Array, Set, Number, String, Date, isFinite,
  document: { documentElement: { setAttribute() {} }, addEventListener() {}, createElement() { return {}; }, hidden: false },
  navigator: { language: 'en-US' },
  localStorage: { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); }, removeItem: k => { delete store[k]; } }
};
sandbox.window = sandbox; vm.createContext(sandbox);
function load(f) { vm.runInContext(fs.readFileSync(path.join(root, f), 'utf8'), sandbox, { filename: f }); }
['js/config.js', 'js/core.js', 'js/i18n.js', 'js/locales/en.js', 'js/locales/ms.js', 'js/storage.js', 'js/validators.js', 'js/adaptive.js', 'js/streak.js', 'js/packs.js',
 'js/entitlements.js', 'js/art.js', 'js/levels/registry.js', 'js/levels/meadow.js', 'js/levels/forest.js', 'js/levels/cove.js'].forEach(load);
const MP = sandbox.MP;

let pass = 0, fail = 0;
function t(name, cond, detail) { if (cond) { pass++; console.log('PASS ' + name); } else { fail++; console.log('FAIL ' + name + (detail !== undefined ? ' — ' + JSON.stringify(detail) : '')); } }

/* ---------- content ---------- */
const free = MP.levels.all();
{ const levels = free;
t('12 levels registered', levels.length === 12, levels.length);
t('3 islands with 4 levels each', MP.islands.length === 3 && MP.islands.every(i => MP.levels.byIsland(i.id).length === 4));
t('level ids unique and order is 1..12', new Set(levels.map(l => l.id)).size === 12 && levels.every((l, i) => l.order === i + 1));
t('every level is in the free pack', levels.every(l => l.pack === 'free-demo'));
t('premium packs ship no level data', MP.packs.premium().every(p => MP.levels.byPack(p.id).length === 0));
t('critter ids unique', new Set(levels.map(l => l.critter.id)).size === 12); }

// premium TEST packs live in /packs and are only loaded in test mode: load them here to validate them too
['crystal-caves','floating-gardens','mechanical-forest','hidden-city','clock-harbour','spice-market','decimal-dunes','frost-peaks','data-reef','star-station','ember-volcano','pirate-cove','jungle-canopy','candy-kingdom','dino-valley','robot-factory','sports-arena','castle-keep','rainbow-bridge','carnival-night','kampung-village','night-market','kite-fields','train-station','bakery-bay','deep-ocean','zoo-park','toy-workshop','treehouse-town','lantern-festival'].forEach(id => load('packs/' + id + '.js'));
const levels = MP.levels.all();
t('312 levels once all thirty test packs are loaded (12 free + 300 premium)', levels.length === 312, levels.length);
t('level ids unique and order is 1..312', new Set(levels.map(l => l.id)).size === 312 && levels.every((l, i) => l.order === i + 1));
t('critter ids unique across all levels', new Set(levels.map(l => l.critter.id)).size === 312);
t('33 islands: 4 free levels on each free island and 10 on each premium island', MP.packs.allIslands().length === 33 && MP.packs.allIslands().every(i => MP.levels.byIsland(i.id).length === (i.pack === 'free-demo' ? 4 : 10)));
t('each premium pack declares the right level count', MP.packs.premium().filter(p => p.testFile).every(p => MP.levels.all().filter(l => l.pack === p.id).length === p.levels));
t('premium levels belong to their pack island', levels.filter(l => l.pack !== 'free-demo').every(l => MP.packs.byId(l.pack).island.id === l.island));

function textObjects(o, out, p) {
  if (o && typeof o === 'object') {
    if (typeof o.en === 'string' || typeof o.ms === 'string') { out.push([p, o]); return out; }
    Object.keys(o).forEach(k => textObjects(o[k], out, p + '.' + k));
  }
  return out;
}
const texts = [];
levels.forEach(l => textObjects(l, texts, l.id));
MP.islands.forEach(i => textObjects(i, texts, i.id)); MP.packs.all().forEach(p => textObjects(p, texts, p.id));
t('every level/pack text has English and Bahasa Melayu', texts.every(([, o]) => o.en && o.en.trim() && o.ms && o.ms.trim()), texts.filter(([, o]) => !(o.en && o.ms)).map(x => x[0]));
t('found a reasonable amount of authored text', texts.length > 200, texts.length);

function nums(s) { return (s.match(/\d+(?:[.,]\d+)?/g) || []).map(x => x.replace(',', '.')).sort().join('|'); }
// Known, reviewed exception: Malay "keempat-empat" ("all four") is a word-form of the English digit "4".
const driftOk = ['m3-2.tiers.1.hint'];
const drift = texts.filter(([p, o]) => !driftOk.includes(p) && nums(o.en) !== nums(o.ms)).map(([p, o]) => p + ': ' + o.en + ' / ' + o.ms);
t('numbers inside each English/Malay pair agree (guards against translation drift)', drift.length === 0, drift.slice(0, 5));

levels.forEach(l => {
  t(l.id + ' has 3 authored tiers with ids a/b/c', l.tiers.length === 3 && l.tiers.every((p, i) => p.id === l.id + '-' + 'abc'[i]));
  l.tiers.forEach(p => {
    t(p.id + ' (' + p.type + ') is solvable and well-formed', MP.validators[p.type] && MP.solvers[p.type](p.spec).ok, MP.solvers[p.type] && MP.solvers[p.type](p.spec));
    t(p.id + ' has prompt, hint and explanation', !!(p.prompt && p.hint && p.explain));
  });
});

// the "steps" puzzles carry a calc string; prove each marked answer really equals the calculation
function calc(expr) {
  const e = expr.replace(/−/g, '-').replace(/×/g, '*').replace(/÷/g, '/');
  if (!/^[-+*/0-9. ()]+$/.test(e)) throw new Error('bad calc ' + expr);
  return Function('"use strict";return (' + e + ')')();
}
levels.filter(l => l.tiers[0].type === 'steps').forEach(l => l.tiers.forEach(p => p.spec.steps.forEach((st, i) => {
  const want = calc(st.calc), got = Number(String(st.choices[st.answer]).replace('−', '-').replace(/[^0-9.\-]/g, ''));
  t(p.id + ' step ' + (i + 1) + ' answer matches its calculation', Math.abs(want - got) < 1e-9, [st.calc, want, st.choices[st.answer]]);
  t(p.id + ' step ' + (i + 1) + ' wrong choices are all different from the answer', st.choices.filter((c, k) => k !== st.answer && String(c) === String(st.choices[st.answer])).length === 0);
})));

// validators reject wrong answers
const V = MP.validators;
t('numberline rejects wrong value', !V.numberline({ target: 7 }, 6) && V.numberline({ target: 7 }, 7));
t('balance rejects wrong sum, repeated tile and wrong count', !V.balance({ target: 10, tiles: [3, 7, 4] }, [0, 2]) && !V.balance({ target: 10, tiles: [5, 5] }, [0, 0]) && !V.balance({ target: 10, tiles: [3, 7, 5, 5], count: 3 }, [0, 1]));
t('share needs equal counts using every item', V.share({ items: 6, baskets: 2 }, [3, 3]) && !V.share({ items: 6, baskets: 2 }, [4, 2]) && !V.share({ items: 6, baskets: 2 }, [2, 2]));
t('tiles rejects the same tile twice', !V.tiles({ tiles: [6, 2], target: 36 }, [0, 0]) && V.tiles({ tiles: [6, 2], target: 12 }, [0, 1]));
t('digitArrange accepts only the true smallest (no leading zero)', V.digitArrange({ digits: [5, 0, 8, 3], goal: 'smallest', noLeadingZero: true }, [3, 0, 5, 8]) && !V.digitArrange({ digits: [5, 0, 8, 3], goal: 'smallest', noLeadingZero: true }, [0, 3, 5, 8]));
t('coins respects exact coin count', V.coins({ target: 245, coins: [5, 10, 20, 50, 100], exactCount: 5 }, [100, 100, 20, 20, 5]) && !V.coins({ target: 245, coins: [5, 10, 20, 50, 100], exactCount: 5 }, [100, 100, 10, 10, 10, 10, 5]));
t('tank checks equivalent fractions (3/4 = 6/8)', V.tank({ parts: 8, n: 3, d: 4 }, 6) && !V.tank({ parts: 8, n: 3, d: 4 }, 3));
t('chart computes mean correctly', MP.mathUtil.chartAnswer({ bars: [{ value: 24 }, { value: 18 }, { value: 36 }, { value: 26 }], ask: { op: 'mean' } }) === 26);

/* ---------- locales ---------- */
const en = vm.runInContext('MP.i18n.dict.en', sandbox), ms = vm.runInContext('MP.i18n.dict.ms', sandbox);
t('UI locale keys identical in English and Malay', Object.keys(en).every(k => k in ms) && Object.keys(ms).every(k => k in en), Object.keys(en).filter(k => !(k in ms)).concat(Object.keys(ms).filter(k => !(k in en))));
const used = new Set();
['js/app.js', 'js/puzzles.js', 'js/ui.js'].forEach(f => {
  const src = fs.readFileSync(path.join(root, f), 'utf8');
  (src.match(/\bt\('([a-zA-Z0-9_.]+)'/g) || []).forEach(m => used.add(m.slice(3, -1)));
  (src.match(/'((?:fb|puz|lvl|done|adapt|tut|map|nav|menu|intro|lang|set|reset|col|hat|par|premium|demo|err|app|place|pals|dash|test|prof|acc|streak|find|ver|fr|chest)\.[a-zA-Z0-9.]+)'/g) || []).forEach(m => used.add(m.slice(1, -1)));
});
const dynamic = ['pals.bond.0', 'pals.bond.1', 'pals.bond.2', 'pals.bond.3', 'pals.bond.4', 'pals.bond.5', 'pals.hello.0', 'pals.hello.1', 'pals.hello.2', 'pals.hello.3', 'pals.hello.4', 'pals.hello.5',
  'pals.pet.1', 'pals.pet.2', 'pals.pet.3', 'pals.feed.1', 'pals.feed.2', 'pals.play.1', 'pals.play.2', 'dash.rank.0', 'dash.rank.1', 'dash.rank.2', 'dash.rank.3', 'dash.skill.new', 'dash.skill.learning', 'dash.skill.growing', 'dash.skill.strong', 'band.explorer', 'band.adventurer', 'band.master', 'band.explorer.ages', 'band.adventurer.ages', 'band.master.ages', 'hat.sprout', 'hat.stargoggles', 'hat.captain', 'hat.rainbow', 'acc.party', 'acc.bow', 'acc.flower', 'acc.glasses', 'acc.bandana', 'acc.goggles', 'acc.hat', 'acc.scarf', 'acc.tophat', 'acc.headphones', 'acc.leafcrown', 'acc.halo', 'acc.wizard', 'acc.crown']
  .concat(levels.map(l => 'skill.' + l.skill), levels.map(l => 'topic.' + l.topic));
const missing = [...used, ...dynamic].filter(k => !k.endsWith('.') && !(k in en));  // keys ending in '.' are prefixes for the dynamic keys listed above
t('every key used by the code exists in the locale files', missing.length === 0, missing);
const unusedKeys = Object.keys(en).filter(k => !used.has(k) && !dynamic.includes(k));
t('no unused locale keys (keeps translation work small)', unusedKeys.length === 0, unusedKeys);
const placeholders = k => ((en[k] || '').match(/\{\w+\}/g) || []).sort().join();
t('placeholders ({n}, {name}…) match between English and Malay', Object.keys(en).every(k => placeholders(k) === ((ms[k] || '').match(/\{\w+\}/g) || []).sort().join()), Object.keys(en).filter(k => placeholders(k) !== ((ms[k] || '').match(/\{\w+\}/g) || []).sort().join()));

/* ---------- money formatting ---------- */
t('money formatting', MP.i18n.money(70) === '70 sen' && MP.i18n.money(135) === 'RM1.35' && MP.i18n.money(200) === 'RM2' && MP.i18n.money(105) === 'RM1.05');

/* ---------- adaptive ---------- */
const A = MP.adaptive, S = MP.store;
function freshSave(band) { const s = S.defaults(); s.band = band; return s; }
const lv = levels[0];
t('tier follows chosen band', [0, 1, 2].every(b => A.tierFor(freshSave(b), lv).tier === b));
{ const s = freshSave(1); A.record(s, lv, { wrong: 0, hints: 0, helped: false }); t('one clean solve does not change tier', A.tierFor(s, lv).tier === 1);
  A.record(s, lv, { wrong: 0, hints: 0, helped: false }); t('two clean solves raise tier by one', A.tierFor(s, lv).tier === 2);
  A.record(s, lv, { wrong: 0, hints: 0, helped: false }); A.record(s, lv, { wrong: 0, hints: 0, helped: false }); t('tier never exceeds the challenge puzzle', A.tierFor(s, lv).tier === 2); }
{ const s = freshSave(1); A.record(s, lv, { wrong: 1, hints: 1, helped: false }); A.record(s, lv, { wrong: 2, hints: 0, helped: false }); t('a few mistakes are normal and change nothing', A.tierFor(s, lv).tier === 1); }
{ const s = freshSave(1); A.record(s, lv, { wrong: 3, hints: 0, helped: false }); t('3+ mistakes lowers the topic one step and flags it for practice', A.tierFor(s, lv).tier === 0 && s.topics[lv.topic].review === true); }
{ const s = freshSave(0); A.record(s, lv, { wrong: 5, hints: 3, helped: true }); t('tier never goes below friendly', A.tierFor(s, lv).tier === 0); }
{ const s = freshSave(2); const l2 = levels[1], other = levels[11]; A.record(s, lv, { wrong: 4, hints: 0, helped: false }); A.record(s, l2, { wrong: 4, hints: 0, helped: false });
  t('confidence booster after two struggles in a row (level in an untouched topic starts one tier easier)', s.struggles === 2 && A.tierFor(s, other).reason === 'booster' && A.tierFor(s, other).tier === 1, A.tierFor(s, other)); }
{ const s = freshSave(1); s.levels[lv.id] = { lastPuzzle: lv.tiers[1].id, done: true, stars: 3, plays: 1, hints: 0, wrong: 0 };
  const pick = A.pickPuzzle(s, lv); t('replay avoids the identical puzzle', pick.puzzle.id !== lv.tiers[1].id); }
t('help is offered after 3 wrong at the friendliest tier and 5 elsewhere', A.offers(0, 3).help && !A.offers(1, 3).help && A.offers(1, 5).help && A.offers(1, 3).friendlier && !A.offers(0, 5).friendlier);
t('stars: clean 3, small slip 2, helped 1', A.stars({ wrong: 0, hints: 0 }) === 3 && A.stars({ wrong: 2, hints: 1 }) === 2 && A.stars({ wrong: 0, hints: 0, helped: true }) === 1 && A.stars({ wrong: 9, hints: 5 }) === 1);

/* ---------- storage ---------- */
t('sanitize(garbage) -> defaults', JSON.stringify(S.sanitize(null)) === JSON.stringify(S.defaults()) && JSON.stringify(S.sanitize('x')) === JSON.stringify(S.defaults()) && JSON.stringify(S.sanitize([1])) === JSON.stringify(S.defaults()));
{ const s = S.sanitize({ coins: 'abc', band: 99, lang: 'fr', textScale: 5, levels: { 'bad id!': {}, ok1: { done: 'yes', stars: 99, plays: -4 }, ok2: { done: true, stars: 7 } }, collection: ['a', 'a', '<script>', 5], wardrobe: { owned: ['sprout'], equipped: 'captain' } });
  t('sanitize clamps numbers, drops bad ids and unknown values', s.coins === 0 && s.band === 2 && s.lang === null && s.textScale === 1 && !s.levels['bad id!'] && s.levels.ok1.done === false && s.levels.ok1.stars === 0 && s.levels.ok1.plays === 0 && s.levels.ok2.stars === 3 && s.collection.length === 1 && s.wardrobe.equipped === null, s); }
{ S.load(); store['mathipelago.save.p.' + S.profiles.activeId()] = '{not json'; const s = S.load(); t('corrupt JSON loads as defaults and keeps a copy for support', s.coins === 0 && store['mathipelago.save.p.p1.corrupt'] === '{not json'); }
{ store['mathipelago.save.p.' + S.profiles.activeId()] = JSON.stringify({ v: 99, coins: 5, extra: { evil: true } }); const s = S.load(); t('newer/unknown save fields are ignored safely', s.coins === 5 && !('extra' in s)); }
{ S.update(s => { s.coins = 42; s.lang = 'ms'; s.levels.x = { done: true, stars: 2, plays: 1, lastPuzzle: null, hints: 0, wrong: 0 }; }); S.resetProgress(); const s = S.get();
  t('resetProgress wipes progress but keeps language', s.coins === 0 && Object.keys(s.levels).length === 0 && s.lang === 'ms'); }

{ const s = S.sanitize({ collection: ['gemmy'], buddy: 'gemmy', pals: { gemmy: { bond: 99, fed: -3, played: 'x' }, 'bad id!': { bond: 1 } }, history: [{ id: 'm1-1', stars: 9, wrong: 2, hints: 0, day: 20261019 }, { id: 'bad id', stars: 1 }, 5] });
  t('sanitize keeps pals, buddy and history within limits', s.buddy === 'gemmy' && s.pals.gemmy.bond === 5 && s.pals.gemmy.fed === 0 && s.pals.gemmy.played === 0 && !s.pals['bad id!'] && s.history.length === 1 && s.history[0].stars === 3 && s.history[0].day === 20261019, s); }
t('buddy must be a collected pal', S.sanitize({ buddy: 'ghost', collection: [] }).buddy === null);
t('history keeps only the last 40 runs', S.sanitize({ history: Array.from({ length: 60 }, (_, i) => ({ id: 'm1-1', stars: 1, wrong: 0, hints: 0, day: 20261019 + i })) }).history.length === 40);

t('music settings are sanitised (on by default, volume 0..100)', S.defaults().music === true && S.defaults().musicVol === 60 && S.sanitize({ musicVol: 999, music: 'x' }).musicVol === 100 && S.sanitize({ musicVol: -5 }).musicVol === 0 && S.sanitize({ music: false }).music === false && S.sanitize({ music: 'no' }).music === true && S.sanitize({ musicVol: 'abc' }).musicVol === 60);
/* ---------- profiles + pal customisation ---------- */
{ for (const k of Object.keys(store)) delete store[k];
  store['mathipelago.save'] = JSON.stringify({ coins: 77, lang: 'ms', levels: { 'm1-1': { done: true, stars: 3 } } });   // a save from before profiles existed
  const s = S.load();
  t('old single save is migrated into player 1 with progress intact', s.coins === 77 && s.levels['m1-1'].stars === 3 && S.profiles.count() === 1 && S.profiles.activeId() === 'p1'); }
{ const id = S.profiles.create('  <b>Aina</b>  ', 'berri');
  t('a new player starts clean, keeps the device language, name is cleaned', id === 'p2' && S.get().coins === 0 && S.get().lang === 'ms' && S.get().avatar === 'berri' && !/[<>]/.test(S.get().name) && S.get().name.indexOf('Aina') !== -1 && S.profiles.count() === 2); }
{ S.update(s => { s.coins = 5; }); S.profiles.switchTo('p1'); const a = S.get().coins; S.profiles.switchTo('p2'); const b = S.get().coins;
  t('players keep separate progress when switching', a === 77 && b === 5); }
{ const l = S.profiles.list(); t('profile list summarises each player', l.length === 2 && l[0].levels === 1 && l[0].stars === 3 && l[1].active === true); }
{ let n = 2; while (S.profiles.canAdd()) { S.profiles.create('x' + n, 'nimbo'); n++; } t('at most 6 players; creating a 7th is refused', S.profiles.count() === 6 && S.profiles.create('no', 'nimbo') === null); }
{ const txt = S.profiles.exportActive(); t('backup is JSON with the save inside', JSON.parse(txt).mathipelago === 1 && JSON.parse(txt).save.name === S.get().name);
  t('importing into a full list is refused and changes nothing', S.profiles.importText(txt) === 'full' && S.profiles.count() === 6);
  t('garbage or foreign backup files are rejected', S.profiles.importText('nope') === 'bad' && S.profiles.importText('{"a":1}') === 'bad' && S.profiles.importText('[]') === 'bad'); }
{ const before = S.profiles.count(); const act = S.profiles.activeId(); S.profiles.remove(act);
  t('deleting a player removes them and picks another', S.profiles.count() === before - 1 && S.profiles.activeId() !== act && ('mathipelago.save.p.' + act) !== null && !(('mathipelago.save.p.' + act) in store)); }
{ while (S.profiles.count() > 1) S.profiles.remove(S.profiles.activeId() === S.profiles.list()[0].id ? S.profiles.list()[1].id : S.profiles.list()[0].id);
  t('the last player cannot be deleted', S.profiles.remove(S.profiles.activeId()) === false && S.profiles.count() === 1); }
{ const id = S.profiles.importText(JSON.stringify({ mathipelago: 1, name: 'Backup', avatar: 'tock', save: { coins: 12, collection: ['gemmy'] } }));
  t('a backup restores as a new player', id !== 'bad' && id !== 'full' && S.get().coins === 12 && S.get().name === 'Backup' && S.get().avatar === 'tock' && S.profiles.count() === 2); }
{ const s = S.sanitize({ collection: ['gemmy'], closet: ['crown', 'crown', 'bad id!'], pals: { gemmy: { acc: 'crown', tint: 99, nick: '<i>Gem</i> the great and mighty' }, other: { acc: 'halo', tint: 'x' } } });
  t('pal customisation is sanitised: owned hats only, tint clamped, nickname cleaned and capped', s.closet.length === 1 && s.pals.gemmy.acc === 'crown' && s.pals.gemmy.tint === 11 && s.pals.gemmy.nick.length <= 12 && !/[<>]/.test(s.pals.gemmy.nick) && s.pals.other.acc === null && s.pals.other.tint === 0); }
t('pal accessories and colours are drawn', ['party', 'bow', 'flower', 'glasses', 'bandana', 'goggles', 'hat', 'scarf', 'tophat', 'headphones', 'leafcrown', 'halo', 'wizard', 'crown'].every(id => MP.art.creature({ body: 'blob' }, { acc: id }).length > MP.art.creature({ body: 'blob' }, { acc: 'none' }).length) && MP.art.TINTS.length === 10 && MP.art.PAL_ACCS.length === 14);

/* ---------- entitlements ---------- */
t('free pack always owned, premium never (prototype provider)', MP.entitlements.hasPack('free-demo') && !MP.entitlements.hasPack('crystal-caves') && MP.entitlements.providerId() === 'free-only');
MP.entitlements.startCheckout('crystal-caves').then(r => {
  t('checkout reports unavailable when no URL is configured', r.ok === false);
  MP.entitlements.useDevUnlock();
  return MP.entitlements.refresh();
}).then(() => {
  t('test-mode provider owns all thirty premium packs', MP.entitlements.isTestMode() && MP.entitlements.hasPack('crystal-caves') && MP.entitlements.hasPack('floating-gardens') && MP.packs.premium().every(p => MP.entitlements.hasPack(p.id)));
  t('dev unlock is on in config for this test build (turn off before publishing)', MP.config.devUnlockPremium === true);
  audioDone.then(finish);
});



/* ---------- daily login streak ---------- */
{
  const S = MP.streak, d = n => '2026-03-' + String(n).padStart(2, '0');
  t('streak: coins rise every day of the week and day 7 is the biggest', S.REWARDS.length === 7 && S.REWARDS.every((v, i) => i === 0 || v > S.REWARDS[i - 1]));
  let st = S.blank();
  t('streak: first ever login is day 1', S.status(st, d(1)).day === 1 && S.status(st, d(1)).reward === S.REWARDS[0]);
  let r = S.claim(st, d(1)); t('streak: claiming pays the day-1 reward', r && r.coins === S.REWARDS[0] && r.st.day === 1 && r.st.last === d(1));
  t('streak: claiming twice the same day is refused', S.claim(r.st, d(1)) === null && S.status(r.st, d(1)).state === 'claimed');
  st = r.st; const paid = [r.coins];
  for (let i = 2; i <= 7; i++) { r = S.claim(st, d(i)); st = r.st; paid.push(r.coins); }
  t('streak: seven days in a row pays 5,10,15,20,30,40 then 50 + perfect-week bonus', JSON.stringify(paid) === JSON.stringify(S.REWARDS.slice(0, 6).concat([S.REWARDS[6] + S.PERFECT_BONUS])), paid);
  t('streak: day 7 is flagged perfect and counts a perfect week', r.perfect === true && r.bonus === S.PERFECT_BONUS && st.weeks === 1 && st.best === 7);
  r = S.claim(st, d(8)); t('streak: the day after a full week starts a new week at day 1 (no bonus)', r.day === 1 && r.bonus === 0 && r.st.weeks === 1);
  r = S.claim(S.claim(S.claim(S.blank(), d(1)).st, d(2)).st, d(5));
  t('streak: missing a day starts again at day 1', r.day === 1 && r.restarted === true && r.coins === S.REWARDS[0]);
  t('streak: best streak is remembered after a reset', r.st.best === 2, r.st);
  const back = S.status({ day: 3, last: d(10), best: 3, weeks: 0, total: 3 }, d(9));
  t('streak: a clock set backwards never pays or resets', back.state === 'claimed');
  t('streak: month and year boundaries count as consecutive days', S.status({ day: 2, last: '2026-02-28', best: 2, weeks: 0, total: 2 }, '2026-03-01').day === 3 && S.status({ day: 4, last: '2025-12-31', best: 4, weeks: 0, total: 4 }, '2026-01-01').day === 5);
  t('streak: garbage dates fall back to a fresh start', S.status({ day: 5, last: 'nope', best: 5, weeks: 0, total: 5 }, d(3)).day === 1);
  const sv = MP.store.sanitize({ streak: { day: 99, last: 'x', best: -4, weeks: 'a', total: 3 }, seenVersion: '<b>' });
  t('streak: saved streak is sanitised', sv.streak.day === 0 && sv.streak.last === null && sv.streak.best === 0 && sv.seenVersion === '');
  const sv2 = MP.store.sanitize({ streak: { day: 4, last: '2026-03-04', best: 5, weeks: 2, total: 20 }, seenVersion: '0.5.0' });
  t('streak: a valid streak and seen version survive', sv2.streak.day === 4 && sv2.streak.weeks === 2 && sv2.seenVersion === '0.5.0');
}

/* ---------- audio resilience (fake Web Audio, no speakers needed) ---------- */
let audioResolve; const audioDone = new Promise(r => { audioResolve = r; });
{
  const listeners = {}; let ctxs = [];
  class FakeCtx {
    constructor() { this.state = 'suspended'; this.currentTime = 0; this.sampleRate = 8000; this.destination = {}; this.resumes = 0; ctxs.push(this); }
    resume() { this.resumes++; const self = this; return Promise.resolve().then(() => { self.state = 'running'; if (self.onstatechange) self.onstatechange(); }); }
    suspend() { this.state = 'suspended'; return Promise.resolve(); }
    createGain() { return { gain: { value: 0, setValueAtTime() {}, exponentialRampToValueAtTime() {}, setTargetAtTime() {} }, connect() {} }; }
    createOscillator() { return { frequency: { setValueAtTime() {}, exponentialRampToValueAtTime() {} }, connect() {}, start() {}, stop() {} }; }
    createBuffer(n, l) { return { getChannelData: () => new Float32Array(l) }; }
    createBufferSource() { return { connect() {}, start() {}, stop() {} }; }
    createBiquadFilter() { return { frequency: {}, connect() {} }; }
  }
  const sb = { console, Math, JSON, Object, Array, Number, isFinite, setTimeout, clearTimeout, setInterval, clearInterval,
    document: { hidden: false, addEventListener(e, f) { (listeners[e] = listeners[e] || []).push(f); } },
    AudioContext: FakeCtx, addEventListener(e, f) { (listeners['w' + e] = listeners['w' + e] || []).push(f); } };
  sb.window = sb; vm.createContext(sb);
  vm.runInContext(fs.readFileSync(path.join(root, 'js/audio.js'), 'utf8'), sb, { filename: 'js/audio.js' });
  const A = sb.MP.audio;
  t('audio: nothing is created before the first gesture', ctxs.length === 0);
  (listeners.pointerdown || []).forEach(f => f({}));
  t('audio: first tap anywhere creates and wakes the engine', ctxs.length === 1 && ctxs[0].resumes >= 1);
  t('audio: a tap listener is registered for pointer, touch, key and click', ['pointerdown', 'touchend', 'keydown', 'click'].every(e => (listeners[e] || []).length === 1));
  setTimeout(() => {
    t('audio: engine reaches running', ctxs[0].state === 'running', ctxs[0].state);
    ctxs[0].state = 'interrupted'; const before = ctxs[0].resumes;
    (listeners.click || []).forEach(f => f({}));
    t('audio: an iOS-style "interrupted" engine is resumed on the next tap', ctxs[0].resumes > before);
    setTimeout(() => {
      t('audio: it runs again afterwards', ctxs[0].state === 'running');
      A.setMusic(true, 70); A.unlock();
      t('audio: music starts and reports playing', A.musicState().playing === true);
      A.setMusic(false, 70);
      t('audio: music can be switched off', A.musicState().playing === false);
      t('audio: play() never throws while suspended', (() => { ctxs[0].state = 'suspended'; try { A.play('ok'); A.play('win'); return true; } catch (e) { return false; } })());
      audioResolve();
    }, 30);
  }, 30);
}

/* ---------- no secrets in the bundle ---------- */
function walk(d) { return fs.readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]); }
const shipped = walk(path.join(root, 'js')).concat([path.join(root, 'index.html'), path.join(root, 'css/style.css')]);
const bad = [];
shipped.forEach(f => { const src = fs.readFileSync(f, 'utf8'); [/sk_live|sk_test|pk_live|pk_test/, /api[_-]?key\s*[:=]/i, /secret\s*[:=]/i, /password\s*[:=]/i, /BEGIN (RSA )?PRIVATE KEY/, /fetch\(|XMLHttpRequest|sendBeacon|WebSocket/, /google-analytics|gtag|fbq\(|facebook\.net|doubleclick/].forEach(re => { if (path.basename(f) === 'friends.js' && /fetch|api|secret/.test(re.source)) return; if (re.test(src)) bad.push(path.relative(root, f) + ' ~ ' + re); }); });
// friends.js is the one allowed network file (optional online friends). It may use fetch and the server's p_secret parameter name; nothing else in it is exempt.
t('friends.js is the only shipped file that calls fetch', shipped.filter(f => /fetch\(/.test(fs.readFileSync(f, 'utf8'))).map(f => path.basename(f)).join() === 'friends.js');
t('friends.js sends nothing until the grown-up switch is on', /function me\(\)[^\n]*online\.on/.test(fs.readFileSync(path.join(root, 'js/friends.js'), 'utf8')));
t('no secrets, network calls or trackers in shipped code', bad.length === 0, bad);
const ext = shipped.filter(f => /\.(html|js|css)$/.test(f)).filter(f => /(https?:)?\/\/(?!www\.w3\.org)[a-z0-9.-]+\.[a-z]{2,}/i.test(fs.readFileSync(f, 'utf8').replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g, '').replace(/xmlns="[^"]*"/g, '')));
t('no external URLs are loaded (fonts, scripts, images)', ext.length === 0, ext.map(f => path.relative(root, f)));

let finished = false;
function finish() {
  if (finished) return; finished = true;
  console.log('\n' + pass + ' passed, ' + fail + ' failed');
  process.exit(fail ? 1 : 0);
}
