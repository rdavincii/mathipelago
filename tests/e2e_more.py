"""
More end-to-end checks (all 36 authored puzzles, adaptive offers, settings, reset, premium preview,
corrupt saves, layout at several screen sizes, keyboard, reduced motion, double-tap protection).
Usage: python tests/e2e_more.py http://localhost:8123/index.html
"""
import os, sys, json, re, os
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from e2e import solve, js, check, results
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8123/index.html'
KEY = 'mathipelago.save'

def seed_all_done(pg, lang='en', band=1):
    js(pg, """([lang,band])=>{ MP.store.update(s=>{ s.lang=lang; s.introDone=true; s.tutorialDone=true; s.band=band; s.coins=200;
        MP.levels.all().forEach(l=>{ s.levels[l.id]={done:true,stars:2,plays:1,lastPuzzle:null,hints:0,wrong:0}; if(s.collection.indexOf(l.critter.id)<0) s.collection.push(l.critter.id); }); });
        MP.app.applySettings(); MP.app.go('menu'); }""", [lang, band])
    pg.wait_for_timeout(200)

def start_level(pg, lid):
    js(pg, "id=>MP.app.go('level',{id})", lid); pg.wait_for_timeout(200)
    if pg.locator('.storycard .btn.big').count(): pg.locator('.storycard .btn.big').click()
    pg.wait_for_timeout(200)

def new_page(b, w=360, h=640, **kw):
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, has_touch=True, is_mobile=(w < 700), **kw)
    pg = ctx.new_page(); pg.problems = []
    if not os.environ.get('TESTMODE'):      # default: behave like the public free demo; TESTMODE=1 keeps premium test packs on
        def _h(route):
            r = route.fetch(); route.fulfill(response=r, body=r.text().replace('devUnlockPremium: true', 'devUnlockPremium: false'))
        pg.route('**/js/config.js', _h)
    pg.on('console', lambda m: pg.problems.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: pg.problems.append('PAGEERROR ' + str(e)))
    return ctx, pg

