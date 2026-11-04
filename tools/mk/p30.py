from lib import *
CODE, BASE = 'lf', 302
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'place-value', 'adventurer', 'lanterns',
        T('Lantern Numbers', 'Nombor Tanglung'),
        T('Each lantern shows a big number. Pick the digit that is worth the most!', 'Setiap tanglung menunjukkan nombor besar. Pilih digit yang paling tinggi nilainya!'),
        T('Place value up to thousands.', 'Nilai tempat hingga ribuan.'),
        'Lampu', T('Lampu glows brighter with every right answer.', 'Lampu bersinar lebih terang dengan setiap jawapan betul.'),
        [placevalue(3472, [1000,100,10,1]), placevalue(5806, [1000,100,10,1]), placevalue(9215, [1000,100,10,1])])
    add(2, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('String of Lanterns', 'Untaian Tanglung'),
        T('Hang each lantern at the right spot on the string!', 'Gantung setiap tanglung pada tempat yang betul di tali!'),
        T('Number line to 1000.', 'Garis nombor hingga 1000.'),
        'Dangle', T('Dangle swings from the string.', 'Dangle berayun dari tali.'),
        [numberline(250, 0, 500, 50, 100), numberline(600, 0, 1000, 100, 200), numberline(875, 0, 1000, 125, 250)])
    add(3, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Lantern Parade Pattern', 'Pola Perarakan Tanglung'),
        T('The parade lanterns follow a number pattern. What comes next?', 'Tanglung perarakan mengikut pola nombor. Apa yang seterusnya?'),
        T('Number patterns.', 'Pola nombor.'),
        'Parade', T('Parade never loses the beat.', 'Parade tidak pernah hilang rentak.'),
        [pattern('arith', 12, 8, 5, seed='lf3a'), pattern('arith', 100, 25, 5, seed='lf3b'), pattern('geo', 3, 2, 5, hidden=4, seed='lf3c')])
    add(4, 'operations', 'addition', 'adventurer', 'scale',
        T('Weigh the Lanterns', 'Timbang Tanglung'),
        T('Choose lanterns that weigh exactly the same as the big one!', 'Pilih tanglung yang beratnya sama dengan yang besar!'),
        T('Add to reach a total.', 'Menambah untuk mencapai jumlah.'),
        'Heavy', T('Heavy only lifts with both paws.', 'Heavy hanya mengangkat dengan kedua-dua kakinya.'),
        [balance(75, [25, 30, 45, 20, 10]), balance(130, [40, 55, 75, 35, 25]), balance(215, [60, 85, 125, 45, 70, 35], 3)])
    add(5, 'operations', 'multiplication', 'adventurer', 'gears',
        T('Lantern Boxes', 'Kotak Tanglung'),
        T('Find the two tiles that multiply to the total number of lanterns!', 'Cari dua jubin yang hasil darabnya ialah jumlah tanglung!'),
        T('Multiplication facts.', 'Fakta darab.'),
        'Boxy', T('Boxy counts in twelves.', 'Boxy mengira dalam kumpulan dua belas.'),
        [tiles(56, [7, 8, 6, 9, 4, 14]), tiles(72, [8, 9, 6, 12, 7, 10]), tiles(144, [12, 12, 9, 16, 8, 18])])
    add(6, 'operations', 'sharing', 'master', 'picnic',
        T('Share the Lanterns', 'Kongsi Tanglung'),
        T('Share the lanterns equally between the stalls. How many go in each?', 'Kongsi tanglung sama banyak antara gerai. Berapa banyak untuk setiap satu?'),
        T('Equal sharing.', 'Perkongsian sama banyak.'),
        'Share-bear', T('Share-bear never keeps the biggest lantern.', 'Share-bear tidak pernah menyimpan tanglung terbesar.'),
        [share(24, 4), share(30, 5), share(28, 4)])
    add(7, 'operations', 'money', 'master', 'chest',
        T('Festival Stall Coins', 'Syiling Gerai Pesta'),
        T('Pay for each festival treat with exactly the right coins!', 'Bayar setiap juadah pesta dengan syiling yang tepat!'),
        T('Exact amounts of money.', 'Jumlah wang yang tepat.'),
        'Tikka', T('Tikka sells the sweetest buns.', 'Tikka menjual bun yang paling manis.'),
        [coins(145, [5, 10, 20, 50]), coins(380, [10, 20, 50, 100]), coins(630, [5, 10, 20, 50, 100])])
    add(8, 'shape-data', 'perimeter', 'master', 'windmill',
        T('Lantern Frames', 'Bingkai Tanglung'),
        T('Find the edge length around each lantern frame!', 'Cari panjang tepi di sekeliling setiap bingkai tanglung!'),
        T('Perimeter of rectangles.', 'Perimeter segi empat tepat.'),
        'Frameo', T('Frameo has a frame for everything.', 'Frameo ada bingkai untuk segala-galanya.'),
        [shapes_perimeter(16, [(5, 3), (6, 2), (4, 4), (7, 2), (8, 1)]), shapes_perimeter(24, [(8, 4), (9, 3), (7, 6), (10, 3), (6, 6)]), shapes_perimeter(34, [(12, 5), (10, 7), (9, 8), (14, 3), (11, 5)])])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Lantern Sales Chart', 'Carta Jualan Tanglung'),
        T('Read the chart of lantern sales and answer the question.', 'Baca carta jualan tanglung dan jawab soalan itu.'),
        T('Reading bar charts.', 'Membaca carta bar.'),
        'Chartie', T('Chartie draws a bar for everything.', 'Chartie melukis bar untuk segala-galanya.'),
        [chart([(T('Red','Merah'), 12, 'coral'), (T('Gold','Emas'), 18, 'sun'), (T('Blue','Biru'), 15, 'sky')], ('diff', 1, 0), T('lanterns', 'tanglung')),
         chart([(T('Red','Merah'), 20, 'coral'), (T('Gold','Emas'), 35, 'sun'), (T('Blue','Biru'), 15, 'sky'), (T('Green','Hijau'), 30, 'mint')], ('sum', [0, 1, 2, 3]), T('lanterns', 'tanglung')),
         chart([(T('Red','Merah'), 20, 'coral'), (T('Gold','Emas'), 40, 'sun'), (T('Blue','Biru'), 30, 'sky')], ('mean',), T('lanterns', 'tanglung'))])
    add(10, 'reasoning', 'multi-step', 'master', 'lanterns',
        T('Grand Lantern Festival', 'Pesta Tanglung Agung'),
        T('The grand festival begins tonight! Solve the three steps to light every lantern.', 'Pesta agung bermula malam ini! Selesaikan tiga langkah untuk menyalakan setiap tanglung.'),
        T('Multi-step problems that use every skill.', 'Masalah berbilang langkah yang menggunakan semua kemahiran.'),
        'Grand Lampu', T('Grand Lampu lights the whole sky.', 'Grand Lampu menerangi seluruh langit.'),
        [steps([step(T('There are 8 stalls with 15 lanterns each. How many lanterns?', 'Ada 8 gerai dengan 15 tanglung setiap satu. Berapa tanglung?'), 120, '8*15'),
                step(T('25 lanterns are sold. How many are left?', '25 tanglung dijual. Berapa yang tinggal?'), 95, '120-25'),
                step(T('The rest are hung in 5 equal rows. How many in each row?', 'Selebihnya digantung dalam 5 baris yang sama. Berapa dalam setiap baris?'), 19, '95/5')],
               T('Multiply, take away, then share.', 'Darab, tolak, kemudian kongsi.'), T('8 × 15 = 120, then 120 − 25 = 95, then 95 ÷ 5 = 19.', '8 × 15 = 120, kemudian 120 − 25 = 95, kemudian 95 ÷ 5 = 19.'), 'lf10a'),
         steps([step(T('A lantern costs RM12. What do 9 lanterns cost?', 'Satu tanglung berharga RM12. Berapa harga 9 tanglung?'), 108, '9*12', RM),
                step(T('A flag costs RM7. What do 6 flags cost?', 'Satu bendera berharga RM7. Berapa harga 6 bendera?'), 42, '6*7', RM),
                step(T('What is the total cost of lanterns and flags?', 'Berapakah jumlah kos tanglung dan bendera?'), 150, '108+42', RM)],
               T('Work out each cost first, then add.', 'Kira setiap kos dahulu, kemudian tambah.'), T('9 × 12 = 108, 6 × 7 = 42, then 108 + 42 = RM150.', '9 × 12 = 108, 6 × 7 = 42, kemudian 108 + 42 = RM150.'), 'lf10b'),
         steps([step(T('The festival has 450 visitors on Friday and 380 on Saturday. How many in all?', 'Pesta itu mempunyai 450 pengunjung pada hari Jumaat dan 380 pada hari Sabtu. Berapa kesemuanya?'), 830, '450+380'),
                step(T('On Sunday there are 170 fewer than the two days together. How many on Sunday?', 'Pada hari Ahad ada 170 kurang daripada dua hari bersama. Berapa pada hari Ahad?'), 660, '830-170'),
                step(T('Add Sunday to the first two days. How many visitors over the weekend?', 'Tambah hari Ahad kepada dua hari pertama. Berapa pengunjung sepanjang hujung minggu?'), 1490, '830+660')],
               T('Add the first two days, then use that total.', 'Tambah dua hari pertama, kemudian guna jumlah itu.'), T('450 + 380 = 830, then 830 − 170 = 660, then 830 + 660 = 1490.', '450 + 380 = 830, kemudian 830 − 170 = 660, kemudian 830 + 660 = 1490.'), 'lf10c')])
    return L
