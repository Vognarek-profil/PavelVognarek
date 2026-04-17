# Web Pavel Vognárek – pavelvognarek.cz

## O projektu
Osobní prezentační web pro Pavla Vognárka, PPC specialistu a digitálního marketingového konzultanta z Velkých Bílovic (u Břeclavi).

## Soubory v projektu
| Soubor | Popis |
|---|---|
| `index.html` | Hlavní web – tmavá modrá animovaná verze (původní) |
| `index2.html` | Varianta – bílá + modrá |
| `index3.html` | Varianta – černá + žlutá |
| `zasady-ochrany-osobnich-udaju.html` | GDPR zásady ochrany osobních údajů (odkaz v patičce všech 3 verzí) |
| `api/contact.js` | Vercel serverless funkce pro odesílání kontaktního formuláře přes Gmail SMTP |
| `package.json` | Závislost `nodemailer` (pro `api/contact.js`) |
| `.gitignore` | Ignoruje `node_modules`, `.env`, `.vercel`, `.claude/` |
| `Foto_Pavel_Vognárek.jpg` | Profilová fotka (JPG fallback) |
| `Foto_Pavel_Vognarek.webp` | Profilová fotka ve WebP (62 % menší, používá se primárně) |
| `og_pavel_vognarek.webp` | OG image pro sdílení na soc. sítích (1200×630) |
| `OG image.webp` | Starší OG image – jen fotka, nepoužívá se |
| `sitemap.xml` | Sitemap pro Google Search Console |
| `robots.txt` | Allow: /, odkaz na sitemap |
| `seo.md` | SEO checklist – co je hotovo, co zbývá |
| `claude.md` | Tento soubor – dokumentace projektu |

## Brand (index.html)
- **Primární barva:** #0A33C8 (navy)
- **Akcentová barva:** #10A5C8 (cyan)
- **Font:** Inter (900/700/600/400) – Google Fonts
- **Logo:** SVG inline – modrý čtverec s „PV", cyan lišta dole

## Architektura webu
Čistý HTML/CSS/JS – vše v jednom souboru. Žádný framework, žádný build step. Backend: **Vercel serverless function** v `api/contact.js` pro formulář.

### Sekce
1. **Nav** – sticky, animovaný modrý gradient, logo, CTA
2. **Hero** – animovaný gradient, H1, lokační podtitulek (Břeclav · Brno · JM), foto v kruhu s rotujícími prstenci
3. **O mně** – bio (Velké Bílovice, Břeclav, brněnské agentury), certifikáty, highlight karty
4. **Problémy klientů** – 5 karet
5. **Služby** – 4 karty, animovaný modrý bg
6. **Proč já?** – 4 důvody + citát + reference (Sklik výzva, případová studie)
7. **FAQ** – accordion, 7 otázek (4 původní + 3 lokální: Břeclav, jižní Morava, remote)
8. **Kontakt** – formulář (Vercel /api/contact + Gmail SMTP) + telefon + email
9. **Footer**

## Klíčové technické detaily

### Animace
- **Pozadí:** `@keyframes bgPulse` – animuje `background-position` na velkém gradientu (nav, hero, services, contact)
- **Fotka:** kruh (`border-radius:50%`) + 3 rotující prstence (`.ring-1/2/3`) + `glowPulse`
- **Statistiky:** `@keyframes` count-up přes `IntersectionObserver` – spustí se při scrollu

### Statistiky (hero)
- Bílá pill karta (roots-network styl) s ikonami SVG
- Count-up animace: `data-target` + `data-suffix` na `.count-up` spanech
- Google Certified je text (bez count-up)

### Fotka
- HTML: `<picture>` element – WebP primárně, JPG fallback
- `loading="lazy"` na `<img>`

### Formulář – Vercel serverless + Gmail SMTP
- Frontend: `<form id="contactForm">` posílá JSON POST na `/api/contact`
- Backend: `api/contact.js` – Nodemailer přes `smtp.gmail.com:465`
- **Honeypot:** skryté pole `name="website"` – pokud se vyplní, zpráva se tiše zahodí
- **Validace:** jméno/email/zpráva povinné, max délky, email regex
- **Reply-to:** nastaveno na odesílatelovu adresu (odpověď chodí přímo klientovi)
- **Env proměnné ve Vercelu** (Settings → Environment Variables, pro Production + Preview + Development):
  - `GMAIL_USER` – `pavogppc@gmail.com`
  - `GMAIL_APP_PASSWORD` – 16místné App Password z Google účtu (bez mezer!)
  - `CONTACT_TO` – kam mailovat notifikace (obvykle shodné s `GMAIL_USER`)
- **Změna App Password:** https://myaccount.google.com/apppasswords → vygenerovat nové → aktualizovat ve Vercelu → **Redeploy** (jinak se nenačte)

## Kontakt na webu
- **Telefon:** +420 608 633 916
- **Email:** pavogppc@gmail.com
- **Sídlo:** Zárybnická 457, 691 02 Velké Bílovice, Jihomoravský kraj
- **IČO:** 76591867 (OSVČ, zapsán 1. 3. 2010)

