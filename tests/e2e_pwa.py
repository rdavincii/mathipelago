"""PWA: installable manifest + the game still opens with the network off. Needs a server on :8123 (python3 -m http.server 8123)."""
import json
from playwright.sync_api import sync_playwright
res = []
def check(n, ok, d=''):
    res.append(bool(ok)); print(('PASS ' if ok else 'FAIL ') + n, '' if ok else d)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}); pg = ctx.new_page()
    pg.goto('http://localhost:8123/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("localStorage.clear()")
    ready = pg.evaluate("navigator.serviceWorker.ready.then(r => !!r.active)")
    check('pwa: the service worker installs and activates', ready)
    pg.reload(); pg.wait_for_timeout(1200)
    check('pwa: the page is controlled by the worker after a reload', pg.evaluate("!!navigator.serviceWorker.controller"))
    man = pg.evaluate("fetch(document.querySelector('link[rel=manifest]').href).then(r => r.json())")
    check('pwa: the manifest is served and has icons', len(man['icons']) >= 3 and man['display'] == 'standalone')
    icon = pg.evaluate("fetch('icons/icon-512.png').then(r => r.headers.get('content-type'))")
    check('pwa: icons are served as PNG', icon == 'image/png', icon)
    ctx.set_offline(True)
    pg.reload(); pg.wait_for_timeout(1500)
    check('pwa: offline, the game still opens', pg.locator('#app .screen').count() >= 1, pg.content()[:200])
    pg.evaluate("MP.app.go('map')"); pg.wait_for_timeout(600)
    check('pwa: offline, the map works', pg.locator('.dmap .node').count() > 20)
    b.close()
print(json.dumps({'passed': sum(res), 'failed': len(res) - sum(res)}))
