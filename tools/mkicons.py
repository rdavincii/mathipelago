"""Render the app icons from the game's own Nimbo artwork. Run: python3 tools/mkicons.py (needs playwright + a server on :8123)."""
import os
from playwright.sync_api import sync_playwright
OUT = os.path.join(os.path.dirname(__file__), '..', 'icons')
HTML = """<body style="margin:0"><div id="i" style="width:512px;height:512px;display:grid;place-items:center;background:radial-gradient(circle at 50% 35%,#e8f7ff 0,#9fd9ff 55%,#5fb8ff 100%)"><div id="n" style="width:@Spx;height:@Spx"></div></div></body>"""
# name, canvas px, nimbo size inside a 512 canvas. Maskable keeps the art inside the central 80% circle.
JOBS = [('icon-192.png', 192, 410), ('icon-512.png', 512, 410), ('icon-maskable-512.png', 512, 310), ('apple-touch-icon.png', 180, 410)]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 600, 'height': 600})
    pg.goto('http://localhost:8123/index.html'); pg.wait_for_function('window.MP && MP.art')
    svg = pg.evaluate("MP.art.nimbo({ mood: 'happy' })")
    for name, px, size in JOBS:
        pg.set_content(HTML.replace('@S', str(size))); pg.evaluate("s => { document.getElementById('n').innerHTML = s; const v = document.querySelector('#n svg'); v.setAttribute('width', '100%'); v.setAttribute('height', '100%'); }", svg)
        pg.locator('#i').screenshot(path=os.path.join(OUT, name), scale='css') if px == 512 else None
        if px != 512:
            pg.locator('#i').screenshot(path=os.path.join(OUT, '_tmp.png'))
            from PIL import Image
            Image.open(os.path.join(OUT, '_tmp.png')).convert('RGB').resize((px, px), Image.LANCZOS).save(os.path.join(OUT, name)); os.remove(os.path.join(OUT, '_tmp.png'))
    b.close()
