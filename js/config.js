/*
 * config.js — the only file a site owner normally needs to edit.
 * Everything here is PUBLIC (it ships to every visitor's browser).
 * NEVER put API keys, payment secrets or customer data in this file.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  MP.config = {
    gameName: 'Mathipelago',            // provisional name — run a trademark search before launch
    version: '0.8.0',

    // Where the "Exit" button in the main menu sends the player (your website's home / shop page).
    // Hidden automatically when the game is opened straight from a file (file://).
    homeUrl: '/',

    // Contact shown in the parents' area. Replace with a real mailbox before launch.
    supportEmail: 'support@example.com',

    // Optional ONLINE FRIENDS (off unless a grown-up switches it on in the Friends screen). The key is a public, publishable key by design.
    // Leave url '' to remove the feature completely. Set these from your own Supabase project (docs/friends-setup.sql).
    friends: { url: 'https://xkfjenkpvldkwnvpgfth.supabase.co', key: 'sb_publishable_I93OE8ZndCnky2rbJDVO_w_UVspKVrw' },

    // Local storage key. Change it if you ever ship a second game on the same domain.
    storageKey: 'mathipelago.save',

    // Premium purchases: this prototype ships NO payment code and NO premium level data.
    // When you are ready, set this to a normal page on YOUR website that handles checkout.
    // The game only opens it in a new tab and never handles card details. Leave '' to show
    // "purchasing is not available yet" in the premium preview.
    checkoutPageUrl: '',

    // TESTING ONLY. When true, this build loads the premium test packs from /packs so you can try them.
    // It is NOT a purchase and NOT secure (anyone can switch it on). Set to false before you publish
    // publicly; with false the premium islands stay locked and the packs/ folder is never requested.
    // In production, premium access comes from a server (see docs/ARCHITECTURE.md).
    devUnlockPremium: true
  };
})();
