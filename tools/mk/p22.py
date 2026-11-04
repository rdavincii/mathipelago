from lib import *
CODE, BASE = 'nm', 222
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'operations', 'money', 'adventurer', 'chest',
        T('Satay Prices', 'Harga Satay'),
        T('The satay man needs exact change! Pay for each order with exactly the right coins.', 'Abang satay memerlukan duit tepat! Bayar setiap pesanan dengan syiling yang tepat.'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Satay', T('Satay smells so good that crowds follow him.', 'Satay berbau sangat sedap sehingga orang ramai mengikutinya.'),
        [coins(90, [5, 10, 20, 50]), coins(165, [5, 10, 20, 50, 100]), coins(355, [5, 10, 20, 50, 100], 6)])
    add(2, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('Market Street', 'Jalan Pasar'),
        T('The night market street has numbered stalls. Slide the lantern to the right stall!', 'Jalan pasar malam mempunyai gerai bernombor. Gelongsorkan tanglung ke gerai yang betul!'),
        T('Place numbers on a line and find the middle.', 'Meletakkan nombor pada garis dan mencari titik tengah.'),
        'Stall', T('Stall knows every stall by number.', 'Stall mengenali setiap gerai mengikut nombor.'),
        [numberline(250, 0, 500, 50, 100), numberline(60, 0, 120, 10, 20), numberline(35, 0, 100, 5, 25, kind='half', a=10, b=60)])
    add(3, 'operations', 'money', 'adventurer', 'ferry',
        T('Change at the Stall', 'Baki di Gerai'),
        T('Customers pay with big notes and wait for their change. Work out each step carefully!', 'Pelanggan membayar dengan wang kertas besar dan menunggu baki. Kira setiap langkah dengan teliti!'),
        T('Total costs and give change.', 'Mengira jumlah harga dan memberi baki.'),
        'Change', T('Change counts every coin twice.', 'Change mengira setiap syiling dua kali.'),
        [steps([step(T('Ali buys 3 satay sets at RM6 each. What is the total?', 'Ali membeli 3 set satay pada harga RM6 setiap satu. Berapa jumlahnya?'), 18, '3*6', RM),
                step(T('He also buys a cendol for RM4. What is the new total?', 'Dia juga membeli sebuah cendol berharga RM4. Berapa jumlah baharu?'), 22, '18+4', RM),
                step(T('He pays with RM50. How much change does he get?', 'Dia membayar dengan RM50. Berapa baki yang diterimanya?'), 28, '50-22', RM)],
               T('Multiply, then add, then subtract.', 'Darab, kemudian tambah, kemudian tolak.'), T('3 × 6 = 18, then 18 + 4 = 22, then 50 − 22 = 28.', '3 × 6 = 18, kemudian 18 + 4 = 22, kemudian 50 − 22 = 28.'), 'nm3a'),
         steps([step(T('A lantern costs RM7. What do 4 lanterns cost?', 'Sebuah tanglung berharga RM7. Berapa harga 4 tanglung?'), 28, '4*7', RM),
                step(T('The seller gives a discount of RM3. How much do you pay?', 'Penjual memberi diskaun RM3. Berapa yang anda bayar?'), 25, '28-3', RM),
                step(T('You pay with RM30. How much change do you get?', 'Anda membayar dengan RM30. Berapa baki yang anda terima?'), 5, '30-25', RM)],
               T('Take the discount off before you work out the change.', 'Tolak diskaun sebelum mengira baki.'), T('4 × 7 = 28, then 28 − 3 = 25, then 30 − 25 = 5.', '4 × 7 = 28, kemudian 28 − 3 = 25, kemudian 30 − 25 = 5.'), 'nm3b'),
         steps([step(T('A pack of kuih costs RM9. What do 5 packs cost?', 'Sepek kuih berharga RM9. Berapa harga 5 pek?'), 45, '5*9', RM),
                step(T('3 friends share the cost equally. How much does each friend pay?', '3 orang kawan berkongsi harga itu sama banyak. Berapa yang dibayar oleh setiap kawan?'), 15, '45/3', RM),
                step(T('Each friend has RM20. How much money is left for each friend?', 'Setiap kawan mempunyai RM20. Berapa wang yang tinggal untuk setiap kawan?'), 5, '20-15', RM)],
               T('Find the total, then share it.', 'Cari jumlah, kemudian kongsinya.'), T('5 × 9 = 45, then 45 ÷ 3 = 15, then 20 − 15 = 5.', '5 × 9 = 45, kemudian 45 ÷ 3 = 15, kemudian 20 − 15 = 5.'), 'nm3c')])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Lantern Rows', 'Barisan Tanglung'),
        T('Lanterns hang in rows that follow a pattern. How many lanterns are in the next row?', 'Tanglung digantung dalam barisan yang mengikut pola. Berapa tanglung dalam barisan seterusnya?'),
        T('Continue counting and doubling patterns.', 'Menyambung pola pengiraan dan penggandaan.'),
        'Glow', T('Glow lights up the whole street.', 'Glow menerangi seluruh jalan.'),
        [pattern('arith', 4, 4, 5, seed='nm4a'), pattern('geo', 1, 2, 6, hidden=4, seed='nm4b'), pattern('arith', 90, -15, 6, hidden=2, seed='nm4c')])
    add(5, 'operations', 'ratio', 'adventurer', 'door',
        T('Price Per Piece', 'Harga Sekeping'),
        T('Stalls sell in bundles. Match each bundle price to the price of one!', 'Gerai menjual secara bungkusan. Padankan harga bungkusan dengan harga satu!'),
        T('Find the price of one from a bundle.', 'Mencari harga satu daripada bungkusan.'),
        'Unit', T('Unit loves to split a bundle into ones.', 'Unit suka memecahkan bungkusan kepada satu-satu.'),
        [match([('3 satay = RM6', 'RM2 each'), ('4 cendol = RM12', 'RM3 each'), ('5 kuih = RM20', 'RM4 each')], MP_, T('Divide the price by the number of pieces.', 'Bahagikan harga dengan bilangan keping.')),
         match([('3 satay = RM6', 'RM2 each'), ('4 cendol = RM12', 'RM3 each'), ('5 kuih = RM20', 'RM4 each'), ('6 buns = RM9', 'RM1.50 each')], MP_, T('Divide the price by the number of pieces.', 'Bahagikan harga dengan bilangan keping.')),
         match([('10 sticks = RM8', '80 sen each'), ('4 apam balik = RM10', 'RM2.50 each'), ('5 drinks = RM15', 'RM3 each'), ('6 skewers = RM9', 'RM1.50 each'), ('8 kuih = RM16', 'RM2 each')], MP_, T('Divide the price by the number of pieces.', 'Bahagikan harga dengan bilangan keping.'))])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Snack Share', 'Kongsi Snek'),
        T('Share the snacks between the friends. Everyone must get the same!', 'Kongsi snek antara kawan-kawan. Semua orang mesti mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Nibble', T('Nibble always asks for one more bite.', 'Nibble sentiasa meminta satu gigitan lagi.'),
        [share(18, 3), share(24, 4), share(30, 5)])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Crowd Counts', 'Kiraan Orang Ramai'),
        T('The crowd lines up in equal rows. Find the two tiles that make each total!', 'Orang ramai beratur dalam barisan yang sama panjang. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Crowd', T('Crowd is never lonely.', 'Crowd tidak pernah kesunyian.'),
        [tiles(36, [4, 9, 6, 3, 12, 5]), tiles(72, [8, 9, 6, 12, 7, 5]), tiles(120, [10, 12, 8, 15, 6, 20])])
    add(8, 'number-sense', 'addition', 'master', 'scale',
        T('Pay by the Sen', 'Bayar dengan Sen'),
        T('The cashier weighs coins on a scale. Pick the coins in sen that make the total!', 'Juruwang menimbang syiling pada penimbang. Pilih syiling dalam sen yang jumlahnya sama!'),
        T('Add amounts of money in sen.', 'Menambah jumlah wang dalam sen.'),
        'Cashy', T('Cashy keeps the till tidy.', 'Cashy menyimpan laci wang dengan kemas.'),
        [balance(300, [100, 200, 150, 50, 250]), balance(550, [250, 300, 200, 400, 150]), balance(1000, [400, 350, 250, 500, 300, 200], 3)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Stall Chart', 'Carta Gerai'),
        T('The market boss charted how many plates each stall sold. Read the chart!', 'Bos pasar menyusun carta berapa pinggan dijual oleh setiap gerai. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Plates', T('Plates stacks everything very high.', 'Plates menyusun segalanya sangat tinggi.'),
        [chart([(T('Satay', 'Satay'), 40, 'coral'), (T('Cendol', 'Cendol'), 25, 'mint'), (T('Apam', 'Apam'), 35, 'sun')], ('diff', 0, 1), T('plates', 'pinggan')),
         chart([(T('Satay', 'Satay'), 40, 'coral'), (T('Cendol', 'Cendol'), 25, 'mint'), (T('Apam', 'Apam'), 35, 'sun'), (T('Kuih', 'Kuih'), 20, 'grape')], ('sum', [0, 1, 2, 3]), T('plates', 'pinggan')),
         chart([(T('Satay', 'Satay'), 24, 'coral'), (T('Cendol', 'Cendol'), 36, 'mint'), (T('Apam', 'Apam'), 18, 'sun'), (T('Kuih', 'Kuih'), 42, 'grape'), (T('Rojak', 'Rojak'), 30, 'sky')], ('mean',), T('plates', 'pinggan'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Night Market Finale', 'Kemuncak Pasar Malam'),
        T('The night market closes with a big crowd! Solve three steps to count the takings.', 'Pasar malam ditutup dengan orang ramai! Selesaikan tiga langkah untuk mengira kutipan.'),
        T('Multi-step problems with money, prices and profit.', 'Masalah berbilang langkah dengan wang, harga dan untung.'),
        'Lampu', T('Lampu glows brightest at the end of the night.', 'Lampu bersinar paling terang pada penghujung malam.'),
        [steps([step(T('Satay costs 80 sen a stick. How many sen do 15 sticks cost?', 'Satay berharga 80 sen sebatang. Berapa sen harga 15 batang?'), 1200, '15*80', lambda v: f'{v} sen'),
                step(T('How many ringgit is that? (100 sen = RM1)', 'Berapa ringgit itu? (100 sen = RM1)'), 12, '1200/100', RM),
                step(T('You pay with RM20. How much change do you get?', 'Anda membayar dengan RM20. Berapa baki yang anda terima?'), 8, '20-12', RM)],
               T('Multiply to get sen, then change to ringgit.', 'Darab untuk mendapat sen, kemudian tukar kepada ringgit.'), T('15 × 80 = 1200 sen, then 1200 ÷ 100 = RM12, then 20 − 12 = 8.', '15 × 80 = 1200 sen, kemudian 1200 ÷ 100 = RM12, kemudian 20 − 12 = 8.'), 'nm10a'),
         steps([step(T('A cendol costs RM4. What do 7 cendols cost?', 'Sebuah cendol berharga RM4. Berapa harga 7 cendol?'), 28, '7*4', RM),
                step(T('Add 5 apam balik at RM3 each. What is the new total?', 'Tambah 5 apam balik pada harga RM3 setiap satu. Berapa jumlah baharu?'), 43, '28+5*3', RM),
                step(T('You pay with RM50. How much change do you get?', 'Anda membayar dengan RM50. Berapa baki yang anda terima?'), 7, '50-43', RM)],
               T('Work out each food, then add.', 'Kira setiap makanan, kemudian tambah.'), T('7 × 4 = 28, then 28 + 5 × 3 = 43, then 50 − 43 = 7.', '7 × 4 = 28, kemudian 28 + 5 × 3 = 43, kemudian 50 − 43 = 7.'), 'nm10b'),
         steps([step(T('A stall sells 3 satay for RM5. How many groups of 3 are in 12 satay?', 'Sebuah gerai menjual 3 satay dengan harga RM5. Berapa kumpulan 3 dalam 12 satay?'), 4, '12/3'),
                step(T('What do those groups cost altogether?', 'Berapa harga semua kumpulan itu?'), 20, '4*5', RM),
                step(T('It cost the stall RM12 to make them. How much profit is that?', 'Kos gerai untuk membuatnya ialah RM12. Berapakah untungnya?'), 8, '20-12', RM)],
               T('Find the groups first, then the money.', 'Cari kumpulan dahulu, kemudian wang.'), T('12 ÷ 3 = 4, then 4 × 5 = 20, then 20 − 12 = 8.', '12 ÷ 3 = 4, kemudian 4 × 5 = 20, kemudian 20 − 12 = 8.'), 'nm10c')])
    return L
