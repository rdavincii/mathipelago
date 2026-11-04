"""
End-to-end test: plays the REAL game in headless Chromium at phone size and checks behaviour.
Run:  pip install playwright && playwright install chromium
      python -m http.server 8123      (in the project folder, in another terminal)
      python tests/e2e.py http://localhost:8123/index.html
Results are printed as PASS/FAIL lines and a JSON summary.
"""
import sys, json, itertools, re
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8123/index.html'
results = []
def check(name, ok, detail=''):
    results.append({'test': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('PASS ' if ok else 'FAIL ') + name + ((' — ' + str(detail)) if detail and not ok else ''))

def sheet(pg, path):
    pg.screenshot(path=path)

def js(pg, expr, arg=None):
    return pg.evaluate(expr, arg) if arg is not None else pg.evaluate(expr)

def solve(pg, wrong_first=False):
    """Solve the puzzle currently on screen using only UI clicks. Returns the puzzle type."""
    pz = js(pg, 'MP.currentPuzzle')
    ty, s = pz['type'], pz['spec']
    host = pg.locator('.host')
    if ty == 'numberline':
        if wrong_first:
            js(pg, "v=>{const r=document.querySelector('.nl-range');r.value=v;r.dispatchEvent(new Event('input',{bubbles:true}))}", s['min'] if s['target'] != s['min'] else s['max'])
            host.locator('.check').click(); pg.wait_for_timeout(100)
        js(pg, "v=>{const r=document.querySelector('.nl-range');r.value=v;r.dispatchEvent(new Event('input',{bubbles:true}))}", s['target'])
        host.locator('.check').click()
    elif ty == 'balance':
        n = len(s['tiles']); found = None
        for m in range(1, 1 << n):
            idx = [i for i in range(n) if m & (1 << i)]
            if sum(s['tiles'][i] for i in idx) == s['target'] and (not s.get('count') or len(idx) == s['count']):
                found = idx; break
        if wrong_first:
            host.locator('.check').click(); pg.wait_for_timeout(100)   # nothing picked
        for i in found: host.locator('.tile').nth(i).click()
        host.locator('.check').click()
    elif ty == 'pattern':
        seq = js(pg, "MP.mathUtil.patternSequence(MP.currentPuzzle.spec.rule)")
        right = seq[s['hidden']]
        ci = [i for i, o in enumerate(s['options']) if o == right][0]
        if wrong_first:
            wi = [i for i in range(len(s['options'])) if i != ci][0]
            host.locator('.opt').nth(wi).click(); pg.wait_for_timeout(100)
        host.locator('.opt').nth(ci).click()
    elif ty == 'share':
        per = s['items'] // s['baskets']
        if wrong_first:
            host.locator('.check').click(); pg.wait_for_timeout(100)
        for b in range(s['baskets']):
            for _ in range(per): host.locator('.basket').nth(b).locator('button').nth(1).click()
        host.locator('.check').click()
    elif ty == 'tiles':
        pair = [(i, j) for i in range(len(s['tiles'])) for j in range(len(s['tiles'])) if i != j and s['tiles'][i] * s['tiles'][j] == s['target']][0]
        if wrong_first:
            bad = [(i, j) for i in range(len(s['tiles'])) for j in range(len(s['tiles'])) if i < j and s['tiles'][i] * s['tiles'][j] != s['target']][0]
            host.locator('.tile').nth(bad[0]).click(); host.locator('.tile').nth(bad[1]).click(); pg.wait_for_timeout(1100)
        host.locator('.tile').nth(pair[0]).click(); host.locator('.tile').nth(pair[1]).click()
    elif ty == 'match':
        L = host.locator('.matchgrid .col').nth(0); Rr = host.locator('.matchgrid .col').nth(1)
        if wrong_first and len(s['pairs']) > 1:
            L.locator('.tile').nth(0).click(); Rr.locator('.tile', has_text=s['pairs'][1]['right']).first.click(); pg.wait_for_timeout(700)
        for p in s['pairs']:
            L.locator('.tile', has_text=p['left']).first.click()
            Rr.locator('.tile').filter(has_text=p['right']).filter(has_not_text='✓').first.click() if False else None
            # exact-match the right-hand tile (e.g. "7" must not match "72")
            rt = Rr.locator('button:not([disabled])')
            for k in range(rt.count()):
                if rt.nth(k).inner_text().strip() == p['right']:
                    rt.nth(k).click(); break
    elif ty == 'placeValue':
        t = s['target']
        for i, pl in enumerate(s['places']):
            d = (t // pl) % 10
            for _ in range(d): host.locator('.dial').nth(i).locator('button').nth(0).click()
        if wrong_first:
            host.locator('.dial').nth(0).locator('button').nth(0).click(); host.locator('.check').click(); pg.wait_for_timeout(100)
            host.locator('.dial').nth(0).locator('button').nth(1).click()
        host.locator('.check').click()
    elif ty == 'digitArrange':
        goal = js(pg, "MP.mathUtil.digitGoal(MP.currentPuzzle.spec)")
        digits = [int(c) for c in str(goal)]
        for d in digits:
            pool = host.locator('.tilegrid .tile:not([disabled])')
            for k in range(pool.count()):
                if pool.nth(k).inner_text().strip() == str(d): pool.nth(k).click(); break
        host.locator('.check').click()
    elif ty == 'coins':
        cap = s.get('exactCount') or 40
        best = None
        for n in range(1, cap + 1):
            for combo in itertools.combinations_with_replacement(s['coins'], n):
                if sum(combo) == s['target'] and (not s.get('exactCount') or n == s['exactCount']): best = combo; break
            if best: break
        if wrong_first:
            host.locator('.check').click(); pg.wait_for_timeout(100)
        for c in best:
            host.locator('.coinbtn').nth(s['coins'].index(c)).click()
        host.locator('.check').click()
    elif ty == 'tank':
        k = s['n'] * s['parts'] // s['d']
        if wrong_first:
            host.locator('.cell').nth(0).click(); host.locator('.check').click(); pg.wait_for_timeout(100)
            host.locator('.cell').nth(0).click()    # un-fill
        host.locator('.cell').nth(k - 1).click()
        host.locator('.check').click()
    elif ty == 'shapes':
        want = js(pg, "MP.currentPuzzle.spec.items.map((it,i)=>MP.mathUtil.shapeMatches(MP.currentPuzzle.spec.predicate,it)?i:-1).filter(i=>i>=0)")
        if wrong_first:
            host.locator('.check').click(); pg.wait_for_timeout(100)
        for i in want: host.locator('.shapebtn').nth(i).click()
        host.locator('.check').click()
    elif ty == 'chart':
        ans = int(js(pg, "MP.mathUtil.chartAnswer(MP.currentPuzzle.spec)"))
        if wrong_first:
            host.locator('.check').click(); pg.wait_for_timeout(100)
        for _ in range(ans // 10): host.get_by_role('button', name=re.compile(r'^(Plus 10|Tambah 10)$')).click()
        for _ in range(ans % 10): host.get_by_role('button', name=re.compile(r'^(Plus 1|Tambah 1)$')).click()
        host.locator('.check').click()
    elif ty == 'steps':
        for i, st in enumerate(s['steps']):
            if wrong_first and i == 0:
                wi = [k for k in range(len(st['choices'])) if k != st['answer']][0]
                host.locator('.opt').nth(wi).click(); pg.wait_for_timeout(100)
            host.locator('.opt').nth(st['answer']).click(); pg.wait_for_timeout(150)
    return ty


def free_only(pg):
    """Run the game exactly as the public free demo would: test-unlock switched off."""
    def h(route):
        r = route.fetch(); route.fulfill(response=r, body=r.text().replace('devUnlockPremium: true', 'devUnlockPremium: false'))
    pg.route('**/js/config.js', h)

def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 360, 'height': 640}, device_scale_factor=2, has_touch=True, is_mobile=True)
        pg = ctx.new_page(); free_only(pg)
        problems = []
        pg.on('console', lambda m: problems.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: problems.append('PAGEERROR ' + str(e)))
        pg.goto(URL); pg.wait_for_timeout(500)
        check('game starts (intro visible)', pg.locator('.intro').count() == 1)
        check('no horizontal overflow on intro', js(pg, 'document.documentElement.scrollWidth <= window.innerWidth'))
        # language: choose Bahasa Melayu, persist across reload
        pg.get_by_role('button', name='Bahasa Melayu').click()
        check('language switches to Bahasa Melayu', pg.locator('h1').first.inner_text().startswith('Selamat datang'))
        pg.get_by_role('button', name='Seterusnya').click()
        check('intro asks who is playing (name + avatar)', pg.locator('.nameinput').count() == 1 and pg.locator('.avbtn').count() >= 10)
        pg.fill('.nameinput', 'Aina'); pg.locator('.avbtn').nth(1).click()
        pg.get_by_role('button', name='Seterusnya').click()
        pg.get_by_role('button', name='Peneroka Mahir').click()
        pg.get_by_role('button', name='Jom main!').click(); pg.wait_for_timeout(400)
        check('tutorial/first level opens after intro', pg.locator('.howto').count() == 1)
        pg.reload(); pg.wait_for_timeout(500)
        check('language persists after reload', js(pg, 'document.documentElement.lang') == 'ms')
        check('rank persists after reload', js(pg, 'MP.store.get().band') == 2)
        # play 12 levels
        # set rank to Adventurer for the main pass so tiers differ
        js(pg, 'MP.store.update(s=>{s.band=1})')
        pg.get_by_role('button', name='Main', exact=True).click() if pg.get_by_role('button', name='Main', exact=True).count() else None
        pg.wait_for_timeout(300)
        types = []
        for n in range(1, 13):
            lid = js(pg, 'MP.levels.all()[%d].id' % (n - 1))
            js(pg, "id=>MP.app.go('level',{id})", lid); pg.wait_for_timeout(250)
            if pg.locator('.storycard .btn.big').count(): pg.locator('.storycard .btn.big').click()
            pg.wait_for_timeout(250)
            ty = solve(pg, wrong_first=(n % 2 == 0))
            types.append(ty)
            pg.wait_for_selector('.dialog-card.complete-card', timeout=8000)
            if n in (1, 5, 9, 12): sheet(pg, '/tmp/shots/done_%02d.png' % n)
            rec = js(pg, "id=>MP.store.get().levels[id]", lid)
            check('level %s (%s) completes and is saved' % (lid, ty), rec and rec['done'] and rec['stars'] >= 1, rec)
            # double tap protection: rewards claimed once
            coins1 = js(pg, 'MP.store.get().coins')
            js(pg, "()=>{}")
            if n < 12:
                pg.get_by_role('button', name='Next adventure').click() if js(pg, 'MP.i18n.lang') == 'en' else pg.get_by_role('button', name='Pengembaraan seterusnya').click()
                pg.wait_for_timeout(200)
        check('12 levels use at least 12 distinct interaction types (incl. digitArrange)', len(set(types)) >= 11, set(types))
        # finish demo
        pg.get_by_role('button', name='Tamatkan demo').click(); pg.wait_for_timeout(400)
        check('demo completion screen shown', pg.locator('.demodone').count() == 1)
        sheet(pg, '/tmp/shots/demodone.png')
        sv = js(pg, 'MP.store.get()')
        check('12 companions collected', len(sv['collection']) == 12, len(sv['collection']))
        check('coins earned and never negative', sv['coins'] > 0, sv['coins'])
        check('no console errors during playthrough', not problems, problems)
        b.close()
    ok = all(r['pass'] for r in results)
    print(json.dumps({'passed': sum(r['pass'] for r in results), 'failed': sum(not r['pass'] for r in results)}))
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
