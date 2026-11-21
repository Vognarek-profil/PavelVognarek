# -*- coding: utf-8 -*-
"""
Grafy pro sekci Jak vyhodnocuji: homepage (blok mezi markery) a /jak-vyhodnocuji/.

Zdroj dat: tools/vyhodnoceni_data.json. Generuje ho skript v dashboardu
(dashboard/tools/export-web-charts.py), ručně se needituje.

Použití:  python tools/build_charts.py   (přepíše blok v index.html)
          podstránku pak přegeneruje python tools/build_pages.py, který si
          odsud bere CHARTS a čísla N.

Pravidla:
  - Žádné jméno klienta, produkt, slevový kód ani částka v Kč. Repo je veřejné.
    E-shopy jsou jen „E-shop A“ a „E-shop B“.
  - Každý graf má tabulku s hodnotami. Tooltip v assets/js/charts.js je navíc.
  - Jedna osa na graf. Objednávky, rozpočet a PNO jsou tři grafy pod sebou
    se stejnou osou X, ne jeden graf se dvěma osami.
"""
import datetime as dt
import io
import json
import math
import os
import sys
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(io.open(os.path.join(ROOT, "tools", "vyhodnoceni_data.json"), encoding="utf-8"))
HTML = os.path.join(ROOT, "index.html")
H_START = "<!-- VYHODNOCENI:START (generovano tools/build_charts.py) -->"
H_END = "<!-- VYHODNOCENI:END -->"

C_ORDERS = "#0A33C8"
C_BUDGET = "#5b7be0"
C_PNO = "#0b87a6"
C_LAST = "#9aa5be"
NBSP = " "
PNO_CAP = 50  # osa PNO končí na 50 %, vyšší dny se useknou a označí ▲ s hodnotou

MESICE = ["leden", "únor", "březen", "duben", "květen", "červen", "červenec", "srpen",
          "září", "říjen", "listopad", "prosinec"]
MESICE_GEN = ["ledna", "února", "března", "dubna", "května", "června", "července", "srpna",
              "září", "října", "listopadu", "prosince"]
MESICE_LOK = ["lednu", "únoru", "březnu", "dubnu", "květnu", "červnu", "červenci", "srpnu",
              "září", "říjnu", "listopadu", "prosinci"]
MESICE_KRATCE = ["led", "úno", "bře", "dub", "kvě", "čvn", "čvc", "srp", "zář", "říj", "lis", "pro"]
DNY = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]
DNY_CELE = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]


# ── formátování ──────────────────────────────────────────────────────────────
def cz(v, d=1):
    s = f"{v:,.{d}f}".replace(",", NBSP).replace(".", ",")
    return s


def num(v):
    return cz(v, 0)


def pct(v):
    return cz(v, 1) + NBSP + "%"


def times(v):
    return cz(v, 1) + "×"


def dm(iso):
    """2026-09-18 -> 18. 9."""
    y, m, d = iso.split("-")
    return f"{int(d)}.{NBSP}{int(m)}."


def month_of(iso):
    return MESICE[int(iso[5:7]) - 1]


def attr_json(v):
    return escape(json.dumps(v, ensure_ascii=False), quote=True)


def nice_axis(maxval):
    """Čistá horní mez osy a krok: 2 až 4 intervaly, co nejmenší rezerva nad maximem."""
    target = maxval * 1.05
    best = None
    for k in range(-2, 6):
        for rank, base in enumerate((1, 2, 5, 2.5, 4)):
            step = base * 10 ** k
            top = math.ceil(target / step - 1e-9) * step
            n = round(top / step)
            if 2 <= n <= 4:
                cand = (top, rank, step)
                if best is None or cand < best:
                    best = cand
    top, _, step = best
    return top, step


def tick_label(v, unit):
    if unit == "pct":
        return f"{num(v)}{NBSP}%"
    if unit == "x":
        return (cz(v, 1) if v % 1 else num(v)) + "×"
    return num(v)


def grid_html(top, step, unit):
    out = []
    v = 0.0
    while v <= top + 1e-9:
        out.append(f'<div class="viz-gl" style="bottom:{v / top * 100:.2f}%"><span>{tick_label(v, unit)}</span></div>')
        v += step
    return "".join(out)


