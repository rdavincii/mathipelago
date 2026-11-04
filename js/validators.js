/*
 * validators.js — pure maths checking. NO DOM, NO randomness, NO text.
 *
 * Every puzzle type has:
 *   MP.validators[type](spec, answer) -> true/false      (what the game uses)
 *   MP.solvers[type](spec)            -> {ok, why}       (what the tests use to prove the puzzle
 *                                                          can actually be solved)
 * Correct answers are always COMPUTED from the puzzle's numbers, never trusted from a typed-in flag.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  /* ---------- helpers ---------- */
  function sum(a) { return a.reduce(function (x, y) { return x + y; }, 0); }
  function eq(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

  function patternSequence(rule) {
    var out = [], i;
    if (rule.kind === 'arith') for (i = 0; i < rule.length; i++) out.push(rule.start + rule.step * i);
    else if (rule.kind === 'geo') for (i = 0; i < rule.length; i++) out.push(rule.start * Math.pow(rule.mult, i));
    else if (rule.kind === 'cycle') for (i = 0; i < rule.length; i++) out.push(rule.items[i % rule.items.length]);
    return out;
  }

  function permutations(arr) {
    if (arr.length <= 1) return [arr.slice()];
    var res = [];
    arr.forEach(function (x, i) {
      var rest = arr.slice(0, i).concat(arr.slice(i + 1));
      permutations(rest).forEach(function (p) { res.push([x].concat(p)); });
    });
    return res;
  }
  function digitsToNumber(d) { return d.reduce(function (n, x) { return n * 10 + x; }, 0); }

  function digitGoal(spec) {
    var best = null;
    permutations(spec.digits).forEach(function (p) {
      if (spec.noLeadingZero && p[0] === 0 && p.length > 1) return;
      var n = digitsToNumber(p);
      if (best === null || (spec.goal === 'smallest' ? n < best : n > best)) best = n;
    });
    return best;
  }

  function placeValueOf(spec, digits) {
    var n = 0;
    for (var i = 0; i < spec.places.length; i++) n += (digits[i] || 0) * spec.places[i];
    return n;
  }

  /* shape facts used by the "shapes" puzzle (computed, not stored) */
  var QUAD_EQUAL = { square: 4, rhombus: 4, rectangle: 2, kite: 2, trapezium: 0 };
  function shapeMatches(predicate, item) {
    if (predicate.indexOf('sides:') === 0) {
      var want = Number(predicate.split(':')[1]);
      var sides = item.k === 'poly' ? item.sides : item.k === 'circle' ? 0 : 4;
      return sides === want;
    }
    if (predicate === 'fourEqualSides') {
      if (item.k === 'rect') return item.w === item.h;
      if (item.k === 'quad') return QUAD_EQUAL[item.type] === 4;
      return false;
    }
    if (predicate.indexOf('area:') === 0) {
      var a = Number(predicate.split(':')[1]);
      return item.k === 'rect' && item.w * item.h === a;
    }
    if (predicate.indexOf('perimeter:') === 0) {
      var p = Number(predicate.split(':')[1]);
      return item.k === 'rect' && 2 * (item.w + item.h) === p;
    }
    return false;
  }

  function chartAnswer(spec) {
    var v = spec.bars.map(function (b) { return b.value; }), a = spec.ask;
    if (a.op === 'diff') return v[a.a] - v[a.b];
    if (a.op === 'sum') return sum(a.of.map(function (i) { return v[i]; }));
    if (a.op === 'mean') return sum(v) / v.length;
    return NaN;
  }

  /* ---------- validators ---------- */
  var V = {
    numberline: function (s, value) { return value === s.target; },

    balance: function (s, idxs) {
      if (!Array.isArray(idxs) || new Set(idxs).size !== idxs.length) return false;
      if (s.count && idxs.length !== s.count) return false;
      var vals = idxs.map(function (i) { return s.tiles[i]; });
      if (vals.some(function (x) { return typeof x !== 'number'; })) return false;
      return sum(vals) === s.target;
    },

    pattern: function (s, option) {
      var seq = patternSequence(s.rule);
      return eq(s.options[option], seq[s.hidden]);
    },

    share: function (s, counts) {
      if (!Array.isArray(counts) || counts.length !== s.baskets) return false;
      if (sum(counts) !== s.items) return false;
      return counts.every(function (c) { return c === counts[0]; });
    },

    tiles: function (s, pair) {
      if (!Array.isArray(pair) || pair.length !== 2) return false;
      if (pair[0] === pair[1] || pair[0] == null || pair[1] == null) return false;
      return s.tiles[pair[0]] * s.tiles[pair[1]] === s.target;
    },

    // match is checked pair-by-pair: left index and right index belong to the same pair id
    match: function (s, leftId, rightId) { return leftId === rightId; },

    placeValue: function (s, digits) { return placeValueOf(s, digits) === s.target; },

    digitArrange: function (s, order) {
      if (!Array.isArray(order) || order.length !== s.digits.length) return false;
      if (!eq(order.slice().sort(), s.digits.slice().sort())) return false;
      return digitsToNumber(order) === digitGoal(s);
    },

    coins: function (s, list) {
      if (!Array.isArray(list)) return false;
      if (s.exactCount && list.length !== s.exactCount) return false;
      return sum(list) === s.target;
    },

    tank: function (s, segs) { return segs * s.d === s.n * s.parts; },

    shapes: function (s, picked) {
      var want = [];
      s.items.forEach(function (it, i) { if (shapeMatches(s.predicate, it)) want.push(i); });
      return eq(want, picked.slice().sort(function (a, b) { return a - b; }));
    },

    chart: function (s, value) { return value === chartAnswer(s); },

    steps: function (s, stepIdx, choiceIdx) { return s.steps[stepIdx].answer === choiceIdx; }
  };

  /* ---------- solvers (used by tests to prove each puzzle is solvable and well-formed) ---------- */
  function ok(why) { return { ok: true, why: why || '' }; }
  function bad(why) { return { ok: false, why: why }; }

  var S = {
    numberline: function (s) {
      if (s.target < s.min || s.target > s.max) return bad('target outside range');
      if ((s.target - s.min) % s.step !== 0) return bad('target not on a tick');
      return ok();
    },
    balance: function (s) {
      var n = s.tiles.length, found = null;
      for (var m = 1; m < (1 << n); m++) {
        var idx = [];
        for (var i = 0; i < n; i++) if (m & (1 << i)) idx.push(i);
        if (V.balance(s, idx)) { found = idx; break; }
      }
      return found ? ok('e.g. tiles ' + found.map(function (i) { return s.tiles[i]; }).join('+')) : bad('no subset sums to target');
    },
    pattern: function (s) {
      var seq = patternSequence(s.rule), right = seq[s.hidden], hits = 0;
      if (s.hidden < 1 || s.hidden >= seq.length) return bad('bad hidden index');
      s.options.forEach(function (o) { if (eq(o, right)) hits++; });
      if (hits !== 1) return bad('correct option must appear exactly once (found ' + hits + ')');
      return ok();
    },
    share: function (s) { return s.items % s.baskets === 0 ? ok() : bad('items not divisible by baskets'); },
    tiles: function (s) {
      for (var i = 0; i < s.tiles.length; i++) for (var j = 0; j < s.tiles.length; j++)
        if (i !== j && V.tiles(s, [i, j])) return ok(s.tiles[i] + '×' + s.tiles[j]);
      return bad('no tile pair multiplies to target');
    },
    match: function (s) {
      var ids = {}, rights = {};
      for (var i = 0; i < s.pairs.length; i++) {
        var p = s.pairs[i];
        if (ids[p.id]) return bad('duplicate pair id');
        ids[p.id] = 1;
        if (rights[p.right]) return bad('two pairs share the same right-hand value');
        rights[p.right] = 1;
      }
      return ok();
    },
    placeValue: function (s) {
      var max = 0; s.places.forEach(function (p) { max += 9 * p; });
      return (s.target >= 0 && s.target <= max) ? ok() : bad('target unreachable');
    },
    digitArrange: function (s) { return digitGoal(s) != null ? ok('goal ' + digitGoal(s)) : bad('no valid arrangement'); },
    coins: function (s) {
      // dynamic programming over (amount, coin count)
      var reach = {}; reach['0|0'] = true;
      var cap = s.exactCount || 40;
      for (var c = 0; c < cap; c++) {
        Object.keys(reach).forEach(function (k) {
          var parts = k.split('|'), a = +parts[0], n = +parts[1];
          if (n !== c) return;
          s.coins.forEach(function (coin) { if (a + coin <= s.target) reach[(a + coin) + '|' + (n + 1)] = true; });
        });
      }
      for (var n = 1; n <= cap; n++) {
        if (reach[s.target + '|' + n] && (!s.exactCount || n === s.exactCount)) return ok(n + ' coins');
      }
      return bad('target cannot be paid with these coins');
    },
    tank: function (s) {
      if ((s.n * s.parts) % s.d !== 0) return bad('fraction does not land on a segment line');
      var segs = (s.n * s.parts) / s.d;
      return (segs > 0 && segs < s.parts) ? ok('segments ' + segs) : bad('segments out of range');
    },
    shapes: function (s) {
      var right = 0; s.items.forEach(function (it) { if (shapeMatches(s.predicate, it)) right++; });
      if (right < 1) return bad('no correct shape');
      if (right === s.items.length) return bad('every shape is correct (no puzzle)');
      return ok(right + ' correct');
    },
    chart: function (s) {
      var a = chartAnswer(s);
      if (!isFinite(a) || a !== Math.floor(a)) return bad('answer is not a whole number: ' + a);
      if (a < 0 || a > 999) return bad('answer out of range');
      return ok('answer ' + a);
    },
    steps: function (s) {
      for (var i = 0; i < s.steps.length; i++) {
        var st = s.steps[i];
        if (st.answer < 0 || st.answer >= st.choices.length) return bad('step ' + i + ' answer index out of range');
        if (new Set(st.choices).size !== st.choices.length) return bad('step ' + i + ' has duplicate choices');
      }
      return ok();
    }
  };

  MP.validators = V;
  MP.solvers = S;
  MP.mathUtil = {
    sum: sum, patternSequence: patternSequence, digitGoal: digitGoal, digitsToNumber: digitsToNumber,
    placeValueOf: placeValueOf, shapeMatches: shapeMatches, chartAnswer: chartAnswer
  };
})();
