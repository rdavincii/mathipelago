from lib import *
CODE, BASE = 'fp', 82
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'negatives', 'adventurer', 'bridge',
        T('Below Zero', 'Bawah Sifar'),
        T('It is freezing on the peaks! Slide the marker to the right temperature.', 'Puncak gunung sangat sejuk! Gelongsorkan penanda ke suhu yang betul.'),
        T('Read temperatures on a line, including below zero.', 'Membaca suhu pada garis, termasuk di bawah sifar.'),
        'Brrr', T('Brrr shivers even in a warm coat.', 'Brrr menggigil walaupun memakai kot tebal.'),
        [numberline(-5, -10, 10, 1, 5), numberline(-15, -20, 20, 5, 10), numberline(-12, -30, 10, 2, 10, kind='half', a=-20, b=0)])
    add(2, 'number-sense', 'negatives', 'adventurer', 'door',
        T('Thermometer Match', 'Padanan Termometer'),
        T('Match each temperature to the number that is the same distance from zero, but on the warm side!', 'Padankan setiap suhu dengan nombor yang sama jaraknya dari sifar, tetapi di sisi panas!'),
        T('Pair a negative number with its positive twin.', 'Memadankan nombor negatif dengan pasangan positifnya.'),
        'Frosty', T('Frosty likes things tidy and in pairs.', 'Frosty suka benda yang kemas dan berpasangan.'),
        [match([('−3', '3'), ('−5', '5'), ('−8', '8')], MP_, T('The twin has the same number but no minus sign.', 'Pasangannya mempunyai nombor yang sama tetapi tiada tanda tolak.')),
         match([('−10', '10'), ('−12', '12'), ('−7', '7'), ('−20', '20')], MP_, T('The twin has the same number but no minus sign.', 'Pasangannya mempunyai nombor yang sama tetapi tiada tanda tolak.')),
         match([('−15', '15'), ('−25', '25'), ('−30', '30'), ('−40', '40'), ('−50', '50')], MP_, T('The twin has the same number but no minus sign.', 'Pasangannya mempunyai nombor yang sama tetapi tiada tanda tolak.'))])
    add(3, 'operations', 'negatives', 'adventurer', 'ferry',
        T('Cold Snap', 'Cuaca Dingin'),
        T('The temperature rises and falls all day. Work out each change!', 'Suhu naik dan turun sepanjang hari. Kira setiap perubahan!'),
        T('Add and subtract temperature changes.', 'Menambah dan menolak perubahan suhu.'),
        'Flurry', T('Flurry loves a sudden snowfall.', 'Flurry sukakan salji yang turun mendadak.'),
        [steps([step(T('It is 4 degrees in the morning. It rises by 6. What is the temperature?', 'Suhu pada waktu pagi ialah 4 darjah. Ia naik 6. Berapakah suhu itu?'), 10, '4+6'),
                step(T('Then it falls by 3. What is the temperature?', 'Kemudian ia turun 3. Berapakah suhu itu?'), 7, '10-3'),
                step(T('Then it doubles. What is the temperature?', 'Kemudian ia menjadi dua kali ganda. Berapakah suhu itu?'), 14, '7*2')],
               T('Rises means add. Falls means subtract.', 'Naik bermaksud tambah. Turun bermaksud tolak.'), T('4 + 6 = 10, then 10 − 3 = 7, then 7 × 2 = 14.', '4 + 6 = 10, kemudian 10 − 3 = 7, kemudian 7 × 2 = 14.'), 'fp3a'),
         steps([step(T('The peak is 12 degrees below the base. The base is 5 degrees. How many degrees is the peak?', 'Puncak 12 darjah lebih rendah daripada pangkalan. Pangkalan 5 darjah. Berapa darjah puncak itu?'), -7, '5-12', minus),
                step(T('A storm makes it 3 degrees colder. What is the temperature?', 'Ribut menjadikannya 3 darjah lebih sejuk. Berapakah suhu itu?'), -10, '-7-3', minus),
                step(T('The sun warms it by 15 degrees. What is the temperature?', 'Matahari menghangatkannya sebanyak 15 darjah. Berapakah suhu itu?'), 5, '-10+15')],
               T('Take it one step at a time.', 'Selesaikan satu langkah pada satu masa.'), T('5 − 12 = −7, then −7 − 3 = −10, then −10 + 15 = 5.', '5 − 12 = −7, kemudian −7 − 3 = −10, kemudian −10 + 15 = 5.'), 'fp3b'),
         steps([step(T('A climber starts at 100 m and goes up 45 m. What height is that?', 'Seorang pendaki bermula pada 100 m dan naik 45 m. Berapa tinggi itu?'), 145, '100+45', lambda v: f'{v} m'),
                step(T('Then goes down 30 m. What height is that?', 'Kemudian turun 30 m. Berapa tinggi itu?'), 115, '145-30', lambda v: f'{v} m'),
                step(T('Then goes up 85 m. What height is that?', 'Kemudian naik 85 m. Berapa tinggi itu?'), 200, '115+85', lambda v: f'{v} m')],
               T('Up means add. Down means subtract.', 'Naik bermaksud tambah. Turun bermaksud tolak.'), T('100 + 45 = 145, then 145 − 30 = 115, then 115 + 85 = 200.', '100 + 45 = 145, kemudian 145 − 30 = 115, kemudian 115 + 85 = 200.'), 'fp3c')])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Snow Steps', 'Langkah Salji'),
        T('Footprints in the snow make a pattern. Which footprint comes next?', 'Tapak kaki di salji membentuk pola. Tapak kaki yang manakah seterusnya?'),
        T('Continue patterns that count down and go through zero.', 'Menyambung pola yang mengira ke bawah dan melepasi sifar.'),
        'Pawsy', T('Pawsy leaves the neatest footprints.', 'Pawsy meninggalkan tapak kaki yang paling kemas.'),
        [pattern('arith', 20, -4, 6, seed='fp4a'), pattern('arith', 12, -3, 6, seed='fp4b'), pattern('arith', 10, -5, 6, hidden=4, seed='fp4c')])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Cocoa Tank', 'Tangki Koko'),
        T('Fill each cocoa tank to the right line. The skiers are waiting!', 'Isi setiap tangki koko hingga garisan yang betul. Para pemain ski sedang menunggu!'),
        T('Fractions of a tank.', 'Pecahan sebuah tangki.'),
        'Cocoa', T('Cocoa is always warm and a little sticky.', 'Cocoa sentiasa hangat dan sedikit melekit.'),
        [tank(8, 1, 4), tank(10, 3, 5), tank(12, 3, 4)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Mitten Share', 'Kongsi Sarung Tangan'),
        T('Share the mittens between the climbers so everyone gets the same number!', 'Kongsi sarung tangan antara pendaki supaya semua orang mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Mitten', T('Mitten always loses one of a pair.', 'Mitten sentiasa kehilangan sebelah daripada sepasang.'),
        [share(18, 3), share(20, 4), share(30, 5)])
    add(7, 'number-sense', 'place-value', 'master', 'door',
        T('Summit Heights', 'Ketinggian Puncak'),
        T('Each peak has a height. Build the height on the lock!', 'Setiap puncak mempunyai ketinggian. Bina ketinggian itu pada kunci!'),
        T('Build numbers up to 9,999 with place value.', 'Membina nombor sehingga 9,999 dengan nilai tempat.'),
        'Summit', T('Summit is the tallest critter in the range.', 'Summit ialah makhluk paling tinggi dalam banjaran itu.'),
        [placevalue(1200, [1000, 100, 10, 1]), placevalue(3450, [1000, 100, 10, 1]), placevalue(8848, [1000, 100, 10, 1])])
    add(8, 'operations', 'times-tables', 'master', 'gears',
        T('Ski Lifts', 'Lif Ski'),
        T('Each ski lift carries skiers up the hill. Find the two tiles that make each total!', 'Setiap lif ski membawa pemain ski ke atas bukit. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Liftie', T('Liftie never loses a skier.', 'Liftie tidak pernah kehilangan pemain ski.'),
        [tiles(36, [4, 9, 6, 3, 12, 5]), tiles(96, [8, 12, 6, 16, 4, 9]), tiles(150, [15, 10, 12, 25, 6, 20])])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Snowfall Chart', 'Carta Salji'),
        T('The rangers measured the snow each day. Read the chart!', 'Renjer mengukur salji setiap hari. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Drifty', T('Drifty is always found where snow piles up.', 'Drifty sentiasa ditemui di tempat salji bertimbun.'),
        [chart([(T('Mon', 'Isnin'), 14, 'sky'), (T('Tue', 'Selasa'), 6, 'grape'), (T('Wed', 'Rabu'), 10, 'mint')], ('diff', 0, 1), T('cm', 'cm')),
         chart([(T('Mon', 'Isnin'), 12, 'sky'), (T('Tue', 'Selasa'), 8, 'grape'), (T('Wed', 'Rabu'), 15, 'mint'), (T('Thu', 'Khamis'), 5, 'sun')], ('sum', [0, 1, 2, 3]), T('cm', 'cm')),
         chart([(T('Mon', 'Isnin'), 10, 'sky'), (T('Tue', 'Selasa'), 20, 'grape'), (T('Wed', 'Rabu'), 15, 'mint'), (T('Thu', 'Khamis'), 5, 'sun'), (T('Fri', 'Jumaat'), 25, 'coral')], ('mean',), T('cm', 'cm'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Peak Finale', 'Kemuncak Puncak'),
        T('The last peak is ahead! Solve three-step problems to plant the flag at the top.', 'Puncak terakhir sudah di depan! Selesaikan masalah tiga langkah untuk menanam bendera di puncak.'),
        T('Multi-step problems with height, time and money.', 'Masalah berbilang langkah dengan ketinggian, masa dan wang.'),
        'Flaggy', T('Flaggy waves at every cloud.', 'Flaggy melambai kepada setiap awan.'),
        [steps([step(T('A climber goes up 150 m each hour. How many metres in 4 hours?', 'Seorang pendaki naik 150 m setiap jam. Berapa meter dalam 4 jam?'), 600, '150*4', lambda v: f'{v} m'),
                step(T('The peak is 800 m high. How many metres are still to climb?', 'Puncak setinggi 800 m. Berapa meter lagi perlu didaki?'), 200, '800-600', lambda v: f'{v} m'),
                step(T('She climbs the rest in 4 equal parts. How many metres in each part?', 'Dia mendaki baki itu dalam 4 bahagian yang sama. Berapa meter dalam setiap bahagian?'), 50, '200/4', lambda v: f'{v} m')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('150 × 4 = 600, then 800 − 600 = 200, then 200 ÷ 4 = 50.', '150 × 4 = 600, kemudian 800 − 600 = 200, kemudian 200 ÷ 4 = 50.'), 'fp10a'),
         steps([step(T('A team has 9 climbers. Each carries 6 kg of food. How many kg of food?', 'Sebuah pasukan mempunyai 9 pendaki. Setiap orang membawa 6 kg makanan. Berapa kg makanan?'), 54, '9*6', lambda v: f'{v} kg'),
                step(T('They eat 14 kg. How many kg are left?', 'Mereka makan 14 kg. Berapa kg yang tinggal?'), 40, '54-14', lambda v: f'{v} kg'),
                step(T('The rest is shared equally between 8 sleds. How many kg on each sled?', 'Bakinya dikongsi sama banyak antara 8 kereta luncur. Berapa kg pada setiap kereta luncur?'), 5, '40/8', lambda v: f'{v} kg')],
               T('Find the total food first.', 'Cari jumlah makanan dahulu.'), T('9 × 6 = 54, then 54 − 14 = 40, then 40 ÷ 8 = 5.', '9 × 6 = 54, kemudian 54 − 14 = 40, kemudian 40 ÷ 8 = 5.'), 'fp10b'),
         steps([step(T('A ski pass costs RM35 a day. What do 3 days cost?', 'Pas ski berharga RM35 sehari. Berapa harga 3 hari?'), 105, '3*35', RM),
                step(T('A hat costs RM18. What is the total for the pass and the hat?', 'Sebuah topi berharga RM18. Berapa jumlah untuk pas dan topi itu?'), 123, '105+18', RM),
                step(T('You pay with RM150. How much change do you get?', 'Anda membayar dengan RM150. Berapa baki yang anda terima?'), 27, '150-123', RM)],
               T('Add the costs, then work out the change.', 'Tambah harga, kemudian kira baki.'), T('3 × 35 = 105, then 105 + 18 = 123, then 150 − 123 = 27.', '3 × 35 = 105, kemudian 105 + 18 = 123, kemudian 150 − 123 = 27.'), 'fp10c')])
    return L
