from lib import *
CODE, BASE = 'sa', 172
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'decimals', 'adventurer', 'door',
        T('Stopwatch Match', 'Padanan Jam Randik'),
        T('The stopwatch shows race times in two ways. Match the times that are the same!', 'Jam randik menunjukkan masa perlumbaan dalam dua cara. Padankan masa yang sama!'),
        T('Match seconds as decimals and as milliseconds.', 'Memadankan saat sebagai perpuluhan dan sebagai milisaat.'),
        'Sprinty', T('Sprinty starts every race a little too early.', 'Sprinty memulakan setiap perlumbaan terlalu awal sedikit.'),
        [match([('1.5 s', '1500 ms'), ('2.5 s', '2500 ms'), ('0.5 s', '500 ms')], MP_, T('1 second is 1000 milliseconds.', '1 saat ialah 1000 milisaat.')),
         match([('3.2 s', '3200 ms'), ('4.5 s', '4500 ms'), ('0.8 s', '800 ms'), ('6000 ms', '6 s')], MP_, T('Multiply the seconds by 1000.', 'Darabkan saat dengan 1000.')),
         match([('7.25 s', '7250 ms'), ('9.5 s', '9500 ms'), ('0.75 s', '750 ms'), ('12 s', '12000 ms'), ('10.2 s', '10200 ms')], MP_, T('1 second is 1000 milliseconds.', '1 saat ialah 1000 milisaat.'))])
    add(2, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('Running Track', 'Trek Larian'),
        T('Place the runner on the right spot along the running track!', 'Letakkan pelari di tempat yang betul sepanjang trek larian!'),
        T('Place numbers on a line in fifties and hundreds.', 'Meletakkan nombor pada garis dalam lima puluh dan seratus.'),
        'Dasher', T('Dasher never trips over the finish line.', 'Dasher tidak pernah tersandung pada garisan penamat.'),
        [numberline(150, 0, 400, 50, 100), numberline(700, 0, 1000, 100, 200), numberline(550, 200, 1000, 50, 200, kind='half', a=300, b=800)])
    add(3, 'operations', 'multi-step', 'adventurer', 'chest',
        T('Scoreboard', 'Papan Markah'),
        T('The scoreboard needs your help. Work out each score in three steps!', 'Papan markah memerlukan bantuan anda. Kira setiap markah dalam tiga langkah!'),
        T('Add, multiply and subtract to find scores.', 'Menambah, mendarab dan menolak untuk mencari markah.'),
        'Scorey', T('Scorey keeps the score in a tiny notebook.', 'Scorey menyimpan markah dalam buku nota kecil.'),
        [steps([step(T('A team scores 3 goals in each of 4 matches. How many goals?', 'Sebuah pasukan menjaringkan 3 gol dalam setiap 4 perlawanan. Berapa gol?'), 12, '3*4'),
                step(T('They score 5 more goals in the final. How many goals now?', 'Mereka menjaringkan 5 gol lagi dalam perlawanan akhir. Berapa gol sekarang?'), 17, '12+5'),
                step(T('The other team has 9 goals. How many more goals does the winner have?', 'Pasukan lawan mempunyai 9 gol. Berapa gol lebih yang dimiliki pemenang?'), 8, '17-9')],
               T('Multiply first, then add, then subtract.', 'Darab dahulu, kemudian tambah, kemudian tolak.'), T('3 × 4 = 12, then 12 + 5 = 17, then 17 − 9 = 8.', '3 × 4 = 12, kemudian 12 + 5 = 17, kemudian 17 − 9 = 8.'), 'sa3a'),
         steps([step(T('A basketball player scores 6 baskets worth 2 points. How many points?', 'Seorang pemain bola keranjang menjaringkan 6 bakul bernilai 2 mata. Berapa mata?'), 12, '6*2'),
                step(T('She scores 4 baskets worth 3 points. How many points from those?', 'Dia menjaringkan 4 bakul bernilai 3 mata. Berapa mata daripada bakul itu?'), 12, '4*3'),
                step(T('How many points does she have in total?', 'Berapa jumlah mata yang dimilikinya?'), 24, '12+12')],
               T('Find the two scores separately, then add.', 'Cari kedua-dua markah secara berasingan, kemudian tambah.'), T('6 × 2 = 12, 4 × 3 = 12, then 12 + 12 = 24.', '6 × 2 = 12, 4 × 3 = 12, kemudian 12 + 12 = 24.'), 'sa3b'),
         steps([step(T('A league has 8 teams. Each team plays 7 matches. How many matches are counted?', 'Sebuah liga mempunyai 8 pasukan. Setiap pasukan bermain 7 perlawanan. Berapa perlawanan yang dikira?'), 56, '8*7'),
                step(T('Each match is counted twice, once for each team. How many real matches are there?', 'Setiap perlawanan dikira dua kali, sekali untuk setiap pasukan. Berapa perlawanan sebenar?'), 28, '56/2'),
                step(T('Each match gives 3 points to the winner. How many points are given out?', 'Setiap perlawanan memberikan 3 mata kepada pemenang. Berapa mata diberikan?'), 84, '28*3')],
               T('Each match has two teams, so halve the count.', 'Setiap perlawanan ada dua pasukan, jadi bahagi dua bilangan itu.'), T('8 × 7 = 56, then 56 ÷ 2 = 28, then 28 × 3 = 84.', '8 × 7 = 56, kemudian 56 ÷ 2 = 28, kemudian 28 × 3 = 84.'), 'sa3c')])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Lap Counter', 'Pengira Pusingan'),
        T('The lap counter follows a pattern. What number comes next?', 'Pengira pusingan mengikut satu pola. Nombor apakah yang seterusnya?'),
        T('Continue patterns that add the same amount each time.', 'Menyambung pola yang menambah jumlah yang sama setiap kali.'),
        'Lappy', T('Lappy goes round and round for fun.', 'Lappy berpusing-pusing untuk bergembira.'),
        [pattern('arith', 4, 4, 5, seed='sa4a'), pattern('arith', 10, 25, 5, seed='sa4b'), pattern('arith', 90, -15, 6, hidden=3, seed='sa4c')])
    add(5, 'shape-data', 'data', 'adventurer', 'lighthouse',
        T('Medal Chart', 'Carta Pingat'),
        T('The arena counted every medal. Read the chart to find the answer!', 'Arena mengira setiap pingat. Baca carta untuk mencari jawapannya!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Medalo', T('Medalo polishes every medal until it shines.', 'Medalo menggilap setiap pingat sehingga berkilau.'),
        [chart([(T('Gold', 'Emas'), 9, 'sun'), (T('Silver', 'Perak'), 6, 'sky'), (T('Bronze', 'Gangsa'), 11, 'coral')], ('diff', 2, 1), T('medals', 'pingat')),
         chart([(T('Gold', 'Emas'), 14, 'sun'), (T('Silver', 'Perak'), 18, 'sky'), (T('Bronze', 'Gangsa'), 12, 'coral'), (T('Fourth', 'Keempat'), 16, 'mint')], ('sum', [0, 1, 2, 3]), T('medals', 'pingat')),
         chart([(T('Mon', 'Isnin'), 20, 'sun'), (T('Tue', 'Selasa'), 35, 'sky'), (T('Wed', 'Rabu'), 25, 'coral'), (T('Thu', 'Khamis'), 45, 'mint'), (T('Fri', 'Jumaat'), 30, 'grape')], ('mean',), T('fans', 'peminat'))])
    add(6, 'operations', 'money', 'adventurer', 'chest',
        T('Ticket Booth', 'Gerai Tiket'),
        T('Pay for each ticket at the booth with exactly the right coins!', 'Bayar setiap tiket di gerai dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Ticky', T('Ticky tears each ticket with a small snip.', 'Ticky mengoyak setiap tiket dengan satu guntingan kecil.'),
        [coins(95, [5, 10, 20, 50]), coins(260, [10, 20, 50, 100]), coins(485, [5, 10, 20, 50, 100], 8)])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Stadium Seats', 'Tempat Duduk Stadium'),
        T('The stadium seats are in equal rows. Find the two tiles that make each total!', 'Tempat duduk stadium disusun dalam baris yang sama. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Seaty', T('Seaty always finds the best seat.', 'Seaty sentiasa menjumpai tempat duduk terbaik.'),
        [tiles(54, [6, 9, 7, 8, 3, 18]), tiles(120, [10, 12, 8, 15, 6, 20]), tiles(224, [14, 16, 8, 28, 12, 7])])
    add(8, 'number-sense', 'fractions', 'master', 'tank',
        T('Water Bottles', 'Botol Air'),
        T('The players are thirsty. Fill each bottle to the right line!', 'Para pemain dahaga. Isi setiap botol hingga garisan yang betul!'),
        T('Fractions of a bottle.', 'Pecahan sebuah botol.'),
        'Sippy', T('Sippy takes tiny sips between rounds.', 'Sippy minum sedikit-sedikit antara pusingan.'),
        [tank(8, 3, 4), tank(10, 7, 10), tank(12, 5, 6)])
    add(9, 'number-sense', 'time', 'master', 'door',
        T('Match Timer', 'Pemasa Perlawanan'),
        T('Match each game length in minutes to the same time in hours and minutes!', 'Padankan setiap tempoh permainan dalam minit dengan masa yang sama dalam jam dan minit!'),
        T('Convert between minutes and hours.', 'Menukar antara minit dan jam.'),
        'Whistle', T('Whistle blows exactly when time is up.', 'Whistle bertiup tepat apabila masa tamat.'),
        [match([('90 min', '1 h 30 min'), ('120 min', '2 h'), ('150 min', '2 h 30 min')], MP_, T('60 minutes make 1 hour.', '60 minit membentuk 1 jam.')),
         match([('75 min', '1 h 15 min'), ('105 min', '1 h 45 min'), ('180 min', '3 h'), ('135 min', '2 h 15 min')], MP_, T('Take away 60 for each whole hour.', 'Tolak 60 bagi setiap jam penuh.')),
         match([('200 min', '3 h 20 min'), ('250 min', '4 h 10 min'), ('310 min', '5 h 10 min'), ('185 min', '3 h 5 min'), ('360 min', '6 h')], MP_, T('Divide by 60 to find the hours.', 'Bahagi dengan 60 untuk mencari jam.'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Championship Finale', 'Kemuncak Kejohanan'),
        T('The championship final is here! Solve the three-step problems to lift the trophy.', 'Perlawanan akhir kejohanan telah tiba! Selesaikan masalah tiga langkah untuk mengangkat piala.'),
        T('Multi-step problems with money, time and scores.', 'Masalah berbilang langkah dengan wang, masa dan markah.'),
        'Trophy', T('Trophy sparkles when the team wins.', 'Trophy berkilauan apabila pasukan menang.'),
        [steps([step(T('A ticket costs RM12. What do 8 tickets cost?', 'Satu tiket berharga RM12. Berapa harga 8 tiket?'), 96, '8*12', RM),
                step(T('A team scarf costs RM15. What is the total for the tickets and the scarf?', 'Sehelai skarf pasukan berharga RM15. Berapa jumlah untuk tiket dan skarf itu?'), 111, '96+15', RM),
                step(T('You pay with RM150. How much change do you get?', 'Anda membayar dengan RM150. Berapa baki yang anda terima?'), 39, '150-111', RM)],
               T('Add the costs, then work out the change.', 'Tambah harga, kemudian kira baki.'), T('8 × 12 = 96, then 96 + 15 = 111, then 150 − 111 = 39.', '8 × 12 = 96, kemudian 96 + 15 = 111, kemudian 150 − 111 = 39.'), 'sa10a'),
         steps([step(T('A game has 4 quarters of 12 minutes. How many minutes of play?', 'Satu permainan mempunyai 4 suku masa selama 12 minit. Berapa minit permainan?'), 48, '4*12'),
                step(T('There are 3 breaks of 5 minutes. How many minutes of break?', 'Terdapat 3 rehat selama 5 minit. Berapa minit rehat?'), 15, '3*5'),
                step(T('How many minutes does the whole game take?', 'Berapa minit keseluruhan permainan itu?'), 63, '48+15')],
               T('Work out play time and break time separately.', 'Kira masa bermain dan masa rehat secara berasingan.'), T('4 × 12 = 48, 3 × 5 = 15, then 48 + 15 = 63.', '4 × 12 = 48, 3 × 5 = 15, kemudian 48 + 15 = 63.'), 'sa10b'),
         steps([step(T('A runner does 5 laps of 400 metres. How many metres?', 'Seorang pelari berlari 5 pusingan sejauh 400 meter. Berapa meter?'), 2000, '5*400', lambda v: f'{v} m'),
                step(T('She runs 2000 metres in 10 minutes. How many metres does she run in 1 minute?', 'Dia berlari 2000 meter dalam 10 minit. Berapa meter yang dilarinya dalam 1 minit?'), 200, '2000/10', lambda v: f'{v} m'),
                step(T('At that speed, how many metres does she run in 25 minutes?', 'Pada kelajuan itu, berapa meter yang dilarinya dalam 25 minit?'), 5000, '200*25', lambda v: f'{v} m')],
               T('Find the distance for 1 minute first.', 'Cari jarak untuk 1 minit dahulu.'), T('5 × 400 = 2,000, then 2,000 ÷ 10 = 200, then 200 × 25 = 5,000.', '5 × 400 = 2,000, kemudian 2,000 ÷ 10 = 200, kemudian 200 × 25 = 5,000.'), 'sa10c')])
    return L
