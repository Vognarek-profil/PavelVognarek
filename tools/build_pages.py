# -*- coding: utf-8 -*-
"""
Generátor podstránek (landing pages) z tools/pages_data.py.

Proč generátor: nav, patička, GTM, consent a JSON-LD se opakují na každé stránce.
Ruční kopírování se rozejde už u třetí stránky. Zdroj pravdy je pages_data.py,
HTML se z něj vždycky přegeneruje.

Použití:  python tools/build_pages.py
"""
import io
import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_data import PAGES, NAV, SITE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = SITE["base"]

CONSENT_GTM = """  <!-- Google Consent Mode v2 (MUST be before GTM) -->
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('consent', 'default', {
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied',
      'analytics_storage': 'denied',
      'functionality_storage': 'granted',
      'security_storage': 'granted',
      'wait_for_update': 500
    });
    try {
      var _c = localStorage.getItem('cookieConsent_v1');
      if (_c) {
        var _parsed = JSON.parse(_c);
        if (Date.now() - _parsed.timestamp < 31536000000) {
          gtag('consent', 'update', _parsed.settings);
        }
      }
    } catch(e) {}
  </script>

  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-MQPCXPXD');</script>
  <!-- End Google Tag Manager -->"""

LOGO_SVG = """      <svg class="logo-icon" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="60" height="60" rx="12" fill="#0A33C8"/>
        <text x="50%" y="52%" font-family="Inter,sans-serif" font-weight="900" font-size="24" fill="white" text-anchor="middle" dominant-baseline="middle">PV</text>
        <rect x="12" y="50" width="36" height="3" rx="1.5" fill="#10A5C8"/>
      </svg>"""

PAGE_JS = """  <script>
    // Mobilní menu
    (function(){
      var btn = document.getElementById('navToggle'), menu = document.getElementById('navLinks');
      if (!btn || !menu) return;
      function setOpen(open){
        menu.classList.toggle('is-open', open);
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
        btn.setAttribute('aria-label', open ? 'Zavřít menu' : 'Otevřít menu');
      }
      btn.addEventListener('click', function(){ setOpen(!menu.classList.contains('is-open')); });
      menu.addEventListener('click', function(e){ if (e.target.tagName === 'A') setOpen(false); });
      document.addEventListener('keydown', function(e){
        if (e.key === 'Escape' && menu.classList.contains('is-open')) { setOpen(false); btn.focus(); }
      });
    })();

    // Kontaktní formulář – stejný endpoint jako na homepage (/api/contact)
    document.getElementById('contactForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      var form = e.target, btn = form.querySelector('.submit-btn'), status = document.getElementById('formStatus');
      btn.disabled = true; btn.textContent = 'Odesílám…'; status.innerHTML = '';
      var data = Object.fromEntries(new FormData(form).entries());
      try {
        var res = await fetch('/api/contact', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify(data)
        });
        var json = await res.json().catch(function(){ return {}; });
        if (res.ok && json.ok) {
          status.innerHTML = '<span style="color:var(--cyan)">Zpráva odeslána. Ozvu se vám co nejdříve.</span>';
          window.dataLayer = window.dataLayer || [];
          window.dataLayer.push({ event: 'form_submit', form_id: 'contactForm', form_location: window.location.pathname });
          form.reset();
        } else { throw new Error(json.error || 'Chyba serveru'); }
      } catch (err) {
        status.innerHTML = '<span style="color:#ff6b6b">Nepodařilo se odeslat. Zkuste to znovu nebo napište přímo na <a href="mailto:pavogppc@gmail.com" style="color:#ff6b6b">pavogppc@gmail.com</a>.</span>';
      }
      btn.disabled = false; btn.textContent = 'Odeslat zprávu →';
    });
  </script>"""


def nav_html(slug):
    links = []
    for item in NAV:
        active = ' class="active"' if item["slug"] == slug else ""
        links.append(f'      <a href="{item["href"]}"{active}>{escape(item["label"])}</a>')
    return f"""  <nav class="site-nav">
    <a href="/" class="logo-nav" aria-label="Pavel Vognárek, úvodní stránka">
{LOGO_SVG}
      <div class="logo-name">
        <strong>Pavel Vognárek</strong>
        <span>PPC Specialista</span>
      </div>
    </a>
    <div class="nav-links" id="navLinks">
{chr(10).join(links)}
    </div>
    <a href="#kontakt" class="nav-cta">Domluvit konzultaci</a>
    <button type="button" class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="navLinks" aria-label="Otevřít menu">
      <span></span><span></span><span></span>
    </button>
  </nav>"""


