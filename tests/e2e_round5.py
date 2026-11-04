"""
Round 5 browser checks: sound engine wake-up, daily gift (streak), version info, level-milestone finds, dashed map path.
Usage: python tests/e2e_round5.py http://localhost:8123/index.html
"""
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from e2e import solve, js, check, results
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8123/index.html'

def page(b, w=390, h=844):
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); pg.problems = []
    pg.on('console', lambda m: pg.problems.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: pg.problems.append('PAGEERROR ' + str(e)))
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    return ctx, pg

SEED = """(n)=>{MP.store.update(s=>{s.introDone=true;s.tutorialDone=true;s.lang='en';s.coins=0;
  MP.levels.all().slice(0,n).forEach(l=>{s.levels[l.id]={done:true,stars:3,plays:1,lastPuzzle:null,hints:0,wrong:0}; s.collection.push(l.critter.id)});}); MP.app.go('menu');}"""

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--autoplay-policy=user-gesture-required'])

        # ---------- sound engine ----------
        ctx, pg = page(b)
        check('sound: no audio engine before the first tap', js(pg, "MP.audio.state()") == 'none')
        pg.mouse.click(200, 400); pg.wait_for_timeout(400)
        check('sound: first tap anywhere wakes the engine', js(pg, "MP.audio.state()") == 'running', js(pg, "MP.audio.state()"))
        js(pg, "MP.audio.setMusic(true, 60)"); pg.wait_for_timeout(300)
        check('sound: music plays after the first tap', js(pg, "MP.audio.musicState().playing") is True)
        js(pg, "window.__ac = 1; document.dispatchEvent(new Event('visibilitychange'))")
        pg.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(200)
        check('sound: engine sleeps while the page is hidden', js(pg, "MP.audio.state()") in ('suspended', 'interrupted'))
        pg.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(300)
        check('sound: engine wakes again when the page is visible', js(pg, "MP.audio.state()") == 'running', js(pg, "MP.audio.state()"))
        pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
        pg.evaluate("Object.defineProperty(document,'hidden',{value:true,configurable:true}); document.dispatchEvent(new Event('visibilitychange'))"); pg.wait_for_timeout(200)
        pg.evaluate("Object.defineProperty(document,'hidden',{value:false,configurable:true})")
        pg.mouse.click(100, 300); pg.wait_for_timeout(300)
        check('sound: a plain tap also wakes a sleeping engine', js(pg, "MP.audio.state()") == 'running')
        check('sound: no page errors', not pg.problems, pg.problems[:3])
        ctx.close()

        # ---------- version & update info ----------
        ctx, pg = page(b)
        js(pg, SEED, 3); pg.wait_for_timeout(300)
        check('version: returning player sees a "new" note on the menu', pg.locator('.newbadge').count() == 1)
        js(pg, "MP.app.go('settings')"); pg.wait_for_timeout(300)
        txt = pg.locator('.about').inner_text()
        check('version: settings shows the version number and what is new', '0.6.0' in txt and "What" in txt and 'Online friends' in txt, txt[:120])
        check('version: earlier updates are in a collapsible list', pg.locator('.about details.older').count() == 1)
        js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(300)
        check('version: the note disappears once settings was opened', pg.locator('.newbadge').count() == 0)
        js(pg, "MP.store.update(s=>{s.lang='ms'}); MP.app.applySettings(); MP.app.go('settings')"); pg.wait_for_timeout(300)
        check('version: update info is translated to Bahasa Melayu', 'Kawan dalam talian' in pg.locator('.about').inner_text())
        ctx.close()

        # ---------- daily gift ----------
        ctx, pg = page(b)
        js(pg, SEED, 1); pg.wait_for_timeout(300)
        check('gift: menu shows a ready button for a new day', pg.locator('.giftbtn.ready').count() == 1)
        pg.locator('.giftbtn').dispatch_event('click'); pg.wait_for_timeout(300)
        check('gift: streak screen shows 7 day tiles with day 7 flagged as the bonus', pg.locator('.daytile').count() == 7 and pg.locator('.daytile.big').count() == 1 and 'bonus' in pg.locator('.daytile.big').inner_text())
        c0 = js(pg, "MP.store.get().coins")
        pg.get_by_role('button', name='Claim 5 coins').click(); pg.wait_for_timeout(400)
        check('gift: claiming adds the day-1 coins once', js(pg, "MP.store.get().coins") == c0 + 5 and js(pg, "MP.store.get().streak.day") == 1)
        check('gift: after claiming there is no claim button and day 1 is ticked', pg.get_by_role('button', name='Claim').count() == 0 and pg.locator('.daytile.done').count() == 1)
        js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(300)
        check('gift: menu no longer pulses today', pg.locator('.giftbtn.ready').count() == 0)
        # next day: pretend yesterday was day 6 -> today is day 7 with the Perfect Week bonus
        js(pg, "(()=>{const d=new Date(Date.now()-86400000);MP.store.update(s=>{s.streak={day:6,last:MP.streak.dayKey(d),best:6,weeks:0,total:6}}); MP.app.go('streak')})()"); pg.wait_for_timeout(300)
        c1 = js(pg, "MP.store.get().coins")
        pg.get_by_role('button', name='Claim 150 coins').click(); pg.wait_for_timeout(400)
        check('gift: day 7 pays 50 + 100 perfect-week bonus and celebrates', js(pg, "MP.store.get().coins") == c1 + 150 and js(pg, "MP.store.get().streak.weeks") == 1 and pg.locator('.dialog-card').count() == 1)
        pg.get_by_role('button', name='OK').click(); pg.wait_for_timeout(200)
        js(pg, "(()=>{const d=new Date(Date.now()-3*86400000);MP.store.update(s=>{s.streak={day:3,last:MP.streak.dayKey(d),best:3,weeks:0,total:3}}); MP.app.go('streak')})()"); pg.wait_for_timeout(300)
        pg.get_by_role('button', name='Claim 5 coins').click(); pg.wait_for_timeout(300)
        check('gift: a missed day restarts at day 1 with a kind note', js(pg, "MP.store.get().streak.day") == 1 and pg.locator('.dialog-card').count() == 1)
        pg.get_by_role('button', name='OK').click(); pg.wait_for_timeout(200)
        pg.reload(); pg.wait_for_timeout(500); js(pg, "MP.app.go('streak')"); pg.wait_for_timeout(300)
        check('gift: the streak survives a reload and cannot be claimed twice', js(pg, "MP.store.get().streak.day") == 1 and pg.get_by_role('button', name='Claim').count() == 0)
        for lang in ('en', 'ms'):
            for w in (320, 390):
                pg.set_viewport_size({'width': w, 'height': 700})
                js(pg, "l=>{MP.store.update(s=>{s.lang=l}); MP.app.applySettings(); MP.app.go('streak')}", lang); pg.wait_for_timeout(200)
                check('gift: no sideways scrolling (%s, %dpx)' % (lang, w), js(pg, 'document.documentElement.scrollWidth <= window.innerWidth + 1'))
        check('gift: no page errors', not pg.problems, pg.problems[:3])
        ctx.close()

        # ---------- finds ----------
        ctx, pg = page(b)
        js(pg, SEED, 2); pg.wait_for_timeout(300)
        check('finds: 2 finished levels is not enough for anything yet', js(pg, "MP.store.get().closet.length") == 0 and js(pg, "MP.store.get().wardrobe.owned.length") == 0)
        lid = js(pg, "MP.levels.next(MP.levels.all()[1].id).id")
        js(pg, "id=>MP.app.go('level',{id})", lid); pg.wait_for_timeout(250)
        if pg.locator('.storycard .btn.big').count(): pg.locator('.storycard .btn.big').click()
        pg.wait_for_timeout(200)
        solve(pg); pg.wait_for_selector('.dialog-card.complete-card', timeout=8000); pg.wait_for_timeout(300)
        check('finds: finishing the 3rd level finds the Party hat', js(pg, "MP.store.get().closet.join()") == 'party', js(pg, "MP.store.get().closet.join()"))
        check('finds: the completion card announces it', 'New find' in pg.locator('.complete-card').inner_text() and 'Party hat' in pg.locator('.complete-card').inner_text())
        js(pg, "MP.app.go('collection')"); pg.wait_for_timeout(250)
        check('finds: Nimbo hats show what is needed, and a locked one explains kindly', 'Finish 5 levels' in pg.locator('.hats').inner_text())
        pg.locator('.hat.locked').first.click(); pg.wait_for_timeout(250)
        check('finds: tapping a locked hat shows "keep playing"', pg.locator('.dialog-card').count() == 1 and 'Keep playing' in pg.locator('.dialog-card').inner_text())
        pg.get_by_role('button', name='OK').click(); pg.wait_for_timeout(200)
        js(pg, SEED, 6); pg.wait_for_timeout(300)
        check('finds: an older save with 6 levels done receives its hats on opening the game', js(pg, "MP.store.get().wardrobe.owned.join()") == 'sprout' and js(pg, "MP.store.get().closet.join()") == 'party,bow')
        js(pg, "MP.app.go('collection')"); pg.wait_for_timeout(250)
        pg.locator('.hat').filter(has_text='Sprout').click(); pg.wait_for_timeout(250)
        check('finds: a found hat is put on Nimbo with one tap', js(pg, "MP.store.get().wardrobe.equipped") == 'sprout')
        check('finds: nothing in the game costs coins to unlock any more', js(pg, "MP.store.get().coins") == 0)
        ctx.close()

        # ---------- dashed, curved map path ----------
        ctx, pg = page(b)
        js(pg, SEED, 5); js(pg, "MP.app.go('map')"); pg.wait_for_timeout(400)
        n = pg.locator('.mappath .seg.top').count()
        check('path: every step between levels has a dashed top line over a dark outline', n > 8 and pg.locator('.mappath .seg.under').count() == n, n)
        check('path: lines are curved (cubic), not straight', js(pg, "[...document.querySelectorAll('.mappath .seg.top')].every(p=>/ C/.test(p.getAttribute('d')))"))
        check('path: dashes, not a solid line', js(pg, "getComputedStyle(document.querySelector('.mappath .seg.top')).strokeDasharray") not in ('none', '', '0'))
        check('path: finished steps are white and the next step is highlighted', pg.locator('.mappath .seg.top.done').count() == 5 and pg.locator('.mappath .seg.top.next').count() == 1)
        pg.screenshot(path='/tmp/map_path.png')
        ctx.close()
        b.close()
    print(json.dumps({'passed': sum(r['pass'] for r in results), 'failed': sum(not r['pass'] for r in results)}))
    sys.exit(0 if all(r['pass'] for r in results) else 1)

main()
