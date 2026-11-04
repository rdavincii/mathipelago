"""
Authoring helpers for the premium packs. Run `python3 tools/mk/build.py` to (re)generate packs/*.js.
Every answer is COMPUTED here from the numbers (never typed by hand), and the generated files are then
re-checked by tests/run-tests.js with the independent solvers in js/validators.js.
Text is bilingual (en/ms); numbers must be formatted identically in both languages (the tests compare them).
"""
import json, random, itertools, re

def T(en, ms): return {'en': en, 'ms': ms}
def n(v):
    """Number as text, same in both languages (thousands separated by commas like the free levels)."""
    return f'{v:,}' if isinstance(v, int) and abs(v) >= 10000 else str(v)
def rm(sen):
    if sen < 100: return f'{sen} sen'
    r, s = divmod(sen, 100)
    return f'RM{r}' if s == 0 else f'RM{r}.{s:02d}'
def minus(v): return ('−' + str(-v)) if v < 0 else str(v)

def rng_for(*parts): return random.Random('|'.join(map(str, parts)))

def P(type_, spec, prompt, hint, explain):
    return {'type': type_, 'spec': spec, 'prompt': prompt, 'hint': hint, 'explain': explain}

# ---------------------------------------------------------------- families
def tiles(target, tl, hint_a=None):
    pairs = [(a, b) for i, a in enumerate(tl) for j, b in enumerate(tl) if i < j and a * b == target]
    assert pairs, ('no pair', target, tl)
    a, b = pairs[0]
    return P('tiles', {'op': '*', 'target': target, 'tiles': tl},
        T(f'Find two tiles that multiply to {target}.', f'Cari dua jubin yang hasil darabnya {target}.'),
        T(f'What number times {a} makes {target}?', f'Nombor apa didarab dengan {a} menjadi {target}?'),
        T(f'{a} × {b} = {target}.', f'{a} × {b} = {target}.'))

def balance(target, tl, count=None):
    sol = None
    for k in ([count] if count else range(1, len(tl) + 1)):
        for c in itertools.combinations(tl, k):
            if sum(c) == target: sol = c; break
        if sol: break
    assert sol, ('no balance', target, tl, count)
    spec = {'target': target, 'tiles': tl}
    if count: spec['count'] = count
    expr = ' + '.join(map(str, sol))
    return P('balance', spec,
        T(f'Choose exactly {count} crates that add up to {target}.', f'Pilih tepat {count} kotak yang jumlahnya {target}.') if count else T(f'Choose crates that add up to {target}.', f'Pilih kotak yang jumlahnya {target}.'),
        T('Pick one crate first. How much is still needed?', 'Pilih satu kotak dahulu. Berapa lagi yang diperlukan?'),
        T(f'{expr} = {target}.', f'{expr} = {target}.'))

def numberline(target, mn, mx, step, label, start=None, kind='at', a=None, b=None, x=None, unit=None):
    assert (target - mn) % step == 0 and mn <= target <= mx
    if start is None: start = mn + step * 2 if mn + step * 2 != target else mn + step
    spec = {'min': mn, 'max': mx, 'step': step, 'labelEvery': label, 'target': target, 'start': start}
    tv, av, bv = minus(target), (minus(a) if a is not None else ''), (minus(b) if b is not None else '')
    if kind == 'half':
        return P('numberline', spec,
            T(f'Place the plank exactly halfway between {av} and {bv}.', f'Letakkan papan tepat di tengah-tengah antara {av} dan {bv}.'),
            T(f'Add the two numbers and halve the answer, or find the gap and halve it.', f'Tambah kedua-dua nombor dan bahagi dua jawapannya, atau cari jarak dan bahagi dua.'),
            T(f'The gap from {av} to {bv} is {abs(b - a)}. Half of that is {abs(b - a) // 2}, so the middle is {tv}.', f'Jarak dari {av} ke {bv} ialah {abs(b - a)}. Separuhnya ialah {abs(b - a) // 2}, jadi titik tengah ialah {tv}.'))
    if kind == 'round':
        u = unit
        return P('numberline', spec,
            T(f'Place the plank at {x} rounded to the nearest {u}.', f'Letakkan papan pada {x} yang dibundarkan kepada {u} yang terdekat.'),
            T(f'Look at the digit after the {u}s place. 5 or more rounds up.', f'Lihat digit selepas tempat {u}. 5 atau lebih dibundarkan ke atas.'),
            T(f'{x} is closest to {tv}, so the plank goes at {tv}.', f'{x} paling hampir dengan {tv}, jadi papan diletakkan di {tv}.'))
    return P('numberline', spec,
        T(f'Place the plank at {tv}.', f'Letakkan papan di nombor {tv}.'),
        T(f'Find the nearest labelled number, then count on or back in steps of {step}.', f'Cari nombor berlabel yang terdekat, kemudian kira ke hadapan atau ke belakang dengan langkah {step}.'),
        T(f'Count in steps of {step} along the line to reach {tv}.', f'Kira dengan langkah {step} sepanjang garis untuk sampai ke {tv}.'))

