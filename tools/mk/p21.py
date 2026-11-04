from lib import *
CODE, BASE = 'kv', 212
MP_ = T('Tap one, then tap the one that is worth the same.', 'Ketik satu, kemudian ketik yang sama nilainya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'operations', 'money', 'adventurer', 'chest',
        T('Sen and Ringgit', 'Sen dan Ringgit'),
        T('At the kampung shop every price is written two ways. Match the ringgit to the sen!', 'Di kedai kampung setiap harga ditulis dua cara. Padankan ringgit dengan sen!'),
        T('Change between ringgit and sen.', 'Menukar antara ringgit dan sen.'),
        'Kuih', T('Kuih is round, soft and always sweet.', 'Kuih bulat, lembut dan sentiasa manis.'),
        [match([('RM1', '100 sen'), ('RM2', '200 sen'), ('50 sen', 'RM0.50')], MP_, T('RM1 is 100 sen.', 'RM1 ialah 100 sen.')),
         match([('RM3', '300 sen'), ('RM1.50', '150 sen'), ('RM0.80', '80 sen'), ('250 sen', 'RM2.50')], MP_, T('RM1 is 100 sen, so RM1.50 is 150 sen.', 'RM1 ialah 100 sen, jadi RM1.50 ialah 150 sen.')),
         match([('RM4.20', '420 sen'), ('RM0.05', '5 sen'), ('RM6.75', '675 sen'), ('310 sen', 'RM3.10'), ('RM10', '1000 sen')], MP_, T('Multiply ringgit by 100 to get sen.', 'Darab ringgit dengan 100 untuk mendapat sen.'))])
    add(2, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('Road to the Village', 'Jalan ke Kampung'),
        T('The village road has a sign every few kilometres. Slide the bicycle to the right sign!', 'Jalan kampung ada papan tanda setiap beberapa kilometer. Gelongsorkan basikal ke papan tanda yang betul!'),
        T('Place numbers on a line in tens and fifties.', 'Meletakkan nombor pada garis dalam puluh dan lima puluh.'),
        'Pedal', T('Pedal rides the same road every morning.', 'Pedal menunggang di jalan yang sama setiap pagi.'),
        [numberline(40, 0, 100, 10, 20), numberline(350, 0, 500, 50, 100), numberline(70, 0, 200, 10, 50, kind='half', a=20, b=120)])
    add(3, 'operations', 'money', 'adventurer', 'chest',
        T('Nasi Lemak Stall', 'Gerai Nasi Lemak'),
        T('Aunty sells nasi lemak at the roadside. Pay for each order with exactly the right coins!', 'Mak Cik menjual nasi lemak di tepi jalan. Bayar setiap pesanan dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Sambal', T('Sambal is spicy but very kind.', 'Sambal pedas tetapi sangat baik hati.'),
        [coins(120, [5, 10, 20, 50]), coins(275, [5, 10, 20, 50, 100]), coins(430, [5, 10, 20, 50, 100], 7)])
    add(4, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Kenduri Share', 'Kongsi Kenduri'),
        T('The whole village is having a kenduri. Share the food so every table gets the same!', 'Seluruh kampung mengadakan kenduri. Kongsi makanan supaya setiap meja mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Kenduri', T('Kenduri always saves the best seat.', 'Kenduri sentiasa menyimpan tempat duduk terbaik.'),
        [share(12, 3), share(20, 4), share(25, 5)])
    add(5, 'number-sense', 'length', 'adventurer', 'scale',
        T('Market Scales', 'Penimbang Pasar'),
        T('The kampung scales need the right weights. Pick weights in grams that make the total!', 'Penimbang kampung memerlukan pemberat yang betul. Pilih pemberat dalam gram yang jumlahnya sama!'),
        T('Add masses in grams.', 'Menambah jisim dalam gram.'),
        'Gram', T('Gram can feel even a single grain of rice.', 'Gram dapat merasa walau sebutir beras.'),
        [balance(750, [500, 250, 300, 200, 100]), balance(1200, [700, 500, 400, 300, 600]), balance(2000, [800, 1200, 500, 700, 900, 300], 3)])
    add(6, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Rambutan Trees', 'Pokok Rambutan'),
        T('Rambutan trees grow in a pattern along the path. How many fruits are on the next tree?', 'Pokok rambutan tumbuh mengikut pola di sepanjang laluan. Berapa buah pada pokok seterusnya?'),
        T('Continue counting patterns.', 'Menyambung pola pengiraan.'),
        'Rambo', T('Rambo is hairy, red and very juicy.', 'Rambo berbulu, merah dan sangat berair.'),
        [pattern('arith', 3, 3, 5, seed='kv6a'), pattern('arith', 100, -10, 6, hidden=3, seed='kv6b'), pattern('geo', 2, 2, 6, hidden=4, seed='kv6c')])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Fruit Baskets', 'Bakul Buah'),
        T('Fruit is packed in baskets of equal size. Find the two tiles that make each total!', 'Buah dipek dalam bakul yang sama saiz. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Basket', T('Basket carries more than it looks.', 'Basket membawa lebih daripada yang kelihatan.'),
        [tiles(24, [3, 8, 4, 6, 2, 12]), tiles(56, [7, 8, 6, 9, 4, 14]), tiles(90, [9, 10, 6, 15, 8, 12])])
    add(8, 'number-sense', 'length', 'master', 'door',
        T('Kilos and Litres', 'Kilo dan Liter'),
        T('The shop weighs rice and pours oil. Match each amount to the same amount in other units!', 'Kedai menimbang beras dan menuang minyak. Padankan setiap jumlah dengan jumlah yang sama dalam unit lain!'),
        T('Convert kilograms, grams, litres and millilitres.', 'Menukar kilogram, gram, liter dan mililiter.'),
        'Kilo', T('Kilo is the heaviest sleeper in the village.', 'Kilo ialah pelena paling berat di kampung.'),
        [match([('1 kg', '1000 g'), ('2 kg', '2000 g'), ('3 kg', '3000 g')], MP_, T('1 kg is 1000 g.', '1 kg ialah 1000 g.')),
         match([('500 g', '0.5 kg'), ('1.5 kg', '1500 g'), ('2.5 kg', '2500 g'), ('4 kg', '4000 g')], MP_, T('1 kg is 1000 g, so half a kilogram is 500 g.', '1 kg ialah 1000 g, jadi setengah kilogram ialah 500 g.')),
         match([('1 L', '1000 mL'), ('2.5 L', '2500 mL'), ('750 mL', '0.75 L'), ('3 L', '3000 mL'), ('250 mL', '0.25 L')], MP_, T('1 L is 1000 mL.', '1 L ialah 1000 mL.'))])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Orchard Chart', 'Carta Kebun'),
        T('The orchard keeper counted the fruit picked today. Read the chart!', 'Penjaga kebun mengira buah yang dipetik hari ini. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Orchard', T('Orchard never lets a fruit fall.', 'Orchard tidak pernah membiarkan buah jatuh.'),
        [chart([(T('Rambutan', 'Rambutan'), 15, 'coral'), (T('Durian', 'Durian'), 9, 'sun'), (T('Mangosteen', 'Manggis'), 12, 'grape')], ('diff', 0, 1), T('fruits', 'buah')),
         chart([(T('Rambutan', 'Rambutan'), 20, 'coral'), (T('Durian', 'Durian'), 15, 'sun'), (T('Mangosteen', 'Manggis'), 25, 'grape'), (T('Banana', 'Pisang'), 30, 'mint')], ('sum', [0, 1, 2, 3]), T('fruits', 'buah')),
         chart([(T('Mon', 'Isnin'), 12, 'coral'), (T('Tue', 'Selasa'), 18, 'sun'), (T('Wed', 'Rabu'), 24, 'grape'), (T('Thu', 'Khamis'), 6, 'sky'), (T('Fri', 'Jumaat'), 30, 'mint')], ('mean',), T('fruits', 'buah'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Kampung Festival', 'Pesta Kampung'),
        T('The kampung festival is today! Help the villagers with three steps of sums.', 'Pesta kampung hari ini! Bantu penduduk kampung dengan tiga langkah pengiraan.'),
        T('Multi-step problems with money, fruit and weights.', 'Masalah berbilang langkah dengan wang, buah dan berat.'),
        'Pesta', T('Pesta claps along with every song.', 'Pesta bertepuk tangan dengan setiap lagu.'),
        [steps([step(T('Nasi lemak costs RM3 a packet. What do 8 packets cost?', 'Nasi lemak berharga RM3 sebungkus. Berapa harga 8 bungkus?'), 24, '8*3', RM),
                step(T('You pay with RM50. How much change do you get?', 'Anda membayar dengan RM50. Berapa baki yang anda terima?'), 26, '50-24', RM),
                step(T('You spend half of the change on kuih. How much do you spend on kuih?', 'Anda membelanjakan separuh baki untuk kuih. Berapa yang dibelanjakan untuk kuih?'), 13, '26/2', RM)],
               T('Multiply, then subtract, then halve.', 'Darab, kemudian tolak, kemudian bahagi dua.'), T('8 × 3 = 24, then 50 − 24 = 26, then 26 ÷ 2 = 13.', '8 × 3 = 24, kemudian 50 − 24 = 26, kemudian 26 ÷ 2 = 13.'), 'kv10a'),
         steps([step(T('A farmer picks 6 baskets with 12 rambutans in each. How many rambutans?', 'Seorang petani memetik 6 bakul dengan 12 rambutan dalam setiap satu. Berapa rambutan?'), 72, '6*12'),
                step(T('He gives away 18. How many are left?', 'Dia memberikan 18. Berapa yang tinggal?'), 54, '72-18'),
                step(T('The rest are shared equally among 9 neighbours. How many does each neighbour get?', 'Bakinya dikongsi sama banyak antara 9 jiran. Berapa yang diperoleh setiap jiran?'), 6, '54/9')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('6 × 12 = 72, then 72 − 18 = 54, then 54 ÷ 9 = 6.', '6 × 12 = 72, kemudian 72 − 18 = 54, kemudian 54 ÷ 9 = 6.'), 'kv10b'),
         steps([step(T('A durian weighs 2 kg. How many grams do 5 durians weigh? (1 kg = 1000 g)', 'Sebiji durian beratnya 2 kg. Berapa gram berat 5 biji durian? (1 kg = 1000 g)'), 10000, '5*2*1000', lambda v: f'{v} g'),
                step(T('The seller sells 3500 g. How many grams are left?', 'Penjual menjual 3500 g. Berapa gram yang tinggal?'), 6500, '10000-3500', lambda v: f'{v} g'),
                step(T('Each bag holds 500 g. How many bags can be filled?', 'Setiap beg memuatkan 500 g. Berapa beg yang boleh diisi?'), 13, '6500/500')],
               T('Change kilograms to grams first.', 'Tukar kilogram kepada gram dahulu.'), T('5 × 2 × 1000 = 10000, then 10000 − 3500 = 6500, then 6500 ÷ 500 = 13.', '5 × 2 × 1000 = 10000, kemudian 10000 − 3500 = 6500, kemudian 6500 ÷ 500 = 13.'), 'kv10c')])
    return L
