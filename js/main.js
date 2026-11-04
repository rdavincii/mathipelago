/* main.js — starts the game and shows a friendly bilingual error if anything fails to load. */
(function () {
  'use strict';
  function fail(err) {
    if (window.console) console.error(err);
    var boot = document.getElementById('boot');
    if (!boot) { boot = document.createElement('div'); boot.id = 'boot'; boot.className = 'boot'; document.body.appendChild(boot); }
    boot.textContent = '';
    var box = document.createElement('div');
    var p = document.createElement('p'); p.textContent = 'Sorry, the game could not start. / Maaf, permainan tidak dapat dimulakan.';
    var b = document.createElement('button'); b.className = 'btn primary'; b.type = 'button'; b.textContent = 'Reload / Muat semula';
    b.addEventListener('click', function () { location.reload(); });
    box.appendChild(p); box.appendChild(b); boot.appendChild(box);
  }
  window.addEventListener('error', function (e) { if (!window.MP || !window.MP.app || !document.getElementById('app').firstChild) fail(e.error || e.message); });
  function start() { try { Promise.resolve(window.MP.app.init()).catch(fail); } catch (e) { fail(e); } }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
