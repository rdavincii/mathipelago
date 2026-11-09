/*
 * app.js — screens and navigation. Each screen is a function (params, scope) -> Node.
 * `scope` collects listeners/timers; it is disposed whenever the player leaves the screen,
 * so repeated navigation does not leak anything.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  var el = MP.util.el, t = MP.t, tx = MP.tx, A = MP.art, S = MP.store, AD = MP.adaptive;

  var rootEl, current = { name: null, params: null, scope: null };
  var SCREENS = {};
  // Hats and pal accessories are FOUND: each unlocks when the player has finished this many levels.
  var HATS = [
    { id: 'sprout', at: 5 }, { id: 'stargoggles', at: 15 }, { id: 'captain', at: 40 }, { id: 'rainbow', at: 80 }
  ];
  var BAND_KEYS = ['explorer', 'adventurer', 'master'];
  var PAL_AT = { party: 3, bow: 6, flower: 9, glasses: 12, bandana: 18, goggles: 25, hat: 32, scarf: 40, tophat: 50, headphones: 62, leafcrown: 75, halo: 90, wizard: 110, crown: 150 };
  /** Gives the player every hat / accessory their finished-level count has reached. Returns what is new. */
  function awardFinds() {
    var n = doneCount(), found = [];
    S.update(function (sv) {
      HATS.forEach(function (h) { if (n >= h.at && sv.wardrobe.owned.indexOf(h.id) === -1) { sv.wardrobe.owned.push(h.id); found.push({ kind: 'hat', id: h.id }); } });
      Object.keys(PAL_AT).forEach(function (id) { if (n >= PAL_AT[id] && sv.closet.indexOf(id) === -1) { sv.closet.push(id); found.push({ kind: 'acc', id: id }); } });
    });
    return found;
  }
  function lockedFind(left) { MP.audio.play('nope'); MP.ui.dialog({ title: t('find.lockedTitle'), body: t('find.lockedBody', { n: left }), buttons: [{ label: t('ok'), cls: 'primary' }] }); }

  /* ---------------- helpers ---------------- */
  function btn(cls, label, onClick, attrs) {
    var b = el('button', { class: 'btn ' + cls, attrs: Object.assign({ type: 'button' }, attrs || {}) });
    if (typeof label === 'string') b.textContent = label; else if (label) b.appendChild(label);
    b.addEventListener('click', function (e) { MP.audio.unlock(); onClick(e, b); });
    return b;
  }
  function icon(svg, cls) { return el('span', { class: 'ico ' + (cls || ''), svg: svg }); }
  function levelRec(id) { return S.get().levels[id] || null; }
  function isDone(id) { var r = levelRec(id); return !!(r && r.done); }
  function isUnlocked(lv) {
    if (!MP.entitlements.hasPack(lv.pack)) return false;   // premium levels need the pack (never a save flag)
    var all = MP.levels.all(), i = all.indexOf(lv);
    if (i <= 0) return true;
    return isDone(all[i - 1].id);
  }
  function freeLevels() { return MP.levels.all().filter(function (l) { return l.pack === 'free-demo'; }); }
  function starsOf(list) { var n = 0; list.forEach(function (l) { var r = levelRec(l.id); if (r) n += r.stars; }); return n; }
  function ownedPals() {
    var sv = S.get(), seen = {}, out = [];
    MP.levels.all().forEach(function (l) { var c = l.critter; if (!seen[c.id] && sv.collection.indexOf(c.id) !== -1) { seen[c.id] = 1; out.push(c); } });
    return out;
  }
  function palRec(id) { return S.get().pals[id] || { bond: 0, fed: 0, played: 0, acc: null, tint: null, nick: '' }; }
  function ensurePal(v, id) { return v.pals[id] || (v.pals[id] = { bond: 0, fed: 0, played: 0, acc: null, tint: null, nick: '' }); }
  /** A pal drawn the way this player dressed it (hat/accessory, colour). */
  function palSvg(c, o) { var r = palRec(c.id); o = o || {}; o.acc = (r.acc === undefined || r.acc === null) ? undefined : r.acc; o.tint = r.tint; return A.creature(c.look, o); }
  function palName(c) { return palRec(c.id).nick || tx(c.name); }
  function avatarIcon(id, cls) { return icon(A.avatar(id, cls), 'avatar'); }
  function nameInput(value, ph, label) {
    var i = document.createElement('input');
    i.type = 'text'; i.className = 'nameinput'; i.maxLength = 14; i.value = value || ''; i.placeholder = ph || '';
    i.setAttribute('autocomplete', 'off'); i.setAttribute('autocapitalize', 'words'); i.setAttribute('aria-label', label || ph || ''); i.setAttribute('enterkeyhint', 'done');
    return i;
  }
  /** Row of avatar buttons. Updates in place (so a typed name is not lost). Returns {node, get}. */
  function avatarPicker(current, onPick) {
    var cur = current || 'nimbo', node = el('div', { class: 'avatars', attrs: { role: 'group', 'aria-label': t('prof.avatar') } }), bs = {};
    A.avatarIds().forEach(function (id) {
      bs[id] = btn('avbtn' + (id === cur ? ' on' : ''), avatarIcon(id), function () {
        cur = id; Object.keys(bs).forEach(function (k) { bs[k].classList.toggle('on', k === id); bs[k].setAttribute('aria-pressed', k === id ? 'true' : 'false'); });
        if (onPick) onPick(id);
      }, { 'aria-pressed': id === cur ? 'true' : 'false', 'aria-label': id === 'nimbo' ? 'Nimbo' : id });
      node.appendChild(bs[id]);
    });
    return { node: node, get: function () { return cur; } };
  }
  function critterById(id) { var a = MP.levels.all(); for (var i = 0; i < a.length; i++) if (a[i].critter.id === id) return a[i].critter; return null; }
  function dayNum(d) { d = d || new Date(); return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate(); }
  function bondOf(rec) { return Math.min(5, Math.floor((rec.fed + rec.played) / 2)); }
  function testBanner() { return MP.entitlements.isTestMode() ? el('div', { class: 'testbanner', text: t('test.banner'), attrs: { role: 'note' } }) : null; }
  function currentLevel() {
    var all = MP.levels.all();
    for (var i = 0; i < all.length; i++) if (!isDone(all[i].id)) return all[i];
    return null;
  }
  function totalStars() {
    var n = 0, lv = S.get().levels; Object.keys(lv).forEach(function (k) { n += lv[k].stars; }); return n;
  }
  function doneCount() { return MP.levels.all().filter(function (l) { return isDone(l.id); }).length; }
  function equippedHat() { var w = S.get().wardrobe; return w.equipped || null; }

  var themeWatch = null;
  function applySettings() {
    var sv = S.get();
    MP.i18n.setLang(sv.lang || MP.i18n.detect());
    MP.audio.setEnabled(sv.sound);
    MP.audio.setMusic(sv.music, sv.musicVol);
    var d = document.documentElement;
    MP.audio.setHaptics(sv.haptics !== false);
    var dark = sv.theme === 'dark' || (sv.theme !== 'light' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches);
    d.setAttribute('data-theme', dark ? 'dark' : 'light');
    if (!themeWatch && window.matchMedia) { themeWatch = window.matchMedia('(prefers-color-scheme: dark)'); if (themeWatch.addEventListener) themeWatch.addEventListener('change', function () { if (!S.get().theme) applySettings(); }); }
    d.setAttribute('data-motion', sv.motion || 'auto');
    d.style.setProperty('--ts', String(sv.textScale));
    document.title = MP.config.gameName + ' — ' + t('app.tagline');
  }

  function go(name, params) {
    if (current.scope) current.scope.dispose();
    MP.ui.closeDialog();
    var scope = new MP.util.Scope();
    current = { name: name, params: params || {}, scope: scope };
    MP.audio.setDuck(name === 'level');
    rootEl.textContent = '';
    var node;
    try { node = SCREENS[name](current.params, scope); }
    catch (e) { console.error(e); node = errorScreen(e); }
    rootEl.appendChild(node);
    window.scrollTo(0, 0);
    var h = node.querySelector('[data-focus]') || node;
    h.setAttribute('tabindex', '-1');
    try { h.focus({ preventScroll: true }); } catch (e2) { /* ignore */ }
  }
  function rerender() { go(current.name, current.params); }

  function errorScreen(e) {
    return el('main', { class: 'screen center' }, [
      el('h1', { text: t('err.title'), attrs: { 'data-focus': '' } }), el('p', { text: t('err.body') }),
      btn('primary', t('err.reload'), function () { location.reload(); })
    ]);
  }

  var FLAME_SVG = '<svg viewBox="0 0 24 28" aria-hidden="true" focusable="false"><path d="M12 1 C13 7 20 9 20 18 A8 8 0 0 1 4 18 C4 13 7 11 8 7 C9 9 10 9 10.5 8.5 C11.5 6.5 11.5 3.5 12 1 Z" fill="currentColor"/><path d="M12 15 C13 18 16 18.5 15.5 21.5 A3.6 3.6 0 0 1 8.5 21.5 C8.5 19 11 18.5 12 15 Z" fill="#fff" opacity=".85"/></svg>';
  var BOLT_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M13.5 1 L4 14 h6 l-1.5 9 L20 9 h-6.5 z" fill="currentColor"/></svg>';
  var GOAL_N = 3, GOAL_COINS = 15, BOOST_MS = 5 * 60 * 1000;
  function streakCount() { var sv = S.get(); return MP.streak.count(sv.streak, MP.streak.dayKey(), sv.freezes); }
  function flameChip() {
    var c = streakCount();
    return btn('flamechip' + (c.safe ? ' lit' : '') + (c.alive ? '' : ' out'), el('span', null, [icon(FLAME_SVG, 'flame'), el('b', { text: String(c.n) })]), function () { go('streak'); }, { 'aria-label': t('streak.flame', { n: c.n }) });
  }
  function boostLeft() { return Math.max(0, S.get().boostUntil - Date.now()); }
  function boostChip() {
    var m = Math.ceil(boostLeft() / 60000);
    return el('span', { class: 'boostchip', attrs: { 'aria-label': t('boost.chip', { n: m }) } }, [icon(BOLT_SVG, 'bolt'), el('b', { text: '\u00d72 \u00b7 ' + m + 'm' })]);
  }
  function goalNow() { var g = S.get().goal, d = MP.streak.dayKey(); return g.day === d ? g : { day: d, n: 0, paid: false }; }
  function hud(opts) {
    var items = [];
    if (opts.back) items.push(btn('round ghost', icon(BACK_SVG), opts.back.fn, { 'aria-label': opts.back.label }));
    if (opts.title) items.push(el('h1', { class: 'hud-title', text: opts.title, attrs: { 'data-focus': '' } }));
    else items.push(el('span', { class: 'spacer' }));
    if (opts.flame) items.push(flameChip());
    if (boostLeft() > 0) items.push(boostChip());
    if (opts.coins !== false) items.push(el('span', { class: 'coins', attrs: { 'aria-label': t('hud.coins', { n: S.get().coins }) } }, [icon(A.coinIcon(), 'sm'), el('b', { text: String(S.get().coins) })]));
    (opts.right || []).forEach(function (r) { items.push(r); });
    return el('header', { class: 'hud' }, items);
  }
  var BACK_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15 5 L8 12 L15 19" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var PAUSE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="6" y="5" width="4" height="14" rx="1.5" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1.5" fill="currentColor"/></svg>';
  var SOUND_ON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 9 h4 l5 -4 v14 l-5 -4 h-4z" fill="currentColor"/><path d="M16 8 q3 4 0 8 M18.5 5.5 q5 6.5 0 13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>';
  var SOUND_OFF = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 9 h4 l5 -4 v14 l-5 -4 h-4z" fill="currentColor"/><path d="M16 9 l6 6 M22 9 l-6 6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>';

  var NOTE_ON = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 18V6l10 -2v12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/><circle cx="7" cy="18" r="3" fill="currentColor"/><circle cx="17" cy="16" r="3" fill="currentColor"/></svg>';
  var NOTE_OFF = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9 18V6l10 -2v12" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round" opacity=".55"/><circle cx="7" cy="18" r="3" fill="currentColor" opacity=".55"/><circle cx="17" cy="16" r="3" fill="currentColor" opacity=".55"/><path d="M3 3 L21 21" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>';
  function musicToggle() {
    var b = btn('round ghost', icon(S.get().music ? NOTE_ON : NOTE_OFF), function () {
      S.update(function (s) { s.music = !s.music; });
      MP.audio.setMusic(S.get().music, S.get().musicVol);
      b.textContent = ''; b.appendChild(icon(S.get().music ? NOTE_ON : NOTE_OFF));
      b.setAttribute('aria-pressed', S.get().music ? 'false' : 'true');
    }, { 'aria-label': t('set.musicToggle'), 'aria-pressed': S.get().music ? 'false' : 'true' });
    return b;
  }

  function soundToggle() {
    var b = btn('round ghost', icon(S.get().sound ? SOUND_ON : SOUND_OFF), function () {
      S.update(function (s) { s.sound = !s.sound; });
      MP.audio.setEnabled(S.get().sound);
      b.textContent = ''; b.appendChild(icon(S.get().sound ? SOUND_ON : SOUND_OFF));
      b.setAttribute('aria-pressed', S.get().sound ? 'false' : 'true');
      MP.audio.play('tap');
    }, { 'aria-label': t('set.soundToggle'), 'aria-pressed': S.get().sound ? 'false' : 'true' });
    return b;
  }

  /** Oval EN | BM switch: the label sits inside a pill that grows to fit, so text never overflows. */
  var GEAR_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 8.6a3.4 3.4 0 1 0 0 6.8 3.4 3.4 0 0 0 0-6.8z" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M10.4 3h3.2l.5 2.4 1.7.7 2.1-1.3 2.3 2.3-1.3 2.1.7 1.7 2.4.5v3.2l-2.4.5-.7 1.7 1.3 2.1-2.3 2.3-2.1-1.3-1.7.7-.5 2.4h-3.2l-.5-2.4-1.7-.7-2.1 1.3-2.3-2.3 1.3-2.1-.7-1.7L3 13.6v-3.2l2.4-.5.7-1.7-1.3-2.1 2.3-2.3 2.1 1.3 1.7-.7z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>';
  function settingsGear() { return btn('round ghost gearbtn', icon(GEAR_SVG), function () { go('settings'); }, { 'aria-label': t('menu.settings') }); }

  function langButtons() {
    var wrap = el('div', { class: 'langs', attrs: { role: 'group', 'aria-label': t('lang.choose') } });
    [['en', 'English'], ['ms', 'Bahasa Melayu']].forEach(function (l) {
      var on = MP.i18n.lang === l[0];
      wrap.appendChild(btn('lang' + (on ? ' on' : ''), l[1], function () {
        S.update(function (s) { s.lang = l[0]; }); applySettings(); rerender();
      }, { lang: l[0] === 'ms' ? 'ms' : 'en', 'aria-pressed': on ? 'true' : 'false' }));
    });
    return wrap;
  }

  /* ---------------- first run: language + starting rank ---------------- */
  SCREENS.intro = function (p, scope) {
    var step = p.step || 1;
    if (step === 1) {
      return el('main', { class: 'screen center intro' }, [
        el('div', { class: 'menu-bg', svg: A.scene('windmill', 'meadow') }),
        el('div', { class: 'panel' }, [
          el('div', { class: 'logo', svg: A.logo() }),
          icon(A.nimbo({ mood: 'happy', cls: 'big fly' }), 'nimbo-wrap'),
          el('h1', { text: t('intro.welcome'), attrs: { 'data-focus': '' } }),
          el('p', { text: t('intro.chooseLang') }),
          langButtons(),
          btn('primary big', t('intro.next'), function () { go('intro', { step: 2 }); })
        ])
      ]);
    }
    if (step === 2) {
      var sv0 = S.get(), ni = nameInput(sv0.name, t('prof.namePh'), t('prof.name')), ap = avatarPicker(sv0.avatar);
      return el('main', { class: 'screen center intro' }, [
        el('div', { class: 'menu-bg', svg: A.scene('windmill', 'meadow') }),
        el('div', { class: 'panel' }, [
          el('h1', { text: t('prof.introTitle'), attrs: { 'data-focus': '' } }),
          el('p', { text: t('prof.introBody') }), ni, ap.node,
          btn('primary big', t('intro.next'), function () {
            S.update(function (s) { s.name = S.cleanName(ni.value); s.avatar = ap.get(); });
            go('intro', { step: 3 });
          })
        ])
      ]);
    }
    var cur = S.get().band;
    var wrap = el('div', { class: 'ranks' });
    BAND_KEYS.forEach(function (k, i) {
      wrap.appendChild(btn('rank' + (cur === i ? ' on' : ''), el('span', null, [el('b', { text: t('band.' + k) }), el('small', { text: t('band.' + k + '.ages') })]), function () {
        S.update(function (s) { s.band = i; }); rerender2();
      }, { 'aria-pressed': cur === i ? 'true' : 'false' }));
    });
    function rerender2() { go('intro', { step: 3 }); }
    return el('main', { class: 'screen center intro' }, [
      el('div', { class: 'menu-bg', svg: A.scene('bridge', 'meadow') }),
      el('div', { class: 'panel' }, [
        el('h1', { text: t('intro.rankTitle'), attrs: { 'data-focus': '' } }),
        el('p', { text: t('intro.rankBody') }), wrap,
        btn('primary big', t('intro.start'), function () {
          S.update(function (s) { s.introDone = true; });
          go('level', { id: 'm1-1' });
        })
      ])
    ]);
  };

  /* ---------------- main menu ---------------- */
  function goalCard() {
    var g = goalNow(), n = Math.min(g.n, GOAL_N), met = n >= GOAL_N;
    var bar = el('div', { class: 'goalbar', attrs: { role: 'progressbar', 'aria-valuemin': '0', 'aria-valuemax': String(GOAL_N), 'aria-valuenow': String(n) } }, [el('span', { class: 'goalfill' })]);
    bar.firstChild.style.width = Math.round(100 * n / GOAL_N) + '%';
    return el('div', { class: 'goalcard' + (met ? ' met' : '') }, [el('b', { text: t('goal.title') }), bar, el('small', { text: met ? t('goal.met') : t('goal.n', { a: n, b: GOAL_N }) })]);
  }

  /* ---------------- daily gift (login streak) ---------------- */
    function streakStatus() { return MP.streak.status(S.get().streak, MP.streak.dayKey(), S.get().freezes); }
  function claimGift(then) {
    var r = MP.streak.claim(S.get().streak, MP.streak.dayKey(), S.get().freezes);
    if (!r) return;
    S.update(function (sv) { sv.coins += r.coins; sv.streak = r.st; sv.freezes = Math.max(0, sv.freezes - r.used); });
    MP.audio.play(r.perfect ? 'win' : 'coin');
    if (then) then(r);
  }
  function dayTile(n, state, reward) {
    var bonus = n === 7;
    return el('li', { class: 'daytile ' + state + (bonus ? ' big' : ''), attrs: { 'aria-label': t('streak.day', { n: n }) + ': ' + t('hud.coins', { n: reward + (bonus ? MP.streak.PERFECT_BONUS : 0) }) + (state === 'done' ? ', ' + t('streak.done') : state === 'today' ? ', ' + t('streak.today') : '') } }, [
      el('small', { text: t('streak.day', { n: n }) }),
      icon(A.coinIcon(), 'coinico'),
      el('b', { text: String(reward) }),
      bonus ? el('em', { text: t('streak.bonusShort', { n: MP.streak.PERFECT_BONUS }) }) : null,
      state === 'done' ? el('span', { class: 'tick', text: '✓', attrs: { 'aria-hidden': 'true' } }) : null
    ]);
  }
  SCREENS.streak = function (p) {
    var sv = S.get(), st = streakStatus(), claimable = st.state === 'claimable';
    var list = el('ol', { class: 'daygrid' });
    for (var i = 1; i <= 7; i++) {
      var state = i <= st.current ? 'done' : (claimable && i === st.day) ? 'today' : 'todo';
      list.appendChild(dayTile(i, state, MP.streak.REWARDS[i - 1]));
    }
    var node = el('main', { class: 'screen scroll streak' }, [
      hud({ title: t('streak.title'), flame: true, back: { label: t('nav.back'), fn: function () { go('menu'); } } }),
      el('p', { class: 'lead', text: t('streak.lead') }),
      list,
      el('p', { class: 'note', text: t('streak.bonus', { n: MP.streak.PERFECT_BONUS }) }),
      claimable ? btn('primary big', t('streak.claim', { n: st.reward + st.bonus }), function () {
        claimGift(function (r) {
          rerender();
          if (r.perfect) MP.ui.dialog({ title: t('streak.perfectTitle'), body: t('streak.perfectBody', { n: r.bonus }), buttons: [{ label: t('ok'), cls: 'primary' }] });
          else if (r.used) MP.ui.dialog({ title: t('streak.got', { n: r.coins }), body: t('streak.saved'), buttons: [{ label: t('ok'), cls: 'primary' }] });
          else if (r.restarted) MP.ui.dialog({ title: t('streak.got', { n: r.coins }), body: t('streak.restarted'), buttons: [{ label: t('ok'), cls: 'primary' }] });
        });
      }) : el('p', { class: 'reward', text: t('streak.claimed') }),
      el('p', { class: 'note', text: t('streak.stats', { a: sv.streak.best, b: sv.streak.weeks }) }),
      el('p', { class: 'note freezenote', text: t('streak.freezes', { n: sv.freezes }) })
    ]);
    return node;
  };

  /* ---------------- online friends (optional, grown-up switch) ---------------- */
  function friendCard(f, refresh) {
    var look = f.pal && f.pal.look ? A.creature(f.pal.look, { acc: f.pal.acc === null ? undefined : f.pal.acc, tint: f.pal.tint, cls: 'float' }) : A.avatar(f.avatar, '');
    var actions = [];
    if (f.status === 'friend') actions.push(btn('small cheerbtn' + (f.cheered ? ' done' : ''), f.cheered ? t('fr.cheered') : t('fr.cheer'), function (e) {
      if (f.cheered) return; e.currentTarget.classList.add('pop'); MP.audio.play('coin');
      MP.friends.cheer(f.id).then(function () { refresh(); });
    }));
    else if (f.status === 'incoming') actions.push(btn('small primary', t('fr.accept'), function () { MP.audio.play('unlock'); MP.friends.accept(f.id).then(function () { refresh(); }); }));
    else actions.push(el('small', { class: 'waiting', text: t('fr.waiting') }));
    return el('li', { class: 'fcard ' + f.status }, [
      icon(look, 'fpal'),
      el('div', { class: 'finfo' }, [el('b', { text: f.name || t('prof.player') }), el('small', { text: f.status === 'friend' || f.status === 'incoming' ? t('fr.stats', { a: f.stars, b: f.levels }) : t('fr.pending') })]),
      el('div', { class: 'facts' }, actions)
    ]);
  }

  /** Race dashboard: you and your accepted friends on one track. Stars decide the order; the track shows levels finished. */
  function raceBoard(friends) {
    var mine = (function () { var st = 0, dn = 0, sv = S.get(); Object.keys(sv.levels).forEach(function (k) { st += sv.levels[k].stars; if (sv.levels[k].done) dn++; }); return { you: true, name: sv.name || t('prof.player'), avatar: sv.avatar, stars: st, levels: dn }; })();
    var rows = friends.filter(function (f) { return f.status === 'friend'; }).concat([mine]);
    if (rows.length < 2) return null;
    rows.sort(function (a, b) { return b.stars - a.stars || b.levels - a.levels; });
    var top = Math.max.apply(null, rows.map(function (r) { return r.levels; })), goal = Math.max(10, Math.ceil(top / 0.9));
    var place = rows.indexOf(mine) + 1;
    var lanes = el('ol', { class: 'lanes' });
    rows.forEach(function (r, i) {
      var tok = el('span', { class: 'racer', attrs: { 'aria-hidden': 'true' } }, [icon(r.pal && r.pal.look ? A.creature(r.pal.look, { acc: r.pal.acc === null ? undefined : r.pal.acc, tint: r.pal.tint }) : A.avatar(r.avatar, ''), 'rtok')]);
      var track = el('div', { class: 'track' }, [el('span', { class: 'fill' }), tok, el('span', { class: 'flag', attrs: { 'aria-hidden': 'true' }, text: '⚑' })]);
      var pct = Math.min(100, Math.round(100 * r.levels / goal));
      track.style.setProperty('--to', pct + '%');
      var lane = el('li', { class: 'lane' + (r.you ? ' you' : '') + (i === 0 ? ' lead' : '') }, [
        el('span', { class: 'rank', text: '#' + (i + 1) }),
        el('div', { class: 'lanebody' }, [el('div', { class: 'lanehead' }, [el('b', { text: r.you ? t('fr.you') + ' · ' + r.name : r.name }), el('small', { text: t('fr.stats', { a: r.stars, b: r.levels }) })]), track])
      ]);
      lane.setAttribute('aria-label', '#' + (i + 1) + ' ' + r.name + ', ' + t('fr.stats', { a: r.stars, b: r.levels }));
      lane.style.setProperty('--i', i); lanes.appendChild(lane);
    });
    requestAnimationFrame(function () { requestAnimationFrame(function () { lanes.classList.add('go'); }); });   // tokens glide from the start line
    return el('section', { class: 'race' }, [el('h2', { text: t('fr.raceTitle') }), el('p', { class: 'note', text: t('fr.racePlace', { a: place, b: rows.length }) }), lanes, el('p', { class: 'note', text: t('fr.raceNote') })]);
  }

  function askGrownUp(onOk) {
    var a = 6 + Math.floor(Math.random() * 4), b = 5 + Math.floor(Math.random() * 4);
    var inp = nameInput('', '?', t('fr.gateLabel')); inp.inputMode = 'numeric'; inp.maxLength = 2;
    MP.ui.dialog({ title: t('fr.gateTitle'), body: el('div', null, [el('p', { text: t('fr.gateBody') }), el('p', { class: 'gateq', text: a + ' + ' + b + ' = ?' }), inp]),
      buttons: [{ label: t('fr.gateGo'), cls: 'primary big', onClick: function () { if (Number(inp.value) === a + b) onOk(); else { MP.audio.play('nope'); setTimeout(function () { askGrownUp(onOk); }, 60); } } }, { label: t('cancel'), cls: 'ghost' }] });
  }
  SCREENS.friends = function (p, scope) {
    var on = MP.friends.isOn(), list = el('ul', { class: 'flist', attrs: { 'aria-live': 'polite' } }), note = el('p', { class: 'note frnote' });
    var main = el('main', { class: 'screen scroll friends' }, [hud({ title: t('fr.title'), back: { label: t('nav.back'), fn: function () { go('menu'); } } })]);
    if (!MP.friends.available()) { main.appendChild(el('p', { class: 'lead', text: t('fr.unavailable') })); return main; }
    if (!on) {
      main.appendChild(el('p', { class: 'lead', text: t('fr.offLead') }));
      main.appendChild(el('p', { class: 'note', text: t('fr.privacy') }));
      main.appendChild(btn('primary big', t('fr.turnOn'), function () {
        askGrownUp(function () {
          note.textContent = t('fr.connecting');
          MP.friends.turnOn().then(function (r) { if (r.ok) go('friends'); else note.textContent = t('fr.offline'); });
        });
      }));
      main.appendChild(note); return main;
    }
    var codeBox = el('div', { class: 'mycode' }, [el('small', { text: t('fr.yourCode') }), el('b', { class: 'code', text: MP.friends.code() }),
      btn('small', t('fr.copy'), function (e) { try { navigator.clipboard.writeText(MP.friends.code()); e.currentTarget.textContent = t('fr.copied'); } catch (x) { /* shown on screen anyway */ } })]);
    var inp = nameInput('', 'ABC234', t('fr.codeLabel')); inp.maxLength = 6; inp.autocapitalize = 'characters';
    var raceBox = el('div', { class: 'racebox' });
    function refresh() {
      MP.friends.sync(); MP.friends.list().then(function (r) {
        if (current.name !== 'friends') return;
        list.textContent = ''; raceBox.textContent = '';
        if (r.ok) { var rb = raceBoard(r.data); if (rb) raceBox.appendChild(rb); }
        if (!r.ok) { note.textContent = t('fr.offline'); return; }
        if (!r.data.length) list.appendChild(el('li', { class: 'fempty', text: t('fr.empty') }));
        r.data.forEach(function (f, i) { var c = friendCard(f, refresh); c.style.setProperty('--i', i); list.appendChild(c); });
      });
    }
    function addIt() {
      var v = inp.value.trim(); if (!v) return; note.textContent = '';
      MP.friends.add(v).then(function (r) {
        var m = { sent: 'fr.sent', accepted: 'fr.nowFriends', exists: 'fr.exists', notfound: 'fr.notFound', self: 'fr.self', limit: 'fr.limit' };
        note.textContent = r.ok ? t(m[r.data] || 'fr.offline') : t('fr.offline'); if (r.ok && (r.data === 'sent' || r.data === 'accepted')) { inp.value = ''; MP.audio.play('unlock'); }
        refresh();
      });
    }
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') addIt(); });
    main.appendChild(codeBox);
    main.appendChild(el('div', { class: 'addrow' }, [inp, btn('primary', t('fr.add'), addIt)]));
    main.appendChild(note); main.appendChild(raceBox); main.appendChild(list);
    main.appendChild(el('p', { class: 'note', text: t('fr.privacy') }));
    main.appendChild(el('div', { class: 'setrow' }, [btn('ghost danger', t('fr.turnOff'), function () { MP.ui.confirm({ title: t('fr.turnOffTitle'), body: t('fr.turnOffBody'), yes: t('fr.turnOffYes'), no: t('cancel'), onYes: function () { MP.friends.turnOff(); go('friends'); } }); })]));
    // cheers received since last time become coins (2 each), then show the list
    MP.friends.collect().then(function (r) {
      if (r.ok && r.data > 0) { S.update(function (v) { v.coins += 2 * r.data; }); MP.audio.play('coin'); note.textContent = t('fr.gotCheers', { n: r.data, c: 2 * r.data }); if (navigator.vibrate) navigator.vibrate(10); }
    });
    refresh();
    return main;
  };

  /* ---------------- version and update info ---------------- */
  function changelogCard() {
    var log = MP.changelog || [], box = el('section', { class: 'setrow about' });
    box.appendChild(el('h2', { text: t('ver.title') }));
    box.appendChild(el('p', { class: 'verline' }, [el('b', { text: t('ver.version', { v: MP.config.version }) }), log[0] ? document.createTextNode(' · ' + t('ver.released', { d: log[0].date })) : null]));
    function entry(c) {
      var ul = el('ul', { class: 'changes' });
      c.items.forEach(function (it) { ul.appendChild(el('li', { text: tx(it) })); });
      return el('div', { class: 'change' }, [el('h3', { text: t('ver.version', { v: c.v }) + ' · ' + c.date }), ul]);
    }
    if (log[0]) { box.appendChild(el('h3', { text: t('ver.whatsNew') })); box.appendChild(entry(log[0])); }
    if (log.length > 1) {
      var d = el('details', { class: 'older' }, [el('summary', { text: t('ver.older') })]);
      log.slice(1).forEach(function (c) { d.appendChild(entry(c)); });
      box.appendChild(d);
    }
    box.appendChild(el('p', { class: 'note', text: t('ver.howTo') }));
    return box;
  }
  /** After an update, a returning player sees a small "new" note on the menu (no pop-up). Opening Settings marks it seen. */
  function showNewBadge() { var sv = S.get(); return !!(MP.changelog && MP.changelog[0] && sv.seenVersion !== MP.config.version && Object.keys(sv.levels).length > 0); }

  SCREENS.menu = function () {
    awardFinds();
    var sv = S.get(), next = currentLevel(), started = Object.keys(sv.levels).length > 0;
    var stx = streakStatus(), ready = stx.state === 'claimable';
    var canExit = MP.config.homeUrl && location.protocol !== 'file:';
    var playLabel = !started ? t('menu.play') : next ? t('menu.continue') : t('menu.playAgain');
    return el('main', { class: 'screen menu' }, [
      el('div', { class: 'menu-bg', svg: A.scene('windmill', 'meadow') }),
      el('div', { class: 'menu-top' }, [btn('profilechip', el('span', { class: 'pchipin' }, [avatarIcon(sv.avatar), el('b', { text: sv.name || t('prof.player') })]), function () { go('profiles'); }, { 'aria-label': t('prof.title') + ': ' + (sv.name || t('prof.player')) }),
        el('span', { class: 'spacer' }), soundToggle(), musicToggle(), settingsGear()]),
      el('div', { class: 'menu-center' }, [
        el('div', { class: 'logo', svg: A.logo() }),
        el('div', { class: 'nimbo-row' }, [icon(A.nimbo({ mood: 'idle', hat: equippedHat(), cls: 'big fly' }), 'nimbo-wrap'),
          (sv.buddy && critterById(sv.buddy)) ? btn('buddybtn', icon(palSvg(critterById(sv.buddy), { cls: 'float' }), 'buddyico'), function () { go('pals', { sel: sv.buddy }); }, { 'aria-label': t('pals.title') }) : null]),
        el('h1', { class: 'sr-only', text: MP.config.gameName, attrs: { 'data-focus': '' } }),
        sv.name ? el('p', { class: 'hello', text: t('prof.hello', { name: sv.name }) }) : null,
        btn('primary big', playLabel, function () {
          if (!started) go('level', { id: 'm1-1' }); else if (next) go('map'); else go('map');
        }),
        showNewBadge() ? btn('newbadge', t('ver.badge', { v: MP.config.version }), function () { go('settings'); }) : null,
        btn('giftbtn' + (ready ? ' ready' : ''), el('span', null, [icon(FLAME_SVG, 'flame' + (streakCount().safe ? ' lit' : '')), document.createTextNode(' ' + (ready ? t('streak.chipReady') : t('streak.flame', { n: streakCount().n })))]), function () { go('streak'); }),
        goalCard(),
        el('div', { class: 'menu-grid' }, [
          btn('', t('menu.map'), function () { go('map'); }),
          btn('', t('menu.dashboard'), function () { go('dashboard'); }),
          btn('', t('menu.pals'), function () { go('pals'); }),
          MP.friends.available() ? btn('', t('menu.friends'), function () { go('friends'); }) : null,
          btn('', t('menu.collectionHats'), function () { go('collection'); }),
          btn('', t('menu.parents'), function () { go('parents'); })
        ]),
        testBanner(),
        canExit ? el('a', { class: 'btn ghost', text: t('menu.exit'), attrs: { href: MP.config.homeUrl } }) : null,
        el('p', { class: 'version', text: MP.config.gameName + ' · ' + (MP.entitlements.isTestMode() ? t('test.badge') : t('menu.demoBuild')) })
      ])
    ]);
  };

  /* ---------------- world map ---------------- */
  /**
   * Layout: islands are stacked upward (island 1 at the bottom). Inside an island the levels read in
   * normal order: the lowest row holds the first levels left-to-right, the next row up continues, and so on,
   * so the numbers always increase left-to-right and bottom-to-top.
   */
  function rowsFor(n) {
    if (n <= 4) return [n];
    var R = Math.ceil(n / 3), base = Math.floor(n / R), extra = n - base * R, rows = [], i;
    for (i = 0; i < R; i++) rows.push(base);
    var mid = []; for (i = 0; i < R; i++) mid.push(i);
    mid.sort(function (x, y) { return Math.abs(x - (R - 1) / 2) - Math.abs(y - (R - 1) / 2); });   // extras go to the middle rows
    for (i = 0; i < extra; i++) rows[mid[i]]++;
    return rows;
  }
  /* ---------------- map: a vertical path of round level buttons, one coloured banner per island, a treasure chest at the end ---------------- */
  var UNIT_COLORS = [['#58cc02', '#46a302'], ['#1cb0f6', '#1899d6'], ['#ce82ff', '#a35fd6'], ['#ff9600', '#d97d00'], ['#ff86d0', '#d964ab'], ['#2bc4b4', '#1f9c8f'], ['#ff6b6b', '#d94f4f'], ['#8c7bff', '#6d5ce0']];
  var WIGGLE = [0, 38, 62, 38, 0, -38, -62, -38];
  function chestSvg() {
    return '<svg viewBox="0 0 80 72" aria-hidden="true" focusable="false"><ellipse cx="40" cy="67" rx="30" ry="4" fill="rgba(0,0,0,.18)"/>' +
      '<rect x="10" y="30" width="60" height="34" rx="6" fill="#1cb0f6" stroke="#1899d6" stroke-width="3"/><rect x="10" y="30" width="60" height="9" fill="#1899d6"/>' +
      '<rect x="8" y="30" width="9" height="34" rx="3" fill="#ffc800"/><rect x="63" y="30" width="9" height="34" rx="3" fill="#ffc800"/>' +
      '<g class="chestglow"><ellipse cx="40" cy="32" rx="22" ry="8" fill="#fff3a0"/></g>' +
      '<g class="chestlid"><path d="M8 30 Q8 8 40 8 Q72 8 72 30 Z" fill="#ffc800" stroke="#e5a800" stroke-width="3"/><rect x="8" y="26" width="64" height="6" fill="#e5a800"/><rect x="34" y="24" width="12" height="14" rx="3" fill="#fff" stroke="#e5a800" stroke-width="2"/></g></svg>';
  }
  function islandStars(isl) { var n = 0; MP.levels.byIsland(isl.id).forEach(function (l) { var r = levelRec(l.id); if (r && r.done) n += r.stars; }); return n; }
  var PRIZE_KEY = { coins: 'chest.prize.coins', boost: 'chest.prize.boost', freeze: 'chest.prize.freeze', find: 'chest.prize.find' };
  function seeded(str) { var h = 2166136261; for (var i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619); return (h >>> 0) / 4294967296; }
  /** Every chest holds coins plus one surprise. The surprise is fixed per island (same chest, same prize), so reloading never rerolls it. */
  function chestPrize(islandId) {
    var sv = S.get(), r = seeded('chest:' + islandId), pool = [];
    HATS.forEach(function (h) { if (sv.wardrobe.owned.indexOf(h.id) === -1) pool.push({ kind: 'hat', id: h.id }); });
    Object.keys(PAL_AT).forEach(function (id) { if (sv.closet.indexOf(id) === -1) pool.push({ kind: 'acc', id: id }); });
    if (r < 0.3) return { kind: 'coins', n: 15 };
    if (r < 0.55) return { kind: 'boost' };
    if (r < 0.78) return sv.freezes < MP.streak.MAX_FREEZES ? { kind: 'freeze' } : { kind: 'boost' };
    return pool.length ? { kind: 'find', item: pool[Math.floor(seeded('pick:' + islandId) * pool.length)] } : { kind: 'coins', n: 15 };
  }
  function chestBox(isl) {
    var coins = 10 + islandStars(isl), box = el('div', { class: 'chestbox' }), pic = el('div', { class: 'chestpic shake', svg: chestSvg() }), msg = el('p', { class: 'chestmsg', attrs: { role: 'status', 'aria-live': 'polite' }, text: '' });
    var open = btn('primary big', t('chest.openBtn'), function () {
      open.disabled = true; pic.classList.remove('shake'); pic.classList.add('opened');
      var prize = chestPrize(isl.id), prizeText = '';
      S.update(function (v) {
        v.coins += coins; v.chests[isl.id] = true;
        if (prize.kind === 'coins') v.coins += prize.n;
        else if (prize.kind === 'boost') v.boostUntil = Math.max(Date.now(), v.boostUntil) + BOOST_MS;
        else if (prize.kind === 'freeze') v.freezes = Math.min(MP.streak.MAX_FREEZES, v.freezes + 1);
        else if (prize.kind === 'find') { if (prize.item.kind === 'hat') v.wardrobe.owned.push(prize.item.id); else v.closet.push(prize.item.id); }
      });
      prizeText = t(PRIZE_KEY[prize.kind], { n: prize.n, name: prize.item ? t((prize.item.kind === 'hat' ? 'hat.' : 'acc.') + prize.item.id) : '' });
      MP.audio.play('chest'); var hc = document.querySelector('.hud .coins'); if (hc) { hc.querySelector('b').textContent = String(S.get().coins); hc.setAttribute('aria-label', t('hud.coins', { n: S.get().coins })); }
      msg.textContent = t('chest.found', { n: coins }) + ' ' + prizeText; msg.classList.add('show');
      for (var k = 0; k < 8; k++) { var c = el('span', { class: 'chestcoin', attrs: { 'aria-hidden': 'true' } }, [icon(A.coinIcon(), 'tiny')]); c.style.setProperty('--a', (k * 45) + 'deg'); box.appendChild(c); }
      open.hidden = true; if (current.name === 'map') { var cb = document.querySelector('[data-chest="' + isl.id + '"]'); if (cb) { cb.classList.remove('ready'); cb.classList.add('done'); cb.setAttribute('aria-label', t('chest.title') + ' — ' + t('chest.opened')); } }
    });
    box.appendChild(pic); box.appendChild(msg); box.appendChild(open);
    return box;
  }
  function openChest(isl) { MP.ui.dialog({ title: t('chest.title'), body: chestBox(isl), cls: 'chestdlg', buttons: [{ label: t('chest.close'), cls: 'ghost' }] }); }
  function chestWaiting(islandId) {
    var lvs = MP.levels.byIsland(islandId);
    return !S.get().chests[islandId] && lvs.length > 0 && lvs.every(function (l) { return isDone(l.id); });
  }

  SCREENS.map = function (p, scope) {
    var cur = currentLevel(), sv = S.get(), all = MP.levels.all();
    var shown = MP.packs.allIslands().filter(function (i) { return MP.levels.byIsland(i.id).length; });
    var missing = MP.packs.premium().filter(function (pk) { return !MP.levels.all().some(function (l) { return l.pack === pk.id; }); });
    var map = el('div', { class: 'map dmap' }), focusNode = null, buddy = sv.buddy && critterById(sv.buddy), idx = 0;

    shown.forEach(function (isl, i) {
      var lvs = MP.levels.byIsland(isl.id), done = lvs.filter(function (l) { return isDone(l.id); }).length, col = UNIT_COLORS[i % UNIT_COLORS.length];
      var sec = el('section', { class: 'unit' }); sec.style.setProperty('--c', col[0]); sec.style.setProperty('--cd', col[1]);
      sec.appendChild(el('div', { class: 'islandname' + (isUnlocked(lvs[0]) ? '' : ' locked') }, [
        el('small', { text: t('map.unit', { n: i + 1 }) + ' · ' + t('map.islandProgress', { a: done, b: lvs.length }) }), el('b', { text: tx(isl.name) })]));
      lvs.forEach(function (lv) {
        var rec = levelRec(lv.id), open = isUnlocked(lv), isDn = !!(rec && rec.done), isCur = cur && cur.id === lv.id;
        var label = t('map.levelN', { n: lv.order }) + ' ' + tx(lv.title) + ' — ' + (isDn ? t('map.stars', { n: rec.stars }) : open ? t('map.ready') : t('map.locked'));
        var inner = [];
        if (!open) inner.push(icon(A.lock(), 'lockico')); else inner.push(el('b', { class: 'num', text: String(lv.order) }));
        var node = btn('node' + (isDn ? ' done' : '') + (open ? '' : ' locked') + (isCur ? ' current' : ''), el('span', { class: 'nodeinner' }, inner),
          function () { if (!open) { MP.audio.play('nope'); toast(t('map.lockedMsg')); return; } go('level', { id: lv.id }); },
          { 'aria-label': label, 'aria-disabled': open ? null : 'true', 'data-order': String(lv.order) });
        var stars = el('span', { class: 'nstars', attrs: { 'aria-hidden': 'true' } });
        if (isDn) for (var s = 1; s <= 3; s++) stars.appendChild(icon(A.star(s <= rec.stars), 'tiny'));
        var wrap = el('div', { class: 'nodewrap' }, [isCur ? el('span', { class: 'startbubble', text: t('map.start') }) : null, node, el('span', { class: 'ncap', text: tx(lv.title) }), isDn ? stars : null]);
        wrap.style.transform = 'translateX(' + WIGGLE[idx % WIGGLE.length] + 'px)'; idx++;
        if (isCur) {
          focusNode = wrap; wrap.appendChild(icon(A.nimbo({ mood: 'happy', hat: equippedHat(), cls: 'map-nimbo fly' }), 'nimbo-pin'));
          if (buddy) wrap.appendChild(icon(palSvg(critterById(sv.buddy), { cls: 'map-buddy float' }), 'buddy-pin'));
        }
        sec.appendChild(wrap);
      });
      var allDone = done === lvs.length, opened = !!sv.chests[isl.id], ready = allDone && !opened;
      var chest = btn('chestbtn' + (ready ? ' ready' : '') + (opened ? ' done' : ''), el('span', { class: 'chestico', svg: chestSvg() }),
        function () {
          if (opened || sv.chests[isl.id]) { toast(t('chest.opened')); return; }
          if (!allDone) { MP.audio.play('nope'); toast(t('chest.locked')); return; }
          openChest(isl);
        }, { 'data-chest': isl.id, 'aria-label': t('chest.title') + ' — ' + (opened ? t('chest.opened') : ready ? t('chest.open') : t('chest.locked')) });
      sec.appendChild(chest);
      map.appendChild(sec);
    });

    if (missing.length) {   // premium packs that are not owned: one teaser at the end instead of many locked islands
      var n = missing.reduce(function (a, pk) { return a + pk.levels; }, 0);
      map.appendChild(el('div', { class: 'unit teaserunit' }, [btn('teaser', el('span', null, [icon(A.lock(), 'lockico sm'), el('b', { text: t('map.moreIslands', { n: n }) }), el('small', { text: t('premium.badge') })]),
        function () { go('premium', { id: missing[0].id }); }, { 'aria-label': t('map.moreIslands', { n: n }) + ' — ' + t('premium.badge') })]));
    }

    var toastEl = el('div', { class: 'toast', attrs: { role: 'status', 'aria-live': 'polite' } });
    function toast(msg) { toastEl.textContent = msg; toastEl.classList.add('show'); scope.timeout(function () { toastEl.classList.remove('show'); }, 2200); }
    scope.timeout(function () {
      if (focusNode && focusNode.scrollIntoView) { try { focusNode.scrollIntoView({ block: 'center', behavior: 'auto' }); } catch (e) { /* ignore */ } }
    }, 30);

    return el('main', { class: 'screen mapscreen' }, [
      hud({ title: t('map.title'), flame: true, back: { label: t('nav.menu'), fn: function () { go('menu'); } },
        right: [btn('small ghost', t('menu.pals'), function () { go('pals'); }, { 'aria-label': t('pals.title') })] }),
      testBanner(),
      map, toastEl
    ]);
  };

  /* ---------------- level (story -> puzzle -> complete) ---------------- */
  SCREENS.level = function (p, scope) {
    var lv = MP.levels.byId(p.id);
    if (!lv || !isUnlocked(lv)) { scope.timeout(function () { go('map'); }, 0); return el('main', { class: 'screen center' }); }
    var screen = el('main', { class: 'screen levelscreen' });
    var stage = el('div', { class: 'stage' });
    var state = { run: null, puzzle: null, svg: null, nimbo: null, solved: false, ps: null };
    var first = !isDone(lv.id);

    var top = hud({
      title: tx(lv.title), back: { label: t('nav.map'), fn: function () { go('map'); } },
      right: [btn('round ghost', icon(PAUSE_SVG), pause, { 'aria-label': t('lvl.pause') })]
    });
    screen.appendChild(top); screen.appendChild(stage);

    function npcAvatar() { return icon(A.npc(lv.npc), 'npc'); }

    function story() {
      var tutorial = !S.get().tutorialDone && lv.id === 'm1-1';
      var card = el('section', { class: 'storycard' }, [
        el('div', { class: 'scenewrap', svg: A.scene(lv.scene, lv.island) }),
        el('div', { class: 'speech' }, [npcAvatar(), el('p', { text: tx(lv.story) })]),
        tutorial ? el('ol', { class: 'howto' }, [
          el('li', { text: t('tut.1') }), el('li', { text: t('tut.2') }), el('li', { text: t('tut.3') }), el('li', { text: t('tut.4') })
        ]) : null,
        el('p', { class: 'learn', text: t('lvl.learn', { x: tx(lv.learn) }) }),
        btn('primary big', t('lvl.go'), begin)
      ]);
      stage.textContent = ''; stage.appendChild(card);
    }

    function begin() {
      var pick = AD.pickPuzzle(S.get(), lv);
      state.run = { tier: pick.tier, wrong: 0, hints: 0, helped: false, claimed: false, reason: pick.reason };
      mount(pick.puzzle, pick.reason);
    }

    function setMood(m) { if (state.nimbo) state.nimbo.querySelector('svg').setAttribute('data-mood', m); }

    function mount(puzzle, reason) {
      if (state.ps) state.ps.dispose();
      state.ps = new MP.util.Scope();
      MP.currentPuzzle = puzzle;   // read-only hook used by tests/e2e.py
      state.puzzle = puzzle; state.solved = false; state.hinted = false; state.tries = 0; state.progress = 0;
      var run = state.run;
      stage.textContent = '';
      var sceneWrap = el('div', { class: 'scenewrap', svg: A.scene(lv.scene, lv.island) });
      state.svg = sceneWrap.firstChild;
      var host = el('div', { class: 'host' });
      var feedback = el('p', { class: 'feedback', attrs: { role: 'status', 'aria-live': 'polite' } });
      var hintBox = el('p', { class: 'hintbox', attrs: { hidden: '' } });
      var helpBox = el('div', { class: 'helpbox', attrs: { hidden: '' } });
      var offers = el('div', { class: 'offers' });
      state.nimbo = icon(A.nimbo({ mood: 'idle', hat: equippedHat(), cls: 'small' }), 'nimbo-wrap');
      var hintBtn = btn('hintbtn', el('span', null, [state.nimbo, el('b', { text: t('lvl.hint') })]), function () {
        if (state.solved) return;
        if (hintBox.hasAttribute('hidden')) {
          hintBox.removeAttribute('hidden'); hintBox.textContent = tx(puzzle.hint);
          if (!state.hinted) { state.hinted = true; run.hints++; }
          setMood('think'); MP.audio.play('select');
        } else hintBox.setAttribute('hidden', '');
      }, { 'aria-label': t('lvl.hintAria') });

      function say(msg, kind) { feedback.textContent = msg || ''; feedback.setAttribute('data-kind', kind || 'info'); }

      function refreshOffers() {
        offers.textContent = '';
        var o = AD.offers(run.tier, state.tries);
        if (o.friendlier) offers.appendChild(btn('ghost', t('lvl.friendlier'), function () {
          var nt = AD.friendlierTier(run.tier); if (nt == null) return;
          run.tier = nt; mount(lv.tiers[nt], 'friendlier'); say(t('fb.friendlierOn'), 'good');
        }));
        if (o.help) offers.appendChild(btn('ghost', t('lvl.showMe'), function () {
          helpBox.removeAttribute('hidden'); helpBox.textContent = '';
          helpBox.appendChild(el('p', { text: tx(puzzle.explain) }));
          helpBox.appendChild(btn('primary', t('lvl.helpContinue'), function () { run.helped = true; finish(puzzle); }));
        }));
      }

      var ctx = {
        host: host, svg: state.svg, scope: state.ps, art: A,
        say: say,
        wrong: function () {
          if (state.solved) return;
          run.wrong++; state.tries++; MP.audio.play('nope'); setMood('think'); refreshOffers();
        },
        progress: function (pp) { state.progress = pp; A.setProgress(state.svg, pp); },
        solved: function () { if (state.solved) return; state.solved = true; say('', 'info'); celebrate(puzzle); }
      };

      stage.appendChild(sceneWrap);
      if (reason === 'friendlier' || reason === 'booster') {
        stage.appendChild(el('p', { class: 'adaptnote', text: reason === 'booster' ? t('adapt.booster') : t('adapt.friendly') }));
      } else if (reason === 'rising') stage.appendChild(el('p', { class: 'adaptnote', text: t('adapt.rising') }));
      stage.appendChild(el('section', { class: 'promptcard' }, [npcAvatar(), el('p', { class: 'prompt', text: tx(puzzle.prompt) })]));
      stage.appendChild(host);
      stage.appendChild(feedback);
      stage.appendChild(el('div', { class: 'helprow' }, [hintBtn]));
      stage.appendChild(hintBox); stage.appendChild(offers); stage.appendChild(helpBox);
      MP.puzzles.render(puzzle.type, puzzle.spec, ctx);
    }

    function celebrate(puzzle) {
      var svg = state.svg, from = state.progress || 0;
      setMood('happy'); MP.audio.play('ok');
      stage.querySelectorAll('.host button').forEach(function (b) { b.disabled = true; });
      var quick = MP.ui.reducedMotion();
      var steps = quick ? 1 : 8, i;
      for (i = 1; i <= steps; i++) (function (i) {
        state.ps.timeout(function () { A.setProgress(svg, from + (1 - from) * i / steps); }, i * (quick ? 0 : 90));
      })(i);
      state.ps.timeout(function () { A.setDone(svg, true); MP.audio.play('unlock'); }, quick ? 50 : 8 * 90 + 60);
      state.ps.timeout(function () { finish(puzzle); }, quick ? 500 : 8 * 90 + 1100);
    }

    function finish(puzzle) {
      var run = state.run;
      if (run.claimed) return;     // double-tap / double-timer guard: rewards are claimed once per run
      run.claimed = true;
      var result = null;
      S.update(function (sv) {
        var rec = sv.levels[lv.id] || (sv.levels[lv.id] = { done: false, stars: 0, plays: 0, lastPuzzle: null, hints: 0, wrong: 0 });
        var kind = AD.record(sv, lv, run), stars = AD.stars(run), wasFirst = !rec.done, old = rec.stars;
        var coins = wasFirst ? 10 + 5 * stars : 5 * Math.max(0, stars - old), boosted = sv.boostUntil > Date.now() && coins > 0, goalHit = false, gd = MP.streak.dayKey();
        if (boosted) coins *= 2;
        if (sv.goal.day !== gd) sv.goal = { day: gd, n: 0, paid: false };
        sv.goal.n += 1;
        if (!sv.goal.paid && sv.goal.n >= GOAL_N) { sv.goal.paid = true; goalHit = true; coins += GOAL_COINS; }
        rec.done = true; rec.stars = Math.max(old, stars); rec.plays += 1; rec.lastPuzzle = puzzle.id;
        rec.hints += run.hints; rec.wrong += run.wrong;
        sv.coins += coins;
        var newCritter = sv.collection.indexOf(lv.critter.id) === -1;
        if (newCritter) sv.collection.push(lv.critter.id);
        if (lv.id === 'm1-1') sv.tutorialDone = true;
        sv.history.push({ id: lv.id, stars: stars, wrong: run.wrong, hints: run.hints, day: dayNum() });
        if (sv.history.length > 40) sv.history = sv.history.slice(-40);
        result = { kind: kind, stars: stars, coins: coins, boosted: boosted, goalHit: goalHit, first: wasFirst, newCritter: newCritter, finds: [] };
      });
      result.finds = awardFinds();
      MP.audio.play('win');
      complete(puzzle, result);
    }

    function complete(puzzle, r) {
      var next = MP.levels.next(lv.id), last = !next;
      var body = el('div', { class: 'complete' });
      var stars = el('div', { class: 'bigstars', attrs: { role: 'img', 'aria-label': t('map.stars', { n: r.stars }) } });
      for (var i = 1; i <= 3; i++) stars.appendChild(icon(A.star(i <= r.stars), 'bigstar s' + i));
      body.appendChild(stars);
      body.appendChild(el('p', { class: 'reward', text: r.coins > 0 ? t('done.coins', { n: r.coins }) : t('done.noCoins') }));
      if (r.boosted) body.appendChild(el('p', { class: 'boostline', text: t('done.boosted') }));
      if (r.goalHit) body.appendChild(el('p', { class: 'goalline', text: t('goal.done', { n: GOAL_COINS }) }));
      body.appendChild(el('p', { class: 'why' }, [el('b', { text: t('done.why') + ' ' }), document.createTextNode(tx(puzzle.explain))]));
      if (r.newCritter) body.appendChild(el('div', { class: 'newcritter' }, [
        icon(A.creature(lv.critter.look, { cls: 'pop' }), 'critterico'),
        el('p', null, [el('b', { text: t('done.newFriend', { name: tx(lv.critter.name) }) }), el('br'), document.createTextNode(tx(lv.critter.blurb))])
      ]));
      (r.finds || []).forEach(function (f) {
        var nm = f.kind === 'hat' ? t('hat.' + f.id) : t('acc.' + f.id);
        body.appendChild(el('div', { class: 'newcritter find' }, [
          icon(f.kind === 'hat' ? A.nimbo({ mood: 'happy', hat: f.id, cls: 'pop' }) : A.creature(lv.critter.look, { acc: f.id, cls: 'pop' }), 'critterico'),
          el('p', null, [el('b', { text: t('find.title') }), el('br'), document.createTextNode(t(f.kind === 'hat' ? 'find.hat' : 'find.acc', { name: nm }))])
        ]));
      });
      if (r.kind === 'struggle') body.appendChild(el('p', { class: 'adaptnote', text: t('adapt.afterStruggle') }));
      else if (r.kind === 'clean') body.appendChild(el('p', { class: 'adaptnote', text: t('adapt.afterClean') }));
      if (chestWaiting(lv.island)) body.appendChild(el('div', { class: 'newcritter chestwin' }, [el('b', { text: t('chest.reach') }), chestBox({ id: lv.island })]));
      if (next && r.first) body.appendChild(el('p', { class: 'unlocked', text: t('done.unlocked', { name: tx(next.title) }) }));
      var buttons = [];
      buttons.push({ label: last ? t('done.finish') : t('done.next'), cls: 'primary big', onClick: function () { if (last) go('demodone'); else go('level', { id: next.id }); } });
      buttons.push({ label: t('done.replay'), cls: '', onClick: function () { go('level', { id: lv.id }); } });
      buttons.push({ label: t('nav.map'), cls: 'ghost', onClick: function () { go('map'); } });
      MP.ui.dialog({ title: t('done.title'), body: body, buttons: buttons, dismissable: false, cls: 'complete-card' });
    }

    function pause() {
      MP.ui.dialog({
        title: t('lvl.paused'),
        body: el('div', { class: 'pausebody' }, [el('p', { text: t('lvl.pausedBody') }), el('div', { class: 'pausesound' }, [soundToggle(), el('span', { text: t('set.soundToggle') })]),
          el('div', { class: 'pauselang' }, [btn('small', MP.i18n.lang === 'ms' ? 'English' : 'Bahasa Melayu', function () { S.update(function (v) { v.lang = MP.i18n.lang === 'ms' ? 'en' : 'ms'; }); applySettings(); rerender(); }, { lang: MP.i18n.lang === 'ms' ? 'en' : 'ms' }), el('small', { text: t('lvl.langNote') })])]),
        dismissable: true,
        buttons: [
          { label: t('lvl.resume'), cls: 'primary big' },
          { label: t('nav.map'), cls: 'ghost', onClick: function () { go('map'); } }
        ]
      });
    }
    scope.add(function () { if (state.ps) state.ps.dispose(); });

    if (first || !S.get().tutorialDone) story(); else begin();
    return screen;
  };

  /* ---------------- collection + Nimbo's wardrobe ---------------- */
  SCREENS.collection = function (p, scope) {
    var sv = S.get(), sel = p.sel || null;
    var grid = el('div', { class: 'critters' });
    MP.levels.all().forEach(function (lv) {
      var has = sv.collection.indexOf(lv.critter.id) !== -1;
      grid.appendChild(btn('critter' + (has ? '' : ' locked') + (sel === lv.id ? ' on' : ''),
        el('span', null, [icon(has ? palSvg(lv.critter) : A.creature(lv.critter.look, { locked: true }), 'critterico'), el('small', { text: has ? palName(lv.critter) : t('col.unknown') })]),
        function () { go('collection', { sel: lv.id }); },
        { 'aria-label': has ? palName(lv.critter) : t('col.locked', { n: lv.order }) }));
    });
    var detail = null;
    if (sel) {
      var l = MP.levels.byId(sel), has = sv.collection.indexOf(l.critter.id) !== -1;
      detail = el('section', { class: 'critterdetail' }, [icon(has ? palSvg(l.critter, { cls: 'big' }) : A.creature(l.critter.look, { locked: true, cls: 'big' }), 'critterico big'),
        el('p', null, has ? [el('b', { text: palName(l.critter) }), el('br'), document.createTextNode(tx(l.critter.blurb))] : [document.createTextNode(t('col.finishToFind', { name: tx(l.title) }))]),
        has ? btn('small', t('pals.dress'), function () { go('pals', { sel: l.critter.id }); }) : null]);
    }
    var wardrobe = el('div', { class: 'hats' });
    var eq = sv.wardrobe.equipped;
    wardrobe.appendChild(btn('hat' + (!eq ? ' on' : ''), t('hat.none'), function () { S.update(function (s) { s.wardrobe.equipped = null; }); rerender(); }, { 'aria-pressed': !eq ? 'true' : 'false' }));
    HATS.forEach(function (h) {
      var owned = sv.wardrobe.owned.indexOf(h.id) !== -1, left = h.at - doneCount();
      var label = t('hat.' + h.id) + (owned ? '' : ' · ' + t('find.at', { n: h.at }));
      wardrobe.appendChild(btn('hat' + (eq === h.id ? ' on' : '') + (owned ? '' : ' locked'), label, function () {
        if (!owned) { lockedFind(Math.max(1, left)); return; }
        S.update(function (s) { s.wardrobe.equipped = (s.wardrobe.equipped === h.id) ? null : h.id; }); rerender();
      }, { 'aria-pressed': eq === h.id ? 'true' : 'false' }));
    });
    return el('main', { class: 'screen scroll' }, [
      hud({ title: t('col.title'), back: { label: t('nav.back'), fn: function () { go('menu'); } } }),
      el('p', { class: 'lead', text: t('col.count', { a: sv.collection.length, b: MP.levels.all().length }) }),
      grid, detail,
      el('section', { class: 'wardrobe' }, [el('h2', { text: t('hat.title') }), icon(A.nimbo({ mood: 'happy', hat: eq, cls: 'big fly' }), 'nimbo-wrap'), el('p', { text: t('hat.body') }), wardrobe])
    ]);
  };

  /* ---------------- Pal Park: pets you can pet, feed, play with and take along ---------------- */
  SCREENS.pals = function (p, scope) {
    var sv = S.get(), pals = ownedPals();
    var back = { label: t('nav.back'), fn: function () { go('menu'); } };
    if (!pals.length) {
      return el('main', { class: 'screen scroll' }, [hud({ title: t('pals.title'), back: back }),
        el('p', { class: 'lead', text: t('pals.empty') }), btn('primary big', t('nav.map'), function () { go('map'); })]);
    }
    var sel = pals.filter(function (c) { return c.id === p.sel; })[0] || pals.filter(function (c) { return c.id === sv.buddy; })[0] || pals[0];
    var name = palName(sel);
    function rec() { return palRec(sel.id); }

    var stage = el('div', { class: 'palstage' });
    var palBtn = btn('palbtn', icon(palSvg(sel, { cls: 'palbig' }), 'palwrap'), function () { pet(); }, { 'aria-label': t('pals.pet') + ': ' + name });
    var says = el('p', { class: 'palsay', attrs: { role: 'status', 'aria-live': 'polite' }, text: t('pals.hello.' + bondOf(rec()), { name: name }) });
    var fill = el('i'), bondLabel = el('b'), counts = el('small');
    var hudNode = hud({ title: t('pals.title'), back: back });

    function refresh() {
      var r = rec(), b = bondOf(r);
      fill.style.width = (b * 20) + '%';
      bondLabel.textContent = t('pals.bond') + ': ' + t('pals.bond.' + b);
      meter.setAttribute('aria-valuenow', String(b));
      counts.textContent = t('pals.counts', { fed: r.fed, played: r.played });
      var cb = hudNode.querySelector('.coins b'); if (cb) cb.textContent = String(S.get().coins);
    }
    function anim(cls) {
      palBtn.classList.remove('hop', 'spin', 'wiggle'); void palBtn.offsetWidth; palBtn.classList.add(cls);
      scope.timeout(function () { palBtn.classList.remove(cls); }, 900);
    }
    function hearts(n) {
      for (var i = 0; i < n; i++) (function (i) {
        var h = el('span', { class: 'heart', text: '♥', attrs: { 'aria-hidden': 'true' } });
        h.style.left = (38 + Math.round(Math.random() * 24)) + '%'; h.style.animationDelay = (i * 120) + 'ms';
        stage.appendChild(h); scope.timeout(function () { if (h.parentNode) h.parentNode.removeChild(h); }, 1700 + i * 120);
      })(i);
    }
    function say(key, n) { says.textContent = t('pals.' + key + '.' + n, { name: name }); }
    function pick(n) { return 1 + Math.floor(Math.random() * n); }
    function bump(field) {
      var before = bondOf(rec()), after;
      S.update(function (v) {
        var r = ensurePal(v, sel.id);
        r[field] += 1; r.bond = bondOf(r);
      });
      after = bondOf(rec());
      refresh();
      if (after > before) { MP.audio.play('unlock'); says.textContent = t('pals.levelUp', { name: name, rank: t('pals.bond.' + after) }); hearts(6); }
    }
    function pet() { MP.audio.play('tap'); anim('wiggle'); hearts(2); say('pet', pick(3)); }
    function feed() {
      if (S.get().coins < 3) { MP.audio.play('nope'); says.textContent = t('pals.tooFew'); return; }
      S.update(function (v) { v.coins -= 3; });
      anim('hop'); hearts(3); say('feed', pick(2)); bump('fed');
    }
    function play() {
      MP.audio.play('win'); anim('spin'); hearts(3); say('play', pick(2));
      var toy = icon(A.star(true), 'toy'); stage.appendChild(toy); scope.timeout(function () { if (toy.parentNode) toy.parentNode.removeChild(toy); }, 1200);
      bump('played');
    }

    stage.appendChild(palBtn);
    var meter = el('div', { class: 'pbar bond', attrs: { role: 'meter', 'aria-valuemin': '0', 'aria-valuemax': '5', 'aria-label': t('pals.bond') } }, [fill]);
    var isBuddy = S.get().buddy === sel.id;
    var picker = el('div', { class: 'palpick', attrs: { role: 'group', 'aria-label': t('pals.pick') } }, pals.map(function (c) {
      return btn('critter small' + (c.id === sel.id ? ' on' : ''), el('span', null, [icon(palSvg(c), 'critterico'), el('small', { text: palName(c) })]),
        function () { go('pals', { sel: c.id }); }, { 'aria-pressed': c.id === sel.id ? 'true' : 'false', 'aria-label': palName(c) });
    }));
    refresh();
    return el('main', { class: 'screen scroll palscreen' }, [
      hudNode, stage, says,
      el('div', { class: 'bondbox' }, [bondLabel, meter, counts]),
      el('div', { class: 'btnrow wrap palacts' }, [
        btn('', t('pals.pet'), pet), btn('', t('pals.feed'), feed), btn('', t('pals.play'), play),
        btn(isBuddy ? 'on' : '', isBuddy ? t('pals.buddyOn') : t('pals.buddy'), function () {
          S.update(function (v) { v.buddy = (v.buddy === sel.id) ? null : sel.id; }); go('pals', { sel: sel.id });
        }, { 'aria-pressed': isBuddy ? 'true' : 'false' })
      ]),
      dressUp(sel), el('h2', { text: t('pals.pick') }), picker,
      btn('ghost', t('pals.toCollection'), function () { go('collection'); })
    ]);
  };


  /* ---------------- dress-up: nickname, colour, hats ---------------- */
  function dressUp(sel) {
    var r = palRec(sel.id), name = palName(sel), box = el('section', { class: 'dress' });
    function again() { go('pals', { sel: sel.id }); }
    function setPal(fn) { S.update(function (v) { fn(ensurePal(v, sel.id)); }); again(); }

    // nickname
    var inp = nameInput(r.nick, t('pals.nick'), t('pals.nick'));
    inp.maxLength = 12;
    function saveNick() { var v = S.cleanName(inp.value).slice(0, 12); setPal(function (p) { p.nick = v; }); }
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') saveNick(); });
    box.appendChild(el('h2', { text: t('pals.dress') }));
    box.appendChild(el('div', { class: 'nickrow' }, [inp, btn('small', t('prof.save'), saveNick)]));

    // colour
    var sw = el('div', { class: 'swatches', attrs: { role: 'group', 'aria-label': t('pals.colour') } });
    sw.appendChild(btn('swatch orig' + (r.tint === null || r.tint === undefined ? ' on' : ''), t('acc.natural'), function () { setPal(function (p) { p.tint = null; }); },
      { 'aria-pressed': (r.tint === null || r.tint === undefined) ? 'true' : 'false' }));
    A.TINTS.forEach(function (c, i) {
      var b = btn('swatch' + (r.tint === i ? ' on' : ''), '', function () { setPal(function (p) { p.tint = i; }); }, { 'aria-pressed': r.tint === i ? 'true' : 'false', 'aria-label': t('pals.swatch', { n: i + 1 }) });
      b.style.background = 'linear-gradient(' + c[0] + ',' + c[1] + ')'; sw.appendChild(b);
    });
    box.appendChild(el('h3', { text: t('pals.colour') })); box.appendChild(sw);

    // hats and accessories (found by finishing levels, then free to swap between all pals)
    var owned = S.get().closet, grid = el('div', { class: 'accgrid', attrs: { role: 'group', 'aria-label': t('pals.hats') } });
    function chip(id, label, on, lockAt, fn) {
      grid.appendChild(btn('accbtn' + (on ? ' on' : '') + (lockAt ? ' locked' : ''), el('span', null, [icon(A.creature(sel.look, { acc: id === 'natural' ? undefined : id, tint: r.tint, cls: 'accprev' }), 'accico'), el('small', { text: lockAt ? t('find.at', { n: lockAt }) : label })]), fn,
        { 'aria-pressed': on ? 'true' : 'false', 'aria-label': label + (lockAt ? ', ' + t('find.at', { n: lockAt }) : '') }));
    }
    chip('natural', t('acc.natural'), r.acc === null || r.acc === undefined, 0, function () { setPal(function (p) { p.acc = null; }); });
    chip('none', t('acc.none'), r.acc === 'none', 0, function () { setPal(function (p) { p.acc = 'none'; }); });
    A.PAL_ACCS.forEach(function (id) {
      var has = owned.indexOf(id) !== -1, label = t('acc.' + id), at = PAL_AT[id];
      chip(id, label, r.acc === id, has ? 0 : at, function () {
        if (has) { setPal(function (p) { p.acc = id; }); return; }
        lockedFind(Math.max(1, at - doneCount()));
      });
    });
    box.appendChild(el('h3', { text: t('pals.hats') })); box.appendChild(grid);
    return box;
  }


  /* ---------------- players (profiles): switch, add, rename, back up ---------------- */
  var folds = {};      // which Players sections the child left open (kept while the game is open)
  function fold(title, key, kids) {
    var d = el('details', { class: 'psec fold' }, [el('summary', { text: title })].concat(kids));
    if (folds[key]) d.open = true;
    d.addEventListener('toggle', function () { folds[key] = d.open; });
    return d;
  }
  SCREENS.profiles = function (p, scope) {
    var sv = S.get(), P = S.profiles, list = P.list();
    var status = el('p', { class: 'note', attrs: { role: 'status', 'aria-live': 'polite' }, text: '' });
    function say(msg) { status.textContent = msg; }
    function again() { applySettings(); go('profiles'); }

    // who is playing now: rename + avatar + delete
    var ni = nameInput(sv.name, t('prof.namePh'), t('prof.name'));
    var ap = avatarPicker(sv.avatar);
    function saveMe() { S.update(function (s) { s.name = S.cleanName(ni.value); s.avatar = ap.get(); }); MP.audio.play('tap'); go('profiles'); }
    ni.addEventListener('keydown', function (e) { if (e.key === 'Enter') saveMe(); });
    var me = fold(t('prof.editTitle'), 'me', [el('label', { class: 'note', text: t('prof.name') }), ni, ap.node,
      el('div', { class: 'btnrow wrap' }, [btn('primary', t('prof.save'), saveMe),
        btn('ghost danger', t('prof.delete'), function () {
          if (P.count() <= 1) { say(t('prof.lastOne')); return; }
          MP.ui.confirm({ title: t('prof.deleteTitle', { name: sv.name || t('prof.player') }), body: t('prof.deleteBody'), yes: t('prof.deleteYes'), no: t('cancel'),
            onYes: function () { P.remove(P.activeId()); again(); } });
        })])]);

    // everyone
    var cards = list.map(function (e) {
      return btn('pcard' + (e.active ? ' on' : ''), el('span', { class: 'pcardin' }, [avatarIcon(e.avatar), el('span', null, [el('b', { text: e.name || t('prof.player') }), el('small', { text: e.active ? t('prof.playing') : t('prof.progress', { stars: e.stars, levels: e.levels }) })])]),
        function () { if (e.active) return; P.switchTo(e.id); MP.audio.play('unlock'); applySettings(); go('menu'); },
        { 'aria-pressed': e.active ? 'true' : 'false', 'aria-label': (e.name || t('prof.player')) + ', ' + t('prof.progress', { stars: e.stars, levels: e.levels }) });
    });

    // add
    var nn = nameInput('', t('prof.namePh'), t('prof.name')), na = avatarPicker('nimbo');
    function addIt() {
      if (!P.canAdd()) { say(t('prof.full', { n: S.MAX_PROFILES })); return; }
      P.create(nn.value, na.get()); MP.audio.play('unlock'); applySettings(); go('menu');
    }
    nn.addEventListener('keydown', function (e) { if (e.key === 'Enter') addIt(); });
    var add = P.canAdd()
      ? fold(t('prof.add'), 'add', [nn, na.node, btn('primary', t('prof.addBtn'), addIt)])
      : fold(t('prof.add'), 'add', [el('p', { class: 'note', text: t('prof.full', { n: S.MAX_PROFILES }) })]);

    // backup
    var file = document.createElement('input'); file.type = 'file'; file.accept = '.json,application/json'; file.className = 'sr-only'; file.setAttribute('aria-label', t('prof.import'));
    file.addEventListener('change', function () {
      var f = file.files && file.files[0]; if (!f) return;
      if (f.size > 400000) { say(t('prof.importBad')); return; }
      var rd = new FileReader();
      rd.onload = function () {
        var r = S.profiles.importText(String(rd.result));
        if (r === 'bad') { say(t('prof.importBad')); return; }
        if (r === 'full') { say(t('prof.full', { n: S.MAX_PROFILES })); return; }
        MP.audio.play('unlock'); applySettings(); go('profiles'); say(t('prof.importOk'));
      };
      rd.onerror = function () { say(t('prof.importBad')); };
      rd.readAsText(f);
    });
    function exportIt() {
      try {
        var blob = new Blob([S.profiles.exportActive()], { type: 'application/json' }), a = document.createElement('a');
        a.href = URL.createObjectURL(blob); a.download = 'mathipelago-' + ((S.get().name || 'player').replace(/[^A-Za-z0-9_-]+/g, '-') || 'player') + '.json';
        document.body.appendChild(a); a.click();
        scope.timeout(function () { URL.revokeObjectURL(a.href); if (a.parentNode) a.parentNode.removeChild(a); }, 500);
      } catch (e) { say(t('err.title')); }
    }
    var backup = el('section', { class: 'psec' }, [el('h2', { text: t('prof.backupTitle') }), el('p', { class: 'note', text: t('prof.backupBody') }),
      el('div', { class: 'btnrow wrap' }, [btn('', t('prof.export'), exportIt), btn('', t('prof.import'), function () { file.click(); })]), file,
      el('p', { class: 'note', text: t('prof.localNote') })]);

    return el('main', { class: 'screen scroll profiles' }, [
      hud({ title: t('prof.title'), back: { label: t('nav.back'), fn: function () { go('menu'); } } }),
      el('p', { class: 'lead', text: t('prof.lead') }),
      el('section', { class: 'psec' }, [el('h2', { text: t('prof.switch') }), el('div', { class: 'pcards' }, cards)]),
      me, add, backup, status
    ]);
  };

  /* ---------------- progress dashboard ---------------- */
  function fmtDay(n, opts) {
    try { return new Date(Math.floor(n / 10000), Math.floor(n / 100) % 100 - 1, n % 100).toLocaleDateString(MP.i18n.lang === 'ms' ? 'ms-MY' : 'en-GB', opts); } catch (e) { return String(n); }
  }
  SCREENS.dashboard = function () {
    var sv = S.get(), all = MP.levels.all(), nextLv = currentLevel();
    function tile(label, value, extra) {
      return el('div', { class: 'tile' }, [el('b', { text: String(value) }), el('span', { text: label }), extra || null]);
    }
    function bar(pct, cls) { var i = el('i'); i.style.width = Math.max(0, Math.min(100, pct)) + '%'; return el('div', { class: 'pbar ' + (cls || '') }, [i]); }

    var tiles = el('div', { class: 'tiles' }, [
      tile(t('dash.stars'), totalStars() + ' / ' + all.length * 3), tile(t('dash.levels'), doneCount() + ' / ' + all.length),
      tile(t('dash.coins'), sv.coins), tile(t('dash.pals'), ownedPals().length + ' / ' + all.length)]);

    // this week: stars per day from the last 40 finished runs
    var days = [], perDay = {}, anyRuns = false, max = 3;
    sv.history.forEach(function (h) { perDay[h.day] = (perDay[h.day] || 0) + h.stars; });
    for (var i = 6; i >= 0; i--) { var d = new Date(); d.setDate(d.getDate() - i); days.push({ n: dayNum(d), d: d }); }
    days.forEach(function (x) { x.v = perDay[x.n] || 0; if (x.v) anyRuns = true; if (x.v > max) max = x.v; });
    var chart = el('div', { class: 'week', attrs: { role: 'img', 'aria-label': t('dash.week') + ': ' + days.map(function (x) { return fmtDay(x.n, { weekday: 'short' }) + ' ' + x.v; }).join(', ') } },
      days.map(function (x) {
        var b = el('div', { class: 'wbar' }, [el('i')]); b.firstChild.style.height = (x.v ? Math.max(8, x.v / max * 100) : 0) + '%';
        return el('div', { class: 'wcol', attrs: { 'aria-hidden': 'true' } }, [el('span', { class: 'wval', text: x.v ? String(x.v) : '' }), b, el('span', { class: 'wday', text: fmtDay(x.n, { weekday: 'short' }) })]);
      }));

    var islandRows = MP.packs.allIslands().filter(function (isl) { return MP.levels.byIsland(isl.id).length; }).map(function (isl) {
      var lvs = MP.levels.byIsland(isl.id), done = lvs.filter(function (l) { return isDone(l.id); }).length, st = starsOf(lvs);
      var prem = isl.pack !== 'free-demo';
      return el('li', { class: 'irow' }, [
        el('div', { class: 'irowtop' }, [el('b', { text: tx(isl.name) }), prem ? el('small', { class: 'ptag', text: t('dash.premiumTag') }) : null,
          el('span', { text: lvs.length ? t('dash.of', { a: done, b: lvs.length }) : '' })]),
        lvs.length ? bar(done / lvs.length * 100, 'mint') : el('p', { class: 'note', text: t('premium.badge') }),
        lvs.length ? el('small', { class: 'istars', text: st + ' / ' + lvs.length * 3 + ' ★' }) : null]);
    });

    // skills acquired: every finished level teaches its skill; more levels and stars level it up
    var bySkill = {};
    all.forEach(function (l) {
      var k = l.skill, o = bySkill[k] || (bySkill[k] = { k: k, total: 0, done: 0, stars: 0 });
      o.total++; var r = levelRec(l.id); if (r && r.done) { o.done++; o.stars += r.stars; }
    });
    var skillList = Object.keys(bySkill).map(function (k) {
      var o = bySkill[k]; o.rank = o.done >= 6 && o.stars >= o.done * 2 ? 3 : o.done >= 3 ? 2 : o.done >= 1 ? 1 : 0; return o;
    }).sort(function (x, y) { return (y.rank - x.rank) || (y.done - x.done) || (x.k < y.k ? -1 : 1); });
    var started = skillList.filter(function (o) { return o.done > 0; }).length;
    var skillCards = skillList.map(function (o) {
      var st = el('span', { class: 'skstars', attrs: { 'aria-hidden': 'true' } });
      for (var q = 1; q <= 3; q++) st.appendChild(icon(A.star(q <= o.rank), 'tiny'));
      return el('li', { class: 'skill r' + o.rank }, [
        el('div', { class: 'skhead' }, [el('b', { text: t('skill.' + o.k) }), st]),
        el('small', { text: t('dash.skillProgress', { a: o.done, b: o.total, s: o.stars }) }),
        el('span', { class: 'skrank', text: t('dash.rank.' + o.rank) })]);
    });
    var skillsSec = el('section', { class: 'psec skillsec' }, [el('h2', { text: t('dash.skillsLearned') }),
      el('p', { class: 'note', text: t('dash.skillsLead') }),
      el('p', { class: 'skcount', text: t('dash.skillCount', { a: started, b: skillList.length }) }),
      el('ul', { class: 'plain skillgrid' }, skillCards)]);

    var review = [];
    var skillRows = Object.keys(MP.topicsInUse()).map(function (k) {
      var tp = sv.topics[k] || { ok: 0, bad: 0, hints: 0, adj: 0, review: false }, tot = tp.ok + tp.bad, rate = tot ? tp.ok / tot : 0;
      var lvl = !tot ? 'new' : (rate >= .8 && tot >= 4) || tp.adj > 0 ? 'strong' : rate >= .55 ? 'growing' : 'learning';
      if (tp.review) review.push(t('topic.' + k));
      return el('li', { class: 'srow' }, [
        el('div', { class: 'irowtop' }, [el('b', { text: t('topic.' + k) }), el('span', { class: 'lvl ' + lvl, text: t('dash.skill.' + lvl) })]),
        bar(tot ? rate * 100 : 0, 'grape')]);
    });

    var recent = sv.history.slice(-8).reverse().filter(function (h) { return MP.levels.byId(h.id); }).map(function (h) {
      var lv = MP.levels.byId(h.id), st = el('span', { class: 'nstars', attrs: { role: 'img', 'aria-label': t('map.stars', { n: h.stars }) } });
      for (var q = 1; q <= 3; q++) st.appendChild(icon(A.star(q <= h.stars), 'tiny'));
      return el('li', { class: 'rrow' }, [el('span', null, [el('b', { text: tx(lv.title) }), el('small', { text: ' · ' + fmtDay(h.day, { day: 'numeric', month: 'short' }) })]), st]);
    });

    var next = nextLv
      ? el('section', { class: 'psec nextcard' }, [el('h2', { text: t('dash.next') }), el('p', { text: t('dash.nextBody', { name: tx(nextLv.title) }) }),
          btn('primary', t('dash.playNow'), function () { go('level', { id: nextLv.id }); })])
      : el('section', { class: 'psec nextcard' }, [el('h2', { text: t('dash.next') }), el('p', { text: t('dash.allDone') })]);

    return el('main', { class: 'screen scroll dashboard' }, [
      hud({ title: t('dash.title'), back: { label: t('nav.back'), fn: function () { go('menu'); } } }),
      testBanner(),
      el('p', { class: 'lead', text: t('dash.keepGoing') }),
      tiles, skillsSec, next,
      el('section', { class: 'psec' }, [el('h2', { text: t('dash.week') }), el('p', { class: 'note', text: anyRuns ? t('dash.weekBody') : t('dash.noWeek') }), chart]),
      el('section', { class: 'psec' }, [el('h2', { text: t('dash.islands') }), el('ul', { class: 'plain' }, islandRows)]),
      el('section', { class: 'psec' }, [el('h2', { text: t('dash.skills') }), el('p', { class: 'note', text: t('dash.skillNote') }), el('ul', { class: 'plain' }, skillRows),
        review.length ? el('p', { class: 'notice', text: t('dash.review', { topics: review.join(', ') }) }) : null]),
      el('section', { class: 'psec' }, [el('h2', { text: t('dash.recent') }), recent.length ? el('ul', { class: 'plain' }, recent) : el('p', { text: t('dash.noRecent') })]),
      btn('ghost', t('menu.parents'), function () { go('parents'); })
    ]);
  };

  /* ---------------- settings ---------------- */
  function seg(label, options, current, onPick) {
    var g = el('div', { class: 'seg', attrs: { role: 'group', 'aria-label': label } });
    options.forEach(function (o) {
      g.appendChild(btn('segbtn' + (o.v === current ? ' on' : ''), o.label, function () { onPick(o.v); }, { 'aria-pressed': o.v === current ? 'true' : 'false' }));
    });
    return el('div', { class: 'setrow' }, [el('h2', { text: label }), g]);
  }
  function askReset() {
    MP.ui.confirm({
      title: t('reset.title'), body: t('reset.body'), no: t('reset.keep'), yes: t('reset.yes'),
      onYes: function () { S.resetProgress(); applySettings(); go('menu'); }
    });
  }

  function musicVolumeRow() {
    var sv = S.get(), out = el('output', { class: 'volout', text: t('set.volumePct', { n: sv.musicVol }) });
    var r = document.createElement('input');
    r.type = 'range'; r.min = '0'; r.max = '100'; r.step = '5'; r.value = String(sv.musicVol); r.className = 'volrange'; r.disabled = !sv.music;
    r.setAttribute('aria-label', t('set.musicVolume'));
    r.addEventListener('input', function () {
      var v = Number(r.value); out.textContent = t('set.volumePct', { n: v });
      S.update(function (s) { s.musicVol = v; }); MP.audio.setMusic(S.get().music, v);
    });
    return el('div', { class: 'setrow' }, [el('h2', { text: t('set.musicVolume') }), el('div', { class: 'volbox' }, [r, out])]);
  }

  SCREENS.settings = function () {
    if (S.get().seenVersion !== MP.config.version) S.update(function (x) { x.seenVersion = MP.config.version; });
    var sv = S.get();
    return el('main', { class: 'screen scroll' }, [
      hud({ title: t('set.title'), coins: false, back: { label: t('nav.back'), fn: function () { go('menu'); } } }),
      el('div', { class: 'setrow' }, [el('h2', { text: t('set.language') }), langButtons()]),
      seg(t('set.sound'), [{ v: true, label: t('set.soundOn') }, { v: false, label: t('set.soundOff') }], sv.sound,
        function (v) { S.update(function (s) { s.sound = v; }); applySettings(); rerender(); }),
      seg(t('set.music'), [{ v: true, label: t('set.musicOn') }, { v: false, label: t('set.musicOff') }], sv.music,
        function (v) { S.update(function (s) { s.music = v; }); applySettings(); rerender(); }),
      musicVolumeRow(),
      seg(t('set.theme'), [{ v: null, label: t('set.themeAuto') }, { v: 'light', label: t('set.themeLight') }, { v: 'dark', label: t('set.themeDark') }], sv.theme,
        function (v) { S.update(function (s) { s.theme = v; }); applySettings(); rerender(); }),
      seg(t('set.haptics'), [{ v: true, label: t('set.hapticsOn') }, { v: false, label: t('set.hapticsOff') }], sv.haptics,
        function (v) { S.update(function (s) { s.haptics = v; }); applySettings(); if (v) MP.audio.buzz('ok'); rerender(); }),
      seg(t('set.motion'), [{ v: null, label: t('set.motionAuto') }, { v: 'reduce', label: t('set.motionReduce') }, { v: 'full', label: t('set.motionFull') }], sv.motion,
        function (v) { S.update(function (s) { s.motion = v; }); applySettings(); rerender(); }),
      seg(t('set.textSize'), [{ v: 1, label: 'A' }, { v: 1.15, label: 'A+' }, { v: 1.3, label: 'A++' }], sv.textScale,
        function (v) { S.update(function (s) { s.textScale = v; }); applySettings(); rerender(); }),
      seg(t('set.band'), BAND_KEYS.map(function (k, i) { return { v: i, label: t('band.' + k) }; }), sv.band,
        function (v) { S.update(function (s) { s.band = v; }); rerender(); }),
      el('p', { class: 'note', text: t('set.bandNote') }),
      el('div', { class: 'setrow' }, [btn('ghost danger', t('reset.button'), askReset)]),
      changelogCard(),
      el('p', { class: 'version', text: MP.config.gameName + ' ' + MP.config.version })
    ]);
  };

  /* ---------------- parents & teachers ---------------- */
  SCREENS.parents = function () {
    var sv = S.get(), all = MP.levels.all();
    function section(title, nodes) { return el('section', { class: 'psec' }, [el('h2', { text: title })].concat(nodes)); }
    function para(k, v) { return el('p', { text: t(k, v) }); }

    var rows = all.map(function (lv) {
      var r = levelRec(lv.id) || { done: false, stars: 0, plays: 0, hints: 0, wrong: 0 };
      return el('tr', null, [el('td', { text: lv.order + '. ' + tx(lv.title) }), el('td', { text: t('skill.' + lv.skill) }),
        el('td', { text: r.done ? t('par.done') : '—' }), el('td', { text: String(r.stars) }), el('td', { text: String(r.hints) }), el('td', { text: String(r.wrong) })]);
    });
    var table = el('div', { class: 'tablewrap' }, [el('table', null, [
      el('thead', null, [el('tr', null, ['par.col.level', 'par.col.skill', 'par.col.status', 'par.col.stars', 'par.col.hints', 'par.col.mistakes'].map(function (k) { return el('th', { text: t(k) }); }))]),
      el('tbody', null, rows)])]);

    var topicRows = Object.keys(MP.topicsInUse()).map(function (k) {
      var tp = sv.topics[k] || { ok: 0, bad: 0, hints: 0, adj: 0, review: false };
      var state = tp.adj > 0 ? t('par.stepHarder') : tp.adj < 0 ? t('par.stepFriendlier') : t('par.steady');
      return el('li', { text: t('topic.' + k) + ': ' + t('par.topicLine', { ok: tp.ok, bad: tp.bad, hints: tp.hints }) + ' · ' + state + (tp.review ? ' · ' + t('par.review') : '') });
    });

    var islandList = MP.packs.allIslands().filter(function (i) { return MP.levels.byIsland(i.id).length; }).map(function (i) { return el('li', null, [el('b', { text: tx(i.name) + ': ' }), document.createTextNode(MP.levels.byIsland(i.id).map(function (l) { return t('skill.' + l.skill); }).join(', '))]); });
    var packList = MP.packs.all().map(function (pk) {
      return el('li', null, [el('b', { text: tx(pk.name) + ' — ' }), document.createTextNode(pk.free ? t('par.free') : MP.entitlements.hasPack(pk.id) ? t('par.testUnlocked') : t('par.paidNotYet'))]);
    });

    return el('main', { class: 'screen scroll parents' }, [
      hud({ title: t('par.title'), coins: false, back: { label: t('nav.back'), fn: function () { go('menu'); } } }),
      el('p', { class: 'lead', text: t('par.intro') }),
      btn('small', t('par.dashboardLink'), function () { go('dashboard'); }),
      section(t('par.summary'), [
        el('ul', { class: 'facts' }, [
          el('li', { text: t('par.levelsDone', { a: doneCount(), b: all.length }) }),
          el('li', { text: t('par.starsTotal', { n: totalStars() }) }),
          el('li', { text: t('par.companions', { a: sv.collection.length, b: all.length }) })
        ]), table]),
      section(t('par.topics'), [el('ul', { class: 'facts' }, islandList), para('par.curriculumNote')]),
      section(t('par.adapt'), [para('par.adaptBody'), el('ul', { class: 'facts' }, topicRows)]),
      section(t('par.freePaid'), [el('ul', { class: 'facts' }, packList), para('par.purchaseBody')]),
      section(t('par.storage'), [para('par.storageBody'), para(MP.store.isPersistent() ? 'par.storageOk' : 'par.storageMemory')]),
      section(t('par.privacy'), [para('par.privacyBody'), para('par.privacyDraft')]),
      section(t('par.reset'), [para('par.resetBody'), btn('ghost danger', t('reset.button'), askReset)]),
      el('p', { class: 'note', text: t('par.contact', { mail: MP.config.supportEmail }) })
    ]);
  };

  /* ---------------- premium preview (honest: no purchase happens in this build) ---------------- */
  SCREENS.premium = function (p) {
    var pack = MP.packs.byId(p.id) || MP.packs.premium()[0];
    var status = el('p', { class: 'note', attrs: { role: 'status', 'aria-live': 'polite' } });
    var unlocked = MP.entitlements.hasPack(pack.id) && MP.entitlements.isLoaded(pack.id);
    var list = MP.packs.premium().map(function (pk) {
      return btn('ghost small' + (pk.id === pack.id ? ' on' : ''), tx(pk.name), function () { go('premium', { id: pk.id }); }, { 'aria-pressed': pk.id === pack.id ? 'true' : 'false' });
    });
    return el('main', { class: 'screen scroll premium' }, [
      hud({ title: t('premium.title'), coins: false, back: { label: t('nav.map'), fn: function () { go('map'); } } }),
      el('div', { class: 'ribbon', text: t('premium.badge') }),
      el('h2', { text: tx(pack.name) }), el('p', { class: 'lead', text: tx(pack.blurb) }),
      el('p', { text: t('premium.levels', { n: pack.levels }) }),
      el('h3', { text: t('premium.practise') }), el('ul', { class: 'facts' }, pack.topics.map(function (x) { return el('li', { text: tx(x) }); })),
      unlocked ? el('p', { class: 'notice', text: t('premium.unlockedTest') }) : el('p', { class: 'notice', text: t('premium.notReady') }),
      unlocked ? btn('primary big', t('premium.playIsland'), function () {
        var first = MP.levels.all().filter(function (l) { return l.pack === pack.id; })[0];
        if (first && isUnlocked(first)) go('level', { id: first.id }); else go('map');
      }) : null,
      (!unlocked && MP.entitlements.hasPack(pack.id)) ? el('p', { class: 'notice', text: t('premium.loadFailed') }) : null,
      unlocked ? null : btn('primary big', t('premium.ask'), function () {
        MP.entitlements.startCheckout(pack.id).then(function (res) {
          if (res.ok && res.url) { window.open(res.url, '_blank', 'noopener'); status.textContent = t('premium.opened'); }
          else status.textContent = t('premium.unavailable');
        });
      }),
      status,
      el('h3', { text: t('premium.more') }), el('div', { class: 'btnrow wrap' }, list),
      btn('ghost', t('nav.map'), function () { go('map'); })
    ]);
  };

  /* ---------------- demo complete ---------------- */
  SCREENS.demodone = function () {
    var prem = MP.packs.premium();
    return el('main', { class: 'screen center demodone' }, [
      el('div', { class: 'menu-bg', svg: A.scene('lighthouse', 'cove') }),
      el('div', { class: 'panel' }, [
        el('h1', { text: t('demo.title'), attrs: { 'data-focus': '' } }),
        icon(A.nimbo({ mood: 'happy', hat: equippedHat() || 'captain', cls: 'big fly' }), 'nimbo-wrap'),
        el('p', { text: t('demo.body', { a: freeLevels().filter(function (l) { return isDone(l.id); }).length, stars: starsOf(freeLevels()) }) }),
        MP.entitlements.isTestMode() ? el('p', { class: 'notice', text: t('demo.testAll') }) : null,
        el('p', { class: 'lead', text: t('demo.more') }),
        el('div', { class: 'btnrow wrap' }, prem.map(function (pk) { return btn('ghost small', tx(pk.name), function () { go('premium', { id: pk.id }); }); })),
        btn('primary big', t('demo.replay'), function () { go('map'); }),
        btn('ghost', t('menu.parents'), function () { go('parents'); })
      ])
    ]);
  };

  /* ---------------- boot ---------------- */
  MP.topicsInUse = function () {
    var o = {}; MP.levels.all().forEach(function (l) { o[l.topic] = true; }); return o;
  };

  MP.app = {
    go: go, rerender: rerender, screens: SCREENS,
    /** Returns a Promise: waits for the entitlement check and any owned pack files, then shows the first screen. */
    init: function () {
      rootEl = document.getElementById('app');
      var save = S.load();
      if (MP.config.devUnlockPremium) MP.entitlements.useDevUnlock();   // TESTING ONLY, see config.js
      function show() {
        if (!MP.levels.all().length) throw new Error('No levels loaded');
        applySettings();
        var boot = document.getElementById('boot'); if (boot) boot.parentNode.removeChild(boot);
        go(save.introDone ? 'menu' : 'intro');
      }
      return MP.entitlements.refresh().then(function () { return MP.entitlements.loadOwnedPacks(); }).then(show);
    },
    applySettings: applySettings
  };
})();
