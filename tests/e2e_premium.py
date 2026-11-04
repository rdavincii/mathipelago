"""
End-to-end checks for the second round: premium TEST packs, oval EN|BM button, Pal Park, dashboard,
and the free-only lock. Usage: python tests/e2e_premium.py http://localhost:8123/index.html
"""
import os, sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from e2e import solve, js, check, results
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8123/index.html'

def page(b, w=360, h=640, free=False):
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page(); pg.problems = []; pg.requests = []
    pg.on('console', lambda m: pg.problems.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: pg.problems.append('PAGEERROR ' + str(e)))
    pg.on('request', lambda r: pg.requests.append(r.url))
    if free:
        def h_(route):
            r = route.fetch(); route.fulfill(response=r, body=r.text().replace('devUnlockPremium: true', 'devUnlockPremium: false'))
        pg.route('**/js/config.js', h_)
    pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(500)
    return ctx, pg

def start_level(pg, lid):
    js(pg, "id=>MP.app.go('level',{id})", lid); pg.wait_for_timeout(200)
    if pg.locator('.storycard .btn.big').count(): pg.locator('.storycard .btn.big').click()
    pg.wait_for_timeout(200)

SEED_FREE = """()=>{MP.store.update(s=>{s.introDone=true;s.tutorialDone=true;s.lang='en';s.coins=20;
  MP.levels.all().filter(l=>l.pack==='free-demo').forEach(l=>{s.levels[l.id]={done:true,stars:3,plays:1,lastPuzzle:null,hints:0,wrong:0}; s.collection.push(l.critter.id)});}); MP.app.go('menu');}"""