def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx, pg = new_page(b)
        pg.goto(URL); pg.wait_for_timeout(400)
        pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(400)
        seed_all_done(pg, 'en', 1)

        # ---- every authored puzzle (3 tiers x 12 levels) solved through the real UI ----
        ok_tiers, bad = 0, []
        for band in ((0, 1, 2) if not os.environ.get('SKIP36') else ()):
            for lv in js(pg, "MP.levels.all().map(l=>l.id)"):
                js(pg, "([id,b])=>MP.store.update(s=>{s.band=b;s.topics={};s.struggles=0;s.levels[id].lastPuzzle=null;})", [lv, band])
                start_level(pg, lv)
                pid = js(pg, 'MP.currentPuzzle.id')
                if not pid.endswith('abc'[band]): bad.append((lv, band, pid))
                try:
                    solve(pg, wrong_first=False)
                    pg.wait_for_selector('.dialog-card.complete-card', timeout=8000)
                    ok_tiers += 1
                except Exception as e:
                    bad.append((lv, band, str(e)[:80]))
        if not os.environ.get('SKIP36'): check('all 36 authored puzzles are solvable through the UI at their intended tier', ok_tiers == 36 and not bad, bad)
        pg.screenshot(path='/tmp/shots/after36.png')

        # ---- adaptive: struggle -> friendlier offer + help, topic gets easier ----
        js(pg, "MP.store.update(s=>{s.band=1;s.topics={};s.struggles=0;s.levels['m2-1'].lastPuzzle=null;})")
        start_level(pg, 'm2-1')
        check('band 1 starts on the standard (b) puzzle', js(pg, 'MP.currentPuzzle.id') == 'm2-1-b')
        s = js(pg, 'MP.currentPuzzle.spec')
        badpair = [(i, j) for i in range(len(s['tiles'])) for j in range(len(s['tiles'])) if i < j and s['tiles'][i] * s['tiles'][j] != s['target']][0]
        for _ in range(3):
            pg.locator('.host .tile').nth(badpair[0]).click(); pg.locator('.host .tile').nth(badpair[1]).click(); pg.wait_for_timeout(1000)
        check('after 3 wrong tries a friendlier version is offered', pg.locator('.offers button').count() >= 1)
        check('wrong answers never remove coins', js(pg, 'MP.store.get().coins') >= 200)
        pg.locator('.offers button').first.click(); pg.wait_for_timeout(200)
        check('friendlier version switches to the easier puzzle', js(pg, 'MP.currentPuzzle.id') == 'm2-1-a')
        s = js(pg, 'MP.currentPuzzle.spec')
        badpair = [(i, j) for i in range(len(s['tiles'])) for j in range(len(s['tiles'])) if i < j and s['tiles'][i] * s['tiles'][j] != s['target']][0]
        for _ in range(3):
            pg.locator('.host .tile').nth(badpair[0]).click(); pg.locator('.host .tile').nth(badpair[1]).click(); pg.wait_for_timeout(1000)
        helpbtn = pg.get_by_role('button', name='Show me how')
        check('"Show me how" appears so a child is never stuck', helpbtn.count() == 1)
        helpbtn.click(); pg.get_by_role('button', name='Got it, continue').click()
        pg.wait_for_selector('.dialog-card.complete-card', timeout=5000)
        rec = js(pg, "MP.store.get().levels['m2-1']")
        topic = js(pg, "MP.store.get().topics['operations']")
        check('helped run gives 1 star and topic steps down (friendlier next time)', rec['stars'] >= 1 and topic['adj'] == -1 and topic['review'] is True, [rec, topic])
        # next play of an operations level starts friendlier
        js(pg, "MP.store.update(s=>{s.levels['m2-2'].lastPuzzle=null})")
        start_level(pg, 'm2-2')
        check('next level in that topic starts one step friendlier', js(pg, 'MP.currentPuzzle.id') == 'm2-2-a')
        # clean solves raise difficulty
        js(pg, "MP.store.update(s=>{s.band=1;s.topics={};s.struggles=0;})")
        for lv in ('m1-2', 'm1-4'):
            js(pg, "id=>MP.store.update(s=>{s.levels[id].lastPuzzle=null})", lv)
            start_level(pg, lv); solve(pg); pg.wait_for_selector('.dialog-card.complete-card', timeout=8000)
        check('two clean solves in a topic raise it one step', js(pg, "MP.store.get().topics['operations'].adj") == 1)
        js(pg, "MP.store.update(s=>{s.levels['m2-1'].lastPuzzle=null})")
        start_level(pg, 'm2-1')
        check('then the next puzzle in that topic is the challenge tier', js(pg, 'MP.currentPuzzle.id') == 'm2-1-c')

        # ---- hint ----
        pg.locator('.hintbtn').click()
        check('hint reveals authored hint text', pg.locator('.hintbox').is_visible() and len(pg.locator('.hintbox').inner_text()) > 5)

        # ---- pause + keyboard + focus return ----
        pg.get_by_role('button', name='Pause').click()
        check('pause dialog opens', pg.locator('.dialog-card').count() == 1)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        check('Escape closes pause dialog and puzzle is still there', pg.locator('.dialog-card').count() == 0 and pg.locator('.host').count() == 1)

        # ---- double-tap protection: two rapid clicks on Check give the reward once ----
        js(pg, "MP.store.update(s=>{s.band=0;s.topics={};s.levels['m1-1'].lastPuzzle=null;s.levels['m1-1'].stars=0;s.coins=0})")
        plays0 = js(pg, "MP.store.get().levels['m1-1'].plays")
        start_level(pg, 'm1-1')
        t = js(pg, 'MP.currentPuzzle.spec.target')
        js(pg, "v=>{const r=document.querySelector('.nl-range');r.value=v;r.dispatchEvent(new Event('input',{bubbles:true}))}", t)
        pg.locator('.host .check').dblclick()
        pg.wait_for_selector('.dialog-card.complete-card', timeout=8000)
        coins, stars = js(pg, 'MP.store.get().coins'), js(pg, "MP.store.get().levels['m1-1'].stars")
        plays = js(pg, "MP.store.get().levels['m1-1'].plays")
        check('double-tap does not double the reward', coins == 5 * stars and plays == plays0 + 1, [coins, stars, plays, plays0])

        # ---- settings ----
        js(pg, "MP.app.go('settings')"); pg.wait_for_timeout(150)
        pg.get_by_role('button', name='A++').click()
        check('text size setting applies', js(pg, "getComputedStyle(document.documentElement).fontSize") == '20.8px')
        pg.get_by_role('button', name='Calmer').click()
        check('reduced-motion setting applies', js(pg, "document.documentElement.dataset.motion") == 'reduce')
        pg.get_by_role('button', name='Sound off').click()
        check('sound can be switched off and game still plays', js(pg, 'MP.store.get().sound') is False and js(pg, 'MP.audio.isEnabled()') is False)
        pg.get_by_role('button', name='Sound on').click()
        pg.get_by_role('button', name='A', exact=True).click()
        # reset confirmation
        js(pg, "MP.store.update(s=>{s.coins=77})")
        pg.get_by_role('button', name='Reset my progress').click()
        pg.get_by_role('button', name='No, keep my progress').click(); pg.wait_for_timeout(150)
        check('reset can be cancelled', js(pg, 'MP.store.get().coins') == 77)
        pg.get_by_role('button', name='Reset my progress').click()
        pg.get_by_role('button', name='Yes, reset').click(); pg.wait_for_timeout(250)
        sv = js(pg, 'MP.store.get()')
        check('reset clears progress but keeps language', sv['coins'] == 0 and not sv['levels'] and sv['lang'] == 'en', sv)

        # ---- language switch keeps progress ----
        seed_all_done(pg, 'en', 1)
        before = js(pg, 'JSON.stringify(MP.store.get().levels)')
        pg.get_by_role('button', name=re.compile('Switch language|Tukar bahasa')).click(); pg.wait_for_timeout(150)
        check('quick language switch keeps progress', js(pg, 'JSON.stringify(MP.store.get().levels)') == before and js(pg, 'MP.i18n.lang') == 'ms')
        pg.get_by_role('button', name=re.compile('Switch language|Tukar bahasa')).click()

        # ---- premium preview (honest) ----
        js(pg, "MP.app.go('map')"); pg.wait_for_timeout(300)
        pg.screenshot(path='/tmp/shots/map_top.png')
        check('map teaser is hit-testable by a real tap', js(pg, "(()=>{const t=document.querySelector('.teaser');t.scrollIntoView({block:'center'});const r=t.getBoundingClientRect();return !!document.elementFromPoint(r.x+r.width/2,r.y+r.height/2).closest('.teaser')})()"))
        js(pg, 'window.scrollTo(0,0)'); pg.wait_for_timeout(100); pg.locator('.teaser').first.dispatch_event('click'); pg.wait_for_timeout(200)
        check('premium preview is clearly labelled and says nothing was purchased', pg.locator('.ribbon').inner_text() == 'Premium' and 'nothing here has been purchased' in pg.locator('.notice').inner_text())
        pg.get_by_role('button', name='Ask a grown-up about this pack').click(); pg.wait_for_timeout(150)
        check('no checkout configured -> "not available" (no fake purchase)', 'not available' in pg.locator('.premium [role=status]').inner_text())
        check('premium pack is not owned and has no level data in the bundle', js(pg, "MP.entitlements.hasPack('crystal-caves')") is False and js(pg, "MP.levels.byPack('crystal-caves').length") == 0)
        pg.screenshot(path='/tmp/shots/premium.png')

        # ---- parents + collection + map screens render ----
        js(pg, "MP.app.go('parents')"); pg.wait_for_timeout(200)
        check('parents area lists all 12 levels', pg.locator('.parents tbody tr').count() == 12)
        pg.screenshot(path='/tmp/shots/parents.png', full_page=True)
        js(pg, "MP.app.go('collection')"); pg.wait_for_timeout(200)
        check('collection shows 12 companions', pg.locator('.critters .critter').count() == 12)
        pg.screenshot(path='/tmp/shots/collection.png')

        # ---- keyboard navigation ----
        js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(200)
        pg.keyboard.press('Tab'); pg.keyboard.press('Tab')
        check('Tab moves focus to a real button', js(pg, "document.activeElement && document.activeElement.tagName") in ('BUTTON', 'A'))
        # keyboard-only: slider
        start_level(pg, 'm1-1')
        pg.locator('.nl-range').focus(); pg.keyboard.press('ArrowRight')
        check('number-line slider works with the keyboard', int(js(pg, "document.querySelector('.nl-range').value")) >= 1)
        check('no console errors in extended run', not pg.problems, pg.problems)
        ctx.close()

        # ---- corrupt / malformed saves ----
        for name, payload in (('invalid JSON', '{bad json'), ('wrong types', json.dumps({'coins': 'abc', 'levels': {'x y!': 1, 'm1-1': {'done': 'yes', 'stars': 99}}, 'band': 7, 'lang': 'fr', 'collection': 'no'})), ('array', '[1,2,3]')):
            ctx, pg = new_page(b)
            pg.goto(URL); pg.evaluate("([k,v])=>localStorage.setItem(k,v)", [KEY, payload]); pg.reload(); pg.wait_for_timeout(400)
            sv = js(pg, 'MP.store.get()')
            check('corrupt save (%s) does not crash' % name, not pg.problems and pg.locator('#app > *').count() == 1 and 0 <= sv['band'] <= 2 and sv['coins'] >= 0, pg.problems)
            ctx.close()

        # ---- progress survives refresh ----
        ctx, pg = new_page(b); pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
        seed_all_done(pg, 'en', 2); pg.reload(); pg.wait_for_timeout(400)
        check('progress survives a refresh', js(pg, 'MP.store.get().coins') == 200 and len(js(pg, 'MP.store.get().collection')) == 12)
        ctx.close()

        # ---- layout: no horizontal overflow, tap targets, several screen sizes + both languages ----
        sizes = [(320, 568), (360, 640), (412, 915), (768, 1024), (1280, 800), (640, 360)]
        overflow, small = [], []
        for (w, h) in sizes:
            for lang in ('en', 'ms'):
                ctx, pg = new_page(b, w, h)
                pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
                seed_all_done(pg, lang, 1)
                js(pg, "()=>MP.store.update(s=>{s.textScale=1.3})") if (w, lang) == (320, 'ms') else None
                if (w, lang) == (320, 'ms'): js(pg, "MP.app.applySettings()")
                screens = [('menu', {}), ('map', {}), ('collection', {}), ('settings', {}), ('parents', {}), ('premium', {'id': 'crystal-caves'}), ('demodone', {})]
                for n, prm in screens:
                    js(pg, "([n,p])=>MP.app.go(n,p)", [n, prm]); pg.wait_for_timeout(120)
                    if not js(pg, 'document.documentElement.scrollWidth <= window.innerWidth + 1'): overflow.append((w, lang, n))
                for lid in js(pg, "MP.levels.all().map(l=>l.id)"):
                    js(pg, "([id,b])=>MP.store.update(s=>{s.band=b;s.levels[id].lastPuzzle=null})", [lid, 2 if lid in ('m3-4', 'm2-2') else 1])
                    start_level(pg, lid)
                    if not js(pg, 'document.documentElement.scrollWidth <= window.innerWidth + 1'): overflow.append((w, lang, lid))
                    if w in (360, 320) and lang == 'en':
                        sm = js(pg, """()=>[...document.querySelectorAll('#app button, #app a.btn, #app input')].filter(e=>e.offsetParent!==null).map(e=>{const r=e.getBoundingClientRect();return [e.className+'|'+(e.textContent||'').trim().slice(0,12),Math.round(r.width),Math.round(r.height)]}).filter(x=>Math.min(x[1],x[2])<44)""")
                        for x in sm: small.append((lid, x))
                    if (w, h, lang) == (360, 640, 'en'): pg.screenshot(path='/tmp/shots/lv_%s.png' % lid)
                if overflow and pg.problems: pass
                ctx.close()
        check('no horizontal overflow on any screen/level at 6 sizes x 2 languages (+130% text at 320)', not overflow, overflow[:6])
        check('all tap targets are at least 44px (360x640 / 320x568)', not small, small[:8])

        # ---- reduced motion via OS setting ----
        ctx, pg = new_page(b, reduced_motion='reduce'); pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(300)
        d = js(pg, "(()=>{const e=document.querySelector('.eyes'); return e? getComputedStyle(e).animationDuration : 'none'})()")
        check('OS reduced-motion preference calms blinking and pop animations', d in ('1e-06s', '0.001ms', '0s') or d.startswith('1e-'), d)
        fly = js(pg, "(()=>{const e=document.querySelector('.fly'); return e? getComputedStyle(e).animationDuration : 'none'})()")
        check('...but the gentle mascot flight and sky drift keep going', fly not in ('none', '0s') and not fly.startswith('1e-'), fly)
        js(pg, "MP.store.update(s=>{s.motion='reduce'}); MP.app.applySettings()"); pg.wait_for_timeout(150)
        fly2 = js(pg, "(()=>{const e=document.querySelector('.fly'); return e? getComputedStyle(e).animationDuration : 'none'})()")
        check('choosing Calmer in Settings stops all motion, mascot included', fly2 in ('1e-06s', '0.001ms', '0s') or fly2.startswith('1e-'), fly2)
        ctx.close()
        b.close()
    print(json.dumps({'passed': sum(r['pass'] for r in results), 'failed': sum(not r['pass'] for r in results)}))
    sys.exit(0 if all(r['pass'] for r in results) else 1)

main()
