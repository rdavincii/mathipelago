/* Island 1 — Cloudberry Meadows (free demo). Number sense, addition, patterns, fair sharing. */
(function () {
  'use strict';
  var L = window.MP.levels;

  /* ---------------- m1-1  The Plank Bridge (interactive number line — also the tutorial) ---------------- */
  L.register({
    id: 'm1-1', pack: 'free-demo', island: 'meadow', order: 1,
    topic: 'number-sense', skill: 'number-line', band: 'explorer', scene: 'bridge', npc: 'berri',
    title: { en: 'The Plank Bridge', ms: 'Jambatan Papan' },
    story: {
      en: 'The bridge to Cloudberry Hill has a gap! Help Nimbo set the missing plank.',
      ms: 'Jambatan ke Bukit Beri Awan ada ruang kosong! Bantu Nimbo meletakkan papan yang hilang.'
    },
    learn: { en: 'Locate whole numbers on a number line.', ms: 'Menentukan kedudukan nombor bulat pada garis nombor.' },
    critter: {
      id: 'plankie', name: { en: 'Plankie', ms: 'Plankie' },
      blurb: { en: 'Plankie loves bridges and hums while it builds.', ms: 'Plankie suka jambatan dan bersenandung ketika membina.' },
      look: { body: 'blob', c1: '#ffb86b', c2: '#ff8f4d', ears: 'round', feat: 'none', acc: 'none' }
    },
    tiers: [
      {
        id: 'm1-1-a', type: 'numberline',
        prompt: { en: 'Nimbo needs a plank at number 7. Slide the glowing plank to 7.', ms: 'Nimbo perlukan papan di nombor 7. Gelongsorkan papan bercahaya ke nombor 7.' },
        hint: { en: 'Count along the line: 1, 2, 3 … 7 comes right after 6.', ms: 'Kira sepanjang garisan: 1, 2, 3 … 7 datang tepat selepas 6.' },
        explain: { en: 'Start at 0 and take 7 jumps. The plank goes at 7.', ms: 'Mula dari 0 dan buat 7 lompatan. Papan diletakkan di 7.' },
        spec: { min: 0, max: 10, step: 1, labelEvery: 1, target: 7, start: 2 }
      },
      {
        id: 'm1-1-b', type: 'numberline',
        prompt: { en: 'Place the plank at 14.', ms: 'Letakkan papan di nombor 14.' },
        hint: { en: '10 is the long mark in the middle. Count on 4 more.', ms: '10 ialah tanda panjang di tengah. Kira 4 lagi.' },
        explain: { en: 'From 10, count on 4 more: 11, 12, 13, 14.', ms: 'Dari 10, kira 4 lagi: 11, 12, 13, 14.' },
        spec: { min: 0, max: 20, step: 1, labelEvery: 5, target: 14, start: 3 }
      },
      {
        id: 'm1-1-c', type: 'numberline',
        prompt: { en: 'Place the plank exactly halfway between 60 and 80.', ms: 'Letakkan papan tepat di tengah-tengah antara 60 dan 80.' },
        hint: { en: '60 + 80 = 140, and half of 140 is 70.', ms: '60 + 80 = 140, dan separuh daripada 140 ialah 70.' },
        explain: { en: 'The gap from 60 to 80 is 20. Half of 20 is 10, so the middle is 60 + 10 = 70.', ms: 'Jarak dari 60 ke 80 ialah 20. Separuh daripada 20 ialah 10, jadi titik tengah ialah 60 + 10 = 70.' },
        spec: { min: 0, max: 100, step: 10, labelEvery: 10, target: 70, start: 20 }
      }
    ]
  });

  /* ---------------- m1-2  Berry Scale (addition by balancing) ---------------- */
  L.register({
    id: 'm1-2', pack: 'free-demo', island: 'meadow', order: 2,
    topic: 'operations', skill: 'addition', band: 'explorer', scene: 'scale', npc: 'berri',
    title: { en: 'Berry Scale', ms: 'Penimbang Beri' },
    story: {
      en: "Mama Berri's scale is wobbly! Put berry crates on it until it balances the big number.",
      ms: 'Penimbang Mama Berri senget! Letakkan kotak beri padanya sehingga seimbang dengan nombor besar.'
    },
    learn: { en: 'Add numbers to reach a target total.', ms: 'Menambah nombor untuk mencapai jumlah sasaran.' },
    critter: {
      id: 'weighby', name: { en: 'Weighby', ms: 'Weighby' },
      blurb: { en: 'Weighby can feel when things are perfectly balanced.', ms: 'Weighby dapat merasa apabila sesuatu seimbang dengan sempurna.' },
      look: { body: 'round', c1: '#9ad7ff', c2: '#5fb7f0', ears: 'point', feat: 'tuft', acc: 'none' }
    },
    tiers: [
      {
        id: 'm1-2-a', type: 'balance',
        prompt: { en: 'Choose crates that add up to 10.', ms: 'Pilih kotak yang jumlahnya 10.' },
        hint: { en: 'Try pairs. Which number goes with 3 to make 10?', ms: 'Cuba pasangan. Nombor apa bersama 3 untuk menjadi 10?' },
        explain: { en: '3 + 7 = 10, so crates 3 and 7 balance the scale.', ms: '3 + 7 = 10, jadi kotak 3 dan 7 menyeimbangkan penimbang.' },
        spec: { target: 10, tiles: [3, 7, 4, 5, 2] }
      },
      {
        id: 'm1-2-b', type: 'balance',
        prompt: { en: 'Choose crates that add up to 25.', ms: 'Pilih kotak yang jumlahnya 25.' },
        hint: { en: 'Start with a big crate. How much is still needed?', ms: 'Mulakan dengan kotak besar. Berapa lagi diperlukan?' },
        explain: { en: '12 + 13 = 25.', ms: '12 + 13 = 25.' },
        spec: { target: 25, tiles: [12, 8, 13, 9, 6, 15] }
      },
      {
        id: 'm1-2-c', type: 'balance',
        prompt: { en: 'Choose exactly 3 crates that add up to 150.', ms: 'Pilih tepat 3 kotak yang jumlahnya 150.' },
        hint: { en: 'Pick one crate, then find two more that make the rest.', ms: 'Pilih satu kotak, kemudian cari dua lagi yang membentuk bakinya.' },
        explain: { en: '35 + 55 + 60 = 150.', ms: '35 + 55 + 60 = 150.' },
        spec: { target: 150, tiles: [45, 60, 35, 55, 90, 25], count: 3 }
      }
    ]
  });

  /* ---------------- m1-3  Windmill Pattern ---------------- */
  L.register({
    id: 'm1-3', pack: 'free-demo', island: 'meadow', order: 3,
    topic: 'number-sense', skill: 'patterns', band: 'explorer', scene: 'windmill', npc: 'berri',
    title: { en: 'Windmill Pattern', ms: 'Corak Kincir Angin' },
    story: {
      en: 'The windmill only spins when the pattern is finished. What comes next?',
      ms: 'Kincir angin hanya berputar apabila corak itu lengkap. Apa yang seterusnya?'
    },
    learn: { en: 'Continue repeating and number patterns.', ms: 'Menyambung corak berulang dan corak nombor.' },
    critter: {
      id: 'whirlette', name: { en: 'Whirlette', ms: 'Whirlette' },
      blurb: { en: 'Whirlette spins when it spots a pattern.', ms: 'Whirlette berpusing apabila ternampak corak.' },
      look: { body: 'drop', c1: '#ffd36b', c2: '#ffb62e', ears: 'none', feat: 'antenna', acc: 'none' }
    },
    tiers: [
      {
        id: 'm1-3-a', type: 'pattern',
        prompt: { en: 'Which shape comes next?', ms: 'Bentuk manakah yang seterusnya?' },
        hint: { en: 'Look at the shapes: they repeat in the same order.', ms: 'Lihat bentuk-bentuk itu: ia berulang dalam susunan yang sama.' },
        explain: { en: 'The pattern is circle, square, circle, square … so a square comes next.', ms: 'Coraknya bulatan, segi empat sama, bulatan, segi empat sama … jadi segi empat sama datang seterusnya.' },
        spec: {
          rule: { kind: 'cycle', items: ['circle:coral', 'square:sky'], length: 6 }, hidden: 5,
          options: ['circle:coral', 'square:sky', 'triangle:sun']
        }
      },
      {
        id: 'm1-3-b', type: 'pattern',
        prompt: { en: 'Which number comes next?', ms: 'Nombor manakah yang seterusnya?' },
        hint: { en: 'How much does each number go up by?', ms: 'Setiap nombor bertambah berapa?' },
        explain: { en: 'The numbers go up by 3 each time: 12 + 3 = 15.', ms: 'Nombor bertambah 3 setiap kali: 12 + 3 = 15.' },
        spec: { rule: { kind: 'arith', start: 3, step: 3, length: 5 }, hidden: 4, options: [14, 15, 16, 18] }
      },
      {
        id: 'm1-3-c', type: 'pattern',
        prompt: { en: 'Which number comes next?', ms: 'Nombor manakah yang seterusnya?' },
        hint: { en: 'Each number is double the one before it.', ms: 'Setiap nombor ialah dua kali ganda nombor sebelumnya.' },
        explain: { en: 'Each number is doubled: 24 × 2 = 48.', ms: 'Setiap nombor digandakan dua kali: 24 × 2 = 48.' },
        spec: { rule: { kind: 'geo', start: 3, mult: 2, length: 5 }, hidden: 4, options: [30, 36, 48, 72] }
      }
    ]
  });

  /* ---------------- m1-4  Fair Share Picnic (division by sharing; drag OR tap) ---------------- */
  L.register({
    id: 'm1-4', pack: 'free-demo', island: 'meadow', order: 4,
    topic: 'operations', skill: 'sharing', band: 'explorer', scene: 'picnic', npc: 'berri',
    title: { en: 'Fair Share Picnic', ms: 'Berkelah Kongsi Adil' },
    story: {
      en: 'Picnic time! Share the berries so every basket has the same.',
      ms: 'Masa berkelah! Kongsi beri supaya setiap bakul mendapat sama banyak.'
    },
    learn: { en: 'Share equally (division as fair sharing).', ms: 'Berkongsi sama banyak (pembahagian sebagai perkongsian adil).' },
    critter: {
      id: 'picnibble', name: { en: 'Picnibble', ms: 'Picnibble' },
      blurb: { en: 'Picnibble always shares its snacks fairly.', ms: 'Picnibble sentiasa berkongsi snek dengan adil.' },
      look: { body: 'round', c1: '#ff9eb5', c2: '#ff6f91', ears: 'round', feat: 'none', acc: 'crown' }
    },
    tiers: [
      {
        id: 'm1-4-a', type: 'share',
        prompt: { en: 'Share 6 berries fairly between 2 baskets.', ms: 'Kongsi 6 biji beri dengan adil dalam 2 bakul.' },
        hint: { en: 'Fair means every basket gets the same number.', ms: 'Adil bermaksud setiap bakul mendapat bilangan yang sama.' },
        explain: { en: '6 ÷ 2 = 3, so 3 berries go in each basket.', ms: '6 ÷ 2 = 3, jadi 3 biji beri dimasukkan ke dalam setiap bakul.' },
        spec: { items: 6, baskets: 2 }
      },
      {
        id: 'm1-4-b', type: 'share',
        prompt: { en: 'Share 12 berries fairly between 3 baskets.', ms: 'Kongsi 12 biji beri dengan adil dalam 3 bakul.' },
        hint: { en: 'Deal the berries out one at a time, like cards.', ms: 'Edarkan beri satu demi satu, seperti mengedar kad.' },
        explain: { en: '12 ÷ 3 = 4, so each basket gets 4 berries.', ms: '12 ÷ 3 = 4, jadi setiap bakul mendapat 4 biji beri.' },
        spec: { items: 12, baskets: 3 }
      },
      {
        id: 'm1-4-c', type: 'share',
        prompt: { en: 'Share 24 berries fairly between 6 baskets.', ms: 'Kongsi 24 biji beri dengan adil dalam 6 bakul.' },
        hint: { en: 'How many in each basket? Think: 6 times what makes 24?', ms: 'Berapa dalam setiap bakul? Fikirkan: 6 darab berapa menjadi 24?' },
        explain: { en: '24 ÷ 6 = 4, because 6 × 4 = 24.', ms: '24 ÷ 6 = 4, kerana 6 × 4 = 24.' },
        spec: { items: 24, baskets: 6 }
      }
    ]
  });
})();