def x_axis(labels_at, n):
    spans = "".join(
        f'<span style="left:{(i + 0.5) / n * 100:.3f}%">{escape(t)}</span>' for i, t in labels_at)
    return f'<div class="viz-x" aria-hidden="true">{spans}</div>'


def table(caption, head, rows):
    th = "".join(f"<th scope=\"col\">{escape(h)}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return (f'<details class="viz-table"><summary>{escape(caption)}</summary>'
            f'<div class="viz-scroll"><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div></details>')


def window(title, sub, inner):
    return (
        '<div class="viz-root viz-window">'
        '<div class="viz-bar" aria-hidden="true"><i></i><i></i><i></i>'
        f'<strong>{escape(title)}</strong><span>{escape(sub)}</span></div>'
        f'<div class="viz-body">{inner}</div></div>'
    )


def kpis(items, cls=""):
    tiles = "".join(
        f'<div class="viz-kpi"><div class="viz-kpi-l">{escape(l)}</div>'
        f'<div class="viz-kpi-v">{escape(v)}</div><div class="viz-kpi-s">{escape(s)}</div></div>'
        for l, v, s in items)
    return f'<div class="viz-kpis{(" " + cls) if cls else ""}">{tiles}</div>'


# ── E-shop A: denní řada ─────────────────────────────────────────────────────
A = DATA["eshop_a"]
DAYS = A["dny"]
NA = len(DAYS)
PEAK_I = [i for i, d in enumerate(DAYS) if A["spicka"]["od"] <= d["datum"] <= A["spicka"]["do"]]
BASE_MONTH = MESICE[int(A["srovnani"]["od"][5:7]) - 1]
BASE_LOK = MESICE_LOK[int(A["srovnani"]["od"][5:7]) - 1]
SHOW_MONTH = MESICE[int(A["obdobi"]["od"][5:7]) - 1]
SHOW_YEAR = A["obdobi"]["od"][:4]


def band_html():
    if not PEAK_I:
        return ""
    left = PEAK_I[0] / NA * 100
    width = len(PEAK_I) / NA * 100
    return f'<div class="viz-band" style="left:{left:.3f}%;width:{width:.3f}%"></div>'


def legend(items):
    """items: [(text, class swatche)], swatch je obdélník jako značka v grafu.
    Třída is-clip místo obdélníku ukáže znak ▲, stejný jako u useknutých dní."""
    def mark(c):
        return '<b aria-hidden="true">▲</b>' if c == "is-clip" else f'<i class="{c}"></i>'
    return '<div class="viz-legend">' + "".join(
        f'<span>{mark(c)}{escape(t)}</span>' for t, c in items) + "</div>"


def a_x_axis():
    picks = [i for i in range(NA) if i % 7 == 0]
    if NA - 1 - picks[-1] >= 4:
        picks.append(NA - 1)
    return x_axis([(i, dm(DAYS[i]["datum"])) for i in picks], NA)


def a_bars(key, cls, unit, title, note, leg=None, short=False):
    vals = [d[key] or 0 for d in DAYS]
    top, step = nice_axis(max(vals))
    imax = max(range(NA), key=lambda i: vals[i])
    lab_txt = num(vals[imax]) if unit == "n" else times(vals[imax])
    cols = "".join(
        f'<span class="viz-col{(" " + cls) if cls else ""}" data-i="{i}" style="height:{v / top * 100:.2f}%">'
        + (f'<span class="viz-lab">{lab_txt}</span>' if i == imax else "") + "</span>"
        for i, v in enumerate(vals))
    return (
        f'<figure class="viz-fig"><figcaption class="viz-head"><span class="viz-title">{escape(title)}</span>'
        f'<span class="viz-note">{escape(note)}</span></figcaption>{legend(leg) if leg else ""}'
        f'<div class="viz-plot{" is-short" if short else ""}" style="--n:{NA}">{grid_html(top, step, unit)}{band_html()}'
        f'<div class="viz-cols">{cols}</div></div>{a_x_axis()}</figure>'
    )


