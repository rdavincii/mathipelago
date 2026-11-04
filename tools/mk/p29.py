from lib import *
CODE, BASE = 'tt', 292
RM = lambda v: f'RM{v}'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'shape-data', 'shapes', 'adventurer', 'door',
        T('Window Shapes', 'Bentuk Tingkap'),
        T('Every treehouse has windows of different shapes. Tap the windows with the right number of sides!', 'Setiap rumah pokok mempunyai tingkap dengan bentuk berbeza. Ketik tingkap yang mempunyai bilangan sisi yang betul!'),
        T('Count the sides of shapes.', 'Mengira sisi bentuk.'),
        'Acorny', T('Acorny peeks out of every window.', 'Acorny mengintai dari setiap tingkap.'),
        [shapes_sides(4, [{'k': 'quad', 'type': 'square', 'color': 'coral'}, {'k': 'poly', 'sides': 3, 'color': 'sky'}, {'k': 'circle', 'color': 'sun'}, {'k': 'rect', 'w': 3, 'h': 2, 'color': 'mint'}, {'k': 'poly', 'sides': 5, 'color': 'grape'}], 'square, rectangle', 'segi empat sama, segi empat tepat'),
         shapes_sides(6, [{'k': 'poly', 'sides': 6, 'color': 'coral'}, {'k': 'poly', 'sides': 5, 'color': 'sky'}, {'k': 'poly', 'sides': 6, 'rot': 30, 'color': 'mint'}, {'k': 'circle', 'color': 'sun'}, {'k': 'poly', 'sides': 4, 'color': 'grape'}], 'hexagon', 'heksagon'),
         shapes_sides(3, [{'k': 'poly', 'sides': 3, 'color': 'coral'}, {'k': 'poly', 'sides': 3, 'rot': 180, 'color': 'sky'}, {'k': 'quad', 'type': 'kite', 'color': 'sun'}, {'k': 'poly', 'sides': 5, 'color': 'mint'}, {'k': 'poly', 'sides': 7, 'color': 'grape'}, {'k': 'circle', 'color': 'coral'}], 'triangle', 'segi tiga')])
    add(2, 'shape-data', 'perimeter', 'adventurer', 'bridge',
        T('Fence Around', 'Pagar Sekeliling'),
        T('Each garden needs a fence all the way around. Find the gardens that need the right length of fence!', 'Setiap taman memerlukan pagar sepanjang sekelilingnya. Cari taman yang memerlukan panjang pagar yang betul!'),
        T('Perimeter of rectangles.', 'Perimeter segi empat tepat.'),
        'Fencey', T('Fencey checks every post twice.', 'Fencey memeriksa setiap tiang dua kali.'),
        [shapes_perimeter(12, [(4, 2), (5, 1), (3, 3), (6, 2), (2, 2)]), shapes_perimeter(18, [(5, 4), (6, 3), (7, 2), (4, 4), (8, 2)]), shapes_perimeter(22, [(8, 3), (7, 4), (9, 2), (6, 4), (10, 1), (5, 5)])])
    add(3, 'shape-data', 'perimeter', 'adventurer', 'door',
        T('Floor Space', 'Ruang Lantai'),
        T('Each treehouse room has a floor. Find the rooms with the right floor area!', 'Setiap bilik rumah pokok mempunyai lantai. Cari bilik yang mempunyai luas lantai yang betul!'),
        T('Area of rectangles.', 'Luas segi empat tepat.'),
        'Floory', T('Floory sweeps every square of the floor.', 'Floory menyapu setiap petak lantai.'),
        [shapes_area(12, [(3, 4), (2, 6), (5, 2), (4, 4), (1, 12)]), shapes_area(18, [(3, 6), (2, 9), (4, 5), (6, 4), (5, 3)]), shapes_area(24, [(4, 6), (3, 8), (2, 12), (5, 5), (6, 3), (7, 4)])])
    add(4, 'reasoning', 'perimeter', 'adventurer', 'scale',
        T('Fence Costs', 'Kos Pagar'),
        T('The builders need to fence the gardens. Work out the length, the cost and the change!', 'Para pembina perlu memagar taman-taman itu. Kira panjang, kos dan bakinya!'),
        T('Perimeter and cost in steps.', 'Perimeter dan kos secara berperingkat.'),
        'Postly', T('Postly knocks in a post with every hop.', 'Postly memacak tiang dengan setiap lompatan.'),
        [steps([step(T('A garden is 8 m long and 5 m wide. What is its perimeter?', 'Sebuah taman panjangnya 8 m dan lebarnya 5 m. Berapakah perimeternya?'), 26, '2*(8+5)', lambda v: f'{v} m'),
                step(T('Fence costs RM3 for each metre. What does the fence cost?', 'Pagar berharga RM3 untuk setiap meter. Berapakah harga pagar itu?'), 78, '26*3', RM),
                step(T('You pay with RM100. How much change do you get?', 'Anda membayar dengan RM100. Berapakah baki yang anda terima?'), 22, '100-78', RM)],
               T('Perimeter is 2 × (length + width).', 'Perimeter ialah 2 × (panjang + lebar).'), T('2 × (8 + 5) = 26, then 26 × 3 = 78, then 100 − 78 = 22.', '2 × (8 + 5) = 26, kemudian 26 × 3 = 78, kemudian 100 − 78 = 22.'), 'tt4a'),
         steps([step(T('A square yard has sides of 9 m. What is its perimeter?', 'Sebuah halaman segi empat sama mempunyai sisi 9 m. Berapakah perimeternya?'), 36, '4*9', lambda v: f'{v} m'),
                step(T('A gate takes up 3 m of the fence. How many metres of fence are still needed?', 'Sebuah pintu pagar mengambil 3 m daripada pagar. Berapa meter pagar yang masih diperlukan?'), 33, '36-3', lambda v: f'{v} m'),
                step(T('Each fence panel is 3 m long. How many panels are needed?', 'Setiap panel pagar panjangnya 3 m. Berapa panel yang diperlukan?'), 11, '33/3')],
               T('A square has 4 equal sides.', 'Segi empat sama mempunyai 4 sisi yang sama.'), T('4 × 9 = 36, then 36 − 3 = 33, then 33 ÷ 3 = 11.', '4 × 9 = 36, kemudian 36 − 3 = 33, kemudian 33 ÷ 3 = 11.'), 'tt4b'),
         steps([step(T('A rectangular field is 15 m long and 10 m wide. What is its perimeter?', 'Sebuah padang segi empat tepat panjangnya 15 m dan lebarnya 10 m. Berapakah perimeternya?'), 50, '2*(15+10)', lambda v: f'{v} m'),
                step(T('Two rows of rope are needed. How many metres of rope is that?', 'Dua baris tali diperlukan. Berapa meter tali itu?'), 100, '50*2', lambda v: f'{v} m'),
                step(T('Rope costs RM2 for each metre. What does the rope cost?', 'Tali berharga RM2 untuk setiap meter. Berapakah harga tali itu?'), 200, '100*2', RM)],
               T('Find the perimeter first, then double it.', 'Cari perimeter dahulu, kemudian gandakannya.'), T('2 × (15 + 10) = 50, then 50 × 2 = 100, then 100 × 2 = 200.', '2 × (15 + 10) = 50, kemudian 50 × 2 = 100, kemudian 100 × 2 = 200.'), 'tt4c')])
    add(5, 'operations', 'times-tables', 'adventurer', 'gears',
        T('Plank Piles', 'Longgokan Papan'),
        T('The builders stack planks in equal piles. Find the two tiles that make each total!', 'Para pembina menyusun papan dalam longgokan yang sama banyak. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Planky', T('Planky counts planks in his sleep.', 'Planky mengira papan dalam tidurnya.'),
        [tiles(42, [6, 7, 5, 9, 4, 8]), tiles(96, [8, 12, 6, 16, 9, 7]), tiles(156, [12, 13, 11, 9, 14, 8])])
    add(6, 'number-sense', 'addition', 'adventurer', 'scale',
        T('Beam Balance', 'Seimbangkan Alang'),
        T('The beams must be balanced. Choose the beams that add up to the total weight!', 'Alang-alang mesti diseimbangkan. Pilih alang yang jumlahnya sama dengan jumlah berat!'),
        T('Add several numbers to reach a total.', 'Menambah beberapa nombor untuk mencapai jumlah.'),
        'Beamy', T('Beamy walks the tightrope without a wobble.', 'Beamy berjalan di atas tali tanpa goyah.'),
        [balance(60, [15, 25, 20, 30, 10]), balance(150, [45, 65, 40, 55, 35, 25]), balance(240, [85, 70, 95, 60, 45, 120], 3)])
    add(7, 'operations', 'money', 'master', 'chest',
        T('Hammer and Nails', 'Tukul dan Paku'),
        T('The hardware shop wants the exact money. Pay each price with the right coins!', 'Kedai perkakas mahukan wang yang tepat. Bayar setiap harga dengan syiling yang betul!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Nailey', T('Nailey keeps a jar of shiny nails.', 'Nailey menyimpan sebalang paku berkilat.'),
        [coins(95, [5, 10, 20, 50]), coins(260, [10, 20, 50, 100]), coins(485, [5, 10, 20, 50, 100], 9)])
    add(8, 'shape-data', 'data', 'master', 'lighthouse',
        T('Wood Chart', 'Carta Kayu'),
        T('The town recorded how many treehouses were built each season. Read the chart!', 'Pekan merekodkan berapa banyak rumah pokok dibina setiap musim. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Chippy', T('Chippy collects every shaving of wood.', 'Chippy mengumpul setiap serpihan kayu.'),
        [chart([(T('Spring', 'Musim bunga'), 14, 'mint'), (T('Summer', 'Musim panas'), 9, 'sun'), (T('Autumn', 'Musim luruh'), 12, 'coral')], ('diff', 0, 1), T('houses', 'rumah')),
         chart([(T('Spring', 'Musim bunga'), 18, 'mint'), (T('Summer', 'Musim panas'), 25, 'sun'), (T('Autumn', 'Musim luruh'), 12, 'coral'), (T('Winter', 'Musim sejuk'), 20, 'sky')], ('sum', [0, 1, 2, 3]), T('houses', 'rumah')),
         chart([(T('Spring', 'Musim bunga'), 24, 'mint'), (T('Summer', 'Musim panas'), 36, 'sun'), (T('Autumn', 'Musim luruh'), 30, 'coral'), (T('Winter', 'Musim sejuk'), 18, 'sky'), (T('Monsoon', 'Musim tengkujuh'), 12, 'grape')], ('mean',), T('houses', 'rumah'))])
    add(9, 'number-sense', 'patterns', 'master', 'lanterns',
        T('Ladder Rungs', 'Anak Tangga'),
        T('The ladder rungs are numbered in a pattern. Which number comes next?', 'Anak tangga dinomborkan dalam satu pola. Nombor yang manakah seterusnya?'),
        T('Continue number patterns.', 'Menyambung pola nombor.'),
        'Rungy', T('Rungy climbs two rungs at a time.', 'Rungy memanjat dua anak tangga sekali gus.'),
        [pattern('arith', 7, 6, 5, seed='tt9a'), pattern('geo', 2, 3, 5, seed='tt9b'), pattern('arith', 200, -15, 6, hidden=4, seed='tt9c')])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Treehouse Finale', 'Kemuncak Rumah Pokok'),
        T('The biggest treehouse in town is almost ready! Solve three steps of building sums.', 'Rumah pokok terbesar di pekan hampir siap! Selesaikan tiga langkah pengiraan pembinaan.'),
        T('Multi-step problems with area, perimeter and money.', 'Masalah berbilang langkah dengan luas, perimeter dan wang.'),
        'Topper', T('Topper plants the flag on the highest branch.', 'Topper menanam bendera di dahan paling tinggi.'),
        [steps([step(T('A treehouse floor is 6 m by 4 m. What is its area?', 'Lantai sebuah rumah pokok ialah 6 m kali 4 m. Berapakah luasnya?'), 24, '6*4', lambda v: f'{v} m²'),
                step(T('Floor boards cost RM5 for each square metre. What do the boards cost?', 'Papan lantai berharga RM5 untuk setiap meter persegi. Berapakah harga papan itu?'), 120, '24*5', RM),
                step(T('The builder has RM150. How much money is left?', 'Pembina ada RM150. Berapa wang yang tinggal?'), 30, '150-120', RM)],
               T('Area is length × width.', 'Luas ialah panjang × lebar.'), T('6 × 4 = 24, then 24 × 5 = 120, then 150 − 120 = 30.', '6 × 4 = 24, kemudian 24 × 5 = 120, kemudian 150 − 120 = 30.'), 'tt10a'),
         steps([step(T('A room is 5 m long and 4 m wide. What is its area?', 'Sebuah bilik panjangnya 5 m dan lebarnya 4 m. Berapakah luasnya?'), 20, '5*4', lambda v: f'{v} m²'),
                step(T('A second room has 3 times that area. What is its area?', 'Bilik kedua mempunyai luas 3 kali ganda. Berapakah luasnya?'), 60, '20*3', lambda v: f'{v} m²'),
                step(T('What is the area of both rooms together?', 'Berapakah luas kedua-dua bilik jika digabungkan?'), 80, '20+60', lambda v: f'{v} m²')],
               T('Find the first area, then multiply, then add.', 'Cari luas pertama, kemudian darab, kemudian tambah.'), T('5 × 4 = 20, then 20 × 3 = 60, then 20 + 60 = 80.', '5 × 4 = 20, kemudian 20 × 3 = 60, kemudian 20 + 60 = 80.'), 'tt10b'),
         steps([step(T('A rope bridge is 12 m long. A town builds 7 bridges. How many metres of bridge is that?', 'Sebuah jambatan tali panjangnya 12 m. Sebuah pekan membina 7 jambatan. Berapa meter jambatan itu?'), 84, '7*12', lambda v: f'{v} m'),
                step(T('Each metre needs 4 ropes. How many ropes are needed?', 'Setiap meter memerlukan 4 tali. Berapa tali yang diperlukan?'), 336, '84*4'),
                step(T('The ropes come in bundles of 8. How many bundles are needed?', 'Tali itu dijual dalam ikatan 8. Berapa ikatan yang diperlukan?'), 42, '336/8')],
               T('Multiply, multiply, then divide.', 'Darab, darab, kemudian bahagi.'), T('7 × 12 = 84, then 84 × 4 = 336, then 336 ÷ 8 = 42.', '7 × 12 = 84, kemudian 84 × 4 = 336, kemudian 336 ÷ 8 = 42.'), 'tt10c')])
    return L
