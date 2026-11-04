"""Friends screen against a MOCKED server (the real one is not reachable from the test sandbox). Usage: python tests/e2e_friends.py [url]"""
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from e2e import js, check, results
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8123/index.html'
ID = '11111111-1111-1111-1111-111111111111'

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True); pg = ctx.new_page()
        calls = []; state = {'friends': [{'id': '22222222-2222-2222-2222-222222222222', 'name': 'Aina', 'avatar': 'nimbo', 'stars': 40, 'levels': 15, 'pal': None, 'status': 'friend', 'cheered': False},
                                         {'id': '33333333-3333-3333-3333-333333333333', 'name': 'Hakim', 'avatar': 'nimbo', 'stars': 3, 'levels': 1, 'pal': None, 'status': 'incoming', 'cheered': False}], 'collect': 3}
        def h(route):
            req = route.request; fn = req.url.rsplit('/', 1)[1]; body = json.loads(req.post_data or '{}'); calls.append((fn, body))
            out = {'mp_join': {'id': ID, 'code': 'ABC234'}, 'mp_sync': True, 'mp_friends': state['friends'], 'mp_add': 'sent', 'mp_cheer': True, 'mp_collect': state['collect'], 'mp_respond': True}[fn]
            if fn == 'mp_cheer': state['friends'][0]['cheered'] = True
            if fn == 'mp_respond': state['friends'][1]['status'] = 'friend'
            if fn == 'mp_collect': state['collect'] = 0
            route.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps(out))
        pg.route('**/rest/v1/rpc/*', h)
        pg.route('**/rest/v1/rpc/*', lambda r: r.fulfill(status=204, headers={'access-control-allow-origin': '*', 'access-control-allow-headers': '*'}) if r.request.method == 'OPTIONS' else h(r))
        pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_timeout(400)
        js(pg, "MP.store.update(s=>{s.introDone=true;s.tutorialDone=true;s.lang='en';s.name='Nina';s.coins=0}); MP.app.go('menu')"); pg.wait_for_timeout(300)
        check('friends: nothing is sent before the grown-up switch', not calls)
        check('friends: menu has a Friends button', pg.get_by_role('button', name='Friends', exact=True).count() == 1)
        js(pg, "MP.app.go('friends')"); pg.wait_for_timeout(300)
        check('friends: off by default and the privacy promise is shown', pg.get_by_role('button', name='Turn on online friends').count() == 1 and 'no chat' in pg.locator('.friends').inner_text())
        pg.get_by_role('button', name='Turn on online friends').dispatch_event('click'); pg.wait_for_timeout(300)
        q = pg.locator('.gateq').inner_text(); a, bb = [int(x) for x in q.replace('= ?', '').split('+')]
        pg.locator('.dialog-card input').fill('99'); pg.get_by_role('button', name='Turn on', exact=True).click(); pg.wait_for_timeout(400)
        check('friends: a wrong grown-up answer sends nothing and asks again', not calls and pg.locator('.gateq').count() == 1)
        q = pg.locator('.gateq').inner_text(); a, bb = [int(x) for x in q.replace('= ?', '').split('+')]
        pg.locator('.dialog-card input').fill(str(a + bb)); pg.get_by_role('button', name='Turn on', exact=True).click(); pg.wait_for_timeout(1000)
        check('friends: the right answer registers the player and shows the code', 'ABC234' in pg.locator('.mycode').inner_text() and js(pg, "MP.store.get().online.on") is True)
        check('friends: the join call carries only name and avatar, no coins or save', [c for c in calls if c[0] == 'mp_join'][0][1].keys() == {'p_secret', 'p_name', 'p_avatar'} and [c for c in calls if c[0] == 'mp_join'][0][1]['p_name'] == 'Nina')
        pg.wait_for_timeout(500)
        check('friends: friends and a request are listed', pg.locator('.fcard').count() == 2 and 'Aina' in pg.locator('.flist').inner_text() and pg.get_by_role('button', name='Accept').count() == 1)
        check('friends: cheers received become 2 coins each', js(pg, "MP.store.get().coins") == 6 and 'Friends cheered you 3 times' in pg.locator('.frnote').inner_text())
        pg.get_by_role('button', name='Cheer!').dispatch_event('click'); pg.wait_for_timeout(500)
        check('friends: cheering once marks it done for today', pg.get_by_role('button', name='Cheered today').count() == 1 and any(c[0] == 'mp_cheer' for c in calls))
        pg.get_by_role('button', name='Accept').dispatch_event('click'); pg.wait_for_timeout(500)
        check('friends: accepting makes them a friend', pg.get_by_role('button', name='Accept').count() == 0 and any(c[0] == 'mp_respond' for c in calls))
        pg.locator('.addrow input').fill('zz9 9x'); pg.get_by_role('button', name='Add friend').click(); pg.wait_for_timeout(400)
        check('friends: a typed code is cleaned to capital letters and numbers', [c for c in calls if c[0] == 'mp_add'][0][1]['p_code'] == 'ZZ99X' and 'Request sent' in pg.locator('.frnote').inner_text())
        check('friends: backup file never carries the online identity', '"token":null' in js(pg, "MP.store.profiles.exportActive()").replace(' ', ''))
        js(pg, "MP.store.update(s=>{s.lang='ms'}); MP.app.applySettings(); MP.app.go('friends')"); pg.wait_for_timeout(500)
        check('friends: Bahasa Melayu', 'Kod kawan anda' in pg.locator('.mycode').inner_text())
        pg.get_by_role('button', name='Matikan kawan dalam talian').dispatch_event('click'); pg.wait_for_timeout(300)
        pg.get_by_role('button', name='Matikan', exact=True).click(); pg.wait_for_timeout(400)
        n = len(calls); js(pg, "MP.app.go('friends')"); pg.wait_for_timeout(400)
        check('friends: turning off forgets the identity and stops all calls', js(pg, "MP.store.get().online.on") is False and len(calls) == n)
        # failure: server down
        pg.unroute('**/rest/v1/rpc/*'); pg.route('**/rest/v1/rpc/*', lambda r: r.abort())
        js(pg, "MP.store.update(s=>{s.lang='en'}); MP.app.applySettings(); MP.app.go('friends')"); pg.wait_for_timeout(300)
        pg.get_by_role('button', name='Turn on online friends').dispatch_event('click'); pg.wait_for_timeout(300)
        q = pg.locator('.gateq').inner_text(); a, bb = [int(x) for x in q.replace('= ?', '').split('+')]
        pg.locator('.dialog-card input').fill(str(a + bb)); pg.get_by_role('button', name='Turn on', exact=True).click(); pg.wait_for_timeout(800)
        check('friends: with no internet the game stays calm and says so', 'Could not reach' in pg.locator('.frnote').inner_text() and js(pg, "MP.store.get().online.on") is False)
        for w in (320, 390):
            pg.set_viewport_size({'width': w, 'height': 700}); pg.wait_for_timeout(150)
            check('friends: no sideways scroll at %dpx' % w, js(pg, 'document.documentElement.scrollWidth <= window.innerWidth + 1'))
        b.close()
    print(json.dumps({'passed': sum(r['pass'] for r in results), 'failed': sum(not r['pass'] for r in results)}))
    sys.exit(0 if all(r['pass'] for r in results) else 1)
main()
