"""Render the profile banner: assets/banner.webp (1600x480, desktop) and assets/banner-square.webp
(1080x1080, swapped in on phones by the README's <picture>). Needs Playwright with Microsoft Edge and Pillow.
Usage: python assets/src/render.py"""
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parent
OUT = SRC.parent

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    for size, (w, h), name in [("wide", (1600, 480), "banner"), ("square", (1080, 1080), "banner-square")]:
        page = browser.new_page(viewport={"width": w, "height": h})
        page.goto((SRC / "banner.html").as_uri() + f"?size={size}")
        page.evaluate("document.fonts.ready")
        for font in ['900 40px "Unbounded"', '600 20px "Montserrat"']:
            if not page.evaluate(f"document.fonts.check('{font}')"):
                sys.exit(f"{name}: font fell back ({font}), nothing saved")
        png = OUT / f"{name}.png"
        page.locator("#banner").screenshot(path=str(png))
        Image.open(png).convert("RGB").save(OUT / f"{name}.webp", quality=92, method=6)
        png.unlink()
        print(f"assets/{name}.webp  {w}x{h}  {(OUT / f'{name}.webp').stat().st_size // 1024} KB")
    browser.close()