def a_pno(title, note):
    pts = [d["pno"] for d in DAYS]
    target = A["cil_pno"]
    # Cesta se přeruší u dne bez tržby (PNO neexistuje), stejně jako v dashboardu.
    path, pen = [], False
    for i, p in enumerate(pts):
        if p is None:
            pen = False
            continue
        y = 100 - min(p, PNO_CAP) / PNO_CAP * 100
        path.append(f'{"L" if pen else "M"}{i + 0.5:.1f} {y:.2f}')
        pen = True
    # Useknuté dny jen značkou ▲. Hodnota s procenty se na mobilu slévala se sousedním dnem,
    # je v tooltipu a v tabulce, legenda to vysvětluje.
    clips = "".join(
        f'<span class="viz-clip" style="left:{(i + 0.5) / NA * 100:.3f}%">▲</span>'
        for i, p in enumerate(pts) if p is not None and p > PNO_CAP)
    # Jeden popisek: nejnižší PNO ve špičce (nebo v celém období, když špička chybí).
    pool = [i for i in (PEAK_I or range(NA)) if pts[i] is not None]
    imin = min(pool, key=lambda i: pts[i])
    lab = (f'<span class="viz-dot" style="left:{(imin + 0.5) / NA * 100:.3f}%;bottom:{pts[imin] / PNO_CAP * 100:.2f}%"></span>'
           f'<span class="viz-lab" style="left:{(imin + 0.5) / NA * 100:.3f}%;bottom:{pts[imin] / PNO_CAP * 100:.2f}%;'
           f'margin-bottom:9px">{pct(pts[imin])}</span>')
    # Cíl je jen čárkovaná čára, popisek je v legendě. Popisek přímo v grafu překrývala čára PNO.
    tgt = f'<div class="viz-target" style="bottom:{target / PNO_CAP * 100:.2f}%"></div>'
    svg = (f'<svg class="viz-line" viewBox="0 0 {NA} 100" preserveAspectRatio="none" aria-hidden="true">'
           f'<path d="{" ".join(path)}" vector-effect="non-scaling-stroke"/></svg>')
    leg = [("PNO za den", "is-pno"), (f"cíl {num(target)}{NBSP}%", "is-target")]
    if clips:
        leg.append((f"nad {num(PNO_CAP)}{NBSP}%, hodnota v tabulce", "is-clip"))
    return (
        f'<figure class="viz-fig"><figcaption class="viz-head"><span class="viz-title">{escape(title)}</span>'
        f'<span class="viz-note">{escape(note)}</span></figcaption>{legend(leg)}'
        f'<div class="viz-plot" style="--n:{NA}">{grid_html(PNO_CAP, 25, "pct")}{band_html()}{tgt}{svg}{lab}{clips}</div>'
        f'{a_x_axis()}</figure>'
    )


def a_tips(with_budget):
    out = []
    for d in DAYS:
        wd = DNY_CELE[dt.date.fromisoformat(d["datum"]).weekday()]
        rows = [[f"{wd} {dm(d['datum'])}"], ["objednávek", num(d["objednavky"]), C_ORDERS]]
        if with_budget:
            rows.append([f"rozpočtu proti {BASE_LOK}", times(d["rozpocet_nasobek"]), C_BUDGET])
        rows.append(["PNO", pct(d["pno"]) if d["pno"] is not None else "bez tržby", C_PNO])
        out.append(rows)
    return out


def a_table(with_budget):
    head = ["Den", "Objednávky", "PNO"]
    if with_budget:
        head.insert(2, f"Rozpočet (průměr {BASE_MONTH} = 1×)")
    rows = []
    for d in DAYS:
        r = [dm(d["datum"]), num(d["objednavky"]), pct(d["pno"]) if d["pno"] is not None else "bez tržby"]
        if with_budget:
            r.insert(2, times(d["rozpocet_nasobek"]))
        rows.append(r)
    return table("Zobrazit data v tabulce", head, rows)


def chart_a(full):
    note = f"{SHOW_MONTH} {SHOW_YEAR}, po dnech"
    parts = [a_bars("objednavky", "", "n", "Objednávky za den", note,
                    leg=[(f"akce {dm(A['spicka']['od'])} až {dm(A['spicka']['do'])}", "is-band")])]
    if full:
        parts.append(a_bars("rozpocet_nasobek", "is-budget", "x", "Denní rozpočet na reklamu",
                            f"1× = průměrný den v {BASE_LOK}, bez částek", short=True))
    parts.append(a_pno("PNO za den", "náklady na reklamu / tržby bez DPH a dopravy"))
    aria = (f"E-shop A, {SHOW_MONTH} {SHOW_YEAR}: {num(A['obdobi']['objednavky'])} objednávek a PNO "
            f"{pct(A['obdobi']['pno'])}, v {BASE_LOK} {num(A['srovnani']['objednavky'])} objednávek a PNO "
            f"{pct(A['srovnani']['pno'])}.")
    return (f'<div data-viz-group data-cross data-tips="{attr_json(a_tips(full))}" role="group" aria-label="{escape(aria)}">'
            + "".join(parts) + "</div>" + a_table(full))


