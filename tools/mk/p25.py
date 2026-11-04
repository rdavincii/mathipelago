from lib import *
CODE, BASE = 'bk', 252
MT = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'fractions', 'adventurer', 'door',
        T('Twin Trays', 'Dulang Kembar'),
        T('Every tray in the bakery has a twin that looks different but holds the same amount. Pair them up!', 'Setiap dulang di kedai roti mempunyai kembar yang kelihatan berbeza tetapi sama banyak. Padankan mereka!'),
        T('Match equivalent fractions.', 'Memadankan pecahan setara.'),
        'Crumb', T('Crumb always sits next to its twin.', 'Crumb sentiasa duduk di sebelah kembarnya.'),
        [match([('1/2', '3/6'), ('1/5', '2/10'), ('3/4', '9/12')], MT, T('Multiply the top and the bottom by the same number.', 'Darabkan atas dan bawah dengan nombor yang sama.')),
         match([('2/5', '4/10'), ('1/6', '2/12'), ('2/3', '8/12'), ('1/4', '5/20')], MT, T('Multiply the top and the bottom by the same number.', 'Darabkan atas dan bawah dengan nombor yang sama.')),
         match([('6/9', '2/3'), ('8/12', '4/6'), ('5/15', '1/3'), ('12/16', '3/4'), ('6/10', '3/5')], MT, T('Divide the top and the bottom by the same number to make it simpler.', 'Bahagikan atas dan bawah dengan nombor yang sama untuk memudahkannya.'))])
    add(2, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Tray of Buns', 'Dulang Roti Bun'),
        T('Fill each tray with the right fraction of dough before it goes into the oven!', 'Isi setiap dulang dengan pecahan doh yang betul sebelum masuk ke dalam ketuhar!'),
        T('Fractions of a tray.', 'Pecahan sebuah dulang.'),
        'Dough', T('Dough is soft, round and a little bit sticky.', 'Dough lembut, bulat dan sedikit melekit.'),
        [tank(8, 1, 2), tank(12, 3, 4), tank(10, 7, 10)])
    add(3, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Bun Share', 'Kongsi Roti Bun'),
        T('Fresh buns must be shared between the hungry customers. Everybody gets the same!', 'Roti bun yang segar mesti dikongsi antara pelanggan yang lapar. Semua orang mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Bunny', T('Bunny always saves the warmest bun.', 'Bunny sentiasa menyimpan roti bun yang paling hangat.'),
        [share(12, 3), share(20, 4), share(25, 5)])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Oven Pattern', 'Pola Ketuhar'),
        T('The oven bakes more every hour in a pattern. How many come next?', 'Ketuhar membakar lebih banyak setiap jam mengikut pola. Berapa banyak yang seterusnya?'),
        T('Continue number patterns that grow.', 'Menyambung pola nombor yang bertambah.'),
        'Whisk', T('Whisk spins faster when the oven is full.', 'Whisk berputar lebih laju apabila ketuhar penuh.'),
        [pattern('arith', 6, 6, 5, seed='bk4a'), pattern('arith', 12, 12, 5, seed='bk4b'), pattern('geo', 3, 2, 6, hidden=4, seed='bk4c')])
    add(5, 'operations', 'ratio', 'adventurer', 'scale',
        T('Recipe Ratios', 'Nisbah Resipi'),
        T('Every recipe needs ingredients in the right ratio. Work out how much of everything is needed!', 'Setiap resipi memerlukan bahan dalam nisbah yang betul. Kira berapa banyak setiap bahan diperlukan!'),
        T('Use a ratio to find amounts of ingredients.', 'Menggunakan nisbah untuk mencari jumlah bahan.'),
        'Ratio Roo', T('Roo measures twice and bakes once.', 'Roo menyukat dua kali dan membakar sekali.'),
        [steps([step(T('A cake uses 2 cups of flour for every 1 cup of sugar. How many cups of flour for 3 cups of sugar?', 'Sebiji kek menggunakan 2 cawan tepung untuk setiap 1 cawan gula. Berapa cawan tepung untuk 3 cawan gula?'), 6, '3*2'),
                step(T('How many cups of flour and sugar are there altogether?', 'Berapa cawan tepung dan gula kesemuanya?'), 9, '6+3'),
                step(T('The mix is shared equally between 3 tins. How many cups in each tin?', 'Adunan itu dikongsi sama banyak antara 3 tin. Berapa cawan dalam setiap tin?'), 3, '9/3')],
               T('For every 1 cup of sugar there are 2 cups of flour.', 'Untuk setiap 1 cawan gula ada 2 cawan tepung.'), T('3 × 2 = 6, then 6 + 3 = 9, then 9 ÷ 3 = 3.', '3 × 2 = 6, kemudian 6 + 3 = 9, kemudian 9 ÷ 3 = 3.'), 'bk5a'),
         steps([step(T('Each batch needs 3 eggs. How many eggs for 4 batches?', 'Setiap kelompok memerlukan 3 biji telur. Berapa biji telur untuk 4 kelompok?'), 12, '4*3'),
                step(T('6 eggs are used up by lunchtime. How many eggs are left?', '6 biji telur habis digunakan pada waktu makan tengah hari. Berapa biji telur yang tinggal?'), 6, '12-6'),
                step(T('The rest are shared equally between 3 bakers. How many eggs does each baker get?', 'Bakinya dikongsi sama banyak antara 3 orang tukang roti. Berapa biji telur yang diperoleh setiap orang?'), 2, '6/3')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('4 × 3 = 12, then 12 − 6 = 6, then 6 ÷ 3 = 2.', '4 × 3 = 12, kemudian 12 − 6 = 6, kemudian 6 ÷ 3 = 2.'), 'bk5b'),
         steps([step(T('The butter to flour ratio is 1 to 4. How many cups of flour for 5 cups of butter?', 'Nisbah mentega kepada tepung ialah 1 kepada 4. Berapa cawan tepung untuk 5 cawan mentega?'), 20, '5*4'),
                step(T('How many cups of butter and flour are there altogether?', 'Berapa cawan mentega dan tepung kesemuanya?'), 25, '20+5'),
                step(T('Each loaf needs 5 cups of the mix. How many loaves can be made?', 'Setiap roti memerlukan 5 cawan adunan. Berapa buku roti yang boleh dibuat?'), 5, '25/5')],
               T('Flour is 4 times the butter.', 'Tepung ialah 4 kali mentega.'), T('5 × 4 = 20, then 20 + 5 = 25, then 25 ÷ 5 = 5.', '5 × 4 = 20, kemudian 20 + 5 = 25, kemudian 25 ÷ 5 = 5.'), 'bk5c')])
    add(6, 'operations', 'money', 'adventurer', 'chest',
        T('Bakery Till', 'Mesin Tunai Kedai Roti'),
        T('Customers pay for their bread. Pay each price with exactly the right coins!', 'Pelanggan membayar untuk roti mereka. Bayar setiap harga dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Penny Pie', T('Penny Pie keeps every coin shiny.', 'Penny Pie memastikan setiap syiling berkilat.'),
        [coins(65, [5, 10, 20, 50]), coins(180, [10, 20, 50, 100]), coins(335, [5, 10, 20, 50, 100], 7)])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Dozens of Rolls', 'Berdozen Roti Gulung'),
        T('Rolls are baked in equal rows. Find the two tiles that make each total!', 'Roti gulung dibakar dalam baris yang sama banyak. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Rollo', T('Rollo rolls down every hill.', 'Rollo bergolek menuruni setiap bukit.'),
        [tiles(24, [3, 8, 4, 6, 2, 12]), tiles(36, [4, 9, 6, 12, 3, 5]), tiles(72, [8, 9, 6, 12, 7, 5])])
    add(8, 'shape-data', 'data', 'master', 'lighthouse',
        T('Bake Sale Chart', 'Carta Jualan Kuih'),
        T('The bakery counted what it sold today. Read the chart!', 'Kedai roti mengira apa yang dijual hari ini. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Sprinkle', T('Sprinkle adds a little extra to everything.', 'Sprinkle menambah sedikit lebih pada setiap benda.'),
        [chart([(T('Buns', 'Roti bun'), 24, 'coral'), (T('Cakes', 'Kek'), 15, 'sun'), (T('Tarts', 'Tart'), 18, 'mint')], ('diff', 0, 1), T('items', 'item')),
         chart([(T('Buns', 'Roti bun'), 20, 'coral'), (T('Cakes', 'Kek'), 35, 'sun'), (T('Tarts', 'Tart'), 15, 'mint'), (T('Pies', 'Pai'), 30, 'sky')], ('sum', [0, 1, 2, 3]), T('items', 'item')),
         chart([(T('Mon', 'Isnin'), 20, 'coral'), (T('Tue', 'Selasa'), 30, 'sun'), (T('Wed', 'Rabu'), 25, 'mint'), (T('Thu', 'Khamis'), 35, 'sky'), (T('Fri', 'Jumaat'), 40, 'grape')], ('mean',), T('items', 'item'))])
    add(9, 'number-sense', 'number-line', 'master', 'bridge',
        T('Baking Time Line', 'Garis Masa Membakar'),
        T('Slide the marker to the right place on the baking line!', 'Gelongsorkan penanda ke tempat yang betul pada garis membakar!'),
        T('Place numbers on a line, including the middle.', 'Meletakkan nombor pada garis, termasuk titik tengah.'),
        'Timer', T('Timer rings before anything burns.', 'Timer berbunyi sebelum apa-apa hangus.'),
        [numberline(250, 0, 500, 50, 100), numberline(75, 0, 100, 5, 25), numberline(60, 0, 120, 10, 30, kind='half', a=20, b=100)])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Grand Bake-Off', 'Pertandingan Membakar Besar'),
        T('It is the Grand Bake-Off! Solve three steps to crown the best baker in the bay.', 'Ini Pertandingan Membakar Besar! Selesaikan tiga langkah untuk menobatkan tukang roti terbaik di teluk.'),
        T('Multi-step problems with fractions and money.', 'Masalah berbilang langkah dengan pecahan dan wang.'),
        'Chef Bao', T('Chef Bao tastes everything twice.', 'Chef Bao merasa setiap benda dua kali.'),
        [steps([step(T('A bakery bakes 8 trays with 12 buns on each tray. How many buns?', 'Sebuah kedai roti membakar 8 dulang dengan 12 biji roti bun pada setiap dulang. Berapa biji roti bun?'), 96, '8*12'),
                step(T('A quarter of the buns are sold in the morning. How many buns is that?', 'Suku daripada roti bun dijual pada waktu pagi. Berapa biji itu?'), 24, '96/4'),
                step(T('Each bun sells for RM2. How much money is that?', 'Setiap roti bun dijual dengan harga RM2. Berapa wang itu?'), 48, '24*2', RM)],
               T('A quarter means divide by 4.', 'Suku bermaksud bahagi dengan 4.'), T('8 × 12 = 96, then 96 ÷ 4 = 24, then 24 × 2 = RM48.', '8 × 12 = 96, kemudian 96 ÷ 4 = 24, kemudian 24 × 2 = RM48.'), 'bk10a'),
         steps([step(T('A cake is cut into 12 slices. Three quarters are eaten. How many slices are eaten?', 'Sebiji kek dipotong kepada 12 keping. Tiga perempat dimakan. Berapa keping dimakan?'), 9, '12/4*3'),
                step(T('How many slices are left?', 'Berapa keping yang tinggal?'), 3, '12-9'),
                step(T('Each slice left sells for RM5. How much money is that?', 'Setiap keping yang tinggal dijual dengan harga RM5. Berapa wang itu?'), 15, '3*5', RM)],
               T('Find one quarter first, then take 3 of them.', 'Cari satu perempat dahulu, kemudian ambil 3 daripadanya.'), T('12 ÷ 4 × 3 = 9, then 12 − 9 = 3, then 3 × 5 = RM15.', '12 ÷ 4 × 3 = 9, kemudian 12 − 9 = 3, kemudian 3 × 5 = RM15.'), 'bk10b'),
         steps([step(T('Flour costs RM6 a bag. What do 5 bags cost?', 'Tepung berharga RM6 sebeg. Berapa harga 5 beg?'), 30, '5*6', RM),
                step(T('Sugar for the cake costs RM12. What is the total?', 'Gula untuk kek berharga RM12. Berapa jumlahnya?'), 42, '30+12', RM),
                step(T('You pay with RM50. How much change do you get?', 'Anda membayar dengan RM50. Berapa baki yang anda terima?'), 8, '50-42', RM)],
               T('Add the costs, then take them from RM50.', 'Tambah harga, kemudian tolak daripada RM50.'), T('5 × 6 = 30, then 30 + 12 = 42, then 50 − 42 = 8.', '5 × 6 = 30, kemudian 30 + 12 = 42, kemudian 50 − 42 = 8.'), 'bk10c')])
    return L
