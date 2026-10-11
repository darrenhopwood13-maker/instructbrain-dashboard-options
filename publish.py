#!/usr/bin/env python3
"""Publish the dashboard design options to GitHub Pages.

Same route as the other deliverables: create the repo if needed, push, enable Pages.
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

HOME = "/root/.hermes/profiles/banksy/home"
REPO = "instructbrain-dashboard-options"
OWNER = "darrenhopwood13-maker"
SRC = "/root/.hermes/profiles/banksy/work/ib-dash-sketches"
ENV = dict(os.environ, HOME=HOME, GIT_TERMINAL_PROMPT="0")


def token():
    txt = open(os.path.join(HOME, ".git-credentials")).read()
    m = re.search(r"https://([^:]+):([^@]+)@github\.com", txt)
    if not m:
        sys.exit("no github credential in the store")
    return m.group(2)


def api(path, method="GET", payload=None, tok=None):
    url = "https://api.github.com" + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "token " + tok)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "banksy-agent")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "{}")


def run(args, cwd=None):
    p = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


tok = token()

# Keep the screenshots and the build script out of the published site.
open(os.path.join(SRC, ".gitignore"), "w").write("shots/\n*.pyc\n__pycache__/\n")
open(os.path.join(SRC, ".nojekyll"), "w").write("")

code, body = api("/user/repos", "POST", {
    "name": REPO, "private": False, "auto_init": False,
    "description": "instructBrain dashboard - three design directions (mockups, 11 Oct 2026)"}, tok)
print("create repo ->", code, body.get("full_name") or body.get("message"))

if not os.path.isdir(os.path.join(SRC, ".git")):
    print(run(["git", "init", "-b", "main"], cwd=SRC))
run(["git", "config", "user.email", "agent@banksy.local"], cwd=SRC)
run(["git", "config", "user.name", "Banksy (agent)"], cwd=SRC)
run(["git", "add", "-A"], cwd=SRC)
rc, out = run(["git", "commit", "-m",
               "Dashboard design options: three directions (mockups, not the product)"], cwd=SRC)
print("commit ->", rc, out.splitlines()[0] if out else "")
rc, out = run(["git", "remote", "get-url", "origin"], cwd=SRC)
if rc != 0:
    run(["git", "remote", "add", "origin", f"https://github.com/{OWNER}/{REPO}.git"], cwd=SRC)
rc, out = run(["git", "push", "-u", "origin", "main", "--force"], cwd=SRC)
print("push ->", rc, re.sub(r"https://[^@]+@", "https://", out)[-200:])

code, body = api(f"/repos/{OWNER}/{REPO}/pages", "POST",
                 {"source": {"branch": "main", "path": "/"}}, tok)
print("enable pages ->", code, body.get("html_url") or body.get("message"))
if code == 409:
    code, body = api(f"/repos/{OWNER}/{REPO}/pages", "PUT",
                     {"source": {"branch": "main", "path": "/"}}, tok)
    print("update pages ->", code, body.get("html_url") or body.get("message"))
print("URL -> https://%s.github.io/%s/" % (OWNER, REPO))
