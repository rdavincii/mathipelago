/*
 * friends.js — OPTIONAL online friends. This is the ONLY file that talks to the network.
 * Off by default: nothing is sent until a grown-up switches "Online friends" on in the Friends screen.
 * Only a first name/nickname (max 14 chars), avatar id, star and level counts and the buddy pal's look are shared. No chat, no email, no location.
 * The server (Supabase, see docs/friends-setup.sql) is reached through nine RPC functions with a random per-player token, not a login.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  function cfg() { return MP.config && MP.config.friends && MP.config.friends.url && MP.config.friends.key ? MP.config.friends : null; }
  function me() { var s = MP.store.get(); return s.online && s.online.on ? s.online : null; }
  function newToken() {
    var a = new Uint8Array(24); (window.crypto || {}).getRandomValues ? crypto.getRandomValues(a) : a.forEach(function (_, i) { a[i] = Math.floor(Math.random() * 256); });
    return Array.prototype.map.call(a, function (b) { return (b < 16 ? '0' : '') + b.toString(16); }).join('');
  }
  /** POST one RPC. Resolves {ok, data}; never throws, so the game keeps working offline. */
  function rpc(fn, body) {
    var c = cfg(); if (!c) return Promise.resolve({ ok: false, why: 'off' });
    return fetch(c.url + '/rest/v1/rpc/' + fn, { method: 'POST', headers: { 'Content-Type': 'application/json', apikey: c.key, Authorization: 'Bearer ' + c.key }, body: JSON.stringify(body) })
      .then(function (r) { return r.ok ? r.json().then(function (d) { return { ok: true, data: d }; }) : { ok: false, why: 'server' }; })
      .catch(function () { return { ok: false, why: 'offline' }; });
  }
  function auth(extra) { var o = me(); var b = { p_id: o.id, p_secret: o.token }; for (var k in extra) b[k] = extra[k]; return b; }

  function palLook() {
    var s = MP.store.get(), id = s.buddy; if (!id) return null;
    var lv = MP.levels.all().filter(function (l) { return l.critter.id === id; })[0]; if (!lv) return null;
    var r = s.pals[id] || {};
    return { look: lv.critter.look, acc: r.acc === undefined ? null : r.acc, tint: r.tint === undefined ? null : r.tint, nick: r.nick || '' };
  }
  function stats() {
    var s = MP.store.get(), st = 0, dn = 0;
    Object.keys(s.levels).forEach(function (k) { st += s.levels[k].stars; if (s.levels[k].done) dn++; });
    return { stars: st, levels: dn };
  }

  MP.friends = {
    available: function () { return !!cfg(); },
    isOn: function () { return !!me() && !!cfg(); },
    /** Grown-up switch ON: registers this player and stores the id + token in this player's save. */
    turnOn: function () {
      var s = MP.store.get(), tok = newToken();
      return rpc('mp_join', { p_secret: tok, p_name: s.name, p_avatar: s.avatar }).then(function (r) {
        if (!r.ok || !r.data || !r.data.id) return { ok: false, why: r.why };
        MP.store.update(function (v) { v.online = { on: true, id: r.data.id, token: tok, code: r.data.code }; });
        return MP.friends.sync().then(function () { return { ok: true }; });
      });
    },
    /** Switch OFF: forget locally. (Deleting the server copy needs the delete function; see docs.) */
    turnOff: function () { MP.store.update(function (v) { v.online = { on: false, id: null, token: null, code: null }; }); },
    code: function () { var o = me(); return o ? o.code : null; },
    sync: function () { var s = MP.store.get(), t = stats(); return me() ? rpc('mp_sync', auth({ p_name: s.name, p_avatar: s.avatar, p_stars: t.stars, p_levels: t.levels, p_pal: palLook() })) : Promise.resolve({ ok: false }); },
    list: function () { return me() ? rpc('mp_friends', auth({})) : Promise.resolve({ ok: false }); },
    add: function (code) { return rpc('mp_add', auth({ p_code: String(code || '').toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 6) })); },
    accept: function (id) { return rpc('mp_respond', auth({ p_friend: id, p_accept: true })); },
    cheer: function (id) { return rpc('mp_cheer', auth({ p_friend: id })); },
    /** Cheers received since last time; the screen turns them into coins. */
    collect: function () { return rpc('mp_collect', auth({})); }
  };
})();
