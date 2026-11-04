from lib import *
CODE, BASE = 'kf', 232
RM = lambda v: f'RM{v}'
MT = T('Tap one, then tap the one that matches it.', 'Ketik satu, kemudian ketik yang sepadan dengannya.')

def build():
    L = []
    def add(i, *a): L.append(level(CODE, i, BASE + i, *a))
    add(1, 'shape-data', 'shapes', 'adventurer', 'door',
        T('Kite Shapes', 'Bentuk Layang-layang'),
        T('Kites of every shape fill the sky. Count the sides to find the right ones!', 'Layang-layang pelbagai bentuk memenuhi langit. Kira sisi untuk mencari yang betul!'),
        T('Count the sides of shapes, even when they are turned.', 'Mengira sisi bentuk, walaupun diputar.'),
        'Wau', T('Wau flies the highest kite of all.', 'Wau menerbangkan layang-layang yang paling tinggi.'),
        [shapes_sides(3, [{'k': 'poly', 'sides': 3, 'color': 'coral'}, {'k': 'quad', 'type': 'kite', 'color': 'sky'}, {'k': 'circle', 'color': 'sun'}, {'k': 'poly', 'sides': 5, 'color': 'mint'}, {'k': 'poly', 'sides': 3, 'rot': 180, 'color': 'grape'}], 'triangles', 'segi tiga'),
         shapes_sides(4, [{'k': 'quad', 'type': 'kite', 'color': 'coral'}, {'k': 'poly', 'sides': 3, 'color': 'sky'}, {'k': 'quad', 'type': 'rhombus', 'color': 'mint'}, {'k': 'circle', 'color': 'sun'}, {'k': 'rect', 'w': 3, 'h': 2, 'color': 'grape'}, {'k': 'poly', 'sides': 6, 'color': 'sky'}], 'quadrilaterals', 'sisi empat'),
         shapes_sides(6, [{'k': 'poly', 'sides': 6, 'color': 'coral'}, {'k': 'poly', 'sides': 5, 'color': 'sky'}, {'k': 'poly', 'sides': 6, 'rot': 30, 'color': 'mint'}, {'k': 'quad', 'type': 'kite', 'color': 'sun'}, {'k': 'poly', 'sides': 8, 'color': 'grape'}, {'k': 'poly', 'sides': 7, 'color': 'sky'}], 'hexagons', 'heksagon')])
    add(2, 'number-sense', 'patterns', 'adventurer', 'lanterns',
        T('Tail Bows', 'Reben Ekor'),
        T('Every kite tail has more bows than the one before. Which number comes next?', 'Setiap ekor layang-layang mempunyai lebih banyak reben daripada yang sebelumnya. Nombor manakah yang seterusnya?'),
        T('Continue number patterns in steps of 2, 5 and 8.', 'Menyambung pola nombor dengan langkah 2, 5 dan 8.'),
        'Tailo', T('Tailo ties a new bow every minute.', 'Tailo mengikat reben baharu setiap minit.'),
        [pattern('arith', 2, 2, 5, seed='kf2a'), pattern('arith', 5, 5, 6, seed='kf2b'), pattern('arith', 8, 8, 6, hidden=3, seed='kf2c')])
    add(3, 'shape-data', 'perimeter', 'adventurer', 'bridge',
        T('Kite Frames', 'Rangka Layang-layang'),
        T('Each kite frame needs a strip of bamboo all the way around. Find the frames that need the right length!', 'Setiap rangka layang-layang memerlukan jalur buluh di sekelilingnya. Cari rangka yang memerlukan panjang yang betul!'),
        T('Perimeter: the distance around a rectangle.', 'Perimeter: jarak mengelilingi segi empat tepat.'),
        'Bamboo', T('Bamboo bends but never breaks.', 'Bamboo melentur tetapi tidak pernah patah.'),
        [shapes_perimeter(14, [(4, 3), (5, 2), (6, 1), (3, 3), (4, 4)]), shapes_perimeter(20, [(6, 4), (7, 3), (5, 5), (8, 2), (9, 2)]), shapes_perimeter(30, [(10, 5), (9, 6), (8, 8), (12, 3), (7, 7), (11, 4)])])
    add(4, 'number-sense', 'number-line', 'adventurer', 'bridge',
        T('Wind Heights', 'Ketinggian Angin'),
        T('The wind carries kites to different heights. Slide the marker to the right height!', 'Angin membawa layang-layang ke ketinggian yang berbeza. Gelongsorkan penanda ke ketinggian yang betul!'),
        T('Place numbers on a line in tens and fifties.', 'Meletakkan nombor pada garis dalam puluh dan lima puluh.'),
        'Breezy', T('Breezy blows everything a little higher.', 'Breezy meniup semuanya sedikit lebih tinggi.'),
        [numberline(30, 0, 100, 10, 20), numberline(240, 0, 400, 40, 80), numberline(250, 0, 500, 50, 100, kind='half', a=100, b=400)])
    add(5, 'operations', 'times-tables', 'adventurer', 'gears',
        T('Kite Bundles', 'Ikatan Layang-layang'),
        T('Kites are tied in bundles of equal size. Find the two tiles that make each total!', 'Layang-layang diikat dalam ikatan yang sama saiz. Cari dua jubin yang membentuk setiap jumlah!'),
        T('Multiplication facts in context.', 'Fakta darab dalam konteks.'),
        'Bundle', T('Bundle never drops a single kite.', 'Bundle tidak pernah menjatuhkan walau sebuah layang-layang.'),
        [tiles(36, [4, 9, 6, 3, 12, 5]), tiles(72, [8, 9, 6, 12, 7, 5]), tiles(144, [12, 9, 16, 8, 18, 14])])
    add(6, 'shape-data', 'perimeter', 'master', 'picnic',
        T('Sky Patches', 'Tampalan Langit'),
        T('Kite sails are sewn from cloth patches. Find the patches that cover the right area!', 'Layar layang-layang dijahit daripada kepingan kain. Cari kepingan yang menutup luas yang betul!'),
        T('Area: count the small squares, or multiply length by width.', 'Luas: kira petak kecil, atau darabkan panjang dengan lebar.'),
        'Patchy', T('Patchy has a patch on every patch.', 'Patchy mempunyai tampalan pada setiap tampalan.'),
        [shapes_area(12, [(3, 4), (2, 6), (5, 2), (4, 4)]), shapes_area(18, [(3, 6), (2, 9), (4, 5), (6, 5), (7, 3)]), shapes_area(40, [(5, 8), (4, 10), (6, 6), (7, 5), (9, 4)])])
    add(7, 'number-sense', 'times-tables', 'master', 'door',
        T('Sail Sums', 'Jumlah Layar'),
        T('Each kite sail is a rectangle. Match each size to its area!', 'Setiap layar layang-layang ialah segi empat tepat. Padankan setiap saiz dengan luasnya!'),
        T('Multiply length by width to find area.', 'Mendarab panjang dengan lebar untuk mencari luas.'),
        'Sailor', T('Sailor reads every number off the sail.', 'Sailor membaca setiap nombor pada layar.'),
        [match([('3 × 4', '12'), ('5 × 5', '25'), ('2 × 9', '18')], MT, T('Area is length × width.', 'Luas ialah panjang × lebar.')),
         match([('4 × 6', '24'), ('7 × 3', '21'), ('8 × 5', '40'), ('9 × 2', '18')], MT, T('Area is length × width.', 'Luas ialah panjang × lebar.')),
         match([('6 × 7', '42'), ('8 × 9', '72'), ('12 × 4', '48'), ('11 × 5', '55'), ('9 × 9', '81')], MT, T('Area is length × width.', 'Luas ialah panjang × lebar.'))])
    add(8, 'operations', 'money', 'master', 'chest',
        T('Kite Shop', 'Kedai Layang-layang'),
        T('The kite shop sells string, paper and glue. Pay each price with exactly the right coins!', 'Kedai layang-layang menjual benang, kertas dan gam. Bayar setiap harga dengan syiling yang tepat!'),
        T('Make exact amounts of money.', 'Membentuk jumlah wang yang tepat.'),
        'Stringy', T('Stringy keeps a ball of string in every pocket.', 'Stringy menyimpan segulung benang dalam setiap poket.'),
        [coins(55, [5, 10, 20, 50]), coins(130, [5, 10, 20, 50, 100]), coins(365, [5, 10, 20, 50, 100], 7)])
    add(9, 'shape-data', 'data', 'master', 'lighthouse',
        T('Kite Contest', 'Pertandingan Layang-layang'),
        T('The judges counted the kites at the big contest. Read the chart!', 'Para hakim mengira layang-layang pada pertandingan besar itu. Baca carta itu!'),
        T('Read bar charts: differences, totals and averages.', 'Membaca carta palang: beza, jumlah dan purata.'),
        'Judge', T('Judge gives a score to every kite, even the wobbly ones.', 'Judge memberi markah kepada setiap layang-layang, malah yang bergoyang.'),
        [chart([(T('Red', 'Merah'), 14, 'coral'), (T('Blue', 'Biru'), 9, 'sky'), (T('Green', 'Hijau'), 11, 'mint')], ('diff', 0, 1), T('kites', 'layang-layang')),
         chart([(T('Red', 'Merah'), 12, 'coral'), (T('Blue', 'Biru'), 18, 'sky'), (T('Green', 'Hijau'), 15, 'mint'), (T('Yellow', 'Kuning'), 9, 'sun')], ('sum', [0, 1, 2, 3]), T('kites', 'layang-layang')),
         chart([(T('Red', 'Merah'), 20, 'coral'), (T('Blue', 'Biru'), 35, 'sky'), (T('Green', 'Hijau'), 25, 'mint'), (T('Yellow', 'Kuning'), 30, 'sun'), (T('Purple', 'Ungu'), 40, 'grape')], ('mean',), T('kites', 'layang-layang'))])
    add(10, 'reasoning', 'multi-step', 'master', 'windmill',
        T('Kite Festival Finale', 'Kemuncak Pesta Layang-layang'),
        T('The great kite festival begins! Solve three steps to launch the biggest kite of all.', 'Pesta layang-layang besar bermula! Selesaikan tiga langkah untuk menerbangkan layang-layang terbesar.'),
        T('Multi-step problems with area, perimeter and money.', 'Masalah berbilang langkah dengan luas, perimeter dan wang.'),
        'Soary', T('Soary lifts off whenever the wind says go.', 'Soary terbang apabila angin memberi isyarat.'),
        [steps([step(T('A kite sail is 8 cm wide and 6 cm tall. What is its area?', 'Layar layang-layang selebar 8 cm dan setinggi 6 cm. Berapakah luasnya?'), 48, '8*6', lambda v: f'{v} cm²'),
                step(T('A festival needs 5 sails the same size. How many square centimetres of cloth is that?', 'Sebuah pesta memerlukan 5 layar yang sama saiz. Berapa sentimeter persegi kain itu?'), 240, '48*5', lambda v: f'{v} cm²'),
                step(T('Each sail needs 4 cm² of glue. How many cm² of glue are needed?', 'Setiap layar memerlukan 4 cm² gam. Berapa cm² gam yang diperlukan?'), 20, '5*4', lambda v: f'{v} cm²')],
               T('Area is length times width.', 'Luas ialah panjang darab lebar.'), T('8 × 6 = 48, then 48 × 5 = 240, then 5 × 4 = 20.', '8 × 6 = 48, kemudian 48 × 5 = 240, kemudian 5 × 4 = 20.'), 'kf10a'),
         steps([step(T('A frame is 9 cm long and 4 cm wide. What is its perimeter?', 'Sebuah rangka sepanjang 9 cm dan selebar 4 cm. Berapakah perimeternya?'), 26, '2*(9+4)', lambda v: f'{v} cm'),
                step(T('Bamboo costs 3 sen for each cm. How many sen is the bamboo for one frame?', 'Buluh berharga 3 sen untuk setiap cm. Berapa sen buluh untuk satu rangka?'), 78, '26*3', lambda v: f'{v} sen'),
                step(T('How many sen is the bamboo for 10 frames?', 'Berapa sen buluh untuk 10 rangka?'), 780, '78*10', lambda v: f'{v} sen')],
               T('Add length and width, then double it.', 'Tambah panjang dan lebar, kemudian gandakannya.'), T('2 × (9 + 4) = 26, then 26 × 3 = 78, then 78 × 10 = 780.', '2 × (9 + 4) = 26, kemudian 26 × 3 = 78, kemudian 78 × 10 = 780.'), 'kf10b'),
         steps([step(T('A shop sells 6 kites for RM4 each. How much do the 6 kites cost?', 'Sebuah kedai menjual 6 layang-layang dengan harga RM4 setiap satu. Berapa harga 6 layang-layang itu?'), 24, '6*4', RM),
                step(T('The shop also sells string for RM7. What is the total?', 'Kedai itu turut menjual benang dengan harga RM7. Berapakah jumlahnya?'), 31, '24+7', RM),
                step(T('You pay with RM50. How much change do you get?', 'Anda membayar dengan RM50. Berapa baki yang anda terima?'), 19, '50-31', RM)],
               T('Add the costs, then take them from RM50.', 'Tambah harga, kemudian tolak daripada RM50.'), T('6 × 4 = 24, then 24 + 7 = 31, then 50 − 31 = 19.', '6 × 4 = 24, kemudian 24 + 7 = 31, kemudian 50 − 31 = 19.'), 'kf10c')])
    return L
