const nodemailer = require('nodemailer');

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const { jmeno, email, telefon, zprava, website } = body;

    if (website) return res.status(200).json({ ok: true });

    if (!jmeno || !email || !zprava) {
      return res.status(400).json({ error: 'Vyplňte prosím jméno, email a zprávu.' });
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return res.status(400).json({ error: 'Neplatný formát emailu.' });
    }
    if (jmeno.length > 200 || email.length > 200 || (telefon || '').length > 50 || zprava.length > 5000) {
      return res.status(400).json({ error: 'Překročena maximální délka pole.' });
    }

    const user = process.env.GMAIL_USER;
    const pass = process.env.GMAIL_APP_PASSWORD;
    const to = process.env.CONTACT_TO || user;

    if (!user || !pass) {
      console.error('Missing GMAIL_USER or GMAIL_APP_PASSWORD env variables');
      return res.status(500).json({ error: 'Server není správně nakonfigurován.' });
    }

    const transporter = nodemailer.createTransport({
      host: 'smtp.gmail.com',
      port: 465,
      secure: true,
      auth: { user, pass },
    });

    const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));

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

    await transporter.sendMail({
      from: `"pavelvognarek.cz" <${user}>`,
      to,
      replyTo: `"${jmeno}" <${email}>`,
      subject: `Informační formulář – ${jmeno}`,
      text,
      html,
    });

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('contact error:', err);
    return res.status(500).json({ error: 'Nepodařilo se odeslat zprávu.' });
  }
};
