/*
 * audio.js — tiny synthesised sound effects and a playful background tune (no audio files to download).
 * Everything is optional: if the browser has no Web Audio, or the sound toggle is off,
 * calls silently do nothing and the game remains fully playable.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  var ctx = null, enabled = true, broken = false;
  var musicOn = true, musicVol = 60, ducked = false, musicGain = null, timer = null, nextT = 0, stepNo = 0, noiseBuf = null;

  var unlocked = false;
  function resumeCtx() {
    if (!ctx || document.hidden) return;   // a hidden page stays quiet; the visibility handler wakes it later
    // 'suspended' = autoplay policy or tab hidden; 'interrupted' = iOS (phone call, lock screen, silent switch change)
    if (ctx.state === 'running') return;
    try { var p = ctx.resume(); if (p && p.catch) p.catch(function () { /* needs a gesture; the next tap retries */ }); } catch (e) { /* ignore */ }
  }
  function silentBlip() {
    // iOS only starts audio output after something is actually played inside a user gesture.
    try { var b = ctx.createBuffer(1, 1, 22050), s = ctx.createBufferSource(); s.buffer = b; s.connect(ctx.destination); s.start(0); } catch (e) { /* ignore */ }
  }
  function ensureCtx() {
    if (broken) return null;
    if (!ctx) {
      try {
        var AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) { broken = true; return null; }
        ctx = new AC();
        ctx.onstatechange = function () {
          if (ctx.state === 'running') {
            nextT = ctx.currentTime + 0.1;   // never replay the notes that piled up while we were away
            if (musicOn && musicGain) { applyVolume(); if (!timer) timer = setInterval(tick, 90); }
          } else if (ctx.state === 'interrupted' || (ctx.state === 'suspended' && !document.hidden)) {
            resumeCtx();
          }
        };
      } catch (e) { broken = true; return null; }
    }
    if (ctx.state !== 'running') resumeCtx();
    return ctx;
  }
  function ensure() { return enabled ? ensureCtx() : null; }

  function tone(freq, start, dur, type, vol) {
    var c = ensure(); if (!c) return;
    if (c.state !== 'running') {
      // try once more a moment later (resume is asynchronous); drop it if still silent so sounds never pile up
      var again = c; setTimeout(function () { if (again.state === 'running' && enabled) tone(freq, start, dur, type, vol); }, 120);
      return;
    }
    try {
      var o = c.createOscillator(), g = c.createGain(), t0 = c.currentTime + start;
      o.type = type || 'sine';
      o.frequency.setValueAtTime(freq, t0);
      g.gain.setValueAtTime(0.0001, t0);
      g.gain.exponentialRampToValueAtTime(vol || 0.15, t0 + 0.012);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
      o.connect(g); g.connect(c.destination);
      o.start(t0); o.stop(t0 + dur + 0.05);
    } catch (e) { /* ignore */ }
  }


  /* ---------------- background music: a bouncy little loop, scheduled a moment ahead ---------------- */
  var MS = 60 / 112 / 2;                     // one eighth note at 112 bpm
  var CHORDS = [[48], [45], [41], [43]];   // bass root per bar of the I - vi - IV - V loop
  var CH_TYPE = [4, 3, 4, 4];   // third above the root: 4 = major, 3 = minor
  var MEL = [
    [76, 0, 79, 76, 74, 0, 72, 0], [72, 0, 76, 79, 81, 0, 79, 0], [77, 0, 76, 72, 74, 0, 77, 0], [79, 0, 76, 74, 71, 0, 74, 0],
    [79, 81, 79, 76, 79, 0, 84, 0], [81, 0, 79, 76, 72, 0, 76, 0], [77, 79, 81, 79, 77, 0, 72, 0], [74, 76, 79, 0, 83, 81, 79, 0]
  ];
  function hz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
  function mtone(freq, t0, dur, type, vol) {
    try {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type; o.frequency.setValueAtTime(freq, t0);
      g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(vol, t0 + 0.015); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
      o.connect(g); g.connect(musicGain); o.start(t0); o.stop(t0 + dur + 0.05);
    } catch (e) { /* ignore */ }
  }
  function noise(t0, dur, vol, hp) {
    try {
      if (!noiseBuf) { noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 0.3, ctx.sampleRate); var d = noiseBuf.getChannelData(0); for (var i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; }
      var src = ctx.createBufferSource(), f = ctx.createBiquadFilter(), g = ctx.createGain();
      src.buffer = noiseBuf; f.type = 'highpass'; f.frequency.value = hp;
      g.gain.setValueAtTime(vol, t0); g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
      src.connect(f); f.connect(g); g.connect(musicGain); src.start(t0); src.stop(t0 + dur + 0.02);
    } catch (e) { /* ignore */ }
  }
  function kick(t0) {
    try {
      var o = ctx.createOscillator(), g = ctx.createGain();
      o.frequency.setValueAtTime(130, t0); o.frequency.exponentialRampToValueAtTime(48, t0 + 0.12);
      g.gain.setValueAtTime(0.32, t0); g.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.16);
      o.connect(g); g.connect(musicGain); o.start(t0); o.stop(t0 + 0.2);
    } catch (e) { /* ignore */ }
  }
  function scheduleStep(n, t0) {
    var bar = Math.floor(n / 8) % 8, st = n % 8, ch = CHORDS[bar % 4], third = CH_TYPE[bar % 4], root = ch[0];
    var m = MEL[bar][st];
    if (m) { mtone(hz(m), t0, MS * 1.7, 'triangle', 0.22); mtone(hz(m + 12), t0, MS * 0.9, 'sine', 0.06); }
    if (st === 0 || st === 3 || st === 4 || st === 7) mtone(hz(st === 3 || st === 7 ? root + 7 : root), t0, MS * 1.5, 'sine', 0.34);   // bouncy bass
    if (st === 2 || st === 6) { [root + 24, root + 24 + third, root + 31].forEach(function (x) { mtone(hz(x), t0, MS * 0.8, 'triangle', 0.07); }); }
    if (st === 0 || st === 4) kick(t0);
    if (st === 2 || st === 6) noise(t0, 0.09, 0.07, 1800);
    if (st % 2 === 1) noise(t0, 0.03, 0.035, 6500);
  }
  function tick() {
    if (!ctx || !musicOn) return;
    if (ctx.state !== 'running') { resumeCtx(); nextT = 0; return; }
    if (nextT < ctx.currentTime - 0.1) nextT = ctx.currentTime + 0.05;   // fell behind (tab throttled): restart the beat, no burst
    while (nextT < ctx.currentTime + 0.35) { scheduleStep(stepNo, Math.max(nextT, ctx.currentTime + 0.02)); nextT += MS; stepNo++; }
  }
  function applyVolume() {
    if (!ctx || !musicGain) return;
    var v = (musicVol / 100); v = v * v * 0.5 * (ducked ? 0.55 : 1);
    try { musicGain.gain.setTargetAtTime(musicOn ? v : 0, ctx.currentTime, 0.08); } catch (e) { /* ignore */ }
  }
  function startMusic() {
    if (!musicOn || broken) return;
    var c = ensureCtx(); if (!c) return;
    if (!musicGain) { musicGain = c.createGain(); musicGain.gain.value = 0; musicGain.connect(c.destination); }
    applyVolume();
    if (!timer) { nextT = c.currentTime + 0.1; timer = setInterval(tick, 90); }
    if (c.state !== 'running') resumeCtx();
  }
  function stopMusic() {
    if (timer) { clearInterval(timer); timer = null; }
    applyVolume();
  }

  var SOUNDS = {
    tap:    function () { tone(620, 0, 0.07, 'sine', 0.10); },
    select: function () { tone(520, 0, 0.06, 'triangle', 0.12); tone(780, 0.05, 0.08, 'triangle', 0.10); },
    place:  function () { tone(330, 0, 0.09, 'triangle', 0.14); },
    // wrong answers are deliberately soft and gentle — never a harsh buzzer
    nope:   function () { tone(300, 0, 0.14, 'sine', 0.09); tone(250, 0.12, 0.18, 'sine', 0.08); },
    ok:     function () { tone(523, 0, 0.12, 'triangle', 0.14); tone(659, 0.09, 0.12, 'triangle', 0.14); tone(784, 0.18, 0.2, 'triangle', 0.14); },
    coin:   function () { tone(988, 0, 0.07, 'square', 0.05); tone(1319, 0.07, 0.14, 'square', 0.05); },
    win:    function () {
      [523, 659, 784, 1047, 784, 1047, 1319].forEach(function (f, i) { tone(f, i * 0.1, 0.22, 'triangle', 0.14); });
    },
    unlock: function () { tone(392, 0, 0.1, 'sine', 0.12); tone(587, 0.1, 0.1, 'sine', 0.12); tone(880, 0.2, 0.25, 'sine', 0.12); },
    chest: function () { [523, 659, 784, 1047, 1319].forEach(function (f, k) { tone(f, k * 0.07, 0.16, 'sine', 0.1); }); },
    whoosh: function () { tone(200, 0, 0.25, 'sawtooth', 0.03); tone(400, 0.05, 0.2, 'sawtooth', 0.02); }
  };

  var hapticsOn = true;
  var BUZZ = { ok: [18], nope: [14, 50, 14], win: [20, 40, 20, 40, 70], unlock: [16], coin: [10], chest: [30, 40, 20, 40, 20, 40, 80] };
  function buzz(name) {
    var pat = BUZZ[name];
    if (pat && hapticsOn && typeof navigator !== 'undefined' && navigator.vibrate && !document.hidden) { try { navigator.vibrate(pat); } catch (e) { /* ignore */ } }
  }

  MP.audio = {
    setEnabled: function (on) { enabled = !!on; },
    isEnabled: function () { return enabled; },
    /** Background music: on/off and volume 0..100. It starts after the first tap (browsers do not allow sound before). */
    setMusic: function (on, vol) {
      musicOn = !!on; musicVol = Math.max(0, Math.min(100, Math.round(Number(vol)))); if (!isFinite(musicVol)) musicVol = 60;
      if (musicOn) { if (ctx) startMusic(); else applyVolume(); } else stopMusic();
    },
    musicState: function () { return { on: musicOn, volume: musicVol, playing: !!timer }; },
    /** Softer while a puzzle is open so it never competes with thinking. */
    setDuck: function (d) { ducked = !!d; applyVolume(); },
    /** Call from a user gesture (first tap) so mobile browsers allow sound. */
    unlock: function () { var c = ensureCtx(); if (c) { silentBlip(); unlocked = true; } if (musicOn && !timer) startMusic(); },
    state: function () { return ctx ? ctx.state : 'none'; },
    play: function (name) { buzz(name); var f = SOUNDS[name]; if (f && enabled) f(); },
    /** Phone vibration (Android browsers; iPhones ignore it). Only for answers and rewards, never for plain taps. */
    setHaptics: function (on) { hapticsOn = !!on; },
    buzz: buzz
  };

  // Any tap, key press or touch anywhere re-wakes a sleeping audio engine (the usual cause of "sound sometimes stops").
  function wake() {
    if (broken) return;
    if (!ctx) { if (enabled || musicOn) MP.audio.unlock(); return; }
    if (ctx.state !== 'running') { resumeCtx(); silentBlip(); }
    if (musicOn && !timer && musicGain) startMusic();
  }
  ['pointerdown', 'touchend', 'keydown', 'click'].forEach(function (ev) { document.addEventListener(ev, wake, { capture: true, passive: true }); });

  document.addEventListener('visibilitychange', function () {
    if (!ctx) return;
    try { if (document.hidden) ctx.suspend(); else { resumeCtx(); nextT = ctx.currentTime + 0.1; } } catch (e) { /* ignore */ }
  });
  window.addEventListener('pageshow', function () { if (ctx) { resumeCtx(); } });
  window.addEventListener('focus', function () { if (ctx) resumeCtx(); });
})();
