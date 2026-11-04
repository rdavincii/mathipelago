/* Island 3 — Glimmer Cove (free demo). Fractions, shapes & perimeter, data, multi-step reasoning. */
(function () {
  'use strict';
  var L = window.MP.levels;

  /* ---------------- m3-1  Tide Tank (visual fractions) ---------------- */
  L.register({
    id: 'm3-1', pack: 'free-demo', island: 'cove', order: 9,
    topic: 'number-sense', skill: 'fractions', band: 'master', scene: 'tank', npc: 'pearla',
    title: { en: 'Tide Tank', ms: 'Tangki Air Pasang' },
    story: {
      en: "Fill Captain Pearla's tank to the right line so the fish can swim!",
      ms: 'Isi tangki Kapten Pearla hingga garisan yang betul supaya ikan boleh berenang!'
    },
    learn: { en: 'Understand fractions as parts of a whole, and equivalent fractions.', ms: 'Memahami pecahan sebagai bahagian daripada keseluruhan, dan pecahan setara.' },
    critter: {
      id: 'drippo', name: { en: 'Drippo', ms: 'Drippo' },
      blurb: { en: 'Drippo is happiest when it is exactly half full.', ms: 'Drippo paling gembira apabila tepat separuh penuh.' },
      look: { body: 'drop', c1: '#63d5ff', c2: '#2fb4f0', ears: 'none', feat: 'fin', acc: 'none' }
    },
    tiers: [
      {
        id: 'm3-1-a', type: 'tank',
        prompt: { en: 'Fill the tank to 1/2.', ms: 'Isi tangki hingga 1/2.' },
        hint: { en: 'Half means 2 equal parts out of 4.', ms: 'Separuh bermaksud 2 bahagian sama saiz daripada 4.' },
        explain: { en: '1/2 of 4 equal parts is 2 parts.', ms: '1/2 daripada 4 bahagian sama saiz ialah 2 bahagian.' },
        spec: { parts: 4, n: 1, d: 2 }
      },
      {
        id: 'm3-1-b', type: 'tank',
        prompt: { en: 'Fill the tank to 3/4.', ms: 'Isi tangki hingga 3/4.' },
        hint: { en: '3/4 means 3 out of every 4 parts. This tank has 8 parts — how many make 3/4?', ms: '3/4 bermaksud 3 daripada setiap 4 bahagian. Tangki ini ada 8 bahagian — berapa bahagian yang sama dengan 3/4?' },
        explain: { en: '3/4 = 6/8, so fill 6 of the 8 parts.', ms: '3/4 = 6/8, jadi isi 6 daripada 8 bahagian.' },
        spec: { parts: 8, n: 3, d: 4 }
      },
      {
        id: 'm3-1-c', type: 'tank',
        prompt: { en: 'Fill the tank to 3/5.', ms: 'Isi tangki hingga 3/5.' },
        hint: { en: '3/5 is the same as 6/10.', ms: '3/5 sama dengan 6/10.' },
        explain: { en: '3/5 = 6/10, so fill 6 of the 10 parts.', ms: '3/5 = 6/10, jadi isi 6 daripada 10 bahagian.' },
        spec: { parts: 10, n: 3, d: 5 }
      }
    ]
  });

  /* ---------------- m3-2  The Shape Door (geometry — tap all that fit) ---------------- */
  L.register({
    id: 'm3-2', pack: 'free-demo', island: 'cove', order: 10,
    topic: 'shape-data', skill: 'shapes', band: 'master', scene: 'door', npc: 'pearla',
    title: { en: 'The Shape Door', ms: 'Pintu Bentuk' },
    story: {
      en: 'The door opens when you find every shape that fits the rule.',
      ms: 'Pintu terbuka apabila anda menjumpai setiap bentuk yang sesuai dengan peraturan.'
    },
    learn: { en: 'Classify shapes by their sides, and work out perimeter.', ms: 'Mengelaskan bentuk mengikut sisinya, dan mengira perimeter.' },
    critter: {
      id: 'prismi', name: { en: 'Prismi', ms: 'Prismi' },
      blurb: { en: 'Prismi loves shapes with sharp corners.', ms: 'Prismi suka bentuk yang bersudut tajam.' },
      look: { body: 'tall', c1: '#ff9f7a', c2: '#ff7a4d', ears: 'none', feat: 'spikes', acc: 'none' }
    },
    tiers: [
      {
        id: 'm3-2-a', type: 'shapes',
        prompt: { en: 'Tap all the triangles.', ms: 'Ketik semua segi tiga.' },
        hint: { en: 'A triangle has 3 straight sides.', ms: 'Segi tiga mempunyai 3 sisi lurus.' },
        explain: { en: 'Triangles have exactly 3 sides. There are two triangles here.', ms: 'Segi tiga mempunyai tepat 3 sisi. Terdapat dua segi tiga di sini.' },
        spec: {
          predicate: 'sides:3',
          items: [
            { k: 'poly', sides: 5, color: 'sky' }, { k: 'poly', sides: 3, color: 'coral' }, { k: 'circle', color: 'sun' },
            { k: 'poly', sides: 4, color: 'mint' }, { k: 'poly', sides: 3, color: 'grape', rot: 180 }, { k: 'poly', sides: 6, color: 'coral' }
          ]
        }
      },
      {
        id: 'm3-2-b', type: 'shapes',
        prompt: { en: 'Tap all the shapes with 4 equal sides.', ms: 'Ketik semua bentuk yang mempunyai 4 sisi sama panjang.' },
        hint: { en: 'Compare the length of every side. Which shapes have all 4 the same?', ms: 'Bandingkan panjang setiap sisi. Bentuk manakah yang keempat-empat sisinya sama?' },
        explain: { en: 'A square and a rhombus have 4 equal sides. The rectangle, kite and trapezium do not.', ms: 'Segi empat sama dan rombus mempunyai 4 sisi sama panjang. Segi empat tepat, layang-layang dan trapezium tidak.' },
        spec: {
          predicate: 'fourEqualSides',
          items: [
            { k: 'quad', type: 'kite', color: 'sun' }, { k: 'quad', type: 'square', color: 'sky' }, { k: 'rect', w: 3, h: 2, color: 'mint' },
            { k: 'quad', type: 'trapezium', color: 'grape' }, { k: 'quad', type: 'rhombus', color: 'coral' }, { k: 'poly', sides: 3, color: 'sun' }
          ]
        }
      },
      {
        id: 'm3-2-c', type: 'shapes',
        prompt: { en: 'Each small square is 1 unit. Tap all the rectangles with a perimeter of 14 units.', ms: 'Setiap petak kecil ialah 1 unit. Ketik semua segi empat tepat yang perimeternya 14 unit.' },
        hint: { en: 'Perimeter is the distance around: 2 × (length + width).', ms: 'Perimeter ialah jarak mengelilingi: 2 × (panjang + lebar).' },
        explain: { en: '4×3, 5×2 and 6×1 all have a perimeter of 14. The others have 16, 12 and 16.', ms: '4×3, 5×2 dan 6×1 semuanya mempunyai perimeter 14. Yang lain ialah 16, 12 dan 16.' },
        spec: {
          predicate: 'perimeter:14',
          items: [
            { k: 'rect', w: 4, h: 3, color: 'sky', grid: true }, { k: 'rect', w: 5, h: 2, color: 'mint', grid: true },
            { k: 'rect', w: 4, h: 4, color: 'coral', grid: true }, { k: 'rect', w: 6, h: 1, color: 'sun', grid: true },
            { k: 'rect', w: 3, h: 3, color: 'grape', grid: true }, { k: 'rect', w: 5, h: 3, color: 'sky', grid: true }
          ]
        }
      }
    ]
  });

  /* ---------------- m3-3  Treasure Tally (reading a bar chart) ---------------- */
  var SHELLS = { en: 'Shells', ms: 'Kerang' }, PEARLS = { en: 'Pearls', ms: 'Mutiara' },
      COINS = { en: 'Coins', ms: 'Syiling' }, GEMS = { en: 'Gems', ms: 'Permata' };

  L.register({
    id: 'm3-3', pack: 'free-demo', island: 'cove', order: 11,
    topic: 'shape-data', skill: 'data', band: 'master', scene: 'chest', npc: 'pearla',
    title: { en: 'Treasure Tally', ms: 'Kiraan Harta Karun' },
    story: {
      en: 'Read the treasure chart to open the chest!',
      ms: 'Baca carta harta karun untuk membuka peti!'
    },
    learn: { en: 'Read bar charts, add, compare and find the mean.', ms: 'Membaca carta palang, menambah, membandingkan dan mencari min.' },
    critter: {
      id: 'tallybean', name: { en: 'Tallybean', ms: 'Tallybean' },
      blurb: { en: 'Tallybean counts everything twice, just to be sure.', ms: 'Tallybean mengira segalanya dua kali, untuk memastikan.' },
      look: { body: 'blob', c1: '#8de28a', c2: '#52c85c', ears: 'leaf', feat: 'none', acc: 'none' }
    },
    tiers: [
      {
        id: 'm3-3-a', type: 'chart',
        prompt: { en: 'How many more coins than shells are there?', ms: 'Berapa banyak syiling lebih daripada kerang?' },
        hint: { en: 'Read the height of each bar, then subtract the smaller from the bigger.', ms: 'Baca ketinggian setiap palang, kemudian tolak yang kecil daripada yang besar.' },
        explain: { en: '8 coins − 3 shells = 5 more coins.', ms: '8 syiling − 3 kerang = 5 syiling lebih.' },
        spec: {
          axisMax: 10, axisStep: 1,
          bars: [{ label: SHELLS, value: 3, color: 'coral' }, { label: PEARLS, value: 5, color: 'sky' }, { label: COINS, value: 8, color: 'sun' }],
          ask: { op: 'diff', a: 2, b: 0 }
        }
      },
      {
        id: 'm3-3-b', type: 'chart',
        prompt: { en: 'How many treasures are there altogether?', ms: 'Berapakah jumlah semua harta karun?' },
        hint: { en: 'Read all three bars, then add them together.', ms: 'Baca ketiga-tiga palang, kemudian tambahkannya.' },
        explain: { en: '12 + 20 + 35 = 67 treasures.', ms: '12 + 20 + 35 = 67 harta karun.' },
        spec: {
          axisMax: 40, axisStep: 5,
          bars: [{ label: SHELLS, value: 12, color: 'coral' }, { label: PEARLS, value: 20, color: 'sky' }, { label: COINS, value: 35, color: 'sun' }],
          ask: { op: 'sum', of: [0, 1, 2] }
        }
      },
      {
        id: 'm3-3-c', type: 'chart',
        prompt: { en: 'What is the mean (average) number of treasures in each group?', ms: 'Berapakah min (purata) bilangan harta karun dalam setiap kumpulan?' },
        hint: { en: 'Add all four bars, then share equally: divide by 4.', ms: 'Tambah keempat-empat palang, kemudian bahagi sama banyak: bahagi dengan 4.' },
        explain: { en: '24 + 18 + 36 + 26 = 104, and 104 ÷ 4 = 26.', ms: '24 + 18 + 36 + 26 = 104, dan 104 ÷ 4 = 26.' },
        spec: {
          axisMax: 40, axisStep: 10,
          bars: [{ label: SHELLS, value: 24, color: 'coral' }, { label: PEARLS, value: 18, color: 'sky' }, { label: COINS, value: 36, color: 'sun' }, { label: GEMS, value: 26, color: 'grape' }],
          ask: { op: 'mean' }
        }
      }
    ]
  });

  /* ---------------- m3-4  Lighthouse Lamps (multi-step challenge — grand finale) ---------------- */
  // `calc` is only used by the automated tests to prove each answer; the game never evaluates it.
  L.register({
    id: 'm3-4', pack: 'free-demo', island: 'cove', order: 12,
    topic: 'reasoning', skill: 'multi-step', band: 'master', scene: 'lighthouse', npc: 'pearla',
    title: { en: 'Lighthouse Lamps', ms: 'Lampu Rumah Api' },
    story: {
      en: 'Three lamps, three puzzles! Solve each one to light the lighthouse.',
      ms: 'Tiga lampu, tiga teka-teki! Selesaikan setiap satu untuk menyalakan rumah api.'
    },
    learn: { en: 'Solve multi-step word problems (operations, ratio, order of operations, negative numbers).', ms: 'Menyelesaikan masalah perkataan berbilang langkah (operasi, nisbah, tertib operasi, nombor negatif).' },
    critter: {
      id: 'beamer', name: { en: 'Beamer', ms: 'Beamer' },
      blurb: { en: 'Beamer shines the way for every sailor.', ms: 'Beamer menyinari jalan untuk setiap kelasi.' },
      look: { body: 'cloud', c1: '#fff3a8', c2: '#ffd84d', ears: 'none', feat: 'antenna', acc: 'hat' }
    },
    tiers: [
      {
        id: 'm3-4-a', type: 'steps',
        prompt: { en: 'Light all three lamps. Solve each step in order.', ms: 'Nyalakan ketiga-tiga lampu. Selesaikan setiap langkah mengikut urutan.' },
        hint: { en: 'Add first, then subtract, then share.', ms: 'Tambah dahulu, kemudian tolak, kemudian kongsi.' },
        explain: { en: '7 + 5 = 12, then 12 − 4 = 8, then 8 ÷ 2 = 4.', ms: '7 + 5 = 12, kemudian 12 − 4 = 8, kemudian 8 ÷ 2 = 4.' },
        spec: { steps: [
          { q: { en: 'Nimbo carries 7 crystals and finds 5 more. How many crystals now?', ms: 'Nimbo membawa 7 kristal dan menjumpai 5 lagi. Berapa kristal sekarang?' },
            choices: ['10', '11', '12', '13'], answer: 2, calc: '7+5' },
          { q: { en: 'The first lamp uses 4 crystals. How many are left?', ms: 'Lampu pertama menggunakan 4 kristal. Berapa yang tinggal?' },
            choices: ['6', '8', '9', '16'], answer: 1, calc: '12−4' },
          { q: { en: 'Share the crystals that are left equally into 2 boxes. How many in each box?', ms: 'Kongsi kristal yang tinggal sama banyak ke dalam 2 kotak. Berapa dalam setiap kotak?' },
            choices: ['2', '3', '4', '6'], answer: 2, calc: '8÷2' }
        ] }
      },
      {
        id: 'm3-4-b', type: 'steps',
        prompt: { en: 'Light all three lamps. Solve each step in order.', ms: 'Nyalakan ketiga-tiga lampu. Selesaikan setiap langkah mengikut urutan.' },
        hint: { en: 'A ratio of 2 : 3 means 3 cups of water for every 2 cups of syrup.', ms: 'Nisbah 2 : 3 bermaksud 3 cawan air untuk setiap 2 cawan sirap.' },
        explain: { en: '6 ÷ 2 = 3 batches; 3 × 3 = 9 cups of water; 6 + 9 = 15 cups altogether.', ms: '6 ÷ 2 = 3 sukatan; 3 × 3 = 9 cawan air; 6 + 9 = 15 cawan kesemuanya.' },
        spec: { steps: [
          { q: { en: 'The festival drink uses 2 cups of syrup for every 3 cups of water. You have 6 cups of syrup. How many batches can you make?', ms: 'Minuman perayaan menggunakan 2 cawan sirap untuk setiap 3 cawan air. Anda ada 6 cawan sirap. Berapa sukatan yang boleh dibuat?' },
            choices: ['2', '3', '4', '6'], answer: 1, calc: '6÷2' },
          { q: { en: 'So how many cups of water do you need for all those batches?', ms: 'Jadi berapa cawan air yang diperlukan untuk semua sukatan itu?' },
            choices: ['6', '8', '9', '12'], answer: 2, calc: '3×3' },
          { q: { en: 'How many cups of drink is that altogether (syrup and water)?', ms: 'Berapa cawan minuman kesemuanya (sirap dan air)?' },
            choices: ['13', '15', '18', '20'], answer: 1, calc: '6+9' }
        ] }
      },
      {
        id: 'm3-4-c', type: 'steps',
        prompt: { en: 'Light all three lamps. Solve each step in order.', ms: 'Nyalakan ketiga-tiga lampu. Selesaikan setiap langkah mengikut urutan.' },
        hint: { en: 'Multiply before you add. For numbers below zero, count down past 0.', ms: 'Darab sebelum menambah. Untuk nombor di bawah sifar, kira turun melepasi 0.' },
        explain: { en: '4 + 3 × 5 = 4 + 15 = 19; 7 − 10 = −3; −12 + 5 = −7.', ms: '4 + 3 × 5 = 4 + 15 = 19; 7 − 10 = −3; −12 + 5 = −7.' },
        spec: { steps: [
          { q: { en: 'What is 4 + 3 × 5?', ms: 'Berapakah 4 + 3 × 5?' },
            choices: ['35', '19', '27', '15'], answer: 1, calc: '4+3×5' },
          { q: { en: 'The lamp room is 7°C. At night it drops by 10°C. What is the temperature now?', ms: 'Bilik lampu bersuhu 7°C. Pada waktu malam suhu turun 10°C. Berapakah suhu sekarang?' },
            choices: ['17', '3', '−3', '−17'], answer: 2, calc: '7−10' },
          { q: { en: 'A diver is at −12 metres and swims up 5 metres. Where is the diver now?', ms: 'Seorang penyelam berada pada −12 meter dan berenang naik 5 meter. Di manakah penyelam itu sekarang?' },
            choices: ['−17', '−7', '7', '17'], answer: 1, calc: '−12+5' }
        ] }
      }
    ]
  });
})();
