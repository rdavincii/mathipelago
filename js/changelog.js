/*
 * changelog.js — "What's new" shown in Settings. Newest first. Edit this (and MP.config.version) when you ship an update.
 * Each item is {en, ms}. Keep it short and friendly: it is read by children and parents.
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});
  MP.changelog = [
    { v: '0.7.0', date: '2026-11-04', items: [
      { en: 'Friends race: see you and your friends racing along a track, ranked by stars.', ms: 'Perlumbaan kawan: lihat anda dan kawan berlumba di landasan, disusun mengikut bintang.' },
      { en: 'Settings is now a gear at the top right. Your player and Add player can fold away.', ms: 'Tetapan kini ikon gear di penjuru kanan atas. Pemain anda dan Tambah pemain boleh dilipat.' },
      { en: 'Fixed the map animations freezing on slower phones.', ms: 'Membaiki animasi peta yang tersekat pada telefon yang lebih perlahan.' }
    ] },
    { v: '0.6.0', date: '2026-11-02', items: [
      { en: 'Online friends: share a friend code, see each other\u2019s stars and pals, and send cheers that give coins. A grown-up turns it on.', ms: 'Kawan dalam talian: kongsi kod kawan, lihat bintang dan kawan masing-masing, dan hantar sorakan yang memberi syiling. Orang dewasa menghidupkannya.' },
      { en: 'Smoother, springier motion: presses, pop-ups and screens now move like a native app.', ms: 'Gerakan lebih lancar dan melantun: tekanan, tetingkap dan skrin kini bergerak seperti aplikasi asli.' }
    ] },
    { v: '0.5.0', date: '2026-10-21', items: [
      { en: 'Daily gift: log in each day for more coins, with a Perfect Week bonus on day 7.', ms: 'Hadiah harian: log masuk setiap hari untuk lebih banyak syiling, dengan bonus Minggu Sempurna pada hari ke-7.' },
      { en: '100 new levels on 10 new islands, up to 312 levels in all.', ms: '100 tahap baharu di 10 pulau baharu, sehingga 312 tahap kesemuanya.' },
      { en: 'Hats and pal accessories are now found by finishing levels, not bought.', ms: 'Topi dan aksesori kawan kini ditemui dengan menamatkan tahap, bukan dibeli.' },
      { en: 'The map path is now a curvy dashed trail.', ms: 'Laluan peta kini ialah denai putus-putus yang melengkung.' },
      { en: 'Sound is more reliable: it wakes up again after a phone call, a lock screen or switching apps.', ms: 'Bunyi lebih dipercayai: ia hidup semula selepas panggilan telefon, skrin kunci atau menukar aplikasi.' },
      { en: 'Version and update info in Settings.', ms: 'Maklumat versi dan kemas kini dalam Tetapan.' }
    ] },
    { v: '0.4.0', date: '2026-10-14', items: [
      { en: 'Playful background music with a volume slider.', ms: 'Muzik latar yang ceria dengan peluncur kelantangan.' },
      { en: 'Rounder, happier islands and drifting clouds.', ms: 'Pulau yang lebih bulat dan ceria serta awan yang melayang.' },
      { en: 'Skills you have learned are shown on the dashboard.', ms: 'Kemahiran yang telah dipelajari ditunjukkan pada papan pemuka.' }
    ] },
    { v: '0.3.0', date: '2026-10-07', items: [
      { en: 'Players (profiles) with backups, and pal dress-up.', ms: 'Pemain (profil) dengan sandaran, dan pakaian untuk kawan.' }
    ] }
  ];
})();