def kpi_a(n):
    best = A["nejlepsi_den"]
    items = [
        (f"Objednávky za {SHOW_MONTH}", num(A["obdobi"]["objednavky"]), f"{BASE_MONTH}: {num(A['srovnani']['objednavky'])}"),
        (f"PNO za {SHOW_MONTH}", pct(A["obdobi"]["pno"]), f"{BASE_MONTH}: {pct(A['srovnani']['pno'])}, cíl {num(A['cil_pno'])}{NBSP}%"),
        ("Nejlepší den", f"{num(best['objednavky'])} objednávek", f"{dm(best['datum'])} při PNO {pct(best['pno'])}"),
    ]
    if n == 4:
        items.append(("Nejvyšší denní rozpočet", times(MAX_BUDGET), f"proti průměrnému dni v {BASE_LOK}"))
    return kpis(items, "is-3" if n == 3 else "")


MAX_BUDGET = max(d["rozpocet_nasobek"] or 0 for d in DAYS)


def phases_a():
    def per_day(p):
        n = (dt.date.fromisoformat(p["do"]) - dt.date.fromisoformat(p["od"])).days + 1
        return p["objednavky"] / n

    def span(p):
        return f"{dm(p['od'])} až {dm(p['do'])}"

    # Nahoře tučně, o jakou fázi jde, pod tím menším písmem data.
    cols = [
        (BASE_MONTH.capitalize(), "celý měsíc", A["srovnani"], False),
        ("Před akcí", span(A["pred_spickou"]), A["pred_spickou"], False),
        ("Akce", span(A["spicka"]), A["spicka"], True),
        ("Po akci", span(A["po_spicce"]), A["po_spicce"], False),
    ]
    th = "".join(f'<th scope="col">{escape(name)}<small>{escape(dates)}</small></th>' for name, dates, _, _ in cols)

    def row(label, f):
        return ("<tr><th scope=\"row\">" + escape(label) + "</th>"
                + "".join(f'<td{" class=\"is-hot\"" if hot else ""}>{escape(f(p))}</td>' for _, _, p, hot in cols) + "</tr>")

    return ('<div class="viz-root viz-phases-wrap"><table class="viz-phases">'
            f'<thead><tr><th scope="col">Období</th>{th}</tr></thead><tbody>'
            + row("Objednávek za den", lambda p: cz(per_day(p), 1))
            + row("Objednávek celkem", lambda p: num(p["objednavky"]))
            + row("PNO", lambda p: pct(p["pno"]))
            + "</tbody></table></div>")


# ── E-shop B: objednávky po měsících, letos proti loňsku ────────────────────
B = DATA["eshop_b"]
Y0, Y1 = B["roky"]
BM = B["mesice"]
NB = len(BM)


