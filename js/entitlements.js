/*
 * entitlements.js — the ONLY place the game asks "does this player own this pack?".
 *
 * Prototype reality (be honest about it):
 *   - There is no payment code, no accounts and no server in this build.
 *   - The only provider is FreeOnlyProvider: the free demo pack is always available,
 *     every premium pack is locked, and checkout is "not available".
 *   - Premium level data is NOT shipped in the browser bundle at all, so there is nothing to
 *     "unlock" client-side and nothing to steal. A localStorage flag is never used as proof of purchase.
 *
 * Production plan (see docs/ARCHITECTURE.md): implement a `ServerProvider` with the same three
 * methods. `fetchOwned()` calls YOUR backend (cookie/session or signed token), the backend checks the
 * payment provider's records, and `loadPackContent()` downloads premium level files from a URL that the
 * backend only serves to entitled users. The game engine does not change.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  /** Interface every provider must implement:
   *    id: string
   *    fetchOwned():           Promise<string[]>   pack ids the player is entitled to
   *    startCheckout(packId):  Promise<{ok:boolean, reason?:string, url?:string}>
   */
  var FreeOnlyProvider = {
    id: 'free-only',
    fetchOwned: function () { return Promise.resolve([]); },
    startCheckout: function () {
      var url = MP.config && MP.config.checkoutPageUrl;
      if (url) return Promise.resolve({ ok: true, url: url });   // just a link to a normal web page
      return Promise.resolve({ ok: false, reason: 'unavailable' });
    }
  };

  /**
   * TEST-ONLY provider. Grants every premium pack that has a test file in /packs so the premium
   * levels can be tried. It is switched on by MP.config.devUnlockPremium and is NOT a purchase and
   * NOT secure. Never enable it on a public site.
   */
  var DevUnlockProvider = {
    id: 'dev-unlock',
    fetchOwned: function () {
      return Promise.resolve(MP.packs.premium().filter(function (p) { return p.testFile; }).map(function (p) { return p.id; }));
    },
    startCheckout: FreeOnlyProvider.startCheckout
  };

  var owned = [];
  var provider = FreeOnlyProvider;
  var loaded = {};

  MP.entitlements = {
    setProvider: function (p) { provider = p; },
    providerId: function () { return provider.id; },

    refresh: function () {
      return provider.fetchOwned().then(function (ids) {
        owned = Array.isArray(ids) ? ids.filter(function (x) { return typeof x === 'string'; }) : [];
        return owned.slice();
      }, function () { return owned.slice(); });
    },

    /** Free packs are always available; paid packs only if the provider said so. */
    hasPack: function (packId) {
      var pack = MP.packs && MP.packs.byId(packId);
      if (!pack) return false;
      return pack.free === true || owned.indexOf(packId) !== -1;
    },

    startCheckout: function (packId) { return provider.startCheckout(packId); },
    useDevUnlock: function () { provider = DevUnlockProvider; },
    isTestMode: function () { return provider === DevUnlockProvider; },

    /**
     * Download the level file of every pack the provider says is owned (packs/<id>.js) and run it.
     * The file registers its levels. Packs that are not owned are never requested.
     */
    loadOwnedPacks: function () {
      var jobs = owned.filter(function (id) { return !loaded[id]; }).map(function (id) {
        return new Promise(function (resolve) {
          var s = document.createElement('script');
          s.src = 'packs/' + id + '.js';
          s.onload = function () { loaded[id] = true; resolve(true); };
          s.onerror = function () { resolve(false); };    // a missing file must never stop the game
          document.head.appendChild(s);
        });
      });
      return Promise.all(jobs);
    },
    isLoaded: function (id) { return !!loaded[id]; }
  };
})();
