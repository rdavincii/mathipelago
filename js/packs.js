/*
 * packs.js — content packs (what can be sold).
 *
 * Only the FREE pack's levels are in the main bundle. The premium packs below are descriptions used by the
 * preview screen and the map; their puzzles live in /packs/<id>.js and are loaded only for owners
 * (in this test build: when MP.config.devUnlockPremium is true). In production a backend serves those files
 * only to paying customers (see docs/ARCHITECTURE.md).
 *
 * Pack format: { id, free, levels:n, testFile, island:{id, order, npc, pack, name, blurb}, name, blurb, topics:[{en,ms}] }
 * The island id doubles as its map/background theme (see js/art.js).
 */
(function () {
  'use strict';
  var MP = (window.MP = window.MP || {});

  var PACKS = [
    {
      id: 'free-demo', free: true, levels: 12,
      name: { en: 'The Starter Islands (free)', ms: 'Pulau Permulaan (percuma)' },
      blurb: { en: 'Three islands, twelve puzzles, and your first twelve companions.', ms: 'Tiga pulau, dua belas teka-teki, dan dua belas rakan pertama anda.' },
      topics: []
    },
    {
      id: "crystal-caves", free: false, levels: 10, testFile: true,
      island: { id: "cave", order: 4, npc: "glim", pack: "crystal-caves", name: {"en": "Crystal Caves", "ms": "Gua Kristal"}, blurb: {"en": "Glowing caves where every crystal is a piece of a whole.", "ms": "Gua bercahaya di mana setiap kristal ialah sebahagian daripada satu keseluruhan."} },
      name: {"en": "Fractions & the Crystal Caves", "ms": "Pecahan & Gua Kristal"},
      blurb: {"en": "Glowing caves where every crystal is a piece of a whole.", "ms": "Gua bercahaya di mana setiap kristal ialah sebahagian daripada satu keseluruhan."},
      topics: [{"en": "Fractions of a whole", "ms": "Pecahan sebagai sebahagian daripada keseluruhan"}, {"en": "Fractions, decimals and percentages", "ms": "Pecahan, perpuluhan dan peratus"}, {"en": "Patterns, money and averages", "ms": "Pola, wang dan purata"}]
    },
    {
      id: "floating-gardens", free: false, levels: 10, testFile: true,
      island: { id: "garden", order: 5, npc: "petal", pack: "floating-gardens", name: {"en": "Floating Gardens", "ms": "Taman Terapung"}, blurb: {"en": "Garden paths in the sky, built with shapes, perimeter and area.", "ms": "Laluan taman di langit, dibina dengan bentuk, perimeter dan luas."} },
      name: {"en": "Geometry & the Floating Gardens", "ms": "Geometri & Taman Terapung"},
      blurb: {"en": "Garden paths in the sky, built with shapes, perimeter and area.", "ms": "Laluan taman di langit, dibina dengan bentuk, perimeter dan luas."},
      topics: [{"en": "Perimeter and area", "ms": "Perimeter dan luas"}, {"en": "Polygons and sides", "ms": "Poligon dan sisi"}, {"en": "Big numbers, sharing and multi-step problems", "ms": "Nombor besar, perkongsian dan masalah berbilang langkah"}]
    },
    {
      id: "mechanical-forest", free: false, levels: 10, testFile: true,
      island: { id: "foundry", order: 6, npc: "cogg", pack: "mechanical-forest", name: {"en": "Mechanical Forest", "ms": "Hutan Mekanikal"}, blurb: {"en": "Power giant machines with times tables, factors and multiples.", "ms": "Hidupkan mesin gergasi dengan sifir, faktor dan gandaan."} },
      name: {"en": "Multiplication & the Mechanical Forest", "ms": "Pendaraban & Hutan Mekanikal"},
      blurb: {"en": "Power giant machines with times tables, factors and multiples.", "ms": "Hidupkan mesin gergasi dengan sifir, faktor dan gandaan."},
      topics: [{"en": "Times tables and arrays", "ms": "Sifir dan tatasusunan"}, {"en": "Factors and multiples", "ms": "Faktor dan gandaan"}, {"en": "Long multiplication and division", "ms": "Darab dan bahagi panjang"}]
    },
    {
      id: "hidden-city", free: false, levels: 10, testFile: true,
      island: { id: "city", order: 7, npc: "sleuth", pack: "hidden-city", name: {"en": "Hidden City", "ms": "Bandar Tersembunyi"}, blurb: {"en": "Crack codes and follow clues through a secret miniature city.", "ms": "Pecahkan kod dan ikuti petunjuk melalui sebuah bandar kecil yang rahsia."} },
      name: {"en": "Logic & the Hidden City", "ms": "Logik & Bandar Tersembunyi"},
      blurb: {"en": "Crack codes and follow clues through a secret miniature city.", "ms": "Pecahkan kod dan ikuti petunjuk melalui sebuah bandar kecil yang rahsia."},
      topics: [{"en": "Number puzzles and balance", "ms": "Teka-teki nombor dan keseimbangan"}, {"en": "Ratio and proportion", "ms": "Nisbah dan kadaran"}, {"en": "Multi-step problems", "ms": "Masalah berbilang langkah"}]
    },
    {
      id: "clock-harbour", free: false, levels: 10, testFile: true,
      island: { id: "harbour", order: 8, npc: "tick", pack: "clock-harbour", name: {"en": "Clock Harbour", "ms": "Pelabuhan Jam"}, blurb: {"en": "A busy harbour where every ship leaves on time.", "ms": "Sebuah pelabuhan sibuk di mana setiap kapal bertolak tepat pada masanya."} },
      name: {"en": "Time & Clock Harbour", "ms": "Masa & Pelabuhan Jam"},
      blurb: {"en": "A busy harbour where every ship leaves on time.", "ms": "Sebuah pelabuhan sibuk di mana setiap kapal bertolak tepat pada masanya."},
      topics: [{"en": "Hours, minutes and seconds", "ms": "Jam, minit dan saat"}, {"en": "Timetables and durations", "ms": "Jadual waktu dan tempoh"}, {"en": "Days, weeks and calendars", "ms": "Hari, minggu dan kalendar"}]
    },
    {
      id: "spice-market", free: false, levels: 10, testFile: true,
      island: { id: "market", order: 9, npc: "mango", pack: "spice-market", name: {"en": "Spice Market", "ms": "Pasar Rempah"}, blurb: {"en": "A lively market with prices, change and measuring.", "ms": "Pasar yang meriah dengan harga, baki dan ukuran."} },
      name: {"en": "Money & the Spice Market", "ms": "Wang & Pasar Rempah"},
      blurb: {"en": "A lively market with prices, change and measuring.", "ms": "Pasar yang meriah dengan harga, baki dan ukuran."},
      topics: [{"en": "Money, prices and change", "ms": "Wang, harga dan baki"}, {"en": "Length, mass and volume", "ms": "Panjang, jisim dan isi padu"}, {"en": "Shopping problems", "ms": "Masalah membeli-belah"}]
    },
    {
      id: "decimal-dunes", free: false, levels: 10, testFile: true,
      island: { id: "desert", order: 10, npc: "dune", pack: "decimal-dunes", name: {"en": "Decimal Dunes", "ms": "Bukit Pasir Perpuluhan"}, blurb: {"en": "Golden dunes where numbers have a point.", "ms": "Bukit pasir keemasan di mana nombor mempunyai titik perpuluhan."} },
      name: {"en": "Decimals & the Decimal Dunes", "ms": "Perpuluhan & Bukit Pasir Perpuluhan"},
      blurb: {"en": "Golden dunes where numbers have a point.", "ms": "Bukit pasir keemasan di mana nombor mempunyai titik perpuluhan."},
      topics: [{"en": "Decimal place value", "ms": "Nilai tempat perpuluhan"}, {"en": "Adding and subtracting decimals", "ms": "Menambah dan menolak perpuluhan"}, {"en": "Rounding and estimating", "ms": "Pembundaran dan anggaran"}]
    },
    {
      id: "frost-peaks", free: false, levels: 10, testFile: true,
      island: { id: "snow", order: 11, npc: "frost", pack: "frost-peaks", name: {"en": "Frost Peaks", "ms": "Puncak Salji"}, blurb: {"en": "Icy mountains where numbers go below zero.", "ms": "Gunung berais di mana nombor turun di bawah sifar."} },
      name: {"en": "Negatives & the Frost Peaks", "ms": "Nombor Negatif & Puncak Salji"},
      blurb: {"en": "Icy mountains where numbers go below zero.", "ms": "Gunung berais di mana nombor turun di bawah sifar."},
      topics: [{"en": "Negative numbers and temperature", "ms": "Nombor negatif dan suhu"}, {"en": "Number sequences and rules", "ms": "Jujukan nombor dan petua"}, {"en": "Balancing and simple algebra", "ms": "Mengimbang dan algebra mudah"}]
    },
    {
      id: "data-reef", free: false, levels: 10, testFile: true,
      island: { id: "reef", order: 12, npc: "coral", pack: "data-reef", name: {"en": "Coral Reef", "ms": "Terumbu Karang"}, blurb: {"en": "Count the fish, read the charts and find the average.", "ms": "Kira ikan, baca carta dan cari purata."} },
      name: {"en": "Data & the Coral Reef", "ms": "Data & Terumbu Karang"},
      blurb: {"en": "Count the fish, read the charts and find the average.", "ms": "Kira ikan, baca carta dan cari purata."},
      topics: [{"en": "Bar charts and totals", "ms": "Carta palang dan jumlah"}, {"en": "Mean (average)", "ms": "Min (purata)"}, {"en": "Shapes and patterns in data", "ms": "Bentuk dan pola dalam data"}]
    },
    {
      id: "star-station", free: false, levels: 10, testFile: true,
      island: { id: "space", order: 13, npc: "nova", pack: "star-station", name: {"en": "Star Station", "ms": "Stesen Bintang"}, blurb: {"en": "The hardest puzzles, mixing everything you have learned.", "ms": "Teka-teki paling sukar, menggabungkan semua yang telah anda pelajari."} },
      name: {"en": "Champion Challenges & Star Station", "ms": "Cabaran Juara & Stesen Bintang"},
      blurb: {"en": "The hardest puzzles, mixing everything you have learned.", "ms": "Teka-teki paling sukar, menggabungkan semua yang telah anda pelajari."},
      topics: [{"en": "Mixed review of every topic", "ms": "Ulang kaji campuran semua topik"}, {"en": "Multi-step reasoning", "ms": "Penaakulan berbilang langkah"}, {"en": "Speed and accuracy", "ms": "Kelajuan dan ketepatan"}]
    },
    {
      id: "ember-volcano", free: false, levels: 10, testFile: true,
      island: { id: "volcano", order: 14, npc: "ember", pack: "ember-volcano", name: {"en": "Ember Volcano", "ms": "Gunung Berapi Ember"}, blurb: {"en": "Times tables, multiples and factors heat up!", "ms": "Sifir, gandaan dan faktor semakin hangat!"} },
      name: {"en": "Champion Tables & Ember Volcano", "ms": "Sifir Juara & Gunung Berapi Ember"},
      blurb: {"en": "Times tables, multiples and factors heat up!", "ms": "Sifir, gandaan dan faktor semakin hangat!"},
      topics: [{"en": "Times tables and division", "ms": "Sifir dan pembahagian"}, {"en": "Multiples and factors", "ms": "Gandaan dan faktor"}, {"en": "Arrays and multi-step problems", "ms": "Tatasusunan dan masalah berbilang langkah"}]
    },
    {
      id: "pirate-cove", free: false, levels: 10, testFile: true,
      island: { id: "pirate", order: 15, npc: "jolly", pack: "pirate-cove", name: {"en": "Pirate Cove", "ms": "Teluk Lanun"}, blurb: {"en": "Count the treasure with big numbers and coins.", "ms": "Kira harta karun dengan nombor besar dan syiling."} },
      name: {"en": "Treasure Maths & Pirate Cove", "ms": "Matematik Harta Karun & Teluk Lanun"},
      blurb: {"en": "Count the treasure with big numbers and coins.", "ms": "Kira harta karun dengan nombor besar dan syiling."},
      topics: [{"en": "Adding and subtracting big numbers", "ms": "Menambah dan menolak nombor besar"}, {"en": "Money and coins", "ms": "Wang dan syiling"}, {"en": "Place value to 10,000", "ms": "Nilai tempat hingga 10,000"}]
    },
    {
      id: "jungle-canopy", free: false, levels: 10, testFile: true,
      island: { id: "jungle", order: 16, npc: "vine", pack: "jungle-canopy", name: {"en": "Jungle Canopy", "ms": "Kanopi Hutan Belantara"}, blurb: {"en": "Swing through shapes, perimeter and area.", "ms": "Berayun melalui bentuk, perimeter dan luas."} },
      name: {"en": "Shape Safari & Jungle Canopy", "ms": "Safari Bentuk & Kanopi Hutan Belantara"},
      blurb: {"en": "Swing through shapes, perimeter and area.", "ms": "Berayun melalui bentuk, perimeter dan luas."},
      topics: [{"en": "Shapes and sides", "ms": "Bentuk dan sisi"}, {"en": "Perimeter and area", "ms": "Perimeter dan luas"}, {"en": "Patterns and charts", "ms": "Pola dan carta"}]
    },
    {
      id: "candy-kingdom", free: false, levels: 10, testFile: true,
      island: { id: "candy", order: 17, npc: "sprinkle", pack: "candy-kingdom", name: {"en": "Candy Kingdom", "ms": "Kerajaan Gula-gula"}, blurb: {"en": "Share sweets fairly with fractions, ratio and percentages.", "ms": "Kongsi gula-gula dengan adil menggunakan pecahan, nisbah dan peratus."} },
      name: {"en": "Sweet Fractions & Candy Kingdom", "ms": "Pecahan Manis & Kerajaan Gula-gula"},
      blurb: {"en": "Share sweets fairly with fractions, ratio and percentages.", "ms": "Kongsi gula-gula dengan adil menggunakan pecahan, nisbah dan peratus."},
      topics: [{"en": "Fractions and equivalents", "ms": "Pecahan dan pecahan setara"}, {"en": "Ratio and sharing", "ms": "Nisbah dan perkongsian"}, {"en": "Percentages as hundredths", "ms": "Peratus sebagai perseratus"}]
    },
    {
      id: "dino-valley", free: false, levels: 10, testFile: true,
      island: { id: "dino", order: 18, npc: "rex", pack: "dino-valley", name: {"en": "Dino Valley", "ms": "Lembah Dinosaur"}, blurb: {"en": "Huge numbers from the time of the dinosaurs.", "ms": "Nombor yang sangat besar dari zaman dinosaur."} },
      name: {"en": "Giant Numbers & Dino Valley", "ms": "Nombor Gergasi & Lembah Dinosaur"},
      blurb: {"en": "Huge numbers from the time of the dinosaurs.", "ms": "Nombor yang sangat besar dari zaman dinosaur."},
      topics: [{"en": "Place value and rounding", "ms": "Nilai tempat dan pembundaran"}, {"en": "Ordering big numbers", "ms": "Menyusun nombor besar"}, {"en": "Time and length", "ms": "Masa dan panjang"}]
    },
    {
      id: "robot-factory", free: false, levels: 10, testFile: true,
      island: { id: "robot", order: 19, npc: "bolt", pack: "robot-factory", name: {"en": "Robot Factory", "ms": "Kilang Robot"}, blurb: {"en": "Rules, patterns and machines that think in numbers.", "ms": "Peraturan, pola dan mesin yang berfikir dengan nombor."} },
      name: {"en": "Rule Machines & Robot Factory", "ms": "Mesin Peraturan & Kilang Robot"},
      blurb: {"en": "Rules, patterns and machines that think in numbers.", "ms": "Peraturan, pola dan mesin yang berfikir dengan nombor."},
      topics: [{"en": "Pattern rules", "ms": "Peraturan pola"}, {"en": "Function machines", "ms": "Mesin fungsi"}, {"en": "Factors and multiples", "ms": "Faktor dan gandaan"}]
    },
    {
      id: "sports-arena", free: false, levels: 10, testFile: true,
      island: { id: "arena", order: 20, npc: "goal", pack: "sports-arena", name: {"en": "Sports Arena", "ms": "Arena Sukan"}, blurb: {"en": "Scores, times and charts on sports day.", "ms": "Markah, masa dan carta pada hari sukan."} },
      name: {"en": "Scoreboard Maths & Sports Arena", "ms": "Matematik Papan Markah & Arena Sukan"},
      blurb: {"en": "Scores, times and charts on sports day.", "ms": "Markah, masa dan carta pada hari sukan."},
      topics: [{"en": "Reading and using charts", "ms": "Membaca dan menggunakan carta"}, {"en": "Time and decimals", "ms": "Masa dan perpuluhan"}, {"en": "Money and multi-step scores", "ms": "Wang dan markah berbilang langkah"}]
    },
    {
      id: "castle-keep", free: false, levels: 10, testFile: true,
      island: { id: "castle", order: 21, npc: "knight", pack: "castle-keep", name: {"en": "Castle Keep", "ms": "Kubu Istana"}, blurb: {"en": "Measure the castle: area, perimeter and more.", "ms": "Ukur istana: luas, perimeter dan banyak lagi."} },
      name: {"en": "Castle Builders & Castle Keep", "ms": "Pembina Istana & Kubu Istana"},
      blurb: {"en": "Measure the castle: area, perimeter and more.", "ms": "Ukur istana: luas, perimeter dan banyak lagi."},
      topics: [{"en": "Area and perimeter", "ms": "Luas dan perimeter"}, {"en": "Shapes and sides", "ms": "Bentuk dan sisi"}, {"en": "Multiplication in context", "ms": "Pendaraban dalam konteks"}]
    },
    {
      id: "rainbow-bridge", free: false, levels: 10, testFile: true,
      island: { id: "rainbow", order: 22, npc: "arc", pack: "rainbow-bridge", name: {"en": "Rainbow Bridge", "ms": "Jambatan Pelangi"}, blurb: {"en": "Cross the bridge with fractions, decimals and ratios.", "ms": "Seberangi jambatan dengan pecahan, perpuluhan dan nisbah."} },
      name: {"en": "Rainbow Fractions & Rainbow Bridge", "ms": "Pecahan Pelangi & Jambatan Pelangi"},
      blurb: {"en": "Cross the bridge with fractions, decimals and ratios.", "ms": "Seberangi jambatan dengan pecahan, perpuluhan dan nisbah."},
      topics: [{"en": "Fractions on the line", "ms": "Pecahan pada garis"}, {"en": "Decimals and percentages", "ms": "Perpuluhan dan peratus"}, {"en": "Ratio and patterns", "ms": "Nisbah dan pola"}]
    },
    {
      id: "carnival-night", free: false, levels: 10, testFile: true,
      island: { id: "carnival", order: 23, npc: "jester", pack: "carnival-night", name: {"en": "Carnival Night", "ms": "Malam Karnival"}, blurb: {"en": "The grand finale: every skill in one big show.", "ms": "Kemuncak besar: setiap kemahiran dalam satu persembahan besar."} },
      name: {"en": "Grand Finale & Carnival Night", "ms": "Kemuncak Besar & Malam Karnival"},
      blurb: {"en": "The grand finale: every skill in one big show.", "ms": "Kemuncak besar: setiap kemahiran dalam satu persembahan besar."},
      topics: [{"en": "Mixed review of every topic", "ms": "Ulang kaji campuran semua topik"}, {"en": "Hardest multi-step puzzles", "ms": "Teka-teki berbilang langkah paling sukar"}, {"en": "Speed and accuracy", "ms": "Kelajuan dan ketepatan"}]
    },
    {
      id: "kampung-village", free: false, levels: 10, testFile: true,
      island: { id: "kampung", order: 24, npc: "ayam", pack: "kampung-village", name: {"en": "Kampung Village", "ms": "Kampung Village"}, blurb: {"en": "Money, measures and sharing in village life.", "ms": "Wang, sukatan dan perkongsian dalam kehidupan kampung."} },
      name: {"en": "Kampung Village", "ms": "Kampung Village"},
      blurb: {"en": "Money, measures and sharing in village life.", "ms": "Wang, sukatan dan perkongsian dalam kehidupan kampung."},
      topics: [{"en": "Money and change", "ms": "Wang dan baki"}, {"en": "Length and measures", "ms": "Panjang dan sukatan"}, {"en": "Sharing equally", "ms": "Berkongsi sama banyak"}]
    },
    {
      id: "night-market", free: false, levels: 10, testFile: true,
      island: { id: "nightmarket", order: 25, npc: "satay", pack: "night-market", name: {"en": "Night Market", "ms": "Pasar Malam"}, blurb: {"en": "Bargains, totals and change at the night stalls.", "ms": "Tawaran, jumlah dan baki di gerai malam."} },
      name: {"en": "Night Market", "ms": "Pasar Malam"},
      blurb: {"en": "Bargains, totals and change at the night stalls.", "ms": "Tawaran, jumlah dan baki di gerai malam."},
      topics: [{"en": "Adding prices", "ms": "Menambah harga"}, {"en": "Making change", "ms": "Membuat baki"}, {"en": "Multi-step shopping", "ms": "Membeli-belah berbilang langkah"}]
    },
    {
      id: "kite-fields", free: false, levels: 10, testFile: true,
      island: { id: "kites", order: 26, npc: "layang", pack: "kite-fields", name: {"en": "Kite Fields", "ms": "Padang Layang-layang"}, blurb: {"en": "Patterns, lines and shapes in the sky.", "ms": "Pola, garis dan bentuk di langit."} },
      name: {"en": "Kite Fields", "ms": "Padang Layang-layang"},
      blurb: {"en": "Patterns, lines and shapes in the sky.", "ms": "Pola, garis dan bentuk di langit."},
      topics: [{"en": "Number patterns", "ms": "Pola nombor"}, {"en": "Number lines", "ms": "Garis nombor"}, {"en": "Shapes and sides", "ms": "Bentuk dan sisi"}]
    },
    {
      id: "train-station", free: false, levels: 10, testFile: true,
      island: { id: "train", order: 27, npc: "choo", pack: "train-station", name: {"en": "Train Station", "ms": "Stesen Kereta Api"}, blurb: {"en": "Timetables, time and rules on the tracks.", "ms": "Jadual, masa dan peraturan di landasan."} },
      name: {"en": "Train Station", "ms": "Stesen Kereta Api"},
      blurb: {"en": "Timetables, time and rules on the tracks.", "ms": "Jadual, masa dan peraturan di landasan."},
      topics: [{"en": "Telling time", "ms": "Menyebut masa"}, {"en": "Timetable sums", "ms": "Kira jadual"}, {"en": "Rule patterns", "ms": "Pola peraturan"}]
    },
    {
      id: "bakery-bay", free: false, levels: 10, testFile: true,
      island: { id: "bakery", order: 28, npc: "bun", pack: "bakery-bay", name: {"en": "Bakery Bay", "ms": "Teluk Bakeri"}, blurb: {"en": "Fractions, ratios and recipes.", "ms": "Pecahan, nisbah dan resipi."} },
      name: {"en": "Bakery Bay", "ms": "Teluk Bakeri"},
      blurb: {"en": "Fractions, ratios and recipes.", "ms": "Pecahan, nisbah dan resipi."},
      topics: [{"en": "Fractions of a whole", "ms": "Pecahan satu keseluruhan"}, {"en": "Ratio and recipes", "ms": "Nisbah dan resipi"}, {"en": "Sharing cakes", "ms": "Berkongsi kek"}]
    },
    {
      id: "deep-ocean", free: false, levels: 10, testFile: true,
      island: { id: "deep", order: 29, npc: "bubbo", pack: "deep-ocean", name: {"en": "Deep Ocean", "ms": "Lautan Dalam"}, blurb: {"en": "Negatives, depths and big numbers below the waves.", "ms": "Nombor negatif, kedalaman dan nombor besar di bawah ombak."} },
      name: {"en": "Deep Ocean", "ms": "Lautan Dalam"},
      blurb: {"en": "Negatives, depths and big numbers below the waves.", "ms": "Nombor negatif, kedalaman dan nombor besar di bawah ombak."},
      topics: [{"en": "Negative numbers", "ms": "Nombor negatif"}, {"en": "Place value", "ms": "Nilai tempat"}, {"en": "Rounding", "ms": "Pembulatan"}]
    },
    {
      id: "zoo-park", free: false, levels: 10, testFile: true,
      island: { id: "zoo", order: 30, npc: "zebra", pack: "zoo-park", name: {"en": "Zoo Park", "ms": "Taman Zoo"}, blurb: {"en": "Feeding, charts and fractions at the zoo.", "ms": "Memberi makan, carta dan pecahan di zoo."} },
      name: {"en": "Zoo Park", "ms": "Taman Zoo"},
      blurb: {"en": "Feeding, charts and fractions at the zoo.", "ms": "Memberi makan, carta dan pecahan di zoo."},
      topics: [{"en": "Multi-step feeding", "ms": "Memberi makan berbilang langkah"}, {"en": "Reading charts", "ms": "Membaca carta"}, {"en": "Fractions", "ms": "Pecahan"}]
    },
    {
      id: "toy-workshop", free: false, levels: 10, testFile: true,
      island: { id: "toys", order: 31, npc: "teddy", pack: "toy-workshop", name: {"en": "Toy Workshop", "ms": "Bengkel Mainan"}, blurb: {"en": "Machines, rules and balancing blocks.", "ms": "Mesin, peraturan dan blok yang seimbang."} },
      name: {"en": "Toy Workshop", "ms": "Bengkel Mainan"},
      blurb: {"en": "Machines, rules and balancing blocks.", "ms": "Mesin, peraturan dan blok yang seimbang."},
      topics: [{"en": "Rule machines", "ms": "Mesin peraturan"}, {"en": "Balancing totals", "ms": "Mengimbangkan jumlah"}, {"en": "Multiplication facts", "ms": "Fakta darab"}]
    },
    {
      id: "treehouse-town", free: false, levels: 10, testFile: true,
      island: { id: "treehouse", order: 32, npc: "acorn", pack: "treehouse-town", name: {"en": "Treehouse Town", "ms": "Pekan Rumah Pokok"}, blurb: {"en": "Perimeter, area and building high.", "ms": "Perimeter, luas dan membina tinggi."} },
      name: {"en": "Treehouse Town", "ms": "Pekan Rumah Pokok"},
      blurb: {"en": "Perimeter, area and building high.", "ms": "Perimeter, luas dan membina tinggi."},
      topics: [{"en": "Perimeter", "ms": "Perimeter"}, {"en": "Area", "ms": "Luas"}, {"en": "Number sense", "ms": "Pemahaman nombor"}]
    },
    {
      id: "lantern-festival", free: false, levels: 10, testFile: true,
      island: { id: "festival", order: 33, npc: "lampu", pack: "lantern-festival", name: {"en": "Lantern Festival", "ms": "Pesta Tanglung"}, blurb: {"en": "The grand finale: every skill under the lanterns.", "ms": "Kemuncak besar: setiap kemahiran di bawah tanglung."} },
      name: {"en": "Lantern Festival", "ms": "Pesta Tanglung"},
      blurb: {"en": "The grand finale: every skill under the lanterns.", "ms": "Kemuncak besar: setiap kemahiran di bawah tanglung."},
      topics: [{"en": "Mixed review", "ms": "Ulang kaji campuran"}, {"en": "Hardest multi-step puzzles", "ms": "Teka-teki berbilang langkah paling sukar"}, {"en": "Speed and accuracy", "ms": "Kelajuan dan ketepatan"}]
    }
  ];

  MP.packs = {
    all: function () { return PACKS.slice(); },
    premium: function () { return PACKS.filter(function (p) { return !p.free; }); },
    /** Free islands + the island each premium pack adds, in map order (lowest first). */
    allIslands: function () {
      return MP.islands.concat(PACKS.filter(function (x) { return x.island; }).map(function (x) { return x.island; }));
    },
    byId: function (id) { return PACKS.filter(function (p) { return p.id === id; })[0] || null; }
  };
})();
