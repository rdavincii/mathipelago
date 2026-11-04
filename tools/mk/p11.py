from lib import *
CODE, BASE = 'ev', 112
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
M = lambda v: f'{v} m'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'operations', 'times-tables', 'adventurer', 'door',
        T('Lava Facts', 'Fakta Lava'),
        T('The volcano gate opens when every multiplication fact finds its answer. Match them!', 'Pintu gunung berapi terbuka apabila setiap fakta darab menemui jawapannya. Padankan mereka!'),
        T('Multiplication facts up to 12 × 12.', 'Fakta darab sehingga 12 × 12.'),
        'Ember', T('Ember glows brighter with every correct fact.', 'Ember bercahaya lebih terang dengan setiap fakta yang betul.'),
        [match([('6 × 7', '42'), ('8 × 4', '32'), ('9 × 5', '45')], MP_, T('Count in steps: 6, 12, 18 ... for the 6 times table.', 'Kira dengan langkah: 6, 12, 18 ... untuk sifir 6.')),
         match([('7 × 8', '56'), ('9 × 6', '54'), ('12 × 4', '48'), ('11 × 3', '33')], MP_, T('Break a fact into two easier facts.', 'Pecahkan satu fakta kepada dua fakta yang lebih mudah.')),
         match([('8 × 8', '64'), ('7 × 9', '63'), ('12 × 6', '72'), ('9 × 9', '81'), ('11 × 7', '77')], MP_, T('Use a fact you know and add or subtract one group.', 'Guna fakta yang anda tahu dan tambah atau tolak satu kumpulan.'))])
    add(2, 'number-sense', 'multiples', 'adventurer', 'lanterns',
        T('Multiple Magma', 'Magma Gandaan'),
        T('Fire-stones glow in a row of multiples. Which one comes next?', 'Batu api bercahaya dalam satu baris gandaan. Yang manakah seterusnya?'),
        T('Continue lists of multiples.', 'Menyambung senarai gandaan.'),
        'Magmo', T('Magmo bubbles once for every multiple.', 'Magmo menggelegak sekali untuk setiap gandaan.'),
        [pattern('arith', 6, 6, 5, seed='ev2a'), pattern('arith', 9, 9, 5, seed='ev2b'), pattern('arith', 12, 12, 6, hidden=3, seed='ev2c')])
    add(3, 'operations', 'factors', 'adventurer', 'gears',
        T('Factor Forge', 'Tempa Faktor'),
        T('The forge needs two factors for every number. Find the two tiles that multiply to the total!', 'Tempa memerlukan dua faktor untuk setiap nombor. Cari dua jubin yang hasil darabnya sama dengan jumlah itu!'),
        T('Find pairs of factors.', 'Mencari pasangan faktor.'),
        'Forgey', T('Forgey hammers out two factors at a time.', 'Forgey menempa dua faktor pada satu masa.'),
        [tiles(24, [3, 8, 5, 6, 4, 7]), tiles(36, [4, 9, 6, 7, 12, 3]), tiles(72, [8, 9, 6, 12, 7, 5])])
    add(4, 'shape-data', 'arrays', 'adventurer', 'door',
        T('Stone Arrays', 'Susunan Batu'),
        T('The stones are laid out in rows and columns. Tap the arrays that hold exactly the right number of stones!', 'Batu disusun dalam baris dan lajur. Ketik susunan yang mempunyai bilangan batu yang tepat!'),
        T('Rows times columns gives the area.', 'Baris darab lajur memberi luas.'),
        'Rowan', T('Rowan likes everything in neat lines.', 'Rowan sukakan segala-galanya dalam barisan kemas.'),
        [shapes_area(16, [(4, 4), (2, 8), (3, 5), (5, 4), (2, 6), (7, 2)]), shapes_area(24, [(4, 6), (3, 8), (2, 9), (5, 5), (6, 3), (7, 3)]), shapes_area(30, [(5, 6), (3, 10), (4, 7), (6, 4), (8, 3), (9, 2)])])
    add(5, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Ash Share', 'Kongsi Abu'),
        T('The fire spirits share their sparks equally. Make every group the same!', 'Roh api berkongsi bunga api mereka sama banyak. Pastikan setiap kumpulan sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Sparky', T('Sparky hands out sparks one by one.', 'Sparky mengagihkan bunga api satu demi satu.'),
        [share(18, 3), share(20, 4), share(25, 5)])
    add(6, 'number-sense', 'multiply-10', 'adventurer', 'bridge',
        T('Ten Times Hotter', 'Sepuluh Kali Lebih Panas'),
        T('Each time the lava gets ten times hotter, the numbers grow. Match each fact to its answer!', 'Setiap kali lava menjadi sepuluh kali lebih panas, nombor bertambah besar. Padankan setiap fakta dengan jawapannya!'),
        T('Multiply by 10, 100 and 1000.', 'Mendarab dengan 10, 100 dan 1000.'),
        'Tenzy', T('Tenzy adds a zero to everything.', 'Tenzy menambah satu sifar pada segala-galanya.'),
        [match([('4 × 10', '40'), ('7 × 10', '70'), ('9 × 10', '90')], MP_, T('Multiplying by 10 moves every digit one place left.', 'Mendarab dengan 10 menggerakkan setiap digit satu tempat ke kiri.')),
         match([('5 × 100', '500'), ('8 × 100', '800'), ('3 × 100', '300'), ('12 × 10', '120')], MP_, T('Multiplying by 100 adds two zeros.', 'Mendarab dengan 100 menambah dua sifar.')),
         match([('25 × 10', '250'), ('36 × 10', '360'), ('14 × 100', '1400'), ('60 × 100', '6000'), ('7 × 1000', '7000')], MP_, T('Count the zeros in 10, 100 and 1000.', 'Kira sifar dalam 10, 100 dan 1000.'))])
    add(7, 'operations', 'times-tables', 'master', 'chest',
        T('Pile It Up', 'Longgokkan'),
        T('The guards sort stones into equal piles. Work out each step!', 'Pengawal mengisih batu ke dalam longgokan yang sama. Kira setiap langkah!'),
        T('Division and multiplication as inverses.', 'Bahagi dan darab sebagai songsangan.'),
        'Pilex', T('Pilex stacks stones as high as a house.', 'Pilex menyusun batu setinggi rumah.'),
        [steps([step(T('A guard has 72 stones. He makes 8 equal piles. How many stones in each pile?', 'Seorang pengawal mempunyai 72 biji batu. Dia membuat 8 longgokan yang sama. Berapa batu dalam setiap longgokan?'), 9, '72/8'),
                step(T('He adds 3 stones to every pile. How many stones in each pile now?', 'Dia menambah 3 batu pada setiap longgokan. Berapa batu dalam setiap longgokan sekarang?'), 12, '9+3'),
                step(T('How many stones are there altogether now?', 'Berapa batu kesemuanya sekarang?'), 96, '8*12')],
               T('Division first, then add, then multiply back.', 'Bahagi dahulu, kemudian tambah, kemudian darab semula.'), T('72 ÷ 8 = 9, then 9 + 3 = 12, then 8 × 12 = 96.', '72 ÷ 8 = 9, kemudian 9 + 3 = 12, kemudian 8 × 12 = 96.'), 'ev7a'),
         steps([step(T('54 gems are shared equally into 6 bags. How many gems in each bag?', '54 permata dikongsi sama banyak ke dalam 6 beg. Berapa permata dalam setiap beg?'), 9, '54/6'),
                step(T('She gives away 2 bags. How many gems does she give away?', 'Dia memberikan 2 beg. Berapa permata yang diberikannya?'), 18, '2*9'),
                step(T('How many gems are left?', 'Berapa permata yang tinggal?'), 36, '54-18')],
               T('Find one bag first.', 'Cari satu beg dahulu.'), T('54 ÷ 6 = 9, then 2 × 9 = 18, then 54 − 18 = 36.', '54 ÷ 6 = 9, kemudian 2 × 9 = 18, kemudian 54 − 18 = 36.'), 'ev7b'),
         steps([step(T('96 sparks are put into groups of 12. How many groups are there?', '96 bunga api dimasukkan ke dalam kumpulan 12. Berapa kumpulan yang ada?'), 8, '96/12'),
                step(T('Then each of the 8 groups gets 5 more sparks. How many sparks is that?', 'Kemudian setiap satu daripada 8 kumpulan mendapat 5 bunga api lagi. Berapa bunga api itu?'), 40, '8*5'),
                step(T('How many sparks are there in total?', 'Berapa bunga api kesemuanya?'), 136, '96+40')],
               T('Divide to find the groups.', 'Bahagi untuk mencari bilangan kumpulan.'), T('96 ÷ 12 = 8, then 8 × 5 = 40, then 96 + 40 = 136.', '96 ÷ 12 = 8, kemudian 8 × 5 = 40, kemudian 96 + 40 = 136.'), 'ev7c')])
    add(8, 'number-sense', 'multiples', 'master', 'scale',
        T('Weighing Rocks', 'Menimbang Batu'),
        T('Each rock weighs a multiple. Choose the rocks that balance the scale!', 'Setiap batu mempunyai berat yang merupakan gandaan. Pilih batu yang menyeimbangkan penimbang!'),
        T('Add multiples to reach a total.', 'Menambah gandaan untuk mencapai jumlah.'),
        'Rocky', T('Rocky never rolls away.', 'Rocky tidak pernah bergolek pergi.'),
        [balance(48, [6, 12, 18, 24, 30, 36]), balance(90, [15, 30, 45, 60, 75, 20]), balance(120, [20, 40, 60, 80, 35, 25], 3)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Crater Chart', 'Carta Kawah'),
        T('The rangers counted the rocks thrown by each crater. Read the chart!', 'Renjer mengira batu yang dilontarkan oleh setiap kawah. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Craty', T('Craty counts the rocks, one crater at a time.', 'Craty mengira batu, satu kawah pada satu masa.'),
        [chart([(T('Red', 'Merah'), 27, 'coral'), (T('Blue', 'Biru'), 15, 'sky'), (T('Gold', 'Emas'), 21, 'sun')], ('diff', 0, 1), T('rocks', 'batu')),
         chart([(T('Red', 'Merah'), 18, 'coral'), (T('Blue', 'Biru'), 25, 'sky'), (T('Gold', 'Emas'), 32, 'sun'), (T('Green', 'Hijau'), 14, 'mint')], ('sum', [0, 1, 2, 3]), T('rocks', 'batu')),
         chart([(T('Red', 'Merah'), 12, 'coral'), (T('Blue', 'Biru'), 20, 'sky'), (T('Gold', 'Emas'), 16, 'sun'), (T('Green', 'Hijau'), 24, 'mint'), (T('Pink', 'Merah jambu'), 28, 'grape')], ('mean',), T('rocks', 'batu'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Volcano Finale', 'Kemuncak Gunung Berapi'),
        T('The volcano is about to erupt! Solve three steps to calm the lava.', 'Gunung berapi hampir meletus! Selesaikan tiga langkah untuk menenangkan lava.'),
        T('Multi-step problems with multiplication, division and measures.', 'Masalah berbilang langkah dengan darab, bahagi dan ukuran.'),
        'Lavaro', T('Lavaro hums when the lava cools down.', 'Lavaro berdengung apabila lava menjadi sejuk.'),
        [steps([step(T('Lava flows 9 metres each minute. How far does it flow in 7 minutes?', 'Lava mengalir 9 meter setiap minit. Sejauh mana ia mengalir dalam 7 minit?'), 63, '9*7', M),
                step(T('Then it flows 37 metres more. How far is that in total?', 'Kemudian ia mengalir 37 meter lagi. Berapa jauh jumlahnya?'), 100, '63+37', M),
                step(T('A wall is built every 20 metres. How many walls are built?', 'Satu tembok dibina setiap 20 meter. Berapa tembok yang dibina?'), 5, '100/20')],
               T('Multiply, then add, then divide.', 'Darab, kemudian tambah, kemudian bahagi.'), T('9 × 7 = 63, then 63 + 37 = 100, then 100 ÷ 20 = 5.', '9 × 7 = 63, kemudian 63 + 37 = 100, kemudian 100 ÷ 20 = 5.'), 'ev10a'),
         steps([step(T('A crater has 6 rows of 8 fire-stones. How many fire-stones?', 'Sebuah kawah mempunyai 6 baris dengan 8 batu api. Berapa batu api?'), 48, '6*8'),
                step(T('9 of them crumble. How many are left?', '9 daripadanya hancur. Berapa yang tinggal?'), 39, '48-9'),
                step(T('The rest are shared equally into 3 baskets. How many in each basket?', 'Bakinya dikongsi sama banyak ke dalam 3 bakul. Berapa dalam setiap bakul?'), 13, '39/3')],
               T('Rows times columns first.', 'Baris darab lajur dahulu.'), T('6 × 8 = 48, then 48 − 9 = 39, then 39 ÷ 3 = 13.', '6 × 8 = 48, kemudian 48 − 9 = 39, kemudian 39 ÷ 3 = 13.'), 'ev10b'),
         steps([step(T('One volcano makes 12 gems a day. How many gems do 3 volcanoes make in a day?', 'Sebuah gunung berapi menghasilkan 12 permata sehari. Berapa permata yang dihasilkan oleh 3 gunung berapi dalam sehari?'), 36, '12*3'),
                step(T('How many gems do they make in 5 days?', 'Berapa permata yang mereka hasilkan dalam 5 hari?'), 180, '36*5'),
                step(T('The gems are sold in packs of 15. How many packs?', 'Permata itu dijual dalam pek 15. Berapa pek?'), 12, '180/15')],
               T('Find one day first.', 'Cari satu hari dahulu.'), T('12 × 3 = 36, then 36 × 5 = 180, then 180 ÷ 15 = 12.', '12 × 3 = 36, kemudian 36 × 5 = 180, kemudian 180 ÷ 15 = 12.'), 'ev10c')])
    return L
