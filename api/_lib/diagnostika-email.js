// E-mail Pavlovi z asistenta Diagnostika. Jen na serveru, návštěvník tyhle texty nevidí.
// Otázky na konzultaci jsou klíčované id pravidla z assets/js/diagnostika-data.js.
// tools/check.py hlídá, že tu má každé pravidlo svůj záznam.
const { esc } = require('./mail');

const BASE = 'https://www.pavelvognarek.cz';

const OTAZKY_NA_KONZULTACI = {
  p_nerosteme: [
    'Jak se vyvíjí PNO nebo ROAS za posledních 6 až 12 měsíců a kde rostou ceny za klik?',
    'Jaká je marže? Podle ní se spočítá strop PNO.',
  ],
  p_mereni: [
    'Jak se dnes měří konverze: GA4, Consent Mode, přenos objednávek z e-shopu?',
    'Sedí konverze v reklamních systémech s objednávkami v e-shopu?',
  ],
  p_kanal_bez_mety: ['Kolik obratu jde z Googlu? Zkoušeli už Metu a s jakým výsledkem?'],
  p_kanal_bez_googlu: ['Kolik obratu jde z Mety? Běží vůbec vyhledávání na brand a produkty?'],
  p_kanal: ['Jaký podíl obratu dělá nejsilnější kanál a co se stane, když zakolísá?'],
  p_brand: [
    'Jak velký je podíl brandového vyhledávání a jak se vyvíjí?',
    'Čím se značka liší od konkurence? Co unese kreativa?',
  ],
  p_agentura: [
    'Co přesně chybí u současné agentury: strategie, komunikace, nebo výsledky?',
    'Kdo vlastní reklamní účty a přístupy?',
  ],
  p_sezona: [
    'Kdy akce začíná, jaká je sleva a je připravený feed i kreativy?',
    'Jak dopadla stejná akce loni?',
  ],
  p_start: [
    'Kam má reklama vést (web, e-shop, poptávkový formulář) a je napojené měření konverzí?',
    'Jaká je marže a průměrná objednávka nebo hodnota zakázky?',
  ],
  p_jine: ['Projít volný text a doptat se na cíl.'],
  p_eshop: ['Platforma e-shopu a odkud jde produktový feed (Mergado, přímý export)?'],
  p_lokalni: ['Jaká oblast a jestli chce schůzku osobně.'],
  p_srovnavace: ['Které srovnávače běží a s jakým PNO?'],
  p_bez_reklamy: ['Jaký rozpočet a marži čekají, aby šel nastavit start?'],
  p_prevzeti: ['Převzetí účtu: přístupy, historie změn a co se dělo posledních 6 měsíců.'],
};

const ZDROJE = {
  hero: 'tlačítko v úvodu stránky',
  problem: 'karta problému',
  kontakt: 'kontaktní sekce',
  plovouci: 'plovoucí tlačítko',
  stranka: 'tlačítko na podstránce',
};

function naleznost(odp) {
  const velky = ['20_100', '100_500', 'nad500'].indexOf(odp.rozpocet) !== -1;
  if (odp.kdy === 'hned' && velky) return 'vysoká';
  if (odp.kdy === 'hned' || odp.kdy === 'mesic') return 'střední';
  return 'nízká';
}

