from lib import *
CODE, BASE = 'jc', 132
RM = lambda v: f'RM{v}'
M2 = lambda v: f'{v} m²'
M = lambda v: f'{v} m'

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'shape-data', 'shapes', 'adventurer', 'door',
        T('Leaf Shapes', 'Bentuk Daun'),
        T('Leaves of every shape hang from the jungle vines. Count the sides to find the right ones!', 'Daun pelbagai bentuk bergantungan pada pokok menjalar hutan. Kira sisi untuk mencari yang betul!'),
        T('Count the sides of shapes, even when they are turned.', 'Mengira sisi bentuk, walaupun diputar.'),
        'Leafy', T('Leafy hides inside the biggest leaf.', 'Leafy bersembunyi di dalam daun yang paling besar.'),
        [shapes_sides(3, [{'k': 'poly', 'sides': 3, 'color': 'coral'}, {'k': 'rect', 'w': 3, 'h': 2, 'color': 'sky'}, {'k': 'circle', 'color': 'sun'}, {'k': 'poly', 'sides': 5, 'color': 'mint'}, {'k': 'poly', 'sides': 3, 'rot': 180, 'color': 'grape'}], 'triangles', 'segi tiga'),
         shapes_sides(4, [{'k': 'quad', 'type': 'square', 'color': 'coral'}, {'k': 'poly', 'sides': 3, 'color': 'sky'}, {'k': 'quad', 'type': 'kite', 'color': 'mint'}, {'k': 'circle', 'color': 'sun'}, {'k': 'rect', 'w': 3, 'h': 2, 'color': 'grape'}, {'k': 'poly', 'sides': 5, 'color': 'sky'}], 'quadrilaterals', 'sisi empat'),
         shapes_sides(5, [{'k': 'poly', 'sides': 5, 'color': 'coral'}, {'k': 'poly', 'sides': 6, 'color': 'sky'}, {'k': 'poly', 'sides': 5, 'rot': 36, 'color': 'mint'}, {'k': 'quad', 'type': 'rhombus', 'color': 'sun'}, {'k': 'poly', 'sides': 7, 'color': 'grape'}, {'k': 'poly', 'sides': 5, 'rot': 72, 'color': 'sky'}], 'pentagons', 'pentagon')])
    add(2, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Vine Counting', 'Mengira Pokok Menjalar'),
        T('Monkeys swing from vine to vine and each vine has more fruit. Which number comes next?', 'Monyet berayun dari satu pokok menjalar ke yang lain dan setiap satu mempunyai lebih banyak buah. Nombor manakah yang seterusnya?'),
        T('Continue number patterns in steps of 3, 4 and 6.', 'Menyambung pola nombor dengan langkah 3, 4 dan 6.'),
        'Swingy', T('Swingy never lets go of a vine before the next one.', 'Swingy tidak pernah melepaskan pokok menjalar sebelum yang seterusnya.'),
        [pattern('arith', 3, 3, 5, seed='jc2a'), pattern('arith', 4, 4, 6, seed='jc2b'), pattern('arith', 6, 6, 6, hidden=3, seed='jc2c')])
    add(3, 'shape-data', 'perimeter', 'adventurer', 'bridge',
        T('Fence the Clearing', 'Pagar Kawasan Lapang'),
        T('The rangers fence every clearing in the jungle. Find the rectangles that need the right length of fence!', 'Renjer memagar setiap kawasan lapang di hutan. Cari segi empat tepat yang memerlukan panjang pagar yang betul!'),
        T('Perimeter: the distance around a rectangle.', 'Perimeter: jarak mengelilingi segi empat tepat.'),
        'Fenny', T('Fenny walks around everything twice, just to be sure.', 'Fenny berjalan mengelilingi setiap benda dua kali, untuk memastikan.'),
        [shapes_perimeter(10, [(3, 2), (4, 1), (2, 2), (5, 2)]), shapes_perimeter(16, [(5, 3), (6, 2), (4, 4), (7, 2), (3, 3)]), shapes_perimeter(24, [(8, 4), (7, 5), (9, 3), (6, 5), (10, 3), (8, 3)])])
    add(4, 'shape-data', 'perimeter', 'adventurer', 'picnic',
        T('Tile the Treehouse', 'Jubin Rumah Pokok'),
        T('Treehouse floors are covered in square tiles. Find the floors that have the right area!', 'Lantai rumah pokok ditutup dengan jubin segi empat sama. Cari lantai yang mempunyai luas yang betul!'),
        T('Area: count the squares, or multiply length by width.', 'Luas: kira petak, atau darabkan panjang dengan lebar.'),
        'Tilly', T('Tilly counts every square twice.', 'Tilly mengira setiap petak dua kali.'),
        [shapes_area(12, [(3, 4), (2, 6), (5, 2), (4, 4)]), shapes_area(20, [(4, 5), (10, 2), (5, 5), (3, 6), (2, 9)]), shapes_area(36, [(6, 6), (4, 9), (3, 12), (5, 7), (8, 4)])])
    add(5, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('Rope Bridge', 'Jambatan Tali'),
        T('The rope bridge has planks marked with numbers. Place the marker on the right plank!', 'Jambatan tali mempunyai papan yang ditanda dengan nombor. Letakkan penanda pada papan yang betul!'),
        T('Place numbers on a line in sixes, fifties and two hundreds.', 'Meletakkan nombor pada garis dalam enam, lima puluh dan dua ratus.'),
        'Planky', T('Planky creaks happily on every step.', 'Planky berdecit riang pada setiap langkah.'),
        [numberline(36, 0, 60, 6, 12), numberline(450, 0, 600, 50, 150), numberline(1600, 1000, 3000, 200, 800, kind='half', a=1200, b=2000)])
    add(6, 'shape-data', 'data', 'master', 'lighthouse',
        T('Jungle Count', 'Kiraan Hutan'),
        T('The rangers counted the animals in the jungle. Read the chart to answer!', 'Renjer mengira haiwan di hutan. Baca carta untuk menjawab!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Tallyo', T('Tallyo keeps a tally on his tail.', 'Tallyo menyimpan kiraan pada ekornya.'),
        [chart([(T('Monkeys', 'Monyet'), 14, 'coral'), (T('Parrots', 'Burung kakak tua'), 9, 'sun'), (T('Frogs', 'Katak'), 20, 'mint')], ('diff', 0, 1), T('animals', 'haiwan')),
         chart([(T('Monkeys', 'Monyet'), 12, 'coral'), (T('Parrots', 'Burung kakak tua'), 18, 'sun'), (T('Frogs', 'Katak'), 15, 'mint'), (T('Snakes', 'Ular'), 25, 'grape')], ('sum', [1, 3]), T('animals', 'haiwan')),
         chart([(T('Monkeys', 'Monyet'), 10, 'coral'), (T('Parrots', 'Burung kakak tua'), 20, 'sun'), (T('Frogs', 'Katak'), 15, 'mint'), (T('Snakes', 'Ular'), 25, 'grape'), (T('Bats', 'Kelawar'), 30, 'sky')], ('mean',), T('animals', 'haiwan'))])
    add(7, 'reasoning', 'multi-step', 'master', 'gears',
        T('Clearing Sums', 'Pengiraan Kawasan Lapang'),
        T('Plan the fences and floors of the jungle camp. Each problem has three steps!', 'Rancang pagar dan lantai perkhemahan hutan. Setiap masalah mempunyai tiga langkah!'),
        T('Multi-step problems with perimeter and area.', 'Masalah berbilang langkah dengan perimeter dan luas.'),
        'Campy', T('Campy sleeps in a hammock made of leaves.', 'Campy tidur dalam buaian yang diperbuat daripada daun.'),
        [steps([step(T('A clearing is 9 m long and 6 m wide. What is its perimeter?', 'Sebuah kawasan lapang panjangnya 9 m dan lebarnya 6 m. Berapakah perimeternya?'), 30, '2*(9+6)', M),
                step(T('Fence costs RM4 for each metre. What does the fence cost?', 'Pagar berharga RM4 untuk setiap meter. Berapakah harga pagar itu?'), 120, '30*4', RM),
                step(T('You pay with RM200. How much change do you get?', 'Anda membayar dengan RM200. Berapa baki yang anda terima?'), 80, '200-120', RM)],
               T('Perimeter is 2 × (length + width).', 'Perimeter ialah 2 × (panjang + lebar).'), T('2 × (9 + 6) = 30, then 30 × 4 = 120, then 200 − 120 = 80.', '2 × (9 + 6) = 30, kemudian 30 × 4 = 120, kemudian 200 − 120 = 80.'), 'jc7a'),
         steps([step(T('A floor is 8 m long and 7 m wide. What is its area?', 'Sebuah lantai panjangnya 8 m dan lebarnya 7 m. Berapakah luasnya?'), 56, '8*7', M2),
                step(T('Each tile covers 4 square metres. How many tiles are needed?', 'Setiap jubin menutup 4 meter persegi. Berapa jubin yang diperlukan?'), 14, '56/4'),
                step(T('Each tile costs RM3. What do all the tiles cost?', 'Setiap jubin berharga RM3. Berapakah harga semua jubin?'), 42, '14*3', RM)],
               T('Area is length × width.', 'Luas ialah panjang × lebar.'), T('8 × 7 = 56, then 56 ÷ 4 = 14, then 14 × 3 = 42.', '8 × 7 = 56, kemudian 56 ÷ 4 = 14, kemudian 14 × 3 = 42.'), 'jc7b'),
         steps([step(T('A square clearing has a perimeter of 36 m. How long is each side?', 'Sebuah kawasan lapang berbentuk segi empat sama mempunyai perimeter 36 m. Berapa panjang setiap sisi?'), 9, '36/4', M),
                step(T('What is the area of the clearing?', 'Berapakah luas kawasan lapang itu?'), 81, '9*9', M2),
                step(T('Each plant needs 3 square metres. How many plants fit?', 'Setiap tumbuhan memerlukan 3 meter persegi. Berapa tumbuhan yang muat?'), 27, '81/3')],
               T('A square has 4 equal sides.', 'Segi empat sama mempunyai 4 sisi yang sama.'), T('36 ÷ 4 = 9, then 9 × 9 = 81, then 81 ÷ 3 = 27.', '36 ÷ 4 = 9, kemudian 9 × 9 = 81, kemudian 81 ÷ 3 = 27.'), 'jc7c')])
    add(8, 'operations', 'times-tables', 'master', 'scale',
        T('Banana Boxes', 'Kotak Pisang'),
        T('Bananas are packed in equal boxes. Find the two tiles that make each total, and weigh the crates!', 'Pisang dipek dalam kotak yang sama saiz. Cari dua jubin yang membentuk setiap jumlah, dan timbang peti itu!'),
        T('Multiplication facts and adding crates.', 'Fakta darab dan menambah peti.'),
        'Nanner', T('Nanner peels a banana in one clean pull.', 'Nanner mengupas pisang dengan satu tarikan.'),
        [tiles(40, [5, 8, 4, 10, 6, 3]), balance(100, [35, 45, 20, 55, 30, 25], 3), tiles(120, [10, 12, 9, 14, 6, 7])])
    add(9, 'number-sense', 'place-value', 'master', 'door',
        T('Totem Numbers', 'Nombor Totem'),
        T('Every jungle totem has a number carved into it. Build the number or arrange the tiles!', 'Setiap totem hutan mempunyai nombor yang diukir padanya. Bina nombor itu atau susun jubin!'),
        T('Build and order numbers with place value.', 'Membina dan menyusun nombor dengan nilai tempat.'),
        'Totty', T('Totty has a different face on every side.', 'Totty mempunyai muka yang berbeza pada setiap sisi.'),
        [placevalue(630, [100, 10, 1]), digitarrange([3, 8, 5, 2], 'largest'), digitarrange([6, 0, 4, 9], 'smallest')])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Canopy Finale', 'Kemuncak Kanopi'),
        T('The top of the canopy is in sight! Solve three steps to reach the golden fruit.', 'Puncak kanopi sudah kelihatan! Selesaikan tiga langkah untuk sampai ke buah emas.'),
        T('Multi-step problems with shapes, money and sharing.', 'Masalah berbilang langkah dengan bentuk, wang dan perkongsian.'),
        'Canopy', T('Canopy lives at the very top of the tallest tree.', 'Canopy tinggal di puncak pokok yang paling tinggi.'),
        [steps([step(T('A rope bridge has 12 planks in each row and 5 rows. How many planks?', 'Sebuah jambatan tali mempunyai 12 papan dalam setiap baris dan 5 baris. Berapa papan?'), 60, '12*5'),
                step(T('8 planks are broken. How many planks are left?', '8 papan patah. Berapa papan yang tinggal?'), 52, '60-8'),
                step(T('Each new plank costs RM2. What do 8 new planks cost?', 'Setiap papan baharu berharga RM2. Berapakah harga 8 papan baharu?'), 16, '8*2', RM)],
               T('Multiply first, then subtract.', 'Darab dahulu, kemudian tolak.'), T('12 × 5 = 60, then 60 − 8 = 52, then 8 × 2 = 16.', '12 × 5 = 60, kemudian 60 − 8 = 52, kemudian 8 × 2 = 16.'), 'jc10a'),
         steps([step(T('A rectangular garden is 15 m long and 10 m wide. What is its area?', 'Sebuah taman segi empat tepat panjangnya 15 m dan lebarnya 10 m. Berapakah luasnya?'), 150, '15*10', M2),
                step(T('Half of the garden is planted with ferns. How many square metres are ferns?', 'Separuh taman ditanam pakis. Berapa meter persegi pakis?'), 75, '150/2', M2),
                step(T('The ferns are planted in 5 equal rows. How many square metres in each row?', 'Pakis ditanam dalam 5 baris yang sama. Berapa meter persegi dalam setiap baris?'), 15, '75/5', M2)],
               T('Half means divide by 2.', 'Separuh bermaksud bahagi dengan 2.'), T('15 × 10 = 150, then 150 ÷ 2 = 75, then 75 ÷ 5 = 15.', '15 × 10 = 150, kemudian 150 ÷ 2 = 75, kemudian 75 ÷ 5 = 15.'), 'jc10b'),
         steps([step(T('A rectangle is 14 m long and 6 m wide. What is its perimeter?', 'Sebuah segi empat tepat panjangnya 14 m dan lebarnya 6 m. Berapakah perimeternya?'), 40, '2*(14+6)', M),
                step(T('A rope costs RM5 for each metre. What does the rope cost?', 'Tali berharga RM5 untuk setiap meter. Berapakah harga tali itu?'), 200, '40*5', RM),
                step(T('Five rangers share the cost equally. How much does each ranger pay?', 'Lima renjer berkongsi kos itu sama banyak. Berapa yang dibayar oleh setiap renjer?'), 40, '200/5', RM)],
               T('Find the perimeter first.', 'Cari perimeter dahulu.'), T('2 × (14 + 6) = 40, then 40 × 5 = 200, then 200 ÷ 5 = 40.', '2 × (14 + 6) = 40, kemudian 40 × 5 = 200, kemudian 200 ÷ 5 = 40.'), 'jc10c')])
    return L
