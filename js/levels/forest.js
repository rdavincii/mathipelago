/* Island 2 — Gearwood Forest (free demo). Multiplication, times tables, place value, money. */
(function () {
  'use strict';
  var L = window.MP.levels;

  /* ---------------- m2-1  Gear Chain (arrange number tiles into an equation) ---------------- */
  L.register({
    id: 'm2-1', pack: 'free-demo', island: 'forest', order: 5,
    topic: 'operations', skill: 'multiplication', band: 'adventurer', scene: 'gears', npc: 'tock',
    title: { en: 'Gear Chain', ms: 'Rantai Gerigi' },
    story: {
      en: "Tock's machine is stuck! Put two number tiles into the gears to make the answer.",
      ms: 'Mesin Tock tersekat! Letakkan dua jubin nombor ke dalam gerigi untuk mendapatkan jawapan.'
    },
    learn: { en: 'Find factor pairs and use multiplication facts.', ms: 'Mencari pasangan faktor dan menggunakan fakta darab.' },
    critter: {
      id: 'cogwhisk', name: { en: 'Cogwhisk', ms: 'Cogwhisk' },
      blurb: { en: 'Cogwhisk keeps the gears turning.', ms: 'Cogwhisk memastikan gerigi terus berputar.' },
      look: { body: 'tall', c1: '#7fe0c3', c2: '#3fc3a0', ears: 'none', feat: 'antenna', acc: 'goggles' }
    },
    tiers: [
      {
        id: 'm2-1-a', type: 'tiles',
        prompt: { en: 'Pick two tiles that multiply to make 12.', ms: 'Pilih dua jubin yang apabila didarab menjadi 12.' },
        hint: { en: 'Think of your 2, 3 and 4 times tables.', ms: 'Fikirkan sifir 2, 3 dan 4.' },
        explain: { en: '3 × 4 = 12 (and 2 × 6 = 12 works too).', ms: '3 × 4 = 12 (dan 2 × 6 = 12 juga betul).' },
        spec: { op: '*', target: 12, tiles: [3, 4, 5, 6, 2] }
      },
      {
        id: 'm2-1-b', type: 'tiles',
        prompt: { en: 'Pick two tiles that multiply to make 24.', ms: 'Pilih dua jubin yang apabila didarab menjadi 24.' },
        hint: { en: 'Try the 3 times table: 3 × ? = 24.', ms: 'Cuba sifir 3: 3 × ? = 24.' },
        explain: { en: '3 × 8 = 24 (and 4 × 6 = 24 works too).', ms: '3 × 8 = 24 (dan 4 × 6 = 24 juga betul).' },
        spec: { op: '*', target: 24, tiles: [3, 4, 6, 8, 7, 5] }
      },
      {
        id: 'm2-1-c', type: 'tiles',
        prompt: { en: 'Pick two tiles that multiply to make 72.', ms: 'Pilih dua jubin yang apabila didarab menjadi 72.' },
        hint: { en: 'Think of the 9 times table or the 6 times table.', ms: 'Fikirkan sifir 9 atau sifir 6.' },
        explain: { en: '8 × 9 = 72 (and 6 × 12 = 72 works too).', ms: '8 × 9 = 72 (dan 6 × 12 = 72 juga betul).' },
        spec: { op: '*', target: 72, tiles: [6, 8, 9, 12, 7, 5] }
      }
    ]
  });

  /* ---------------- m2-2  Lantern Match (matching pairs) ---------------- */
  L.register({
    id: 'm2-2', pack: 'free-demo', island: 'forest', order: 6,
    topic: 'operations', skill: 'times-tables', band: 'adventurer', scene: 'lanterns', npc: 'tock',
    title: { en: 'Lantern Match', ms: 'Padanan Tanglung' },
    story: {
      en: 'Light the lanterns by matching each question with its answer.',
      ms: 'Nyalakan tanglung dengan memadankan setiap soalan dengan jawapannya.'
    },
    learn: { en: 'Recall multiplication and division facts.', ms: 'Mengingat fakta darab dan bahagi.' },
    critter: {
      id: 'glowbug', name: { en: 'Glowbug', ms: 'Glowbug' },
      blurb: { en: 'Glowbug lights up when it sees a match.', ms: 'Glowbug bercahaya apabila ternampak padanan.' },
      look: { body: 'blob', c1: '#ffe27a', c2: '#ffc933', ears: 'none', feat: 'antenna', acc: 'none' }
    },
    tiers: [
      {
        id: 'm2-2-a', type: 'match',
        prompt: { en: 'Tap a question, then tap its answer.', ms: 'Ketik satu soalan, kemudian ketik jawapannya.' },
        hint: { en: 'Start with the one you know best.', ms: 'Mulakan dengan yang paling anda tahu.' },
        explain: { en: '2 × 3 = 6, 2 × 5 = 10 and 4 × 2 = 8.', ms: '2 × 3 = 6, 2 × 5 = 10 dan 4 × 2 = 8.' },
        spec: { pairs: [
          { id: 'a', left: '2 × 3', right: '6' }, { id: 'b', left: '2 × 5', right: '10' }, { id: 'c', left: '4 × 2', right: '8' }
        ] }
      },
      {
        id: 'm2-2-b', type: 'match',
        prompt: { en: 'Tap a question, then tap its answer.', ms: 'Ketik satu soalan, kemudian ketik jawapannya.' },
        hint: { en: 'Skip the hard ones first and come back to them.', ms: 'Langkau yang sukar dahulu dan kembali kepadanya kemudian.' },
        explain: { en: '3 × 4 = 12, 5 × 6 = 30, 4 × 7 = 28 and 6 × 3 = 18.', ms: '3 × 4 = 12, 5 × 6 = 30, 4 × 7 = 28 dan 6 × 3 = 18.' },
        spec: { pairs: [
          { id: 'a', left: '3 × 4', right: '12' }, { id: 'b', left: '5 × 6', right: '30' },
          { id: 'c', left: '4 × 7', right: '28' }, { id: 'd', left: '6 × 3', right: '18' }
        ] }
      },
      {
        id: 'm2-2-c', type: 'match',
        prompt: { en: 'Tap a question, then tap its answer.', ms: 'Ketik satu soalan, kemudian ketik jawapannya.' },
        hint: { en: 'Division undoes multiplication: 56 ÷ 8 asks "8 × ? = 56".', ms: 'Bahagi membatalkan darab: 56 ÷ 8 bermaksud "8 × ? = 56".' },
        explain: { en: '6 × 7 = 42, 8 × 9 = 72, 56 ÷ 8 = 7, 9 × 6 = 54 and 48 ÷ 6 = 8.', ms: '6 × 7 = 42, 8 × 9 = 72, 56 ÷ 8 = 7, 9 × 6 = 54 dan 48 ÷ 6 = 8.' },
        spec: { pairs: [
          { id: 'a', left: '6 × 7', right: '42' }, { id: 'b', left: '8 × 9', right: '72' },
          { id: 'c', left: '56 ÷ 8', right: '7' }, { id: 'd', left: '9 × 6', right: '54' },
          { id: 'e', left: '48 ÷ 6', right: '8' }
        ] }
      }
    ]
  });

  /* ---------------- m2-3  Rusty Gate Code (place value) ---------------- */
  L.register({
    id: 'm2-3', pack: 'free-demo', island: 'forest', order: 7,
    topic: 'number-sense', skill: 'place-value', band: 'adventurer', scene: 'gate', npc: 'tock',
    title: { en: 'Rusty Gate Code', ms: 'Kod Pintu Berkarat' },
    story: {
      en: 'The old gate opens with a secret number. Build the number to open it!',
      ms: 'Pintu lama itu terbuka dengan nombor rahsia. Bina nombor itu untuk membukanya!'
    },
    learn: { en: 'Understand place value up to thousands.', ms: 'Memahami nilai tempat sehingga ribu.' },
    critter: {
      id: 'gatekin', name: { en: 'Gatekin', ms: 'Gatekin' },
      blurb: { en: 'Gatekin knows every secret code.', ms: 'Gatekin tahu setiap kod rahsia.' },
      look: { body: 'tall', c1: '#c9a0ff', c2: '#9b6cff', ears: 'point', feat: 'horn', acc: 'none' }
    },
    tiers: [
      {
        id: 'm2-3-a', type: 'placeValue',
        prompt: { en: 'Build the number 325. Use + and − to set the hundreds, tens and ones.', ms: 'Bina nombor 325. Guna + dan − untuk menetapkan ratus, puluh dan sa.' },
        hint: { en: '3 hundreds, 2 tens and 5 ones: 300 + 20 + 5.', ms: '3 ratus, 2 puluh dan 5 sa: 300 + 20 + 5.' },
        explain: { en: '325 = 300 + 20 + 5, so 3 hundreds, 2 tens and 5 ones.', ms: '325 = 300 + 20 + 5, jadi 3 ratus, 2 puluh dan 5 sa.' },
        spec: { places: [100, 10, 1], target: 325 }
      },
      {
        id: 'm2-3-b', type: 'placeValue',
        prompt: { en: 'Build the number 4,072.', ms: 'Bina nombor 4,072.' },
        hint: { en: 'Four thousands, no hundreds, seven tens and two ones.', ms: 'Empat ribu, tiada ratus, tujuh puluh dan dua sa.' },
        explain: { en: '4,072 = 4,000 + 0 + 70 + 2.', ms: '4,072 = 4,000 + 0 + 70 + 2.' },
        spec: { places: [1000, 100, 10, 1], target: 4072 }
      },
      {
        id: 'm2-3-c', type: 'digitArrange',
        prompt: { en: 'Arrange the tiles to make the smallest 4-digit number. A number cannot start with 0.', ms: 'Susun jubin untuk membentuk nombor 4 digit yang paling kecil. Nombor tidak boleh bermula dengan 0.' },
        hint: { en: 'Put the smallest digit that is allowed in the thousands place first.', ms: 'Letakkan digit terkecil yang dibenarkan pada tempat ribu dahulu.' },
        explain: { en: 'The smallest digit that is not 0 is 3, then 0, 5, 8: 3,058.', ms: 'Digit terkecil selain 0 ialah 3, kemudian 0, 5, 8: 3,058.' },
        spec: { digits: [5, 0, 8, 3], goal: 'smallest', noLeadingZero: true }
      }
    ]
  });

  /* ---------------- m2-4  Ferry Tickets (money — coins) ---------------- */
  L.register({
    id: 'm2-4', pack: 'free-demo', island: 'forest', order: 8,
    topic: 'operations', skill: 'money', band: 'adventurer', scene: 'ferry', npc: 'tock',
    title: { en: 'Ferry Tickets', ms: 'Tiket Feri' },
    story: {
      en: 'The ferry ticket machine only accepts the exact money. Tap coins to pay!',
      ms: 'Mesin tiket feri hanya menerima wang yang tepat. Ketik syiling untuk membayar!'
    },
    learn: { en: 'Make amounts of money (ringgit and sen).', ms: 'Membentuk jumlah wang (ringgit dan sen).' },
    critter: {
      id: 'ticketty', name: { en: 'Ticketty', ms: 'Ticketty' },
      blurb: { en: 'Ticketty always has the exact change.', ms: 'Ticketty sentiasa ada wang yang tepat.' },
      look: { body: 'round', c1: '#8fd0ff', c2: '#4aa8f0', ears: 'none', feat: 'fin', acc: 'scarf' }
    },
    tiers: [
      {
        id: 'm2-4-a', type: 'coins',
        prompt: { en: 'Pay exactly 70 sen.', ms: 'Bayar tepat 70 sen.' },
        hint: { en: 'Try 50 sen first. How much more do you need?', ms: 'Cuba 50 sen dahulu. Berapa lagi yang diperlukan?' },
        explain: { en: '50 + 20 = 70 sen.', ms: '50 + 20 = 70 sen.' },
        spec: { target: 70, coins: [5, 10, 20, 50] }
      },
      {
        id: 'm2-4-b', type: 'coins',
        prompt: { en: 'Pay exactly RM1.35.', ms: 'Bayar tepat RM1.35.' },
        hint: { en: 'RM1 is 100 sen. Then 35 sen is left to pay.', ms: 'RM1 ialah 100 sen. Kemudian tinggal 35 sen untuk dibayar.' },
        explain: { en: '100 + 20 + 10 + 5 = 135 sen = RM1.35.', ms: '100 + 20 + 10 + 5 = 135 sen = RM1.35.' },
        spec: { target: 135, coins: [5, 10, 20, 50, 100] }
      },
      {
        id: 'm2-4-c', type: 'coins',
        prompt: { en: 'Pay exactly RM2.45 using exactly 5 pieces of money.', ms: 'Bayar tepat RM2.45 menggunakan tepat 5 keping wang.' },
        hint: { en: 'Two RM1 notes make RM2. Then 45 sen is left — use 3 coins.', ms: 'Dua keping RM1 ialah RM2. Kemudian tinggal 45 sen — guna 3 keping syiling.' },
        explain: { en: '100 + 100 + 20 + 20 + 5 = 245 sen, using 5 pieces.', ms: '100 + 100 + 20 + 20 + 5 = 245 sen, menggunakan 5 keping.' },
        spec: { target: 245, coins: [5, 10, 20, 50, 100], exactCount: 5 }
      }
    ]
  });
})();
