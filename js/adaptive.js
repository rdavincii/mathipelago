/*
 * adaptive.js — local, predictable, explainable difficulty.
 *
 * Every level has three AUTHORED puzzles ("tiers"): 0 friendly, 1 standard, 2 challenge.
 *
 *   tier = clamp(startingBand + topicAdjustment, 0, 2)
 *
 * startingBand      the rank the child (or parent) chose: Explorer 0, Adventurer 1, Master Explorer 2.
 * topicAdjustment   -1, 0 or +1, remembered per maths topic (never a label for the child):
 *     • two "clean" solves in a row in a topic (no mistakes, no hints)  -> +1 (one step harder)
 *     • a "struggle" (helper used, 3+ mistakes, or 2+ hints)             -> -1 (one step friendlier)
 *       and the topic is flagged so it is offered again as practice.
 *     • anything in between changes nothing (a few mistakes are normal learning).
 *
 * Confidence booster: after two struggles in a row, the next level starts one tier easier (once).
 * During a level: after 3 wrong tries the child may switch to a friendlier version (no penalty),
 *   and after 5 wrong tries (or 3 at the friendliest tier) a worked "Show me how" is offered, so
 *   nobody is ever stuck. Nothing here ever removes coins or locks content.
 *
 * Replays: if the chosen puzzle is the same one played last time, the nearest OTHER tier is used so
 *   a replay is not word-for-word the same.
 *
 * Only local data is used. No server, no profile, no personal data.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  var MAXT = 2;

  function clamp(n, lo, hi) { return Math.min(hi, Math.max(lo, n)); }

  var A = {
    CLEAN_TO_RISE: 2,
    WRONG_FOR_FRIENDLIER: 3,
    WRONG_FOR_HELP: 5,
    WRONG_FOR_HELP_AT_FLOOR: 3,

    topicAdj: function (save, topic) { var t = save.topics[topic]; return t ? t.adj : 0; },

    /** Which tier should this level start at right now? Pure: does not change the save. */
    tierFor: function (save, level) {
      var adj = A.topicAdj(save, level.topic);
      var tier = clamp(save.band + adj, 0, MAXT);
      var reason = adj > 0 ? 'rising' : adj < 0 ? 'friendlier' : 'base';
      if (save.struggles >= 2 && tier > 0) { tier -= 1; reason = 'booster'; }
      return { tier: tier, reason: reason };
    },

    /** Choose the actual puzzle object for a start, avoiding an identical replay. Pure. */
    pickPuzzle: function (save, level) {
      var t = A.tierFor(save, level), tier = t.tier;
      var prev = save.levels[level.id] && save.levels[level.id].lastPuzzle;
      var puzzle = level.tiers[tier];
      if (prev && puzzle.id === prev) {
        var order = [tier + 1, tier - 1, tier + 2, tier - 2].filter(function (x) { return x >= 0 && x <= MAXT; });
        // when the child was struggling prefer the easier neighbour
        if (t.reason === 'friendlier' || t.reason === 'booster') order = order.sort(function (a, b) { return a - b; });
        if (order.length) { tier = order[0]; puzzle = level.tiers[tier]; }
      }
      return { tier: tier, puzzle: puzzle, reason: t.reason };
    },

    friendlierTier: function (tier) { return tier > 0 ? tier - 1 : null; },

    /** Should the UI offer "friendlier version" / "show me how" after this many wrong tries? */
    offers: function (tier, wrong) {
      return {
        friendlier: tier > 0 && wrong >= A.WRONG_FOR_FRIENDLIER,
        help: wrong >= (tier > 0 ? A.WRONG_FOR_HELP : A.WRONG_FOR_HELP_AT_FLOOR)
      };
    },

    classify: function (run) {
      if (run.helped || run.wrong >= 3 || run.hints >= 2) return 'struggle';
      if (run.wrong === 0 && run.hints === 0) return 'clean';
      return 'ok';
    },

    stars: function (run) {
      if (run.helped) return 1;
      if (run.wrong === 0 && run.hints === 0) return 3;
      if (run.wrong <= 2 && run.hints <= 1) return 2;
      return 1;
    },

    /** Update topic memory after a finished level. Mutates `save` (caller saves). */
    record: function (save, level, run) {
      var topic = save.topics[level.topic] || (save.topics[level.topic] = { ok: 0, bad: 0, hints: 0, adj: 0, clean: 0, review: false });
      var kind = A.classify(run);
      topic.hints += run.hints;
      topic.bad += run.wrong;
      if (kind === 'struggle') {
        topic.adj = clamp(topic.adj - 1, -1, 1);
        topic.clean = 0;
        topic.review = true;
        save.struggles = clamp(save.struggles + 1, 0, 99);
      } else {
        topic.ok += 1;
        save.struggles = 0;
        if (kind === 'clean') {
          topic.clean += 1;
          if (topic.clean >= A.CLEAN_TO_RISE) { topic.adj = clamp(topic.adj + 1, -1, 1); topic.clean = 0; }
          if (topic.adj >= 0) topic.review = false;
        } else {
          topic.clean = 0;
        }
      }
      return kind;
    }
  };

  MP.adaptive = A;
})();