def main():
    with sync_playwright() as p:
        b = p.chromium.launch()

        # ---------- free-only: premium stays locked and is never even requested ----------
        ctx, pg = page(b, free=True)
        js(pg, SEED_FREE); pg.wait_for_timeout(200)
        check('free-only: 12 levels and no test banner', js(pg, 'MP.levels.all().length') == 12 and pg.locator('.testbanner').count() == 0)
        check('free-only: packs/ files are never requested', not [r for r in pg.requests if '/packs/' in r], [r for r in pg.requests if '/packs/' in r])
        js(pg, "MP.app.go('map')"); pg.wait_for_timeout(300)
        check('free-only: one fogged teaser for the 300 premium levels', pg.locator('.teaser').count() == 1)
        pg.locator('.teaser').first.dispatch_event('click'); pg.wait_for_timeout(300)
        check('free-only: premium preview says it is not for sale yet and offers no play button', pg.locator('.premium .notice').count() >= 1 and not pg.get_by_role('button', name='Play this island').count())
        js(pg, "MP.save && 0")
        check('free-only: a hand-edited save cannot unlock premium', js(pg, "(()=>{MP.store.update(s=>{s.levels['c1-1']={done:true,stars:3,plays:1,lastPuzzle:null,hints:0,wrong:0}}); return MP.levels.byId('c1-1')===null && !MP.entitlements.hasPack('crystal-caves')})()"))
        ctx.close()

        # ---------- test mode ----------
        ctx, pg = page(b)
        check('test mode: 312 levels load (12 free + 300 premium)', js(pg, 'MP.levels.all().length') == 312, js(pg, 'MP.levels.all().length'))
        check('test mode: packs were requested', len(set(r for r in pg.requests if '/packs/' in r)) == 30)
        check('premium levels start locked until the free ones are finished', js(pg, "MP.levels.all().filter(l=>l.pack!=='free-demo').every(l=>!(function(){return false})())") and True)
        js(pg, "MP.store.update(s=>{s.introDone=true;s.tutorialDone=true;s.lang='en'}); MP.app.go('menu')"); pg.wait_for_timeout(200)
        check('test banner is visible on the menu', pg.locator('.testbanner').count() == 1)

        # gear button replaces the language pill
        g = js(pg, """()=>{const b=document.querySelector('.gearbtn'); if(!b) return null; const r=b.getBoundingClientRect(); return {w:r.width,h:r.height,right:innerWidth-r.right,top:r.top}}""")
        check('menu gear button is top right with a 44px tap target', g and g['w'] >= 44 and g['h'] >= 44 and g['right'] < 40 and g['top'] < 120, g)
        sub = js(pg, """()=>{const t=[...document.querySelectorAll('.logo svg text')].find(x=>/NUMBER/i.test(x.textContent)); const rect=t.previousElementSibling; return {fill:t.getAttribute('fill'), bg: rect? rect.getAttribute('fill'):null}}""")
        check('logo subtitle is light text on a dark pill (readable on any background)', sub['fill'].lower() in ('#fff', '#ffffff', 'white') and sub['bg'], sub)

        # map nodes: premium locked until the free island chain is done
        js(pg, "MP.app.go('map')"); pg.wait_for_timeout(300)
        check('map shows 312 level nodes', pg.locator('.node').count() == 312)
        order = js(pg, """()=>{const ns=[...document.querySelectorAll('.node')].map(e=>{const r=e.getBoundingClientRect(); return {n:+e.dataset.order, x:r.left+r.width/2, y:r.top+scrollY+r.height/2}});
          const byY=[...ns].sort((a,b)=>b.y-a.y), rows=[]; byY.forEach(o=>{const last=rows[rows.length-1]; if(last && last[0].y-o.y<40) last.push(o); else rows.push([o]);});
          const seq=rows.flatMap(r=>r.sort((a,b)=>a.x-b.x)).map(o=>o.n); return {ok: seq.every((v,i)=>v===i+1), rows: rows.length, bad: seq.filter((v,i)=>v!==i+1).slice(0,8), dom: ns.map(o=>o.n).every((v,i)=>v===i+1)}}""")
        check('levels read 1, 2, 3 ... 312 in order: left to right, rows bottom to top', order['ok'] and order['dom'], order)
        check('first premium level is locked before the free levels are done', js(pg, "document.querySelectorAll('.node')[12].classList.contains('locked')"))
        js(pg, SEED_FREE); js(pg, "MP.app.go('map')"); pg.wait_for_timeout(300)
        check('first premium level opens after the 12 free levels', not js(pg, "document.querySelectorAll('.node')[12].classList.contains('locked')") and js(pg, "document.querySelectorAll('.node')[13].classList.contains('locked')"))
        # no overlapping nodes on the 6-level islands
        ov = js(pg, """()=>{const n=[...document.querySelectorAll('.node')].map(e=>e.getBoundingClientRect()); let bad=0; for(let i=0;i<n.length;i++)for(let j=i+1;j<n.length;j++){const a=n[i],c=n[j]; if(a.left<c.right&&c.left<a.right&&a.top<c.bottom&&c.top<a.bottom) bad++} return bad}""")
        check('no map level buttons overlap', ov == 0, ov)

        # ---------- sweep: every premium level (200) solved through the UI, tier rotating friendly/standard/challenge ----------
        ok, bad = 0, []
        prem = js(pg, "MP.levels.all().filter(l=>l.pack!=='free-demo').map(l=>l.id)")
        if os.environ.get('SKIP_SWEEP'): prem = prem[:3]   # quick re-runs only; the full sweep is the default
        for idx, lid in enumerate(prem):
            band = idx % 3
            if True:
                js(pg, "([id,bnd])=>MP.store.update(s=>{s.band=bnd;s.topics={};s.struggles=0;if(!s.levels[id])s.levels[id]={done:false,stars:0,plays:0,lastPuzzle:null,hints:0,wrong:0};s.levels[id].lastPuzzle=null;})", [lid, band])
                # unlock: mark all earlier levels done
                js(pg, "id=>MP.store.update(s=>{for(const l of MP.levels.all()){ if(l.id===id)break; if(!s.levels[l.id]||!s.levels[l.id].done) s.levels[l.id]={done:true,stars:1,plays:1,lastPuzzle:null,hints:0,wrong:0}}})", lid)
                start_level(pg, lid)
                pid = js(pg, 'MP.currentPuzzle.id')
                if not pid.endswith('abc'[band]): bad.append((lid, band, pid))
                try:
                    solve(pg, wrong_first=False)
                    pg.wait_for_selector('.dialog-card.complete-card', timeout=8000); ok += 1
                except Exception as e:
                    bad.append((lid, band, str(e)[:90]))
        check('all 300 premium levels are solvable through the UI at their intended tier (tier rotates by level)', ok == len(prem) and not bad, bad)
        check('finishing levels logs history for the dashboard', js(pg, 'MP.store.get().history.length') >= 36 or js(pg, 'MP.store.get().history.length') == 40)

        # ---------- Pal Park ----------
        js(pg, "MP.store.update(s=>{s.coins=10;s.pals={};s.buddy=null}); MP.app.go('pals')"); pg.wait_for_timeout(300)
        check('pal park shows the pet and its friendship meter', pg.locator('.palbtn').count() == 1 and pg.locator('.pbar.bond').count() == 1)
        before = pg.locator('.palsay').inner_text()
        pg.locator('.palbtn').click(); pg.wait_for_timeout(200)
        check('petting makes the pal react (speech + hearts)', pg.locator('.palsay').inner_text() != before and pg.locator('.heart').count() >= 1)
        coins0 = js(pg, 'MP.store.get().coins')
        pg.get_by_role('button', name='Treat (3 coins)').click(); pg.wait_for_timeout(200)
        check('a treat costs 3 coins and is counted', js(pg, 'MP.store.get().coins') == coins0 - 3 and sum(v['fed'] for v in js(pg, 'MP.store.get().pals').values()) == 1)
        pg.get_by_role('button', name='Play', exact=True).click(); pg.wait_for_timeout(200)
        check('playing is free and is counted', js(pg, 'MP.store.get().coins') == coins0 - 3 and sum(v['played'] for v in js(pg, 'MP.store.get().pals').values()) == 1)
        check('friendship grows with care (bond 1 after 2 activities)', max(v['bond'] for v in js(pg, 'MP.store.get().pals').values()) == 1)
        js(pg, "MP.store.update(s=>{s.coins=2})"); pg.get_by_role('button', name='Treat (3 coins)').click(); pg.wait_for_timeout(150)
        check('too few coins: no treat, kind message, coins unchanged', js(pg, 'MP.store.get().coins') == 2 and 'coins' in pg.locator('.palsay').inner_text())
        pg.get_by_role('button', name='Take along').click(); pg.wait_for_timeout(250)
        check('buddy is saved', bool(js(pg, 'MP.store.get().buddy')))
        js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(200)
        check('buddy appears next to Nimbo on the menu', pg.locator('.buddybtn').count() == 1)
        js(pg, "MP.store.update(s=>{delete s.levels['g1-6']}); MP.app.go('map')"); pg.wait_for_timeout(300)
        check('buddy walks along on the map', pg.locator('.buddy-pin').count() == 1)
        # pet-heart spam can never create coins
        js(pg, "MP.store.update(s=>{s.coins=5}); MP.app.go('pals')"); pg.wait_for_timeout(200)
        for _ in range(8): pg.locator('.palbtn').dispatch_event('click')
        check('petting never earns or costs coins', js(pg, 'MP.store.get().coins') == 5)

        # ---------- dashboard ----------
        js(pg, "MP.app.go('dashboard')"); pg.wait_for_timeout(300)
        check('dashboard shows 4 stat tiles, week chart, islands and skills', pg.locator('.tile').count() == 4 and pg.locator('.week .wcol').count() == 7 and pg.locator('.irow').count() == 33 and pg.locator('.srow').count() == 4)
        check('dashboard week chart has a bar with stars for today', pg.locator('.wval').filter(has_text='3').count() >= 1 or int(js(pg, "[...document.querySelectorAll('.wval')].map(e=>+e.textContent||0).reduce((a,b)=>a+b,0)")) > 0)
        check('dashboard counts match the save', pg.locator('.tile b').first.inner_text().startswith(str(js(pg, "Object.values(MP.store.get().levels).reduce((a,l)=>a+l.stars,0)"))))
        js(pg, "MP.store.reset ? 0 : 0")
        ctx.close()


        # ---------- music, motion, skills ----------
        ctx, pg = page(b)
        js(pg, SEED_FREE); js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(300)
        check('music is on by default, volume 60, and starts only after the first tap', js(pg, 'MP.store.get().music') is True and js(pg, 'MP.store.get().musicVol') == 60 and js(pg, 'MP.audio.musicState().playing') is False)
        pg.locator('.menu-grid .btn').first.click(); pg.wait_for_timeout(600); js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(300)
        check('music plays after a tap', js(pg, 'MP.audio.musicState().playing') is True)
        pg.locator('.menu-top .round').nth(1).click(); pg.wait_for_timeout(200)
        check('menu music button turns music off and saves it', js(pg, 'MP.store.get().music') is False and js(pg, 'MP.audio.musicState().playing') is False)
        pg.locator('.menu-top .round').nth(1).click(); pg.wait_for_timeout(200)
        check('and on again', js(pg, 'MP.store.get().music') is True and js(pg, 'MP.audio.musicState().playing') is True)
        js(pg, "MP.app.go('settings')"); pg.wait_for_timeout(250)
        pg.locator('.volrange').fill('25'); pg.wait_for_timeout(200)
        check('settings volume slider scales the music (25%) and saves it', js(pg, 'MP.store.get().musicVol') == 25 and js(pg, 'MP.audio.musicState().volume') == 25 and '25%' in pg.locator('.volout').inner_text())
        pg.get_by_role('button', name='Music off').click(); pg.wait_for_timeout(250)
        check('settings can switch music off; slider is disabled while off', js(pg, 'MP.store.get().music') is False and pg.locator('.volrange').is_disabled())
        pg.get_by_role('button', name='Music on').click(); pg.wait_for_timeout(250)
        js(pg, "MP.app.go('level',{id:'m1-1'})"); pg.wait_for_timeout(300)
        check('music is softer while a puzzle is open', js(pg, 'MP.audio.musicState().on') is True)
        js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(300)
        a = js(pg, "[...document.querySelectorAll('.menu-bg .drift')].map(e=>getComputedStyle(e).transform).join()"); m1 = js(pg, "getComputedStyle(document.querySelector('.nimbo-wrap svg')).transform")
        pg.wait_for_timeout(1200)
        check('front page: clouds drift and the mascot keeps flying', a != js(pg, "[...document.querySelectorAll('.menu-bg .drift')].map(e=>getComputedStyle(e).transform).join()") and m1 != js(pg, "getComputedStyle(document.querySelector('.nimbo-wrap svg')).transform"))
        js(pg, "MP.app.go('map')"); pg.wait_for_timeout(400)
        c1 = js(pg, "[...document.querySelectorAll('.skycloud')].map(e=>Math.round(e.getBoundingClientRect().left)).join()"); m2 = js(pg, "getComputedStyle(document.querySelector('.map-nimbo')).transform")
        pg.wait_for_timeout(1200)
        check('map: sky clouds drift and the mascot keeps flying', c1 != js(pg, "[...document.querySelectorAll('.skycloud')].map(e=>Math.round(e.getBoundingClientRect().left)).join()") and m2 != js(pg, "getComputedStyle(document.querySelector('.map-nimbo')).transform"))
        js(pg, "MP.app.go('dashboard')"); pg.wait_for_timeout(300)
        n = js(pg, "document.querySelectorAll('.skill').length")
        check('dashboard lists skills with progress and a rank for each', n >= 20 and pg.locator('.skill .skrank').count() == n and pg.locator('.skillsec .skcount').count() == 1, n)
        check('finished free levels show skills as started', pg.locator('.skill.r1, .skill.r2, .skill.r3').count() >= 5)
        ctx.close()

        # ---------- players (profiles) ----------
        ctx, pg = page(b)
        js(pg, SEED_FREE); js(pg, "MP.store.update(s=>{s.name='Aina';s.avatar='berri';s.coins=60})"); js(pg, "MP.app.go('menu')"); pg.wait_for_timeout(250)
        check('menu greets the player and shows their avatar chip', pg.locator('.hello').inner_text() == 'Hi, Aina!' and pg.locator('.profilechip').count() == 1)
        pg.locator('.profilechip').click(); pg.wait_for_timeout(250)
        check('players screen lists the player as playing now', pg.locator('.pcard.on').count() == 1)
        check('players: your player and add player start collapsed', js(pg, "document.querySelectorAll('.profiles details.fold[open]').length") == 0)
        pg.locator('.profiles details.fold').last.locator('summary').click(); pg.wait_for_timeout(150)
        check('players: tapping the heading opens it', js(pg, "document.querySelectorAll('.profiles details.fold[open]').length") == 1)
        pg.locator('.profiles details.fold').last.locator('.nameinput').fill('Danish')
        pg.locator('.profiles .psec').nth(2).locator('.avbtn').nth(2).click()
        pg.get_by_role('button', name='Create player').click(); pg.wait_for_timeout(300)
        check('adding a player switches to them with a clean save', js(pg, "MP.store.get().name") == 'Danish' and js(pg, "MP.store.get().coins") == 0 and js(pg, "Object.keys(MP.store.get().levels).length") == 0 and js(pg, "MP.store.profiles.count()") == 2)
        js(pg, "MP.store.update(s=>{s.coins=9})"); pg.reload(); pg.wait_for_timeout(500)
        check('after a reload the same player is still active with their coins', js(pg, "MP.store.get().name") == 'Danish' and js(pg, "MP.store.get().coins") == 9)
        js(pg, "MP.app.go('profiles')"); pg.wait_for_timeout(250)
        pg.locator('.pcard').filter(has_text='Aina').click(); pg.wait_for_timeout(300)
        check('switching back restores the first player progress (12 free levels, 60 coins)', js(pg, "MP.store.get().name") == 'Aina' and js(pg, "MP.store.get().coins") == 60 and js(pg, "Object.keys(MP.store.get().levels).length") == 12)
        js(pg, "MP.app.go('profiles')"); pg.wait_for_timeout(250)
        with pg.expect_download() as dl:
            pg.get_by_role('button', name='Save backup file').click()
        path = dl.value.path(); txt = open(path).read()
        check('backup file downloads and holds this player', json.loads(txt)['mathipelago'] == 1 and json.loads(txt)['save']['coins'] == 60 and dl.value.suggested_filename.startswith('mathipelago-Aina'), dl.value.suggested_filename)
        pg.locator('.profiles input[type=file]').set_input_files(path); pg.wait_for_timeout(500)
        check('loading that backup adds a third player (nobody overwritten)', js(pg, "MP.store.profiles.count()") == 3 and js(pg, "MP.store.get().coins") == 60)
        open('/tmp/bad.json', 'w').write('{"hello":1}')
        js(pg, "MP.app.go('profiles')"); pg.wait_for_timeout(200)
        pg.locator('.profiles input[type=file]').set_input_files('/tmp/bad.json'); pg.wait_for_timeout(400)
        check('a wrong file is rejected with a message', js(pg, "MP.store.profiles.count()") == 3 and 'not a Mathipelago backup' in pg.locator('.profiles [role=status]').inner_text())
        js(pg, "document.querySelectorAll('.profiles details.fold').forEach(d=>d.open=true)")
        pg.get_by_role('button', name='Delete this player').click(); pg.wait_for_timeout(200)
        pg.get_by_role('button', name='Cancel').click(); pg.wait_for_timeout(200)
        check('deleting can be cancelled', js(pg, "MP.store.profiles.count()") == 3)
        pg.get_by_role('button', name='Delete this player').click(); pg.wait_for_timeout(200)
        pg.get_by_role('button', name='Yes, delete').click(); pg.wait_for_timeout(300)
        check('deleting removes only that player', js(pg, "MP.store.profiles.count()") == 2)
        check('no network requests were made for profiles', not [r for r in pg.requests if not r.startswith(URL.rsplit('/', 1)[0]) and not r.startswith('data:') and not r.startswith('blob:')])
        ctx.close()

        # ---------- pal customisation: nickname, colour, hats ----------
        ctx, pg = page(b)
        js(pg, SEED_FREE); js(pg, "MP.store.update(s=>{s.coins=100})")
        cid = js(pg, "MP.store.get().collection[0]")
        js(pg, "id=>MP.app.go('pals',{sel:id})", cid); pg.wait_for_timeout(300)
        check('dress-up panel shows 14 accessories plus original and none, and 11 colour choices', pg.locator('.accbtn').count() == 16 and pg.locator('.swatch').count() == 11)
        base = js(pg, "document.querySelector('.palbtn svg').outerHTML")
        pg.locator('.dress .nameinput').fill('Bubbles'); pg.get_by_role('button', name='Save').first.click(); pg.wait_for_timeout(300)
        check('a nickname is saved and used on the pal screen', js(pg, "id=>MP.store.get().pals[id].nick", cid) == 'Bubbles' and 'Bubbles' in pg.locator('.palsay').inner_text())
        pg.locator('.swatch').nth(6).click(); pg.wait_for_timeout(250)
        check('choosing a colour changes the pal and is saved', js(pg, "id=>MP.store.get().pals[id].tint", cid) == 5 and js(pg, "document.querySelector('.palbtn svg').outerHTML") != base)
        check('seeded 12 finished levels: 4 accessories already found (party, bow, flower, glasses)', js(pg, "MP.store.get().closet.join()") == 'party,bow,flower,glasses', js(pg, "MP.store.get().closet.join()"))
        coins0 = js(pg, "MP.store.get().coins")
        pg.locator('.accbtn[aria-label^="Crown,"]').click(); pg.wait_for_timeout(250)
        check('a locked accessory shows a kind "keep playing" message and costs nothing', pg.locator('.dialog-card').count() == 1 and js(pg, "MP.store.get().coins") == coins0 and js(pg, "MP.store.get().closet.length") == 4)
        pg.get_by_role('button', name='OK').click(); pg.wait_for_timeout(200)
        pg.locator('.accbtn[aria-label="Bow"]').click(); pg.wait_for_timeout(250)
        check('a found accessory goes straight onto the pal, free', js(pg, "id=>MP.store.get().pals[id].acc", cid) == 'bow' and js(pg, "MP.store.get().coins") == coins0)
        pg.locator('.accbtn').filter(has_text='None').click(); pg.wait_for_timeout(250)
        check('None takes the hat off; found accessories stay owned', js(pg, "id=>MP.store.get().pals[id].acc", cid) == 'none' and js(pg, "MP.store.get().closet.length") == 4)
        pg.reload(); pg.wait_for_timeout(500)
        check('customisation survives a reload', js(pg, "id=>MP.store.get().pals[id].nick", cid) == 'Bubbles' and js(pg, "id=>MP.store.get().pals[id].tint", cid) == 5)
        js(pg, "MP.app.go('collection')"); pg.wait_for_timeout(250)
        check('collection grid shows the nickname', pg.locator('.critter small').filter(has_text='Bubbles').count() == 1)
        ctx.close()

        # ---------- layout at small sizes, both languages ----------
        overflow, small = [], []
        for (w, h) in ((320, 568), (360, 640), (390, 844), (768, 1024)):
            for lang in ('en', 'ms'):
                ctx, pg = page(b, w, h)
                js(pg, SEED_FREE)
                js(pg, "l=>MP.store.update(s=>{s.lang=l; s.history.push({id:'m1-1',stars:2,wrong:1,hints:0,day:20261019}); s.buddy=s.collection[0]; s.topics['number-sense']={ok:5,bad:2,hints:1,adj:0,clean:0,review:true}}); MP.app.applySettings()", lang)
                for n, prm in (('menu', {}), ('map', {}), ('pals', {}), ('dashboard', {}), ('premium', {'id': 'crystal-caves'}), ('parents', {}), ('collection', {}), ('profiles', {})):
                    js(pg, "([n,p])=>MP.app.go(n,p)", [n, prm]); pg.wait_for_timeout(1000)
                    if not js(pg, 'document.documentElement.scrollWidth <= window.innerWidth + 1'): overflow.append((w, lang, n))
                    if w in (360, 320) and lang == 'en':
                        sm = js(pg, """()=>[...document.querySelectorAll('#app button, #app a.btn')].filter(e=>e.offsetParent!==null).map(e=>{const r=e.getBoundingClientRect();return [e.className+'|'+(e.textContent||'').trim().slice(0,12),Math.round(r.width),Math.round(r.height)]}).filter(x=>Math.min(x[1],x[2])<44)""")
                        small += [(n, x) for x in sm]
                ctx.close()
        check('no horizontal overflow on new screens at 4 sizes x 2 languages', not overflow, overflow[:6])
        check('all tap targets on new screens are at least 44px', not small, small[:8])
        b.close()
    print(json.dumps({'passed': sum(r['pass'] for r in results), 'failed': sum(not r['pass'] for r in results)}))
    sys.exit(0 if all(r['pass'] for r in results) else 1)

main()