def share(items, baskets):
    assert items % baskets == 0 and items <= 30 and 2 <= baskets <= 5
    q = items // baskets
    return P('share', {'items': items, 'baskets': baskets},
        T(f'Share {items} berries fairly between {baskets} baskets.', f'Kongsi {items} biji beri dengan adil dalam {baskets} bakul.'),
        T('Fair means every basket gets the same number. Deal them out one at a time.', 'Adil bermaksud setiap bakul mendapat bilangan yang sama. Edarkan satu demi satu.'),
        T(f'{items} ÷ {baskets} = {q}, so each basket gets {q}.', f'{items} ÷ {baskets} = {q}, jadi setiap bakul mendapat {q}.'))

def _seq(rule):
    k = rule['kind']
    if k == 'arith': return [rule['start'] + rule['step'] * i for i in range(rule['length'])]
    if k == 'geo': return [rule['start'] * rule['mult'] ** i for i in range(rule['length'])]
def pattern(kind, start, d, length, hidden=None, options=None, seed='x'):
    rule = {'kind': kind, 'start': start, ('step' if kind == 'arith' else 'mult'): d, 'length': length}
    seq = _seq(rule); hid = length - 1 if hidden is None else hidden
    ans = seq[hid]; r = rng_for(seed, start, d)
    if options is None:
        cands = [ans + d, ans - d, ans + 1, ans - 1, ans * 2, ans + 10, ans - 10, ans + 2] if kind == 'arith' else [ans + start, ans * 2, ans + d, ans - 1, ans * d + 1, ans + 10, ans - 10]
        opts = []
        for c in cands:
            if c != ans and c not in opts and c >= (0 if min(seq) >= 0 else -999): opts.append(c)
        r.shuffle(opts); opts = opts[:3] + [ans]; r.shuffle(opts)
    else: opts = options
    prev = seq[hid - 1] if hid > 0 else seq[hid + 1]
    if kind == 'arith':
        up = d > 0; ad = abs(d)
        expl = (T(f'The numbers go {"up" if up else "down"} by {ad} each time: {minus(prev)} {"+" if up else "−"} {ad} = {minus(ans)}.', f'Nombor {"bertambah" if up else "berkurang"} {ad} setiap kali: {minus(prev)} {"+" if up else "−"} {ad} = {minus(ans)}.') if hid > 0 else
                T(f'The numbers go {"up" if up else "down"} by {ad} each time, so the first number is {minus(ans)}.', f'Nombor {"bertambah" if up else "berkurang"} {ad} setiap kali, jadi nombor pertama ialah {minus(ans)}.'))
        hint = T('How much does each number go up or down by?', 'Setiap nombor bertambah atau berkurang berapa?')
    else:
        expl = T(f'Each number is multiplied by {d}: {prev} × {d} = {ans}.', f'Setiap nombor didarab dengan {d}: {prev} × {d} = {ans}.')
        hint = T(f'Each number is {d} times the one before it.', f'Setiap nombor ialah {d} kali nombor sebelumnya.')
    prompt = T('Which number comes next?', 'Nombor manakah yang seterusnya?') if hid == length - 1 else T('Which number is missing?', 'Nombor manakah yang hilang?')
    return P('pattern', {'rule': rule, 'hidden': hid, 'options': opts}, prompt, hint, expl)

