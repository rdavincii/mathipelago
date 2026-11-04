/*
 * levels/registry.js — the central place where levels and islands are registered.
 *
 * LEVEL DATA FORMAT (documented in docs/CONTENT-GUIDE.md)
 * -------------------------------------------------------
 * MP.levels.register({
 *   id:      'm1-1',                 unique, lowercase letters/digits/-/_
 *   pack:    'free-demo',            which content pack owns it (see js/packs.js)
 *   island:  'meadow',               one of MP.islands ids
 *   order:   1,                      position inside the whole pack (unlock order)
 *   topic:   'number-sense',         ADAPTATION strand: levels sharing a strand share difficulty memory
 *   skill:   'number-line',          fine-grained skill name (key `skill.<skill>` in the locale files)
 *   band:    'explorer',             'explorer' | 'adventurer' | 'master'  (the age band it mostly fits)
 *   scene:   'bridge',               which animated scene to draw (js/art.js)
 *   npc:     'berri',                story character shown in the speech bubble
 *   title / story / learn            {en, ms} text objects
 *   critter: { id, name, blurb, look }   the collectible earned on first completion
 *   tiers:   [ puzzle0, puzzle1, puzzle2 ]   friendly / standard / challenge — all AUTHORED, never generated
 * });
 *
 * PUZZLE FORMAT (each entry of `tiers`)
 *   { id, type, prompt:{en,ms}, hint:{en,ms}, explain:{en,ms}, spec:{...type specific...} }
 * Allowed `type`s are the keys of MP.validators (numberline, balance, pattern, share, tiles, match,
 * placeValue, digitArrange, coins, tank, shapes, chart, steps).
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  var list = [];
  var index = {};

  MP.islands = [
    {
      id: 'meadow', order: 1, npc: 'berri', pack: 'free-demo',
      name: { en: 'Cloudberry Meadows', ms: 'Padang Beri Awan' },
      blurb: { en: 'Floating gardens where numbers grow like berries.', ms: 'Taman terapung tempat nombor tumbuh seperti beri.' }
    },
    {
      id: 'forest', order: 2, npc: 'tock', pack: 'free-demo',
      name: { en: 'Gearwood Forest', ms: 'Hutan Gerigi' },
      blurb: { en: 'A clockwork forest full of gears, lanterns and secret gates.', ms: 'Hutan jentera penuh gerigi, tanglung dan pintu rahsia.' }
    },
    {
      id: 'cove', order: 3, npc: 'pearla', pack: 'free-demo',
      name: { en: 'Glimmer Cove', ms: 'Teluk Berkilau' },
      blurb: { en: 'Shining shores, tide tanks and a lighthouse waiting to glow.', ms: 'Pantai berkilau, tangki air pasang dan sebuah rumah api yang menunggu untuk bersinar.' }
    }
  ];

  MP.levels = {
    register: function (lv) {
      if (index[lv.id]) throw new Error('Duplicate level id ' + lv.id);
      list.push(lv);
      list.sort(function (a, b) { return a.order - b.order; });
      index[lv.id] = lv;
    },
    all: function () { return list.slice(); },
    byId: function (id) { return index[id] || null; },
    byIsland: function (islandId) { return list.filter(function (l) { return l.island === islandId; }); },
    byPack: function (packId) { return list.filter(function (l) { return l.pack === packId; }); },
    next: function (id) {
      var i = list.findIndex(function (l) { return l.id === id; });
      return i >= 0 && i + 1 < list.length ? list[i + 1] : null;
    },
    island: function (id) { return MP.islands.filter(function (i) { return i.id === id; })[0] || null; }
  };
})();
