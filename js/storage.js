/*
 * storage.js — local save data (prototype: browser localStorage only).
 *
 * Safety rules implemented here:
 *  - Missing, corrupt, hand-edited or newer-version data never crashes the game: it is sanitised
 *    field by field and anything unusable falls back to defaults.
 *  - If localStorage is blocked (private mode, strict settings) we keep progress in memory.
 *  - Nothing here is a security boundary. Players can edit their own save. Never use it to
 *    prove a purchase (see docs/ARCHITECTURE.md).
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  var SCHEMA = 1;
  var ID_RE = /^[a-z0-9_\-]{1,48}$/;

  function defaults() {
    return {
      v: SCHEMA,
      lang: null,            // null = not chosen yet (first run)
      sound: true,
      music: true,           // background music on/off
      musicVol: 60,          // 0..100
      theme: null,           // null = follow the device; 'light' | 'dark'
      haptics: true,         // short phone vibrations on answers and rewards (Android phones)
      chests: {},            // islandId -> true once its treasure chest was opened
      motion: null,          // null = follow the device's "reduce motion" setting; 'reduce' | 'full'
      textScale: 1,          // 1 | 1.15 | 1.3
      band: 1,               // 0 Explorer, 1 Adventurer, 2 Master Explorer (starting difficulty)
      introDone: false,
      tutorialDone: false,
      coins: 0,
      levels: {},            // id -> {done, stars, plays, lastPuzzle, hints, wrong}
      topics: {},            // topic -> {ok, bad, hints, adj, clean, review}
      struggles: 0,          // consecutive "struggle" runs (drives the confidence booster)
      collection: [],        // collectible ids
      pals: {},              // critterId -> {bond 0..5, fed, played}
      buddy: null,           // critterId shown next to the player on the map
      history: [],           // last 40 finished runs: {id, stars, wrong, hints, day}
      wardrobe: { owned: [], equipped: null },
      name: '',              // player name (profiles)
      avatar: 'nimbo',       // avatar id: 'nimbo' or a critter-look name
      closet: [],            // pal accessories found or earned (ids)
      streak: { day: 0, last: null, best: 0, weeks: 0, total: 0, run: 0 },
      freezes: 0,            // streak freezes (cover a missed day), at most 2
      boostUntil: 0,         // ms timestamp until which level coins are doubled
      goal: { day: null, n: 0, paid: false },   // today's daily goal progress   // daily login streak
      online: { on: false, id: null, token: null, code: null },   // optional online friends (see js/friends.js)
      seenVersion: ''        // last app version whose "what's new" the player has seen
    };
  }

  var MAX_PROFILES = 6;
  function cleanName(x) {
    return String(x == null ? '' : x).replace(/[<>&"\u0000-\u001f\u007f]/g, '').replace(/\s+/g, ' ').trim().slice(0, 14);
  }
  function cleanNick(x) { return cleanName(x).slice(0, 12); }

  function int(n, lo, hi, dflt) {
    n = Number(n);
    if (!isFinite(n)) return dflt;
    return Math.min(hi, Math.max(lo, Math.round(n)));
  }

  /** Turn anything (including garbage) into a valid save object. Pure function — unit tested. */
  function sanitize(raw) {
    var d = defaults();
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) return d;

    if (raw.lang === 'en' || raw.lang === 'ms') d.lang = raw.lang;
    if (typeof raw.sound === 'boolean') d.sound = raw.sound;
    if (typeof raw.music === 'boolean') d.music = raw.music;
    d.musicVol = int(raw.musicVol, 0, 100, 60);
    d.freezes = int(raw.freezes, 0, 2, 0);
    d.boostUntil = (typeof raw.boostUntil === 'number' && isFinite(raw.boostUntil) && raw.boostUntil > 0 && raw.boostUntil < 4e12) ? Math.floor(raw.boostUntil) : 0;
    if (raw.goal && typeof raw.goal === 'object') d.goal = { day: (typeof raw.goal.day === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(raw.goal.day)) ? raw.goal.day : null, n: int(raw.goal.n, 0, 1000, 0), paid: raw.goal.paid === true };
    if (raw.theme === 'light' || raw.theme === 'dark') d.theme = raw.theme;
    if (typeof raw.haptics === 'boolean') d.haptics = raw.haptics;
    if (raw.chests && typeof raw.chests === 'object' && !Array.isArray(raw.chests)) Object.keys(raw.chests).slice(0, 200).forEach(function (k) { if (/^[a-z0-9-]{1,40}$/.test(k) && raw.chests[k] === true) d.chests[k] = true; });
    if (raw.motion === 'reduce' || raw.motion === 'full') d.motion = raw.motion;
    if (raw.textScale === 1 || raw.textScale === 1.15 || raw.textScale === 1.3) d.textScale = raw.textScale;
    d.band = int(raw.band, 0, 2, 1);
    d.introDone = raw.introDone === true;
    d.tutorialDone = raw.tutorialDone === true;
    d.coins = int(raw.coins, 0, 1000000, 0);
    d.struggles = int(raw.struggles, 0, 99, 0);
    if (raw.streak && typeof raw.streak === 'object') {
      var sk = raw.streak;
      d.streak = { day: int(sk.day, 0, 7, 0), last: (typeof sk.last === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(sk.last)) ? sk.last : null,
        best: int(sk.best, 0, 7, 0), weeks: int(sk.weeks, 0, 9999, 0), total: int(sk.total, 0, 99999, 0) };
      d.streak.run = int(sk.run, 0, 100000, 0);
      if (!d.streak.last) { d.streak.day = 0; d.streak.run = 0; }
      if (d.streak.run < d.streak.day) d.streak.run = d.streak.day;
    }
    if (raw.online && raw.online.on === true && /^[0-9a-f-]{36}$/.test(raw.online.id) && /^[0-9a-f]{20,80}$/.test(raw.online.token) && /^[A-Z0-9]{6}$/.test(raw.online.code)) d.online = { on: true, id: raw.online.id, token: raw.online.token, code: raw.online.code };
    if (typeof raw.seenVersion === 'string' && /^[0-9a-z.\-]{1,20}$/i.test(raw.seenVersion)) d.seenVersion = raw.seenVersion;

    if (raw.levels && typeof raw.levels === 'object') {
      Object.keys(raw.levels).slice(0, 300).forEach(function (id) {
        if (!ID_RE.test(id)) return;
        var l = raw.levels[id];
        if (!l || typeof l !== 'object') return;
        d.levels[id] = {
          done: l.done === true,
          stars: int(l.stars, 0, 3, 0),
          plays: int(l.plays, 0, 100000, 0),
          lastPuzzle: (typeof l.lastPuzzle === 'string' && ID_RE.test(l.lastPuzzle)) ? l.lastPuzzle : null,
          hints: int(l.hints, 0, 100000, 0),
          wrong: int(l.wrong, 0, 100000, 0)
        };
        if (!d.levels[id].done) d.levels[id].stars = 0;
      });
    }

    if (raw.topics && typeof raw.topics === 'object') {
      Object.keys(raw.topics).slice(0, 100).forEach(function (k) {
        if (!ID_RE.test(k)) return;
        var t = raw.topics[k];
        if (!t || typeof t !== 'object') return;
        d.topics[k] = {
          ok: int(t.ok, 0, 100000, 0), bad: int(t.bad, 0, 100000, 0), hints: int(t.hints, 0, 100000, 0),
          adj: int(t.adj, -1, 1, 0), clean: int(t.clean, 0, 10, 0), review: t.review === true
        };
      });
    }

    if (Array.isArray(raw.collection)) {
      raw.collection.slice(0, 200).forEach(function (id) {
        if (typeof id === 'string' && ID_RE.test(id) && d.collection.indexOf(id) === -1) d.collection.push(id);
      });
    }

    if (raw.pals && typeof raw.pals === 'object') {
      Object.keys(raw.pals).slice(0, 100).forEach(function (k) {
        var p = raw.pals[k];
        if (!ID_RE.test(k) || !p || typeof p !== 'object') return;
        d.pals[k] = { bond: int(p.bond, 0, 5, 0), fed: int(p.fed, 0, 100000, 0), played: int(p.played, 0, 100000, 0) };
        d.pals[k]._acc = p.acc; d.pals[k].tint = (p.tint === null || p.tint === undefined || p.tint === '') ? null : int(p.tint, 0, 11, 0);
        d.pals[k].nick = cleanNick(p.nick);
      });
    }
    if (Array.isArray(raw.closet)) {
      raw.closet.slice(0, 40).forEach(function (id) {
        if (typeof id === 'string' && ID_RE.test(id) && d.closet.indexOf(id) === -1) d.closet.push(id);
      });
    }
    // a pal may only wear something that is bought ('none' = bare, null = its natural look)
    Object.keys(d.pals).forEach(function (k) {
      var a = d.pals[k]._acc; delete d.pals[k]._acc;
      d.pals[k].acc = (a === 'none' || (typeof a === 'string' && d.closet.indexOf(a) !== -1)) ? a : null;
    });
    d.name = cleanName(raw.name);
    d.avatar = (typeof raw.avatar === 'string' && ID_RE.test(raw.avatar)) ? raw.avatar : 'nimbo';
    if (typeof raw.buddy === 'string' && ID_RE.test(raw.buddy) && d.collection.indexOf(raw.buddy) !== -1) d.buddy = raw.buddy;
    if (Array.isArray(raw.history)) {
      raw.history.slice(-40).forEach(function (h) {
        if (!h || typeof h !== 'object' || typeof h.id !== 'string' || !ID_RE.test(h.id)) return;
        d.history.push({ id: h.id, stars: int(h.stars, 0, 3, 0), wrong: int(h.wrong, 0, 999, 0), hints: int(h.hints, 0, 999, 0), day: int(h.day, 20200101, 29991231, 20200101) });
      });
    }

    if (raw.wardrobe && typeof raw.wardrobe === 'object') {
      if (Array.isArray(raw.wardrobe.owned)) {
        raw.wardrobe.owned.slice(0, 50).forEach(function (id) {
          if (typeof id === 'string' && ID_RE.test(id) && d.wardrobe.owned.indexOf(id) === -1) d.wardrobe.owned.push(id);
        });
      }
      var eq = raw.wardrobe.equipped;
      if (typeof eq === 'string' && d.wardrobe.owned.indexOf(eq) !== -1) d.wardrobe.equipped = eq;
    }
    return d;
  }

  var mem = {};              // used for any key if localStorage is unavailable
  var state = defaults();
  var persistent = false;
  var index = { active: 'p1', list: [{ id: 'p1', name: '', avatar: 'nimbo' }] };

  function ls() {
    try {
      var s = window.localStorage;
      var k = '__mp_test__';
      s.setItem(k, '1'); s.removeItem(k);
      return s;
    } catch (e) { return null; }
  }
  function rd(key) {
    var s = (typeof window !== 'undefined') ? ls() : null;
    if (s) { try { return s.getItem(key); } catch (e) { return null; } }
    return Object.prototype.hasOwnProperty.call(mem, key) ? mem[key] : null;
  }
  function wr(key, txt) {
    var s = (typeof window !== 'undefined') ? ls() : null;
    if (s) { try { s.setItem(key, txt); persistent = true; return true; } catch (e) { persistent = false; } }
    mem[key] = txt; return false;
  }
  function rm(key) {
    var s = (typeof window !== 'undefined') ? ls() : null;
    if (s) { try { s.removeItem(key); } catch (e) { /* ignore */ } }
    delete mem[key];
  }
  function baseKey() { return MP.config.storageKey; }
  function idxKey() { return baseKey() + '.profiles'; }
  function dataKey(id) { return baseKey() + '.p.' + id; }

  function parseSave(txt, key) {
    var raw = null;
    if (txt) {
      try { raw = JSON.parse(txt); }
      catch (e) {
        // Keep the unreadable text once so support can look at it, then start clean.
        wr(key + '.corrupt', String(txt).slice(0, 20000));
        raw = null;
      }
    }
    return sanitize(raw);
  }
  function cleanIndex(raw) {
    var out = { active: null, list: [] }, seen = {};
    if (raw && typeof raw === 'object' && Array.isArray(raw.list)) {
      raw.list.slice(0, MAX_PROFILES).forEach(function (e) {
        if (!e || typeof e.id !== 'string' || !ID_RE.test(e.id) || seen[e.id]) return;
        seen[e.id] = 1;
        out.list.push({ id: e.id, name: cleanName(e.name), avatar: (typeof e.avatar === 'string' && ID_RE.test(e.avatar)) ? e.avatar : 'nimbo' });
      });
      if (typeof raw.active === 'string' && seen[raw.active]) out.active = raw.active;
    }
    if (out.list.length && !out.active) out.active = out.list[0].id;
    return out;
  }
  function saveIndex() { return wr(idxKey(), JSON.stringify(index)); }
  function entry(id) { for (var i = 0; i < index.list.length; i++) if (index.list[i].id === id) return index.list[i]; return null; }
  function newId() { var n = 1; while (entry('p' + n)) n++; return 'p' + n; }

  var store = {
    SCHEMA: SCHEMA,
    MAX_PROFILES: MAX_PROFILES,
    sanitize: sanitize,
    defaults: defaults,
    cleanName: cleanName,

    /** Load the profile index and the active profile. Migrates a pre-profile save into player 1. */
    load: function () {
      var idxRaw = null, txt;
      persistent = !!((typeof window !== 'undefined') && ls());
      try { idxRaw = JSON.parse(rd(idxKey())); } catch (e) { idxRaw = null; }
      index = cleanIndex(idxRaw);
      if (!index.list.length) {
        index = { active: 'p1', list: [{ id: 'p1', name: '', avatar: 'nimbo' }] };
        var legacy = rd(baseKey());                       // save from before profiles existed
        if (legacy) { state = parseSave(legacy, baseKey()); }
        else state = defaults();
        index.list[0].name = state.name; index.list[0].avatar = state.avatar;
        wr(dataKey('p1'), JSON.stringify(state)); saveIndex();
        return state;
      }
      state = parseSave(rd(dataKey(index.active)), dataKey(index.active));
      var e = entry(index.active); if (e) { state.name = state.name || e.name; state.avatar = state.avatar === 'nimbo' ? e.avatar : state.avatar; }
      return state;
    },

    get: function () { return state; },
    isPersistent: function () { return persistent; },

    save: function () {
      var txt;
      try { txt = JSON.stringify(state); } catch (e) { return false; }
      var ok = wr(dataKey(index.active), txt);
      var e = entry(index.active);
      if (e && (e.name !== state.name || e.avatar !== state.avatar)) { e.name = state.name; e.avatar = state.avatar; saveIndex(); }
      return ok;
    },

    /** Change state with a function, then save. Keeps all callers going through one door. */
    update: function (fn) { fn(state); store.save(); return state; },

    /** Wipes progress but keeps language/sound/accessibility choices and who the player is. */
    resetProgress: function () {
      var keep = { lang: state.lang, sound: state.sound, music: state.music, musicVol: state.musicVol, motion: state.motion, theme: state.theme, haptics: state.haptics, textScale: state.textScale, name: state.name, avatar: state.avatar, seenVersion: state.seenVersion };
      state = defaults();
      for (var k in keep) state[k] = keep[k];
      state.introDone = true;      // don't replay the first-run flow after a reset
      store.save();
      return state;
    },

    profiles: {
      activeId: function () { return index.active; },
      count: function () { return index.list.length; },
      canAdd: function () { return index.list.length < MAX_PROFILES; },
      /** [{id, name, avatar, active, stars, levels}] — progress summary read from each profile's own save. */
      list: function () {
        return index.list.map(function (e) {
          var sv = e.id === index.active ? state : parseSave(rd(dataKey(e.id)), dataKey(e.id)), st = 0, dn = 0;
          Object.keys(sv.levels).forEach(function (k) { st += sv.levels[k].stars; if (sv.levels[k].done) dn++; });
          return { id: e.id, name: e.name, avatar: e.avatar, active: e.id === index.active, stars: st, levels: dn };
        });
      },
      /** Add a player and switch to them. Returns the new id, or null when full. */
      create: function (name, avatar, from) {
        if (index.list.length >= MAX_PROFILES) return null;
        store.save();
        var id = newId(), d = from ? sanitize(from) : defaults();
        if (!from) { d.lang = state.lang; d.sound = state.sound; d.music = state.music; d.musicVol = state.musicVol; d.motion = state.motion; d.theme = state.theme; d.haptics = state.haptics; d.textScale = state.textScale; d.introDone = true; }
        d.name = cleanName(name) || d.name;
        d.avatar = (typeof avatar === 'string' && ID_RE.test(avatar)) ? avatar : (d.avatar || 'nimbo');
        index.list.push({ id: id, name: d.name, avatar: d.avatar });
        wr(dataKey(id), JSON.stringify(d));
        index.active = id; saveIndex();
        state = d;
        return id;
      },
      switchTo: function (id) {
        if (!entry(id) || id === index.active) return false;
        store.save();
        index.active = id; saveIndex();
        state = parseSave(rd(dataKey(id)), dataKey(id));
        return true;
      },
      /** Delete a player and their progress. The last remaining player cannot be deleted. */
      remove: function (id) {
        if (!entry(id) || index.list.length <= 1) return false;
        index.list = index.list.filter(function (e) { return e.id !== id; });
        rm(dataKey(id));
        if (index.active === id) { index.active = index.list[0].id; state = parseSave(rd(dataKey(index.active)), dataKey(index.active)); }
        saveIndex();
        return true;
      },
      /** Backup text for the active player (a small JSON file the family can keep). */
      exportActive: function () {
        store.save();
        var copy = JSON.parse(JSON.stringify(state)); copy.online = { on: false, id: null, token: null, code: null };   // a backup must never copy an online identity
        return JSON.stringify({ mathipelago: 1, name: state.name, avatar: state.avatar, save: copy });
      },
      /** Restore a backup as a NEW player (never overwrites anyone). Returns id, or 'bad' / 'full'. */
      importText: function (txt) {
        var o;
        try { o = JSON.parse(txt); } catch (e) { return 'bad'; }
        if (!o || typeof o !== 'object' || o.mathipelago !== 1 || !o.save || typeof o.save !== 'object') return 'bad';
        if (index.list.length >= MAX_PROFILES) return 'full';
        var id = store.profiles.create(o.name || (o.save && o.save.name), o.avatar || (o.save && o.save.avatar), o.save);
        return id || 'full';
      }
    }
  };

  MP.store = store;
})();
