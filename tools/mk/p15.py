from lib import *
CODE, BASE = 'dv', 152
MP_ = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'number-sense', 'place-value', 'adventurer', 'door',
        T('Egg Counts', 'Kiraan Telur'),
        T('The dino nest holds thousands of eggs. Build each number on the stone lock!', 'Sarang dinosaur menyimpan ribuan telur. Bina setiap nombor pada kunci batu!'),
        T('Build numbers up to 9,999 with place value.', 'Membina nombor sehingga 9,999 dengan nilai tempat.'),
        'Eggy', T('Eggy guards the nest day and night.', 'Eggy menjaga sarang siang dan malam.'),
        [placevalue(340, [100, 10, 1]), placevalue(1205, [1000, 100, 10, 1]), placevalue(6482, [1000, 100, 10, 1])])
    add(2, 'number-sense', 'place-value', 'adventurer', 'gears',
        T('Bone Numbers', 'Nombor Tulang'),
        T('The diggers found number bones. Arrange them to make the smallest or the biggest number!', 'Penggali menjumpai tulang bernombor. Susun untuk membentuk nombor terkecil atau terbesar!'),
        T('Order digits to make the largest or smallest number.', 'Menyusun digit untuk membentuk nombor terbesar atau terkecil.'),
        'Bonesy', T('Bonesy buries a bone at every dig.', 'Bonesy menanam tulang di setiap penggalian.'),
        [digitarrange([4, 9, 2], 'smallest'), digitarrange([3, 0, 7, 5], 'largest'), digitarrange([8, 2, 0, 6], 'smallest')])
    add(3, 'number-sense', 'rounding', 'adventurer', 'bridge',
        T('Round the Rocks', 'Bundarkan Batu'),
        T('The rock counts are rounded to make them easy to read. Slide the marker to the rounded number!', 'Bilangan batu dibundarkan supaya mudah dibaca. Gelongsorkan penanda ke nombor yang dibundarkan!'),
        T('Round to the nearest 10, 100 and 1,000.', 'Membundarkan kepada 10, 100 dan 1,000 yang terdekat.'),
        'Pebble', T('Pebble is the roundest rock in the valley.', 'Pebble ialah batu paling bulat di lembah itu.'),
        [numberline(60, 0, 100, 10, 20, kind='round', x=64, unit='10'), numberline(500, 0, 1000, 100, 200, kind='round', x=462, unit='100'), numberline(2000, 0, 5000, 500, 1000, kind='round', x=2380, unit='1000')])
    add(4, 'number-sense', 'number-line', 'adventurer', 'lanterns',
        T('Fossil Line', 'Garis Fosil'),
        T('Fossils are lined up along a path in hundreds and thousands. Slide the marker to the right fossil!', 'Fosil disusun di sepanjang laluan dalam ratus dan ribu. Gelongsorkan penanda ke fosil yang betul!'),
        T('Place numbers on a line in hundreds and thousands.', 'Meletakkan nombor pada garis dalam ratus dan ribu.'),
        'Fossy', T('Fossy hums a tune from long ago.', 'Fossy menyanyikan lagu dari zaman dahulu.'),
        [numberline(600, 0, 1000, 100, 200), numberline(3500, 0, 5000, 500, 1000), numberline(5000, 0, 10000, 500, 2500, kind='half', a=2000, b=8000)])
    add(5, 'number-sense', 'length', 'adventurer', 'ferry',
        T('Dino Lengths', 'Panjang Dinosaur'),
        T('Dinosaur sizes are written in different units. Match each size to the same size in another unit!', 'Saiz dinosaur ditulis dalam unit yang berbeza. Padankan setiap saiz dengan saiz yang sama dalam unit lain!'),
        T('Convert metres, kilometres, kilograms and litres.', 'Menukar meter, kilometer, kilogram dan liter.'),
        'Metrex', T('Metrex measures everything twice.', 'Metrex mengukur segalanya dua kali.'),
        [match([('3 m', '300 cm'), ('5 m', '500 cm'), ('2 m', '200 cm')], MP_, T('There are 100 centimetres in 1 metre.', 'Terdapat 100 sentimeter dalam 1 meter.')),
         match([('2 km', '2000 m'), ('6 km', '6000 m'), ('700 cm', '7 m'), ('4000 m', '4 km')], MP_, T('There are 1000 metres in 1 kilometre.', 'Terdapat 1000 meter dalam 1 kilometer.')),
         match([('5 kg', '5000 g'), ('3 L', '3000 mL'), ('2500 m', '2.5 km'), ('4500 g', '4.5 kg'), ('1500 mL', '1.5 L')], MP_, T('Multiply by 1000 to go to the smaller unit.', 'Darab dengan 1000 untuk menukar kepada unit yang lebih kecil.'))])
    add(6, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Footprint Trail', 'Jejak Tapak Kaki'),
        T('Giant footprints go across the valley in a pattern. Which number comes next?', 'Tapak kaki gergasi melintasi lembah dalam satu pola. Nombor manakah yang seterusnya?'),
        T('Continue patterns that grow, shrink or multiply.', 'Menyambung pola yang bertambah, berkurang atau berganda.'),
        'Stompy', T('Stompy makes the ground shake with every step.', 'Stompy menggegarkan tanah pada setiap langkah.'),
        [pattern('arith', 150, 50, 5, seed='dv6a'), pattern('geo', 3, 2, 5, seed='dv6b'), pattern('arith', 2000, -250, 6, hidden=3, seed='dv6c')])
    add(7, 'operations', 'times-tables', 'master', 'picnic',
        T('Egg Nests', 'Sarang Telur'),
        T('Every nest holds the same number of eggs. Find the two tiles that make each total!', 'Setiap sarang memuatkan bilangan telur yang sama. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Nesty', T('Nesty fluffs up every nest until it is perfect.', 'Nesty memberi seri pada setiap sarang sehingga sempurna.'),
        [tiles(54, [6, 9, 7, 8, 3, 12]), tiles(96, [8, 12, 5, 7, 9, 11]), tiles(144, [9, 16, 7, 5, 11, 13])])
    add(8, 'operations', 'money', 'master', 'chest',
        T('Fossil Shop', 'Kedai Fosil'),
        T('The fossil shop sells shiny bones and shells. Pay each price with exactly the right coins!', 'Kedai fosil menjual tulang dan kulit kerang yang berkilau. Bayar setiap harga dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Shelly', T('Shelly collects the shiniest shells.', 'Shelly mengumpul kulit kerang yang paling berkilau.'),
        [coins(135, [5, 10, 20, 50, 100]), coins(260, [10, 20, 50, 100]), coins(485, [5, 10, 20, 50, 100], 8)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Dino Count', 'Bilangan Dinosaur'),
        T('The rangers counted the dinosaurs they spotted in the valley. Read the chart!', 'Renjer mengira dinosaur yang mereka nampak di lembah. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Tallyrex', T('Tallyrex never loses count of a dinosaur.', 'Tallyrex tidak pernah tersilap mengira dinosaur.'),
        [chart([(T('T-Rex', 'T-Rex'), 14, 'coral'), (T('Raptors', 'Raptor'), 9, 'sun'), (T('Stegos', 'Stego'), 12, 'mint')], ('diff', 0, 1), T('dinosaurs', 'dinosaur')),
         chart([(T('T-Rex', 'T-Rex'), 18, 'coral'), (T('Raptors', 'Raptor'), 26, 'sun'), (T('Stegos', 'Stego'), 12, 'mint'), (T('Brontos', 'Bronto'), 24, 'sky')], ('sum', [1, 3]), T('dinosaurs', 'dinosaur')),
         chart([(T('T-Rex', 'T-Rex'), 30, 'coral'), (T('Raptors', 'Raptor'), 45, 'sun'), (T('Stegos', 'Stego'), 25, 'mint'), (T('Bronto', 'Bronto'), 60, 'sky'), (T('Trikes', 'Trike'), 40, 'grape')], ('mean',), T('dinosaurs', 'dinosaur'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Valley Finale', 'Kemuncak Lembah'),
        T('The last egg is about to hatch! Solve three-step problems to welcome the baby dinosaur.', 'Telur terakhir hampir menetas! Selesaikan masalah tiga langkah untuk menyambut anak dinosaur.'),
        T('Multi-step problems with eggs, lengths and money.', 'Masalah berbilang langkah dengan telur, panjang dan wang.'),
        'Rexy', T('Rexy roars very softly, just in case.', 'Rexy mengaum dengan sangat perlahan, untuk berjaga-jaga.'),
        [steps([step(T('A nest holds 8 eggs. How many eggs are in 7 nests?', 'Sebuah sarang memuatkan 8 telur. Berapa telur dalam 7 sarang?'), 56, '8*7'),
                step(T('12 eggs crack by accident. How many eggs are left?', '12 telur pecah secara tidak sengaja. Berapa telur yang tinggal?'), 44, '56-12'),
                step(T('The rest are shared equally by 4 caretakers. How many eggs does each caretaker get?', 'Baki itu dikongsi sama banyak oleh 4 penjaga. Berapa telur yang diperoleh setiap penjaga?'), 11, '44/4')],
               T('Multiply, then subtract, then share.', 'Darab, kemudian tolak, kemudian kongsi.'), T('8 × 7 = 56, then 56 − 12 = 44, then 44 ÷ 4 = 11.', '8 × 7 = 56, kemudian 56 − 12 = 44, kemudian 44 ÷ 4 = 11.'), 'dv10a'),
         steps([step(T('An adult dinosaur is 12 m long. Its baby is a quarter as long. How many metres is the baby?', 'Seekor dinosaur dewasa sepanjang 12 m. Anaknya sepanjang suku daripadanya. Berapa meter panjang anak itu?'), 3, '12/4', lambda v: f'{v} m'),
                step(T('The baby grows 2 m every year. How many metres does it grow in 5 years?', 'Anak itu membesar 2 m setiap tahun. Berapa meter ia membesar dalam 5 tahun?'), 10, '2*5', lambda v: f'{v} m'),
                step(T('How many metres long is the dinosaur after 5 years?', 'Berapa meter panjang dinosaur itu selepas 5 tahun?'), 13, '3+10', lambda v: f'{v} m')],
               T('A quarter means divide by 4.', 'Suku bermaksud bahagi dengan 4.'), T('12 ÷ 4 = 3, then 2 × 5 = 10, then 3 + 10 = 13.', '12 ÷ 4 = 3, kemudian 2 × 5 = 10, kemudian 3 + 10 = 13.'), 'dv10b'),
         steps([step(T('A museum ticket costs RM12. What do 15 tickets cost?', 'Tiket muzium berharga RM12. Berapa harga 15 tiket?'), 180, '15*12', RM),
                step(T('The school gets RM30 off. How much does it pay?', 'Sekolah mendapat potongan RM30. Berapa yang dibayarnya?'), 150, '180-30', RM),
                step(T('The teacher pays with RM200. How much change does she get?', 'Guru membayar dengan RM200. Berapa baki yang diterimanya?'), 50, '200-150', RM)],
               T('Multiply first, then take off the discount.', 'Darab dahulu, kemudian tolak potongan.'), T('15 × 12 = 180, then 180 − 30 = 150, then 200 − 150 = 50.', '15 × 12 = 180, kemudian 180 − 30 = 150, kemudian 200 − 150 = 50.'), 'dv10c')])
    return L
