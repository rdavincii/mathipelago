from lib import *

def crystal():
    """Crystal Caves levels 7..10 (orders 19..22), appended to the hand-written first six."""
    L = []
    def add(i, *a): L.append(level('c1', i, 18 + i - 6, *a))
    add(7, 'number-sense', 'fractions', 'master', 'door',
        T('Twin Crystals', 'Kristal Kembar'),
        T('Every crystal has a twin that looks different but is worth the same. Pair them up!', 'Setiap kristal mempunyai kembar yang kelihatan berbeza tetapi sama nilainya. Padankan mereka!'),
        T('Match equivalent fractions.', 'Memadankan pecahan setara.'),
        'Twinkle', T('Twinkle always shows up in pairs.', 'Twinkle sentiasa muncul berpasangan.'),
        [match([('1/2', '2/4'), ('1/3', '2/6'), ('3/4', '6/8')], T('Tap a fraction, then tap the fraction that is equal to it.', 'Ketik satu pecahan, kemudian ketik pecahan yang sama nilainya.'), T('Multiply the top and the bottom by the same number.', 'Darabkan atas dan bawah dengan nombor yang sama.')),
         match([('2/3', '4/6'), ('1/4', '3/12'), ('5/10', '1/2'), ('3/5', '6/10')], T('Tap a fraction, then tap the fraction that is equal to it.', 'Ketik satu pecahan, kemudian ketik pecahan yang sama nilainya.'), T('Multiply the top and the bottom by the same number.', 'Darabkan atas dan bawah dengan nombor yang sama.')),
         match([('2/8', '1/4'), ('6/8', '3/4'), ('4/10', '2/5'), ('3/9', '1/3'), ('10/15', '2/3')], T('Tap a fraction, then tap the fraction that is equal to it.', 'Ketik satu pecahan, kemudian ketik pecahan yang sama nilainya.'), T('Divide the top and the bottom by the same number to make it simpler.', 'Bahagikan atas dan bawah dengan nombor yang sama untuk memudahkannya.'))])
    add(8, 'operations', 'fractions', 'master', 'picnic',
        T('Gem Shares', 'Perkongsian Permata'),
        T('The miners share the gems in fractions. Work out how many each group gets!', 'Para pelombong berkongsi permata dalam pecahan. Kira berapa banyak yang diperoleh setiap kumpulan!'),
        T('Find a fraction of an amount, then keep going in steps.', 'Mencari pecahan bagi suatu jumlah, kemudian meneruskan langkah demi langkah.'),
        'Shardy', T('Shardy counts gems into neat piles.', 'Shardy mengira permata menjadi longgokan yang kemas.'),
        [steps([step(T('A box holds 12 gems. Half of them are pink. How many pink gems?', 'Sebuah kotak mengandungi 12 permata. Separuh daripadanya berwarna merah jambu. Berapa permata merah jambu?'), 6, '12/2'),
                step(T('3 more pink gems are found. How many pink gems now?', '3 lagi permata merah jambu dijumpai. Berapa permata merah jambu sekarang?'), 9, '6+3'),
                step(T('Share them equally into 3 pouches. How many in each pouch?', 'Kongsi sama banyak ke dalam 3 uncang. Berapa dalam setiap uncang?'), 3, '9/3')],
               T('Half means divide by 2. Then add, then share.', 'Separuh bermaksud bahagi dengan 2. Kemudian tambah, kemudian kongsi.'), T('12 ÷ 2 = 6, then 6 + 3 = 9, then 9 ÷ 3 = 3.', '12 ÷ 2 = 6, kemudian 6 + 3 = 9, kemudian 9 ÷ 3 = 3.'), 'c1-8a'),
         steps([step(T('A box holds 20 gems. A quarter of them are blue. How many blue gems?', 'Sebuah kotak mengandungi 20 permata. Suku daripadanya berwarna biru. Berapa permata biru?'), 5, '20/4'),
                step(T('Another box has 3 times as many blue gems. How many is that?', 'Sebuah kotak lain mempunyai 3 kali ganda permata biru. Berapa banyak?'), 15, '5*3'),
                step(T('How many blue gems are there in both boxes together?', 'Berapa permata biru dalam kedua-dua kotak jika digabungkan?'), 20, '5+15')],
               T('A quarter means divide by 4.', 'Suku bermaksud bahagi dengan 4.'), T('20 ÷ 4 = 5, then 5 × 3 = 15, then 5 + 15 = 20.', '20 ÷ 4 = 5, kemudian 5 × 3 = 15, kemudian 5 + 15 = 20.'), 'c1-8b'),
         steps([step(T('A chest has 60 gems. Two thirds of them are green. How many green gems?', 'Sebuah peti mempunyai 60 permata. Dua pertiga daripadanya berwarna hijau. Berapa permata hijau?'), 40, '60/3*2'),
                step(T('10 green gems are sold. How many green gems are left?', '10 permata hijau dijual. Berapa permata hijau yang tinggal?'), 30, '40-10'),
                step(T('Share the rest equally between 5 miners. How many does each miner get?', 'Kongsi baki sama banyak antara 5 pelombong. Berapa yang diperoleh setiap pelombong?'), 6, '30/5')],
               T('Find one third first, then double it.', 'Cari satu pertiga dahulu, kemudian gandakannya.'), T('60 ÷ 3 = 20, so two thirds is 40. Then 40 − 10 = 30, then 30 ÷ 5 = 6.', '60 ÷ 3 = 20, jadi dua pertiga ialah 40. Kemudian 40 − 10 = 30, kemudian 30 ÷ 5 = 6.'), 'c1-8c')])
    add(9, 'number-sense', 'patterns', 'master', 'lanterns',
        T('Echo Tunnel', 'Terowong Gema'),
        T('The tunnel echoes numbers back to you. Can you guess which number comes next?', 'Terowong itu menggemakan nombor kepada anda. Bolehkah anda meneka nombor yang seterusnya?'),
        T('Continue patterns that go up, down or multiply.', 'Menyambung pola yang bertambah, berkurang atau bergandaan.'),
        'Echo', T('Echo repeats everything, but only the right numbers.', 'Echo mengulang segalanya, tetapi hanya nombor yang betul.'),
        [pattern('arith', 4, 4, 6, seed='c19a'), pattern('arith', 100, -8, 6, seed='c19b'), pattern('geo', 3, 4, 5, seed='c19c')])
    add(10, 'reasoning', 'multi-step', 'master', 'chest',
        T('The Crystal Heart', 'Jantung Kristal'),
        T('Deep in the cave beats the Crystal Heart. Solve three steps to wake it up!', 'Jauh di dalam gua berdenyut Jantung Kristal. Selesaikan tiga langkah untuk membangunkannya!'),
        T('Multi-step problems with multiplication, fractions, percentages and ratio.', 'Masalah berbilang langkah dengan pendaraban, pecahan, peratus dan nisbah.'),
        'Pulse', T('Pulse glows brighter with every correct answer.', 'Pulse bersinar lebih terang dengan setiap jawapan yang betul.'),
        [steps([step(T('The heart has 8 beams with 5 crystals on each. How many crystals?', 'Jantung itu mempunyai 8 alur dengan 5 kristal pada setiap alur. Berapa kristal?'), 40, '8*5'),
                step(T('5 crystals crack. How many whole crystals are left?', '5 kristal retak. Berapa kristal yang masih utuh?'), 35, '40-5'),
                step(T('Share them equally between 5 holders. How many does each get?', 'Kongsi sama banyak antara 5 pemegang. Berapa yang diperoleh setiap orang?'), 7, '35/5')],
               T('Multiply first, then subtract, then share.', 'Darab dahulu, kemudian tolak, kemudian kongsi.'), T('8 × 5 = 40, then 40 − 5 = 35, then 35 ÷ 5 = 7.', '8 × 5 = 40, kemudian 40 − 5 = 35, kemudian 35 ÷ 5 = 7.'), 'c1-10a'),
         steps([step(T('The heart has 9 beams with 6 crystals on each. How many crystals?', 'Jantung itu mempunyai 9 alur dengan 6 kristal pada setiap alur. Berapa kristal?'), 54, '9*6'),
                step(T('Half of them go to the museum. How many are left?', 'Separuh daripadanya dihantar ke muzium. Berapa yang tinggal?'), 27, '54/2'),
                step(T('13 new crystals are added. How many crystals now?', '13 kristal baharu ditambah. Berapa kristal sekarang?'), 40, '27+13')],
               T('Half means divide by 2.', 'Separuh bermaksud bahagi dengan 2.'), T('9 × 6 = 54, then 54 ÷ 2 = 27, then 27 + 13 = 40.', '9 × 6 = 54, kemudian 54 ÷ 2 = 27, kemudian 27 + 13 = 40.'), 'c1-10b'),
         steps([step(T('There are 120 crystals. 25% of them are pink. How many pink crystals?', 'Terdapat 120 kristal. 25% daripadanya berwarna merah jambu. Berapa kristal merah jambu?'), 30, '120/4'),
                step(T('The pink crystals are shared in the ratio 1 : 2 between Glim and Rocky. How many does Rocky get?', 'Kristal merah jambu dikongsi dalam nisbah 1 : 2 antara Glim dan Rocky. Berapa yang diperoleh Rocky?'), 20, '30/3*2'),
                step(T('Rocky already had 15 crystals. How many does Rocky have now?', 'Rocky sudah mempunyai 15 kristal. Berapa kristal Rocky sekarang?'), 35, '20+15')],
               T('25% is one quarter. A ratio of 1 : 2 makes 3 equal parts.', '25% ialah satu perempat. Nisbah 1 : 2 menghasilkan 3 bahagian sama.'), T('120 ÷ 4 = 30. Then 30 ÷ 3 = 10 for each part, so Rocky gets 20. Then 20 + 15 = 35.', '120 ÷ 4 = 30. Kemudian 30 ÷ 3 = 10 untuk setiap bahagian, jadi Rocky mendapat 20. Kemudian 20 + 15 = 35.'), 'c1-10c')])
    return L