def chart_b():
    v0 = [m[Y0] for m in BM]
    v1 = [m[Y1] for m in BM]
    top, step = nice_axis(max(v0 + v1))
    s0, s1 = B["sezona"]["od_mesic"], B["sezona"]["do_mesic"]
    left = (s0 - 1) / NB * 100
    width = (s1 - s0 + 1) / NB * 100
    band = f'<div class="viz-band" style="left:{left:.3f}%;width:{width:.3f}%"></div>'
    # Popisky jen u dvou měsíců, o kterých je text: největší propad a největší nárůst.
    drop = min(range(NB), key=lambda i: (v1[i] - v0[i]) if v0[i] else 0)
    rise = max(range(NB), key=lambda i: v1[i] - v0[i])
    show = {drop, rise}

    def bar(v, cls, i, soft):
        lab = f'<span class="viz-lab{" is-soft" if soft else ""}">{num(v)}</span>' if i in show else ""
        return f'<span class="viz-col{cls}" style="height:{v / top * 100:.2f}%">{lab}</span>'

    groups = "".join(
        f'<div class="viz-grp" data-i="{i}">{bar(a, " is-last", i, True)}{bar(b, "", i, False)}</div>'
        for i, (a, b) in enumerate(zip(v0, v1)))
    tips = [[[MESICE[m["mesic"] - 1].capitalize()], [Y1, num(m[Y1]), C_ORDERS], [Y0, num(m[Y0]), C_LAST]] for m in BM]
    leg = legend([(Y1, ""), (Y0, "is-last"), (f"sezóna {MESICE[s0 - 1]} až {MESICE[s1 - 1]}", "is-band")])
    xa = x_axis([(i, MESICE_KRATCE[m["mesic"] - 1]) for i, m in enumerate(BM)], NB)
    aria = (f"E-shop B, objednávky po měsících, {Y1} proti {Y0}. Sezóna {MESICE[s0 - 1]} až {MESICE[s1 - 1]}: "
            f"{num(B['sezona'][Y1])} proti {num(B['sezona'][Y0])}.")
    fig = (
        f'<div data-viz-group data-tips="{attr_json(tips)}" role="group" aria-label="{escape(aria)}">'
        f'<figure class="viz-fig"><figcaption class="viz-head"><span class="viz-title">Objednávky po měsících</span>'
        f'<span class="viz-note">{Y1} proti {Y0}</span></figcaption>{leg}'
        f'<div class="viz-plot" style="--n:{NB}">{grid_html(top, step, "n")}{band}<div class="viz-cols">{groups}</div></div>'
        f'{xa}</figure></div>'
    )
    tab = table("Zobrazit data v tabulce", ["Měsíc", Y1, Y0],
                [[MESICE[m["mesic"] - 1], num(m[Y1]), num(m[Y0])] for m in BM])
    return fig + tab


def kpi_b():
    s0, s1 = B["sezona"]["od_mesic"], B["sezona"]["do_mesic"]
    i_rise = max(range(NB), key=lambda i: BM[i][Y1] - BM[i][Y0])
    i_drop = min(range(NB), key=lambda i: (BM[i][Y1] - BM[i][Y0]) if BM[i][Y0] else 0)
    r, d = BM[i_rise], BM[i_drop]
    return kpis([
        (f"Sezóna {MESICE[s0 - 1]} až {MESICE[s1 - 1]}", num(B["sezona"][Y1]), f"{Y0}: {num(B['sezona'][Y0])}, {N['b_season_change']}"),
        (f"{MESICE[r['mesic'] - 1].capitalize()} {Y1}", num(r[Y1]), f"{Y0}: {num(r[Y0])}, {times(r[Y1] / r[Y0])}"),
        (f"{MESICE[d['mesic'] - 1].capitalize()} {Y1}", num(d[Y1]), f"{Y0}: {num(d[Y0])}, {N['b_drop_change']}"),
    ], "is-3")


