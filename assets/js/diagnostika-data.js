/* ──────────────────────────────────────────────────────────────────────────
   Diagnostika: otázky asistenta, volby a pravidla doporučení.

   JEDINÝ ZDROJ PRAVDY pro prohlížeč i server. Prohlížeč ho načte jako běžný
   skript (window.DIAGNOSTIKA), funkce api/diagnostika.js ho načte přes
   require() a podle něj ověří odpovědi a sestaví e-mail. Když se tu změní
   otázka nebo volba, server ji pozná automaticky.

   Texty pro Pavla (otázky na konzultaci) sem nepatří, soubor je veřejný.
   Jsou v api/_lib/diagnostika-email.js a klíčují se podle id pravidla.
   tools/check.py hlídá, že každé pravidlo tam má svůj záznam.

   Pravidla psaní: žádné vykřičníky, žádné pomlčky uprostřed věty,
   Sklik se u samotného Slovenska nenabízí.
   ────────────────────────────────────────────────────────────────────────── */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.DIAGNOSTIKA = factory();
})(this, function () {
  'use strict';

  var OTAZKY = [
    {
      id: 'problem', kratce: 'Hlavní problém', typ: 'jedna',
      text: 'S čím teď potřebujete pomoct nejvíc?',
      volby: [
        { id: 'nerosteme', text: 'Utrácíme víc, ale nerosteme' },
        { id: 'mereni', text: 'Nevíme, co nám vlastně funguje' },
        { id: 'jeden_kanal', text: 'Jsme závislí na jednom kanálu' },
        { id: 'brand', text: 'Lidé naši značku neznají' },
        { id: 'agentura', text: 'Agentura řeší jen kampaně, celek nikdo' },
        { id: 'sezona', text: 'Chystám akci nebo sezónu, třeba Black Friday' },
        { id: 'start', text: 'Začínám s reklamou nebo spouštím nový e-shop' },
        { id: 'jine', text: 'Něco jiného' }
      ]
    },
    {
      id: 'typ', kratce: 'Typ podnikání', typ: 'jedna',
      text: 'Co děláte?',
      volby: [
        { id: 'eshop', text: 'Mám e-shop' },
        { id: 'b2b', text: 'B2B firma nebo služby' },
        { id: 'lokalni', text: 'Lokální firma, služby v regionu' },
        { id: 'jine', text: 'Něco jiného' }
      ]
    },
    {
      id: 'trh', kratce: 'Trh', typ: 'jedna',
      text: 'Kde prodáváte?',
      volby: [
        { id: 'cz', text: 'Česko' },
        { id: 'sk', text: 'Slovensko' },
        { id: 'czsk', text: 'Česko i Slovensko' },
        { id: 'jinde', text: 'Jinde v zahraničí' }
      ]
    },
    {
      id: 'kanaly', kratce: 'Kde inzeruje', typ: 'vice',
      text: 'Kde dnes inzerujete? Můžete vybrat víc možností.',
      volby: [
        { id: 'google', text: 'Google Ads' },
        { id: 'sklik', text: 'Sklik', skrytKdyz: { trh: ['sk'] } },
        { id: 'meta', text: 'Facebook a Instagram' },
        { id: 'bing', text: 'Microsoft Ads (Bing)' },
        { id: 'youtube', text: 'YouTube' },
        { id: 'chatgpt', text: 'ChatGPT' },
        { id: 'srovnavace', text: 'Zbožové srovnávače' },
        { id: 'nikde', text: 'Zatím nikde', vylucna: true }
      ]
    },
    {
      id: 'sprava', kratce: 'Kdo spravuje', typ: 'jedna',
      text: 'Kdo se o reklamu stará?',
      preskocitKdyz: { kanaly: ['nikde'] },
      volby: [
        { id: 'sami', text: 'Sami ve firmě' },
        { id: 'agentura', text: 'Agentura' },
        { id: 'freelancer', text: 'Freelancer' },
        { id: 'nikdo', text: 'Nikdo pravidelně, kampaně jen běží' }
      ]
    },
    {
      id: 'rozpocet', kratce: 'Měsíční rozpočet', typ: 'jedna',
      text: 'Kolik měsíčně do reklamy dáváte, nebo chcete dávat?',
      volby: [
        { id: 'do20', text: 'Do 20 tisíc Kč', textSk: 'Do 800 €' },
        { id: '20_100', text: '20 až 100 tisíc Kč', textSk: '800 až 4 000 €' },
        { id: '100_500', text: '100 až 500 tisíc Kč', textSk: '4 000 až 20 000 €' },
        { id: 'nad500', text: 'Přes 500 tisíc Kč', textSk: 'Přes 20 000 €' },
        { id: 'nevim', text: 'Zatím nevím' },
        { id: 'neuvadet', text: 'Nechci uvádět' }
      ]
    },
    {
      id: 'kdy', kratce: 'Naléhavost', typ: 'jedna',
      text: 'Jak rychle to potřebujete řešit?',
      volby: [
        { id: 'hned', text: 'Co nejdřív' },
        { id: 'mesic', text: 'Během měsíce' },
        { id: 'zjistuji', text: 'Zatím se jen rozhlížím' }
      ]
    }
  ];

  var SLUZBY = {
    audit: {
      nazev: 'Audit PPC a optimalizace ROAS', url: '/ppc-audit/',
      popis: 'Projdu účty, měření i feed a ukážu, kde utíkají peníze a co opravit jako první.'
    },
    google: {
      nazev: 'Správa Google Ads a Sklik', nazevSk: 'Správa Google Ads', url: '/sprava-google-ads/',
      popis: 'Vyhledávání, nákupy a Performance Max řízené podle marže, ne podle počtu kliknutí.'
    },
    meta: {
      nazev: 'Správa Meta Ads', url: '/sprava-meta-ads/',
      popis: 'Facebook a Instagram jako rovnocenný kanál: kreativy, publika a katalog, které prodávají.'
    },
    eshop: {
      nazev: 'PPC pro e-shopy a srovnávače', url: '/ppc-pro-eshopy/',
      popis: 'Produktový feed, nákupní kampaně a srovnávače napojené na skutečné objednávky.'
    },
    vyhodnoceni: {
      nazev: 'Vyhodnocení na skutečných objednávkách', url: '/jak-vyhodnocuji/',
      popis: 'Přehled, kde se objednávky z e-shopu potkají s náklady ze všech reklamních účtů.'
    },
    sezona: {
      nazev: 'Black Friday a sezónní kampaně', url: '/#sluzby',
      popis: 'Příprava akce: rozpočty, feed, kreativy a vypnutí po skončení. Strategie, se kterou jsem vyhrál Sklik výzvu Black Friday 2025.',
      popisSk: 'Příprava akce: rozpočty, feed, kreativy a vypnutí po skončení.'
    },
    lokalni: {
      nazev: 'PPC pro firmy z jižní Moravy', url: '/ppc-specialista-brno/',
      popis: 'Kampaně cílené na váš region a schůzka osobně v Brně, Břeclavi nebo u vás ve firmě.'
    }
  };

  // Pravidla se procházejí v pořadí, služby se skládají bez opakování, nejvýš MAX_SLUZEB.
  // kdyz: {otazka: [id]} = odpověď je jedna z voleb (u otázky s více volbami: aspoň jedna).
  // nema: {otazka: [id]} = žádná z vyjmenovaných voleb nevybraná.
  var PRAVIDLA = [
    { id: 'p_nerosteme', kdyz: { problem: ['nerosteme'] }, sluzby: ['audit', 'vyhodnoceni'] },
    { id: 'p_mereni', kdyz: { problem: ['mereni'] }, sluzby: ['vyhodnoceni', 'audit'] },
    { id: 'p_kanal_bez_mety', kdyz: { problem: ['jeden_kanal'], kanaly: ['google', 'sklik'] }, nema: { kanaly: ['meta'] }, sluzby: ['meta'] },
    { id: 'p_kanal_bez_googlu', kdyz: { problem: ['jeden_kanal'], kanaly: ['meta'] }, nema: { kanaly: ['google'] }, sluzby: ['google'] },
    { id: 'p_kanal', kdyz: { problem: ['jeden_kanal'] }, sluzby: ['google', 'meta'] },
    { id: 'p_brand', kdyz: { problem: ['brand'] }, sluzby: ['meta', 'google'] },
    { id: 'p_agentura', kdyz: { problem: ['agentura'] }, sluzby: ['audit', 'vyhodnoceni'] },
    { id: 'p_sezona', kdyz: { problem: ['sezona'] }, sluzby: ['sezona'] },
    { id: 'p_start', kdyz: { problem: ['start'] }, sluzby: ['google', 'meta'] },
    { id: 'p_jine', kdyz: { problem: ['jine'] }, sluzby: ['audit'] },
    { id: 'p_eshop', kdyz: { typ: ['eshop'] }, sluzby: ['eshop'] },
    { id: 'p_lokalni', kdyz: { typ: ['lokalni'], trh: ['cz', 'czsk'] }, sluzby: ['lokalni'] },
    { id: 'p_srovnavace', kdyz: { kanaly: ['srovnavace'] }, sluzby: ['eshop'] },
    { id: 'p_bez_reklamy', kdyz: { kanaly: ['nikde'] }, sluzby: ['google', 'meta'] },
    { id: 'p_prevzeti', kdyz: { sprava: ['agentura', 'freelancer', 'nikdo'] }, sluzby: ['audit'] }
  ];
  var MAX_SLUZEB = 3;

  function jakoPole(v) {
    if (v == null) return [];
    return Array.isArray(v) ? v : [v];
  }

  function splnuje(podminky, odpovedi, zadna) {
    for (var otazka in podminky) {
      if (!Object.prototype.hasOwnProperty.call(podminky, otazka)) continue;
      var mam = jakoPole(odpovedi[otazka]);
      var shoda = podminky[otazka].some(function (id) { return mam.indexOf(id) !== -1; });
      if (zadna ? shoda : !shoda) return false;
    }
    return true;
  }

  function jenSlovensko(odpovedi) { return odpovedi.trh === 'sk'; }

  function otazka(id) {
    for (var i = 0; i < OTAZKY.length; i++) if (OTAZKY[i].id === id) return OTAZKY[i];
    return null;
  }

  // Volby, které se mají ukázat (Sklik pryč, když se prodává jen na Slovensku).
  function volby(o, odpovedi) {
    return o.volby.filter(function (v) { return !v.skrytKdyz || !splnuje(v.skrytKdyz, odpovedi); });
  }

  function popisekVolby(v, odpovedi) {
    return (jenSlovensko(odpovedi) && v.textSk) ? v.textSk : v.text;
  }

  function preskocit(o, odpovedi) {
    return !!o.preskocitKdyz && splnuje(o.preskocitKdyz, odpovedi);
  }

  // Otázky, které se v daném průchodu opravdu kladou.
  function aktivniOtazky(odpovedi) {
    return OTAZKY.filter(function (o) { return !preskocit(o, odpovedi); });
  }

  function sluzba(id, odpovedi) {
    var s = SLUZBY[id], sk = jenSlovensko(odpovedi);
    return {
      id: id, url: s.url,
      nazev: (sk && s.nazevSk) ? s.nazevSk : s.nazev,
      popis: (sk && s.popisSk) ? s.popisSk : s.popis
    };
  }

  // Doporučení: které služby nabídnout a která pravidla k tomu vedla.
  function doporuc(odpovedi) {
    var ids = [], pravidla = [];
    PRAVIDLA.forEach(function (p) {
      if (!splnuje(p.kdyz, odpovedi)) return;
      if (p.nema && !splnuje(p.nema, odpovedi, true)) return;
      pravidla.push(p.id);
      p.sluzby.forEach(function (s) { if (ids.indexOf(s) === -1) ids.push(s); });
    });
    if (!ids.length) ids.push('audit');
    return {
      sluzby: ids.slice(0, MAX_SLUZEB).map(function (id) { return sluzba(id, odpovedi); }),
      pravidla: pravidla
    };
  }

  return {
    verze: 1,
    otazky: OTAZKY,
    sluzby: SLUZBY,
    pravidla: PRAVIDLA,
    otazka: otazka,
    volby: volby,
    popisekVolby: popisekVolby,
    preskocit: preskocit,
    aktivniOtazky: aktivniOtazky,
    doporuc: doporuc,
    texty: {
      uvod: 'Dobrý den. Pár otázkami zjistíme, s čím vám můžu pomoct. Zabere to asi dvě minuty. Odpovědi uvidím, až na konci vyplníte kontakt a odešlete je.',
      doplneni: 'Chcete něco doplnit vlastními slovy? Třeba co se poslední dobou změnilo, nebo co by pro vás byl úspěch za tři měsíce.',
      shrnuti: 'Podle odpovědí vám můžu pomoct hlavně s tímhle:',
      dalsiKrok: 'Dalším krokem je úvodní konzultace. Trvá asi 30 minut a je zdarma. Nechte mi kontakt a ozvu se vám.',
      souhlas: 'Odesláním souhlasíte se zpracováním osobních údajů podle zásad ochrany osobních údajů. Údaje používám výhradně pro odpověď na vaši poptávku.',
      hotovo: 'Hotovo, odpovědi mám. Ozvu se vám co nejdříve.'
    }
  };
});
