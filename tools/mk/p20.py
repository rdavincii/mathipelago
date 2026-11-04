from lib import *
CODE, BASE = 'cn', 202
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'operations', 'money', 'master', 'chest',
        T('Ticket Booth', 'Kaunter Tiket'),
        T('Welcome to the carnival! Pay for every ticket with exactly the right coins.', 'Selamat datang ke karnival! Bayar setiap tiket dengan syiling yang tepat.'),
        T('Make exact amounts of money with few or many coins.', 'Membentuk jumlah wang yang tepat dengan syiling sedikit atau banyak.'),
        'Ticket', T('Ticket tears every stub in a perfect line.', 'Ticket mengoyak setiap kepingan dalam garisan yang lurus.'),
        [coins(285, [5, 10, 20, 50, 100]), coins(470, [10, 20, 50, 100], 7), coins(695, [5, 10, 20, 50, 100], 10)])
    add(2, 'number-sense', 'time', 'master', 'ferry',
        T('Ferris Wheel Clock', 'Jam Roda Ferris'),
        T('The Ferris wheel clock shows times in hours and minutes. Match each one to the same time in another unit!', 'Jam roda Ferris menunjukkan masa dalam jam dan minit. Padankan setiap satu dengan masa yang sama dalam unit lain!'),
        T('Convert between hours, minutes and seconds.', 'Menukar antara jam, minit dan saat.'),
        'Spinner', T('Spinner rides the wheel all night long.', 'Spinner menunggang roda sepanjang malam.'),
        [match([('3 h', '180 min'), ('2 h 30 min', '150 min'), ('5 min', '300 s')], MP_, T('1 hour is 60 minutes and 1 minute is 60 seconds.', '1 jam ialah 60 minit dan 1 minit ialah 60 saat.')),
         match([('4 h 15 min', '255 min'), ('3 h 40 min', '220 min'), ('7 min', '420 s'), ('2 h 5 min', '125 min')], MP_, T('Change the hours to minutes first, then add the rest.', 'Tukar jam kepada minit dahulu, kemudian tambah bakinya.')),
         match([('6 h 20 min', '380 min'), ('9 min', '540 s'), ('1 h 55 min', '115 min'), ('10 min', '600 s'), ('5 h 45 min', '345 min')], MP_, T('Multiply hours by 60 for minutes and minutes by 60 for seconds.', 'Darab jam dengan 60 untuk minit dan minit dengan 60 untuk saat.'))])
    add(3, 'number-sense', 'place-value', 'master', 'door',
        T('Number Juggler', 'Pemain Juggling Nombor'),
        T('The juggler tosses number tiles in the air. Catch them in the right order!', 'Pemain juggling melambung jubin nombor di udara. Sambutnya mengikut urutan yang betul!'),
        T('Order digits to make the biggest or smallest number.', 'Menyusun digit untuk membentuk nombor terbesar atau terkecil.'),
        'Juggly', T('Juggly never drops a single digit.', 'Juggly tidak pernah menjatuhkan walau satu digit.'),
        [digitarrange([6, 0, 3, 9, 2], 'smallest'), digitarrange([8, 5, 0, 7, 1], 'largest'), digitarrange([4, 0, 5, 0, 9], 'smallest')])
    add(4, 'number-sense', 'rounding', 'master', 'bridge',
        T('Cannon Heights', 'Ketinggian Meriam'),
        T('The human cannon lands near a mark on the line. Round the height, or find the middle!', 'Meriam manusia mendarat berhampiran satu tanda pada garis. Bundarkan ketinggian itu, atau cari titik tengahnya!'),
        T('Round numbers and find the middle on a number line.', 'Membundarkan nombor dan mencari titik tengah pada garis nombor.'),
        'Boomer', T('Boomer lands on the exact spot every time.', 'Boomer mendarat di tempat yang tepat setiap kali.'),
        [numberline(2600, 0, 5000, 100, 500, kind='round', x=2640, unit='100'), numberline(7000, 0, 10000, 500, 1000, kind='round', x=6820, unit='1000'), numberline(-35, -50, 50, 5, 25, kind='half', a=-50, b=-20)])
    add(5, 'shape-data', 'perimeter', 'master', 'windmill',
        T('Tent Shapes', 'Bentuk Khemah'),
        T('The tents are rectangles of many sizes. Find the ones with the perimeter or area you need!', 'Khemah ialah segi empat tepat pelbagai saiz. Cari yang mempunyai perimeter atau luas yang anda perlukan!'),
        T('Find perimeter and area of rectangles.', 'Mencari perimeter dan luas segi empat tepat.'),
        'Tenty', T('Tenty always pitches a perfect rectangle.', 'Tenty sentiasa mendirikan segi empat tepat yang sempurna.'),
        [shapes_perimeter(26, [(8, 5), (7, 6), (9, 4), (10, 3), (6, 6), (12, 2)]), shapes_area(24, [(4, 6), (3, 8), (2, 12), (5, 5), (6, 3), (7, 4)]), shapes_area(36, [(6, 6), (4, 9), (3, 12), (5, 7), (8, 4), (9, 5)])])
    add(6, 'number-sense', 'fractions', 'master', 'tank',
        T('Balloon Tank', 'Tangki Belon'),
        T('Fill each balloon tank to the right line so the balloons can float!', 'Isi setiap tangki belon hingga garisan yang betul supaya belon boleh terapung!'),
        T('Show fractions of a tank, including big denominators.', 'Menunjukkan pecahan sebuah tangki, termasuk penyebut yang besar.'),
        'Floaty', T('Floaty bobs at the top of every tank.', 'Floaty terapung di bahagian atas setiap tangki.'),
        [tank(12, 5, 6), tank(20, 3, 5), tank(18, 7, 9)])
    add(7, 'number-sense', 'patterns', 'master', 'lanterns',
        T('Prize Patterns', 'Corak Hadiah'),
        T('The prize shelf follows a pattern. Work out which number comes next or is missing!', 'Rak hadiah mengikut satu pola. Cari nombor yang seterusnya atau yang hilang!'),
        T('Continue and complete number patterns.', 'Menyambung dan melengkapkan pola nombor.'),
        'Prizey', T('Prizey keeps the best prize for last.', 'Prizey menyimpan hadiah terbaik untuk akhir.'),
        [pattern('arith', 7, 13, 6, seed='cn7a'), pattern('geo', 3, 2, 6, hidden=4, seed='cn7b'), pattern('arith', 500, -45, 6, hidden=3, seed='cn7c')])
    add(8, 'operations', 'times-tables', 'master', 'gears',
        T('Popcorn Boxes', 'Kotak Bertih Jagung'),
        T('Popcorn is packed into boxes of equal size. Find the two tiles that make each total!', 'Bertih jagung dipek dalam kotak yang sama saiz. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts with bigger numbers.', 'Fakta darab dengan nombor yang lebih besar.'),
        'Popper', T('Popper jumps every time a kernel pops.', 'Popper melompat setiap kali sebutir jagung meletup.'),
        [tiles(144, [12, 16, 9, 8, 18, 6]), tiles(210, [14, 15, 21, 10, 12, 7]), tiles(360, [24, 15, 18, 20, 16, 12])])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Carnival Chart', 'Carta Karnival'),
        T('The ticket seller recorded sales for the whole week. Read the chart!', 'Penjual tiket merekodkan jualan untuk seminggu penuh. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Tally Ho', T('Tally Ho draws a stripe for every ticket sold.', 'Tally Ho melukis satu garisan untuk setiap tiket yang dijual.'),
        [chart([(T('Rides', 'Tunggangan'), 85, 'coral'), (T('Games', 'Permainan'), 60, 'sun'), (T('Food', 'Makanan'), 75, 'mint')], ('diff', 0, 1), T('tickets', 'tiket')),
         chart([(T('Rides', 'Tunggangan'), 85, 'coral'), (T('Games', 'Permainan'), 60, 'sun'), (T('Food', 'Makanan'), 75, 'mint'), (T('Shows', 'Persembahan'), 120, 'grape')], ('sum', [0, 2, 3]), T('tickets', 'tiket')),
         chart([(T('Mon', 'Isnin'), 45, 'coral'), (T('Tue', 'Selasa'), 30, 'sun'), (T('Wed', 'Rabu'), 60, 'mint'), (T('Thu', 'Khamis'), 35, 'sky'), (T('Fri', 'Jumaat'), 50, 'grape')], ('mean',), T('tickets', 'tiket'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Grand Finale', 'Kemuncak Besar'),
        T('The whole carnival cheers! Solve the hardest problems of all to light the grand finale fireworks.', 'Seluruh karnival bersorak! Selesaikan masalah paling sukar untuk menyalakan bunga api kemuncak besar.'),
        T('Hard multi-step problems with money, time, fractions and sharing.', 'Masalah berbilang langkah yang sukar dengan wang, masa, pecahan dan perkongsian.'),
        'Sparkle', T('Sparkle saves the biggest firework for the end.', 'Sparkle menyimpan bunga api terbesar untuk akhir.'),
        [steps([step(T('The carnival sells 240 tickets in the morning and 3 times as many in the afternoon. How many tickets in the afternoon?', 'Karnival menjual 240 tiket pada waktu pagi dan 3 kali ganda pada waktu petang. Berapa tiket pada waktu petang?'), 720, '240*3'),
                step(T('How many tickets in the whole day?', 'Berapa tiket sepanjang hari?'), 960, '240+720'),
                step(T('Each ticket costs RM5. How much money is that in total?', 'Setiap tiket berharga RM5. Berapa jumlah wangnya?'), 4800, '960*5', RM)],
               T('Multiply first, then add.', 'Darab dahulu, kemudian tambah.'), T('240 × 3 = 720, then 240 + 720 = 960, then 960 × 5 = RM4800.', '240 × 3 = 720, kemudian 240 + 720 = 960, kemudian 960 × 5 = RM4800.'), 'cn10a'),
         steps([step(T('A show lasts 2 hours and 15 minutes. How many minutes is that?', 'Sebuah persembahan berlangsung selama 2 jam 15 minit. Berapa minit itu?'), 135, '2*60+15'),
                step(T('There are 4 shows a day. How many minutes of shows in a day?', 'Ada 4 persembahan sehari. Berapa minit persembahan dalam sehari?'), 540, '135*4'),
                step(T('How many hours is that?', 'Berapa jam itu?'), 9, '540/60')],
               T('Change hours to minutes first.', 'Tukar jam kepada minit dahulu.'), T('2 × 60 + 15 = 135, then 135 × 4 = 540, then 540 ÷ 60 = 9.', '2 × 60 + 15 = 135, kemudian 135 × 4 = 540, kemudian 540 ÷ 60 = 9.'), 'cn10b'),
         steps([step(T('A prize stall has 360 toys. Two thirds are small. How many small toys?', 'Sebuah gerai hadiah mempunyai 360 mainan. Dua pertiga daripadanya kecil. Berapa mainan kecil?'), 240, '360/3*2'),
                step(T('The small toys are packed in boxes of 15. How many boxes?', 'Mainan kecil dipek dalam kotak yang berisi 15. Berapa kotak?'), 16, '240/15'),
                step(T('Each box sells for RM18. How much money from all the boxes?', 'Setiap kotak dijual dengan harga RM18. Berapa wang daripada semua kotak?'), 288, '16*18', RM)],
               T('Find one third first, then double it.', 'Cari satu pertiga dahulu, kemudian gandakannya.'), T('360 ÷ 3 × 2 = 240, then 240 ÷ 15 = 16, then 16 × 18 = RM288.', '360 ÷ 3 × 2 = 240, kemudian 240 ÷ 15 = 16, kemudian 16 × 18 = RM288.'), 'cn10c')])
    return L
