from lib import *
CODE, BASE = 'do', 262
MT = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
M = lambda v: f'{minus(v)} m'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'negatives', 'adventurer', 'bridge',
        T('Dive Line', 'Garis Menyelam'),
        T('The diver goes below zero! Slide the marker to the right depth.', 'Penyelam turun di bawah sifar! Gelongsorkan penanda ke kedalaman yang betul.'),
        T('Read numbers below zero on a line.', 'Membaca nombor di bawah sifar pada garis.'),
        'Bubbo', T('Bubbo blows the best bubbles in the sea.', 'Bubbo meniup gelembung terbaik di laut.'),
        [numberline(-30, -100, 0, 10, 20), numberline(-250, -500, 0, 50, 100), numberline(-40, -100, 0, 10, 20, kind='half', a=-60, b=-20)])
    add(2, 'number-sense', 'negatives', 'adventurer', 'door',
        T('Sum Splash', 'Percikan Pengiraan'),
        T('Waves bring sums that go above and below zero. Match each sum to its answer!', 'Ombak membawa pengiraan yang naik dan turun melepasi sifar. Padankan setiap pengiraan dengan jawapannya!'),
        T('Add and subtract with negative numbers.', 'Menambah dan menolak dengan nombor negatif.'),
        'Splashy', T('Splashy leaps over every wave.', 'Splashy melompat melepasi setiap ombak.'),
        [match([('−3 + 5', '2'), ('−4 + 4', '0'), ('2 − 6', '−4')], MT, T('Count up from the first number for adding, down for taking away.', 'Kira ke atas dari nombor pertama untuk menambah, ke bawah untuk menolak.')),
         match([('−10 + 3', '−7'), ('5 − 9', '−4'), ('−2 − 3', '−5'), ('−6 + 10', '4')], MT, T('Imagine a number line and move left or right.', 'Bayangkan garis nombor dan bergerak ke kiri atau kanan.')),
         match([('−15 + 20', '5'), ('8 − 20', '−12'), ('−9 − 6', '−15'), ('−30 + 45', '15'), ('12 − 25', '−13')], MT, T('Imagine a number line and move left or right.', 'Bayangkan garis nombor dan bergerak ke kiri atau kanan.'))])
    add(3, 'operations', 'negatives', 'adventurer', 'ferry',
        T('Submarine Dive', 'Selaman Kapal Selam'),
        T('The submarine dives and rises all day. Work out its depth after every move!', 'Kapal selam menyelam dan naik sepanjang hari. Kira kedalamannya selepas setiap pergerakan!'),
        T('Add and subtract depth changes.', 'Menambah dan menolak perubahan kedalaman.'),
        'Sonar', T('Sonar pings everything it can see.', 'Sonar berbunyi pada semua yang dapat dilihatnya.'),
        [steps([step(T('A diver starts at the surface (0 m) and goes down 12 m. What is the depth?', 'Seorang penyelam bermula di permukaan (0 m) dan turun 12 m. Berapakah kedalamannya?'), -12, '0-12', M),
                step(T('She goes down 8 m more. What is the depth?', 'Dia turun 8 m lagi. Berapakah kedalamannya?'), -20, '-12-8', M),
                step(T('She swims up 5 m. What is the depth?', 'Dia berenang naik 5 m. Berapakah kedalamannya?'), -15, '-20+5', M)],
               T('Down means subtract. Up means add.', 'Turun bermaksud tolak. Naik bermaksud tambah.'), T('0 − 12 = −12, then −12 − 8 = −20, then −20 + 5 = −15.', '0 − 12 = −12, kemudian −12 − 8 = −20, kemudian −20 + 5 = −15.'), 'do3a'),
         steps([step(T('A submarine is at −50 m. It rises 20 m. What is the depth?', 'Sebuah kapal selam berada pada −50 m. Ia naik 20 m. Berapakah kedalamannya?'), -30, '-50+20', M),
                step(T('It dives 45 m. What is the depth?', 'Ia menyelam 45 m. Berapakah kedalamannya?'), -75, '-30-45', M),
                step(T('It rises 100 m. What is the height now?', 'Ia naik 100 m. Berapakah ketinggiannya sekarang?'), 25, '-75+100', M)],
               T('Take one move at a time.', 'Selesaikan satu pergerakan pada satu masa.'), T('−50 + 20 = −30, then −30 − 45 = −75, then −75 + 100 = 25.', '−50 + 20 = −30, kemudian −30 − 45 = −75, kemudian −75 + 100 = 25.'), 'do3b'),
         steps([step(T('A robot starts at −8 m and goes down 17 m. What is the depth?', 'Sebuah robot bermula pada −8 m dan turun 17 m. Berapakah kedalamannya?'), -25, '-8-17', M),
                step(T('It rises 10 m. What is the depth?', 'Ia naik 10 m. Berapakah kedalamannya?'), -15, '-25+10', M),
                step(T('It dives 35 m. What is the depth?', 'Ia menyelam 35 m. Berapakah kedalamannya?'), -50, '-15-35', M)],
               T('Going down makes the number smaller.', 'Turun menjadikan nombor lebih kecil.'), T('−8 − 17 = −25, then −25 + 10 = −15, then −15 − 35 = −50.', '−8 − 17 = −25, kemudian −25 + 10 = −15, kemudian −15 − 35 = −50.'), 'do3c')])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Sinking Pattern', 'Pola Tenggelam'),
        T('Treasure chests sink in a pattern. Which number comes next?', 'Peti harta karun tenggelam mengikut pola. Nombor manakah yang seterusnya?'),
        T('Continue patterns that count down through zero.', 'Menyambung pola yang mengira ke bawah melepasi sifar.'),
        'Chesty', T('Chesty guards the sunken treasure.', 'Chesty menjaga harta karun yang tenggelam.'),
        [pattern('arith', 10, -5, 6, seed='do4a'), pattern('arith', 100, -30, 6, seed='do4b'), pattern('arith', -20, 10, 6, hidden=3, seed='do4c')])
    add(5, 'number-sense', 'rounding', 'adventurer', 'door',
        T('Round the Reef', 'Bundarkan Terumbu'),
        T('The sonar rounds every depth. Slide the marker to the rounded number!', 'Sonar membundarkan setiap kedalaman. Gelongsorkan penanda ke nombor yang dibundarkan!'),
        T('Round to the nearest 10, 100 and 1000.', 'Membundarkan kepada 10, 100 dan 1000 yang terdekat.'),
        'Roundfish', T('Roundfish is the roundest fish in the ocean.', 'Roundfish ialah ikan paling bulat di lautan.'),
        [numberline(120, 0, 200, 10, 20, kind='round', x=118, unit='10'), numberline(500, 0, 1000, 100, 200, kind='round', x=462, unit='100'), numberline(3000, 0, 5000, 1000, 1000, kind='round', x=3480, unit='1000')])
    add(6, 'number-sense', 'place-value', 'master', 'door',
        T('Deepest Depths', 'Kedalaman Paling Dalam'),
        T('The ocean floor has very big numbers. Build each depth on the lock!', 'Dasar lautan mempunyai nombor yang sangat besar. Bina setiap kedalaman pada kunci!'),
        T('Build numbers up to 9,999 with place value.', 'Membina nombor sehingga 9,999 dengan nilai tempat.'),
        'Trench', T('Trench lives in the deepest valley.', 'Trench tinggal di lembah paling dalam.'),
        [placevalue(1450, [1000, 100, 10, 1]), placevalue(3806, [1000, 100, 10, 1]), placevalue(9020, [1000, 100, 10, 1])])
    add(7, 'number-sense', 'place-value', 'master', 'chest',
        T('Treasure Digits', 'Digit Harta Karun'),
        T('Put the digit tiles in the best order to open the treasure chest!', 'Letakkan jubin digit dalam susunan terbaik untuk membuka peti harta karun!'),
        T('Make the smallest and largest numbers from digits.', 'Membentuk nombor terkecil dan terbesar daripada digit.'),
        'Pearl', T('Pearl is happiest when everything is in order.', 'Pearl paling gembira apabila segalanya teratur.'),
        [digitarrange([4, 0, 7, 2], 'smallest'), digitarrange([9, 3, 5, 1], 'largest'), digitarrange([8, 0, 2, 5], 'smallest')])
    add(8, 'number-sense', 'length', 'master', 'scale',
        T('Metres and Centimetres', 'Meter dan Sentimeter'),
        T('Reef creatures are measured in metres and centimetres. Match the same length in two ways!', 'Makhluk terumbu diukur dalam meter dan sentimeter. Padankan panjang yang sama dalam dua cara!'),
        T('Convert metres and centimetres.', 'Menukar meter dan sentimeter.'),
        'Ruler Ray', T('Ruler Ray measures everything that swims by.', 'Ruler Ray mengukur segala yang berenang lalu.'),
        [match([('2 m', '200 cm'), ('3 m', '300 cm'), ('5 m', '500 cm')], MT, T('There are 100 centimetres in 1 metre.', 'Terdapat 100 sentimeter dalam 1 meter.')),
         match([('1 m 50 cm', '150 cm'), ('2 m 5 cm', '205 cm'), ('3 m 40 cm', '340 cm'), ('4 m 10 cm', '410 cm')], MT, T('Change the metres to centimetres first, then add.', 'Tukar meter kepada sentimeter dahulu, kemudian tambah.')),
         match([('250 cm', '2 m 50 cm'), ('305 cm', '3 m 5 cm'), ('105 cm', '1 m 5 cm'), ('480 cm', '4 m 80 cm'), ('700 cm', '7 m')], MT, T('Every 100 centimetres makes 1 metre.', 'Setiap 100 sentimeter membentuk 1 meter.'))])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Ocean Census', 'Banci Lautan'),
        T('The marine rangers counted the sea creatures they saw. Read the chart!', 'Renjer marin mengira makhluk laut yang mereka lihat. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Counter', T('Counter never loses count of the fish.', 'Counter tidak pernah tersalah kira ikan.'),
        [chart([(T('Sharks', 'Jerung'), 14, 'grape'), (T('Turtles', 'Penyu'), 9, 'mint'), (T('Rays', 'Pari'), 12, 'sky')], ('diff', 0, 1), T('animals', 'haiwan')),
         chart([(T('Sharks', 'Jerung'), 10, 'grape'), (T('Turtles', 'Penyu'), 25, 'mint'), (T('Rays', 'Pari'), 15, 'sky'), (T('Whales', 'Ikan paus'), 30, 'coral')], ('sum', [0, 1, 2, 3]), T('animals', 'haiwan')),
         chart([(T('Mon', 'Isnin'), 20, 'grape'), (T('Tue', 'Selasa'), 35, 'mint'), (T('Wed', 'Rabu'), 25, 'sky'), (T('Thu', 'Khamis'), 40, 'coral'), (T('Fri', 'Jumaat'), 30, 'sun')], ('mean',), T('animals', 'haiwan'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Abyss Finale', 'Kemuncak Jurang'),
        T('The last dive goes to the very bottom of the ocean! Solve three steps to reach it.', 'Selaman terakhir sampai ke dasar lautan! Selesaikan tiga langkah untuk sampai ke sana.'),
        T('Multi-step problems with depth, length and big numbers.', 'Masalah berbilang langkah dengan kedalaman, panjang dan nombor besar.'),
        'Abyssal', T('Abyssal glows in the dark.', 'Abyssal bercahaya dalam gelap.'),
        [steps([step(T('A submarine dives 25 m every minute for 4 minutes. How many metres down is that?', 'Sebuah kapal selam menyelam 25 m setiap minit selama 4 minit. Berapa meter ke bawah itu?'), 100, '4*25', lambda v: f'{v} m'),
                step(T('Then it rises 30 m. How many metres below the surface is it now?', 'Kemudian ia naik 30 m. Berapa meter di bawah permukaan ia sekarang?'), 70, '100-30', lambda v: f'{v} m'),
                step(T('Rescue cables are 10 m long. How many cables reach that depth?', 'Kabel penyelamat sepanjang 10 m. Berapa kabel yang sampai ke kedalaman itu?'), 7, '70/10')],
               T('Multiply, then subtract, then divide.', 'Darab, kemudian tolak, kemudian bahagi.'), T('4 × 25 = 100, then 100 − 30 = 70, then 70 ÷ 10 = 7.', '4 × 25 = 100, kemudian 100 − 30 = 70, kemudian 70 ÷ 10 = 7.'), 'do10a'),
         steps([step(T('A coral reef is 8 m wide. A diver swims along it 6 times. How many metres does she swim?', 'Sebuah terumbu karang selebar 8 m. Seorang penyelam berenang di sepanjangnya 6 kali. Berapa meter dia berenang?'), 48, '8*6', lambda v: f'{v} m'),
                step(T('How many centimetres is that? (1 m = 100 cm)', 'Berapa sentimeter itu? (1 m = 100 cm)'), 4800, '48*100', lambda v: f'{v} cm'),
                step(T('She swims 200 cm more. How many centimetres in total?', 'Dia berenang 200 cm lagi. Berapa sentimeter kesemuanya?'), 5000, '4800+200', lambda v: f'{v} cm')],
               T('Multiply by 100 to change metres into centimetres.', 'Darab dengan 100 untuk menukar meter kepada sentimeter.'), T('8 × 6 = 48, then 48 × 100 = 4,800, then 4,800 + 200 = 5,000.', '8 × 6 = 48, kemudian 48 × 100 = 4,800, kemudian 4,800 + 200 = 5,000.'), 'do10b'),
         steps([step(T('Some fish live at 50 m. Whales dive 6 times deeper. How deep is that?', 'Sesetengah ikan tinggal pada 50 m. Ikan paus menyelam 6 kali lebih dalam. Berapa dalam itu?'), 300, '50*6', lambda v: f'{v} m'),
                step(T('A giant squid lives 80 m deeper than the whale. How deep is the squid?', 'Sotong gergasi tinggal 80 m lebih dalam daripada ikan paus. Berapa dalam sotong itu?'), 380, '300+80', lambda v: f'{v} m'),
                step(T('The seabed is at 1000 m. How many metres is it below the squid?', 'Dasar laut berada pada 1000 m. Berapa meter ia di bawah sotong itu?'), 620, '1000-380', lambda v: f'{v} m')],
               T('Work down one depth at a time.', 'Kira satu kedalaman pada satu masa.'), T('50 × 6 = 300, then 300 + 80 = 380, then 1000 − 380 = 620.', '50 × 6 = 300, kemudian 300 + 80 = 380, kemudian 1000 − 380 = 620.'), 'do10c')])
    return L
