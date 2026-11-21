# -*- coding: utf-8 -*-
"""
IndexNow: oznámí Bingu a Seznamu nové a změněné stránky (Google IndexNow nepoužívá).

Klíč je v souboru <klíč>.txt v kořeni webu (veřejný, tak to protokol chce). Adresy bere
ze sitemap.xml: bez parametrů jen ty s nejnovějším lastmod, tedy co se změnilo při
posledním nasazení. Posílat jen po nasazení na produkci a jen změněné stránky.

  python tools/indexnow.py                 # jen vypíše, co by poslal
  python tools/indexnow.py --odeslat       # pošle na Seznam a Bing
  python tools/indexnow.py --vse --odeslat # všechny URL ze sitemap (jednorázově, třeba poprvé)

Odpovědi: 200 nebo 202 přijato, 403 špatný klíč (soubor na webu není nebo nesedí),
422 neplatné URL, 429 moc požadavků. Zdroj: skill seo-geo, references/seznam.md.
"""
import glob
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "www.pavelvognarek.cz"
ENDPOINTS = ["https://search.seznam.cz/indexnow", "https://www.bing.com/indexnow"]


def klic():
    kandidati = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "*.txt"))
                 if re.fullmatch(r"[0-9a-f]{32}", os.path.basename(p)[:-4])]
    if len(kandidati) != 1:
        sys.exit(f"CHYBA: v kořeni má být právě jeden soubor s klíčem <32 hex>.txt, je {len(kandidati)}")
    k = kandidati[0]
    obsah = io.open(os.path.join(ROOT, k + ".txt"), encoding="utf-8").read().strip()
    if obsah != k:
        sys.exit("CHYBA: obsah souboru s klíčem se neshoduje s jeho názvem")
    return k


def adresy(vse):
    sm = io.open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    rows = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", sm)
    if vse:
        return [u for u, _ in rows]
    nejnovejsi = max(m for _, m in rows)
    return [u for u, m in rows if m == nejnovejsi]


def main():
    vse = "--vse" in sys.argv
    odeslat = "--odeslat" in sys.argv
    k = klic()
    urls = adresy(vse)
    print(f"klíč {k}, {len(urls)} URL:")
    for u in urls:
        print("  ", u)
    if not odeslat:
        print("Jen náhled. Odeslat: python tools/indexnow.py --odeslat")
        return
    data = json.dumps({"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt",
                       "urlList": urls}).encode("utf-8")
    for ep in ENDPOINTS:
        req = urllib.request.Request(ep, data=data, method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"{ep}: {r.status}")
        except urllib.error.HTTPError as e:
            print(f"{ep}: {e.code} {e.reason}")
        except urllib.error.URLError as e:
            print(f"{ep}: chyba spojení {e.reason}")


if __name__ == "__main__":
    main()
