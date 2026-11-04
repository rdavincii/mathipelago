/*
 * art.js — ALL artwork is original vector (SVG) drawn in code. No downloaded images, no emoji art.
 * Style rules (so everything looks like one game): ink-navy outlines (INK), rounded shapes,
 * a small shared palette, soft top-light highlights, big friendly eyes.
 *
 * Scenes are "living": elements marked data-at="0.4" appear when progress >= 0.4, and the root's
 * data-state="done" triggers the celebration animations defined in css/style.css.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  var INK = '#2b2350';
  var PAL = { coral: '#ff6f61', sky: '#5fb8ff', sun: '#ffc93c', mint: '#4fd4a4', grape: '#8c6bff', cream: '#fff6e0' };
  var seq = 0;
  function uid() { seq += 1; return 'u' + seq + '_'; }

  function strokeAttr(w) { return ' stroke="' + INK + '" stroke-width="' + (w || 3) + '" stroke-linejoin="round" stroke-linecap="round"'; }

  /* ---------------- gear + star helpers ---------------- */
  function gearPath(cx, cy, r, teeth, depth) {
    var pts = [], n = teeth * 4, i, a, rr;
    depth = depth || r * 0.22;
    for (i = 0; i < n; i++) {
      a = (i / n) * Math.PI * 2;
      rr = (i % 4 === 0 || i % 4 === 1) ? r + depth : r;
      pts.push((cx + Math.cos(a) * rr).toFixed(1) + ' ' + (cy + Math.sin(a) * rr).toFixed(1));
    }
    return 'M' + pts.join(' L') + 'Z';
  }
  function starPath(cx, cy, R, r) {
    var pts = [], i;
    for (i = 0; i < 10; i++) {
      var a = -Math.PI / 2 + (i * Math.PI) / 5, rr = i % 2 ? r : R;
      pts.push((cx + Math.cos(a) * rr).toFixed(1) + ' ' + (cy + Math.sin(a) * rr).toFixed(1));
    }
    return 'M' + pts.join(' L') + 'Z';
  }

  function cloud(x, y, s, dur, delay) {
    return '<g class="drift" style="--dur:' + dur + 's;--delay:-' + delay + 's"><g transform="translate(' + x + ' ' + y + ') scale(' + s + ')">' +
      '<ellipse cx="0" cy="8" rx="30" ry="11" fill="#fff" opacity=".92"/><circle cx="-12" cy="0" r="12" fill="#fff" opacity=".92"/>' +
      '<circle cx="6" cy="-5" r="15" fill="#fff" opacity=".92"/><circle cx="20" cy="3" r="10" fill="#fff" opacity=".92"/></g></g>';
  }

  /* ---------------- backgrounds (viewBox 0 0 400 240) ---------------- */
  var BG = {
    meadow: function (u) {
      return '<defs><linearGradient id="' + u + 'sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#86d8ff"/><stop offset="1" stop-color="#fff2cc"/></linearGradient></defs>' +
        '<rect width="400" height="240" fill="url(#' + u + 'sky)"/>' +
        '<circle class="pulse" cx="334" cy="46" r="34" fill="#ffe27a" opacity=".35"/><circle cx="334" cy="46" r="24" fill="#ffd54a"' + strokeAttr(2.5) + '/>' +
        cloud(70, 38, 1, 40, 0) + cloud(250, 70, 0.8, 55, 20) + cloud(380, 28, 0.7, 48, 8) +
        // distant floating islets with berry bushes
        '<g opacity=".95"><path d="M250 112 q30 -22 62 0 q-8 16 -31 18 q-24 -2 -31 -18z" fill="#9be58f"' + strokeAttr(2) + '/>' +
        '<circle cx="268" cy="100" r="7" fill="#ff7f9d"' + strokeAttr(2) + '/><circle cx="288" cy="97" r="8" fill="#ff7f9d"' + strokeAttr(2) + '/></g>' +
        '<g opacity=".95"><path d="M30 120 q25 -18 50 0 q-6 13 -25 14 q-19 -1 -25 -14z" fill="#9be58f"' + strokeAttr(2) + '/>' +
        '<circle cx="48" cy="109" r="6" fill="#ff7f9d"' + strokeAttr(2) + '/></g>' +
        '<path d="M0 168 Q70 128 150 160 T300 152 T400 146 V240 H0Z" fill="#8be08a"' + strokeAttr(2.5) + '/>' +
        '<path d="M0 196 Q90 170 190 192 T400 184 V240 H0Z" fill="#5fcf72"' + strokeAttr(2.5) + '/>';
    },
    forest: function (u) {
      var trunks = [[26, 30], [352, 36], [150, 22]].map(function (t) {
        return '<g><rect x="' + t[0] + '" y="40" width="' + t[1] + '" height="150" rx="10" fill="#9a6a4a"' + strokeAttr(2.5) + '/>' +
          '<path d="M' + (t[0] + 8) + ' 70 h' + (t[1] - 16) + 'M' + (t[0] + 8) + ' 110 h' + (t[1] - 16) + '" stroke="#7a4f36" stroke-width="3" fill="none" stroke-linecap="round"/>' +
          '<circle cx="' + (t[0] + t[1] / 2) + '" cy="40" r="34" fill="#3fbf9a"' + strokeAttr(2.5) + '/>' +
          '<path d="' + gearPath(t[0] + t[1] / 2, 38, 11, 8, 4) + '" fill="#ffd36b"' + strokeAttr(2) + ' class="gear cw slow"/></g>';
      }).join('');
      return '<defs><linearGradient id="' + u + 'sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fd3c5"/><stop offset="1" stop-color="#f7ecb2"/></linearGradient></defs>' +
        '<rect width="400" height="240" fill="url(#' + u + 'sky)"/>' + trunks +
        '<g class="twinkle"><circle cx="90" cy="90" r="3" fill="#fff5a0"/><circle cx="310" cy="70" r="3" fill="#fff5a0"/><circle cx="230" cy="40" r="2.5" fill="#fff5a0"/><circle cx="120" cy="150" r="2.5" fill="#fff5a0"/></g>' +
        '<path d="M0 172 Q80 146 170 168 T310 162 T400 158 V240 H0Z" fill="#59b975"' + strokeAttr(2.5) + '/>' +
        '<path d="M0 200 Q100 178 200 198 T400 190 V240 H0Z" fill="#3f9b63"' + strokeAttr(2.5) + '/>';
    },
    cave: function (u) {
      var crystals = [[40, 150, '#ff9ff3'], [120, 120, '#9fe0ff'], [300, 130, '#c9a0ff'], [360, 160, '#ff9ff3'], [210, 100, '#7de0c8']].map(function (c, i) {
        return '<g class="twinkle"><path d="M' + c[0] + ' ' + (c[1] + 70) + ' L' + (c[0] - 16) + ' ' + (c[1] + 14) + ' L' + c[0] + ' ' + c[1] + ' L' + (c[0] + 16) + ' ' + (c[1] + 14) + 'Z" fill="' + c[2] + '"' + strokeAttr(2.5) + '/>' +
          '<path d="M' + c[0] + ' ' + c[1] + ' L' + (c[0] - 6) + ' ' + (c[1] + 40) + '" stroke="#fff" stroke-width="3" opacity=".6" stroke-linecap="round"/></g>';
      }).join('');
      return '<defs><linearGradient id="' + u + 'sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b2f7a"/><stop offset="1" stop-color="#8a6fd6"/></linearGradient></defs>' +
        '<rect width="400" height="240" fill="url(#' + u + 'sky)"/>' +
        '<path d="M0 0 H400 V30 q-20 24 -40 0 q-20 34 -50 0 q-24 22 -50 0 q-26 40 -60 0 q-30 26 -60 0 q-24 20 -50 0 q-30 28 -60 0 q-18 12 -30 0Z" fill="#2a2058"' + strokeAttr(2.5) + '/>' +
        crystals +
        '<path d="M0 176 Q80 150 170 172 T320 166 T400 160 V240 H0Z" fill="#6a56b8"' + strokeAttr(2.5) + '/>' +
        '<path d="M0 204 Q100 184 200 202 T400 194 V240 H0Z" fill="#4c3b94"' + strokeAttr(2.5) + '/>';
    },
    garden: function (u) {
      var flowers = [[50, 176], [110, 188], [300, 180], [360, 190]].map(function (f, i) {
        var col = ['#ff7f9d', '#ffd54a', '#ff9f43', '#c9a0ff'][i];
        return '<g><path d="M' + f[0] + ' ' + f[1] + ' v22" stroke="#2f8f4f" stroke-width="4" stroke-linecap="round"/><circle cx="' + f[0] + '" cy="' + f[1] + '" r="9" fill="' + col + '"' + strokeAttr(2.2) + '/><circle cx="' + f[0] + '" cy="' + f[1] + '" r="3.5" fill="#fff6a0"/></g>';
      }).join('');
      return '<defs><linearGradient id="' + u + 'sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ee3ff"/><stop offset="1" stop-color="#ffe9f3"/></linearGradient></defs>' +
        '<rect width="400" height="240" fill="url(#' + u + 'sky)"/>' +
        cloud(80, 34, 1, 44, 2) + cloud(300, 52, 0.8, 58, 22) +
        '<g opacity=".95"><path d="M40 110 q40 -26 80 0 q-10 20 -40 22 q-30 -2 -40 -22z" fill="#b6f09a"' + strokeAttr(2) + '/><path d="M270 96 q40 -26 80 0 q-10 20 -40 22 q-30 -2 -40 -22z" fill="#b6f09a"' + strokeAttr(2) + '/></g>' +
        '<path d="M0 168 Q70 140 150 164 T300 156 T400 150 V240 H0Z" fill="#9be58f"' + strokeAttr(2.5) + '/>' +
        '<path d="M0 198 Q90 176 190 196 T400 188 V240 H0Z" fill="#6fd16a"' + strokeAttr(2.5) + '/>' + flowers;
    },
    cove: function (u) {
      return '<defs><linearGradient id="' + u + 'sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6cc4f5"/><stop offset="1" stop-color="#eaf8ff"/></linearGradient>' +
        '<linearGradient id="' + u + 'sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3cc0ea"/><stop offset="1" stop-color="#1d82c8"/></linearGradient></defs>' +
        '<rect width="400" height="240" fill="url(#' + u + 'sky)"/>' +
        '<circle class="pulse" cx="70" cy="52" r="32" fill="#fff2a8" opacity=".5"/><circle cx="70" cy="52" r="22" fill="#ffe36b"' + strokeAttr(2.5) + '/>' +
        cloud(230, 40, 0.9, 50, 5) + cloud(340, 70, 0.7, 62, 30) +
        '<path d="M250 150 q10 -50 45 -50 q35 0 45 50z" fill="#b9c4dd"' + strokeAttr(2.5) + '/><path d="M278 150 q8 -26 17 -26 q9 0 17 26z" fill="#74c9f7"/>' +
        '<rect y="146" width="400" height="94" fill="url(#' + u + 'sea)"/>' +
        '<g class="waves"><path d="M-40 168 q20 -10 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0" fill="none" stroke="#bff0ff" stroke-width="3" stroke-linecap="round" opacity=".8"/></g>' +
        '<g class="waves rev"><path d="M-40 205 q20 -10 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0" fill="none" stroke="#9fe0ff" stroke-width="3" stroke-linecap="round" opacity=".7"/></g>' +
        '<path d="M0 190 Q60 166 130 186 Q160 196 150 240 H0Z" fill="#ffe3a4"' + strokeAttr(2.5) + '/>';
    }
  };

  /* ---------------- contraptions: the part of the scene that REACTS to the solution ---------------- */
  function burst(cx, cy) {
    var out = '<g class="burst">';
    for (var i = 0; i < 10; i++) {
      var a = (i / 10) * Math.PI * 2, d = 60 + (i % 3) * 14;
      out += '<path class="spark" d="' + starPath(cx, cy, 8, 3.5) + '" fill="' + (i % 2 ? '#ffd54a' : '#fff') + '"' + strokeAttr(1.5) +
        ' style="--dx:' + Math.round(Math.cos(a) * d) + 'px;--dy:' + Math.round(Math.sin(a) * d) + 'px"/>';
    }
    return out + '</g>';
  }

  var STUFF = {
    bridge: function () {
      var planks = '', ghosts = '', i;
      for (i = 0; i < 7; i++) {
        ghosts += '<rect class="off-done" x="' + (113 + i * 25.5) + '" y="148" width="21" height="9" rx="3" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="4 3" opacity=".8"/>';
        planks += '<rect class="reveal" data-at="' + ((i + 1) / 7).toFixed(3) + '" style="--i:' + i + '" x="' + (113 + i * 25.5) + '" y="146" width="21" height="11" rx="3" fill="#d79a5b"' + strokeAttr(2.5) + '/>';
      }
      return '<g><rect x="110" y="200" width="180" height="40" fill="#42b5e8"/><path class="waves" d="M100 206 q10 -8 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0" fill="none" stroke="#bff0ff" stroke-width="3" stroke-linecap="round"/>' +
        '<path d="M0 150 H112 V240 H0Z" fill="#b9885c"' + strokeAttr(3) + '/><path d="M0 150 H112 v-8 q-50 -14 -112 0z" fill="#7fe08f"' + strokeAttr(3) + '/>' +
        '<path d="M288 150 H400 V240 H288Z" fill="#b9885c"' + strokeAttr(3) + '/><path d="M288 150 v-8 q56 -14 112 0 v8z" fill="#7fe08f"' + strokeAttr(3) + '/>' +
        '<rect x="104" y="120" width="10" height="34" rx="3" fill="#8a5a36"' + strokeAttr(2.5) + '/><rect x="286" y="120" width="10" height="34" rx="3" fill="#8a5a36"' + strokeAttr(2.5) + '/>' +
        ghosts + planks + '<path class="reveal" data-at="1" d="M114 126 Q200 150 286 126" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round"/>' + burst(200, 120) + '</g>';
    },
    scale: function () {
      return '<g><path d="M150 232 L200 150 L250 232Z" fill="#c98a52"' + strokeAttr(3) + '/><rect x="194" y="92" width="12" height="62" rx="4" fill="#e7b46f"' + strokeAttr(3) + '/>' +
        '<g class="beam"><rect x="112" y="88" width="176" height="12" rx="6" fill="#ffd36b"' + strokeAttr(3) + '/>' +
        '<g class="pan l"><path d="M120 100 L100 140 M120 100 L140 140" stroke="' + INK + '" stroke-width="2.5" fill="none"/><path d="M92 140 h56 q-4 18 -28 18 q-24 0 -28 -18z" fill="#ff8f6b"' + strokeAttr(3) + '/>' +
        '<text data-text="sum" x="120" y="153" text-anchor="middle" font-size="16" font-weight="900" fill="#fff" stroke="' + INK + '" stroke-width="0.6">0</text></g>' +
        '<g class="pan r"><path d="M280 100 L260 140 M280 100 L300 140" stroke="' + INK + '" stroke-width="2.5" fill="none"/><path d="M252 140 h56 q-4 18 -28 18 q-24 0 -28 -18z" fill="#5fb8ff"' + strokeAttr(3) + '/>' +
        '<text data-text="target" x="280" y="153" text-anchor="middle" font-size="16" font-weight="900" fill="#fff" stroke="' + INK + '" stroke-width="0.6">?</text></g></g>' +
        '<circle cx="200" cy="94" r="8" fill="#fff"' + strokeAttr(3) + '/>' + burst(200, 100) + '</g>';
    },
    windmill: function () {
      var blades = '', i;
      for (i = 0; i < 4; i++) {
        blades += '<g transform="rotate(' + (i * 90) + ' 200 88)" class="' + (i === 3 ? 'reveal fixblade' : '') + '" ' + (i === 3 ? 'data-at="1"' : '') + '>' +
          '<rect x="194" y="30" width="12" height="54" rx="3" fill="#fff6e0"' + strokeAttr(2.5) + '/><rect x="206" y="34" width="22" height="44" rx="3" fill="#ff8f6b"' + strokeAttr(2.5) + '/></g>';
      }
      return '<g><path d="M172 190 L184 96 H216 L228 190Z" fill="#f6d9a0"' + strokeAttr(3) + '/><path d="M186 190 v-26 a14 14 0 0 1 28 0 v26z" fill="#9a6a4a"' + strokeAttr(3) + '/>' +
        '<path d="M178 100 L200 62 L222 100Z" fill="#ff6f61"' + strokeAttr(3) + '/>' +
        '<g class="blades" style="transform-origin:200px 88px">' + blades + '</g><circle cx="200" cy="88" r="8" fill="#ffd36b"' + strokeAttr(3) + '/>' +
        '<circle cx="120" cy="192" r="6" fill="#ff7f9d"' + strokeAttr(2) + '/><circle cx="288" cy="196" r="6" fill="#ffd54a"' + strokeAttr(2) + '/>' + burst(200, 90) + '</g>';
    },
    picnic: function () {
      var kids = [[120, '#ff9eb5'], [200, '#9ad7ff'], [280, '#ffd36b']].map(function (k) {
        return '<g class="bob" style="--delay:-' + (k[0] % 3) + 's"><ellipse cx="' + k[0] + '" cy="170" rx="26" ry="24" fill="' + k[1] + '"' + strokeAttr(3) + '/>' +
          '<circle cx="' + (k[0] - 9) + '" cy="164" r="5" fill="#fff"/><circle cx="' + (k[0] + 9) + '" cy="164" r="5" fill="#fff"/>' +
          '<circle cx="' + (k[0] - 9) + '" cy="165" r="2.4" fill="' + INK + '"/><circle cx="' + (k[0] + 9) + '" cy="165" r="2.4" fill="' + INK + '"/>' +
          '<path class="off-done" d="M' + (k[0] - 6) + ' 178 h12" stroke="' + INK + '" stroke-width="2.5" fill="none" stroke-linecap="round"/>' +
          '<path class="on-done" d="M' + (k[0] - 7) + ' 176 q7 9 14 0" stroke="' + INK + '" stroke-width="2.5" fill="none" stroke-linecap="round"/></g>';
      }).join('');
      return '<g><path d="M60 200 L90 150 H310 L340 200Z" fill="#ff8f8f"' + strokeAttr(3) + '/>' +
        '<path d="M96 160 L84 190 M140 150 L132 200 M190 150 V200 M240 150 L248 200 M290 150 L304 190" stroke="#fff" stroke-width="5" opacity=".55"/>' +
        kids + '<g class="on-done hearts"><path d="M160 120 q-8 -10 -14 -2 q-4 8 14 18 q18 -10 14 -18 q-6 -8 -14 2z" fill="#ff6f91"' + strokeAttr(2) + '/>' +
        '<path d="M250 108 q-6 -8 -11 -1 q-3 6 11 14 q14 -8 11 -14 q-5 -7 -11 1z" fill="#ff6f91"' + strokeAttr(2) + '/></g>' + burst(200, 130) + '</g>';
    },
    gears: function () {
      return '<g><rect x="96" y="70" width="208" height="130" rx="18" fill="#6b7fd0"' + strokeAttr(3.5) + '/><rect x="106" y="80" width="188" height="110" rx="12" fill="#4a5ba6"/>' +
        '<path class="gear cw" d="' + gearPath(165, 138, 30, 10) + '" fill="#ffd36b"' + strokeAttr(3) + '/><circle cx="165" cy="138" r="9" fill="#fff"' + strokeAttr(2.5) + '/>' +
        '<path class="gear ccw" d="' + gearPath(226, 150, 21, 8) + '" fill="#ff8f6b"' + strokeAttr(3) + '/><circle cx="226" cy="150" r="7" fill="#fff"' + strokeAttr(2.5) + '/>' +
        '<path class="gear cw" d="' + gearPath(262, 112, 15, 7) + '" fill="#4fd4a4"' + strokeAttr(3) + '/><circle cx="262" cy="112" r="5" fill="#fff"' + strokeAttr(2.5) + '/>' +
        '<rect x="188" y="44" width="24" height="28" rx="6" fill="#c9d2ff"' + strokeAttr(3) + '/><circle class="off-done" cx="200" cy="36" r="14" fill="#9aa3c7"' + strokeAttr(3) + '/>' +
        '<circle class="on-done lamp" cx="200" cy="36" r="14" fill="#ffe14a"' + strokeAttr(3) + '/><g class="on-done steam"><circle cx="128" cy="62" r="7" fill="#fff" opacity=".85"/><circle cx="140" cy="48" r="5" fill="#fff" opacity=".7"/></g>' +
        burst(200, 120) + '</g>';
    },
    lanterns: function () {
      var out = '<path d="M30 78 Q200 112 370 78" fill="none" stroke="' + INK + '" stroke-width="3.5"/><rect x="18" y="70" width="14" height="130" rx="5" fill="#9a6a4a"' + strokeAttr(3) + '/><rect x="368" y="70" width="14" height="130" rx="5" fill="#9a6a4a"' + strokeAttr(3) + '/>', i;
      var hues = ['#ff6f61', '#ff9f43', '#ff6f91', '#ff8f6b', '#ffb347'];
      for (i = 0; i < 5; i++) {
        var x = 78 + i * 61, y = 100 + Math.round(Math.sin((i / 4) * Math.PI) * 6) + 6 - 6;
        out += '<g class="lantern reveal-lit" data-at="' + ((i + 1) / 5).toFixed(3) + '"><line x1="' + x + '" y1="' + (y - 18) + '" x2="' + x + '" y2="' + (y + 4) + '" stroke="' + INK + '" stroke-width="2.5"/>' +
          '<circle class="glow" cx="' + x + '" cy="' + (y + 32) + '" r="34" fill="#ffe27a" opacity="0"/>' +
          '<rect x="' + (x - 8) + '" y="' + (y + 2) + '" width="16" height="7" rx="3" fill="#6b4a2e"' + strokeAttr(2) + '/>' +
          '<ellipse class="body" cx="' + x + '" cy="' + (y + 32) + '" rx="19" ry="25" fill="' + hues[i] + '"' + strokeAttr(3) + '/>' +
          '<path d="M' + (x - 10) + ' ' + (y + 14) + ' q10 -6 20 0 M' + (x - 14) + ' ' + (y + 32) + ' h28 M' + (x - 10) + ' ' + (y + 50) + ' q10 6 20 0" stroke="' + INK + '" stroke-width="2" fill="none" opacity=".6"/>' +
          '<rect x="' + (x - 6) + '" y="' + (y + 56) + '" width="12" height="6" rx="3" fill="#6b4a2e"' + strokeAttr(2) + '/></g>';
      }
      return '<g>' + out + burst(200, 120) + '</g>';
    },
    gate: function () {
      return '<g><rect x="120" y="60" width="160" height="150" rx="10" fill="#ffe27a" opacity=".9"/><rect class="on-done" x="120" y="60" width="160" height="150" rx="10" fill="#fff8c4"/>' +
        '<g class="door-l"><rect x="122" y="74" width="78" height="136" rx="6" fill="#8a7f9e"' + strokeAttr(3) + '/><path d="M142 86 V208 M162 86 V208 M182 86 V208" stroke="' + INK + '" stroke-width="3" opacity=".55"/>' +
        '<circle cx="140" cy="130" r="5" fill="#c9742e" class="off-done"/><circle cx="170" cy="168" r="6" fill="#c9742e" class="off-done"/></g>' +
        '<g class="door-r"><rect x="200" y="74" width="78" height="136" rx="6" fill="#8a7f9e"' + strokeAttr(3) + '/><path d="M220 86 V208 M240 86 V208 M260 86 V208" stroke="' + INK + '" stroke-width="3" opacity=".55"/>' +
        '<circle cx="258" cy="120" r="6" fill="#c9742e" class="off-done"/></g>' +
        '<rect x="104" y="52" width="26" height="160" rx="8" fill="#b9b0cf"' + strokeAttr(3) + '/><rect x="270" y="52" width="26" height="160" rx="8" fill="#b9b0cf"' + strokeAttr(3) + '/>' +
        '<path d="M104 56 Q200 20 296 56" fill="none" stroke="' + INK + '" stroke-width="3.5"/><path d="M104 56 Q200 20 296 56 V70 Q200 36 104 70Z" fill="#cfc6e6"' + strokeAttr(3) + '/>' +
        '<g class="lock off-done"><rect x="186" y="128" width="28" height="24" rx="5" fill="#ffd36b"' + strokeAttr(3) + '/><path d="M192 128 v-8 a8 8 0 0 1 16 0 v8" fill="none" stroke="' + INK + '" stroke-width="3.5"/></g>' + burst(200, 130) + '</g>';
    },
    ferry: function () {
      return '<g><rect y="170" width="400" height="70" fill="#37b5e6" opacity=".0"/>' +
        '<g class="boat"><path d="M168 150 H300 q-12 34 -40 34 H198 q-24 0 -30 -34z" fill="#ff6f61"' + strokeAttr(3.5) + '/><rect x="196" y="112" width="70" height="40" rx="8" fill="#fff6e0"' + strokeAttr(3) + '/>' +
        '<rect x="206" y="122" width="16" height="16" rx="4" fill="#9fe0ff"' + strokeAttr(2.5) + '/><rect x="232" y="122" width="16" height="16" rx="4" fill="#9fe0ff"' + strokeAttr(2.5) + '/>' +
        '<rect x="224" y="90" width="18" height="24" rx="4" fill="#5fb8ff"' + strokeAttr(3) + '/><path class="flag" d="M262 112 V84 l26 8 l-26 8" fill="#ffc93c"' + strokeAttr(2.5) + '/></g>' +
        '<path d="M0 160 H150 V240 H0Z" fill="#b9885c"' + strokeAttr(3) + '/><path d="M0 160 H150 M0 180 H150 M0 200 H150" stroke="#8a5a36" stroke-width="3"/>' +
        '<rect x="96" y="100" width="40" height="58" rx="8" fill="#6b7fd0"' + strokeAttr(3) + '/><rect x="104" y="110" width="24" height="12" rx="3" fill="#2b2350"/>' +
        '<circle class="off-done" cx="116" cy="136" r="7" fill="#ff6f61"' + strokeAttr(2.5) + '/><circle class="on-done" cx="116" cy="136" r="7" fill="#4fd4a4"' + strokeAttr(2.5) + '/>' + burst(200, 110) + '</g>';
    },
    tank: function () {
      var ticks = '', i;
      for (i = 1; i < 4; i++) ticks += '<path d="M138 ' + (60 + i * 30) + ' h12" stroke="' + INK + '" stroke-width="2" opacity=".45"/>';
      return '<g><rect x="120" y="200" width="160" height="30" rx="8" fill="#c98a52"' + strokeAttr(3) + '/><rect x="140" y="226" width="14" height="14" fill="#9a6a4a"/><rect x="246" y="226" width="14" height="14" fill="#9a6a4a"/>' +
        '<defs><clipPath id="tankclip"><rect x="130" y="52" width="140" height="150" rx="14"/></clipPath></defs>' +
        '<rect x="130" y="52" width="140" height="150" rx="14" fill="#e8f8ff" opacity=".7"/>' +
        '<g clip-path="url(#tankclip)"><rect class="water" x="130" y="52" width="140" height="150" fill="#3cc0ea" opacity=".85"/><path class="waves" d="M110 70 q10 -8 20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0 t20 0" fill="none" stroke="#bff0ff" stroke-width="3" opacity=".0"/></g>' +
        ticks + '<g class="fish reveal" data-at="1"><ellipse cx="200" cy="150" rx="18" ry="11" fill="#ff9f43"' + strokeAttr(2.5) + '/><path d="M182 150 l-14 -10 v20z" fill="#ff9f43"' + strokeAttr(2.5) + '/><circle cx="208" cy="147" r="3" fill="' + INK + '"/></g>' +
        '<rect x="130" y="52" width="140" height="150" rx="14" fill="none"' + strokeAttr(3.5) + '/>' +
        '<g><rect x="298" y="110" width="64" height="40" rx="8" fill="#fff6e0"' + strokeAttr(3) + '/><text data-text="frac" x="330" y="137" text-anchor="middle" font-size="19" font-weight="900" fill="' + INK + '">?</text></g>' + burst(200, 110) + '</g>';
    },
    door: function () {
      return '<g><rect x="90" y="40" width="220" height="180" rx="14" fill="#9fb4d0"' + strokeAttr(3.5) + '/><path d="M90 90 h220 M90 140 h220 M150 40 v50 M230 40 v50 M120 90 v50 M200 90 v50 M280 90 v50" stroke="#7b92b3" stroke-width="2.5"/>' +
        '<path d="M150 220 V104 a50 50 0 0 1 100 0 V220Z" fill="#fff0a0"/><rect class="on-done" x="150" y="54" width="100" height="166" fill="#fff8c4"/>' +
        '<g class="portcullis"><path d="M150 220 V104 a50 50 0 0 1 100 0 V220Z" fill="#8c6bff"' + strokeAttr(3.5) + '/>' +
        '<circle cx="200" cy="114" r="11" fill="#ffc93c"' + strokeAttr(2.5) + '/><path d="M176 170 l12 -22 l12 22z" fill="#4fd4a4"' + strokeAttr(2.5) + '/><rect x="212" y="148" width="20" height="20" rx="3" fill="#ff6f61"' + strokeAttr(2.5) + '/>' +
        '<circle cx="232" cy="190" r="4" fill="#ffd36b"' + strokeAttr(2) + '/></g>' + burst(200, 120) + '</g>';
    },
    chest: function () {
      var coins = [[170, 150], [196, 140], [222, 148], [246, 156], [184, 160]].map(function (c, i) {
        return '<g class="loot" style="--i:' + i + '"><circle cx="' + c[0] + '" cy="' + c[1] + '" r="11" fill="#ffd54a"' + strokeAttr(2.5) + '/><circle cx="' + c[0] + '" cy="' + c[1] + '" r="6" fill="none" stroke="#e0a800" stroke-width="2"/></g>';
      }).join('');
      return '<g><ellipse cx="200" cy="206" rx="110" ry="16" fill="#e3c280"' + strokeAttr(2.5) + '/>' +
        coins +
        '<rect x="132" y="150" width="136" height="56" rx="10" fill="#b9733a"' + strokeAttr(3.5) + '/><path d="M132 176 h136" stroke="' + INK + '" stroke-width="3"/>' +
        '<rect x="188" y="162" width="24" height="26" rx="5" fill="#ffd36b"' + strokeAttr(3) + '/><circle cx="200" cy="174" r="4" fill="' + INK + '"/>' +
        '<g class="lid"><path d="M132 150 a68 38 0 0 1 136 0z" fill="#d38a48"' + strokeAttr(3.5) + '/><path d="M132 150 h136" stroke="' + INK + '" stroke-width="3"/><path d="M170 120 v30 M230 120 v30" stroke="#ffd36b" stroke-width="7" stroke-linecap="round"/></g>' + burst(200, 120) + '</g>';
    },
    lighthouse: function () {
      return '<g><path class="rock" d="M120 222 Q160 176 200 190 Q250 172 290 222Z" fill="#9ab0c9"' + strokeAttr(3) + '/>' +
        '<path d="M172 196 L182 70 H218 L228 196Z" fill="#fff6e0"' + strokeAttr(3.5) + '/><path d="M175 168 L178 140 H222 L225 168Z M180 112 L183 86 H217 L220 112Z" fill="#ff6f61"' + strokeAttr(2.5) + '/>' +
        '<rect class="reveal-lit" data-at="0.333" x="192" y="150" width="16" height="14" rx="4" fill="#9fb3d6"' + strokeAttr(2.5) + '/>' +
        '<rect class="reveal-lit" data-at="0.667" x="192" y="118" width="16" height="14" rx="4" fill="#9fb3d6"' + strokeAttr(2.5) + '/>' +
        '<rect x="176" y="62" width="48" height="12" rx="5" fill="#6b7fd0"' + strokeAttr(3) + '/><rect x="184" y="38" width="32" height="26" rx="6" fill="#cfe9ff"' + strokeAttr(3) + '/>' +
        '<circle class="reveal-lit lamp" data-at="1" cx="200" cy="51" r="9" fill="#9fb3d6"' + strokeAttr(2.5) + '/>' +
        '<path d="M178 38 L200 14 L222 38Z" fill="#6b7fd0"' + strokeAttr(3) + '/>' +
        '<g class="beamwrap on-done"><path class="lightbeam" d="M200 51 L40 20 V84Z" fill="#fff6a0" opacity=".65"/><path class="lightbeam" d="M200 51 L360 20 V84Z" fill="#fff6a0" opacity=".65"/></g>' + burst(200, 60) + '</g>';
    }
  };


  /* ---- extra island backdrops: one generic builder, each theme supplies colours + a little scenery ---- */
  function landBG(c) {
    return function (u) {
      return '<defs><linearGradient id="' + u + 'sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + c.s1 + '"/><stop offset="1" stop-color="' + c.s2 + '"/></linearGradient></defs>' +
        '<rect width="400" height="240" fill="url(#' + u + 'sky)"/>' + (c.deco || '') +
        '<path d="M0 172 Q80 146 170 168 T310 162 T400 158 V240 H0Z" fill="' + c.h1 + '"' + strokeAttr(2.5) + '/>' +
        '<path d="M0 202 Q100 180 200 200 T400 192 V240 H0Z" fill="' + c.h2 + '"' + strokeAttr(2.5) + '/>';
    };
  }
  function stars(n, seed) {
    var o = '<g class="twinkle">';
    for (var i = 0; i < n; i++) o += '<circle cx="' + ((i * 97 + seed * 31) % 380 + 10) + '" cy="' + ((i * 53 + seed * 17) % 120 + 8) + '" r="' + (1.5 + (i % 3) * .7) + '" fill="#fff6c8"/>';
    return o + '</g>';
  }
  BG.foundry = landBG({ s1: '#ffb98a', s2: '#fff0d6', h1: '#c98a5a', h2: '#a2673f',
    deco: '<path class="gear cw slow" d="' + gearPath(70, 96, 30, 10, 5) + '" fill="#ffd36b"' + strokeAttr(2.5) + '/><path class="gear ccw slow" d="' + gearPath(330, 80, 24, 9, 5) + '" fill="#ff8f6b"' + strokeAttr(2.5) + '/>' +
      '<rect x="180" y="70" width="22" height="90" rx="5" fill="#9a6a4a"' + strokeAttr(2.5) + '/><circle cx="196" cy="56" r="14" fill="#fff" opacity=".7"/><circle cx="208" cy="38" r="10" fill="#fff" opacity=".5"/>' });
  BG.city = landBG({ s1: '#8fb4ff', s2: '#e9efff', h1: '#7b88b8', h2: '#5a6595',
    deco: [[30, 60, 44], [86, 40, 52], [150, 76, 40], [200, 30, 60], [270, 58, 46], [330, 44, 50]].map(function (b) {
      var o = '<rect x="' + b[0] + '" y="' + (170 - b[1] - 60) + '" width="' + b[2] + '" height="' + (b[1] + 60) + '" fill="#a9b6e6"' + strokeAttr(2.5) + '/>';
      for (var w = 0; w < 3; w++) o += '<rect x="' + (b[0] + 8 + (w % 2) * 18) + '" y="' + (170 - b[1] - 46 + w * 22) + '" width="9" height="11" rx="2" fill="#fff3a8"/>';
      return o;
    }).join('') });
  BG.harbour = landBG({ s1: '#ff9a8b', s2: '#ffe7b0', h1: '#4aa3d8', h2: '#2d7fbf',
    deco: '<circle cx="300" cy="120" r="46" fill="#ffd54a" opacity=".85"/>' +
      '<rect x="60" y="60" width="44" height="100" rx="6" fill="#fff6e0"' + strokeAttr(2.5) + '/><path d="M56 62 L82 34 L108 62Z" fill="#ff6f61"' + strokeAttr(2.5) + '/><circle cx="82" cy="88" r="14" fill="#fff"' + strokeAttr(2.5) + '/><path d="M82 88 v-9 M82 88 l7 4" stroke="#2b2350" stroke-width="2.6" stroke-linecap="round" fill="none"/>' });
  BG.market = landBG({ s1: '#ffd27a', s2: '#fff3d6', h1: '#e6a05a', h2: '#c47d3c',
    deco: [[40, '#ff6f61'], [150, '#5fb8ff'], [260, '#4fd4a4']].map(function (st) {
      return '<g><rect x="' + (st[0] + 8) + '" y="100" width="6" height="64" fill="#9a6a4a"/><rect x="' + (st[0] + 80) + '" y="100" width="6" height="64" fill="#9a6a4a"/>' +
        '<path d="M' + st[0] + ' 104 L' + (st[0] + 94) + ' 104 L' + (st[0] + 84) + ' 80 L' + (st[0] + 10) + ' 80Z" fill="' + st[1] + '"' + strokeAttr(2.5) + '/>' +
        '<path d="M' + (st[0] + 34) + ' 80 L' + (st[0] + 30) + ' 104 M' + (st[0] + 60) + ' 80 L' + (st[0] + 64) + ' 104" stroke="#fff" stroke-width="5" opacity=".7"/></g>';
    }).join('') });
  BG.desert = landBG({ s1: '#9fdcff', s2: '#ffeeb8', h1: '#f5d27a', h2: '#e0b25a',
    deco: '<circle cx="320" cy="50" r="28" fill="#ffd54a"' + strokeAttr(2.5) + '/><path d="M0 150 Q60 110 130 150Z" fill="#f9dc8c"' + strokeAttr(2.5) + '/><path d="M240 156 Q300 112 370 156Z" fill="#f9dc8c"' + strokeAttr(2.5) + '/>' +
      '<g><rect x="190" y="104" width="16" height="62" rx="8" fill="#58c76b"' + strokeAttr(2.5) + '/><path d="M190 128 q-18 0 -18 -18 M206 120 q18 0 18 -16" stroke="#2f8f4f" stroke-width="9" fill="none" stroke-linecap="round"/></g>' });
  BG.snow = landBG({ s1: '#b5dcff', s2: '#f4fbff', h1: '#ffffff', h2: '#dbeaf7',
    deco: '<path d="M20 170 L110 62 L200 170Z" fill="#9ab8e0"' + strokeAttr(2.5) + '/><path d="M86 90 L110 62 L134 90 L120 84 L110 94 L100 84Z" fill="#fff"/><path d="M150 170 L250 40 L350 170Z" fill="#86a6d6"' + strokeAttr(2.5) + '/><path d="M222 78 L250 40 L278 78 L262 70 L250 84 L238 70Z" fill="#fff"/>' +
      '<g class="twinkle"><circle cx="60" cy="40" r="3" fill="#fff"/><circle cx="330" cy="30" r="3" fill="#fff"/><circle cx="200" cy="24" r="2.5" fill="#fff"/></g>' });
  BG.reef = landBG({ s1: '#6fd8e8', s2: '#c7f5ee', h1: '#3bb8c4', h2: '#2a8ea8',
    deco: '<g class="twinkle"><circle cx="60" cy="60" r="7" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="90" cy="100" r="5" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="330" cy="70" r="8" fill="none" stroke="#fff" stroke-width="2.5"/></g>' +
      '<path d="M230 170 q-8 -40 6 -60 q6 22 -2 60z M252 170 q4 -34 20 -48 q0 26 -12 48z" fill="#ff8fa3"' + strokeAttr(2.5) + '/><path d="M60 170 q-10 -30 8 -52 q8 24 -4 52z" fill="#ffb86b"' + strokeAttr(2.5) + '/>' });
  BG.space = landBG({ s1: '#2a1f6b', s2: '#6a4fd0', h1: '#4b3d9a', h2: '#352b78',
    deco: stars(26, 3) + '<circle cx="310" cy="70" r="34" fill="#ff9f7a"' + strokeAttr(2.5) + '/><ellipse cx="310" cy="72" rx="52" ry="10" fill="none" stroke="#ffd9c0" stroke-width="5" transform="rotate(-18 310 72)"/>' +
      '<circle cx="80" cy="64" r="16" fill="#9fe0ff"' + strokeAttr(2.5) + '/>' });

  BG.volcano = landBG({ s1: '#ff9a6b', s2: '#ffe1b8', h1: '#b5654a', h2: '#8a4a3a',
    deco: '<path d="M120 170 L170 60 L220 170Z" fill="#8a5a4a"' + strokeAttr(2.5) + '/><path d="M158 64 L170 52 L184 66 Q170 78 158 64Z" fill="#ff6f3c"/><circle cx="186" cy="38" r="12" fill="#fff" opacity=".6"/><circle cx="200" cy="22" r="9" fill="#fff" opacity=".45"/>' });
  BG.pirate = landBG({ s1: '#6fd0ff', s2: '#fff0c8', h1: '#3aa0d8', h2: '#2a78b8',
    deco: '<path d="M240 160 h90 l-12 20 h-66z" fill="#8a5a3a"' + strokeAttr(2.5) + '/><rect x="282" y="76" width="5" height="84" fill="#5a3a22"/><path d="M287 80 h34 v24 h-34z" fill="#2b2350"/><circle cx="304" cy="92" r="5" fill="#fff"/><path d="M240 130 l40 -30 v60z" fill="#fff6e0"' + strokeAttr(2.5) + '/>' });
  BG.jungle = landBG({ s1: '#9be7a8', s2: '#e8ffd0', h1: '#3fb56a', h2: '#2a8c52',
    deco: '<rect x="70" y="70" width="14" height="100" fill="#8a5a3a"' + strokeAttr(2.5) + '/><circle cx="76" cy="66" r="34" fill="#35c46a"' + strokeAttr(2.5) + '/><circle cx="330" cy="80" r="28" fill="#4fd37a"' + strokeAttr(2.5) + '/><path d="M330 108 v60" stroke="#8a5a3a" stroke-width="10"/><circle cx="210" cy="62" r="8" fill="#ff5f5f"' + strokeAttr(2) + '/>' });
  BG.candy = landBG({ s1: '#ffc8e8', s2: '#fff4fb', h1: '#ff9ccd', h2: '#f27bb5',
    deco: '<path d="M90 170 V84" stroke="#fff" stroke-width="7"/><circle cx="90" cy="70" r="26" fill="#ff6fa8"' + strokeAttr(2.5) + '/><path d="M72 70 a18 18 0 0 1 36 0" fill="none" stroke="#fff" stroke-width="5"/><path d="M300 170 V92 q0 -28 24 -28" stroke="#ff4f7a" stroke-width="9" fill="none" stroke-linecap="round"/>' });
  BG.dino = landBG({ s1: '#ffd38a', s2: '#fff4d0', h1: '#8ac060', h2: '#5f9a46',
    deco: '<ellipse cx="90" cy="150" rx="46" ry="26" fill="#6fcf6a"' + strokeAttr(2.5) + '/><path d="M126 140 q40 -50 50 -88 q22 6 14 22 q-8 30 -30 74z" fill="#6fcf6a"' + strokeAttr(2.5) + '/><circle cx="174" cy="56" r="3" fill="#2b2350"/><path d="M280 170 q-6 -50 20 -64 q26 14 20 64z" fill="#fff6e0"' + strokeAttr(2.5) + '/>' });
  BG.robot = landBG({ s1: '#b9c8e6', s2: '#eef3ff', h1: '#8a9ac0', h2: '#6a7aa0',
    deco: '<path class="gear cw slow" d="' + gearPath(80, 90, 30, 10, 5) + '" fill="#ffd36b"' + strokeAttr(2.5) + '/><rect x="250" y="60" width="70" height="100" rx="12" fill="#aab8d8"' + strokeAttr(2.5) + '/><circle cx="272" cy="96" r="9" fill="#fff"/><circle cx="298" cy="96" r="9" fill="#fff"/><path d="M285 60 v-20" stroke="#2b2350" stroke-width="4"/><circle cx="285" cy="36" r="6" fill="#ff6f61"/>' });
  BG.arena = landBG({ s1: '#8fd4ff', s2: '#eaf9ff', h1: '#5fcf6f', h2: '#3fb257',
    deco: '<path d="M60 168 V96 H150 V168" fill="none" stroke="#fff" stroke-width="6"/><path d="M60 110 H150 M60 124 H150 M60 138 H150" stroke="#fff" stroke-width="2" opacity=".7"/><circle cx="300" cy="150" r="16" fill="#fff"' + strokeAttr(2.5) + '/><path d="M300 138 l8 8 l-3 10 h-10 l-3 -10z" fill="#2b2350"/>' });
  BG.castle = landBG({ s1: '#a8c8ff', s2: '#f0f4ff', h1: '#9a9aa8', h2: '#76768a',
    deco: '<rect x="130" y="70" width="140" height="100" fill="#cfcfdc"' + strokeAttr(2.5) + '/><rect x="110" y="50" width="36" height="120" fill="#bdbdd0"' + strokeAttr(2.5) + '/><rect x="254" y="50" width="36" height="120" fill="#bdbdd0"' + strokeAttr(2.5) + '/><path d="M110 50 l18 -26 l18 26z M254 50 l18 -26 l18 26z" fill="#ff6f61"' + strokeAttr(2.5) + '/><path d="M178 170 v-34 a22 22 0 0 1 44 0 v34z" fill="#6a5a8a"' + strokeAttr(2.5) + '/>' });
  BG.rainbow = landBG({ s1: '#b9e4ff', s2: '#fff8fd', h1: '#c9f0b0', h2: '#9fe0a0',
    deco: ['#ff6f61', '#ffc93c', '#7de08f', '#5fb8ff', '#b88cff'].map(function (c, i) { return '<path d="M' + (40 + i * 10) + ' 170 a' + (160 - i * 10) + ' ' + (130 - i * 10) + ' 0 0 1 ' + (2 * (160 - i * 10)) + ' 0" fill="none" stroke="' + c + '" stroke-width="10"/>'; }).join('') });
  BG.carnival = landBG({ s1: '#5a2f9a', s2: '#ff9ad8', h1: '#8a4ac0', h2: '#6a34a0',
    deco: stars(14, 5) + '<circle cx="110" cy="100" r="44" fill="none" stroke="#ffd54a" stroke-width="6"/><path d="M110 56 v88 M66 100 h88 M79 69 l62 62 M141 69 l-62 62" stroke="#ffd54a" stroke-width="3"/><path d="M250 170 l30 -70 l30 70z" fill="#ff6f61"' + strokeAttr(2.5) + '/><path d="M265 170 l15 -70 l15 70z" fill="#fff"/>' });

  BG.kampung = landBG({ s1: '#ffe9a8', s2: '#fff8dc', h1: '#9ad66a', h2: '#6fb84a',
    deco: '<path d="M120 170 v-50 h110 v50z" fill="#c9954a"' + strokeAttr(2.5) + '/><path d="M108 120 l67 -44 l67 44z" fill="#a0522d"' + strokeAttr(2.5) + '/><rect x="160" y="136" width="26" height="34" fill="#6a4a2a"/><path d="M300 170 v-60 M300 110 q-26 -10 -30 -34 M300 110 q26 -10 30 -34" stroke="#4fa84f" stroke-width="6" fill="none"/> ' });
  BG.nightmarket = landBG({ s1: '#2a2060', s2: '#7a4aa8', h1: '#4a3a8a', h2: '#33296a',
    deco: stars(10, 4) + '<path d="M40 120 h90 l-10 -30 h-70z" fill="#ff6f61"' + strokeAttr(2.5) + '/><path d="M250 120 h90 l-10 -30 h-70z" fill="#ffd54a"' + strokeAttr(2.5) + '/><circle cx="190" cy="60" r="10" fill="#ffd54a"/><circle cx="160" cy="76" r="8" fill="#ff9a3a"/><circle cx="222" cy="76" r="8" fill="#ff6f61"/> ' });
  BG.kites = landBG({ s1: '#8fd4ff', s2: '#eaf9ff', h1: '#9ae07a', h2: '#6fc95a',
    deco: '<path d="M100 40 l26 30 l-26 36 l-26 -36z" fill="#ff6f61"' + strokeAttr(2.5) + '/><path d="M280 60 l22 24 l-22 30 l-22 -30z" fill="#ffd54a"' + strokeAttr(2.5) + '/><path d="M100 106 q-20 30 0 60 M280 114 q20 24 0 54" stroke="#2b2350" stroke-width="2" fill="none"/> ' });
  BG.train = landBG({ s1: '#bfe0ff', s2: '#f4faff', h1: '#a8a8b8', h2: '#7c7c92',
    deco: '<path d="M20 170 h360" stroke="#5a4a3a" stroke-width="6"/><rect x="110" y="110" width="100" height="46" rx="8" fill="#ff6f61"' + strokeAttr(2.5) + '/><rect x="210" y="90" width="50" height="66" rx="6" fill="#5fb8ff"' + strokeAttr(2.5) + '/><circle cx="135" cy="162" r="10" fill="#2b2350"/><circle cx="235" cy="162" r="10" fill="#2b2350"/><circle cx="130" cy="80" r="10" fill="#fff" opacity=".8"/> ' });
  BG.bakery = landBG({ s1: '#ffe0c8', s2: '#fff6ec', h1: '#f0c08a', h2: '#d8a060',
    deco: '<rect x="120" y="90" width="150" height="80" rx="10" fill="#ffd9a8"' + strokeAttr(2.5) + '/><path d="M110 90 q85 -60 170 0z" fill="#e8683a"' + strokeAttr(2.5) + '/><rect x="176" y="120" width="40" height="50" rx="6" fill="#8a5a3a"/> ' });
  BG.deep = landBG({ s1: '#0a2a5a', s2: '#2a7aba', h1: '#1a5a8a', h2: '#0f4470',
    deco: stars(10, 4) + '<circle cx="90" cy="70" r="12" fill="#fff" opacity=".5"/><circle cx="110" cy="100" r="7" fill="#fff" opacity=".5"/><path d="M240 160 q10 -60 30 -80 q4 40 -2 80z" fill="#ff8ab8"' + strokeAttr(2.5) + '/><ellipse cx="320" cy="120" rx="26" ry="14" fill="#ffd54a"' + strokeAttr(2.5) + '/> ' });
  BG.zoo = landBG({ s1: '#c0f0ff', s2: '#f4fcff', h1: '#8ad868', h2: '#60b848',
    deco: '<rect x="70" y="100" width="90" height="70" fill="#c9954a"' + strokeAttr(2.5) + '/><path d="M60 100 h110 l-55 -34z" fill="#ff6f61"' + strokeAttr(2.5) + '/><path d="M250 170 v-70 M250 100 q-24 -24 -4 -44 M250 100 q24 -24 4 -44" stroke="#4fa84f" stroke-width="7" fill="none"/> ' });
  BG.toys = landBG({ s1: '#ffd8f0', s2: '#fff4fa', h1: '#ffc060', h2: '#e89a3a',
    deco: '<rect x="90" y="110" width="60" height="60" rx="6" fill="#ff6f61"' + strokeAttr(2.5) + '/><rect x="164" y="90" width="60" height="80" rx="6" fill="#5fb8ff"' + strokeAttr(2.5) + '/><rect x="238" y="124" width="50" height="46" rx="6" fill="#ffd54a"' + strokeAttr(2.5) + '/><circle cx="120" cy="140" r="9" fill="#fff"/><circle cx="194" cy="130" r="9" fill="#fff"/> ' });
  BG.treehouse = landBG({ s1: '#c8f0a0', s2: '#f4ffe8', h1: '#5fb848', h2: '#3f9a38',
    deco: '<rect x="170" y="90" width="44" height="80" fill="#7a5a3a"' + strokeAttr(2.5) + '/><circle cx="192" cy="70" r="52" fill="#3fa84f"' + strokeAttr(2.5) + '/><rect x="164" y="60" width="56" height="36" rx="5" fill="#d8a060"' + strokeAttr(2.5) + '/><path d="M158 60 l34 -24 l34 24z" fill="#ff6f61"' + strokeAttr(2.5) + '/> ' });
  BG.festival = landBG({ s1: '#2a1a5a', s2: '#ff9a5a', h1: '#6a3a8a', h2: '#4a2a6a',
    deco: stars(10, 4) + '<path d="M40 40 q150 40 320 0" fill="none" stroke="#2b2350" stroke-width="3"/><ellipse cx="100" cy="68" rx="16" ry="20" fill="#ff6f61"' + strokeAttr(2.5) + '/><ellipse cx="190" cy="76" rx="16" ry="20" fill="#ffd54a"' + strokeAttr(2.5) + '/><ellipse cx="280" cy="68" rx="16" ry="20" fill="#ff6f61"' + strokeAttr(2.5) + '/> ' });

  /** Build one scene. Returns an <svg> string. */
  function scene(sceneKey, islandKey) {
    var u = uid();
    var bg = (BG[islandKey] || BG.meadow)(u);
    var stuff = (STUFF[sceneKey] || function () { return ''; })();
    return '<svg class="scene" viewBox="0 0 400 240" preserveAspectRatio="xMidYMid slice" role="img" aria-hidden="true" focusable="false" data-state="broken" style="--p:0">' + bg + stuff + '</svg>';
  }

  /** Update a live scene: progress 0..1 reveals data-at items; vars set CSS custom properties. */
  function setProgress(svg, p) {
    if (!svg) return;
    svg.style.setProperty('--p', String(p));
    var items = svg.querySelectorAll('[data-at]');
    for (var i = 0; i < items.length; i++) {
      var at = parseFloat(items[i].getAttribute('data-at'));
      if (p + 1e-9 >= at) items[i].classList.add('on'); else items[i].classList.remove('on');
    }
  }
  function setVar(svg, name, value) { if (svg) svg.style.setProperty('--' + name, value); }
  function setText(svg, key, value) {
    if (!svg) return;
    var nodes = svg.querySelectorAll('[data-text="' + key + '"]');
    for (var i = 0; i < nodes.length; i++) nodes[i].textContent = value;
  }
  function setDone(svg, done) { if (svg) svg.setAttribute('data-state', done ? 'done' : 'broken'); }

  /* ---------------- creatures (collectibles + story characters) ---------------- */
  var BODY = {
    blob:  { d: 'M18 68 C8 40 28 14 55 14 C82 14 94 40 82 68 C76 88 26 90 18 68Z', eyeY: 46, top: 14, mouthY: 62 },
    round: { c: [50, 56, 34], eyeY: 50, top: 22, mouthY: 66 },
    tall:  { r: [28, 12, 44, 78, 22], eyeY: 40, top: 12, mouthY: 56 },
    drop:  { d: 'M50 8 C62 32 86 44 86 66 C86 84 70 94 50 94 C30 94 14 84 14 66 C14 44 38 32 50 8Z', eyeY: 62, top: 8, mouthY: 78 },
    cloud: { cloud: true, eyeY: 54, top: 28, mouthY: 70 }
  };

  var TINTS = [['#ffb3a8', '#ef6f5e'], ['#ffd6a0', '#e8a050'], ['#fff3a8', '#ffd84d'], ['#bff5a8', '#6fd45a'], ['#a8f0e0', '#3fc0a8'],
    ['#9fc4ff', '#5f8ff0'], ['#c9a0ff', '#9b6cff'], ['#ffb3f0', '#d26be0'], ['#e6e6ee', '#a9a6c4'], ['#5a5578', '#2f2b4a']];
  var PAL_ACCS = ['party', 'bow', 'flower', 'glasses', 'bandana', 'goggles', 'hat', 'scarf', 'tophat', 'headphones', 'leafcrown', 'halo', 'wizard', 'crown'];

  function creature(look, opts) {
    look = look || {};
    var u = uid(), b = BODY[look.body] || BODY.blob;
    var c1 = look.c1 || '#ffb86b', c2 = look.c2 || '#ff8f4d', w = 3;
    if (opts && opts.tint !== undefined && opts.tint !== null && TINTS[opts.tint]) { c1 = TINTS[opts.tint][0]; c2 = TINTS[opts.tint][1]; }
    var accId = (opts && opts.acc !== undefined && opts.acc !== null) ? opts.acc : look.acc;
    var fill = 'url(#' + u + 'g)';
    var ears = '', feat = '', acc = '', shape;
    var ex = 38, ex2 = 62, ey = b.eyeY;

    if (look.ears === 'round') ears = '<circle cx="27" cy="' + (b.top + 8) + '" r="11" fill="' + c2 + '"' + strokeAttr(w) + '/><circle cx="73" cy="' + (b.top + 8) + '" r="11" fill="' + c2 + '"' + strokeAttr(w) + '/>';
    else if (look.ears === 'point') ears = '<path d="M24 ' + (b.top + 20) + ' L22 ' + (b.top - 6) + ' L44 ' + (b.top + 6) + 'Z" fill="' + c2 + '"' + strokeAttr(w) + '/><path d="M76 ' + (b.top + 20) + ' L78 ' + (b.top - 6) + ' L56 ' + (b.top + 6) + 'Z" fill="' + c2 + '"' + strokeAttr(w) + '/>';
    else if (look.ears === 'leaf') ears = '<path d="M34 ' + (b.top + 6) + ' q-18 -4 -16 -20 q18 0 24 14z" fill="#7de08f"' + strokeAttr(w) + '/><path d="M66 ' + (b.top + 6) + ' q18 -4 16 -20 q-18 0 -24 14z" fill="#7de08f"' + strokeAttr(w) + '/>';

    if (b.d) shape = '<path d="' + b.d + '" fill="' + fill + '"' + strokeAttr(w) + '/>';
    else if (b.c) shape = '<circle cx="' + b.c[0] + '" cy="' + b.c[1] + '" r="' + b.c[2] + '" fill="' + fill + '"' + strokeAttr(w) + '/>';
    else if (b.r) shape = '<rect x="' + b.r[0] + '" y="' + b.r[1] + '" width="' + b.r[2] + '" height="' + b.r[3] + '" rx="' + b.r[4] + '" fill="' + fill + '"' + strokeAttr(w) + '/>';
    else shape = '<g fill="' + fill + '"' + strokeAttr(w) + '><circle cx="30" cy="62" r="20"/><circle cx="52" cy="48" r="26"/><circle cx="74" cy="62" r="20"/><rect x="30" y="62" width="44" height="20" rx="6" stroke="none"/></g>';

    var top = b.top;
    if (look.feat === 'antenna') feat = '<path d="M50 ' + top + ' Q46 ' + (top - 10) + ' 52 ' + (top - 16) + '" fill="none"' + strokeAttr(w) + '/><circle cx="52" cy="' + (top - 18) + '" r="5" fill="#ffd54a"' + strokeAttr(2.5) + ' class="pulse"/>';
    else if (look.feat === 'horn') feat = '<path d="M42 ' + (top + 2) + ' L50 ' + (top - 16) + ' L58 ' + (top + 2) + 'Z" fill="#ffd36b"' + strokeAttr(w) + '/>';
    else if (look.feat === 'fin') feat = '<path d="M16 ' + (ey + 10) + ' q-14 4 -10 20 q14 -2 18 -12z" fill="' + c2 + '"' + strokeAttr(w) + '/><path d="M84 ' + (ey + 10) + ' q14 4 10 20 q-14 -2 -18 -12z" fill="' + c2 + '"' + strokeAttr(w) + '/>';
    else if (look.feat === 'tuft') feat = '<path d="M44 ' + (top + 2) + ' q-4 -10 -10 -12 M50 ' + top + ' q0 -12 0 -16 M56 ' + (top + 2) + ' q4 -10 10 -12" fill="none"' + strokeAttr(w) + '/>';
    else if (look.feat === 'spikes') feat = '<path d="M30 ' + (top + 12) + ' L36 ' + (top - 8) + ' L44 ' + (top + 6) + ' L50 ' + (top - 12) + ' L56 ' + (top + 6) + ' L64 ' + (top - 8) + ' L70 ' + (top + 12) + 'Z" fill="#ffd36b"' + strokeAttr(w) + '/>';

    var eyes = '<g class="eyes"><ellipse cx="' + ex + '" cy="' + ey + '" rx="8.5" ry="10" fill="#fff"' + strokeAttr(2.5) + '/><ellipse cx="' + ex2 + '" cy="' + ey + '" rx="8.5" ry="10" fill="#fff"' + strokeAttr(2.5) + '/>' +
      '<circle cx="' + (ex + 1) + '" cy="' + (ey + 1) + '" r="5" fill="' + INK + '"/><circle cx="' + (ex2 + 1) + '" cy="' + (ey + 1) + '" r="5" fill="' + INK + '"/>' +
      '<circle cx="' + (ex + 3) + '" cy="' + (ey - 2) + '" r="1.8" fill="#fff"/><circle cx="' + (ex2 + 3) + '" cy="' + (ey - 2) + '" r="1.8" fill="#fff"/></g>';
    var cheeks = '<ellipse cx="' + (ex - 8) + '" cy="' + (ey + 14) + '" rx="5" ry="3.2" fill="#ff7f9d" opacity=".55"/><ellipse cx="' + (ex2 + 8) + '" cy="' + (ey + 14) + '" rx="5" ry="3.2" fill="#ff7f9d" opacity=".55"/>';
    var mouth = '<path d="M44 ' + b.mouthY + ' q6 7 12 0" fill="none"' + strokeAttr(2.8) + '/>';

    if (accId === 'goggles') acc = '<path d="M26 ' + ey + ' H74" stroke="' + INK + '" stroke-width="5" fill="none"/><circle cx="' + ex + '" cy="' + ey + '" r="12" fill="#9fe0ff" opacity=".55"' + strokeAttr(3.5) + '/><circle cx="' + ex2 + '" cy="' + ey + '" r="12" fill="#9fe0ff" opacity=".55"' + strokeAttr(3.5) + '/>';
    else if (accId === 'hat') acc = '<path d="M26 ' + (top + 10) + ' q24 -22 48 0z" fill="#2f4a9c"' + strokeAttr(w) + '/><rect x="22" y="' + (top + 8) + '" width="56" height="7" rx="3.5" fill="#1d2f70"' + strokeAttr(2.5) + '/><circle cx="50" cy="' + (top + 1) + '" r="3.5" fill="#ffd54a"/>';
    else if (accId === 'crown') acc = '<path d="M32 ' + (top + 6) + ' L34 ' + (top - 10) + ' L42 ' + (top - 2) + ' L50 ' + (top - 14) + ' L58 ' + (top - 2) + ' L66 ' + (top - 10) + ' L68 ' + (top + 6) + 'Z" fill="#ffd54a"' + strokeAttr(w) + '/>';
    else if (accId === 'scarf') acc = '<path d="M26 ' + (b.mouthY + 14) + ' q24 14 48 0 v9 q-24 14 -48 0z" fill="#ff6f61"' + strokeAttr(w) + '/><path d="M62 ' + (b.mouthY + 20) + ' l6 18 l10 -8 l-6 -14z" fill="#ff6f61"' + strokeAttr(2.5) + '/>';
    else if (accId === 'leafcrown') acc = '<path d="M30 ' + (top + 8) + ' q-8 -14 4 -18 q6 8 0 18z M44 ' + (top + 2) + ' q-4 -16 8 -18 q4 10 -2 18z M58 ' + (top + 2) + ' q4 -16 -8 -18 M70 ' + (top + 8) + ' q8 -14 -4 -18 q-6 8 0 18z" fill="#7de08f"' + strokeAttr(2.5) + '/><circle cx="50" cy="' + (top - 10) + '" r="5" fill="#ff7f9d"' + strokeAttr(2.5) + '/>';
    else if (accId === 'tophat') acc = '<rect x="22" y="' + (top + 2) + '" width="56" height="7" rx="3.5" fill="#2b2350"' + strokeAttr(2.5) + '/><rect x="32" y="' + (top - 20) + '" width="36" height="26" rx="4" fill="#3b3070"' + strokeAttr(w) + '/><rect x="32" y="' + (top - 4) + '" width="36" height="6" fill="#ff6f61"' + strokeAttr(2) + '/>';
    else if (accId === 'party') acc = '<path d="M34 ' + (top + 8) + ' L50 ' + (top - 22) + ' L66 ' + (top + 8) + 'Z" fill="#ff7fa6"' + strokeAttr(w) + '/><circle cx="50" cy="' + (top - 24) + '" r="4.5" fill="#ffd54a"' + strokeAttr(2.2) + '/><circle cx="46" cy="' + (top - 2) + '" r="2.6" fill="#fff"/><circle cx="55" cy="' + (top + 3) + '" r="2.6" fill="#7de08f"/>';
    else if (accId === 'bow') acc = '<path d="M64 ' + (top + 4) + ' L82 ' + (top - 6) + ' V' + (top + 14) + 'Z M64 ' + (top + 4) + ' L46 ' + (top - 6) + ' V' + (top + 14) + 'Z" fill="#ff7fa6"' + strokeAttr(2.8) + '/><circle cx="64" cy="' + (top + 4) + '" r="5" fill="#ff4d86"' + strokeAttr(2.5) + '/>';
    else if (accId === 'wizard') acc = '<path d="M28 ' + (top + 10) + ' L54 ' + (top - 30) + ' L74 ' + (top + 10) + 'Z" fill="#6a4fd0"' + strokeAttr(w) + '/><ellipse cx="51" cy="' + (top + 10) + '" rx="30" ry="6" fill="#4b36a8"' + strokeAttr(2.5) + '/><path d="' + starPath(54, top - 8, 7, 3.2) + '" fill="#ffd54a"/>';
    else if (accId === 'flower') acc = '<g' + strokeAttr(2.2) + '><circle cx="68" cy="' + (top - 4) + '" r="6" fill="#ff9ec2"/><circle cx="78" cy="' + (top + 4) + '" r="6" fill="#ff9ec2"/><circle cx="72" cy="' + (top + 14) + '" r="6" fill="#ff9ec2"/><circle cx="60" cy="' + (top + 10) + '" r="6" fill="#ff9ec2"/><circle cx="69" cy="' + (top + 5) + '" r="5" fill="#ffd54a"/></g>';
    else if (accId === 'halo') acc = '<ellipse cx="50" cy="' + (top - 10) + '" rx="20" ry="6" fill="none" stroke="#ffd54a" stroke-width="5"/><ellipse cx="50" cy="' + (top - 10) + '" rx="20" ry="6" fill="none" stroke="' + INK + '" stroke-width="1.4" opacity=".6"/>';
    else if (accId === 'bandana') acc = '<path d="M22 ' + (top + 14) + ' q28 -26 56 0 v7 q-28 -12 -56 0z" fill="#e8483f"' + strokeAttr(w) + '/><circle cx="40" cy="' + (top + 8) + '" r="2" fill="#fff"/><circle cx="52" cy="' + (top + 5) + '" r="2" fill="#fff"/><circle cx="63" cy="' + (top + 9) + '" r="2" fill="#fff"/><path d="M76 ' + (top + 16) + ' l10 6 l-12 2z" fill="#e8483f"' + strokeAttr(2.2) + '/>';
    else if (accId === 'headphones') acc = '<path d="M24 ' + (ey - 4) + ' Q50 ' + (top - 30) + ' 76 ' + (ey - 4) + '" fill="none" stroke="' + INK + '" stroke-width="5.5" stroke-linecap="round"/><rect x="17" y="' + (ey - 8) + '" width="12" height="20" rx="5" fill="#5fb8ff"' + strokeAttr(2.8) + '/><rect x="71" y="' + (ey - 8) + '" width="12" height="20" rx="5" fill="#5fb8ff"' + strokeAttr(2.8) + '/>';
    else if (accId === 'glasses') acc = '<g fill="#fff" fill-opacity=".25"' + strokeAttr(3) + '><circle cx="' + ex + '" cy="' + ey + '" r="12"/><circle cx="' + ex2 + '" cy="' + ey + '" r="12"/></g><path d="M50 ' + ey + ' h0 M47 ' + (ey - 1) + ' q3 -3 6 0" fill="none"' + strokeAttr(2.6) + '/>';

    var belly = '<ellipse cx="50" cy="' + (look.body === 'tall' ? 70 : look.body === 'drop' ? 80 : 74) + '" rx="17" ry="11" fill="#fff" opacity=".35"/>';
    var cls = (opts && opts.cls) || '';
    var locked = opts && opts.locked;
    if (locked) {
      return '<svg class="creature locked ' + cls + '" viewBox="0 0 100 100" aria-hidden="true" focusable="false">' + ears + shape.replace(fill, '#b7b3cc') + '<text x="50" y="68" text-anchor="middle" font-size="34" font-weight="900" fill="#fff" stroke="' + INK + '" stroke-width="1.5">?</text></svg>';
    }
    return '<svg class="creature ' + cls + '" viewBox="0 0 100 100" aria-hidden="true" focusable="false"><defs><linearGradient id="' + u + 'g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + c1 + '"/><stop offset="1" stop-color="' + c2 + '"/></linearGradient></defs>' +
      ears + feat + shape + belly + eyes + cheeks + mouth + acc + '</svg>';
  }

  var NPCS = {
    berri:  { body: 'round', c1: '#ff7a8a', c2: '#e84a68', ears: 'round', feat: 'none', acc: 'leafcrown' },
    tock:   { body: 'blob',  c1: '#8bb8ff', c2: '#4f86e8', ears: 'round', feat: 'antenna', acc: 'goggles' },
    pearla: { body: 'drop',  c1: '#f6f0ff', c2: '#cdb8ff', ears: 'none', feat: 'fin', acc: 'hat' },
    glim:   { body: 'tall',  c1: '#ffb3f0', c2: '#d26be0', ears: 'point', feat: 'horn', acc: 'none' },
    petal:  { body: 'round', c1: '#bff5a8', c2: '#6fd45a', ears: 'leaf', feat: 'tuft', acc: 'leafcrown' },
    cogg:   { body: 'blob',  c1: '#ffc48a', c2: '#e8873a', ears: 'round', feat: 'antenna', acc: 'goggles' },
    sleuth: { body: 'tall',  c1: '#b9c6ff', c2: '#7e8fe0', ears: 'point', feat: 'none', acc: 'hat' },
    tick:   { body: 'round', c1: '#ffb3a8', c2: '#ef6f5e', ears: 'round', feat: 'tuft', acc: 'scarf' },
    mango:  { body: 'drop',  c1: '#ffe08a', c2: '#ffb12e', ears: 'leaf', feat: 'none', acc: 'crown' },
    dune:   { body: 'cloud', c1: '#ffe9b0', c2: '#e8c06a', ears: 'none', feat: 'spikes', acc: 'scarf' },
    frost:  { body: 'blob',  c1: '#e6f4ff', c2: '#9fcdf2', ears: 'round', feat: 'none', acc: 'scarf' },
    coral:  { body: 'drop',  c1: '#ffb3c7', c2: '#ff7fa0', ears: 'none', feat: 'fin', acc: 'none' },
    nova:   { body: 'tall',  c1: '#d4c2ff', c2: '#8a6cf0', ears: 'point', feat: 'antenna', acc: 'goggles' },
    ember:  { body: 'drop',  c1: '#ffb07a', c2: '#ff5f3c', ears: 'point', feat: 'tuft', acc: 'none' },
    jolly:  { body: 'round', c1: '#ffe08a', c2: '#e8a82e', ears: 'round', feat: 'none', acc: 'bandana' },
    vine:   { body: 'blob',  c1: '#a8f0a0', c2: '#3fbf6a', ears: 'leaf', feat: 'tuft', acc: 'flower' },
    sprinkle: { body: 'round', c1: '#ffc2e2', c2: '#ff7fb8', ears: 'round', feat: 'tuft', acc: 'party' },
    rex:    { body: 'tall',  c1: '#c8f08a', c2: '#7ac24a', ears: 'none', feat: 'spikes', acc: 'none' },
    bolt:   { body: 'blob',  c1: '#d0dcf0', c2: '#8a9ac0', ears: 'round', feat: 'antenna', acc: 'headphones' },
    goal:   { body: 'round', c1: '#9fe8a8', c2: '#3fb257', ears: 'round', feat: 'none', acc: 'glasses' },
    knight: { body: 'tall',  c1: '#d8d8e8', c2: '#9a9ab4', ears: 'point', feat: 'horn', acc: 'none' },
    arc:    { body: 'cloud', c1: '#d8f0ff', c2: '#a8d4f8', ears: 'none', feat: 'none', acc: 'bow' },
    jester: { body: 'drop',  c1: '#ffb3f0', c2: '#b05ad8', ears: 'point', feat: 'antenna', acc: 'tophat' },
    ayam: { body: 'round', c1: '#ffd36b', c2: '#ff9a3a', ears: 'round', feat: 'tuft', acc: 'none' },
    satay: { body: 'blob', c1: '#ffb27a', c2: '#e8683a', ears: 'round', feat: 'antenna', acc: 'none' },
    layang: { body: 'tall', c1: '#ff8ab8', c2: '#e8508a', ears: 'point', feat: 'none', acc: 'none' },
    choo: { body: 'blob', c1: '#ff9a8a', c2: '#d8503a', ears: 'round', feat: 'antenna', acc: 'goggles' },
    bun: { body: 'round', c1: '#ffd9a8', c2: '#e8a05a', ears: 'round', feat: 'tuft', acc: 'none' },
    bubbo: { body: 'drop', c1: '#9af0ff', c2: '#3ab0d8', ears: 'none', feat: 'fin', acc: 'none' },
    zebra: { body: 'round', c1: '#f6f6f6', c2: '#8a8a9a', ears: 'round', feat: 'tuft', acc: 'none' },
    teddy: { body: 'round', c1: '#d8a070', c2: '#a8703a', ears: 'round', feat: 'none', acc: 'hat' },
    acorn: { body: 'round', c1: '#d8a060', c2: '#a8703a', ears: 'leaf', feat: 'tuft', acc: 'leafcrown' },
    lampu: { body: 'drop', c1: '#ffe27a', c2: '#ff8a3a', ears: 'none', feat: 'antenna', acc: 'none' }
  };
  function npc(id, opts) { return creature(NPCS[id] || NPCS.berri, opts); }

  /* ---------------- Nimbo, the cloud-sprite companion ---------------- */
  var HATS = {
    sprout: '<path d="M50 20 q-2 -12 4 -18" fill="none"' + strokeAttr(3) + '/><path d="M54 4 q14 -6 18 6 q-12 6 -18 -6z M52 8 q-14 -8 -20 2 q10 8 20 0z" fill="#7de08f"' + strokeAttr(2.5) + '/>',
    stargoggles: '<path d="M22 54 H78" stroke="' + INK + '" stroke-width="5" fill="none"/><path d="' + starPath(38, 54, 15, 7) + '" fill="#ffd54a"' + strokeAttr(3) + '/><path d="' + starPath(62, 54, 15, 7) + '" fill="#ffd54a"' + strokeAttr(3) + '/>',
    captain: '<path d="M28 26 q22 -26 44 0z" fill="#2f4a9c"' + strokeAttr(3) + '/><rect x="24" y="24" width="52" height="7" rx="3.5" fill="#1d2f70"' + strokeAttr(2.5) + '/><circle cx="50" cy="16" r="3.5" fill="#ffd54a"/>',
    rainbow: ''
  };

  function nimbo(opts) {
    opts = opts || {};
    var hat = opts.hat || null, u = uid();
    var propColors = hat === 'rainbow' ? ['#ff6f61', '#ffc93c', '#4fd4a4', '#5fb8ff'] : ['#ff6f61', '#5fb8ff', '#ff6f61', '#5fb8ff'];
    return '<svg class="nimbo ' + (opts.cls || '') + '" viewBox="0 0 100 100" data-mood="' + (opts.mood || 'idle') + '" aria-hidden="true" focusable="false">' +
      '<defs><linearGradient id="' + u + 'g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#cfe6ff"/></linearGradient></defs>' +
      '<g class="prop" style="transform-origin:50px 17px"><rect x="48" y="16" width="4" height="9" rx="2" fill="' + INK + '"/>' +
      '<ellipse cx="34" cy="14" rx="16" ry="4.5" fill="' + propColors[0] + '"' + strokeAttr(2.2) + '/><ellipse cx="66" cy="14" rx="16" ry="4.5" fill="' + propColors[1] + '"' + strokeAttr(2.2) + '/></g>' +
      '<g fill="url(#' + u + 'g)"' + strokeAttr(3) + '><circle cx="30" cy="60" r="19"/><circle cx="52" cy="46" r="25"/><circle cx="72" cy="60" r="19"/><rect x="30" y="60" width="42" height="19" rx="8" stroke="none"/></g>' +
      '<path d="M22 68 q14 14 30 12 q22 0 30 -14" fill="none" stroke="#bcd8ff" stroke-width="5" opacity=".6" stroke-linecap="round"/>' +
      '<g class="eyes"><ellipse cx="42" cy="54" rx="8" ry="9.5" fill="#fff"' + strokeAttr(2.5) + '/><ellipse cx="62" cy="54" rx="8" ry="9.5" fill="#fff"' + strokeAttr(2.5) + '/>' +
      '<circle cx="43" cy="55" r="4.6" fill="' + INK + '"/><circle cx="63" cy="55" r="4.6" fill="' + INK + '"/><circle cx="45" cy="52" r="1.7" fill="#fff"/><circle cx="65" cy="52" r="1.7" fill="#fff"/></g>' +
      '<ellipse cx="33" cy="66" rx="5" ry="3" fill="#ff7f9d" opacity=".6"/><ellipse cx="71" cy="66" rx="5" ry="3" fill="#ff7f9d" opacity=".6"/>' +
      '<path class="m-idle" d="M46 68 q6 6 12 0" fill="none"' + strokeAttr(2.8) + '/>' +
      '<path class="m-happy" d="M44 66 q8 12 16 0z" fill="#ff7f9d"' + strokeAttr(2.8) + '/>' +
      '<ellipse class="m-think" cx="52" cy="70" rx="3.5" ry="4" fill="#ff7f9d"' + strokeAttr(2.5) + '/>' +
      (HATS[hat] || '') + '</svg>';
  }

  /* ---------------- puzzle pieces ---------------- */
  function shapeSvg(token, size) {
    var parts = String(token).split(':'), kind = parts[0], col = PAL[parts[1]] || PAL.sky, s = size || 56, h = s / 2;
    var inner;
    if (kind === 'circle') inner = '<circle cx="28" cy="28" r="20" fill="' + col + '"' + strokeAttr(3) + '/>';
    else if (kind === 'square') inner = '<rect x="9" y="9" width="38" height="38" rx="6" fill="' + col + '"' + strokeAttr(3) + '/>';
    else if (kind === 'triangle') inner = '<path d="M28 8 L50 47 H6Z" fill="' + col + '"' + strokeAttr(3) + '/>';
    else if (kind === 'star') inner = '<path d="' + starPath(28, 29, 22, 10) + '" fill="' + col + '"' + strokeAttr(3) + '/>';
    else inner = '<path d="M28 6 L50 28 L28 50 L6 28Z" fill="' + col + '"' + strokeAttr(3) + '/>';
    return '<svg viewBox="0 0 56 56" width="' + s + '" height="' + s + '" aria-hidden="true" focusable="false">' + inner + '</svg>';
  }

  function polyPoints(sides, cx, cy, r, rotDeg) {
    var pts = [], i;
    for (i = 0; i < sides; i++) {
      var a = ((rotDeg || 0) * Math.PI) / 180 - Math.PI / 2 + (i * 2 * Math.PI) / sides;
      pts.push((cx + Math.cos(a) * r).toFixed(1) + ',' + (cy + Math.sin(a) * r).toFixed(1));
    }
    return pts.join(' ');
  }

  /** Draw one item of the "shapes" puzzle. Geometry comes from the data so what you see is what is checked. */
  function puzzleShape(item) {
    var col = PAL[item.color] || PAL.sky, f = ' fill="' + col + '"' + strokeAttr(3), vb = '0 0 100 100', body;
    if (item.k === 'poly') {
      var rot = item.rot || (item.sides === 4 ? 45 : 0);
      body = '<polygon points="' + polyPoints(item.sides, 50, 52, item.sides === 4 ? 38 : 40, rot) + '"' + f + '/>';
    } else if (item.k === 'circle') body = '<circle cx="50" cy="50" r="36"' + f + '/>';
    else if (item.k === 'rect' && item.grid) {
      var u = 11, w = item.w * u, h = item.h * u, x0 = (100 - w) / 2, y0 = (100 - h) / 2, g = '', i;
      body = '<rect x="' + x0 + '" y="' + y0 + '" width="' + w + '" height="' + h + '"' + f + '/>';
      for (i = 1; i < item.w; i++) g += 'M' + (x0 + i * u) + ' ' + y0 + ' v' + h;
      for (i = 1; i < item.h; i++) g += 'M' + x0 + ' ' + (y0 + i * u) + ' h' + w;
      body += '<path d="' + g + '" stroke="#fff" stroke-width="1.6" opacity=".85" fill="none"/>';
      vb = '0 0 100 100';
    } else if (item.k === 'rect') {
      var rw = item.w * 18, rh = item.h * 18;
      body = '<rect x="' + (50 - rw / 2) + '" y="' + (50 - rh / 2) + '" width="' + rw + '" height="' + rh + '" rx="4"' + f + '/>';
    } else if (item.k === 'quad') {
      var P = {
        square: '24,24 76,24 76,76 24,76', rhombus: '50,12 84,50 50,88 16,50',
        kite: '50,10 78,40 50,92 22,40', trapezium: '30,28 70,28 90,74 10,74'
      };
      body = '<polygon points="' + P[item.type] + '"' + f + '/>';
    } else body = '';
    return '<svg viewBox="' + vb + '" aria-hidden="true" focusable="false">' + body + '</svg>';
  }

  function coinSvg(value) {
    if (value >= 100) {
      return '<svg viewBox="0 0 100 70" aria-hidden="true" focusable="false"><rect x="6" y="8" width="88" height="54" rx="8" fill="#6fd08c"' + strokeAttr(3) + '/><rect x="14" y="16" width="72" height="38" rx="5" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/>' +
        '<text x="50" y="44" text-anchor="middle" font-size="24" font-weight="900" fill="#fff" stroke="' + INK + '" stroke-width="1.2">RM' + (value / 100) + '</text></svg>';
    }
    return '<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false"><circle cx="50" cy="50" r="40" fill="#ffd45a"' + strokeAttr(3.5) + '/><circle cx="50" cy="50" r="30" fill="none" stroke="#e0a800" stroke-width="3"/>' +
      '<text x="50" y="58" text-anchor="middle" font-size="' + (value >= 10 ? 30 : 34) + '" font-weight="900" fill="' + INK + '">' + value + '</text>' +
      '<text x="50" y="76" text-anchor="middle" font-size="12" font-weight="800" fill="' + INK + '">sen</text></svg>';
  }

  function berrySvg() {
    return '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><circle cx="20" cy="23" r="13" fill="#ff5f86"' + strokeAttr(2.5) + '/><circle cx="15" cy="19" r="3" fill="#fff" opacity=".6"/>' +
      '<path d="M20 11 q-6 -6 -10 -2 q4 6 10 2z M20 11 q6 -6 10 -2 q-4 6 -10 2z" fill="#58c76b"' + strokeAttr(2) + '/></svg>';
  }

  function crateBerries() {
    return '<svg viewBox="0 0 40 24" aria-hidden="true" focusable="false"><circle cx="9" cy="10" r="6" fill="#ff5f86"/><circle cx="20" cy="8" r="6" fill="#ff5f86"/><circle cx="31" cy="10" r="6" fill="#ff5f86"/></svg>';
  }

  function lockSvg() {
    return '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><rect x="8" y="17" width="24" height="19" rx="5" fill="#ffd36b"' + strokeAttr(2.5) + '/><path d="M13 17 v-5 a7 7 0 0 1 14 0 v5" fill="none"' + strokeAttr(3) + '/><circle cx="20" cy="26" r="3" fill="' + INK + '"/></svg>';
  }
  function starSvg(on) {
    return '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><path d="' + starPath(20, 21, 17, 7.5) + '" fill="' + (on ? '#ffc93c' : '#d9d4ea') + '"' + strokeAttr(2.4) + '/></svg>';
  }
  function coinIcon() {
    return '<svg viewBox="0 0 40 40" aria-hidden="true" focusable="false"><circle cx="20" cy="20" r="16" fill="#ffd45a"' + strokeAttr(2.5) + '/><circle cx="20" cy="20" r="10" fill="none" stroke="#e0a800" stroke-width="2"/></svg>';
  }

  /* ---------------- logo + world map art ---------------- */
  function logo() {
    return '<svg class="logo-svg" viewBox="0 0 360 122" role="img" aria-label="Mathipelago"><defs><linearGradient id="lg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6a8"/><stop offset="1" stop-color="#ffb62e"/></linearGradient></defs>' +
      '<g font-family="ui-rounded, \'Arial Rounded MT Bold\', \'Trebuchet MS\', system-ui, sans-serif" font-weight="900" text-anchor="middle">' +
      '<text x="180" y="62" font-size="58" fill="' + INK + '" stroke="' + INK + '" stroke-width="14" stroke-linejoin="round">Mathipelago</text>' +
      '<text x="180" y="62" font-size="58" fill="url(#lg)">Mathipelago</text></g>' +
      '<rect x="78" y="92" width="204" height="24" rx="12" fill="' + INK + '"/><rect x="78" y="92" width="204" height="24" rx="12" fill="none" stroke="#fff" stroke-width="2" opacity=".9"/>' +
      '<text x="180" y="109" font-size="13" font-weight="900" fill="#fff" text-anchor="middle" font-family="ui-rounded, \'Trebuchet MS\', system-ui, sans-serif" letter-spacing="2.5">THE NUMBER ISLANDS</text></svg>';
  }

  /** A smooth, lobed closed path (Catmull-Rom through points around an ellipse). */
  function lobedPath(cx, cy, rx, ry, seed) {
    var N = 18, pts = [], k, a, r, ph1 = (seed * 1.7) % 6.28, ph2 = (seed * 2.9) % 6.28;
    for (k = 0; k < N; k++) {
      a = k / N * Math.PI * 2;
      r = 1 + 0.05 * Math.sin(3 * a + ph1) + 0.035 * Math.sin(5 * a + ph2);
      pts.push([cx + Math.cos(a) * rx * r, cy + Math.sin(a) * ry * r]);
    }
    var d = 'M' + pts[0][0].toFixed(1) + ' ' + pts[0][1].toFixed(1);
    for (k = 0; k < N; k++) {
      var p0 = pts[(k + N - 1) % N], p1 = pts[k], p2 = pts[(k + 1) % N], p3 = pts[(k + 2) % N];
      d += ' C' + (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1) + ' ' + (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1) + ' ' + (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1) + ' ' + (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1) + ' ' + p2[0].toFixed(1) + ' ' + p2[1].toFixed(1);
    }
    return d + 'Z';
  }
  /** A floating island: foam ring, rocky underside, sandy beach rim, grassy top with flowers, then the theme scenery. */
  function islandBlob(x, y, w, h, top, side, deco, seed, rim) {
    var cx = w / 2, cy = h * 0.46, rx = w / 2 - 6, ry = h * 0.43, i, o = '';
    var tuft = ['#fff', '#ffd54a', '#ff8fb3', '#fff'], flowers = '';
    for (i = 0; i < 9; i++) {
      var ang = (i * 40 + seed * 23) % 360 * Math.PI / 180, fx = cx + Math.cos(ang) * rx * 0.8, fy = cy + Math.sin(ang) * ry * 0.8;
      flowers += '<circle cx="' + fx.toFixed(1) + '" cy="' + fy.toFixed(1) + '" r="3.2" fill="' + tuft[i % 4] + '" opacity=".9"/>';
    }
    var xL = cx - rx * 0.88, xR = cx + rx * 0.88, yS = cy + ry * 0.42, yB = h + 18;
    o += '<g transform="translate(' + x + ' ' + y + ')"><g class="islandbob" style="--delay:-' + ((seed % 5) * 0.9).toFixed(1) + 's">';
    o += '<path class="foam" d="' + lobedPath(cx, cy + 4, rx + 10, ry + 8, seed) + '" fill="#fff" opacity=".5"/>';
    o += '<path d="M' + xL + ' ' + yS + ' C' + (xL + 6) + ' ' + (yB - 34) + ' ' + (cx - rx * 0.5) + ' ' + yB + ' ' + cx + ' ' + yB + ' C' + (cx + rx * 0.5) + ' ' + yB + ' ' + (xR - 6) + ' ' + (yB - 34) + ' ' + xR + ' ' + yS + 'Z" fill="' + side + '"' + strokeAttr(3.5) + '/>';
    o += '<path d="M' + (xL + 16) + ' ' + (yS + 18) + ' q' + (rx * 0.5) + ' 14 ' + (rx * 1.5) + ' 0 M' + (xL + 34) + ' ' + (yS + 44) + ' q' + (rx * 0.4) + ' 10 ' + (rx * 1.1) + ' 0" fill="none" stroke="#000" stroke-opacity=".14" stroke-width="5" stroke-linecap="round"/>';
    o += '<path d="' + lobedPath(cx, cy, rx, ry, seed) + '" fill="' + (rim || '#ffe9b0') + '"' + strokeAttr(3.5) + '/>';
    o += '<path d="' + lobedPath(cx, cy, rx * 0.93, ry * 0.93, seed) + '" fill="' + top + '"' + strokeAttr(3) + '/>';
    o += '<path d="' + lobedPath(cx - 6, cy - ry * 0.12, rx * 0.72, ry * 0.7, seed) + '" fill="#fff" opacity=".13"/>';
    o += flowers;
    // scenery scattered down both edges so tall islands do not look empty
    var kinds = ['<circle r="12" fill="#58c76b"' + strokeAttr(2.5) + '/>', '<path d="M-8 6 l8 -18 l8 18z" fill="#3fa65a"' + strokeAttr(2.5) + '/>', '<ellipse rx="11" ry="7" fill="#c9c2d8"' + strokeAttr(2.5) + '/>'];
    for (i = 0; h > 300 && i * 120 + 150 < h - 70; i++) {
      o += '<g transform="translate(' + (30 + (i % 2) * 6) + ' ' + (150 + i * 120) + ')">' + kinds[(seed + i) % 3] + '</g>';
      o += '<g transform="translate(' + (w - 30 - ((i + 1) % 2) * 6) + ' ' + (190 + i * 120) + ')">' + kinds[(seed + i + 1) % 3] + '</g>';
    }
    o += (deco || '') + '</g></g>';
    return o;
  }

  /** Island colours + scenery for the world map (keyed by island id). */
  var THEMES = {
    meadow: { top: '#86e08f', side: '#c08a5c', deco: function () { return berryDeco(); } },
    forest: { top: '#5fcf9a', side: '#9a6a4a', deco: function () { return gearDeco(); } },
    cove: { top: '#ffe7a8', side: '#c9a36a', deco: function () { return coveDeco(); } },
    cave: { top: '#b9a6f2', side: '#7d6bc0', deco: function () { return caveDeco(); } },
    garden: { top: '#b6f09a', side: '#a2784f', deco: function () { return gardenDeco(); } },
    foundry: { top: '#f0b27a', side: '#a2673f', deco: function () { return gearDeco(); } },
    city: { top: '#b4c0ee', side: '#6f7bb0', deco: function () { return cityDeco(); } },
    harbour: { top: '#ffd0b0', side: '#c98a6a', deco: function () { return coveDeco(); } },
    market: { top: '#ffd98a', side: '#c9954a', deco: function () { return marketDeco(); } },
    desert: { top: '#f9e19a', side: '#d8b05a', deco: function () { return desertDeco(); } },
    snow: { top: '#f4fbff', side: '#a9c4e4', deco: function () { return snowDeco(); } },
    reef: { top: '#8de8d8', side: '#3a9fb0', deco: function () { return reefDeco(); } },
    space: { top: '#a894ee', side: '#5a49b0', deco: function () { return spaceDeco(); } },
    volcano: { top: '#ffb27a', side: '#8a4b3a', rim: '#ffd9a8', deco: function () { return volcanoDeco(); } },
    pirate: { top: '#ffe08a', side: '#b8864a', rim: '#fff0b8', deco: function () { return pirateDeco(); } },
    jungle: { top: '#4fd37a', side: '#7a5a3a', rim: '#d8f0a0', deco: function () { return jungleDeco(); } },
    candy: { top: '#ffc2e2', side: '#e089b4', rim: '#fff0f8', deco: function () { return candyDeco(); } },
    dino: { top: '#b8e07a', side: '#a07a4a', rim: '#f2e3b0', deco: function () { return dinoDeco(); } },
    robot: { top: '#c9d6e8', side: '#6b7a99', rim: '#eef3ff', deco: function () { return robotDeco(); } },
    arena: { top: '#7be08a', side: '#5a8a5a', rim: '#e6f6d0', deco: function () { return arenaDeco(); } },
    castle: { top: '#d9d2c4', side: '#8a8478', rim: '#efe9dc', deco: function () { return castleDeco(); } },
    rainbow: { top: '#d8f0ff', side: '#b9a6f2', rim: '#fff8fd', deco: function () { return rainbowDeco(); } },
    carnival: { top: '#ffd0f0', side: '#a05ac0', rim: '#fff0fb', deco: function () { return carnivalDeco(); } },
    kampung: { top: '#c8ee8a', side: '#9a6a3a', rim: '#f0ffd0', deco: function () { return kampungDeco(); } },
    nightmarket: { top: '#ffd0a0', side: '#7a4a6a', rim: '#fff0dc', deco: function () { return nightmarketDeco(); } },
    kites: { top: '#c0f0a0', side: '#8a9a4a', rim: '#f4ffe0', deco: function () { return kitesDeco(); } },
    train: { top: '#d8d8e8', side: '#6a6a82', rim: '#f4f4fc', deco: function () { return trainDeco(); } },
    bakery: { top: '#ffe7c2', side: '#c98a5a', rim: '#fff8ec', deco: function () { return bakeryDeco(); } },
    deep: { top: '#6ad0e8', side: '#2a6a9a', rim: '#c8f4ff', deco: function () { return deepDeco(); } },
    zoo: { top: '#b8f090', side: '#7a6a3a', rim: '#f0ffd8', deco: function () { return zooDeco(); } },
    toys: { top: '#ffd0e8', side: '#c98a6a', rim: '#fff0f8', deco: function () { return toysDeco(); } },
    treehouse: { top: '#9ae070', side: '#7a5a3a', rim: '#e8ffd0', deco: function () { return treehouseDeco(); } },
    festival: { top: '#ffd0a0', side: '#a04a5a', rim: '#fff0dc', deco: function () { return festivalDeco(); } }
  };
  function kampungDeco() { return '<g transform="translate(30 10) scale(.75)"><path d="M120 170 v-50 h110 v50z" fill="#c9954a"' + strokeAttr(3) + '/><path d="M108 120 l67 -44 l67 44z" fill="#a0522d"' + strokeAttr(3) + '/><rect x="160" y="136" width="26" height="34" fill="#6a4a2a"/><path d="M300 170 v-60 M300 110 q-26 -10 -30 -34 M300 110 q26 -10 30 -34" stroke="#4fa84f" stroke-width="6" fill="none"/></g>'; }
  function nightmarketDeco() { return '<g transform="translate(30 10) scale(.75)"><path d="M40 120 h90 l-10 -30 h-70z" fill="#ff6f61"' + strokeAttr(3) + '/><path d="M250 120 h90 l-10 -30 h-70z" fill="#ffd54a"' + strokeAttr(3) + '/><circle cx="190" cy="60" r="10" fill="#ffd54a"/><circle cx="160" cy="76" r="8" fill="#ff9a3a"/><circle cx="222" cy="76" r="8" fill="#ff6f61"/></g>'; }
  function kitesDeco() { return '<g transform="translate(30 10) scale(.75)"><path d="M100 40 l26 30 l-26 36 l-26 -36z" fill="#ff6f61"' + strokeAttr(3) + '/><path d="M280 60 l22 24 l-22 30 l-22 -30z" fill="#ffd54a"' + strokeAttr(3) + '/><path d="M100 106 q-20 30 0 60 M280 114 q20 24 0 54" stroke="#2b2350" stroke-width="2" fill="none"/></g>'; }
  function trainDeco() { return '<g transform="translate(30 10) scale(.75)"><path d="M20 170 h360" stroke="#5a4a3a" stroke-width="6"/><rect x="110" y="110" width="100" height="46" rx="8" fill="#ff6f61"' + strokeAttr(3) + '/><rect x="210" y="90" width="50" height="66" rx="6" fill="#5fb8ff"' + strokeAttr(3) + '/><circle cx="135" cy="162" r="10" fill="#2b2350"/><circle cx="235" cy="162" r="10" fill="#2b2350"/><circle cx="130" cy="80" r="10" fill="#fff" opacity=".8"/></g>'; }
  function bakeryDeco() { return '<g transform="translate(30 10) scale(.75)"><rect x="120" y="90" width="150" height="80" rx="10" fill="#ffd9a8"' + strokeAttr(3) + '/><path d="M110 90 q85 -60 170 0z" fill="#e8683a"' + strokeAttr(3) + '/><rect x="176" y="120" width="40" height="50" rx="6" fill="#8a5a3a"/></g>'; }
  function deepDeco() { return '<g transform="translate(30 10) scale(.75)"><circle cx="90" cy="70" r="12" fill="#fff" opacity=".5"/><circle cx="110" cy="100" r="7" fill="#fff" opacity=".5"/><path d="M240 160 q10 -60 30 -80 q4 40 -2 80z" fill="#ff8ab8"' + strokeAttr(3) + '/><ellipse cx="320" cy="120" rx="26" ry="14" fill="#ffd54a"' + strokeAttr(3) + '/></g>'; }
  function zooDeco() { return '<g transform="translate(30 10) scale(.75)"><rect x="70" y="100" width="90" height="70" fill="#c9954a"' + strokeAttr(3) + '/><path d="M60 100 h110 l-55 -34z" fill="#ff6f61"' + strokeAttr(3) + '/><path d="M250 170 v-70 M250 100 q-24 -24 -4 -44 M250 100 q24 -24 4 -44" stroke="#4fa84f" stroke-width="7" fill="none"/></g>'; }
  function toysDeco() { return '<g transform="translate(30 10) scale(.75)"><rect x="90" y="110" width="60" height="60" rx="6" fill="#ff6f61"' + strokeAttr(3) + '/><rect x="164" y="90" width="60" height="80" rx="6" fill="#5fb8ff"' + strokeAttr(3) + '/><rect x="238" y="124" width="50" height="46" rx="6" fill="#ffd54a"' + strokeAttr(3) + '/><circle cx="120" cy="140" r="9" fill="#fff"/><circle cx="194" cy="130" r="9" fill="#fff"/></g>'; }
  function treehouseDeco() { return '<g transform="translate(30 10) scale(.75)"><rect x="170" y="90" width="44" height="80" fill="#7a5a3a"' + strokeAttr(3) + '/><circle cx="192" cy="70" r="52" fill="#3fa84f"' + strokeAttr(3) + '/><rect x="164" y="60" width="56" height="36" rx="5" fill="#d8a060"' + strokeAttr(3) + '/><path d="M158 60 l34 -24 l34 24z" fill="#ff6f61"' + strokeAttr(3) + '/></g>'; }
  function festivalDeco() { return '<g transform="translate(30 10) scale(.75)"><path d="M40 40 q150 40 320 0" fill="none" stroke="#2b2350" stroke-width="3"/><ellipse cx="100" cy="68" rx="16" ry="20" fill="#ff6f61"' + strokeAttr(3) + '/><ellipse cx="190" cy="76" rx="16" ry="20" fill="#ffd54a"' + strokeAttr(3) + '/><ellipse cx="280" cy="68" rx="16" ry="20" fill="#ff6f61"' + strokeAttr(3) + '/></g>'; }
  function cityDeco() { return '<g><rect x="50" y="30" width="30" height="60" rx="3" fill="#8f9fd8"' + strokeAttr(3) + '/><rect x="94" y="48" width="26" height="42" rx="3" fill="#a9b6e6"' + strokeAttr(3) + '/><rect x="270" y="24" width="34" height="66" rx="3" fill="#8f9fd8"' + strokeAttr(3) + '/><rect x="150" y="56" width="22" height="34" rx="3" fill="#a9b6e6"' + strokeAttr(3) + '/></g>'; }
  function marketDeco() { return '<g><path d="M44 80 h58 l-6 -26 h-46z" fill="#ff6f61"' + strokeAttr(3) + '/><path d="M268 80 h58 l-6 -26 h-46z" fill="#5fb8ff"' + strokeAttr(3) + '/><circle cx="160" cy="70" r="12" fill="#ffb12e"' + strokeAttr(3) + '/></g>'; }
  function desertDeco() { return '<g><rect x="60" y="36" width="14" height="50" rx="7" fill="#58c76b"' + strokeAttr(3) + '/><path d="M60 58 q-14 0 -14 -14" stroke="#2f8f4f" stroke-width="8" fill="none" stroke-linecap="round"/><path d="M250 86 q30 -50 66 0z" fill="#f5d27a"' + strokeAttr(3) + '/></g>'; }
  function snowDeco() { return '<g><path d="M40 90 L84 28 L128 90Z" fill="#9ab8e0"' + strokeAttr(3) + '/><path d="M70 50 L84 28 L98 50 L88 46 L84 54 L78 46Z" fill="#fff"/><path d="M262 90 L300 34 L338 90Z" fill="#86a6d6"' + strokeAttr(3) + '/></g>'; }
  function reefDeco() { return '<g><path d="M56 88 q-10 -40 6 -60 q8 24 -2 60z" fill="#ff8fa3"' + strokeAttr(3) + '/><path d="M284 88 q-8 -36 8 -56 q8 22 -2 56z" fill="#ffb86b"' + strokeAttr(3) + '/><circle cx="150" cy="52" r="9" fill="none" stroke="#fff" stroke-width="3"/></g>'; }
  function spaceDeco() { return '<g><circle cx="70" cy="56" r="20" fill="#ff9f7a"' + strokeAttr(3) + '/><ellipse cx="70" cy="58" rx="32" ry="7" fill="none" stroke="#ffd9c0" stroke-width="4"/><path d="M290 80 l8 -40 l8 40z" fill="#fff"' + strokeAttr(3) + '/><circle cx="298" cy="34" r="6" fill="#ffd54a"' + strokeAttr(2.5) + '/></g>'; }

  function volcanoDeco() { return '<g><path d="M120 92 L170 18 L220 92Z" fill="#8a5a4a"' + strokeAttr(3) + '/><path d="M158 24 L170 12 L184 26 Q170 40 158 24Z" fill="#ff6f3c"/><path d="M170 28 q-4 30 -14 50" stroke="#ff8f3c" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="188" cy="2" r="9" fill="#fff" opacity=".7"/><circle cx="64" cy="70" r="14" fill="#ff8f3c"' + strokeAttr(3) + '/></g>'; }
  function pirateDeco() { return '<g><path d="M58 86 q-4 -44 18 -58 q6 24 0 58z" fill="#58c76b"' + strokeAttr(3) + '/><rect x="62" y="70" width="8" height="22" rx="3" fill="#8a5a3a"/><rect x="262" y="52" width="48" height="36" rx="6" fill="#b9733a"' + strokeAttr(3) + '/><rect x="280" y="64" width="12" height="12" rx="3" fill="#ffd36b"' + strokeAttr(2.5) + '/><rect x="150" y="14" width="4" height="64" fill="#5a3a22"/><path d="M154 16 h32 v22 h-32z" fill="#2b2350"/><circle cx="170" cy="27" r="5" fill="#fff"/></g>'; }
  function jungleDeco() { return '<g><rect x="56" y="40" width="12" height="50" rx="5" fill="#8a5a3a"' + strokeAttr(3) + '/><circle cx="62" cy="34" r="28" fill="#35c46a"' + strokeAttr(3) + '/><circle cx="300" cy="46" r="22" fill="#4fd37a"' + strokeAttr(3) + '/><rect x="294" y="60" width="10" height="30" rx="4" fill="#8a5a3a"/><circle cx="160" cy="44" r="8" fill="#ff5f5f"' + strokeAttr(2.5) + '/><path d="M150 44 l-12 -6 l8 10z" fill="#ffd54a"/></g>'; }
  function candyDeco() { return '<g><path d="M60 92 V44" stroke="#fff" stroke-width="7"' + '/><circle cx="60" cy="32" r="22" fill="#ff6fa8"' + strokeAttr(3) + '/><path d="M46 32 a14 14 0 0 1 28 0" fill="none" stroke="#fff" stroke-width="5"/><path d="M296 92 V50 q0 -24 22 -24" stroke="#ff4f7a" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M296 84 v-6 M296 66 v-6" stroke="#fff" stroke-width="9"/><circle cx="170" cy="60" r="14" fill="#ffd0a8"' + strokeAttr(3) + '/><circle cx="170" cy="48" r="9" fill="#fff"' + strokeAttr(2.5) + '/></g>'; }
  function dinoDeco() { return '<g><ellipse cx="80" cy="74" rx="34" ry="20" fill="#6fcf6a"' + strokeAttr(3) + '/><path d="M104 64 q30 -34 36 -58 q18 4 12 18 q-6 24 -24 54z" fill="#6fcf6a"' + strokeAttr(3) + '/><circle cx="144" cy="12" r="3" fill="#2b2350"/><path d="M270 92 q-6 -40 16 -52 q22 12 16 52z" fill="#fff6e0"' + strokeAttr(3) + '/><circle cx="284" cy="62" r="4" fill="#ff9f7a"/><circle cx="278" cy="76" r="3" fill="#ff9f7a"/></g>'; }
  function robotDeco() { return '<g><path class="gear cw slow" d="' + gearPath(60, 62, 22, 9) + '" fill="#ffd36b"' + strokeAttr(3) + '/><rect x="250" y="30" width="56" height="62" rx="10" fill="#aab8d8"' + strokeAttr(3) + '/><circle cx="266" cy="54" r="7" fill="#fff"/><circle cx="290" cy="54" r="7" fill="#fff"/><path d="M278 30 v-14" stroke="#2b2350" stroke-width="4"/><circle cx="278" cy="12" r="6" fill="#ff6f61"/></g>'; }
  function arenaDeco() { return '<g><path d="M50 90 V44 H112 V90" fill="none" stroke="#fff" stroke-width="6"' + '/><path d="M50 56 H112 M50 68 H112" stroke="#fff" stroke-width="2" opacity=".7"/><circle cx="290" cy="72" r="16" fill="#fff"' + strokeAttr(3) + '/><path d="M290 60 l8 8 l-3 10 h-10 l-3 -10z" fill="#2b2350"/><path d="M160 90 V30" stroke="#8a5a3a" stroke-width="5"/><path d="M160 30 l30 10 l-30 10z" fill="#ff6f61"' + strokeAttr(2.5) + '/></g>'; }
  function castleDeco() { return '<g><rect x="130" y="38" width="100" height="56" fill="#cfcfdc"' + strokeAttr(3) + '/><rect x="116" y="22" width="26" height="72" fill="#bdbdd0"' + strokeAttr(3) + '/><rect x="218" y="22" width="26" height="72" fill="#bdbdd0"' + strokeAttr(3) + '/><path d="M116 22 l13 -20 l13 20z M218 22 l13 -20 l13 20z" fill="#ff6f61"' + strokeAttr(3) + '/><path d="M160 94 v-22 a20 20 0 0 1 40 0 v22z" fill="#6a5a8a"' + strokeAttr(2.5) + '/></g>'; }
  function rainbowDeco() { return '<g>' + ['#ff6f61', '#ffc93c', '#7de08f', '#5fb8ff'].map(function (c, i) { return '<path d="M' + (90 + i * 9) + ' 92 a' + (90 - i * 9) + ' ' + (70 - i * 9) + ' 0 0 1 ' + (2 * (90 - i * 9)) + ' 0" fill="none" stroke="' + c + '" stroke-width="9"/>'; }).join('') + '<circle cx="76" cy="84" r="14" fill="#fff"' + strokeAttr(3) + '/><circle cx="294" cy="84" r="14" fill="#fff"' + strokeAttr(3) + '/></g>'; }
  function carnivalDeco() { return '<g><path d="M60 92 l30 -64 l30 64z" fill="#ff6f61"' + strokeAttr(3) + '/><path d="M76 92 l14 -64 l14 64z" fill="#fff"/><circle cx="280" cy="52" r="34" fill="none" stroke="#ffd54a" stroke-width="6"/><path d="M280 18 v68 M246 52 h68" stroke="#ffd54a" stroke-width="3"/><path d="M170 80 v-30" stroke="#2b2350" stroke-width="3"/><ellipse cx="170" cy="40" rx="12" ry="15" fill="#5fb8ff"' + strokeAttr(2.5) + '/></g>'; }

  /**
   * The whole archipelago. layout = [{ y, h, theme }] (island 0 is the lowest); H = total height of the 400-wide map.
   * Level buttons are HTML laid over it by app.js.
   */
  function worldMap(layout, H) {
    var out = '<defs><linearGradient id="mapsea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fdcff"/><stop offset=".55" stop-color="#4fb9ec"/><stop offset="1" stop-color="#2a8fd0"/></linearGradient>' +
      '<linearGradient id="mapfog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e3ff"/><stop offset="1" stop-color="#e9e3ff" stop-opacity="0"/></linearGradient></defs>' +
      '<rect width="400" height="' + H + '" fill="url(#mapsea)"/>';
    var i;
    for (i = 0; i < Math.floor(H / 92); i++) {
      var wy = 60 + i * 92, wx = (i * 83) % 330 + 20;
      out += '<path class="waves" d="M' + wx + ' ' + wy + ' q10 -7 20 0 t20 0 t20 0" fill="none" stroke="#d6f4ff" stroke-width="3" stroke-linecap="round" opacity=".6"/>';
    }
    layout.forEach(function (it, n) {
      var th = THEMES[it.theme] || THEMES.meadow;
      out += islandBlob(30, it.y, 340, it.h, th.top, th.side, th.deco(), n + 1, th.rim);
    });
    return out;
  }
  function berryDeco() {
    return '<g><circle cx="52" cy="70" r="17" fill="#58c76b"' + strokeAttr(3) + '/><circle cx="46" cy="64" r="5" fill="#ff5f86"/><circle cx="58" cy="76" r="5" fill="#ff5f86"/>' +
      '<circle cx="292" cy="62" r="19" fill="#58c76b"' + strokeAttr(3) + '/><circle cx="286" cy="56" r="5" fill="#ff5f86"/><circle cx="298" cy="68" r="5" fill="#ff5f86"/>' +
      '<path d="M150 56 q10 -20 20 0z" fill="#fff"' + strokeAttr(2.5) + '/></g>';
  }
  function gearDeco() {
    return '<g><path class="gear cw slow" d="' + gearPath(60, 66, 20, 9) + '" fill="#ffd36b"' + strokeAttr(3) + '/><path class="gear ccw slow" d="' + gearPath(286, 60, 16, 8) + '" fill="#ff8f6b"' + strokeAttr(3) + '/>' +
      '<rect x="150" y="30" width="16" height="44" rx="6" fill="#9a6a4a"' + strokeAttr(3) + '/><circle cx="158" cy="30" r="20" fill="#3fbf9a"' + strokeAttr(3) + '/></g>';
  }
  function coveDeco() {
    return '<g><path d="M56 80 q-4 -40 20 -54 q4 24 -2 54z" fill="#58c76b"' + strokeAttr(3) + '/><rect x="62" y="70" width="8" height="20" rx="3" fill="#9a6a4a"/>' +
      '<path d="M270 80 l12 -38 h16 l12 38z" fill="#fff6e0"' + strokeAttr(3) + '/><path d="M274 62 h32" stroke="#ff6f61" stroke-width="7"/><circle cx="290" cy="36" r="6" fill="#ffd54a"' + strokeAttr(2.5) + '/></g>';
  }
  function caveDeco() {
    return '<g><path d="M52 84 l-14 -44 l16 -14 l16 14z" fill="#ff9ff3"' + strokeAttr(3) + '/><path d="M96 84 l-8 -30 l12 -10 l12 10z" fill="#9fe0ff"' + strokeAttr(3) + '/>' +
      '<path d="M276 84 l-14 -48 l18 -16 l18 16z" fill="#c9a0ff"' + strokeAttr(3) + '/><path d="M150 70 l8 -26 l8 26z" fill="#7de0c8"' + strokeAttr(3) + '/></g>';
  }
  function gardenDeco() {
    return '<g><circle cx="60" cy="64" r="16" fill="#ff7f9d"' + strokeAttr(3) + '/><circle cx="60" cy="64" r="6" fill="#fff6a0"/><path d="M60 80 v14" stroke="#2f8f4f" stroke-width="5"/>' +
      '<circle cx="290" cy="58" r="18" fill="#ffd54a"' + strokeAttr(3) + '/><circle cx="290" cy="58" r="7" fill="#ff9f43"/><path d="M290 76 v16" stroke="#2f8f4f" stroke-width="5"/>' +
      '<path d="M150 80 q-6 -40 20 -50 q18 14 6 50z" fill="#58c76b"' + strokeAttr(3) + '/></g>';
  }

  function toastIcon() { return starSvg(true); }

  MP.art = {
    INK: INK, PAL: PAL,
    scene: scene, setProgress: setProgress, setVar: setVar, setText: setText, setDone: setDone,
    cloudSvg: function () { return '<svg viewBox="-44 -24 88 48" aria-hidden="true" focusable="false"><ellipse cx="0" cy="8" rx="32" ry="11" fill="#fff"/><circle cx="-13" cy="0" r="12" fill="#fff"/><circle cx="6" cy="-6" r="16" fill="#fff"/><circle cx="22" cy="3" r="10" fill="#fff"/></svg>'; }, creature: creature, npc: npc, TINTS: TINTS, PAL_ACCS: PAL_ACCS, avatarIds: function () { return ['nimbo'].concat(Object.keys(NPCS)); }, avatar: function (id, cls) { return id === 'nimbo' || !NPCS[id] ? nimbo({ mood: 'happy', cls: cls }) : npc(id, { cls: cls }); }, nimbo: nimbo, hats: Object.keys(HATS),
    shape: shapeSvg, puzzleShape: puzzleShape, coin: coinSvg, berry: berrySvg, crateBerries: crateBerries,
    lock: lockSvg, star: starSvg, coinIcon: coinIcon, logo: logo, worldMap: worldMap, toastIcon: toastIcon,
    gearPath: gearPath, starPath: starPath
  };
})();
