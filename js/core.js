/*
 * core.js — tiny shared helpers (DOM builder, random, cleanup scopes).
 * No game logic lives here.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  var SVGNS = 'http://www.w3.org/2000/svg';

  function clamp(n, lo, hi) { return Math.min(hi, Math.max(lo, n)); }

  // Fisher–Yates; `rng` optional (returns [0,1)) so tests can be deterministic.
  function shuffle(arr, rng) {
    var a = arr.slice(), r = rng || Math.random;
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(r() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /**
   * el('div', {class:'x', text:'hi', attrs:{role:'button'}, on:{click:fn}, style:{...}}, child1, child2)
   * Text is always set with textContent (never innerHTML) so level text can't inject markup.
   * `svg:'<svg…>'` is only for trusted, in-repo art strings.
   */
  function el(tag, props, children) {
    var node = document.createElement(tag);
    props = props || {};
    if (props.class) node.className = props.class;
    if (props.id) node.id = props.id;
    if (props.text != null) node.textContent = props.text;
    if (props.svg) node.innerHTML = props.svg; // trusted art only
    if (props.attrs) for (var k in props.attrs) if (props.attrs[k] != null) node.setAttribute(k, props.attrs[k]);
    if (props.style) for (var s in props.style) node.style.setProperty(s, props.style[s]);
    if (props.on) for (var e in props.on) node.addEventListener(e, props.on[e]);
    var kids = Array.prototype.slice.call(arguments, 2);
    if (Array.isArray(children)) kids = children.concat(kids.slice(1));
    else if (children != null) kids.unshift(children);
    kids.forEach(function (c) {
      if (c == null || c === false) return;
      node.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
    });
    return node;
  }

  /**
   * A Scope remembers listeners/timers so a screen can clean up everything in one call.
   * This is how we avoid leaks when screens are swapped repeatedly.
   */
  function Scope() {
    this.items = [];
    this.disposed = false;
  }
  Scope.prototype.on = function (target, type, fn, opts) {
    target.addEventListener(type, fn, opts);
    this.items.push(function () { target.removeEventListener(type, fn, opts); });
  };
  Scope.prototype.timeout = function (fn, ms) {
    var self = this;
    var id = setTimeout(function () { if (!self.disposed) fn(); }, ms);
    this.items.push(function () { clearTimeout(id); });
    return id;
  };
  Scope.prototype.interval = function (fn, ms) {
    var id = setInterval(fn, ms);
    this.items.push(function () { clearInterval(id); });
    return id;
  };
  Scope.prototype.add = function (cleanup) { this.items.push(cleanup); };
  Scope.prototype.dispose = function () {
    this.disposed = true;
    this.items.forEach(function (f) { try { f(); } catch (e) { /* ignore */ } });
    this.items = [];
  };

  MP.util = { SVGNS: SVGNS, clamp: clamp, shuffle: shuffle, el: el, Scope: Scope };
})();
