#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT = Path("/tmp/sg-deck/v2")
HTML = "file://" + str((ROOT / "index.html").resolve())
SLIDES = ROOT / "slides"; SLIDES.mkdir(exist_ok=True)
SIDS = [f"s{i:02d}" for i in range(1, 24)]
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 720}, device_scale_factor=2)
    page = ctx.new_page()
    page.goto(HTML, wait_until="load")
    page.wait_for_timeout(1200)
    for sid in SIDS:
        try:
            page.locator(f"#{sid}").screenshot(path=str(SLIDES / f"{sid}.png"))
        except Exception as e:
            print(f"  {sid} ✗ {e}")
    b.close()
print("rendered")