## GitHub & deployment
- **Repozitář:** https://github.com/Vognarek-profil/PavelVognarek
- **Branch:** main
- **Doména:** pavelvognarek.cz (auto-deploy z GitHubu přes Vercel)
- **Git identita:** vognarek@gmail.com / Pavel Vognárek
- **Push:** `git add [soubory] && git commit -m "..." && git push origin main`
- **Vercel projekt:** `pavel-vognarek` (osobní účet vognarek@gmail.com)

## SEO (stav duben 2026)
Viz `seo.md` pro kompletní checklist. Aktuální zaměření: **lokální SEO pro Břeclav + jižní Moravu**.

### Cílené lokality
- **Primárně:** Břeclav, Velké Bílovice, Brno, jižní Morava (Hodonín, Mikulov, Znojmo, Kyjov)
- **Sekundárně:** Praha (zmíněna v textu jako fact o klientech, není v `areaServed`)
- **Globálně:** online pro celou ČR

### Implementováno
- Title + meta description + OG + Twitter – obsahují Břeclav + Brno + jižní Moravu ✅
- Canonical, robots, lang=cs, charset UTF-8 ✅
- Schema.org JSON-LD – **dva bloky:**
  - `Person` – s adresou Velké Bílovice (PSČ 691 02) + `workLocation` (VB, Břeclav, Brno, JM)
  - `ProfessionalService` – s `areaServed` (VB, Břeclav, Brno, Hodonín, Mikulov, Znojmo, Kyjov, Jihomoravský kraj, ČR) + `serviceType`
- H1 podtitulek (bílý uppercase text) s lokacemi ✅
- Alt tag fotky rozšířen o lokality ✅
- Text „O mně" – zmiňuje Velké Bílovice, Břeclav, Brno, jižní Moravu, Prahu ✅
- FAQ – 3 lokální otázky (Břeclavsko, jižní Morava, remote po ČR) ✅
- sitemap.xml + robots.txt ✅
- GSC doména ověřena ✅

### Rozpracováno
- Sitemap odeslat v GSC – ⏳
- **Google Business Profile** – založen (jméno: „Pavel Vognárek – PPC specialista"), ověřen, bývalá klientka „Černý kočky" odebrána. **Zbývá upravit:**
  - Obslužná oblast – smazat „Česká republika", přidat: VB, Břeclav, Hodonín, Mikulov, Brno, Kyjov, Znojmo, okres Břeclav, Jihomoravský kraj
  - Popis firmy (~700 znaků s klíčovými slovy + lokality)
  - Služby, fotky, recenze (3–5 od klientů pro lokální ranking)
- Lokální katalogy (Firmy.cz, Najisto, Zivefirmy) – ⏳
- Samostatné landing pages `/ppc-specialista-breclav/`, `/marketing-jizni-morava/` – ⏳ (delší hra)

## Reference / externí odkazy
- [Sklik výzva – Black Friday 2025](https://blog.seznam.cz/2025/12/sklik-vyzva-nejlepsi-black-friday-strategie-ma-viteze/)
- [Případová studie Doppler – Sklik Akademie](https://www.sklikakademie.cz/cs/pripadove-studie/detail/~/17/)

## Cookie consent + Consent Mode v2
Vlastní řešení v `index.html` (žádný CookieYes, žádný 3rd-party CMP):

- **Consent Mode v2** nastaven v `<head>` **PŘED** GTM snippetem — default `denied` pro `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`. Funkční/security `granted`.
- Na startu inline skript zkontroluje `localStorage['cookieConsent_v1']` a pokud je záznam mladší 12 měsíců, hned provede `gtag('consent','update',...)` — GTM a GA4 tak nestřílí před souhlasem.
- **Cookie banner** + **settings modal** — HTML na konci `<body>`, CSS v `<style>` (hledej komentář `/* COOKIE BANNER */`), JS IIFE s API `window.cookieConsent.acceptAll() / rejectAll() / openSettings() / saveCustom() / toggle()`.
- Kategorie: Nezbytné (locked on), Analytické (GA4), Marketingové (remarketing). Marketingové jedním toggleem ovládají všechny 3 Consent Mode klíče.
- **Odkaz „Nastavení cookies"** v patičce otevírá modal i po udělení souhlasu (trigger: `onclick="cookieConsent.openSettings()"`).
- Nasazeno pouze v `index.html` (index2/3 nepoužívány).

## Vytvořeno / aktualizováno
- Původně: duben 2026
- **2026-04-16** – výměna Formspree za vlastní Vercel serverless + Gmail SMTP, lokální SEO pro Břeclav/jižní Moravu, ProfessionalService schema, 3 nové FAQ
- **2026-04-17** – GDPR zásady ochrany osobních údajů, vlastní cookie consent banner + Google Consent Mode v2 (odchod od CookieYes)
