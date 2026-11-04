from lib import *
CODE, BASE = 'rf', 162
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Bolt Beat', 'Rentak Bolt'),
        T('The robots blink their lights in a pattern. Which number comes next?', 'Robot mengerdipkan lampu mereka dalam satu pola. Nombor manakah yang seterusnya?'),
        T('Find the rule of a number pattern.', 'Mencari peraturan bagi pola nombor.'),
        'Blinky', T('Blinky flashes in time with the music.', 'Blinky berkelip mengikut irama muzik.'),
        [pattern('arith', 4, 4, 5, seed='rf1a'), pattern('arith', 7, 6, 5, seed='rf1b'), pattern('geo', 2, 3, 5, seed='rf1c')])
    add(2, 'reasoning', 'multi-step', 'adventurer', 'gears',
        T('Function Machine', 'Mesin Fungsi'),
        T('Numbers go into the machine and change step by step. Work out what comes out!', 'Nombor masuk ke dalam mesin dan berubah langkah demi langkah. Kira apa yang keluar!'),
        T('Follow a rule through several steps.', 'Mengikut satu peraturan melalui beberapa langkah.'),
        'Machy', T('Machy is happiest when every gear turns.', 'Machy paling gembira apabila setiap gear berputar.'),
        [steps([step(T('Put 4 into the machine. It multiplies by 3. What comes out?', 'Masukkan 4 ke dalam mesin. Ia mendarab dengan 3. Apa yang keluar?'), 12, '4*3'),
                step(T('A second machine adds 5. What comes out now?', 'Mesin kedua menambah 5. Apa yang keluar sekarang?'), 17, '12+5'),
                step(T('A third machine subtracts 7. What comes out?', 'Mesin ketiga menolak 7. Apa yang keluar?'), 10, '17-7')],
               T('Do each machine one at a time.', 'Lakukan setiap mesin satu demi satu.'), T('4 × 3 = 12, then 12 + 5 = 17, then 17 − 7 = 10.', '4 × 3 = 12, kemudian 12 + 5 = 17, kemudian 17 − 7 = 10.'), 'rf2a'),
         steps([step(T('Put 6 into the machine. It multiplies by 5. What comes out?', 'Masukkan 6 ke dalam mesin. Ia mendarab dengan 5. Apa yang keluar?'), 30, '6*5'),
                step(T('A second machine subtracts 8. What comes out now?', 'Mesin kedua menolak 8. Apa yang keluar sekarang?'), 22, '30-8'),
                step(T('A third machine halves the number. What comes out?', 'Mesin ketiga membahagi dua nombor itu. Apa yang keluar?'), 11, '22/2')],
               T('Halving means dividing by 2.', 'Membahagi dua bermaksud bahagi dengan 2.'), T('6 × 5 = 30, then 30 − 8 = 22, then 22 ÷ 2 = 11.', '6 × 5 = 30, kemudian 30 − 8 = 22, kemudian 22 ÷ 2 = 11.'), 'rf2b'),
         steps([step(T('Put 9 into the machine. It multiplies by 4. What comes out?', 'Masukkan 9 ke dalam mesin. Ia mendarab dengan 4. Apa yang keluar?'), 36, '9*4'),
                step(T('A second machine adds 14. What comes out now?', 'Mesin kedua menambah 14. Apa yang keluar sekarang?'), 50, '36+14'),
                step(T('A third machine divides by 5. What comes out?', 'Mesin ketiga membahagi dengan 5. Apa yang keluar?'), 10, '50/5')],
               T('Do each machine one at a time.', 'Lakukan setiap mesin satu demi satu.'), T('9 × 4 = 36, then 36 + 14 = 50, then 50 ÷ 5 = 10.', '9 × 4 = 36, kemudian 36 + 14 = 50, kemudian 50 ÷ 5 = 10.'), 'rf2c')])
    add(3, 'operations', 'factors', 'adventurer', 'gears',
        T('Gear Factors', 'Faktor Gear'),
        T('Each gear fits only two tiles that multiply to its number. Find the pair!', 'Setiap gear hanya muat dua jubin yang hasil darabnya ialah nombornya. Cari pasangan itu!'),
        T('Find two factors of a number.', 'Mencari dua faktor bagi sesuatu nombor.'),
        'Cogwell', T('Cogwell knows every gear by its number.', 'Cogwell mengenali setiap gear melalui nombornya.'),
        [tiles(24, [3, 8, 5, 7, 6, 2]), tiles(36, [4, 9, 5, 7, 6, 3]), tiles(60, [4, 15, 7, 8, 9, 11])])
    add(4, 'number-sense', 'addition', 'adventurer', 'scale',
        T('Weigh the Bolts', 'Timbang Bolt'),
        T('The robot scale needs exactly the right weights. Choose the weights that add up to the total!', 'Penimbang robot memerlukan pemberat yang tepat. Pilih pemberat yang jumlahnya sama dengan jumlah keseluruhan!'),
        T('Add masses to reach a total.', 'Menambah jisim untuk mencapai jumlah.'),
        'Boltsy', T('Boltsy has a bolt for every job.', 'Boltsy ada bolt untuk setiap tugasan.'),
        [balance(60, [25, 15, 35, 20, 10]), balance(150, [45, 60, 35, 70, 55, 90]), balance(400, [120, 150, 90, 175, 60, 220], 3)])
    add(5, 'operations', 'money', 'adventurer', 'chest',
        T('Spare Parts', 'Alat Ganti'),
        T('The spare parts shop sells screws, wires and tiny batteries. Pay for each part with exact coins!', 'Kedai alat ganti menjual skru, wayar dan bateri kecil. Bayar setiap bahagian dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Wirey', T('Wirey is always a little bit tangled.', 'Wirey sentiasa sedikit kusut.'),
        [coins(75, [5, 10, 20, 50]), coins(210, [10, 20, 50, 100]), coins(365, [5, 10, 20, 50, 100], 7)])
    add(6, 'operations', 'multiples', 'adventurer', 'door',
        T('Multiple Match', 'Padanan Gandaan'),
        T('The robots store their answers in lockers. Match each sum to the number in the locker!', 'Robot menyimpan jawapan mereka dalam loker. Padankan setiap pengiraan dengan nombor dalam loker!'),
        T('Link multiplication facts with their multiples.', 'Menghubungkan fakta darab dengan gandaannya.'),
        'Lockie', T('Lockie keeps every secret locked tight.', 'Lockie menyimpan setiap rahsia dengan rapat.'),
        [match([('3 × 4', '12'), ('5 × 6', '30'), ('7 × 3', '21')], MP_, T('Multiply the two numbers.', 'Darabkan kedua-dua nombor itu.')),
         match([('4 × 8', '32'), ('6 × 5', '30'), ('9 × 3', '27'), ('7 × 6', '42')], MP_, T('Multiply the two numbers.', 'Darabkan kedua-dua nombor itu.')),
         match([('6 × 7', '42'), ('8 × 9', '72'), ('9 × 4', '36'), ('12 × 5', '60'), ('11 × 3', '33')], MP_, T('Start with the facts you know best.', 'Mulakan dengan fakta yang paling anda tahu.'))])
    add(7, 'operations', 'sharing', 'master', 'picnic',
        T('Oil Cans', 'Tin Minyak'),
        T('The robots share their oil cans equally. Make sure every robot gets the same!', 'Robot berkongsi tin minyak mereka sama banyak. Pastikan setiap robot mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Oily', T('Oily squeaks until it gets a drop of oil.', 'Oily berdecit sehingga mendapat setitik minyak.'),
        [share(12, 3), share(24, 4), share(30, 5)])
    add(8, 'number-sense', 'fractions', 'master', 'tank',
        T('Battery Tank', 'Tangki Bateri'),
        T('Charge each battery tank to the right line before the robots wake up!', 'Cas setiap tangki bateri hingga garisan yang betul sebelum robot bangun!'),
        T('Fractions of a tank.', 'Pecahan sebuah tangki.'),
        'Voltie', T('Voltie crackles when the battery is full.', 'Voltie berdesing apabila bateri penuh.'),
        [tank(8, 3, 4), tank(10, 2, 5), tank(12, 5, 6)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Production Chart', 'Carta Pengeluaran'),
        T('The factory counted the robots it built each day. Read the chart!', 'Kilang mengira robot yang dibinanya setiap hari. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Chartbot', T('Chartbot draws a bar for everything.', 'Chartbot melukis palang untuk segalanya.'),
        [chart([(T('Mon', 'Isnin'), 28, 'sky'), (T('Tue', 'Selasa'), 19, 'grape'), (T('Wed', 'Rabu'), 24, 'mint')], ('diff', 0, 1), T('robots', 'robot')),
         chart([(T('Mon', 'Isnin'), 22, 'sky'), (T('Tue', 'Selasa'), 35, 'grape'), (T('Wed', 'Rabu'), 18, 'mint'), (T('Thu', 'Khamis'), 40, 'sun')], ('sum', [0, 1, 2, 3]), T('robots', 'robot')),
         chart([(T('Mon', 'Isnin'), 24, 'sky'), (T('Tue', 'Selasa'), 36, 'grape'), (T('Wed', 'Rabu'), 30, 'mint'), (T('Thu', 'Khamis'), 42, 'sun'), (T('Fri', 'Jumaat'), 18, 'coral')], ('mean',), T('robots', 'robot'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Factory Finale', 'Kemuncak Kilang'),
        T('The factory is about to build its greatest robot! Solve three steps to switch it on.', 'Kilang hampir membina robot terhebatnya! Selesaikan tiga langkah untuk menghidupkannya.'),
        T('Multi-step problems with output, money and time.', 'Masalah berbilang langkah dengan hasil pengeluaran, wang dan masa.'),
        'Megabot', T('Megabot is the biggest and the gentlest robot.', 'Megabot ialah robot paling besar dan paling lembut.'),
        [steps([step(T('A machine makes 9 robots every hour. How many robots in 8 hours?', 'Sebuah mesin membuat 9 robot setiap jam. Berapa robot dalam 8 jam?'), 72, '9*8'),
                step(T('15 robots are faulty. How many robots work?', '15 robot rosak. Berapa robot yang berfungsi?'), 57, '72-15'),
                step(T('The working robots are packed 3 to a box. How many boxes are needed?', 'Robot yang berfungsi dipek 3 dalam sekotak. Berapa kotak diperlukan?'), 19, '57/3')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('9 × 8 = 72, then 72 − 15 = 57, then 57 ÷ 3 = 19.', '9 × 8 = 72, kemudian 72 − 15 = 57, kemudian 57 ÷ 3 = 19.'), 'rf10a'),
         steps([step(T('A robot costs RM25. What do 6 robots cost?', 'Seorang robot berharga RM25. Berapa harga 6 robot?'), 150, '6*25', RM),
                step(T('The factory gives RM20 off. How much do you pay?', 'Kilang memberi potongan RM20. Berapa yang anda bayar?'), 130, '150-20', RM),
                step(T('5 shops share the cost equally. How much does each shop pay?', '5 buah kedai berkongsi kos itu sama banyak. Berapa yang dibayar oleh setiap kedai?'), 26, '130/5', RM)],
               T('Take the discount off before you share.', 'Tolak potongan sebelum berkongsi.'), T('6 × 25 = 150, then 150 − 20 = 130, then 130 ÷ 5 = 26.', '6 × 25 = 150, kemudian 150 − 20 = 130, kemudian 130 ÷ 5 = 26.'), 'rf10b'),
         steps([step(T('A battery lasts 45 minutes. How many minutes do 4 batteries last?', 'Sebuah bateri tahan selama 45 minit. Berapa minit 4 bateri tahan?'), 180, '4*45'),
                step(T('How many hours is that? (60 minutes = 1 hour)', 'Berapa jam itu? (60 minit = 1 jam)'), 3, '180/60'),
                step(T('The robot uses 12 litres of oil every hour. How many litres does it use in that time?', 'Robot itu menggunakan 12 liter minyak setiap jam. Berapa liter yang digunakannya dalam masa itu?'), 36, '3*12', lambda v: f'{v} L')],
               T('Change the minutes into hours first.', 'Tukar minit kepada jam dahulu.'), T('4 × 45 = 180, then 180 ÷ 60 = 3, then 3 × 12 = 36.', '4 × 45 = 180, kemudian 180 ÷ 60 = 3, kemudian 3 × 12 = 36.'), 'rf10c')])
    return L
