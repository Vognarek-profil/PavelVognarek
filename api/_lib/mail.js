// Sdílené pomůcky pro funkce, které posílají e-mail (api/contact.js, api/diagnostika.js).
// Složka začíná podtržítkem, takže z ní Vercel nedělá samostatnou funkci.
const nodemailer = require('nodemailer');

// Jednoduchý rate limit v paměti instance.
// POZOR: Vercel škáluje po instancích, takže tohle NENÍ tvrdý globální limit.
// Zastaví naivní flood na jednu teplou instanci, ne cílený distribuovaný útok.
// Pořádné řešení je sdílené úložiště (Vercel KV / Upstash) nebo Cloudflare Turnstile.
function createRateLimiter(windowMs, maxHits) {
  const hits = new Map();
  return function tooManyRequests(ip) {
    const now = Date.now();
    // úklid starých záznamů, aby Map nerostla donekonečna
    for (const [key, times] of hits) {
      const fresh = times.filter((t) => now - t < windowMs);
      if (fresh.length) hits.set(key, fresh);
      else hits.delete(key);
    }
    const times = hits.get(ip) || [];
    if (times.length >= maxHits) return true;
    times.push(now);
    hits.set(ip, times);
    return false;
  };
}

function clientIp(req) {
  return (req.headers['x-forwarded-for'] || '').split(',')[0].trim()
    || (req.socket && req.socket.remoteAddress) || 'unknown';
}

function parseBody(req) {
  return typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
}

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[c]));

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Odeslání přes Gmail SMTP. Vrací false, když chybí env proměnné (zaloguje to).
async function sendMail({ replyTo, subject, text, html }) {
  const user = process.env.GMAIL_USER;
  const pass = process.env.GMAIL_APP_PASSWORD;
  const to = process.env.CONTACT_TO || user;
  if (!user || !pass) {
    console.error('Missing GMAIL_USER or GMAIL_APP_PASSWORD env variables');
    return false;
  }
  const transporter = nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: { user, pass },
  });
  await transporter.sendMail({
    from: `"pavelvognarek.cz" <${user}>`,
    to,
    replyTo,
    subject,
    text,
    html,
  });
  return true;
}

module.exports = { createRateLimiter, clientIp, parseBody, esc, EMAIL_RE, sendMail };
