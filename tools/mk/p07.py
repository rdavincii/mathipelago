from lib import *
CODE, BASE = 'dd', 72
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'decimals', 'adventurer', 'door',
        T('Sand Fractions', 'Pecahan Pasir'),
        T('The dune scribes write the same amount as a fraction and as a decimal. Match them!', 'Jurutulis bukit pasir menulis jumlah yang sama sebagai pecahan dan perpuluhan. Padankan mereka!'),
        T('Match tenths and hundredths to decimals.', 'Memadankan persepuluh dan perseratus dengan perpuluhan.'),
        'Dusty', T('Dusty writes in the sand with his tail.', 'Dusty menulis di atas pasir dengan ekornya.'),
        [match([('1/10', '0.1'), ('3/10', '0.3'), ('7/10', '0.7')], MP_, T('1/10 is 0.1, so 3/10 is 0.3.', '1/10 ialah 0.1, jadi 3/10 ialah 0.3.')),
         match([('1/2', '0.5'), ('1/4', '0.25'), ('3/4', '0.75'), ('9/10', '0.9')], MP_, T('1/2 is 5/10, which is 0.5.', '1/2 ialah 5/10, iaitu 0.5.')),
         match([('1/100', '0.01'), ('7/100', '0.07'), ('25/100', '0.25'), ('2/5', '0.4'), ('3/5', '0.6')], MP_, T('Make the bottom 10 or 100 first.', 'Jadikan penyebut 10 atau 100 dahulu.'))])
    add(2, 'number-sense', 'place-value', 'adventurer', 'bridge',
        T('Dune Line', 'Garis Bukit'),
        T('Slide the camel to the right place on the dune line!', 'Gelongsorkan unta ke tempat yang betul pada garis bukit!'),
        T('Place numbers on a line in tens and fifties.', 'Meletakkan nombor pada garis dalam puluh dan lima puluh.'),
        'Camby', T('Camby walks the whole line without stopping.', 'Camby berjalan sepanjang garis tanpa berhenti.'),
        [numberline(60, 0, 100, 10, 20), numberline(350, 0, 500, 50, 100), numberline(750, 500, 1000, 50, 250, kind='half', a=600, b=900)])
    add(3, 'operations', 'money', 'adventurer', 'chest',
        T('Oasis Shop', 'Kedai Oasis'),
        T('The oasis shop sells cool drinks. Pay for each one with exact coins!', 'Kedai oasis menjual minuman sejuk. Bayar setiap satu dengan syiling yang tepat!'),
        T('Make exact amounts of money in sen.', 'Membentuk jumlah wang yang tepat dalam sen.'),
        'Sipper', T('Sipper loves every cold drink.', 'Sipper sukakan setiap minuman sejuk.'),
        [coins(70, [5, 10, 20, 50]), coins(135, [5, 10, 20, 50, 100]), coins(385, [5, 10, 20, 50, 100], 7)])
    add(4, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Camel Caravan', 'Kafilah Unta'),
        T('The camels walk in a caravan with a pattern. How far will the next one be?', 'Unta berjalan dalam kafilah mengikut pola. Berapa jauh unta yang seterusnya?'),
        T('Continue patterns with bigger steps.', 'Menyambung pola dengan langkah yang lebih besar.'),
        'Humphrey', T('Humphrey leads the caravan with a swagger.', 'Humphrey mengetuai kafilah dengan bergaya.'),
        [pattern('arith', 100, 50, 5, seed='dd4a'), pattern('arith', 20, 15, 5, seed='dd4b'), pattern('arith', 900, -75, 6, hidden=3, seed='dd4c')])
    add(5, 'number-sense', 'fractions', 'adventurer', 'tank',
        T('Water Skin', 'Kantung Air'),
        T('Fill each water skin to the right line before the caravan leaves!', 'Isi setiap kantung air hingga garisan yang betul sebelum kafilah bertolak!'),
        T('Fractions of a container.', 'Pecahan sebuah bekas.'),
        'Splashy', T('Splashy hates a dry day.', 'Splashy bencikan hari yang kering.'),
        [tank(10, 1, 2), tank(10, 7, 10), tank(8, 5, 8)])
    add(6, 'operations', 'sharing', 'adventurer', 'picnic',
        T('Date Share', 'Kongsi Kurma'),
        T('The travellers share their dates. Everyone must get the same number!', 'Para pengembara berkongsi kurma mereka. Semua orang mesti mendapat bilangan yang sama!'),
        T('Share equally using division facts.', 'Berkongsi sama banyak menggunakan fakta bahagi.'),
        'Datey', T('Datey saves the stones in a pocket.', 'Datey menyimpan biji kurma dalam poket.'),
        [share(15, 3), share(24, 4), share(30, 5)])
    add(7, 'number-sense', 'decimals', 'master', 'gears',
        T('Decimal Doors', 'Pintu Perpuluhan'),
        T('Each stone door opens when you match the decimal to the money or the length it stands for!', 'Setiap pintu batu terbuka apabila anda memadankan perpuluhan dengan wang atau panjang yang diwakilinya!'),
        T('Link decimals with money and metres.', 'Menghubungkan perpuluhan dengan wang dan meter.'),
        'Pointy', T('Pointy always stands at the dot.', 'Pointy sentiasa berdiri di titik itu.'),
        [match([('RM1.50', '150 sen'), ('RM2.00', '200 sen'), ('RM0.75', '75 sen')], MP_, T('RM1 is 100 sen.', 'RM1 ialah 100 sen.')),
         match([('1.5 m', '150 cm'), ('2.5 m', '250 cm'), ('0.5 m', '50 cm'), ('3.2 m', '320 cm')], MP_, T('1 m is 100 cm.', '1 m ialah 100 cm.')),
         match([('0.5 kg', '500 g'), ('1.2 kg', '1200 g'), ('2.5 kg', '2500 g'), ('0.25 L', '250 mL'), ('1.5 L', '1500 mL')], MP_, T('1 kg is 1000 g and 1 L is 1000 mL.', '1 kg ialah 1000 g dan 1 L ialah 1000 mL.'))])
    add(8, 'operations', 'times-tables', 'master', 'door',
        T('Sand Bags', 'Beg Pasir'),
        T('Sand is packed into equal bags. Find the two tiles that make each total!', 'Pasir dipek dalam beg yang sama saiz. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Grainy', T('Grainy counts every grain, or tries to.', 'Grainy mengira setiap butir, atau cuba mengiranya.'),
        [tiles(48, [6, 8, 4, 12, 3, 9]), tiles(84, [7, 12, 6, 14, 8, 9]), tiles(132, [11, 12, 9, 8, 13, 10])])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Desert Chart', 'Carta Gurun'),
        T('The explorers charted the heat of each day. Read the chart!', 'Para penjelajah mencatat kepanasan setiap hari. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Sunny', T('Sunny wears sunglasses all day.', 'Sunny memakai cermin mata hitam sepanjang hari.'),
        [chart([(T('Mon', 'Isnin'), 32, 'coral'), (T('Tue', 'Selasa'), 38, 'sun'), (T('Wed', 'Rabu'), 35, 'mint')], ('diff', 1, 0), T('degrees', 'darjah')),
         chart([(T('Mon', 'Isnin'), 30, 'coral'), (T('Tue', 'Selasa'), 36, 'sun'), (T('Wed', 'Rabu'), 40, 'mint'), (T('Thu', 'Khamis'), 34, 'sky')], ('sum', [0, 1]), T('degrees', 'darjah')),
         chart([(T('Mon', 'Isnin'), 28, 'coral'), (T('Tue', 'Selasa'), 34, 'sun'), (T('Wed', 'Rabu'), 40, 'mint'), (T('Thu', 'Khamis'), 36, 'sky'), (T('Fri', 'Jumaat'), 32, 'grape')], ('mean',), T('degrees', 'darjah'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Oasis Finale', 'Kemuncak Oasis'),
        T('Reach the oasis by solving three-step problems about the long desert road!', 'Sampai ke oasis dengan menyelesaikan masalah tiga langkah tentang jalan gurun yang panjang!'),
        T('Multi-step problems with distance, money and sharing.', 'Masalah berbilang langkah dengan jarak, wang dan perkongsian.'),
        'Mirage', T('Mirage is never quite where you see it.', 'Mirage tidak pernah betul-betul di tempat anda melihatnya.'),
        [steps([step(T('A caravan walks 18 km each day. How many km in 5 days?', 'Sebuah kafilah berjalan 18 km setiap hari. Berapa km dalam 5 hari?'), 90, '18*5', lambda v: f'{v} km'),
                step(T('The oasis is 120 km away. How many km are still left?', 'Oasis berada 120 km jauhnya. Berapa km yang masih tinggal?'), 30, '120-90', lambda v: f'{v} km'),
                step(T('They walk the rest in 3 equal days. How many km each day?', 'Mereka berjalan baki itu dalam 3 hari yang sama. Berapa km setiap hari?'), 10, '30/3', lambda v: f'{v} km')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('18 × 5 = 90, then 120 − 90 = 30, then 30 ÷ 3 = 10.', '18 × 5 = 90, kemudian 120 − 90 = 30, kemudian 30 ÷ 3 = 10.'), 'dd10a'),
         steps([step(T('Each camel drinks 8 litres a day. How many litres do 6 camels drink?', 'Setiap unta minum 8 liter sehari. Berapa liter diminum oleh 6 ekor unta?'), 48, '6*8', lambda v: f'{v} L'),
                step(T('The caravan has 100 litres. How many litres are left after one day?', 'Kafilah ada 100 liter. Berapa liter yang tinggal selepas sehari?'), 52, '100-48', lambda v: f'{v} L'),
                step(T('The well gives 20 litres more. How many litres now?', 'Perigi memberi 20 liter lagi. Berapa liter sekarang?'), 72, '52+20', lambda v: f'{v} L')],
               T('Find the drinking first.', 'Cari jumlah minuman dahulu.'), T('6 × 8 = 48, then 100 − 48 = 52, then 52 + 20 = 72.', '6 × 8 = 48, kemudian 100 − 48 = 52, kemudian 52 + 20 = 72.'), 'dd10b'),
         steps([step(T('A rug costs RM15. What do 4 rugs cost?', 'Sehelai permaidani berharga RM15. Berapa harga 4 helai?'), 60, '4*15', RM),
                step(T('A lamp costs RM25. What is the total for the rugs and the lamp?', 'Sebuah lampu berharga RM25. Berapa jumlah untuk permaidani dan lampu itu?'), 85, '60+25', RM),
                step(T('You pay with RM100. How much change do you get?', 'Anda membayar dengan RM100. Berapa baki yang anda terima?'), 15, '100-85', RM)],
               T('Add the costs, then take them from RM100.', 'Tambah harga, kemudian tolak daripada RM100.'), T('4 × 15 = 60, then 60 + 25 = 85, then 100 − 85 = 15.', '4 × 15 = 60, kemudian 60 + 25 = 85, kemudian 100 − 85 = 15.'), 'dd10c')])
    return L