// Web zadaný návštěvníkem: „mujeshop.cz“ -> https://mujeshop.cz. Neplatný zůstane jen jako text.
function webUrl(web) {
  if (!web) return null;
  try {
    const u = new URL(/^https?:\/\//i.test(web) ? web : `https://${web}`);
    if (!/^https?:$/.test(u.protocol) || u.hostname.indexOf('.') === -1) return null;
    return u.href;
  } catch (e) {
    return null;
  }
}

function popisOdpovedi(D, otazka, odp) {
  const o = D.otazka(otazka);
  const ids = Array.isArray(odp[otazka]) ? odp[otazka] : [odp[otazka]];
  return ids.map((id) => {
    const v = o.volby.find((x) => x.id === id);
    if (!v) return id;
    // Rozpočet u Slovenska: eura i koruny, ať je to v e-mailu jednoznačné.
    if (v.textSk && odp.trh === 'sk') return `${v.textSk} (${v.text})`;
    return v.text;
  }).join(', ');
}

function buildEmail(D, data) {
  const { odpovedi: odp, text, jmeno, email, telefon, web, stranka, zdroj } = data;
  const dop = D.doporuc(odp);
  const priorita = naleznost(odp);
  const otazky = [];
  dop.pravidla.forEach((id) => (OTAZKY_NA_KONZULTACI[id] || []).forEach((q) => {
    if (otazky.indexOf(q) === -1) otazky.push(q);
  }));
  const radky = D.aktivniOtazky(odp).map((o) => [o.kratce, popisOdpovedi(D, o.id, odp)]);
  const webOdkaz = webUrl(web);
  const strankaUrl = BASE + (stranka || '/');
  const odkud = ZDROJE[zdroj] || 'neznámo';

  const problem = popisOdpovedi(D, 'problem', odp);
  const subject = `Diagnostika (${priorita}): ${popisOdpovedi(D, 'typ', odp)} | ${problem} | ${popisOdpovedi(D, 'rozpocet', odp)}`;

  const textVerze = [
    'Nová diagnostika z pavelvognarek.cz',
    `Naléhavost: ${priorita}`,
    '',
    `Jméno: ${jmeno}`,
    `E-mail: ${email}`,
    `Telefon: ${telefon || '(neuvedeno)'}`,
    `Web: ${web || '(neuvedeno)'}`,
    `Spuštěno z: ${strankaUrl} (${odkud})`,
    '',
    'ODPOVĚDI',
    ...radky.map(([k, v]) => `${k}: ${v}`),
    '',
    'VLASTNÍMI SLOVY',
    text || '(nevyplněno)',
    '',
    'CO VIDĚL JAKO DOPORUČENÍ',
    ...dop.sluzby.map((s) => `${s.nazev}: ${BASE}${s.url}`),
    '',
    'NA CO SE ZEPTAT NA KONZULTACI',
    ...otazky.map((q) => `- ${q}`),
    '',
    'Odpověď na tento e-mail půjde přímo návštěvníkovi.',
  ].join('\n');

  const td = 'padding:6px 14px 6px 0;vertical-align:top;color:#666;white-space:nowrap';
  const tdv = 'padding:6px 0;vertical-align:top';
  const h3 = 'margin:22px 0 8px;font-size:15px;color:#0A33C8';
  const barva = { 'vysoká': '#b42318', 'střední': '#b54708', 'nízká': '#475569' }[priorita];

  const html = `
<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.5;color:#040e2e;max-width:640px">
  <h2 style="margin:0 0 6px">Nová diagnostika z pavelvognarek.cz</h2>
  <p style="margin:0 0 14px"><span style="display:inline-block;padding:2px 10px;border-radius:12px;background:${barva};color:#fff;font-weight:bold;font-size:12px">Naléhavost: ${esc(priorita)}</span></p>
  <table style="border-collapse:collapse;font-size:14px">
    <tr><td style="${td}">Jméno</td><td style="${tdv}"><strong>${esc(jmeno)}</strong></td></tr>
    <tr><td style="${td}">E-mail</td><td style="${tdv}"><a href="mailto:${esc(email)}">${esc(email)}</a></td></tr>
    <tr><td style="${td}">Telefon</td><td style="${tdv}">${telefon ? `<a href="tel:${esc(telefon.replace(/[^\d+]/g, ''))}">${esc(telefon)}</a>` : '(neuvedeno)'}</td></tr>
    <tr><td style="${td}">Web</td><td style="${tdv}">${webOdkaz ? `<a href="${esc(webOdkaz)}">${esc(web)}</a>` : esc(web || '(neuvedeno)')}</td></tr>
    <tr><td style="${td}">Spuštěno z</td><td style="${tdv}"><a href="${esc(strankaUrl)}">${esc(stranka || '/')}</a>, ${esc(odkud)}</td></tr>
  </table>

  <h3 style="${h3}">Odpovědi</h3>
  <table style="border-collapse:collapse;font-size:14px">
    ${radky.map(([k, v]) => `<tr><td style="${td}">${esc(k)}</td><td style="${tdv}"><strong>${esc(v)}</strong></td></tr>`).join('\n    ')}
  </table>

  <h3 style="${h3}">Vlastními slovy</h3>
  <div style="padding:12px 14px;background:#f5f7fb;border-left:3px solid #0A33C8;white-space:pre-wrap">${text ? esc(text) : '<span style="color:#666">(nevyplněno)</span>'}</div>

  <h3 style="${h3}">Co viděl jako doporučení</h3>
  <ul style="margin:0;padding-left:20px">
    ${dop.sluzby.map((s) => `<li><a href="${esc(BASE + s.url)}">${esc(s.nazev)}</a>: ${esc(s.popis)}</li>`).join('\n    ')}
  </ul>

  <h3 style="${h3}">Na co se zeptat na konzultaci</h3>
  <ul style="margin:0;padding-left:20px">
    ${otazky.map((q) => `<li>${esc(q)}</li>`).join('\n    ')}
  </ul>

  <p style="margin:22px 0 0;color:#666;font-size:12px">Odpověď na tento e-mail půjde přímo návštěvníkovi.</p>
</div>`;

  return { subject, text: textVerze, html };
}

module.exports = { buildEmail, OTAZKY_NA_KONZULTACI, webUrl };
