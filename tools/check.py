# -*- coding: utf-8 -*-
"""
Kontrola konzistence webu pavelvognarek.cz. Spouštět po každé změně, před commitem.

  python tools/check.py

Ověřuje:
  1. charset v prvních 1024 bajtech každé HTML stránky
  2. žádný non-www odkaz na vlastní doménu
  3. každý JSON-LD blok je validní JSON, vypíše typy
  4. FAQPage schema se shoduje ZNAK PO ZNAKU s viditelným FAQ textem
  5. přesně jeden <h1> na stránku
  6. všechny lokální soubory, na které se odkazuje (src/href), existují na disku
  7. každé URL v sitemap.xml odpovídá stránce v repu
"""
import glob
import io
import json
import os
import re
import sys
from html import unescape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.pavelvognarek.cz"
errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def html_pages():
    """Jen stránky, které jsou v gitu, tedy ty, co se reálně nasadí na Vercel."""
    import subprocess
    try:
        # --cached: už v repu, --others --exclude-standard: nové soubory, které nejsou v .gitignore.
        # Dohromady = přesně to, co po commitu poletí na Vercel.
        tracked = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard",
                                  "*.html", "*/*.html"], cwd=ROOT,
                                 capture_output=True, text=True, check=True).stdout.splitlines()
        out = [os.path.join(ROOT, t) for t in tracked if t.strip()]
    except Exception:
        out = []
        for pat in ("*.html", "*/index.html"):
            out += glob.glob(os.path.join(ROOT, pat))
    return sorted(p for p in out if "node_modules" not in p and os.path.exists(p))


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def strip_tags(x):
    return unescape(re.sub(r"<[^>]+>", "", x)).strip()


for path in html_pages():
    name = rel(path)
    raw = io.open(path, "rb").read()
    s = raw.decode("utf-8")

    # 1) charset do 1024 B
    if b"charset" not in raw[:1024]:
        err(f"{name}: <meta charset> není v prvních 1024 bajtech")

    # 2) non-www odkazy
    for m in set(re.findall(r"https://pavelvognarek\.cz[^\"'\s<)]*", s)):
        err(f"{name}: non-www odkaz {m}")

    # 3) JSON-LD
    faq_schema = None
    for i, block in enumerate(re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S), 1):
        try:
            d = json.loads(block)
        except json.JSONDecodeError as e:
            err(f"{name}: JSON-LD blok {i} není validní JSON ({e})")
            continue
        nodes = d.get("@graph", [d])
        for n in nodes:
            if n.get("@type") == "FAQPage":
                faq_schema = n

    # 4) FAQPage vs. viditelný text
    vis = re.findall(
        r'<summary class="faq-q">(.*?)\s*<span class="faq-toggle".*?</summary>\s*<div class="faq-a">(.*?)</div>',
        s, re.S)
    if faq_schema:
        pairs = [(q["name"], q["acceptedAnswer"]["text"]) for q in faq_schema.get("mainEntity", [])]
        if len(pairs) != len(vis):
            err(f"{name}: FAQPage má {len(pairs)} otázek, na stránce je jich {len(vis)}")
        else:
            for (sq, sa), (vq, va) in zip(pairs, vis):
                if sq.strip() != strip_tags(vq):
                    err(f"{name}: otázka v schema != viditelný text\n    schema: {sq[:70]}\n    stránka: {strip_tags(vq)[:70]}")
                if sa.strip() != strip_tags(va):
                    err(f"{name}: odpověď v schema != viditelný text u „{sq[:50]}“")
    elif vis:
        err(f"{name}: na stránce je {len(vis)} FAQ otázek, ale chybí FAQPage JSON-LD")

    # 5) jeden H1
    h1 = len(re.findall(r"<h1[\s>]", s))
    if h1 != 1:
        err(f"{name}: {h1}x <h1> (má být přesně 1)")

    # 6) lokální soubory existují
    for attr in re.findall(r'(?:src|href)="([^"#?][^"]*)"', s):
        if attr.startswith(("http", "mailto:", "tel:", "data:", "//", "#")):
            continue
        target = attr.split("#")[0].split("?")[0]
        if not target:
            continue
        base = ROOT if target.startswith("/") else os.path.dirname(path)
        fp = os.path.join(base, target.lstrip("/"))
        if os.path.isdir(fp):
            fp = os.path.join(fp, "index.html")
        if not os.path.exists(fp):
            err(f"{name}: odkaz na neexistující soubor {attr}")

    # 7) srcset
    for ss in re.findall(r'(?:srcset|imagesrcset)="([^"]+)"', s):
        for cand in ss.split(","):
            u = cand.strip().split()[0]
            if u.startswith(("http", "data:")):
                continue
            base = ROOT if u.startswith("/") else os.path.dirname(path)
            if not os.path.exists(os.path.join(base, u.lstrip("/"))):
                err(f"{name}: srcset odkazuje na neexistující {u}")

# 8) sitemap vs. realita
sm = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(sm):
    body = io.open(sm, encoding="utf-8").read()
    for loc in re.findall(r"<loc>(.*?)</loc>", body):
        if not loc.startswith(DOMAIN):
            err(f"sitemap.xml: {loc} není na {DOMAIN}")
            continue
        p = loc[len(DOMAIN):].lstrip("/")
        fp = os.path.join(ROOT, p) if p else os.path.join(ROOT, "index.html")
        if os.path.isdir(fp):
            fp = os.path.join(fp, "index.html")
        if not os.path.exists(fp):
            err(f"sitemap.xml: {loc} neodpovídá žádnému souboru ({p or 'index.html'})")
    for path in html_pages():
        n = rel(path)
        if n in ("404.html",):
            continue
        url = DOMAIN + "/" + (n.replace("/index.html", "/") if n != "index.html" else "")
        if f"<loc>{url}</loc>" not in body:
            warn(f"sitemap.xml: chybí {url}")

print(f"stránek zkontrolováno: {len(html_pages())}")
for w in warnings:
    print("  UPOZORNĚNÍ:", w)
if errors:
    print(f"\nCHYB: {len(errors)}")
    for e in errors:
        print("  X", e)
    sys.exit(1)
print("OK: bez chyb")
