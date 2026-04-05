# Web Pavel Vognárek – pavelvognarek.cz

## O projektu
Osobní prezentační web pro Pavla Vognárka, PPC specialistu a digitálního marketingového konzultanta.

## Soubory v projektu
| Soubor | Popis |
|---|---|
| `index.html` | Hlavní web – tmavá modrá animovaná verze (původní) |
| `index2.html` | Varianta – bílá + modrá |
| `index3.html` | Varianta – černá + žlutá |
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
Čistý HTML/CSS/JS – vše v jednom souboru. Žádný framework, žádný build step.

### Sekce
1. **Nav** – sticky, animovaný modrý gradient, logo, CTA
2. **Hero** – animovaný gradient, H1, foto v kruhu s rotujícími prstenci
3. **O mně** – bio, certifikáty, highlight karty
4. **Problémy klientů** – 5 karet
5. **Služby** – 4 karty, animovaný modrý bg
6. **Proč já?** – 4 důvody + citát + reference (Sklik výzva, případová studie)
7. **FAQ** – accordion
8. **Kontakt** – formulář (Formspree) + telefon + email
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

### Formulář
- Formspree – `FORMSPREE_ID` konstanta v JS (zatím `YOUR_FORM_ID`, nutno doplnit)

## Kontakt na webu
- **Telefon:** +420 608 633 916
- **Email:** pavogppc@gmail.com

## GitHub & deployment
- **Repozitář:** https://github.com/Vognarek-profil/PavelVognarek
- **Branch:** main
- **Doména:** pavelvognarek.cz (auto-deploy z GitHubu)
- **Git identita:** vognarek@gmail.com / Pavel Vognárek
- **Push:** `git add [soubory] && git commit -m "..." && git push origin main`

## SEO (stav duben 2026)
Viz `seo.md` pro kompletní checklist. Klíčové:
- Title, meta description, canonical, robots – ✅
- OG + Twitter Card tagy – ✅ (`og_pavel_vognarek.webp`)
- Schema.org JSON-LD (Person) – ✅
- sitemap.xml + robots.txt – ✅ (nahrát na server)
- GSC doména ověřena – ✅
- Sitemap odeslat v GSC – ⏳

## Reference / externí odkazy
- [Sklik výzva – Black Friday 2025](https://blog.seznam.cz/2025/12/sklik-vyzva-nejlepsi-black-friday-strategie-ma-viteze/)
- [Případová studie Doppler – Sklik Akademie](https://www.sklikakademie.cz/cs/pripadove-studie/detail/~/17/)

## Vytvořeno / aktualizováno
- Původně: duben 2026
- Poslední aktualizace: duben 2026