def gardens():
    """Floating Gardens levels 7..10 (orders 29..32)."""
    L = []
    def add(i, *a): L.append(level('g1', i, 28 + i - 6, *a))
    add(7, 'shape-data', 'perimeter', 'adventurer', 'bridge',
        T('Path Pavers', 'Pemasang Laluan'),
        T('Petal is laying paving stones. Find the paths with the right size!', 'Petal sedang memasang batu laluan. Cari laluan yang bersaiz betul!'),
        T('Compare area and perimeter of rectangles.', 'Membandingkan luas dan perimeter segi empat tepat.'),
        'Pebble', T('Pebble hops from stone to stone.', 'Pebble melompat dari batu ke batu.'),
        [shapes_area(12, [(3, 4), (2, 5), (6, 2), (5, 3), (4, 4), (2, 6)]), shapes_area(18, [(3, 6), (6, 3), (2, 9), (4, 5), (3, 3), (5, 4)]), shapes_perimeter(22, [(7, 4), (6, 5), (8, 3), (9, 2), (5, 5), (6, 4)])])
    add(8, 'shape-data', 'polygons', 'adventurer', 'door',
        T('Polygon Pots', 'Pasu Poligon'),
        T('Every flower pot has a different number of sides. Sort the right pots for Petal!', 'Setiap pasu bunga mempunyai bilangan sisi yang berbeza. Pilih pasu yang betul untuk Petal!'),
        T('Name and count sides of polygons.', 'Menamakan dan mengira sisi poligon.'),
        'Hexy', T('Hexy collects shapes with lots of sides.', 'Hexy mengumpul bentuk yang mempunyai banyak sisi.'),
        [shapes_sides(3, [{'k': 'poly', 'sides': 3, 'color': 'coral'}, {'k': 'rect', 'w': 3, 'h': 2, 'color': 'sky'}, {'k': 'circle', 'color': 'sun'}, {'k': 'poly', 'sides': 5, 'color': 'mint'}, {'k': 'poly', 'sides': 3, 'rot': 180, 'color': 'grape'}, {'k': 'poly', 'sides': 6, 'color': 'coral'}], 'triangles', 'segi tiga'),
         shapes_sides(8, [{'k': 'poly', 'sides': 8, 'color': 'coral'}, {'k': 'poly', 'sides': 6, 'color': 'sky'}, {'k': 'poly', 'sides': 8, 'rot': 22, 'color': 'mint'}, {'k': 'poly', 'sides': 5, 'color': 'sun'}, {'k': 'poly', 'sides': 7, 'color': 'grape'}, {'k': 'circle', 'color': 'sky'}], 'octagons', 'oktagon'),
         shapes_sides(7, [{'k': 'poly', 'sides': 7, 'color': 'coral'}, {'k': 'poly', 'sides': 8, 'color': 'sky'}, {'k': 'poly', 'sides': 7, 'rot': 40, 'color': 'mint'}, {'k': 'poly', 'sides': 6, 'color': 'sun'}, {'k': 'poly', 'sides': 7, 'rot': 90, 'color': 'grape'}, {'k': 'poly', 'sides': 5, 'color': 'sky'}], 'heptagons', 'heptagon')])
    add(9, 'operations', 'times-tables', 'adventurer', 'windmill',
        T('Seed Tables', 'Sifir Benih'),
        T('The seed packets are numbered in times tables. Find the pairs that grow the right number!', 'Peket benih bernombor mengikut sifir. Cari pasangan yang menghasilkan nombor yang betul!'),
        T('Practise multiplication facts.', 'Berlatih fakta darab.'),
        'Sprout', T('Sprout counts seeds in twos, threes and fours.', 'Sprout mengira benih secara dua, tiga dan empat.'),
        [tiles(24, [3, 8, 4, 6, 5, 2]), tiles(56, [7, 8, 6, 9, 4, 5]), tiles(96, [12, 8, 9, 6, 16, 7])])
    add(10, 'reasoning', 'multi-step', 'master', 'lighthouse',
        T('Garden Grand Opening', 'Pembukaan Besar Taman'),
        T('Opening day is here! Plan the fence, the flowers and the lanterns in three steps.', 'Hari pembukaan telah tiba! Rancang pagar, bunga dan tanglung dalam tiga langkah.'),
        T('Multi-step problems with perimeter, area and money.', 'Masalah berbilang langkah dengan perimeter, luas dan wang.'),
        'Bud', T('Bud cuts the ribbon on opening day.', 'Bud memotong reben pada hari pembukaan.'),
        [steps([step(T('A bed is 5 m long and 4 m wide. What is its perimeter?', 'Sebuah batas panjangnya 5 m dan lebarnya 4 m. Berapakah perimeternya?'), 18, '2*(5+4)', lambda v: f'{v} m'),
                step(T('Fence costs RM3 for each metre. How much for the whole fence?', 'Pagar berharga RM3 untuk setiap meter. Berapa harga seluruh pagar?'), 54, '18*3', lambda v: f'RM{v}'),
                step(T('You pay with RM100. How much change do you get?', 'Anda membayar dengan RM100. Berapa baki yang anda terima?'), 46, '100-54', lambda v: f'RM{v}')],
               T('Perimeter first, then multiply, then subtract.', 'Perimeter dahulu, kemudian darab, kemudian tolak.'), T('2 × (5 + 4) = 18, then 18 × 3 = 54, then 100 − 54 = 46.', '2 × (5 + 4) = 18, kemudian 18 × 3 = 54, kemudian 100 − 54 = 46.'), 'g1-10a'),
         steps([step(T('A flower bed is 8 m long and 7 m wide. What is its area?', 'Sebuah batas bunga panjangnya 8 m dan lebarnya 7 m. Berapakah luasnya?'), 56, '8*7', lambda v: f'{v} m²'),
                step(T('Each flower needs 2 m². How many flowers fit?', 'Setiap bunga memerlukan 2 m². Berapa bunga yang muat?'), 28, '56/2'),
                step(T('Each flower costs RM4. How much for all the flowers?', 'Setiap bunga berharga RM4. Berapa harga untuk semua bunga?'), 112, '28*4', lambda v: f'RM{v}')],
               T('Area is length × width.', 'Luas ialah panjang × lebar.'), T('8 × 7 = 56, then 56 ÷ 2 = 28, then 28 × 4 = 112.', '8 × 7 = 56, kemudian 56 ÷ 2 = 28, kemudian 28 × 4 = 112.'), 'g1-10b'),
         steps([step(T('A garden is 15 m long and 9 m wide. What is its perimeter?', 'Sebuah taman panjangnya 15 m dan lebarnya 9 m. Berapakah perimeternya?'), 48, '2*(15+9)', lambda v: f'{v} m'),
                step(T('A lantern post is placed every 4 m round the edge. How many posts?', 'Sebatang tiang tanglung diletakkan setiap 4 m di sekeliling tepi. Berapa batang tiang?'), 12, '48/4'),
                step(T('Each post costs RM9. How much for all the posts?', 'Setiap tiang berharga RM9. Berapa harga untuk semua tiang?'), 108, '12*9', lambda v: f'RM{v}')],
               T('Add the length and the width before you double.', 'Tambah panjang dan lebar sebelum menggandakan.'), T('2 × (15 + 9) = 48, then 48 ÷ 4 = 12, then 12 × 9 = 108.', '2 × (15 + 9) = 48, kemudian 48 ÷ 4 = 12, kemudian 12 × 9 = 108.'), 'g1-10c')])
    return L
