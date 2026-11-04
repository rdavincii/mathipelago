from lib import *
CODE, BASE = 'ss', 102
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'place-value', 'adventurer', 'door',
        T('Launch Codes', 'Kod Pelancaran'),
        T('The rocket will not launch without the right code. Build each number on the lock!', 'Roket tidak akan dilancarkan tanpa kod yang betul. Bina setiap nombor pada kunci!'),
        T('Build large numbers with place value.', 'Membina nombor besar dengan nilai tempat.'),
        'Rocky', T('Rocky counts down from ten, every time.', 'Rocky mengira detik dari sepuluh, setiap kali.'),
        [placevalue(840, [100, 10, 1]), placevalue(4205, [1000, 100, 10, 1]), placevalue(9730, [1000, 100, 10, 1])])
    add(2, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Star Patterns', 'Corak Bintang'),
        T('Stars blink in a pattern. How many blinks come next?', 'Bintang berkelip dalam satu pola. Berapa kelipan yang datang seterusnya?'),
        T('Continue number patterns.', 'Menyambung pola nombor.'),
        'Twinkly', T('Twinkly blinks once for every star.', 'Twinkly berkelip sekali untuk setiap bintang.'),
        [pattern('arith', 11, 11, 5, seed='ss2a'), pattern('geo', 3, 3, 5, seed='ss2b'), pattern('arith', 500, 250, 6, hidden=3, seed='ss2c')])
    add(3, 'number-sense', 'length', 'adventurer', 'bridge',
        T('Orbit Line', 'Garis Orbit'),
        T('Place each planet at the right distance along the orbit line!', 'Letakkan setiap planet pada jarak yang betul di sepanjang garis orbit!'),
        T('Place numbers on a line in hundreds and thousands.', 'Meletakkan nombor pada garis dalam ratus dan ribu.'),
        'Orbit', T('Orbit goes round and round in the same path.', 'Orbit berpusing dalam laluan yang sama.'),
        [numberline(400, 0, 1000, 100, 200), numberline(3000, 0, 5000, 500, 1000), numberline(7500, 5000, 10000, 500, 2500, kind='half', a=6000, b=9000)])
    add(4, 'operations', 'times-tables', 'adventurer', 'gears',
        T('Rocket Crates', 'Peti Roket'),
        T('The rocket carries crates of equal size. Find the two tiles that make each total!', 'Roket membawa peti yang sama saiz. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Crater', T('Crater is full of dents and good stories.', 'Crater penuh dengan lekuk dan cerita yang menarik.'),
        [tiles(56, [7, 8, 6, 9, 4, 14]), tiles(105, [15, 7, 5, 21, 9, 12]), tiles(168, [12, 14, 8, 21, 7, 16])])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Fuel Tank', 'Tangki Bahan Api'),
        T('Fill each fuel tank to the right line before launch!', 'Isi setiap tangki bahan api hingga garisan yang betul sebelum pelancaran!'),
        T('Fractions of a tank.', 'Pecahan sebuah tangki.'),
        'Fuely', T('Fuely hums when the tank is full.', 'Fuely berdengung apabila tangki penuh.'),
        [tank(12, 1, 4), tank(10, 9, 10), tank(12, 7, 12)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Space Snacks', 'Snek Angkasa'),
        T('Share the space snacks between the crew. Everyone gets the same!', 'Kongsi snek angkasa antara kru. Semua orang mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Snacky', T('Snacky floats after every meal.', 'Snacky terapung selepas setiap hidangan.'),
        [share(15, 5), share(24, 4), share(30, 3)])
    add(7, 'number-sense', 'decimals', 'master', 'door',
        T('Planet Pairs', 'Pasangan Planet'),
        T('Match each distance to the same distance in other units!', 'Padankan setiap jarak dengan jarak yang sama dalam unit lain!'),
        T('Convert kilometres and metres.', 'Menukar kilometer dan meter.'),
        'Planty', T('Planty waters tiny space gardens.', 'Planty menyiram taman angkasa kecil.'),
        [match([('1 km', '1000 m'), ('3 km', '3000 m'), ('5 km', '5000 m')], MP_, T('1 km is 1000 m.', '1 km ialah 1000 m.')),
         match([('2.5 km', '2500 m'), ('1.5 km', '1500 m'), ('0.5 km', '500 m'), ('4000 m', '4 km')], MP_, T('Half a kilometre is 500 m.', 'Setengah kilometer ialah 500 m.')),
         match([('6.5 km', '6500 m'), ('0.2 km', '200 m'), ('3.4 km', '3400 m'), ('8000 m', '8 km'), ('7500 m', '7.5 km')], MP_, T('Multiply by 1000 to change km into m.', 'Darab dengan 1000 untuk menukar km kepada m.'))])
    add(8, 'operations', 'money', 'master', 'chest',
        T('Moon Market', 'Pasar Bulan'),
        T('The moon market uses small coins. Pay each price exactly!', 'Pasar bulan menggunakan syiling kecil. Bayar setiap harga dengan tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Lunar', T('Lunar hops very high on the moon.', 'Lunar melompat sangat tinggi di bulan.'),
        [coins(115, [5, 10, 20, 50]), coins(290, [10, 20, 50, 100]), coins(545, [5, 10, 20, 50, 100], 8)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Star Chart', 'Carta Bintang'),
        T('The astronomers counted the stars they saw each night. Read the chart!', 'Ahli astronomi mengira bintang yang mereka lihat setiap malam. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Stargaze', T('Stargaze never blinks at night.', 'Stargaze tidak pernah berkelip pada waktu malam.'),
        [chart([(T('Mon', 'Isnin'), 40, 'grape'), (T('Tue', 'Selasa'), 25, 'sky'), (T('Wed', 'Rabu'), 35, 'sun')], ('diff', 0, 1), T('stars', 'bintang')),
         chart([(T('Mon', 'Isnin'), 30, 'grape'), (T('Tue', 'Selasa'), 45, 'sky'), (T('Wed', 'Rabu'), 20, 'sun'), (T('Thu', 'Khamis'), 55, 'mint')], ('sum', [0, 1, 2, 3]), T('stars', 'bintang')),
         chart([(T('Mon', 'Isnin'), 20, 'grape'), (T('Tue', 'Selasa'), 50, 'sky'), (T('Wed', 'Rabu'), 35, 'sun'), (T('Thu', 'Khamis'), 45, 'mint'), (T('Fri', 'Jumaat'), 30, 'coral')], ('mean',), T('stars', 'bintang'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Mission Finale', 'Kemuncak Misi'),
        T('Mission control needs you for the final launch! Solve the three-step problems.', 'Kawalan misi memerlukan anda untuk pelancaran terakhir! Selesaikan masalah tiga langkah itu.'),
        T('Multi-step problems with time, distance and sharing.', 'Masalah berbilang langkah dengan masa, jarak dan perkongsian.'),
        'Nova Jr', T('Nova Jr dreams of flying to every island.', 'Nova Jr bermimpi untuk terbang ke setiap pulau.'),
        [steps([step(T('A rocket flies 400 km every minute. How many km in 6 minutes?', 'Sebuah roket terbang 400 km setiap minit. Berapa km dalam 6 minit?'), 2400, '400*6', lambda v: f'{v} km'),
                step(T('The moon is 3000 km away. How many km are still to go?', 'Bulan berada 3000 km jauhnya. Berapa km lagi yang perlu dilalui?'), 600, '3000-2400', lambda v: f'{v} km'),
                step(T('The rocket flies the rest in 3 equal parts. How many km in each part?', 'Roket terbang baki itu dalam 3 bahagian yang sama. Berapa km dalam setiap bahagian?'), 200, '600/3', lambda v: f'{v} km')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('400 × 6 = 2,400, then 3,000 − 2,400 = 600, then 600 ÷ 3 = 200.', '400 × 6 = 2,400, kemudian 3,000 − 2,400 = 600, kemudian 600 ÷ 3 = 200.'), 'ss10a'),
         steps([step(T('A crew of 8 astronauts each needs 3 meals a day. How many meals a day?', 'Sebuah kru yang terdiri daripada 8 angkasawan masing-masing memerlukan 3 hidangan sehari. Berapa hidangan sehari?'), 24, '8*3'),
                step(T('The trip lasts 5 days. How many meals for the whole trip?', 'Perjalanan itu berlangsung selama 5 hari. Berapa hidangan untuk keseluruhan perjalanan?'), 120, '24*5'),
                step(T('The ship carries 150 meals. How many spare meals are there?', 'Kapal itu membawa 150 hidangan. Berapa hidangan simpanan yang ada?'), 30, '150-120')],
               T('Find the meals for one day first.', 'Cari hidangan untuk satu hari dahulu.'), T('8 × 3 = 24, then 24 × 5 = 120, then 150 − 120 = 30.', '8 × 3 = 24, kemudian 24 × 5 = 120, kemudian 150 − 120 = 30.'), 'ss10b'),
         steps([step(T('A space station orbits the planet 16 times a day. How many orbits in 7 days?', 'Sebuah stesen angkasa mengorbit planet 16 kali sehari. Berapa orbit dalam 7 hari?'), 112, '16*7'),
                step(T('A solar panel makes 5 units of power on each orbit. How many units of power?', 'Panel solar menghasilkan 5 unit kuasa pada setiap orbit. Berapa unit kuasa?'), 560, '112*5'),
                step(T('The station uses 260 units. How many units are left?', 'Stesen itu menggunakan 260 unit. Berapa unit yang tinggal?'), 300, '560-260')],
               T('Orbits first, then power.', 'Orbit dahulu, kemudian kuasa.'), T('16 × 7 = 112, then 112 × 5 = 560, then 560 − 260 = 300.', '16 × 7 = 112, kemudian 112 × 5 = 560, kemudian 560 − 260 = 300.'), 'ss10c')])
    return L
