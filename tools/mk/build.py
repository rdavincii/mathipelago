#!/usr/bin/env python3
"""Regenerates the generated premium levels into packs/*.js.  Usage: python3 tools/mk/build.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib, p_extras, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30
PK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'packs')

NEW = [  # file/pack id, island theme, npc, title, module
    ('mechanical-forest', 'foundry', 'cogg', 'The Mechanical Forest', p03),
    ('hidden-city', 'city', 'sleuth', 'The Hidden City', p04),
    ('clock-harbour', 'harbour', 'tick', 'Clock Harbour', p05),
    ('spice-market', 'market', 'mango', 'Spice Market', p06),
    ('decimal-dunes', 'desert', 'dune', 'Decimal Dunes', p07),
    ('frost-peaks', 'snow', 'frost', 'Frost Peaks', p08),
    ('data-reef', 'reef', 'coral', 'Data Reef', p09),
    ('star-station', 'space', 'nova', 'Star Station', p10),
    ('ember-volcano', 'volcano', 'ember', 'Champion Tables & Ember Volcano', p11),
    ('pirate-cove', 'pirate', 'jolly', 'Treasure Maths & Pirate Cove', p12),
    ('jungle-canopy', 'jungle', 'vine', 'Shape Safari & Jungle Canopy', p13),
    ('candy-kingdom', 'candy', 'sprinkle', 'Sweet Fractions & Candy Kingdom', p14),
    ('dino-valley', 'dino', 'rex', 'Giant Numbers & Dino Valley', p15),
    ('robot-factory', 'robot', 'bolt', 'Rule Machines & Robot Factory', p16),
    ('sports-arena', 'arena', 'goal', 'Scoreboard Maths & Sports Arena', p17),
    ('castle-keep', 'castle', 'knight', 'Castle Builders & Castle Keep', p18),
    ('rainbow-bridge', 'rainbow', 'arc', 'Rainbow Fractions & Rainbow Bridge', p19),
    ('carnival-night', 'carnival', 'jester', 'Grand Finale & Carnival Night', p20),
    ('kampung-village', 'kampung', 'ayam', 'Kampung Village', p21),
    ('night-market', 'nightmarket', 'satay', 'Night Market', p22),
    ('kite-fields', 'kites', 'layang', 'Kite Fields', p23),
    ('train-station', 'train', 'choo', 'Train Station', p24),
    ('bakery-bay', 'bakery', 'bun', 'Bakery Bay', p25),
    ('deep-ocean', 'deep', 'bubbo', 'Deep Ocean', p26),
    ('zoo-park', 'zoo', 'zebra', 'Zoo Park', p27),
    ('toy-workshop', 'toys', 'teddy', 'Toy Workshop', p28),
    ('treehouse-town', 'treehouse', 'acorn', 'Treehouse Town', p29),
    ('lantern-festival', 'festival', 'lampu', 'Lantern Festival', p30),
]
for pid, isl, npc, title, mod in NEW:
    lv = mod.build()
    lib.emit(os.path.join(PK, pid + '.js'), pid, isl, npc, title, lv)
    print(pid, len(lv))

lib.emit(os.path.join(PK, 'crystal-caves.js'), 'crystal-caves', 'cave', 'glim', '', p_extras.crystal(), append_to=True)
gp = os.path.join(PK, 'floating-gardens.js')
s = open(gp).read()
s = re.sub(r"(id: 'g1-(\d+)', order: )\d+", lambda m: m.group(1) + str(22 + int(m.group(2))), s)
open(gp, 'w').write(s)
lib.emit(gp, 'floating-gardens', 'garden', 'petal', '', p_extras.gardens(), append_to=True)
print('ok')
