from lib import *
CODE, BASE = 'zp', 272
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'
KG = lambda v: f'{v} kg'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'operations', 'times-tables', 'adventurer', 'door',
        T('Feeding Time Facts', 'Fakta Waktu Makan'),
        T('The zoo gate opens when every feeding fact finds its answer. Match them!', 'Pintu zoo terbuka apabila setiap fakta waktu makan menemui jawapannya. Padankan mereka!'),
        T('Multiplication facts in feeding problems.', 'Fakta darab dalam masalah memberi makan.'),
        'Stripey', T('Stripey counts every banana twice.', 'Stripey mengira setiap pisang dua kali.'),
        [match([('6 × 8', '48'), ('7 × 7', '49'), ('9 × 4', '36')], MP_, T('Count in steps of the first number.', 'Kira dengan langkah nombor pertama.')),
         match([('8 × 5', '40'), ('7 × 6', '42'), ('9 × 7', '63'), ('12 × 3', '36')], MP_, T('Break a fact into two easier facts.', 'Pecahkan satu fakta kepada dua fakta yang lebih mudah.')),
         match([('8 × 9', '72'), ('7 × 8', '56'), ('11 × 6', '66'), ('12 × 7', '84'), ('9 × 9', '81')], MP_, T('Use a fact you know and add or subtract one group.', 'Guna fakta yang anda tahu dan tambah atau tolak satu kumpulan.'))])
    add(2, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Paw Prints', 'Tapak Kaki'),
        T('Animal paw prints walk across the path in a pattern. Which number comes next?', 'Tapak kaki haiwan berjalan di sepanjang laluan dalam satu pola. Nombor manakah seterusnya?'),
        T('Continue number patterns.', 'Menyambung pola nombor.'),
        'Pawly', T('Pawly leaves the neatest prints in the zoo.', 'Pawly meninggalkan tapak kaki paling kemas di zoo.'),
        [pattern('arith', 5, 5, 5, seed='zp2a'), pattern('geo', 3, 2, 5, seed='zp2b'), pattern('arith', 48, -6, 6, hidden=3, seed='zp2c')])
    add(3, 'operations', 'multiplication', 'adventurer', 'ferry',
        T('Hungry Zoo', 'Zoo yang Lapar'),
        T('The keeper must feed every animal. Work out the food in three steps!', 'Penjaga mesti memberi makan setiap haiwan. Kira makanan dalam tiga langkah!'),
        T('Multiply, then add or share in short chains.', 'Mendarab, kemudian menambah atau berkongsi dalam rantaian pendek.'),
        'Munchy', T('Munchy never says no to a snack.', 'Munchy tidak pernah menolak snek.'),
        [steps([step(T('Each monkey eats 4 bananas a day. How many bananas do 7 monkeys eat in a day?', 'Setiap monyet makan 4 biji pisang sehari. Berapa biji pisang dimakan oleh 7 ekor monyet sehari?'), 28, '7*4'),
                step(T('How many bananas do they eat in 3 days?', 'Berapa biji pisang yang mereka makan dalam 3 hari?'), 84, '28*3'),
                step(T('The bananas come in bunches of 6. How many bunches are needed?', 'Pisang itu datang dalam sesikat 6 biji. Berapa sikat yang diperlukan?'), 14, '84/6')],
               T('Multiply for one day, then for 3 days.', 'Darab untuk satu hari, kemudian untuk 3 hari.'), T('7 × 4 = 28, then 28 × 3 = 84, then 84 ÷ 6 = 14.', '7 × 4 = 28, kemudian 28 × 3 = 84, kemudian 84 ÷ 6 = 14.'), 'zp3a'),
         steps([step(T('A keeper feeds 9 elephants 8 kg of hay each. How many kilograms of hay is that?', 'Seorang penjaga memberi 9 ekor gajah 8 kg jerami seorang. Berapa kilogram jerami itu?'), 72, '9*8', KG),
                step(T('A bale of hay holds 12 kg. How many bales are needed?', 'Seikat jerami memuatkan 12 kg. Berapa ikat yang diperlukan?'), 6, '72/12'),
                step(T('Each bale costs RM15. How much do all the bales cost?', 'Setiap ikat berharga RM15. Berapa harga semua ikat itu?'), 90, '6*15', RM)],
               T('Find the total hay first.', 'Cari jumlah jerami dahulu.'), T('9 × 8 = 72, then 72 ÷ 12 = 6, then 6 × 15 = 90.', '9 × 8 = 72, kemudian 72 ÷ 12 = 6, kemudian 6 × 15 = 90.'), 'zp3b'),
         steps([step(T('12 penguins eat 5 fish each. How many fish do they eat?', '12 ekor penguin makan 5 ekor ikan seekor. Berapa ekor ikan yang mereka makan?'), 60, '12*5'),
                step(T('The keeper adds 15 extra fish. How many fish are there now?', 'Penjaga menambah 15 ekor ikan lagi. Berapa ekor ikan sekarang?'), 75, '60+15'),
                step(T('The fish are shared equally between 3 pools. How many fish in each pool?', 'Ikan itu dikongsi sama banyak antara 3 kolam. Berapa ekor ikan dalam setiap kolam?'), 25, '75/3')],
               T('Multiply, then add, then share.', 'Darab, kemudian tambah, kemudian kongsi.'), T('12 × 5 = 60, then 60 + 15 = 75, then 75 ÷ 3 = 25.', '12 × 5 = 60, kemudian 60 + 15 = 75, kemudian 75 ÷ 3 = 25.'), 'zp3c')])
    add(4, 'shape-data', 'data', 'adventurer', 'lighthouse',
        T('Animal Count', 'Kiraan Haiwan'),
        T('The zoo counted the animals in each house. Read the chart!', 'Zoo mengira haiwan di setiap rumah. Baca carta itu!'),
        T('Read bar charts: differences, totals and subsets.', 'Membaca carta palang: beza, jumlah dan sebahagian.'),
        'Tallyho', T('Tallyho makes a tiny mark for every animal.', 'Tallyho membuat tanda kecil untuk setiap haiwan.'),
        [chart([(T('Lions', 'Singa'), 6, 'coral'), (T('Zebras', 'Zebra'), 9, 'sky'), (T('Monkeys', 'Monyet'), 14, 'sun')], ('diff', 2, 0), T('animals', 'haiwan')),
         chart([(T('Lions', 'Singa'), 12, 'coral'), (T('Zebras', 'Zebra'), 18, 'sky'), (T('Monkeys', 'Monyet'), 9, 'sun'), (T('Parrots', 'Burung kakak tua'), 15, 'mint')], ('sum', [0, 1, 2, 3]), T('animals', 'haiwan')),
         chart([(T('Lions', 'Singa'), 12, 'coral'), (T('Zebras', 'Zebra'), 18, 'sky'), (T('Monkeys', 'Monyet'), 24, 'sun'), (T('Parrots', 'Burung kakak tua'), 15, 'mint'), (T('Otters', 'Memerang'), 21, 'grape')], ('sum', [1, 4]), T('animals', 'haiwan'))])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Water Trough', 'Palung Air'),
        T('Fill each water trough to the right line before the animals get thirsty!', 'Isi setiap palung air hingga garisan yang betul sebelum haiwan menjadi dahaga!'),
        T('Fractions of a tank.', 'Pecahan sebuah tangki.'),
        'Sippy', T('Sippy loves a full trough.', 'Sippy sukakan palung yang penuh.'),
        [tank(8, 1, 2), tank(12, 2, 3), tank(10, 7, 10)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Zoo Picnic', 'Berkelah di Zoo'),
        T('Share the picnic fruit between the baskets so every animal gets the same!', 'Kongsi buah berkelah antara bakul supaya setiap haiwan mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Fruity', T('Fruity picks the juiciest fruit for last.', 'Fruity memilih buah paling berair untuk yang terakhir.'),
        [share(12, 3), share(20, 4), share(30, 5)])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Cage Numbers', 'Nombor Kandang'),
        T('Every cage holds the same number of animals. Find the two tiles that make each total!', 'Setiap kandang memuatkan bilangan haiwan yang sama. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Cagey', T('Cagey always knows how many are inside.', 'Cagey sentiasa tahu berapa ramai di dalam.'),
        [tiles(42, [6, 7, 3, 14, 8, 9]), tiles(56, [7, 8, 6, 9, 4, 14]), tiles(96, [8, 12, 6, 16, 4, 9])])
    add(8, 'number-sense', 'place-value', 'master', 'door',
        T('Visitor Tickets', 'Tiket Pengunjung'),
        T('The ticket machine prints big numbers. Build each number on the lock!', 'Mesin tiket mencetak nombor besar. Bina setiap nombor pada kunci!'),
        T('Build numbers up to 9,999 with place value.', 'Membina nombor sehingga 9,999 dengan nilai tempat.'),
        'Ticky', T('Ticky tears the tickets in neat lines.', 'Ticky mengoyak tiket dalam garisan yang kemas.'),
        [placevalue(275, [100, 10, 1]), placevalue(3140, [1000, 100, 10, 1]), placevalue(6805, [1000, 100, 10, 1])])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Zoo Chart', 'Carta Zoo'),
        T('The zoo kept a chart of how many treats each animal ate today. Read it!', 'Zoo menyimpan carta berapa banyak hidangan yang dimakan setiap haiwan hari ini. Bacalah!'),
        T('Read bar charts: differences and averages.', 'Membaca carta palang: beza dan purata.'),
        'Chartie', T('Chartie draws a very straight bar.', 'Chartie melukis palang yang sangat lurus.'),
        [chart([(T('Lions', 'Singa'), 28, 'coral'), (T('Zebras', 'Zebra'), 16, 'sky'), (T('Monkeys', 'Monyet'), 22, 'sun')], ('diff', 0, 1), T('treats', 'hidangan')),
         chart([(T('Lions', 'Singa'), 16, 'coral'), (T('Zebras', 'Zebra'), 24, 'sky'), (T('Monkeys', 'Monyet'), 12, 'sun'), (T('Parrots', 'Burung kakak tua'), 20, 'mint')], ('mean',), T('treats', 'hidangan')),
         chart([(T('Lions', 'Singa'), 12, 'coral'), (T('Zebras', 'Zebra'), 15, 'sky'), (T('Monkeys', 'Monyet'), 18, 'sun'), (T('Parrots', 'Burung kakak tua'), 9, 'mint'), (T('Otters', 'Memerang'), 21, 'grape')], ('mean',), T('treats', 'hidangan'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Zoo Finale', 'Kemuncak Zoo'),
        T('It is the zoo’s big birthday! Solve three steps to get everything ready.', 'Ini hari lahir besar zoo! Selesaikan tiga langkah untuk menyediakan segalanya.'),
        T('Multi-step problems with animals, money and sharing.', 'Masalah berbilang langkah dengan haiwan, wang dan perkongsian.'),
        'Roary', T('Roary roars the happiest birthday song.', 'Roary mengaum lagu hari jadi paling gembira.'),
        [steps([step(T('The zoo has 8 enclosures with 6 animals in each. How many animals?', 'Zoo mempunyai 8 kandang dengan 6 haiwan dalam setiap satu. Berapa haiwan?'), 48, '8*6'),
                step(T('15 animals go to a new zoo. How many animals are left?', '15 haiwan dihantar ke zoo baharu. Berapa haiwan yang tinggal?'), 33, '48-15'),
                step(T('27 new animals arrive. How many animals are there now?', '27 haiwan baharu tiba. Berapa haiwan sekarang?'), 60, '33+27')],
               T('Multiply, then subtract, then add.', 'Darab, kemudian tolak, kemudian tambah.'), T('8 × 6 = 48, then 48 − 15 = 33, then 33 + 27 = 60.', '8 × 6 = 48, kemudian 48 − 15 = 33, kemudian 33 + 27 = 60.'), 'zp10a'),
         steps([step(T('A zoo ticket costs RM12. What do 25 tickets cost?', 'Tiket zoo berharga RM12. Berapa harga 25 tiket?'), 300, '25*12', RM),
                step(T('The zoo spends RM80 on food. How much money is left?', 'Zoo membelanjakan RM80 untuk makanan. Berapa wang yang tinggal?'), 220, '300-80', RM),
                step(T('The rest is shared equally between 4 keepers. How much does each keeper get?', 'Bakinya dikongsi sama banyak antara 4 penjaga. Berapa yang diperoleh setiap penjaga?'), 55, '220/4', RM)],
               T('Multiply first, then take away the food.', 'Darab dahulu, kemudian tolak makanan.'), T('25 × 12 = 300, then 300 − 80 = 220, then 220 ÷ 4 = 55.', '25 × 12 = 300, kemudian 300 − 80 = 220, kemudian 220 ÷ 4 = 55.'), 'zp10b'),
         steps([step(T('A giraffe eats 30 kg of leaves a day. How many kilograms in 7 days?', 'Seekor zirafah makan 30 kg daun sehari. Berapa kilogram dalam 7 hari?'), 210, '30*7', KG),
                step(T('The zoo has 6 giraffes. How many kilograms do they eat in 7 days?', 'Zoo mempunyai 6 ekor zirafah. Berapa kilogram yang mereka makan dalam 7 hari?'), 1260, '210*6', KG),
                step(T('Leaves come in bags of 20 kg. How many bags are needed?', 'Daun datang dalam beg 20 kg. Berapa beg yang diperlukan?'), 63, '1260/20')],
               T('Find one giraffe first, then all of them.', 'Cari seekor zirafah dahulu, kemudian semuanya.'), T('30 × 7 = 210, then 210 × 6 = 1,260, then 1,260 ÷ 20 = 63.', '30 × 7 = 210, kemudian 210 × 6 = 1,260, kemudian 1,260 ÷ 20 = 63.'), 'zp10c')])
    return L
