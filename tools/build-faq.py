# -*- coding: utf-8 -*-
"""
Generuje FAQ sekci (nativní <details>) a FAQPage JSON-LD z jednoho zdroje: tools/faq.json.

Proč skript a ne ruční editace: FAQPage schema se MUSÍ shodovat s viditelným textem
na stránce. Ručně se to rozejde pokaždé, když se do odpovědi přidá věta. Zdroj pravdy
je tools/faq.json, obojí se generuje z něj.

Použití:  python tools/build-faq.py
Markery v index.html musí existovat (FAQ:START/END a FAQ-SCHEMA:START/END).
"""
import io
import json
import os
import sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")
SRC = os.path.join(ROOT, "tools", "faq.json")
PAGE_URL = "https://www.pavelvognarek.cz/"

H_START = "<!-- FAQ:START (generovano tools/build-faq.py) -->"
H_END = "<!-- FAQ:END -->"
S_START = "<!-- FAQ-SCHEMA:START (generovano tools/build-faq.py) -->"
S_END = "<!-- FAQ-SCHEMA:END -->"


def build_html(items):
    rows = []
    for it in items:
        q = escape(it["q"], quote=False)
        a = escape(it["a"], quote=False)
        rows.append(
            '        <details class="faq-item">\n'
            f'          <summary class="faq-q">{q} <span class="faq-toggle" aria-hidden="true">+</span></summary>\n'
            f'          <div class="faq-a">{a}</div>\n'
            "        </details>"
        )
    return (
        f"{H_START}\n"
        '      <div class="faq-list">\n' + "\n".join(rows) + "\n      </div>\n"
        f"      {H_END}"
    )


def build_schema(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": PAGE_URL + "#faq",
        "inLanguage": "cs-CZ",
        "isPartOf": {"@id": PAGE_URL + "#website"},
        "mainEntity": [
            {
                "@type": "Question",
                "name": it["q"],
                "acceptedAnswer": {"@type": "Answer", "text": it["a"]},
            }
            for it in items
        ],
    }
    body = "\n".join("  " + ln for ln in json.dumps(data, ensure_ascii=False, indent=2).splitlines())
    return f'{S_START}\n  <script type="application/ld+json">\n{body}\n  </script>\n  {S_END}'


def replace_block(s, start, end, new, label):
    if start not in s or end not in s:
        sys.exit(f"CHYBA: markery pro {label} nenalezeny v index.html")
    i, j = s.index(start), s.index(end) + len(end)
    return s[:i] + new + s[j:]


def main():
    items = json.load(io.open(SRC, encoding="utf-8"))
    s = io.open(HTML, encoding="utf-8").read()
    s = replace_block(s, H_START, H_END, build_html(items), "viditelnou FAQ sekci")
    s = replace_block(s, S_START, S_END, build_schema(items), "FAQPage JSON-LD")
    io.open(HTML, "w", encoding="utf-8", newline="").write(s)
    print(f"OK: {len(items)} otázek vygenerováno do HTML i do FAQPage JSON-LD")


if __name__ == "__main__":
    main()
