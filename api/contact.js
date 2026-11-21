const { createRateLimiter, clientIp, parseBody, esc, EMAIL_RE, sendMail } = require('./_lib/mail');

// Max 5 odeslání z jedné IP za 10 minut (jen v paměti instance, viz _lib/mail.js).
const tooManyRequests = createRateLimiter(10 * 60 * 1000, 5);

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  if (tooManyRequests(clientIp(req))) {
    res.setHeader('Retry-After', '600');
    return res.status(429).json({ error: 'Příliš mnoho pokusů. Zkuste to prosím za chvíli, nebo napište přímo na pavogppc@gmail.com.' });
  }

  try {
    const { jmeno, email, telefon, zprava, website } = parseBody(req);

    if (website) return res.status(200).json({ ok: true });

    if (!jmeno || !email || !zprava) {
      return res.status(400).json({ error: 'Vyplňte prosím jméno, email a zprávu.' });
    }
    if (!EMAIL_RE.test(email)) {
      return res.status(400).json({ error: 'Neplatný formát emailu.' });
    }
    if (jmeno.length > 200 || email.length > 200 || (telefon || '').length > 50 || zprava.length > 5000) {
      return res.status(400).json({ error: 'Překročena maximální délka pole.' });
    }

    const text = [
      `Nová zpráva z pavelvognarek.cz`,
      ``,
      `Jméno: ${jmeno}`,
      `Email: ${email}`,
      `Telefon: ${telefon || '(neuvedeno)'}`,
      ``,
      `Zpráva:`,
      zprava,
    ].join('\n');

    const html = `
      <h2 style="margin:0 0 12px;font-family:Arial,sans-serif">Nová zpráva z pavelvognarek.cz</h2>
      <table style="font-family:Arial,sans-serif;font-size:14px;border-collapse:collapse">
        <tr><td style="padding:4px 12px 4px 0;color:#666">Jméno:</td><td style="padding:4px 0"><strong>${esc(jmeno)}</strong></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#666">Email:</td><td style="padding:4px 0"><a href="mailto:${esc(email)}">${esc(email)}</a></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#666">Telefon:</td><td style="padding:4px 0">${esc(telefon || '(neuvedeno)')}</td></tr>
      </table>
      <div style="margin-top:16px;padding:16px;background:#f5f7fb;border-left:3px solid #0A33C8;font-family:Arial,sans-serif;font-size:14px;line-height:1.5;white-space:pre-wrap">${esc(zprava)}</div>
    `;

    const sent = await sendMail({
      replyTo: { name: String(jmeno).slice(0, 200), address: email },
      subject: `Informační formulář – ${jmeno}`,
      text,
      html,
    });
    if (!sent) return res.status(500).json({ error: 'Server není správně nakonfigurován.' });

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('contact error:', err);
    return res.status(500).json({ error: 'Nepodařilo se odeslat zprávu.' });
  }
};
