/*
 * streak.js — daily login streak. Pure functions (unit tested); the screens live in app.js.
 *
 * A "week" is 7 days in a row. Each day pays more than the day before; claiming day 7 of an unbroken week
 * also pays a PERFECT WEEK bonus. Missing a day starts again at day 1. After day 7 the next login starts a new week.
 * Dates are the player's LOCAL calendar days, written 'YYYY-MM-DD'. No network, no clock tricks needed.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  var REWARDS = [5, 10, 15, 20, 30, 40, 50];   // coins for day 1..7
  var PERFECT_BONUS = 100;                      // extra coins for finishing all 7 days without a miss

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function dayKey(d) { d = d || new Date(); return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
  function dayNum(key) {                         // whole days since 1970-01-01 for 'YYYY-MM-DD' (timezone-proof)
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(key));
    if (!m) return null;
    return Math.round(Date.UTC(+m[1], +m[2] - 1, +m[3]) / 86400000);
  }
  function blank() { return { day: 0, last: null, best: 0, weeks: 0, total: 0, run: 0 }; }
  var MAX_FREEZES = 2;

  /** What would happen if the player claims today? Does not change anything. */
  function status(st, today, freezes) {
    st = st || blank(); freezes = freezes || 0;
    var t = dayNum(today), l = dayNum(st.last);
    var out = { state: 'claimable', day: 1, reward: REWARDS[0], bonus: 0, broken: false, current: 0, saved: 0 };
    if (l !== null && t !== null) {
      var gap = t - l;
      if (gap <= 0) {                           // already claimed today (or the clock went backwards: never punish that)
        return { state: 'claimed', day: st.day, reward: 0, bonus: 0, broken: false, current: st.day };
      }
      if (gap === 1) out.day = st.day >= 7 ? 1 : st.day + 1;
      else if (st.day > 0 && freezes >= gap - 1) { out.day = st.day >= 7 ? 1 : st.day + 1; out.saved = gap - 1; }   // a streak freeze covers each missed day
      else { out.day = 1; out.broken = st.day > 0; }
    }
    out.current = out.day - 1;                  // days already banked in the running week
    out.reward = REWARDS[out.day - 1];
    out.bonus = out.day === 7 ? PERFECT_BONUS : 0;
    return out;
  }

  /** Claim today's reward. Returns {st, coins, reward, bonus, day, perfect} — or null if already claimed. */
  function claim(st, today, freezes) {
    st = st || blank();
    var s = status(st, today, freezes);
    if (s.state !== 'claimable') return null;
    var n = {
      day: s.day, last: today, best: Math.max(st.best || 0, s.day),
      weeks: (st.weeks || 0) + (s.day === 7 ? 1 : 0), total: (st.total || 0) + 1,
      run: s.broken || !st.last ? 1 : (st.run || st.day || 0) + 1 + s.saved
    };
    return { st: n, coins: s.reward + s.bonus, reward: s.reward, bonus: s.bonus, day: s.day, perfect: s.day === 7, restarted: s.broken, used: s.saved };
  }

  /** The flame number: how many days in a row, whether it is already safe today, and whether it is still alive at all. */
  function count(st, today, freezes) {
    st = st || blank();
    var t = dayNum(today), l = dayNum(st.last);
    if (l === null || t === null || !st.day) return { n: 0, safe: false, alive: false };
    var gap = t - l, run = st.run || st.day;
    if (gap <= 0) return { n: run, safe: true, alive: true };
    if (gap === 1 || (freezes || 0) >= gap - 1) return { n: run, safe: false, alive: true };
    return { n: 0, safe: false, alive: false };
  }

  MP.streak = { MAX_FREEZES: MAX_FREEZES, count: count, REWARDS: REWARDS, PERFECT_BONUS: PERFECT_BONUS, dayKey: dayKey, dayNum: dayNum, blank: blank, status: status, claim: claim };
})();
