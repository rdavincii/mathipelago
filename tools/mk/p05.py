from lib import *
CODE, BASE = 'ch', 52
MT = T('Tap a question, then tap its answer.', 'Ketik satu soalan, kemudian ketik jawapannya.')

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'time', 'adventurer', 'ferry',
        T('Dock Minutes', 'Minit di Dermaga'),
        T('Ships at the dock leave on the minute. Match each time to the same time in other units!', 'Kapal di dermaga bertolak tepat pada masanya. Padankan setiap masa dengan masa yang sama dalam unit lain!'),
        T('Convert between hours, minutes and seconds.', 'Menukar antara jam, minit dan saat.'),
        'Tickle', T('Tickle can count sixty seconds without a clock.', 'Tickle boleh mengira enam puluh saat tanpa jam.'),
        [match([('2 min', '120 s'), ('3 min', '180 s'), ('1 min', '60 s')], T('Tap a time, then tap the same time in other units.', 'Ketik satu masa, kemudian ketik masa yang sama dalam unit lain.'), T('There are 60 seconds in 1 minute.', 'Terdapat 60 saat dalam 1 minit.')),
         match([('2 h', '120 min'), ('3 h', '180 min'), ('1 h', '60 min'), ('4 h', '240 min')], T('Tap a time, then tap the same time in other units.', 'Ketik satu masa, kemudian ketik masa yang sama dalam unit lain.'), T('There are 60 minutes in 1 hour.', 'Terdapat 60 minit dalam 1 jam.')),
         match([('2 h 30 min', '150 min'), ('1 h 45 min', '105 min'), ('3 h 15 min', '195 min'), ('2 h 10 min', '130 min'), ('90 min', '1 h 30 min')], T('Tap a time, then tap the same time in other units.', 'Ketik satu masa, kemudian ketik masa yang sama dalam unit lain.'), T('Change the hours to minutes first, then add the minutes.', 'Tukar jam kepada minit dahulu, kemudian tambah minit.'))])
    add(2, 'number-sense', 'time', 'adventurer', 'bridge',
        T('Departure Board', 'Papan Perlepasan'),
        T('The departure board shows minutes on a long line. Slide the marker to the right time!', 'Papan perlepasan menunjukkan minit pada garis panjang. Gelongsorkan penanda ke masa yang betul!'),
        T('Read minutes on a number line.', 'Membaca minit pada garis nombor.'),
        'Tocky', T('Tocky taps every time the minute hand moves.', 'Tocky mengetuk setiap kali jarum minit bergerak.'),
        [numberline(45, 0, 60, 5, 15), numberline(135, 0, 180, 15, 30), numberline(55, 0, 120, 5, 30, kind='half', a=20, b=90)])
    add(3, 'operations', 'time', 'adventurer', 'ferry',
        T('Ferry Timetable', 'Jadual Feri'),
        T('The harbour master needs help with the ferry timetable. Work out how long everything takes!', 'Tuan pelabuhan memerlukan bantuan dengan jadual feri. Kira berapa lama setiap perkara mengambil masa!'),
        T('Add and multiply durations in minutes.', 'Menambah dan mendarab tempoh dalam minit.'),
        'Ferrick', T('Ferrick crosses the bay again and again.', 'Ferrick menyeberangi teluk berulang kali.'),
        [steps([step(T('A ferry trip takes 25 minutes. How many minutes is a trip there and back?', 'Satu perjalanan feri mengambil masa 25 minit. Berapa minit untuk pergi dan balik?'), 50, '25*2'),
                step(T('The ferry waits 10 minutes before leaving again. How many minutes is that in total?', 'Feri menunggu 10 minit sebelum bertolak semula. Berapa minit jumlahnya?'), 60, '50+10'),
                step(T('How many 20-minute breaks fit into that time?', 'Berapa rehat 20 minit yang muat dalam masa itu?'), 3, '60/20')],
               T('There and back is double the trip.', 'Pergi dan balik ialah dua kali perjalanan.'), T('25 × 2 = 50, then 50 + 10 = 60, then 60 ÷ 20 = 3.', '25 × 2 = 50, kemudian 50 + 10 = 60, kemudian 60 ÷ 20 = 3.'), 'ch3a'),
         steps([step(T('A boat makes 3 trips and each trip takes 40 minutes. How many minutes is that?', 'Sebuah bot membuat 3 perjalanan dan setiap perjalanan mengambil masa 40 minit. Berapa minit itu?'), 120, '3*40'),
                step(T('Loading takes 30 minutes more. How many minutes in total?', 'Memuatkan barang mengambil 30 minit lagi. Berapa minit jumlahnya?'), 150, '120+30'),
                step(T('How many 15-minute breaks fit into that time?', 'Berapa rehat 15 minit yang muat dalam masa itu?'), 10, '150/15')],
               T('Multiply, then add, then divide.', 'Darab, kemudian tambah, kemudian bahagi.'), T('3 × 40 = 120, then 120 + 30 = 150, then 150 ÷ 15 = 10.', '3 × 40 = 120, kemudian 120 + 30 = 150, kemudian 150 ÷ 15 = 10.'), 'ch3b'),
         steps([step(T('A boat runs for 18 hours a day. How many minutes is that?', 'Sebuah bot beroperasi selama 18 jam sehari. Berapa minit itu?'), 1080, '18*60'),
                step(T('Each trip takes 45 minutes. How many trips fit into the day?', 'Setiap perjalanan mengambil masa 45 minit. Berapa perjalanan yang muat dalam sehari?'), 24, '1080/45'),
                step(T('Each trip carries 12 passengers. How many passengers in a day?', 'Setiap perjalanan membawa 12 penumpang. Berapa penumpang sehari?'), 288, '24*12')],
               T('Change hours to minutes by multiplying by 60.', 'Tukar jam kepada minit dengan mendarab dengan 60.'), T('18 × 60 = 1,080, then 1,080 ÷ 45 = 24, then 24 × 12 = 288.', '18 × 60 = 1,080, kemudian 1,080 ÷ 45 = 24, kemudian 24 × 12 = 288.'), 'ch3c')])
    add(4, 'number-sense', 'calendar', 'adventurer', 'lanterns',
        T('Calendar Wall', 'Dinding Kalendar'),
        T('The harbour calendar skips from week to week. Find the date that comes next!', 'Kalendar pelabuhan melompat dari minggu ke minggu. Cari tarikh yang seterusnya!'),
        T('Count in sevens for weeks and in fourteens for fortnights.', 'Mengira dalam tujuh untuk minggu dan empat belas untuk dua minggu.'),
        'Datey', T('Datey marks every Friday with a star.', 'Datey menandakan setiap hari Jumaat dengan bintang.'),
        [pattern('arith', 3, 7, 5, seed='ch4a'), pattern('arith', 2, 14, 5, seed='ch4b'), pattern('arith', 5, 7, 6, hidden=3, seed='ch4c')])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Tide Tank', 'Tangki Air Pasang'),
        T('The tide tank must be filled to the right line before the ships can sail!', 'Tangki air pasang mesti diisi hingga garisan yang betul sebelum kapal boleh belayar!'),
        T('Fractions of a tank, including equivalent fractions.', 'Pecahan sebuah tangki, termasuk pecahan setara.'),
        'Tidey', T('Tidey rises and falls with the tide.', 'Tidey naik dan turun mengikut air pasang.'),
        [tank(12, 1, 3), tank(12, 5, 6), tank(20, 3, 4)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Clock Share', 'Perkongsian Jam'),
        T('Sailors share their berries at every bell. Make sure every basket gets the same!', 'Para kelasi berkongsi beri mereka pada setiap loceng. Pastikan setiap bakul mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Belly', T('Belly rings once for every full basket.', 'Belly berbunyi sekali untuk setiap bakul yang penuh.'),
        [share(10, 2), share(21, 3), share(28, 4)])
    add(7, 'operations', 'times-tables', 'master', 'gears',
        T('Seconds Counter', 'Pengira Saat'),
        T('The clock tower counts seconds, minutes and hours. Find the two tiles that make each total!', 'Menara jam mengira saat, minit dan jam. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts with time.', 'Fakta darab dengan masa.'),
        'Ticker', T('Ticker never loses a single second.', 'Ticker tidak pernah kehilangan walau satu saat.'),
        [tiles(60, [6, 10, 5, 7, 3, 2]), tiles(180, [12, 15, 9, 20, 6, 18]), tiles(1440, [24, 60, 48, 30, 12, 36])])
    add(8, 'operations', 'money', 'master', 'chest',
        T('Pay the Pier', 'Bayar di Jeti'),
        T('Every ship pays a fee at the pier. Pay it with exactly the right coins!', 'Setiap kapal membayar yuran di jeti. Bayarnya dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Dockie', T('Dockie collects the fees in a little tin.', 'Dockie mengumpul yuran dalam tin kecil.'),
        [coins(60, [5, 10, 20, 50]), coins(175, [5, 10, 20, 50, 100]), coins(395, [5, 10, 20, 50, 100], 7)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Harbour Chart', 'Carta Pelabuhan'),
        T('The harbour master recorded the ships that arrived each day. Read the chart!', 'Tuan pelabuhan merekodkan kapal yang tiba setiap hari. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Logbook', T('Logbook writes down every ship, big or small.', 'Logbook mencatat setiap kapal, besar atau kecil.'),
        [chart([(T('Mon', 'Isnin'), 8, 'coral'), (T('Tue', 'Selasa'), 5, 'sky'), (T('Wed', 'Rabu'), 11, 'mint')], ('diff', 2, 1), T('ships', 'kapal')),
         chart([(T('Mon', 'Isnin'), 12, 'coral'), (T('Tue', 'Selasa'), 18, 'sky'), (T('Wed', 'Rabu'), 9, 'mint'), (T('Thu', 'Khamis'), 16, 'sun')], ('sum', [0, 1, 2, 3]), T('ships', 'kapal')),
         chart([(T('Mon', 'Isnin'), 24, 'coral'), (T('Tue', 'Selasa'), 18, 'sky'), (T('Wed', 'Rabu'), 30, 'mint'), (T('Thu', 'Khamis'), 12, 'sun'), (T('Fri', 'Jumaat'), 36, 'grape')], ('mean',), T('ships', 'kapal'))])
    add(10, 'reasoning', 'multi-step', 'master', 'lighthouse',
        T('Clock Tower Finale', 'Kemuncak Menara Jam'),
        T('The great clock tower is about to chime! Solve three steps to set every clock right.', 'Menara jam besar hampir berbunyi! Selesaikan tiga langkah untuk menetapkan setiap jam dengan betul.'),
        T('Multi-step problems with time and money.', 'Masalah berbilang langkah dengan masa dan wang.'),
        'Chimey', T('Chimey sings when every clock agrees.', 'Chimey menyanyi apabila semua jam sepakat.'),
        [steps([step(T('A clock chimes every 15 minutes. How many chimes in 1 hour?', 'Sebuah jam berbunyi setiap 15 minit. Berapa kali ia berbunyi dalam 1 jam?'), 4, '60/15'),
                step(T('How many chimes in 6 hours?', 'Berapa kali ia berbunyi dalam 6 jam?'), 24, '4*6'),
                step(T('Each chime needs 2 minutes of oil. How many minutes of oil in total?', 'Setiap bunyi memerlukan 2 minit minyak. Berapa minit minyak kesemuanya?'), 48, '24*2')],
               T('There are 60 minutes in an hour.', 'Terdapat 60 minit dalam satu jam.'), T('60 ÷ 15 = 4, then 4 × 6 = 24, then 24 × 2 = 48.', '60 ÷ 15 = 4, kemudian 4 × 6 = 24, kemudian 24 × 2 = 48.'), 'ch10a'),
         steps([step(T('A watch loses 3 minutes every day. How many minutes does it lose in 14 days?', 'Sebuah jam tangan kehilangan 3 minit setiap hari. Berapa minit ia hilang dalam 14 hari?'), 42, '3*14'),
                step(T('The watchmaker adds back 30 minutes. How many minutes is the watch still behind?', 'Pembuat jam menambah semula 30 minit. Berapa minit jam tangan itu masih ketinggalan?'), 12, '42-30'),
                step(T('Repairs cost RM5 for each minute behind. How much is the repair?', 'Pembaikan berharga RM5 untuk setiap minit ketinggalan. Berapa harga pembaikan itu?'), 60, '12*5', lambda v: f'RM{v}')],
               T('Multiply first, then subtract.', 'Darab dahulu, kemudian tolak.'), T('3 × 14 = 42, then 42 − 30 = 12, then 12 × 5 = 60.', '3 × 14 = 42, kemudian 42 − 30 = 12, kemudian 12 × 5 = 60.'), 'ch10b'),
         steps([step(T('A ship sails for 3 hours and 30 minutes. How many minutes is that?', 'Sebuah kapal belayar selama 3 jam 30 minit. Berapa minit itu?'), 210, '3*60+30'),
                step(T('It sails 2 km every 15 minutes. How many 15-minute parts are in the trip?', 'Ia belayar 2 km setiap 15 minit. Berapa bahagian 15 minit dalam perjalanan itu?'), 14, '210/15'),
                step(T('How many kilometres does the ship sail?', 'Berapa kilometer kapal itu belayar?'), 28, '14*2')],
               T('Change hours to minutes first.', 'Tukar jam kepada minit dahulu.'), T('3 × 60 + 30 = 210, then 210 ÷ 15 = 14, then 14 × 2 = 28.', '3 × 60 + 30 = 210, kemudian 210 ÷ 15 = 14, kemudian 14 × 2 = 28.'), 'ch10c')])
    return L
