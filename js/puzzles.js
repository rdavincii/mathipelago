/*
 * puzzles.js — how each puzzle type LOOKS and how the child INTERACTS with it.
 * Right/wrong is never decided here: every check calls MP.validators (js/validators.js).
 *
 * Every renderer is  R[type](spec, ctx)  where ctx provides:
 *   ctx.host      the element to fill with controls
 *   ctx.svg       the live scene (for ctx.art.setText/setVar)
 *   ctx.scope     MP.util.Scope — register listeners/timers so they are cleaned up
 *   ctx.say(text, kind)   show a feedback line (kind: 'info' | 'good' | 'nudge')
 *   ctx.wrong()   report one wrong try (app counts it, plays a soft sound)
 *   ctx.solved()  report the puzzle solved (app guards against double-claims)
 *   ctx.progress(p)  0..1 reveal progress in the scene (match, steps)
 * Every essential interaction is TAP based (no dragging needed), and every control is a real
 * <button>, so it works with touch, mouse and keyboard.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  var el = MP.util.el, t = MP.t, V = MP.validators, A = MP.art, U = MP.mathUtil;

  function btn(cls, content, onClick, attrs) {
    var b = el('button', { class: cls, attrs: Object.assign({ type: 'button' }, attrs || {}) });
    if (typeof content === 'string') b.textContent = content; else if (content) b.appendChild(content);
    b.addEventListener('click', function (e) { MP.audio.unlock(); onClick(e, b); });
    return b;
  }
  function svgBox(svg, cls) { return el('span', { class: cls || 'ico', svg: svg }); }
  function fmt(n) { return Number(n).toLocaleString('en-US'); }
  function checkBtn(label, onClick) { return btn('btn primary check', label, onClick); }
  function pressed(b, on) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.classList.toggle('sel', !!on); }

  var R = {};

  /* ---------------- number line ---------------- */
  R.numberline = function (s, ctx) {
    var value = s.start;
    var range = el('input', { class: 'nl-range', attrs: { type: 'range', min: s.min, max: s.max, step: s.step, value: value, 'aria-label': t('puz.slider') } });
    var readout = el('output', { class: 'nl-out', text: String(value), attrs: { 'aria-live': 'polite' } });
    var ticks = el('div', { class: 'nl-ticks', attrs: { 'aria-hidden': 'true' } });
    var span = s.max - s.min, i;
    for (i = s.min; i <= s.max; i += s.step) {
      var major = (i - s.min) % s.labelEvery === 0;
      ticks.appendChild(el('span', { class: 'tick' + (major ? ' major' : ''), style: { left: ((i - s.min) / span * 100) + '%' } },
        major ? [el('b', { text: String(i) })] : []));
    }
    function set(v) {
      v = MP.util.clamp(v, s.min, s.max);
      value = v; range.value = String(v); readout.textContent = String(v); MP.audio.play('tap');
    }
    ctx.scope.on(range, 'input', function () { value = Number(range.value); readout.textContent = String(value); });
    var row = el('div', { class: 'nl-row' }, [
      btn('btn round', '−', function () { set(value - s.step); }, { 'aria-label': t('puz.less') }),
      el('div', { class: 'nl-track' }, [range, ticks]),
      btn('btn round', '+', function () { set(value + s.step); }, { 'aria-label': t('puz.more') })
    ]);
    ctx.host.appendChild(el('div', { class: 'puz nl' }, [readout, row,
      checkBtn(t('puz.placePlank'), function () {
        if (V.numberline(s, value)) ctx.solved();
        else { ctx.say(value < s.target ? t('fb.higher') : t('fb.lower'), 'nudge'); ctx.wrong(); }
      })]));
  };

  /* ---------------- balance (add crates to reach a target) ---------------- */
  R.balance = function (s, ctx) {
    var sel = [], btns = [];
    var sumEl = el('div', { class: 'sumline', attrs: { 'aria-live': 'polite' } });
    function sum() { return sel.reduce(function (a, i) { return a + s.tiles[i]; }, 0); }
    function refresh() {
      var sm = sum();
      sumEl.textContent = t('puz.sumLine', { sum: sm, target: s.target });
      A.setText(ctx.svg, 'sum', sm); A.setText(ctx.svg, 'target', s.target);
      var tilt = MP.util.clamp((s.target - sm) / s.target, -1, 1) * 14;
      A.setVar(ctx.svg, 'tilt', tilt.toFixed(1) + 'deg');
      btns.forEach(function (b, i) { pressed(b, sel.indexOf(i) !== -1); });
    }
    var grid = el('div', { class: 'tilegrid' });
    s.tiles.forEach(function (n, i) {
      var b = btn('tile crate', null, function () {
        var k = sel.indexOf(i);
        if (k === -1) sel.push(i); else sel.splice(k, 1);
        MP.audio.play('place'); refresh();
      }, { 'aria-pressed': 'false' });
      b.appendChild(svgBox(A.crateBerries(), 'crate-ico'));
      b.appendChild(el('b', { text: String(n) }));
      btns.push(b); grid.appendChild(b);
    });
    var note = s.count ? el('p', { class: 'note', text: t('puz.pickExactly', { n: s.count }) }) : null;
    ctx.host.appendChild(el('div', { class: 'puz' }, [note, grid, sumEl,
      checkBtn(t('puz.balance'), function () {
        if (V.balance(s, sel)) return ctx.solved();
        var sm = sum();
        if (!sel.length) ctx.say(t('fb.pickSome'), 'nudge');
        else if (s.count && sel.length !== s.count) ctx.say(t('fb.needCount', { n: s.count }), 'nudge');
        else ctx.say(sm < s.target ? t('fb.tooLight') : t('fb.tooHeavy'), 'nudge');
        ctx.wrong();
      })]));
    refresh();
  };

  /* ---------------- pattern ---------------- */
  function patCell(item) {
    if (typeof item === 'string' && item.indexOf(':') > 0) return svgBox(A.shape(item, 46), 'patshape');
    return el('b', { text: String(item) });
  }
  R.pattern = function (s, ctx) {
    var seq = U.patternSequence(s.rule), slot;
    var strip = el('div', { class: 'patstrip', attrs: { 'aria-label': t('puz.patternStrip') } });
    seq.forEach(function (item, i) {
      if (i === s.hidden) { slot = el('div', { class: 'patcell slot', text: '?' }); strip.appendChild(slot); }
      else strip.appendChild(el('div', { class: 'patcell' }, [patCell(item)]));
    });
    var opts = el('div', { class: 'optrow' });
    s.options.forEach(function (o, i) {
      var b = btn('tile opt', patCell(o), function () {
        if (V.pattern(s, i)) {
          slot.textContent = ''; slot.appendChild(patCell(o)); slot.classList.add('ok');
          opts.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
          ctx.solved();
        } else {
          b.disabled = true; b.classList.add('tried'); ctx.say(t('fb.notThat'), 'nudge'); ctx.wrong();
        }
      });
      opts.appendChild(b);
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [strip, opts]));
  };

  /* ---------------- fair sharing ---------------- */
  R.share = function (s, ctx) {
    var counts = []; for (var i = 0; i < s.baskets; i++) counts.push(0);
    var pool = el('div', { class: 'pool', attrs: { 'aria-live': 'polite' } });
    var cols = [];
    function left() { return s.items - U.sum(counts); }
    function refresh() {
      var l = left();
      pool.textContent = '';
      pool.appendChild(el('span', { class: 'poollabel', text: t('puz.pile', { n: l }) }));
      for (var k = 0; k < Math.min(l, 24); k++) pool.appendChild(svgBox(A.berry(), 'berry'));
      cols.forEach(function (c, bi) {
        c.num.textContent = String(counts[bi]);
        c.fill.textContent = '';
        for (var k2 = 0; k2 < counts[bi]; k2++) c.fill.appendChild(svgBox(A.berry(), 'berry sm'));
        c.plus.disabled = l <= 0; c.minus.disabled = counts[bi] <= 0;
      });
    }
    var row = el('div', { class: 'baskets' });
    counts.forEach(function (_, bi) {
      var num = el('b', { class: 'bnum', text: '0' }), fill = el('div', { class: 'bfill' });
      var plus = btn('btn round sm', '+', function () { if (left() > 0) { counts[bi]++; MP.audio.play('place'); refresh(); } }, { 'aria-label': t('puz.addTo', { n: bi + 1 }) });
      var minus = btn('btn round sm', '−', function () { if (counts[bi] > 0) { counts[bi]--; MP.audio.play('tap'); refresh(); } }, { 'aria-label': t('puz.takeFrom', { n: bi + 1 }) });
      cols.push({ num: num, fill: fill, plus: plus, minus: minus });
      row.appendChild(el('div', { class: 'basket' }, [el('span', { class: 'blabel', text: t('puz.basket', { n: bi + 1 }) }), fill, num, el('div', { class: 'bbtns' }, [minus, plus])]));
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [pool, row,
      checkBtn(t('puz.isFair'), function () {
        if (V.share(s, counts)) return ctx.solved();
        ctx.say(left() > 0 ? t('fb.pileLeft') : t('fb.notEqual'), 'nudge'); ctx.wrong();
      })]));
    refresh();
  };

  /* ---------------- multiplication tiles ---------------- */
  R.tiles = function (s, ctx) {
    var sel = [], btns = [], locked = false;
    var eq = el('div', { class: 'equation', attrs: { 'aria-live': 'polite' } });
    function refresh() {
      var a = sel[0] != null ? s.tiles[sel[0]] : '?', b = sel[1] != null ? s.tiles[sel[1]] : '?';
      eq.textContent = a + ' × ' + b + ' = ' + s.target;
      btns.forEach(function (x, i) { pressed(x, sel.indexOf(i) !== -1); });
    }
    var grid = el('div', { class: 'tilegrid' });
    s.tiles.forEach(function (n, i) {
      var b = btn('tile cog', null, function () {
        if (locked) return;
        var k = sel.indexOf(i);
        if (k !== -1) sel.splice(k, 1); else if (sel.length < 2) sel.push(i);
        MP.audio.play('select'); refresh();
        if (sel.length === 2) {
          if (V.tiles(s, sel)) { locked = true; ctx.solved(); }
          else {
            locked = true; ctx.say(t('fb.notProduct', { a: s.tiles[sel[0]], b: s.tiles[sel[1]], p: s.tiles[sel[0]] * s.tiles[sel[1]], target: s.target }), 'nudge'); ctx.wrong();
            ctx.scope.timeout(function () { sel = []; locked = false; refresh(); }, 900);
          }
        }
      }, { 'aria-pressed': 'false' });
      b.appendChild(el('b', { text: String(n) }));
      btns.push(b); grid.appendChild(b);
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [el('p', { class: 'note', text: t('puz.pickTwo') }), grid, eq]));
    refresh();
  };

  /* ---------------- matching pairs ---------------- */
  R.match = function (s, ctx) {
    var selLeft = null, done = {}, count = 0, locked = false;
    var rights = MP.util.shuffle(s.pairs);
    var lb = {}, rb = {};
    function clearSel() { if (selLeft) { pressed(lb[selLeft], false); selLeft = null; } }
    function mark(id) {
      [lb[id], rb[id]].forEach(function (b) { b.disabled = true; b.classList.add('matched'); b.appendChild(el('span', { class: 'tickmark', text: ' ✓', attrs: { 'aria-hidden': 'true' } })); });
    }
    var lcol = el('div', { class: 'col' }), rcol = el('div', { class: 'col' });
    s.pairs.forEach(function (p) {
      lb[p.id] = btn('tile', p.left, function () {
        if (locked || done[p.id]) return;
        clearSel(); selLeft = p.id; pressed(lb[p.id], true); MP.audio.play('select');
      }, { 'aria-pressed': 'false' });
      lcol.appendChild(lb[p.id]);
    });
    rights.forEach(function (p) {
      rb[p.id] = btn('tile', p.right, function () {
        if (locked || done[p.id]) return;
        if (!selLeft) { ctx.say(t('fb.tapQuestionFirst'), 'info'); return; }
        if (V.match(s, selLeft, p.id)) {
          var id = selLeft; done[id] = true; count++; clearSel(); mark(id); MP.audio.play('ok');
          ctx.progress(count / s.pairs.length);
          ctx.say(t('fb.pairFound', { n: count, total: s.pairs.length }), 'good');
          if (count === s.pairs.length) ctx.solved();
        } else {
          locked = true; ctx.say(t('fb.notPair'), 'nudge'); ctx.wrong();
          ctx.scope.timeout(function () { clearSel(); locked = false; }, 600);
        }
      });
      rcol.appendChild(rb[p.id]);
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [el('div', { class: 'matchgrid' }, [lcol, rcol])]));
  };

  /* ---------------- place value dials ---------------- */
  var PLACE_KEYS = { 1: 'place.ones', 10: 'place.tens', 100: 'place.hundreds', 1000: 'place.thousands' };
  R.placeValue = function (s, ctx) {
    var digits = s.places.map(function () { return 0; });
    var total = el('div', { class: 'bignum', attrs: { 'aria-live': 'polite' } });
    var cells = [];
    function refresh() {
      total.textContent = fmt(U.placeValueOf(s, digits));
      cells.forEach(function (c, i) { c.textContent = String(digits[i]); });
    }
    var row = el('div', { class: 'dials' });
    s.places.forEach(function (pl, i) {
      var cell = el('b', { class: 'dialnum', text: '0' });
      cells.push(cell);
      row.appendChild(el('div', { class: 'dial' }, [
        el('span', { class: 'dlabel', text: t(PLACE_KEYS[pl]) }),
        btn('btn round', '+', function () { digits[i] = Math.min(9, digits[i] + 1); MP.audio.play('tap'); refresh(); }, { 'aria-label': t('puz.plusPlace', { p: t(PLACE_KEYS[pl]) }) }),
        cell,
        btn('btn round', '−', function () { digits[i] = Math.max(0, digits[i] - 1); MP.audio.play('tap'); refresh(); }, { 'aria-label': t('puz.minusPlace', { p: t(PLACE_KEYS[pl]) }) })
      ]));
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [row, total,
      checkBtn(t('puz.tryCode'), function () {
        if (V.placeValue(s, digits)) return ctx.solved();
        var now = U.placeValueOf(s, digits);
        ctx.say(t('fb.codeIs', { n: fmt(now) }), 'nudge'); ctx.wrong();
      })]));
    refresh();
  };

  /* ---------------- digit arrange ---------------- */
  R.digitArrange = function (s, ctx) {
    var placed = [];        // indices into s.digits, in slot order
    var slots = el('div', { class: 'slots' }), pool = el('div', { class: 'tilegrid' });
    function order() { return placed.map(function (i) { return s.digits[i]; }); }
    function refresh() {
      slots.textContent = '';
      s.digits.forEach(function (_, k) {
        if (k < placed.length) slots.appendChild(btn('tile slot filled', String(s.digits[placed[k]]), function () { placed.splice(k, 1); MP.audio.play('tap'); refresh(); }, { 'aria-label': t('puz.removeDigit', { d: s.digits[placed[k]] }) }));
        else slots.appendChild(el('div', { class: 'tile slot', text: '·' }));
      });
      pool.textContent = '';
      s.digits.forEach(function (d, i) {
        var used = placed.indexOf(i) !== -1;
        var b = btn('tile', String(d), function () { if (placed.length < s.digits.length) { placed.push(i); MP.audio.play('place'); refresh(); } });
        b.disabled = used; pool.appendChild(b);
      });
      check.disabled = placed.length !== s.digits.length;
    }
    var check = checkBtn(t('puz.tryCode'), function () {
      if (V.digitArrange(s, order())) return ctx.solved();
      ctx.say(t('fb.numberIs', { n: fmt(U.digitsToNumber(order())), goal: s.goal === 'smallest' ? t('puz.smallest') : t('puz.largest') }), 'nudge'); ctx.wrong();
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [slots, pool, check]));
    refresh();
  };

  /* ---------------- coins ---------------- */
  R.coins = function (s, ctx) {
    var list = [];
    var purse = el('div', { class: 'purse', attrs: { 'aria-live': 'polite' } });
    var totalEl = el('div', { class: 'sumline' });
    function refresh() {
      purse.textContent = '';
      list.slice().sort(function (a, b) { return b - a; }).forEach(function (c) { purse.appendChild(svgBox(A.coin(c), 'coinico sm')); });
      if (!list.length) purse.appendChild(el('span', { class: 'note', text: t('puz.purseEmpty') }));
      totalEl.textContent = t('puz.paid', { paid: MP.i18n.money(U.sum(list)), target: MP.i18n.money(s.target) }) + (s.exactCount ? ' · ' + t('puz.coinCount', { n: list.length, max: s.exactCount }) : '');
    }
    var wallet = el('div', { class: 'wallet' });
    s.coins.forEach(function (c) {
      wallet.appendChild(btn('tile coinbtn', svgBox(A.coin(c), 'coinico'), function () { list.push(c); MP.audio.play('coin'); refresh(); }, { 'aria-label': t('puz.addCoin', { v: MP.i18n.money(c) }) }));
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [
      s.exactCount ? el('p', { class: 'note', text: t('puz.useExactly', { n: s.exactCount }) }) : null,
      wallet, purse, totalEl,
      el('div', { class: 'btnrow' }, [
        btn('btn ghost', t('puz.undo'), function () { list.pop(); refresh(); }),
        btn('btn ghost', t('puz.clear'), function () { list = []; refresh(); })
      ]),
      checkBtn(t('puz.pay'), function () {
        if (V.coins(s, list)) return ctx.solved();
        var sm = U.sum(list);
        if (!list.length) ctx.say(t('fb.pickSome'), 'nudge');
        else if (sm < s.target) ctx.say(t('fb.needMore', { n: MP.i18n.money(s.target - sm) }), 'nudge');
        else if (sm > s.target) ctx.say(t('fb.tooMuch', { n: MP.i18n.money(sm - s.target) }), 'nudge');
        else ctx.say(t('fb.needCount', { n: s.exactCount }), 'nudge');
        ctx.wrong();
      })]));
    refresh();
  };

  /* ---------------- fraction tank ---------------- */
  R.tank = function (s, ctx) {
    var level = 0, cells = [];
    var lab = el('div', { class: 'sumline', attrs: { 'aria-live': 'polite' } });
    A.setText(ctx.svg, 'frac', s.n + '/' + s.d);
    function refresh() {
      A.setVar(ctx.svg, 'fill', String(level / s.parts));
      lab.textContent = t('puz.partsFilled', { k: level, parts: s.parts });
      cells.forEach(function (c, i) { c.classList.toggle('full', i < level); c.setAttribute('aria-pressed', i < level ? 'true' : 'false'); });
    }
    var gauge = el('div', { class: 'gauge' });
    for (var i = 0; i < s.parts; i++) (function (i) {
      var c = btn('cell', String(i + 1), function () { level = (level === i + 1) ? i : i + 1; MP.audio.play('tap'); refresh(); }, { 'aria-label': t('puz.fillTo', { k: i + 1, parts: s.parts }) });
      cells.push(c); gauge.appendChild(c);
    })(i);
    ctx.host.appendChild(el('div', { class: 'puz' }, [el('p', { class: 'note', text: t('puz.tankNote', { parts: s.parts }) }), gauge, lab,
      checkBtn(t('puz.fill'), function () {
        if (V.tank(s, level)) return ctx.solved();
        ctx.say(level * s.d < s.n * s.parts ? t('fb.moreWater') : t('fb.lessWater'), 'nudge'); ctx.wrong();
      })]));
    refresh();
  };

  /* ---------------- shapes ---------------- */
  R.shapes = function (s, ctx) {
    var sel = [], btns = [];
    var grid = el('div', { class: 'shapegrid' });
    s.items.forEach(function (it, i) {
      var b = btn('tile shapebtn', svgBox(A.puzzleShape(it), 'shapeico'), function () {
        var k = sel.indexOf(i); if (k === -1) sel.push(i); else sel.splice(k, 1);
        MP.audio.play('select'); pressed(b, k === -1);
      }, { 'aria-pressed': 'false', 'aria-label': t('puz.shapeN', { n: i + 1 }) });
      b.appendChild(el('span', { class: 'badge', text: '✓', attrs: { 'aria-hidden': 'true' } }));
      btns.push(b); grid.appendChild(b);
    });
    ctx.host.appendChild(el('div', { class: 'puz' }, [grid,
      checkBtn(t('puz.open'), function () {
        if (V.shapes(s, sel)) return ctx.solved();
        var wrongPick = sel.some(function (i) { return !U.shapeMatches(s.predicate, s.items[i]); });
        ctx.say(!sel.length ? t('fb.pickSome') : wrongPick ? t('fb.extraShape') : t('fb.missingShape'), 'nudge'); ctx.wrong();
      })]));
  };

  /* ---------------- bar chart ---------------- */
  /** Bar label split over up to two lines (by words) so neighbouring labels can never run into each other. */
  function chartLabel(text, cx, y, fs) {
    var w = text.split(/\s+/), lines = [];
    if (w.length <= 2) lines = w; else { var half = Math.ceil(w.length / 2); lines = [w.slice(0, half).join(' '), w.slice(half).join(' ')]; }
    return '<text text-anchor="middle" font-size="' + fs + '" font-weight="800" fill="#2b2350">' + lines.map(function (ln, i) {
      return '<tspan x="' + cx + '" y="' + (y + i * (fs + 2)) + '">' + ln + '</tspan>';
    }).join('') + '</text>';
  }

  R.chart = function (s, ctx) {
    var W = 320, H = 214, L = 34, B = 48, T = 10, n = s.bars.length, bw = Math.min(54, (W - L - 10) / n - 14), slot = (W - L - 16) / n, fs = slot < 52 ? 10.5 : slot < 70 ? 11.5 : 12.5;
    var svg = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + t('puz.chartLabel') + '" focusable="false">', y, i;
    for (y = 0; y <= s.axisMax; y += s.axisStep) {
      var py = H - B - (y / s.axisMax) * (H - B - T);
      svg += '<line x1="' + L + '" x2="' + (W - 6) + '" y1="' + py + '" y2="' + py + '" stroke="#cfc8ea" stroke-width="1"/><text x="' + (L - 6) + '" y="' + (py + 4) + '" text-anchor="end" font-size="11" font-weight="700" fill="#2b2350">' + y + '</text>';
    }
    s.bars.forEach(function (b, k) {
      var h = (b.value / s.axisMax) * (H - B - T), x = L + 10 + k * ((W - L - 16) / n) + ((W - L - 16) / n - bw) / 2;
      svg += '<rect x="' + x + '" y="' + (H - B - h) + '" width="' + bw + '" height="' + h + '" rx="4" fill="' + (A.PAL[b.color] || A.PAL.sky) + '" stroke="' + A.INK + '" stroke-width="2.5"/>' +
        chartLabel(MP.tx(b.label).replace(/[<>&]/g, ''), x + bw / 2, H - B + 14, fs);
    });
    svg += '</svg>';
    var val = 0, out = el('output', { class: 'bignum', text: '0', attrs: { 'aria-live': 'polite' } });
    function add(d) { val = MP.util.clamp(val + d, 0, 999); out.textContent = String(val); MP.audio.play('tap'); }
    ctx.host.appendChild(el('div', { class: 'puz' }, [
      el('div', { class: 'chartbox', svg: svg }),
      el('div', { class: 'stepper' }, [
        btn('btn round', '−10', function () { add(-10); }, { 'aria-label': t('puz.minus10') }), btn('btn round', '−1', function () { add(-1); }, { 'aria-label': t('puz.minus1') }),
        out,
        btn('btn round', '+1', function () { add(1); }, { 'aria-label': t('puz.plus1') }), btn('btn round', '+10', function () { add(10); }, { 'aria-label': t('puz.plus10') })
      ]),
      checkBtn(t('puz.open'), function () {
        if (V.chart(s, val)) return ctx.solved();
        ctx.say(t('fb.checkBars'), 'nudge'); ctx.wrong();
      })]));
  };

  /* ---------------- multi-step ---------------- */
  R.steps = function (s, ctx) {
    var idx = 0, box = el('div', { class: 'puz steps' });
    function show() {
      box.textContent = '';
      var st = s.steps[idx];
      box.appendChild(el('p', { class: 'stephead', text: t('puz.stepOf', { i: idx + 1, n: s.steps.length }) }));
      box.appendChild(el('p', { class: 'stepq', text: MP.tx(st.q) }));
      var opts = el('div', { class: 'optrow wide' });
      st.choices.forEach(function (c, ci) {
        var b = btn('tile opt', c, function () {
          if (V.steps(s, idx, ci)) {
            idx++; MP.audio.play('ok'); ctx.progress(idx / s.steps.length);
            if (idx >= s.steps.length) { opts.querySelectorAll('button').forEach(function (x) { x.disabled = true; }); ctx.solved(); }
            else { ctx.say(t('fb.lampLit', { n: idx }), 'good'); show(); }
          } else { b.disabled = true; b.classList.add('tried'); ctx.say(t('fb.notThat'), 'nudge'); ctx.wrong(); }
        });
        opts.appendChild(b);
      });
      box.appendChild(opts);
    }
    ctx.host.appendChild(box); show();
  };

  MP.puzzles = {
    types: Object.keys(R),
    render: function (type, spec, ctx) {
      if (!R[type]) throw new Error('Unknown puzzle type ' + type);
      R[type](spec, ctx);
    }
  };
})();
