from lib import *
CODE, BASE = 'tr', 242
RM = lambda v: f'RM{v}'
MT = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'time', 'adventurer', 'door',
        T('Platform Clocks', 'Jam Platform'),
        T('The station clocks show the same time in different ways. Match them!', 'Jam stesen menunjukkan masa yang sama dengan cara berbeza. Padankan mereka!'),
        T('Convert between hours and minutes.', 'Menukar antara jam dan minit.'),
        'Choo', T('Choo toots once for every hour.', 'Choo berbunyi sekali untuk setiap jam.'),
        [match([('1 h', '60 min'), ('2 h', '120 min'), ('3 h', '180 min')], MT, T('There are 60 minutes in 1 hour.', 'Terdapat 60 minit dalam 1 jam.')),
         match([('1 h 30 min', '90 min'), ('2 h 15 min', '135 min'), ('3 h 30 min', '210 min'), ('4 h', '240 min')], MT, T('Change the hours to minutes, then add the minutes.', 'Tukar jam kepada minit, kemudian tambah minit.')),
         match([('2 h 45 min', '165 min'), ('1 h 20 min', '80 min'), ('3 h 5 min', '185 min'), ('4 h 10 min', '250 min'), ('5 h 25 min', '325 min')], MT, T('Change the hours to minutes, then add the minutes.', 'Tukar jam kepada minit, kemudian tambah minit.'))])
    add(2, 'number-sense', 'time', 'adventurer', 'bridge',
        T('Departure Line', 'Garis Perlepasan'),
        T('Trains leave at different minutes. Slide the marker to the right minute!', 'Kereta api bertolak pada minit yang berbeza. Gelongsorkan penanda ke minit yang betul!'),
        T('Read minutes on a number line.', 'Membaca minit pada garis nombor.'),
        'Rails', T('Rails knows every minute of the timetable.', 'Rails tahu setiap minit dalam jadual.'),
        [numberline(40, 0, 60, 5, 10), numberline(105, 0, 180, 15, 30), numberline(90, 0, 120, 10, 30, kind='half', a=60, b=120)])
    add(3, 'operations', 'time', 'adventurer', 'ferry',
        T('Timetable Trouble', 'Masalah Jadual'),
        T('The stationmaster is working out the timetable. Help her add up the minutes!', 'Ketua stesen sedang mengira jadual. Bantu dia menambah minit!'),
        T('Add and multiply durations in minutes.', 'Menambah dan mendarab tempoh dalam minit.'),
        'Timer', T('Timer checks the big clock twice an hour.', 'Timer memeriksa jam besar dua kali sejam.'),
        [steps([step(T('A train trip takes 35 minutes. How many minutes is a trip there and back?', 'Satu perjalanan kereta api mengambil masa 35 minit. Berapa minit untuk pergi dan balik?'), 70, '35*2'),
                step(T('The train rests for 15 minutes at the end. How many minutes is that in total?', 'Kereta api berehat selama 15 minit di hujung. Berapa minit jumlahnya?'), 85, '70+15'),
                step(T('How many minutes is that in 3 round trips?', 'Berapa minit jumlahnya untuk 3 perjalanan pergi dan balik?'), 255, '85*3')],
               T('There and back is double the trip.', 'Pergi dan balik ialah dua kali perjalanan.'), T('35 × 2 = 70, then 70 + 15 = 85, then 85 × 3 = 255.', '35 × 2 = 70, kemudian 70 + 15 = 85, kemudian 85 × 3 = 255.'), 'tr3a'),
         steps([step(T('A train leaves every 20 minutes. How many trains leave in 2 hours? (2 h = 120 min)', 'Sebuah kereta api bertolak setiap 20 minit. Berapa kereta api bertolak dalam 2 jam? (2 jam = 120 min)'), 6, '120/20'),
                step(T('Each train carries 40 passengers. How many passengers is that?', 'Setiap kereta api membawa 40 penumpang. Berapa penumpang itu?'), 240, '6*40'),
                step(T('300 people wait at the platform. How many cannot get on?', '300 orang menunggu di platform. Berapa orang yang tidak dapat naik?'), 60, '300-240')],
               T('Divide the time by the gap between trains.', 'Bahagi masa dengan sela antara kereta api.'), T('120 ÷ 20 = 6, then 6 × 40 = 240, then 300 − 240 = 60.', '120 ÷ 20 = 6, kemudian 6 × 40 = 240, kemudian 300 − 240 = 60.'), 'tr3b'),
         steps([step(T('A journey takes 4 hours. How many minutes is that?', 'Satu perjalanan mengambil masa 4 jam. Berapa minit itu?'), 240, '4*60'),
                step(T('The train stops 8 times for 5 minutes each. How many minutes of stopping?', 'Kereta api berhenti 8 kali selama 5 minit setiap kali. Berapa minit berhenti?'), 40, '8*5'),
                step(T('How many minutes does the train really spend moving?', 'Berapa minit sebenarnya kereta api itu bergerak?'), 200, '240-40')],
               T('Take the stopping time away from the whole journey.', 'Tolak masa berhenti daripada keseluruhan perjalanan.'), T('4 × 60 = 240, 8 × 5 = 40, then 240 − 40 = 200.', '4 × 60 = 240, 8 × 5 = 40, kemudian 240 − 40 = 200.'), 'tr3c')])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Carriage Numbers', 'Nombor Gerabak'),
        T('The carriages are numbered in a pattern. Which number comes next?', 'Gerabak bernombor mengikut satu pola. Nombor manakah yang seterusnya?'),
        T('Continue number patterns in steps of 10, 12 and 25.', 'Menyambung pola nombor dengan langkah 10, 12 dan 25.'),
        'Carry', T('Carry hops from carriage to carriage.', 'Carry melompat dari gerabak ke gerabak.'),
        [pattern('arith', 10, 10, 5, seed='tr4a'), pattern('arith', 12, 12, 6, seed='tr4b'), pattern('arith', 25, 25, 6, hidden=4, seed='tr4c')])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Fuel Stop', 'Perhentian Bahan Api'),
        T('The engine needs fuel before it can leave. Fill each tank to the line shown!', 'Enjin memerlukan bahan api sebelum boleh bertolak. Isi setiap tangki hingga garisan yang ditunjukkan!'),
        T('Fractions of a tank.', 'Pecahan sebuah tangki.'),
        'Puffy', T('Puffy puffs a little steam when the tank is full.', 'Puffy mengeluarkan sedikit wap apabila tangki penuh.'),
        [tank(8, 1, 2), tank(12, 2, 3), tank(10, 3, 5)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Seat Sharing', 'Perkongsian Tempat Duduk'),
        T('Passengers sit in equal groups in each carriage. Share them out fairly!', 'Penumpang duduk dalam kumpulan yang sama banyak dalam setiap gerabak. Agihkan dengan adil!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Seaty', T('Seaty saves a window seat for everyone.', 'Seaty menyimpan tempat duduk tepi tingkap untuk semua orang.'),
        [share(12, 3), share(20, 4), share(25, 5)])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Carriage Seats', 'Tempat Duduk Gerabak'),
        T('Every carriage has the same number of seats. Find the two tiles that make each total!', 'Setiap gerabak mempunyai bilangan tempat duduk yang sama. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Seatly', T('Seatly counts every seat before the train leaves.', 'Seatly mengira setiap tempat duduk sebelum kereta api bertolak.'),
        [tiles(48, [6, 8, 4, 12, 3, 9]), tiles(96, [8, 12, 6, 16, 4, 9]), tiles(168, [12, 14, 8, 21, 7, 16])])
    add(8, 'operations', 'money', 'master', 'chest',
        T('Ticket Counter', 'Kaunter Tiket'),
        T('Tickets cost different prices. Pay for each one with exactly the right coins!', 'Tiket berharga berbeza. Bayar setiap satu dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Ticky', T('Ticky stamps every ticket twice.', 'Ticky mengecop setiap tiket dua kali.'),
        [coins(75, [5, 10, 20, 50]), coins(180, [10, 20, 50, 100]), coins(445, [5, 10, 20, 50, 100], 7)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Passenger Chart', 'Carta Penumpang'),
        T('The station counted the passengers on each train. Read the chart!', 'Stesen mengira penumpang pada setiap kereta api. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Counter', T('Counter clicks a little button for every passenger.', 'Counter menekan butang kecil untuk setiap penumpang.'),
        [chart([(T('Morning', 'Pagi'), 120, 'sky'), (T('Noon', 'Tengah hari'), 80, 'sun'), (T('Evening', 'Petang'), 150, 'coral')], ('diff', 2, 1), T('passengers', 'penumpang')),
         chart([(T('Morning', 'Pagi'), 110, 'sky'), (T('Noon', 'Tengah hari'), 70, 'sun'), (T('Evening', 'Petang'), 130, 'coral'), (T('Night', 'Malam'), 50, 'grape')], ('sum', [0, 1, 2, 3]), T('passengers', 'penumpang')),
         chart([(T('Mon', 'Isnin'), 200, 'sky'), (T('Tue', 'Selasa'), 150, 'sun'), (T('Wed', 'Rabu'), 250, 'coral'), (T('Thu', 'Khamis'), 100, 'mint'), (T('Fri', 'Jumaat'), 300, 'grape')], ('mean',), T('passengers', 'penumpang'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Express Finale', 'Kemuncak Ekspres'),
        T('The express train is ready to roll! Solve three steps to give the green light.', 'Kereta api ekspres sedia untuk bergerak! Selesaikan tiga langkah untuk memberi lampu hijau.'),
        T('Multi-step problems with time, money and sharing.', 'Masalah berbilang langkah dengan masa, wang dan perkongsian.'),
        'Express', T('Express never stops at a station that is not on the list.', 'Express tidak pernah berhenti di stesen yang tiada dalam senarai.'),
        [steps([step(T('The express has 8 carriages with 60 seats each. How many seats are there?', 'Ekspres itu mempunyai 8 gerabak dengan 60 tempat duduk setiap satu. Berapa tempat duduk kesemuanya?'), 480, '8*60'),
                step(T('It runs 3 times a day. How many seats are available in a day?', 'Ia beroperasi 3 kali sehari. Berapa tempat duduk tersedia dalam sehari?'), 1440, '480*3'),
                step(T('1,000 people travel. How many seats are empty?', '1,000 orang melakukan perjalanan. Berapa tempat duduk yang kosong?'), 440, '1440-1000')],
               T('Multiply to find the seats, then subtract the passengers.', 'Darab untuk mencari tempat duduk, kemudian tolak penumpang.'), T('8 × 60 = 480, then 480 × 3 = 1,440, then 1,440 − 1,000 = 440.', '8 × 60 = 480, kemudian 480 × 3 = 1,440, kemudian 1,440 − 1,000 = 440.'), 'tr10a'),
         steps([step(T('A ticket costs RM12. What do 5 tickets cost?', 'Satu tiket berharga RM12. Berapa harga 5 tiket?'), 60, '5*12', RM),
                step(T('A snack costs RM8. What is the total for the tickets and the snack?', 'Sebuah snek berharga RM8. Berapa jumlah untuk tiket dan snek itu?'), 68, '60+8', RM),
                step(T('You pay with RM100. How much change do you get?', 'Anda membayar dengan RM100. Berapa baki yang anda terima?'), 32, '100-68', RM)],
               T('Add the costs, then take them from RM100.', 'Tambah harga, kemudian tolak daripada RM100.'), T('5 × 12 = 60, then 60 + 8 = 68, then 100 − 68 = 32.', '5 × 12 = 60, kemudian 60 + 8 = 68, kemudian 100 − 68 = 32.'), 'tr10b'),
         steps([step(T('A train leaves at minute 0 and the trip takes 2 hours 30 minutes. How many minutes is that?', 'Sebuah kereta api bertolak pada minit 0 dan perjalanan mengambil masa 2 jam 30 minit. Berapa minit itu?'), 150, '2*60+30'),
                step(T('It travels 90 km every hour. How many km does it travel in 150 minutes? (Work out in 30-minute parts: 5 parts of 45 km.)', 'Ia bergerak 90 km setiap jam. Berapa km ia bergerak dalam 150 minit? (Kira dalam bahagian 30 minit: 5 bahagian setiap satu 45 km.)'), 225, '5*45', lambda v: f'{v} km'),
                step(T('The whole track is 300 km. How many km are left?', 'Seluruh landasan sepanjang 300 km. Berapa km lagi yang tinggal?'), 75, '300-225', lambda v: f'{v} km')],
               T('150 minutes is 5 parts of 30 minutes.', '150 minit ialah 5 bahagian 30 minit.'), T('2 × 60 + 30 = 150, then 5 × 45 = 225, then 300 − 225 = 75.', '2 × 60 + 30 = 150, kemudian 5 × 45 = 225, kemudian 300 − 225 = 75.'), 'tr10c')])
    return L