# ── Heatmapa: kdy chodí objednávky ───────────────────────────────────────────
def _oklab(hexc):
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    l = 0.4122214708 * lin[0] + 0.5363325363 * lin[1] + 0.0514459929 * lin[2]
    m = 0.2119034982 * lin[0] + 0.6806995451 * lin[1] + 0.1073969566 * lin[2]
    s = 0.0883024619 * lin[0] + 0.2817188376 * lin[1] + 0.6299787005 * lin[2]
    l, m, s = (x ** (1 / 3) for x in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _hex(lab):
    L, a, b = lab
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    out = ""
    for c in rgb:
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        out += f"{round(c * 255):02x}"
    return "#" + out


HEAT_LO, HEAT_HI = _oklab("#eef2fb"), _oklab("#0A33C8")


def heat_color(v):
    t = v / 100
    return _hex(tuple(lo + (hi - lo) * t for lo, hi in zip(HEAT_LO, HEAT_HI)))


def heat_a():
    H = A["heatmapa"]
    grid = H["radky_po_az_ne"]
    cells = []
    for d, row in enumerate(grid):
        cells.append(f"<b>{DNY[d]}</b>")
        for h, v in enumerate(row):
            tip = [[f"{DNY_CELE[d]} {h}:00 až {h + 1}:00"], ["z nejsilnější hodiny", f"{num(v)}{NBSP}%", ""]]
            cells.append(f'<span class="viz-cell" style="background:{heat_color(v)}" data-tip="{attr_json(tip)}"></span>')
    hours = "<span></span>" + "".join(
        f'<span style="grid-column:{h + 2}">{h}</span>' if h % 6 == 0 else "" for h in range(24))
    od, do = H["od"], H["do"]
    note = f"{MESICE[int(od[5:7]) - 1]} až {MESICE[int(do[5:7]) - 1]} {do[:4]}, den v týdnu × hodina"
    grad = f"linear-gradient(90deg,{heat_color(0)},{heat_color(50)},{heat_color(100)})"
    return (
        f'<figure class="viz-fig"><figcaption class="viz-head"><span class="viz-title">Kdy chodí objednávky</span>'
        f'<span class="viz-note">{escape(note)}</span></figcaption>'
        f'<div class="viz-heat" role="img" aria-label="{escape(N["heat_summary"])}">{"".join(cells)}</div>'
        f'<div class="viz-heat-x" aria-hidden="true">{hours}</div>'
        f'<div class="viz-scale" aria-hidden="true"><span>méně</span><i style="background:{grad}"></i><span>více objednávek</span></div>'
        f'</figure>'
    )


# ── čísla pro texty (pages_data.py je bere odsud, ať texty nikdy neodporují grafům) ──
def _season_change():
    a, b = B["sezona"][Y0], B["sezona"][Y1]
    ch = (b - a) / a * 100
    return ("+" if ch >= 0 else "−") + num(abs(ch)) + NBSP + "%"


def _drop_change():
    i = min(range(NB), key=lambda i: (BM[i][Y1] - BM[i][Y0]) if BM[i][Y0] else 0)
    ch = (BM[i][Y1] - BM[i][Y0]) / BM[i][Y0] * 100
    return ("+" if ch >= 0 else "−") + num(abs(ch)) + NBSP + "%"


def _change_words(old, new):
    """246 -> 276: „o 12 % víc“. Kolem poloviny dolů „o polovinu“."""
    ch = (new - old) / old * 100
    if ch < 0 and 45 <= -ch <= 55:
        return "o polovinu"
    return f"o {num(abs(ch))}{NBSP}% {'víc' if ch >= 0 else 'méně'}"


def _dni(n):
    """Český tvar: 1 den, 2 až 4 dny, 5 a víc dní."""
    return f"{n}{NBSP}" + ("den" if n == 1 else "dny" if 2 <= n <= 4 else "dní")


def _months_words(od, do):
    """2026-07-01 až 2026-08-31 -> „červenec a srpen“, delší úsek „květen až srpen“."""
    m0, m1 = int(od[5:7]), int(do[5:7])
    if m0 == m1:
        return MESICE[m0 - 1]
    if m1 - m0 == 1:
        return f"{MESICE[m0 - 1]} a {MESICE[m1 - 1]}"
    return f"{MESICE[m0 - 1]} až {MESICE[m1 - 1]}"


def _heat_peaks():
    """Nejsilnější hodiny ve všední dny: hodiny nad 80 % maxima, spojené do úseků, dva nejsilnější úseky.
    Vrací text typu „ráno mezi 7. a 10. hodinou a večer mezi 20. a 23. hodinou“."""
    g = A["heatmapa"]["radky_po_az_ne"]
    avg = [sum(g[d][h] for d in range(5)) / 5 for h in range(24)]
    lim = max(avg) * 0.8
    runs, cur = [], []
    for h in range(24):
        if avg[h] >= lim:
            cur.append(h)
        elif cur:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    runs = sorted(sorted(runs, key=lambda r: -sum(avg[h] for h in r))[:2])

    def part(r):
        a, b = r[0], r[-1] + 1
        when = "ráno" if a < 10 else "dopoledne" if a < 12 else "odpoledne" if a < 18 else "večer"
        return f"{when} mezi {a}. a {b}. hodinou"
    return " a ".join(part(r) for r in runs)


def _heat_weakest():
    days = [sum(r) for r in A["heatmapa"]["radky_po_az_ne"]]
    return DNY_CELE[days.index(min(days))]


def _heat_weekdays_stronger():
    days = [sum(r) for r in A["heatmapa"]["radky_po_az_ne"]]
    return sum(days[:5]) / 5 > sum(days[5:]) / 2


def _heat_summary():
    kdy = "ve všední dny " if _heat_weekdays_stronger() else ""
    return (f"Heatmapa objednávek E-shopu A podle dne v týdnu a hodiny. Nejvíc objednávek přichází "
            f"{kdy}{_heat_peaks()}, nejslabší den je {_heat_weakest()}.")


i_rise = max(range(NB), key=lambda i: BM[i][Y1] - BM[i][Y0])
i_drop = min(range(NB), key=lambda i: (BM[i][Y1] - BM[i][Y0]) if BM[i][Y0] else 0)
N = {
    "a_month": SHOW_MONTH, "a_year": SHOW_YEAR, "a_base_month": BASE_MONTH,
    "a_month_lok": MESICE_LOK[int(A["obdobi"]["od"][5:7]) - 1],
    "a_base_lok": BASE_LOK, "a_base_gen": MESICE_GEN[int(A["srovnani"]["od"][5:7]) - 1],
    # „z října“, ale „ze srpna“ a „ze září“: před s a z se píše ze.
    "a_base_z_gen": ("ze " if MESICE_GEN[int(A["srovnani"]["od"][5:7]) - 1][0] in "szšž" else "z ")
                    + MESICE_GEN[int(A["srovnani"]["od"][5:7]) - 1],
    "a_base_orders": num(A["srovnani"]["objednavky"]), "a_base_pno": pct(A["srovnani"]["pno"]),
    "a_orders": num(A["obdobi"]["objednavky"]), "a_pno": pct(A["obdobi"]["pno"]),
    "a_target": f"{num(A['cil_pno'])}{NBSP}%",
    "a_before_pno": pct(A["pred_spickou"]["pno"]), "a_before_to": dm(A["pred_spickou"]["do"]),
    "a_peak_from": dm(A["spicka"]["od"]), "a_peak_to": dm(A["spicka"]["do"]),
    "a_peak_orders": num(A["spicka"]["objednavky"]), "a_peak_pno": pct(A["spicka"]["pno"]),
    "a_after_pno": pct(A["po_spicce"]["pno"]),
    "a_best_orders": num(A["nejlepsi_den"]["objednavky"]), "a_best_pno": pct(A["nejlepsi_den"]["pno"]),
    "a_best_day": dm(A["nejlepsi_den"]["datum"]),
    "a_max_budget": cz(MAX_BUDGET, 1),
    "b_y0": Y0, "b_y1": Y1,
    "b_season": f"{MESICE[B['sezona']['od_mesic'] - 1]} až {MESICE[B['sezona']['do_mesic'] - 1]}",
    "b_season_y0": num(B["sezona"][Y0]), "b_season_y1": num(B["sezona"][Y1]),
    "b_season_change": _season_change(),
    "b_rise_month": MESICE[BM[i_rise]["mesic"] - 1], "b_rise_y0": num(BM[i_rise][Y0]), "b_rise_y1": num(BM[i_rise][Y1]),
    "b_rise_x": cz(BM[i_rise][Y1] / BM[i_rise][Y0], 1),
    "b_drop_month": MESICE[BM[i_drop]["mesic"] - 1], "b_drop_y0": num(BM[i_drop][Y0]), "b_drop_y1": num(BM[i_drop][Y1]),
    "b_drop_change": _drop_change(), "b_drop_lok": MESICE_LOK[BM[i_drop]["mesic"] - 1],
    "b_pno": pct(B["pno_od_cervence"]["pno"]),
    "b_pno_from": MESICE_GEN[int(B["pno_od_cervence"]["od"][5:7]) - 1],
    "b_pno_to": MESICE[int(B["pno_od_cervence"]["do"][5:7]) - 1],
    "b_pno_months": _months_words(B["pno_od_cervence"]["od"], B["pno_od_cervence"]["do"]),
    # Cíl E-shopu B posílá export od 21. 11. 2026, starší JSON ho nemá. Oba klienti mají cíl 30 %.
    "b_target": f"{num(B.get('cil_pno', A['cil_pno']))}{NBSP}%",
    "b_target_rel": "pod cílem" if B["pno_od_cervence"]["pno"] <= B.get("cil_pno", A["cil_pno"]) else "nad cílem",
    "b_season_change_txt": _change_words(B["sezona"][Y0], B["sezona"][Y1]),
    "b_drop_words": _change_words(BM[i_drop][Y0], BM[i_drop][Y1]),
    "a_peak_days": _dni(len(PEAK_I)),
    "heat_peaks": _heat_peaks(),
    "heat_weekdays": "všední dny " if _heat_weekdays_stronger() else "",
    "heat_weakest": _heat_weakest(),
    "heat_summary": _heat_summary(),
}

FOOT = ("Skutečná data z klientského dashboardu. Jméno e-shopu a částky v korunách nezveřejňuji, "
        "počty objednávek a PNO jsou přesně tak, jak je dashboard ukazuje.")

CHARTS = {
    "a": window("Dashboard klienta", f"E-shop A · {SHOW_MONTH} {SHOW_YEAR}",
                kpi_a(4) + chart_a(full=True)),
    "a_phases": phases_a(),
    "b": window("Dashboard klienta", f"E-shop B · sezóna {Y1}", kpi_b() + chart_b()),
    # Krátký popisek: na mobilu se dlouhý text v liště lámal na dva řádky.
    "heat": window("Dashboard klienta", "E-shop A · den a hodina", heat_a()),
    "foot": f'<p class="viz-root viz-foot">{escape(FOOT)}</p>',
}


def konstelace_teaser():
    """Náhled konstelace Meta a Google na homepage. ZATÍM SE NEPOUŽÍVÁ: Pavel 21. 11. 2026 konstelaci
    z webu odložil. Pro návrat přidat volání do homepage_block() a vrátit snímky do assets/img/vyhodnoceni/."""
    img = "/assets/img/vyhodnoceni/konstelace-prunik-meta-google"
    return (
        '<figure class="viz-root shot"><picture>'
        f'<source media="(max-width: 599px)" srcset="{img}-mobil.webp" width="720" height="417">'
        f'<img src="{img}-desktop.webp" width="1200" height="824" loading="lazy" decoding="async" '
        'alt="Ukázka průniku Mety a Googlu: kusy prodané přes Metu proti kusům prodaným přes Google u stejných produktů">'
        '</picture><figcaption>Meta a Google v jednom obraze: které produkty prodávají na obou kanálech. '
        'Na podstránce ukazuji celý pohled z mého dashboardu. <span class="shot-tag">Ukázková data</span></figcaption></figure>'
    )


def homepage_block():
    inner = window("Dashboard klienta", f"E-shop A · {SHOW_MONTH} {SHOW_YEAR}", kpi_a(3) + chart_a(full=False))
    return (
        f"{H_START}\n"
        '      <div class="section-tag">Jak vyhodnocuji</div>\n'
        '      <h2 class="section-title">Výsledky měřím na objednávkách, ne v reklamním systému</h2>\n'
        '      <p class="answer-first">V dashboardu se potkají skutečné objednávky z e-shopu '
        's náklady ze všech reklamních účtů, data jsou průběžně aktualizovaná. PNO počítám z tržeb bez DPH a bez dopravy, takže si ho Google ani Meta '
        'nemůžou přikrášlit. Podle toho se rozhoduje, kam přidat rozpočet a kde ubrat.</p>\n'
        f"      {inner}\n"
        f'      <p class="viz-root viz-foot">{escape(FOOT)}</p>\n'
        '      <a class="viz-root viz-more" href="/jak-vyhodnocuji/">Jak přesně vyhodnocuji →</a>\n'
        f"      {H_END}"
    )


def main():
    s = io.open(HTML, encoding="utf-8").read()
    if H_START not in s or H_END not in s:
        sys.exit("CHYBA: markery VYHODNOCENI nenalezeny v index.html")
    i, j = s.index(H_START), s.index(H_END) + len(H_END)
    s = s[:i] + homepage_block() + s[j:]
    io.open(HTML, "w", encoding="utf-8", newline="").write(s)
    print(f"OK: homepage blok Jak vyhodnocuji (E-shop A {SHOW_MONTH} {SHOW_YEAR}: "
          f"{N['a_orders']} obj., PNO {N['a_pno']})")


if __name__ == "__main__":
    main()
