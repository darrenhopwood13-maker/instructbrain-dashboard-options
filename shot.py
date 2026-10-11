#!/usr/bin/env python3
"""Screenshot a mockup variant, and report console noise. Usage: shot.py <file> <out-name>"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).resolve()
name = sys.argv[2]
out = pathlib.Path("/root/.hermes/profiles/banksy/work/ib-dash-sketches/shots")
out.mkdir(parents=True, exist_ok=True)

errors: list[str] = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = b.new_context(viewport={"width": 1440, "height": 1100})
    pg = ctx.new_page()
    pg.on("console", lambda m: errors.append(f"{m.type}: {m.text[:200]}") if m.type == "error" else None)
    pg.on("pageerror", lambda e: errors.append(f"pageerror: {str(e)[:200]}"))
    pg.goto(f"file://{src}", wait_until="load")
    pg.wait_for_timeout(1800)

    # Prove the page is not a blank shell: read the headline numbers it computed.
    print("title:", pg.title())
    for sel in ["#r-reports", "#r-items", "#r-overdue", "#r-projects", "#g-pct", "#rail-window"]:
        el = pg.locator(sel)
        if el.count():
            print(f"  {sel} = {el.first.inner_text()!r}")
    print("  bars:", pg.locator(".bar").count(), " projects:", pg.locator(".proj").count(),
          " cards:", pg.locator(".cell").count())

    pg.screenshot(path=str(out / f"{name}-full.png"), full_page=True)
    pg.screenshot(path=str(out / f"{name}-fold.png"))
    b.close()

print("console errors:", len(errors))
for e in errors[:6]:
    print("  ", e)