def match(pairs, prompt=None, hint=None):
    ps = [{'id': 'abcdefg'[i], 'left': l, 'right': rr} for i, (l, rr) in enumerate(pairs)]
    assert len({p['right'] for p in ps}) == len(ps)
    expl = '; '.join(f'{l} = {rr}' for l, rr in pairs)
    return P('match', {'pairs': ps},
        prompt or T('Tap a question, then tap its answer.', 'Ketik satu soalan, kemudian ketik jawapannya.'),
        hint or T('Start with the one you know best.', 'Mulakan dengan yang paling anda tahu.'),
        T(expl + '.', expl + '.'))

def placevalue(target, places):
    names_en = {1: 'ones', 10: 'tens', 100: 'hundreds', 1000: 'thousands'}; names_ms = {1: 'sa', 10: 'puluh', 100: 'ratus', 1000: 'ribu'}
    ds, rest = [], target
    for p in places:
        ds.append(rest // p); rest %= p
    assert rest == 0
    # note: places are given highest first
    parts = ' + '.join(str(d * p) for d, p in zip(ds, places))
    return P('placeValue', {'places': places, 'target': target},
        T(f'Build the number {n(target)}.', f'Bina nombor {n(target)}.'),
        T('Say the number out loud and think about how many of each place it needs.', 'Sebut nombor itu dan fikirkan berapa banyak setiap tempat yang diperlukan.'),
        T(f'{n(target)} = {parts}.', f'{n(target)} = {parts}.'))

def digitarrange(digits, goal):
    best = None
    for p in itertools.permutations(digits):
        if p[0] == 0: continue
        v = int(''.join(map(str, p)))
        if best is None or (v < best if goal == 'smallest' else v > best): best = v
    k = len(digits)
    gs = ('smallest', 'terkecil') if goal == 'smallest' else ('largest', 'terbesar')
    return P('digitArrange', {'digits': digits, 'goal': goal, 'noLeadingZero': True},
        T(f'Arrange the tiles to make the {gs[0]} {k}-digit number. A number cannot start with 0.', f'Susun jubin untuk membentuk nombor {k} digit yang paling {"kecil" if goal == "smallest" else "besar"}. Nombor tidak boleh bermula dengan 0.'),
        T(f'Put the {"smallest" if goal == "smallest" else "biggest"} allowed digit in the highest place first.', f'Letakkan digit {"terkecil" if goal == "smallest" else "terbesar"} yang dibenarkan pada tempat tertinggi dahulu.'),
        T(f'The {gs[0]} number is {n(best)}.', f'Nombor {gs[1]} ialah {n(best)}.'))

def coins(target, cl, exact=None):
    # find a representation (min coins, or exactly `exact`)
    best = None
    def rec(i, rem, used):
        nonlocal best
        if rem == 0:
            if (exact is None or len(used) == exact) and (best is None or len(used) < len(best) or exact): best = best or list(used)
            return
        if best and exact: return
        if i < 0 or (exact and len(used) >= exact): return
        c = cl[i]
        for k in range(rem // c, -1, -1):
            rec(i - 1, rem - k * c, used + [c] * k)
    cl = sorted(cl); rec(len(cl) - 1, target, [])
    assert best, ('no coins', target, cl, exact)
    spec = {'target': target, 'coins': cl}
    if exact: spec['exactCount'] = exact
    expr = ' + '.join(map(str, best))
    tt = rm(target)
    return P('coins', spec,
        T(f'Pay exactly {tt} using exactly {exact} pieces of money.', f'Bayar tepat {tt} menggunakan tepat {exact} keping wang.') if exact else T(f'Pay exactly {tt}.', f'Bayar tepat {tt}.'),
        T('Start with the biggest coin that fits. How much is left to pay?', 'Mulakan dengan syiling terbesar yang muat. Berapa lagi yang tinggal untuk dibayar?'),
        T(f'{expr} = {target} sen = {tt}.', f'{expr} = {target} sen = {tt}.'))

def tank(parts, nn, d):
    assert (nn * parts) % d == 0
    segs = nn * parts // d
    return P('tank', {'parts': parts, 'n': nn, 'd': d},
        T(f'Fill the tank to {nn}/{d}.', f'Isi tangki hingga {nn}/{d}.'),
        T(f'{nn}/{d} means {nn} out of every {d} equal parts. This tank has {parts} parts.', f'{nn}/{d} bermaksud {nn} daripada setiap {d} bahagian sama saiz. Tangki ini ada {parts} bahagian.'),
        T(f'{nn}/{d} = {segs}/{parts}, so fill {segs} of the {parts} parts.', f'{nn}/{d} = {segs}/{parts}, jadi isi {segs} daripada {parts} bahagian.'))

def shapes_sides(k, items, name_en, name_ms):
    right = sum(1 for it in items if (it['sides'] if it['k'] == 'poly' else 0 if it['k'] == 'circle' else 4) == k)
    assert 1 <= right < len(items)
    return P('shapes', {'predicate': f'sides:{k}', 'items': items},
        T(f'Tap all the shapes with {k} sides ({name_en}).', f'Ketik semua bentuk yang mempunyai {k} sisi ({name_ms}).'),
        T('Count the straight sides of each shape. A circle has none.', 'Kira sisi lurus setiap bentuk. Bulatan tidak mempunyai sisi lurus.'),
        T(f'{right} of the shapes have exactly {k} sides.', f'{right} daripada bentuk itu mempunyai tepat {k} sisi.'))

def _rects(spec_list):
    cols = ['sky', 'mint', 'coral', 'sun', 'grape', 'sky']
    return [{'k': 'rect', 'w': w, 'h': h, 'color': cols[i % 6], 'grid': True} for i, (w, h) in enumerate(spec_list)]
def shapes_perimeter(P_, rl):
    items = _rects(rl); ok = [f'{w}×{h}' for w, h in rl if 2 * (w + h) == P_]
    assert 1 <= len(ok) < len(rl)
    others = ', '.join(str(2 * (w + h)) for w, h in rl if 2 * (w + h) != P_)
    return P('shapes', {'predicate': f'perimeter:{P_}', 'items': items},
        T(f'Each small square is 1 unit. Tap all the rectangles with a perimeter of {P_} units.', f'Setiap petak kecil ialah 1 unit. Ketik semua segi empat tepat yang perimeternya {P_} unit.'),
        T('Perimeter is the distance around: 2 × (length + width).', 'Perimeter ialah jarak mengelilingi: 2 × (panjang + lebar).'),
        T(f'{", ".join(ok)} each have a perimeter of {P_}. The others have {others}.', f'{", ".join(ok)} masing-masing mempunyai perimeter {P_}. Yang lain ialah {others}.'))
def shapes_area(A_, rl):
    items = _rects(rl); ok = [f'{w}×{h}' for w, h in rl if w * h == A_]
    assert 1 <= len(ok) < len(rl)
    others = ', '.join(str(w * h) for w, h in rl if w * h != A_)
    return P('shapes', {'predicate': f'area:{A_}', 'items': items},
        T(f'Each small square is 1 unit. Tap all the rectangles with an area of {A_} square units.', f'Setiap petak kecil ialah 1 unit. Ketik semua segi empat tepat yang luasnya {A_} unit persegi.'),
        T('Area is length × width, or count the small squares.', 'Luas ialah panjang × lebar, atau kira petak kecil.'),
        T(f'{", ".join(ok)} each have an area of {A_}. The others have {others}.', f'{", ".join(ok)} masing-masing mempunyai luas {A_}. Yang lain ialah {others}.'))

def chart(bars, ask, noun, axis_step=None):
    """bars: list of (label T, value, colour). ask: ('diff',i,j) | ('sum',[i..]) | ('mean',). noun: T plural, e.g. T('fish','ikan')."""
    vals = [b[1] for b in bars]; mx = max(vals)
    step = axis_step or next(s for s in (1, 2, 5, 10, 20, 25, 50) if mx / s <= 8)
    top = ((mx + step - 1) // step) * step
    if ask[0] == 'diff':
        i, j = ask[1], ask[2]; ans = vals[i] - vals[j]
        A, B = bars[i][0], bars[j][0]
        prompt = T(f'How many more {A["en"]} than {B["en"]} are there?', f'Berapa banyak {A["ms"]} lebih daripada {B["ms"]}?')
        hint = T('Read the two bars, then subtract the smaller from the bigger.', 'Baca dua palang itu, kemudian tolak yang kecil daripada yang besar.')
        expl = T(f'{vals[i]} − {vals[j]} = {ans} more {A["en"]}.', f'{vals[i]} − {vals[j]} = {ans} {A["ms"]} lebih.')
        a = {'op': 'diff', 'a': i, 'b': j}
    elif ask[0] == 'sum':
        idx = ask[1]; ans = sum(vals[k] for k in idx)
        if len(idx) == len(bars):
            prompt = T(f'How many {noun["en"]} are there altogether?', f'Berapakah jumlah semua {noun["ms"]}?')
            hint = T('Read every bar, then add them together.', 'Baca setiap palang, kemudian tambahkannya.')
        else:
            names_en = ' and '.join(bars[k][0]['en'] for k in idx); names_ms = ' dan '.join(bars[k][0]['ms'] for k in idx)
            prompt = T(f'How many {names_en} are there together?', f'Berapakah {names_ms} jika digabungkan?')
            hint = T('Find only those bars, then add them.', 'Cari palang-palang itu sahaja, kemudian tambahkannya.')
        ex = ' + '.join(str(vals[k]) for k in idx)
        expl = T(f'{ex} = {ans}.', f'{ex} = {ans}.')
        a = {'op': 'sum', 'of': idx}
    else:
        tot = sum(vals); assert tot % len(vals) == 0; ans = tot // len(vals)
        prompt = T(f'What is the mean (average) number of {noun["en"]} in each group?', f'Berapakah min (purata) bilangan {noun["ms"]} dalam setiap kumpulan?')
        hint = T(f'Add all the bars, then divide by {len(vals)}.', f'Tambah semua palang, kemudian bahagi dengan {len(vals)}.')
        ex = ' + '.join(map(str, vals))
        expl = T(f'{ex} = {tot}, and {tot} ÷ {len(vals)} = {ans}.', f'{ex} = {tot}, dan {tot} ÷ {len(vals)} = {ans}.')
        a = {'op': 'mean'}
    return P('chart', {'axisMax': top, 'axisStep': step, 'bars': [{'label': l, 'value': v, 'color': c} for l, v, c in bars], 'ask': a}, prompt, hint, expl)

# ---- multi-step
def step(q, val, calc, fmt=None):
    return {'q': q, 'val': val, 'calc': calc, 'fmt': fmt or (lambda v: ('%g' % v))}
def steps(sl, hint, explain, seed):
    out = []
    for i, st in enumerate(sl):
        v = st['val']; r = rng_for(seed, i, v)
        if isinstance(v, float) and v != int(v):
            cands = [v + .5, v - .5, v + 1, v - 1, v + .1, v - .1, v * 2, v + 10, v + .25, v - .25]
        else:
            cands = [v + 1, v - 1, v + 10, v - 10, v * 2, v + 2, v - 2, v // 2 if v % 2 == 0 and v > 1 else v + 3, v + 5, v - 5, v + 100]
        r.shuffle(cands)
        opts = []
        for c in cands:
            c = round(c, 2)
            if c != v and c not in opts and (c >= 0 or v < 0): opts.append(c)
            if len(opts) == 3: break
        allv = opts + [v]; r.shuffle(allv)
        out.append({'q': st['q'], 'choices': [st['fmt'](x) for x in allv], 'answer': allv.index(v), 'calc': st['calc']})
    return P('steps', {'steps': out}, T('Solve each step in order.', 'Selesaikan setiap langkah mengikut urutan.'), hint, explain)

# ---------------------------------------------------------------- critters + levels
BODIES = ['blob', 'round', 'tall', 'drop', 'cloud']
EARS = ['none', 'round', 'point', 'leaf']
FEATS = ['none', 'antenna', 'horn', 'fin', 'tuft', 'spikes']
ACCS = ['none', 'none', 'goggles', 'hat', 'crown', 'scarf', 'leafcrown']
COLS = [('#ffb3a8', '#ef6f5e'), ('#ffd6a0', '#e8a050'), ('#fff3a8', '#ffd84d'), ('#bff5a8', '#6fd45a'), ('#a8f0e0', '#3fc0a8'),
        ('#bff0ff', '#6fd0f0'), ('#9fc4ff', '#5f8ff0'), ('#c9a0ff', '#9b6cff'), ('#ffb3f0', '#d26be0'), ('#ffc2d8', '#ff7fa6'),
        ('#e6dccf', '#b79c84'), ('#d4f0a0', '#9ac43c')]
def look_for(seed):
    r = rng_for('look', seed); c = r.choice(COLS)
    return {'body': r.choice(BODIES), 'c1': c[0], 'c2': c[1], 'ears': r.choice(EARS), 'feat': r.choice(FEATS), 'acc': r.choice(ACCS)}

def level(pack_code, idx, order, topic, skill, band, scene, title, story, learn, cname, cblurb, tiers):
    lid = f'{pack_code}-{idx}'
    for t_, k in zip(tiers, 'abc'): t_['id'] = f'{lid}-{k}'
    return {'id': lid, 'order': order, 'topic': topic, 'skill': skill, 'band': band, 'scene': scene,
            'title': title, 'story': story, 'learn': learn,
            'critter': {'id': re.sub(r'[^a-z0-9]', '', cname.lower()) + pack_code.replace('-', ''), 'name': T(cname, cname), 'blurb': cblurb, 'look': look_for(lid)},
            'tiers': [{'id': t_['id'], 'type': t_['type'], 'prompt': t_['prompt'], 'hint': t_['hint'], 'explain': t_['explain'], 'spec': t_['spec']} for t_ in tiers]}

def emit(path, pack_id, island_id, npc, title, levels, append_to=None):
    body = ''.join('  lvl(' + json.dumps(l, ensure_ascii=False, separators=(',', ':')) + ');\n' for l in levels)
    if append_to:
        s = open(path).read()
        marker = '/* ---- generated levels ---- */'
        if marker in s: s = s[:s.index(marker)].rstrip() + '\n})();\n'
        i = s.rindex('})();')
        s = s[:i] + '  ' + marker + '\n' + body + s[i:]
        open(path, 'w').write(s)
        return
    open(path, 'w').write(f"""/*
 * PREMIUM TEST PACK: {title} ({len(levels)} levels).
 * GENERATED by tools/mk (python3 tools/mk/build.py): edit the generator, not this file.
 * Not part of the free bundle; loaded only in test mode (MP.config.devUnlockPremium). Same level format as js/levels/registry.js.
 */
(function () {{
  'use strict';
  function lvl(o) {{ o.pack = {json.dumps(pack_id)}; o.island = {json.dumps(island_id)}; o.npc = {json.dumps(npc)}; window.MP.levels.register(o); }}
{body}}})();
""")
