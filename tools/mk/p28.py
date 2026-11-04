from lib import *
CODE, BASE = 'tw', 282
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Toy Train Track', 'Landasan Kereta Api Mainan'),
        T('The toy train track repeats a number pattern. Which number comes next?', 'Landasan kereta api mainan mengulang pola nombor. Nombor manakah seterusnya?'),
        T('Continue number patterns.', 'Menyambung pola nombor.'),
        'Choo Choo', T('Choo Choo toots at every number.', 'Choo Choo berbunyi pada setiap nombor.'),
        [pattern('arith', 4, 4, 5, seed='tw1a'), pattern('arith', 7, 6, 5, seed='tw1b'), pattern('geo', 2, 3, 5, hidden=3, seed='tw1c')])
    add(2, 'number-sense', 'multiples', 'adventurer', 'door',
        T('Machine In, Machine Out', 'Mesin Masuk, Mesin Keluar'),
        T('The toy machine changes every number the same way. Match each number going in to the number coming out!', 'Mesin mainan menukar setiap nombor dengan cara yang sama. Padankan setiap nombor yang masuk dengan nombor yang keluar!'),
        T('Find the rule: multiply by 3.', 'Cari peraturan: darab dengan 3.'),
        'Gizmo', T('Gizmo whirs when the rule is right.', 'Gizmo berdesing apabila peraturan betul.'),
        [match([('2', '6'), ('4', '12'), ('5', '15')], MP_, T('The machine multiplies by 3.', 'Mesin itu mendarab dengan 3.')),
         match([('1', '3'), ('6', '18'), ('7', '21'), ('9', '27')], MP_, T('The machine multiplies by 3.', 'Mesin itu mendarab dengan 3.')),
         match([('3', '9'), ('8', '24'), ('10', '30'), ('11', '33'), ('12', '36')], MP_, T('The machine multiplies by 3.', 'Mesin itu mendarab dengan 3.'))])
    add(3, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('Toy Shelf Line', 'Garis Rak Mainan'),
        T('Put each toy on the right spot of the shelf line!', 'Letakkan setiap mainan pada tempat yang betul di garis rak!'),
        T('Place numbers on a line.', 'Meletakkan nombor pada garis.'),
        'Shelfie', T('Shelfie keeps every toy in its place.', 'Shelfie menyimpan setiap mainan di tempatnya.'),
        [numberline(30, 0, 60, 5, 10), numberline(120, 0, 200, 20, 40), numberline(450, 0, 1000, 50, 250)])
    add(4, 'operations', 'addition', 'adventurer', 'scale',
        T('Balance the Blocks', 'Imbangkan Blok'),
        T('Pick the blocks that weigh exactly the same as the toy on the scale!', 'Pilih blok yang beratnya sama dengan mainan di atas penimbang!'),
        T('Add to make a total.', 'Menambah untuk mencapai jumlah.'),
        'Blocky', T('Blocky stacks everything in towers.', 'Blocky menyusun semuanya dalam menara.'),
        [balance(40, [10, 15, 25, 5, 20]), balance(90, [20, 35, 45, 30, 15]), balance(150, [35, 55, 40, 25, 60, 45], 3)])
    add(5, 'operations', 'times-tables', 'adventurer', 'gears',
        T('Gear Boxes', 'Kotak Gear'),
        T('Each box holds the same number of gears. Find the two tiles that make each total!', 'Setiap kotak mengandungi gear yang sama banyak. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts.', 'Fakta darab.'),
        'Cogsy', T('Cogsy spins when it is happy.', 'Cogsy berpusing apabila gembira.'),
        [tiles(24, [3, 8, 4, 6, 2, 12]), tiles(60, [6, 10, 5, 12, 4, 15]), tiles(96, [8, 12, 6, 16, 9, 10])])
    add(6, 'operations', 'factors', 'adventurer', 'picnic',
        T('Teddy Teams', 'Pasukan Teddy'),
        T('Teddies line up in equal teams. Which tile pairs multiply to the number of teddies?', 'Teddy beratur dalam pasukan yang sama banyak. Pasangan jubin manakah yang hasil darabnya ialah bilangan teddy?'),
        T('Factors of a number.', 'Faktor bagi suatu nombor.'),
        'Fuzzy', T('Fuzzy hugs the whole team.', 'Fuzzy memeluk seluruh pasukan.'),
        [tiles(18, [2, 9, 3, 6, 4, 5]), tiles(36, [4, 9, 6, 12, 3, 8]), tiles(48, [6, 8, 4, 12, 16, 3])])
    add(7, 'operations', 'money', 'master', 'chest',
        T('Toy Shop Coins', 'Syiling Kedai Mainan'),
        T('Pay for each toy with exactly the right coins!', 'Bayar setiap mainan dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Penny Toy', T('Penny Toy loves the sound of coins.', 'Penny Toy suka bunyi syiling.'),
        [coins(95, [5, 10, 20, 50]), coins(260, [10, 20, 50, 100]), coins(485, [5, 10, 20, 50, 100])])
    add(8, 'number-sense', 'fractions', 'master', 'tank',
        T('Paint Pots', 'Pasu Cat'),
        T('Fill each paint pot to the right line to paint the toys!', 'Isi setiap pasu cat hingga garisan yang betul untuk mengecat mainan!'),
        T('Fractions of a container.', 'Pecahan sebuah bekas.'),
        'Dabby', T('Dabby has paint on every paw.', 'Dabby ada cat pada setiap kakinya.'),
        [tank(8, 3, 4), tank(10, 2, 5), tank(12, 5, 6)])
    add(9, 'operations', 'multi-step', 'master', 'lighthouse',
        T('Rule Machine Chains', 'Rantaian Mesin Peraturan'),
        T('Two machines in a row! Follow each number through both machines.', 'Dua mesin berturutan! Ikuti setiap nombor melalui kedua-dua mesin.'),
        T('Follow a rule through two steps.', 'Mengikut peraturan melalui dua langkah.'),
        'Chainy', T('Chainy links everything together.', 'Chainy menghubungkan semuanya.'),
        [steps([step(T('Machine A adds 5. Put in 7. What comes out?', 'Mesin A menambah 5. Masukkan 7. Apa yang keluar?'), 12, '7+5'),
                step(T('Machine B doubles. Put in that number. What comes out?', 'Mesin B menggandakan. Masukkan nombor itu. Apa yang keluar?'), 24, '12*2'),
                step(T('Machine C subtracts 4. What comes out now?', 'Mesin C menolak 4. Apa yang keluar sekarang?'), 20, '24-4')],
               T('Do the machines one at a time.', 'Lakukan mesin satu demi satu.'), T('7 + 5 = 12, then 12 × 2 = 24, then 24 − 4 = 20.', '7 + 5 = 12, kemudian 12 × 2 = 24, kemudian 24 − 4 = 20.'), 'tw9a'),
         steps([step(T('Machine A multiplies by 4. Put in 6. What comes out?', 'Mesin A mendarab dengan 4. Masukkan 6. Apa yang keluar?'), 24, '6*4'),
                step(T('Machine B adds 16. What comes out?', 'Mesin B menambah 16. Apa yang keluar?'), 40, '24+16'),
                step(T('Machine C halves. What comes out now?', 'Mesin C membahagi dua. Apa yang keluar sekarang?'), 20, '40/2')],
               T('Do the machines one at a time.', 'Lakukan mesin satu demi satu.'), T('6 × 4 = 24, then 24 + 16 = 40, then 40 ÷ 2 = 20.', '6 × 4 = 24, kemudian 24 + 16 = 40, kemudian 40 ÷ 2 = 20.'), 'tw9b'),
         steps([step(T('Machine A subtracts 8. Put in 50. What comes out?', 'Mesin A menolak 8. Masukkan 50. Apa yang keluar?'), 42, '50-8'),
                step(T('Machine B divides by 6. What comes out?', 'Mesin B membahagi dengan 6. Apa yang keluar?'), 7, '42/6'),
                step(T('Machine C multiplies by 9. What comes out now?', 'Mesin C mendarab dengan 9. Apa yang keluar sekarang?'), 63, '7*9')],
               T('Do the machines one at a time.', 'Lakukan mesin satu demi satu.'), T('50 − 8 = 42, then 42 ÷ 6 = 7, then 7 × 9 = 63.', '50 − 8 = 42, kemudian 42 ÷ 6 = 7, kemudian 7 × 9 = 63.'), 'tw9c')])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Toy Workshop Finale', 'Kemuncak Bengkel Mainan'),
        T('The toy workshop must finish every order before the party! Solve the three steps.', 'Bengkel mainan mesti menyiapkan setiap tempahan sebelum majlis! Selesaikan tiga langkah itu.'),
        T('Multi-step problems with toys, boxes and money.', 'Masalah berbilang langkah dengan mainan, kotak dan wang.'),
        'Partyhat', T('Partyhat wears a paper hat all year.', 'Partyhat memakai topi kertas sepanjang tahun.'),
        [steps([step(T('The workshop makes 15 toys an hour. How many toys in 6 hours?', 'Bengkel membuat 15 mainan sejam. Berapa mainan dalam 6 jam?'), 90, '15*6'),
                step(T('The toys go into boxes of 10. How many boxes are filled?', 'Mainan dimasukkan ke dalam kotak berisi 10. Berapa kotak yang penuh?'), 9, '90/10'),
                step(T('Each box costs RM4 to ship. How much is that in total?', 'Setiap kotak menelan belanja RM4 untuk dihantar. Berapa jumlahnya?'), 36, '9*4', RM)],
               T('Multiply, then share, then multiply.', 'Darab, kemudian bahagi, kemudian darab.'), T('15 × 6 = 90, then 90 ÷ 10 = 9, then 9 × 4 = RM36.', '15 × 6 = 90, kemudian 90 ÷ 10 = 9, kemudian 9 × 4 = RM36.'), 'tw10a'),
         steps([step(T('A robot kit has 24 parts. How many parts in 5 kits?', 'Satu set robot mempunyai 24 bahagian. Berapa bahagian dalam 5 set?'), 120, '5*24'),
                step(T('12 parts are broken. How many good parts are left?', '12 bahagian rosak. Berapa bahagian baik yang tinggal?'), 108, '120-12'),
                step(T('Good parts are shared equally between 9 workers. How many parts each?', 'Bahagian yang baik dikongsi sama banyak antara 9 pekerja. Berapa bahagian setiap orang?'), 12, '108/9')],
               T('Take away the broken parts before sharing.', 'Tolak bahagian yang rosak sebelum berkongsi.'), T('5 × 24 = 120, then 120 − 12 = 108, then 108 ÷ 9 = 12.', '5 × 24 = 120, kemudian 120 − 12 = 108, kemudian 108 ÷ 9 = 12.'), 'tw10b'),
         steps([step(T('A teddy costs RM18. What do 7 teddies cost?', 'Seekor teddy berharga RM18. Berapa harga 7 ekor teddy?'), 126, '7*18', RM),
                step(T('A discount takes RM26 off. How much do you pay?', 'Diskaun memotong RM26. Berapa yang anda bayar?'), 100, '126-26', RM),
                step(T('You pay with RM150. How much change do you get?', 'Anda membayar dengan RM150. Berapa baki yang anda terima?'), 50, '150-100', RM)],
               T('Take the discount off first.', 'Tolak diskaun dahulu.'), T('7 × 18 = 126, then 126 − 26 = 100, then 150 − 100 = 50.', '7 × 18 = 126, kemudian 126 − 26 = 100, kemudian 150 − 100 = 50.'), 'tw10c')])
    return L
