#!/usr/bin/env python3
"""Verify the published dashboard options are really being served, byte for byte."""
import hashlib
import pathlib
import time
import urllib.request

BASE = "https://darrenhopwood13-maker.github.io/instructbrain-dashboard-options/"
LOCAL = pathlib.Path("/root/.hermes/profiles/banksy/work/ib-dash-sketches")
PAGES = {
    "": "index.html",
    "001-control-room/": "001-control-room/index.html",
    "002-ledger/": "002-ledger/index.html",
    "003-blueprint-grid/": "003-blueprint-grid/index.html",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (banksy verify)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


for attempt in range(1, 25):
    ok = 0
    results = []
    for path, local in PAGES.items():
        try:
            status, body = fetch(BASE + path)
            want = (LOCAL / local).read_bytes()
            same = hashlib.sha256(body).hexdigest() == hashlib.sha256(want).hexdigest()
            results.append((path or "/", status, len(body), "MATCHES local" if same else "served length differs"))
            if status == 200 and same:
                ok += 1
        except Exception as e:
            results.append((path or "/", "-", 0, type(e).__name__))
    print(f"attempt {attempt}: {ok}/{len(PAGES)} pages verified")
    if ok == len(PAGES):
        for r in results:
            print(f"  {r[0]:22} {r[1]}  {r[2]:>7} bytes  {r[3]}")
        raise SystemExit(0)
    time.sleep(12)

print("not fully live after ~5 minutes:")
for r in results:
    print(f"  {r[0]:22} {r[1]}  {r[2]:>7}  {r[3]}")
raise SystemExit(1)
