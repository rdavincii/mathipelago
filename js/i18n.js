/*
 * i18n.js — localisation.
 *   MP.i18n.t('menu.play')            -> UI string from js/locales/<lang>.js
 *   MP.i18n.tx({en:'..', ms:'..'})    -> text object that lives inside level/pack data
 * Adding a language = add js/locales/xx.js, register it, add 'xx' to MP.i18n.supported.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  var i18n = {
    supported: ['en', 'ms'],
    lang: 'en',
    dict: {},
    missing: {},   // filled at runtime so tests / devs can spot gaps

    register: function (lang, strings) { this.dict[lang] = strings; },

    setLang: function (lang) {
      if (this.supported.indexOf(lang) === -1) lang = 'en';
      this.lang = lang;
      if (typeof document !== 'undefined') document.documentElement.setAttribute('lang', lang === 'ms' ? 'ms' : 'en');
    },

    /** Best first-run guess from the browser; the player can always change it. */
    detect: function () {
      var l = (typeof navigator !== 'undefined' && (navigator.language || '')) || '';
      l = l.toLowerCase();
      return (l.indexOf('ms') === 0 || l.indexOf('id') === 0) ? 'ms' : 'en';
    },

    _fill: function (s, vars) {
      if (!vars) return s;
      return s.replace(/\{(\w+)\}/g, function (m, k) { return vars[k] != null ? vars[k] : m; });
    },

    t: function (key, vars) {
      var d = this.dict[this.lang], s = d && d[key];
      if (s == null) {
        this.missing[this.lang + ':' + key] = true;
        var fb = this.dict.en && this.dict.en[key];
        s = fb != null ? fb : key;
      }
      return this._fill(s, vars);
    },

    /** Text object {en, ms}. Falls back to English, never to an empty string. */
    tx: function (obj, vars) {
      if (obj == null) return '';
      if (typeof obj === 'string') return this._fill(obj, vars);
      var s = obj[this.lang];
      if (s == null) { this.missing[this.lang + ':obj:' + (obj.en || '?').slice(0, 24)] = true; s = obj.en; }
      return this._fill(s == null ? '' : s, vars);
    },

    /** Money is stored as whole sen. 135 -> "RM1.35", 70 -> "70 sen". Same in both languages. */
    money: function (sen) {
      if (sen < 100) return sen + ' sen';
      var rm = Math.floor(sen / 100), rest = sen % 100;
      return 'RM' + rm + (rest ? '.' + (rest < 10 ? '0' : '') + rest : '');
    }
  };

  MP.i18n = i18n;
  MP.t = function (k, v) { return i18n.t(k, v); };
  MP.tx = function (o, v) { return i18n.tx(o, v); };
})();
