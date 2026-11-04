from lib import *
CODE, BASE = 'mf', 32

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'operations', 'times-tables', 'adventurer', 'gears',
        T('Gear Pairs', 'Pasangan Gerigi'),
        T('The giant machine needs gears that fit together. Find the pair that multiplies to the number on the plate!', 'Mesin gergasi memerlukan gerigi yang sepadan. Cari pasangan yang hasil darabnya sama dengan nombor pada plat!'),
        T('Practise multiplication facts up to 12 × 12.', 'Berlatih fakta darab sehingga 12 × 12.'),
        'Cogsy', T('Cogsy ticks happily when two gears mesh.', 'Cogsy berbunyi gembira apabila dua gerigi bertaut.'),
        [tiles(24, [3, 8, 5, 6, 2, 9]), tiles(63, [7, 9, 6, 8, 5, 4]), tiles(132, [11, 12, 9, 8, 13, 10])])
    add(2, 'operations', 'arrays', 'adventurer', 'door',
        T('Array Yard', 'Laman Tatasusunan'),
        T('The yard is full of crates stacked in rows and columns. Count them the clever way!', 'Laman itu penuh dengan peti yang disusun dalam baris dan lajur. Kira dengan cara yang bijak!'),
        T('Multiply rows by columns to count an array.', 'Mendarab baris dengan lajur untuk mengira tatasusunan.'),
        'Stacky', T('Stacky builds towers of perfect rows.', 'Stacky membina menara dengan baris yang sempurna.'),
        [match([('3 × 4', '12'), ('2 × 5', '10'), ('3 × 3', '9')], T('Each question is rows × columns. Tap a question, then its answer.', 'Setiap soalan ialah baris × lajur. Ketik satu soalan, kemudian jawapannya.')),
         match([('6 × 4', '24'), ('5 × 7', '35'), ('9 × 2', '18'), ('4 × 8', '32')], T('Each question is rows × columns. Tap a question, then its answer.', 'Setiap soalan ialah baris × lajur. Ketik satu soalan, kemudian jawapannya.')),
         match([('7 × 8', '56'), ('9 × 6', '54'), ('12 × 5', '60'), ('11 × 4', '44'), ('8 × 8', '64')], T('Each question is rows × columns. Tap a question, then its answer.', 'Setiap soalan ialah baris × lajur. Ketik satu soalan, kemudian jawapannya.'))])
    add(3, 'operations', 'times-tables', 'adventurer', 'ferry',
        T('Splitter Station', 'Stesen Pembahagi'),
        T('Boxes arrive on the belt and must be split into equal piles. Match each division to its answer!', 'Kotak tiba di tali sawat dan mesti dibahagi kepada longgokan yang sama banyak. Padankan setiap pembahagian dengan jawapannya!'),
        T('Use multiplication facts to divide.', 'Menggunakan fakta darab untuk membahagi.'),
        'Splitz', T('Splitz cuts everything into equal pieces.', 'Splitz memotong segalanya kepada kepingan yang sama.'),
        [match([('12 ÷ 3', '4'), ('20 ÷ 4', '5'), ('18 ÷ 2', '9')], T('Tap a division, then tap its answer.', 'Ketik satu pembahagian, kemudian ketik jawapannya.'), T('Think: what times the small number makes the big number?', 'Fikirkan: berapa kali nombor kecil menjadi nombor besar?')),
         match([('24 ÷ 6', '4'), ('35 ÷ 7', '5'), ('48 ÷ 8', '6'), ('63 ÷ 9', '7')], T('Tap a division, then tap its answer.', 'Ketik satu pembahagian, kemudian ketik jawapannya.'), T('Think: what times the small number makes the big number?', 'Fikirkan: berapa kali nombor kecil menjadi nombor besar?')),
         match([('72 ÷ 8', '9'), ('96 ÷ 12', '8'), ('84 ÷ 7', '12'), ('121 ÷ 11', '11'), ('130 ÷ 13', '10')], T('Tap a division, then tap its answer.', 'Ketik satu pembahagian, kemudian ketik jawapannya.'), T('Think: what times the small number makes the big number?', 'Fikirkan: berapa kali nombor kecil menjadi nombor besar?'))])
    add(4, 'number-sense', 'multiples', 'adventurer', 'lanterns',
        T('Multiple Machine', 'Mesin Gandaan'),
        T('This machine only lights up on multiples. Keep the pattern going!', 'Mesin ini hanya menyala pada gandaan. Teruskan pola itu!'),
        T('Continue patterns of multiples.', 'Menyambung pola gandaan.'),
        'Multi', T('Multi hums a tune in steps of seven.', 'Multi menyanyi lagu dalam langkah tujuh.'),
        [pattern('arith', 7, 7, 5, seed='mf4a'), pattern('arith', 9, 9, 6, seed='mf4b'), pattern('arith', 12, 12, 6, hidden=3, seed='mf4c')])
    add(5, 'number-sense', 'factors', 'adventurer', 'gate',
        T('Factor Furnace', 'Relau Faktor'),
        T('The furnace door has a number lock. Find the missing factor to open it!', 'Pintu relau mempunyai kunci nombor. Cari faktor yang hilang untuk membukanya!'),
        T('Find missing factors.', 'Mencari faktor yang hilang.'),
        'Embera', T('Embera keeps the furnace warm.', 'Embera memastikan relau sentiasa hangat.'),
        [match([('? × 4 = 28', '7'), ('3 × ? = 18', '6'), ('? × 5 = 45', '9')], T('Tap an equation, then tap the missing number.', 'Ketik satu persamaan, kemudian ketik nombor yang hilang.'), T('Divide the answer by the factor you already know.', 'Bahagikan jawapan dengan faktor yang anda sudah tahu.')),
         match([('? × 6 = 54', '9'), ('8 × ? = 64', '8'), ('? × 7 = 56', '7'), ('5 × ? = 60', '12')], T('Tap an equation, then tap the missing number.', 'Ketik satu persamaan, kemudian ketik nombor yang hilang.')),
         match([('? × 12 = 96', '8'), ('9 × ? = 108', '12'), ('? × 11 = 143', '13'), ('14 × ? = 98', '7'), ('? × 15 = 90', '6')], T('Tap an equation, then tap the missing number.', 'Ketik satu persamaan, kemudian ketik nombor yang hilang.'), T('Divide the answer by the factor you already know.', 'Bahagikan jawapan dengan faktor yang anda sudah tahu.'))])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Fair Fuel', 'Bahan Api Adil'),
        T('Share the fuel berries between the machines so every one gets the same!', 'Kongsi beri bahan api antara mesin supaya setiap satu mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Fuely', T('Fuely loves a fair share of berries.', 'Fuely suka mendapat bahagian beri yang adil.'),
        [share(12, 3), share(20, 4), share(30, 5)])
    add(7, 'number-sense', 'multiply-10', 'master', 'tank',
        T('Power of Ten', 'Kuasa Sepuluh'),
        T('The big pistons multiply by 10 and 100. Match each machine to its output!', 'Omboh besar mendarab dengan 10 dan 100. Padankan setiap mesin dengan hasilnya!'),
        T('Multiply by 10, 100 and 1,000.', 'Mendarab dengan 10, 100 dan 1,000.'),
        'Pistie', T('Pistie pumps up and down all day.', 'Pistie mengepam naik turun sepanjang hari.'),
        [match([('4 × 10', '40'), ('7 × 10', '70'), ('25 × 10', '250')], T('Tap a question, then tap its answer.', 'Ketik satu soalan, kemudian ketik jawapannya.'), T('Multiplying by 10 moves every digit one place to the left.', 'Mendarab dengan 10 menggerakkan setiap digit satu tempat ke kiri.')),
         match([('36 × 10', '360'), ('8 × 100', '800'), ('45 × 100', '4500'), ('12 × 10', '120')], T('Tap a question, then tap its answer.', 'Ketik satu soalan, kemudian ketik jawapannya.'), T('Multiplying by 100 moves every digit two places to the left.', 'Mendarab dengan 100 menggerakkan setiap digit dua tempat ke kiri.')),
         match([('250 × 10', '2500'), ('34 × 100', '3400'), ('9 × 1000', '9000'), ('120 × 100', '12000'), ('7 × 100', '700')], T('Tap a question, then tap its answer.', 'Ketik satu soalan, kemudian ketik jawapannya.'), T('Count the zeros you are multiplying by and add them to the end.', 'Kira bilangan sifar yang anda darabkan dan tambahkannya di hujung.'))])
    add(8, 'operations', 'money', 'master', 'chest',
        T('Cog Coins', 'Syiling Gerigi'),
        T('The cog shop only takes exact change. Pay with the coins in your pocket!', 'Kedai gerigi hanya menerima wang tepat. Bayar dengan syiling dalam poket anda!'),
        T('Make amounts of money with coins and notes.', 'Membentuk jumlah wang dengan syiling dan wang kertas.'),
        'Coiny', T('Coiny jingles when it walks.', 'Coiny berdenting apabila berjalan.'),
        [coins(135, [5, 10, 20, 50, 100]), coins(350, [10, 20, 50, 100], 5), coins(495, [5, 10, 20, 50, 100], 8)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Output Chart', 'Carta Hasil'),
        T('The factory counted what each machine made today. Read the bars to find the answer!', 'Kilang mengira apa yang dihasilkan setiap mesin hari ini. Baca palang untuk mencari jawapannya!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Tally-Bot', T('Tally-Bot counts every bolt twice.', 'Tally-Bot mengira setiap bolt dua kali.'),
        [chart([(T('Cogs', 'Gerigi'), 12, 'coral'), (T('Bolts', 'Bolt'), 8, 'sky'), (T('Springs', 'Spring'), 5, 'mint')], ('diff', 0, 2), T('parts', 'alat ganti')),
         chart([(T('Cogs', 'Gerigi'), 30, 'coral'), (T('Bolts', 'Bolt'), 45, 'sky'), (T('Springs', 'Spring'), 25, 'mint'), (T('Pipes', 'Paip'), 40, 'sun')], ('sum', [0, 1, 2, 3]), T('parts', 'alat ganti')),
         chart([(T('Cogs', 'Gerigi'), 48, 'coral'), (T('Bolts', 'Bolt'), 36, 'sky'), (T('Springs', 'Spring'), 60, 'mint'), (T('Pipes', 'Paip'), 52, 'sun'), (T('Gears', 'Roda gigi'), 44, 'grape')], ('mean',), T('parts', 'alat ganti'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Forest Finale', 'Kemuncak Hutan'),
        T('Start the great Mechanical Forest! Three steps to bring every machine to life.', 'Hidupkan Hutan Mekanikal yang hebat! Tiga langkah untuk menghidupkan setiap mesin.'),
        T('Multi-step problems with multiplication and division.', 'Masalah berbilang langkah dengan pendaraban dan pembahagian.'),
        'Whirrly', T('Whirrly spins faster with every machine you wake.', 'Whirrly berpusing lebih laju dengan setiap mesin yang anda hidupkan.'),
        [steps([step(T('A machine makes 6 cogs every minute. How many cogs in 7 minutes?', 'Sebuah mesin menghasilkan 6 gerigi setiap minit. Berapa gerigi dalam 7 minit?'), 42, '6*7'),
                step(T('9 cogs are faulty. How many good cogs are left?', '9 gerigi rosak. Berapa gerigi yang baik masih ada?'), 33, '42-9'),
                step(T('Pack the good cogs equally into 3 boxes. How many in each box?', 'Pek gerigi yang baik sama banyak ke dalam 3 kotak. Berapa dalam setiap kotak?'), 11, '33/3')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('6 × 7 = 42, then 42 − 9 = 33, then 33 ÷ 3 = 11.', '6 × 7 = 42, kemudian 42 − 9 = 33, kemudian 33 ÷ 3 = 11.'), 'mf10a'),
         steps([step(T('There are 8 rows of 12 trees. How many trees?', 'Terdapat 8 baris dengan 12 pokok. Berapa pokok?'), 96, '8*12'),
                step(T('A third of the trees need new gears. How many trees is that?', 'Satu pertiga pokok memerlukan gerigi baharu. Berapa pokok itu?'), 32, '96/3'),
                step(T('Each tree needs 4 gears. How many gears are needed?', 'Setiap pokok memerlukan 4 gerigi. Berapa gerigi diperlukan?'), 128, '32*4')],
               T('Multiply first, then find a third.', 'Darab dahulu, kemudian cari satu pertiga.'), T('8 × 12 = 96, then 96 ÷ 3 = 32, then 32 × 4 = 128.', '8 × 12 = 96, kemudian 96 ÷ 3 = 32, kemudian 32 × 4 = 128.'), 'mf10b'),
         steps([step(T('A factory has 15 machines. Each makes 24 cogs a day. How many cogs a day?', 'Sebuah kilang mempunyai 15 mesin. Setiap mesin menghasilkan 24 gerigi sehari. Berapa gerigi sehari?'), 360, '15*24'),
                step(T('In 5 days the factory makes how many cogs?', 'Dalam 5 hari kilang itu menghasilkan berapa gerigi?'), 1800, '360*5'),
                step(T('The cogs are packed in boxes of 12. How many boxes are needed?', 'Gerigi itu dipek dalam kotak yang masing-masing mengandungi 12. Berapa kotak diperlukan?'), 150, '1800/12')],
               T('Multiply, multiply again, then divide.', 'Darab, darab lagi, kemudian bahagi.'), T('15 × 24 = 360, then 360 × 5 = 1,800, then 1,800 ÷ 12 = 150.', '15 × 24 = 360, kemudian 360 × 5 = 1,800, kemudian 1,800 ÷ 12 = 150.'), 'mf10c')])
    return L
