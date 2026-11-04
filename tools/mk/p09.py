from lib import *
CODE, BASE = 'dr', 92
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'rounding', 'adventurer', 'bridge',
        T('Round the Reef', 'Bundarkan Terumbu'),
        T('Fish counts are rounded to the nearest ten. Slide the marker to the rounded number!', 'Bilangan ikan dibundarkan kepada puluh terdekat. Gelongsorkan penanda ke nombor yang dibundarkan!'),
        T('Round to the nearest 10 and 100.', 'Membundarkan kepada 10 dan 100 yang terdekat.'),
        'Roundy', T('Roundy is the roundest fish in the sea.', 'Roundy ialah ikan paling bulat di laut.'),
        [numberline(40, 0, 100, 10, 20, kind='round', x=43, unit='10'), numberline(70, 0, 100, 10, 20, kind='round', x=68, unit='10'), numberline(300, 0, 500, 100, 100, kind='round', x=349, unit='100')])
    add(2, 'number-sense', 'rounding', 'adventurer', 'door',
        T('Estimate Pairs', 'Pasangan Anggaran'),
        T('Match each number to its rounded friend!', 'Padankan setiap nombor dengan kawan bundarannya!'),
        T('Round numbers to the nearest 10 and 100.', 'Membundarkan nombor kepada 10 dan 100 yang terdekat.'),
        'Guessy', T('Guessy is almost always close.', 'Guessy hampir sentiasa dekat.'),
        [match([('23', '20'), ('47', '50'), ('62', '60')], MP_, T('Look at the ones digit. 5 or more rounds up.', 'Lihat digit sa. 5 atau lebih dibundarkan ke atas.')),
         match([('184', '180'), ('235', '240'), ('391', '390'), ('507', '510')], MP_, T('Round to the nearest 10.', 'Bundarkan kepada 10 terdekat.')),
         match([('240', '200'), ('350', '400'), ('618', '600'), ('781', '800'), ('1449', '1400')], MP_, T('Round to the nearest 100.', 'Bundarkan kepada 100 terdekat.'))])
    add(3, 'operations', 'money', 'adventurer', 'ferry',
        T('Fish Feast', 'Jamuan Ikan'),
        T('The reef cafe feeds hungry fish. Work out the food in three steps!', 'Kafe terumbu memberi makan ikan yang lapar. Kira makanan dalam tiga langkah!'),
        T('Multiply, add and share in short chains.', 'Mendarab, menambah dan berkongsi dalam rantaian pendek.'),
        'Nibbles', T('Nibbles takes tiny bites of everything.', 'Nibbles menggigit sedikit setiap benda.'),
        [steps([step(T('A fish eats 6 shrimp a day. How many shrimp do 5 fish eat?', 'Seekor ikan makan 6 udang sehari. Berapa udang dimakan oleh 5 ekor ikan?'), 30, '5*6'),
                step(T('The reef has 50 shrimp. How many are left?', 'Terumbu ada 50 udang. Berapa yang tinggal?'), 20, '50-30'),
                step(T('The shrimp are shared equally between 4 crabs. How many does each crab get?', 'Udang dikongsi sama banyak antara 4 ekor ketam. Berapa yang diperoleh setiap ketam?'), 5, '20/4')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('5 × 6 = 30, then 50 − 30 = 20, then 20 ÷ 4 = 5.', '5 × 6 = 30, kemudian 50 − 30 = 20, kemudian 20 ÷ 4 = 5.'), 'dr3a'),
         steps([step(T('A diver finds 12 shells on each trip. How many shells in 4 trips?', 'Seorang penyelam menjumpai 12 kulit kerang setiap perjalanan. Berapa kulit kerang dalam 4 perjalanan?'), 48, '4*12'),
                step(T('She gives away 18 shells. How many shells are left?', 'Dia memberikan 18 kulit kerang. Berapa kulit kerang yang tinggal?'), 30, '48-18'),
                step(T('She puts the rest in 6 equal bags. How many shells in each bag?', 'Dia memasukkan bakinya ke dalam 6 beg yang sama banyak. Berapa kulit kerang dalam setiap beg?'), 5, '30/6')],
               T('Find how many shells in total first.', 'Cari jumlah kulit kerang dahulu.'), T('4 × 12 = 48, then 48 − 18 = 30, then 30 ÷ 6 = 5.', '4 × 12 = 48, kemudian 48 − 18 = 30, kemudian 30 ÷ 6 = 5.'), 'dr3b'),
         steps([step(T('A fish tank costs RM45. What do 3 tanks cost?', 'Sebuah tangki ikan berharga RM45. Berapa harga 3 tangki?'), 135, '3*45', RM),
                step(T('Fish food costs RM12. What is the total?', 'Makanan ikan berharga RM12. Berapa jumlahnya?'), 147, '135+12', RM),
                step(T('You pay with RM200. How much change do you get?', 'Anda membayar dengan RM200. Berapa baki yang anda terima?'), 53, '200-147', RM)],
               T('Add everything, then take it from RM200.', 'Tambah semuanya, kemudian tolak daripada RM200.'), T('3 × 45 = 135, then 135 + 12 = 147, then 200 − 147 = 53.', '3 × 45 = 135, kemudian 135 + 12 = 147, kemudian 200 − 147 = 53.'), 'dr3c')])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Bubble Trail', 'Jejak Gelembung'),
        T('Bubbles rise in a pattern. How many bubbles come next?', 'Gelembung naik dalam satu pola. Berapa gelembung yang datang seterusnya?'),
        T('Continue doubling and counting patterns.', 'Menyambung pola berganda dan pengiraan.'),
        'Bubbly', T('Bubbly pops when it is surprised.', 'Bubbly meletup apabila terkejut.'),
        [pattern('geo', 2, 2, 5, seed='dr4a'), pattern('arith', 4, 6, 5, seed='dr4b'), pattern('geo', 3, 2, 6, hidden=4, seed='dr4c')])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Reef Tank', 'Tangki Terumbu'),
        T('Fill each reef tank to the line shown!', 'Isi setiap tangki terumbu hingga garisan yang ditunjukkan!'),
        T('Fractions of a tank.', 'Pecahan sebuah tangki.'),
        'Finley', T('Finley swims in tidy circles.', 'Finley berenang dalam bulatan yang kemas.'),
        [tank(6, 1, 3), tank(10, 4, 5), tank(12, 2, 3)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Fish Feast Share', 'Kongsi Jamuan Ikan'),
        T('Share the food between the hungry fish. Everyone gets the same!', 'Kongsi makanan antara ikan yang lapar. Semua mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Munchy', T('Munchy is the first to the table.', 'Munchy ialah yang pertama ke meja.'),
        [share(20, 5), share(16, 4), share(27, 3)])
    add(7, 'number-sense', 'place-value', 'master', 'door',
        T('Treasure Counts', 'Kiraan Harta Karun'),
        T('The reef treasure is counted in thousands, hundreds, tens and ones. Build each number!', 'Harta karun terumbu dikira dalam ribu, ratus, puluh dan sa. Bina setiap nombor!'),
        T('Build numbers up to 9,999 with place value.', 'Membina nombor sehingga 9,999 dengan nilai tempat.'),
        'Pearly', T('Pearly keeps one pearl for luck.', 'Pearly menyimpan sebutir mutiara untuk tuah.'),
        [placevalue(520, [100, 10, 1]), placevalue(2306, [1000, 100, 10, 1]), placevalue(7059, [1000, 100, 10, 1])])
    add(8, 'operations', 'times-tables', 'master', 'gears',
        T('School of Fish', 'Sekumpulan Ikan'),
        T('Fish swim in schools of equal size. Find the two tiles that make each total!', 'Ikan berenang dalam kumpulan yang sama saiz. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Schooly', T('Schooly is always top of the class.', 'Schooly sentiasa terbaik dalam kelas.'),
        [tiles(42, [6, 7, 3, 14, 8, 9]), tiles(90, [9, 10, 6, 15, 8, 12]), tiles(156, [12, 13, 9, 8, 14, 11])])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Reef Chart', 'Carta Terumbu'),
        T('The reef rangers counted the fish they saw. Read the chart!', 'Renjer terumbu mengira ikan yang mereka lihat. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Tally', T('Tally makes a mark for every fish.', 'Tally membuat satu tanda untuk setiap ikan.'),
        [chart([(T('Clown', 'Badut'), 18, 'coral'), (T('Blue', 'Biru'), 12, 'sky'), (T('Yellow', 'Kuning'), 15, 'sun')], ('diff', 0, 1), T('fish', 'ikan')),
         chart([(T('Clown', 'Badut'), 20, 'coral'), (T('Blue', 'Biru'), 35, 'sky'), (T('Yellow', 'Kuning'), 15, 'sun'), (T('Green', 'Hijau'), 30, 'mint')], ('sum', [0, 1, 2, 3]), T('fish', 'ikan')),
         chart([(T('Clown', 'Badut'), 16, 'coral'), (T('Blue', 'Biru'), 24, 'sky'), (T('Yellow', 'Kuning'), 8, 'sun'), (T('Green', 'Hijau'), 20, 'mint'), (T('Pink', 'Merah jambu'), 32, 'grape')], ('mean',), T('fish', 'ikan'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Reef Finale', 'Kemuncak Terumbu'),
        T('The coral crown is hidden in the deepest part of the reef. Solve three steps to find it!', 'Mahkota karang tersembunyi di bahagian terumbu yang paling dalam. Selesaikan tiga langkah untuk menjumpainya!'),
        T('Multi-step problems with data, money and sharing.', 'Masalah berbilang langkah dengan data, wang dan perkongsian.'),
        'Crowny', T('Crowny wears a coral crown on special days.', 'Crowny memakai mahkota karang pada hari istimewa.'),
        [steps([step(T('A reef has 8 rows of coral with 9 corals in each row. How many corals?', 'Sebuah terumbu mempunyai 8 baris karang dengan 9 karang dalam setiap baris. Berapa karang?'), 72, '8*9'),
                step(T('A storm breaks 15 corals. How many corals are left?', 'Ribut memecahkan 15 karang. Berapa karang yang tinggal?'), 57, '72-15'),
                step(T('Divers plant 23 new corals. How many corals now?', 'Penyelam menanam 23 karang baharu. Berapa karang sekarang?'), 80, '57+23')],
               T('Multiply, then subtract, then add.', 'Darab, kemudian tolak, kemudian tambah.'), T('8 × 9 = 72, then 72 − 15 = 57, then 57 + 23 = 80.', '8 × 9 = 72, kemudian 72 − 15 = 57, kemudian 57 + 23 = 80.'), 'dr10a'),
         steps([step(T('A boat takes 25 tourists on each trip. How many tourists in 6 trips?', 'Sebuah bot membawa 25 pelancong setiap perjalanan. Berapa pelancong dalam 6 perjalanan?'), 150, '6*25'),
                step(T('Each tourist pays RM4. How much money is that in total?', 'Setiap pelancong membayar RM4. Berapa jumlah wang itu?'), 600, '150*4', RM),
                step(T('The boat costs RM350 to run. How much money is left?', 'Bot itu menelan belanja RM350 untuk dikendalikan. Berapa wang yang tinggal?'), 250, '600-350', RM)],
               T('Find the tourists first, then the money.', 'Cari bilangan pelancong dahulu, kemudian wang.'), T('6 × 25 = 150, then 150 × 4 = 600, then 600 − 350 = 250.', '6 × 25 = 150, kemudian 150 × 4 = 600, kemudian 600 − 350 = 250.'), 'dr10b'),
         steps([step(T('A fish tank holds 48 litres. How many litres do 5 tanks hold?', 'Sebuah tangki ikan memuatkan 48 liter. Berapa liter dimuatkan oleh 5 tangki?'), 240, '5*48', lambda v: f'{v} L'),
                step(T('2 litres are lost to splashes. How many litres are left?', '2 liter hilang akibat percikan. Berapa liter yang tinggal?'), 238, '240-2', lambda v: f'{v} L'),
                step(T('The water is poured into 7 buckets, plus 7 litres left over. Each bucket has the same amount. How many litres in each bucket?', 'Air itu dituang ke dalam 7 baldi, dan 7 liter lagi tertinggal. Setiap baldi mempunyai jumlah yang sama. Berapa liter dalam setiap baldi?'), 33, '(238-7)/7', lambda v: f'{v} L')],
               T('Take away the left-over litres before you share.', 'Tolak liter yang berbaki sebelum berkongsi.'), T('5 × 48 = 240, then 240 − 2 = 238, then (238 − 7) ÷ 7 = 33.', '5 × 48 = 240, kemudian 240 − 2 = 238, kemudian (238 − 7) ÷ 7 = 33.'), 'dr10c')])
    return L
