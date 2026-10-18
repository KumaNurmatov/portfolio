// Cloudflare Worker: принимает бриф с сайта и пересылает его в Telegram.
// Секреты задаются в настройках воркера (Settings → Variables and Secrets), в коде их нет:
//   BOT_TOKEN       — токен бота от @BotFather
//   CHAT_ID         — куда слать (ваш личный chat id или id группы)
//   ALLOWED_ORIGIN  — https://kumanurmatov.github.io (через запятую можно добавить другие домены)

const clip = (v, n) => String(v ?? '').trim().slice(0, n);
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const list = v => (Array.isArray(v) ? v : []).map(x => clip(x, 60)).filter(Boolean).slice(0, 12);

export default {
  async fetch(req, env) {
    const origin = req.headers.get('Origin') || '';
    const allowed = (env.ALLOWED_ORIGIN || '').split(',').map(s => s.trim()).filter(Boolean);
    const okOrigin = !allowed.length || allowed.includes(origin);
    const cors = {
      'Access-Control-Allow-Origin': okOrigin ? origin || '*' : allowed[0],
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Vary': 'Origin',
    };
    const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { ...cors, 'Content-Type': 'application/json' } });

    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (req.method !== 'POST') return json({ ok: false, error: 'method' }, 405);
    if (!okOrigin) return json({ ok: false, error: 'origin' }, 403);

    let d;
    try { d = await req.json(); } catch { return json({ ok: false, error: 'json' }, 400); }
    if (d.website) return json({ ok: true });            // ловушка для ботов: поле, невидимое людям

    const contact = clip(d.contact, 120);
    if (!contact) return json({ ok: false, error: 'contact' }, 400);

    const row = (k, v) => (v ? `<b>${k}:</b> ${esc(v)}` : null);
    const text = [
      '🟦 <b>Новая заявка с сайта</b>',
      '',
      row('Имя', clip(d.name, 80)),
      row('Связь', `${clip(d.channel, 20)} ${contact}`),
      '',
      row('Услуги', list(d.services).join(', ')),
      row('Детали', list(d.detail).join(', ')),
      row('Цель', clip(d.goal, 80)),
      row('Сфера', clip(d.sphere, 80)),
      row('Сроки', clip(d.timing, 40)),
      row('Бюджет', clip(d.budget, 40)),
      '',
      '<b>Бриф:</b>',
      esc(clip(d.brief, 1500)),
      '',
      row('Страница', clip(d.page, 200)),
    ].filter(x => x !== null).join('\n').replace(/\n{3,}/g, '\n\n');

    const tg = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ chat_id: env.CHAT_ID, text, parse_mode: 'HTML', disable_web_page_preview: true }),
    });
    if (!tg.ok) return json({ ok: false, error: 'telegram' }, 502);
    return json({ ok: true });
  },
};