def jsonld(p, url):
    graph = [
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": p["title"],
            "description": p["description"],
            "isPartOf": {"@id": BASE + "/#website"},
            "about": {"@id": url + "#service"},
            "inLanguage": "cs-CZ",
            "dateModified": SITE["modified"],
            "breadcrumb": {"@id": url + "#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Úvod", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": p["crumb"], "item": url},
            ],
        },
        {
            "@type": "Service",
            "@id": url + "#service",
            "name": p["service_name"],
            "serviceType": p["service_type"],
            "description": p["description"],
            "url": url,
            "provider": {"@id": BASE + "/#service"},
            "areaServed": [{"@type": "Country", "name": n} for n in p.get("area", ["Česká republika"])],
            "inLanguage": "cs-CZ",
        },
        {
            "@type": "FAQPage",
            "@id": url + "#faq",
            "inLanguage": "cs-CZ",
            "isPartOf": {"@id": BASE + "/#website"},
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in p["faq"]
            ],
        },
    ]
    body = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
    return "\n".join("  " + ln for ln in body.splitlines())


def render(p):
    slug = p["slug"]
    url = f"{BASE}/{slug}/"
    faq_rows = "\n".join(
        '        <details class="faq-item">\n'
        f'          <summary class="faq-q">{escape(q, quote=False)} <span class="faq-toggle" aria-hidden="true">+</span></summary>\n'
        f'          <div class="faq-a">{escape(a, quote=False)}</div>\n'
        "        </details>"
        for q, a in p["faq"]
    )
    sections = "\n".join(
        f'  <section{" class=" + chr(34) + sec["class"] + chr(34) if sec.get("class") else ""}>\n'
        '    <div class="container">\n'
        f'      <h2>{escape(sec["h2"], quote=False)}</h2>\n'
        f'      <div class="prose">{sec["html"]}</div>\n'
        "    </div>\n"
        "  </section>"
        for sec in p["sections"]
    )
    related = "\n".join(
        f'        <a href="/{r}/">{escape(PAGES_BY_SLUG[r]["nav_label"], quote=False)}'
        f'<span>{escape(PAGES_BY_SLUG[r]["teaser"], quote=False)}</span></a>'
        for r in p["related"]
    )
    foot_nav = "\n".join(
        f'      <a href="{i["href"]}">{escape(i["label"], quote=False)}</a>' for i in NAV
    )

    return f"""<!DOCTYPE html>
<html lang="cs">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>

{CONSENT_GTM}

  <title>{escape(p["title"], quote=False)}</title>
  <meta name="description" content="{escape(p["description"])}"/>
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"/>
  <meta name="author" content="Pavel Vognárek"/>

  <link rel="canonical" href="{url}"/>
  <link rel="alternate" hreflang="cs-CZ" href="{url}"/>
  <link rel="alternate" hreflang="x-default" href="{url}"/>

  <meta name="geo.region" content="CZ-JM"/>
  <meta name="geo.placename" content="Velké Bílovice, Břeclav"/>
  <meta name="geo.position" content="48.84946;16.89932"/>
  <meta name="ICBM" content="48.84946, 16.89932"/>

  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 60 60'%3E%3Crect width='60' height='60' rx='12' fill='%230A33C8'/%3E%3Ctext x='50%25' y='54%25' font-family='Inter,sans-serif' font-weight='900' font-size='24' fill='white' text-anchor='middle' dominant-baseline='middle'%3EPV%3C/text%3E%3C/svg%3E"/>
  <link rel="apple-touch-icon" sizes="180x180" href="/assets/icons/apple-touch-icon.png"/>
  <meta name="theme-color" content="#0A33C8"/>

  <meta property="og:type" content="website"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:title" content="{escape(p["title"])}"/>
  <meta property="og:description" content="{escape(p["description"])}"/>
  <meta property="og:image" content="{BASE}/og_pavel_vognarek.jpg"/>
  <meta property="og:image:type" content="image/jpeg"/>
  <meta property="og:image:width" content="1200"/>
  <meta property="og:image:height" content="630"/>
  <meta property="og:image:alt" content="Pavel Vognárek, PPC specialista a Google Ads konzultant z Břeclavi"/>
  <meta property="og:locale" content="cs_CZ"/>
  <meta property="og:site_name" content="Pavel Vognárek"/>

  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{escape(p["title"])}"/>
  <meta name="twitter:description" content="{escape(p["description"])}"/>
  <meta name="twitter:image" content="{BASE}/og_pavel_vognarek.jpg"/>
  <meta name="twitter:image:alt" content="Pavel Vognárek, PPC specialista a Google Ads konzultant z Břeclavi"/>

  <script type="application/ld+json">
{jsonld(p, url)}
  </script>

  <link rel="stylesheet" href="/assets/css/lp.css"/>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap" media="print" onload="this.media='all';this.onload=null"/>
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap"/></noscript>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MQPCXPXD"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

  <a class="skip-link" href="#obsah">Přeskočit na obsah</a>

{nav_html(slug)}

  <main id="obsah">

  <header class="lp-hero">
    <div class="container">
      <nav class="crumbs" aria-label="Drobečková navigace">
        <a href="/">Úvod</a><span>›</span>{escape(p["crumb"], quote=False)}
      </nav>
      <h1>{p["h1"]}</h1>
      <p class="lead">{escape(p["lead"], quote=False)}</p>
      <div class="hero-btns">
        <a class="btn btn-primary" href="#kontakt">Domluvit konzultaci zdarma</a>
        <a class="btn btn-ghost" href="#faq">Časté otázky</a>
      </div>
    </div>
  </header>

{sections}

  <section class="bg-light" id="faq">
    <div class="container">
      <div class="section-tag">FAQ</div>
      <h2>{escape(p["faq_title"], quote=False)}</h2>
      <div class="faq-list">
{faq_rows}
      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-tag">Dál na webu</div>
      <h2>Související služby</h2>
      <div class="related">
{related}
      </div>
    </div>
  </section>

  <section class="contact-bg" id="kontakt">
    <div class="container">
      <div class="section-tag" style="color:var(--cyan)">Kontakt</div>
      <h2>{escape(p["cta_title"], quote=False)}</h2>
      <p class="contact-lead">{escape(p["cta_text"], quote=False)}</p>
      <div class="contact-rows">
        <a href="tel:+420608633916">+420 608 633 916</a>
        <a href="mailto:pavogppc@gmail.com">pavogppc@gmail.com</a>
      </div>
      <div class="form-wrap">
        <form id="contactForm">
          <div style="position:absolute;left:-9999px;top:-9999px" aria-hidden="true">
            <label for="f-website">Website</label>
            <input id="f-website" type="text" name="website" tabindex="-1" autocomplete="off"/>
          </div>
          <div class="form-row">
            <label for="f-jmeno">Jméno</label>
            <input id="f-jmeno" type="text" name="jmeno" placeholder="Jan Novák" autocomplete="name" required/>
          </div>
          <div class="form-row">
            <label for="f-email">Email</label>
            <input id="f-email" type="email" name="email" placeholder="jan@firma.cz" autocomplete="email" required/>
          </div>
          <div class="form-row">
            <label for="f-telefon">Telefon</label>
            <input id="f-telefon" type="tel" name="telefon" placeholder="+420 ..." autocomplete="tel"/>
          </div>
          <div class="form-row">
            <label for="f-zprava">Zpráva</label>
            <textarea id="f-zprava" name="zprava" placeholder="{escape(p["form_placeholder"])}" required></textarea>
          </div>
          <button type="submit" class="submit-btn">Odeslat zprávu →</button>
          <p class="form-consent">Odesláním formuláře souhlasíte se zpracováním osobních údajů podle <a href="/zasady-ochrany-osobnich-udaju.html">zásad ochrany osobních údajů</a>. Údaje používám výhradně pro odpověď na vaši poptávku.</p>
          <div class="form-status" id="formStatus" role="status" aria-live="polite"></div>
        </form>
      </div>
    </div>
  </section>

  </main>

  <footer>
    <div class="foot-nav">
      <a href="/">Úvod</a>
{foot_nav}
    </div>
    <p>&copy; 2026 Pavel Vognárek · IČO 76591867 · Velké Bílovice ·
      <a href="/zasady-ochrany-osobnich-udaju.html">Zásady ochrany osobních údajů</a></p>
  </footer>

{PAGE_JS}
</body>
</html>
"""


PAGES_BY_SLUG = {p["slug"]: p for p in PAGES}


def main():
    for p in PAGES:
        d = os.path.join(ROOT, p["slug"])
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, "index.html")
        io.open(out, "w", encoding="utf-8", newline="").write(render(p))
        words = len(" ".join(sec["html"] for sec in p["sections"]).split())
        print(f"  {p['slug']:26s} -> {p['slug']}/index.html   (~{words} slov v sekcích, {len(p['faq'])} FAQ)")
    print(f"OK: {len(PAGES)} stránek")


if __name__ == "__main__":
    main()
