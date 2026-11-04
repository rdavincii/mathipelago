from lib import *
CODE, BASE = 'rb', 192
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Red Stripe Tank', 'Tangki Jalur Merah'),
        T('The red stripe of the rainbow needs paint! Fill each tank to the right line.', 'Jalur merah pelangi memerlukan cat! Isi setiap tangki hingga garisan yang betul.'),
        T('Show fractions of a tank.', 'Menunjukkan pecahan sebuah tangki.'),
        'Rosy', T('Rosy paints the first stripe every morning.', 'Rosy mengecat jalur pertama setiap pagi.'),
        [tank(8, 3, 4), tank(12, 2, 3), tank(10, 7, 10)])
    add(2, 'number-sense', 'fractions', 'adventurer', 'door',
        T('Orange Twins', 'Kembar Oren'),
        T('Orange paint comes in matching pairs. Pair each fraction with its equal twin!', 'Cat oren datang berpasangan. Padankan setiap pecahan dengan kembarnya yang sama nilai!'),
        T('Match equivalent fractions.', 'Memadankan pecahan setara.'),
        'Tangy', T('Tangy always arrives with a twin.', 'Tangy sentiasa datang bersama kembarnya.'),
        [match([('1/2', '3/6'), ('1/3', '4/12'), ('2/5', '4/10')], MP_, T('Multiply the top and the bottom by the same number.', 'Darabkan atas dan bawah dengan nombor yang sama.')),
         match([('3/4', '9/12'), ('2/3', '8/12'), ('5/6', '10/12'), ('1/5', '3/15')], MP_, T('Multiply the top and the bottom by the same number.', 'Darabkan atas dan bawah dengan nombor yang sama.')),
         match([('6/9', '2/3'), ('9/15', '3/5'), ('12/16', '3/4'), ('4/20', '1/5'), ('10/12', '5/6')], MP_, T('Divide the top and the bottom by the same number.', 'Bahagikan atas dan bawah dengan nombor yang sama.'))])
    add(3, 'number-sense', 'decimals', 'adventurer', 'door',
        T('Yellow Decimals', 'Perpuluhan Kuning'),
        T('Yellow paint pots are labelled with fractions and decimals. Match the same amounts!', 'Pasu cat kuning dilabel dengan pecahan dan perpuluhan. Padankan jumlah yang sama!'),
        T('Match fractions with decimals.', 'Memadankan pecahan dengan perpuluhan.'),
        'Sunny', T('Sunny glows brighter with every match.', 'Sunny bercahaya lebih terang setiap kali padanan betul.'),
        [match([('1/10', '0.1'), ('1/2', '0.5'), ('3/10', '0.3')], MP_, T('Tenths have one digit after the point.', 'Persepuluh mempunyai satu digit selepas titik.')),
         match([('1/4', '0.25'), ('3/4', '0.75'), ('1/5', '0.2'), ('4/5', '0.8')], MP_, T('Change the fraction so the bottom is 10 or 100.', 'Tukar pecahan supaya penyebutnya 10 atau 100.')),
         match([('7/100', '0.07'), ('9/20', '0.45'), ('3/25', '0.12'), ('7/50', '0.14'), ('13/20', '0.65')], MP_, T('Make the bottom 100 first.', 'Jadikan penyebut 100 dahulu.'))])
    add(4, 'number-sense', 'decimals', 'master', 'gate',
        T('Green Percent', 'Peratus Hijau'),
        T('Percent means out of 100. Match each percent to the fraction or decimal it equals!', 'Peratus bermaksud daripada 100. Padankan setiap peratus dengan pecahan atau perpuluhan yang sama nilainya!'),
        T('Match percentages with fractions and decimals.', 'Memadankan peratus dengan pecahan dan perpuluhan.'),
        'Leafy', T('Leafy turns a deeper green with every percent.', 'Leafy menjadi semakin hijau dengan setiap peratus.'),
        [match([('50%', '1/2'), ('25%', '1/4'), ('75%', '3/4')], MP_, T('50% is 50 out of 100, which is one half.', '50% ialah 50 daripada 100, iaitu setengah.')),
         match([('10%', '0.1'), ('20%', '1/5'), ('60%', '0.6'), ('40%', '2/5')], MP_, T('Percent means hundredths: 10% = 10/100 = 0.1.', 'Peratus bermaksud perseratus: 10% = 10/100 = 0.1.')),
         match([('5%', '0.05'), ('35%', '0.35'), ('80%', '4/5'), ('12%', '0.12'), ('90%', '9/10')], MP_, T('Write the percent over 100.', 'Tulis peratus itu dalam 100.'))])
    add(5, 'number-sense', 'ratio', 'master', 'picnic',
        T('Blue Mix', 'Campuran Biru'),
        T('Blue paint is mixed from two colours. Keep the ratio the same as you make more!', 'Cat biru dicampur daripada dua warna. Kekalkan nisbah apabila membuat lebih banyak!'),
        T('Use ratios to scale a recipe up.', 'Menggunakan nisbah untuk menggandakan resipi.'),
        'Splash', T('Splash never mixes the colours too early.', 'Splash tidak pernah mencampur warna terlalu awal.'),
        [steps([step(T('The mix uses 2 tins of white for every 1 tin of blue. How many tins of white for 3 tins of blue?', 'Campuran menggunakan 2 tin putih bagi setiap 1 tin biru. Berapa tin putih untuk 3 tin biru?'), 6, '3*2'),
                step(T('How many tins is that altogether (white and blue)?', 'Berapa tin kesemuanya (putih dan biru)?'), 9, '6+3'),
                step(T('Each tin costs RM4. How much is the whole mix?', 'Setiap tin berharga RM4. Berapa harga seluruh campuran itu?'), 36, '9*4', RM)],
               T('For every 1 blue there are 2 white.', 'Bagi setiap 1 biru ada 2 putih.'), T('3 × 2 = 6, then 6 + 3 = 9, then 9 × 4 = RM36.', '3 × 2 = 6, kemudian 6 + 3 = 9, kemudian 9 × 4 = RM36.'), 'rb5a'),
         steps([step(T('Paint is 3 parts red to 2 parts yellow. How many parts of red for 4 batches?', 'Cat itu 3 bahagian merah kepada 2 bahagian kuning. Berapa bahagian merah untuk 4 kelompok?'), 12, '4*3'),
                step(T('How many parts of yellow for 4 batches?', 'Berapa bahagian kuning untuk 4 kelompok?'), 8, '4*2'),
                step(T('How many parts of paint in total?', 'Berapa bahagian cat kesemuanya?'), 20, '12+8')],
               T('Multiply each part by the number of batches.', 'Darabkan setiap bahagian dengan bilangan kelompok.'), T('4 × 3 = 12, 4 × 2 = 8, then 12 + 8 = 20.', '4 × 3 = 12, 4 × 2 = 8, kemudian 12 + 8 = 20.'), 'rb5b'),
         steps([step(T('A mix is 5 parts blue to 3 parts white. How many parts are in one batch?', 'Satu campuran ialah 5 bahagian biru kepada 3 bahagian putih. Berapa bahagian dalam satu kelompok?'), 8, '5+3'),
                step(T('Each part holds 25 mL. How many mL of paint in one batch?', 'Setiap bahagian memuatkan 25 mL. Berapa mL cat dalam satu kelompok?'), 200, '8*25', lambda v: f'{v} mL'),
                step(T('How many mL of blue paint are in 6 batches?', 'Berapa mL cat biru dalam 6 kelompok?'), 750, '6*5*25', lambda v: f'{v} mL')],
               T('Blue is 5 of the 8 parts.', 'Biru ialah 5 daripada 8 bahagian.'), T('5 + 3 = 8, then 8 × 25 = 200, and 6 × 5 × 25 = 750.', '5 + 3 = 8, kemudian 8 × 25 = 200, dan 6 × 5 × 25 = 750.'), 'rb5c')])
    add(6, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Indigo Lanterns', 'Tanglung Nila'),
        T('Indigo lanterns glow in a pattern along the bridge. Which number comes next?', 'Tanglung nila bercahaya mengikut pola di sepanjang jambatan. Nombor manakah yang seterusnya?'),
        T('Continue number patterns with big steps.', 'Menyambung pola nombor dengan langkah besar.'),
        'Glowy', T('Glowy lights up in the same order every night.', 'Glowy menyala dalam urutan yang sama setiap malam.'),
        [pattern('arith', 12, 12, 5, seed='rb6a'), pattern('geo', 2, 3, 5, seed='rb6b'), pattern('arith', 100, -15, 6, hidden=4, seed='rb6c')])
    add(7, 'number-sense', 'number-line', 'master', 'bridge',
        T('Violet Percent Line', 'Garis Peratus Ungu'),
        T('The violet line runs from 0 to 100 percent. Slide the marker to the right place!', 'Garis ungu bermula dari 0 hingga 100 peratus. Gelongsorkan penanda ke tempat yang betul!'),
        T('Place numbers from 0 to 100 on a line.', 'Meletakkan nombor dari 0 hingga 100 pada garis.'),
        'Violet', T('Violet slides smoothly along the line.', 'Violet menggelongsor dengan lancar di sepanjang garis.'),
        [numberline(25, 0, 100, 5, 25), numberline(85, 0, 100, 5, 25), numberline(45, 0, 100, 5, 25, kind='half', a=30, b=60)])
    add(8, 'shape-data', 'data', 'master', 'lighthouse',
        T('Rainbow Chart', 'Carta Pelangi'),
        T('The sky watchers counted how many times each colour showed. Read the chart!', 'Pemerhati langit mengira berapa kali setiap warna muncul. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Prism', T('Prism splits every light into colours.', 'Prism memecahkan setiap cahaya kepada warna.'),
        [chart([(T('Red', 'Merah'), 14, 'coral'), (T('Yellow', 'Kuning'), 9, 'sun'), (T('Blue', 'Biru'), 12, 'sky')], ('diff', 0, 1), T('rainbows', 'pelangi')),
         chart([(T('Red', 'Merah'), 20, 'coral'), (T('Yellow', 'Kuning'), 35, 'sun'), (T('Blue', 'Biru'), 25, 'sky'), (T('Green', 'Hijau'), 40, 'mint')], ('sum', [0, 1, 2, 3]), T('rainbows', 'pelangi')),
         chart([(T('Red', 'Merah'), 18, 'coral'), (T('Yellow', 'Kuning'), 30, 'sun'), (T('Blue', 'Biru'), 24, 'sky'), (T('Green', 'Hijau'), 12, 'mint'), (T('Violet', 'Ungu'), 36, 'grape')], ('mean',), T('rainbows', 'pelangi'))])
    add(9, 'operations', 'money', 'master', 'chest',
        T('Pot of Gold', 'Periuk Emas'),
        T('At the end of the rainbow is a pot of gold coins. Pay for each treasure exactly!', 'Di hujung pelangi ada periuk syiling emas. Bayar setiap harta dengan tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Goldie', T('Goldie counts the coins twice, just to be sure.', 'Goldie mengira syiling dua kali, untuk pastikan.'),
        [coins(165, [5, 10, 20, 50, 100]), coins(330, [10, 20, 50, 100], 7), coins(595, [5, 10, 20, 50, 100], 9)])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Rainbow Finale', 'Kemuncak Pelangi'),
        T('Every colour is ready. Solve the three-step problems to finish the rainbow bridge!', 'Setiap warna sudah sedia. Selesaikan masalah tiga langkah untuk melengkapkan jambatan pelangi!'),
        T('Multi-step problems with fractions, percent and money.', 'Masalah berbilang langkah dengan pecahan, peratus dan wang.'),
        'Arcie', T('Arcie bends over every bridge in the sky.', 'Arcie melengkung di setiap jambatan di langit.'),
        [steps([step(T('A rainbow has 60 tiles. One third are red. How many red tiles?', 'Sebuah pelangi mempunyai 60 jubin. Satu pertiga berwarna merah. Berapa jubin merah?'), 20, '60/3'),
                step(T('Half of the red tiles are painted twice. How many tiles is that?', 'Separuh daripada jubin merah dicat dua kali. Berapa jubin itu?'), 10, '20/2'),
                step(T('Each painted tile uses 3 tins. How many tins are used for them?', 'Setiap jubin yang dicat menggunakan 3 tin. Berapa tin digunakan untuknya?'), 30, '10*3')],
               T('One third means divide by 3.', 'Satu pertiga bermaksud bahagi dengan 3.'), T('60 ÷ 3 = 20, then 20 ÷ 2 = 10, then 10 × 3 = 30.', '60 ÷ 3 = 20, kemudian 20 ÷ 2 = 10, kemudian 10 × 3 = 30.'), 'rb10a'),
         steps([step(T('A shop has 200 paint pots. 25% are sold. How many pots are sold?', 'Sebuah kedai mempunyai 200 pasu cat. 25% dijual. Berapa pasu dijual?'), 50, '200/4'),
                step(T('Each sold pot costs RM6. How much money is that?', 'Setiap pasu yang dijual berharga RM6. Berapa jumlah wang itu?'), 300, '50*6', RM),
                step(T('The shop spends RM120 on new brushes. How much money is left?', 'Kedai itu membelanjakan RM120 untuk berus baharu. Berapa wang yang tinggal?'), 180, '300-120', RM)],
               T('25% is the same as one quarter.', '25% sama dengan satu perempat.'), T('200 ÷ 4 = 50, then 50 × 6 = RM300, then 300 − 120 = RM180.', '200 ÷ 4 = 50, kemudian 50 × 6 = RM300, kemudian 300 − 120 = RM180.'), 'rb10b'),
         steps([step(T('A bridge is 3/5 painted. The bridge has 40 planks. How many planks are painted?', 'Sebuah jambatan telah dicat 3/5. Jambatan itu mempunyai 40 papan. Berapa papan telah dicat?'), 24, '40/5*3'),
                step(T('How many planks are not painted yet?', 'Berapa papan belum dicat?'), 16, '40-24'),
                step(T('A painter paints 4 planks an hour. How many hours to finish?', 'Seorang pelukis mengecat 4 papan sejam. Berapa jam untuk menyiapkannya?'), 4, '16/4')],
               T('Find one fifth first, then multiply by 3.', 'Cari satu perlima dahulu, kemudian darab dengan 3.'), T('40 ÷ 5 × 3 = 24, then 40 − 24 = 16, then 16 ÷ 4 = 4.', '40 ÷ 5 × 3 = 24, kemudian 40 − 24 = 16, kemudian 16 ÷ 4 = 4.'), 'rb10c')])
    return L
