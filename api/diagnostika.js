// Asistent Diagnostika: přijme odpovědi z průvodce na webu a pošle Pavlovi podrobný e-mail.
// Otázky a volby bere ze stejného souboru jako prohlížeč, takže přijme jen to, co web nabízí.
const D = require('../assets/js/diagnostika-data.js');
const { createRateLimiter, clientIp, parseBody, EMAIL_RE, sendMail } = require('./_lib/mail');
const { buildEmail } = require('./_lib/diagnostika-email');

const tooManyRequests = createRateLimiter(10 * 60 * 1000, 5);

// Odkud smí požadavek přijít: produkční doména, náhledy projektu na Vercelu, lokální vývoj.
function originAllowed(req) {
  const src = req.headers.origin || req.headers.referer || '';
  let host;
  try { host = new URL(src).hostname; } catch (e) { return false; }
  return host === 'www.pavelvognarek.cz' || host === 'pavelvognarek.cz'
    || /^pavel-vognarek(-[a-z0-9-]+)?\.vercel\.app$/.test(host)
    || host === 'localhost' || host === '127.0.0.1';
}

const LIMITY = { text: 2000, jmeno: 200, email: 200, telefon: 50, web: 300, stranka: 200 };
const ZDROJE = ['hero', 'problem', 'kontakt', 'plovouci', 'stranka'];

function str(v) { return typeof v === 'string' ? v.trim() : ''; }

// Vrátí očištěné odpovědi, nebo text chyby.
function overOdpovedi(vstup) {
  if (!vstup || typeof vstup !== 'object' || Array.isArray(vstup)) return 'Chybí odpovědi.';
  const odp = {};
  // trh rozhoduje o viditelných volbách, proto se ověří jako první
  for (const o of D.otazky) {
    const v = vstup[o.id];
    if (o.typ === 'vice') {
      if (!Array.isArray(v)) { odp[o.id] = []; continue; }
      odp[o.id] = [...new Set(v.filter((x) => typeof x === 'string'))];
    } else {
      odp[o.id] = typeof v === 'string' ? v : '';
    }
  }
  for (const o of D.otazky) {
    if (D.preskocit(o, odp)) { delete odp[o.id]; continue; }
    const povolene = D.volby(o, odp).map((x) => x.id);
    if (o.typ === 'vice') {
      const vyber = odp[o.id];
      if (!vyber.length) return `Chybí odpověď: ${o.kratce}.`;
      if (vyber.some((id) => povolene.indexOf(id) === -1)) return `Neplatná odpověď: ${o.kratce}.`;
      const vylucne = o.volby.filter((x) => x.vylucna).map((x) => x.id);
      if (vyber.length > 1 && vyber.some((id) => vylucne.indexOf(id) !== -1)) return `Neplatná kombinace: ${o.kratce}.`;
    } else if (povolene.indexOf(odp[o.id]) === -1) {
      return odp[o.id] ? `Neplatná odpověď: ${o.kratce}.` : `Chybí odpověď: ${o.kratce}.`;
    }
  }
  return odp;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!originAllowed(req)) {
    return res.status(403).json({ error: 'Požadavek nepřišel z webu pavelvognarek.cz.' });
  }
  if (tooManyRequests(clientIp(req))) {
    res.setHeader('Retry-After', '600');
    return res.status(429).json({ error: 'Příliš mnoho pokusů. Zkuste to prosím za chvíli, nebo napište přímo na pavogppc@gmail.com.' });
  }

  try {
    const body = parseBody(req);
    if (body.website) return res.status(200).json({ ok: true }); // honeypot

    const pole = {};
    for (const k of Object.keys(LIMITY)) pole[k] = str(body[k]);
    for (const [k, max] of Object.entries(LIMITY)) {
      if (pole[k].length > max) return res.status(400).json({ error: 'Překročena maximální délka pole.' });
    }
    if (!pole.jmeno || !pole.email) {
      return res.status(400).json({ error: 'Vyplňte prosím jméno a e-mail.' });
    }
    if (!EMAIL_RE.test(pole.email)) {
      return res.status(400).json({ error: 'Neplatný formát e-mailu.' });
    }
    if (pole.stranka && !/^\/[\w\-./]*$/.test(pole.stranka)) pole.stranka = '/';
    const zdroj = ZDROJE.indexOf(body.zdroj) !== -1 ? body.zdroj : '';

    const odpovedi = overOdpovedi(body.odpovedi);
    if (typeof odpovedi === 'string') return res.status(400).json({ error: odpovedi });

    const mail = buildEmail(D, { ...pole, odpovedi, zdroj });
    const sent = await sendMail({
      replyTo: { name: pole.jmeno, address: pole.email },
      subject: mail.subject,
      text: mail.text,
      html: mail.html,
    });
    if (!sent) return res.status(500).json({ error: 'Server není správně nakonfigurován.' });

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('diagnostika error:', err);
    return res.status(500).json({ error: 'Nepodařilo se odeslat.' });
  }
};
