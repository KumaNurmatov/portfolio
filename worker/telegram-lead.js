// Cloudflare Worker: заявки с сайта → Telegram + автоответы бота клиенту.
//
// Как это работает:
//   1. Сайт шлёт бриф на POST /        → воркер сохраняет заявку, присылает её владельцу, возвращает id.
//   2. Клиент жмёт «Открыть в Telegram» → бот получает /start <id> и сразу отвечает: бриф, что дальше, кнопки.
//   3. Сообщения клиента боту пересылаются владельцу. Ответ владельца (reply на пересланное) уходит клиенту.
//
// Настройки воркера (Settings → Variables and Secrets):
//   BOT_TOKEN       секрет — токен бота от @BotFather
//   CHAT_ID         ваш chat id (куда приходят заявки)
//   BOT_USERNAME    username бота без @, например kurmanbek_brief_bot
//   WEBHOOK_SECRET  секрет — любая длинная строка, защищает вебхук
//   ALLOWED_ORIGIN  https://kumanurmatov.github.io
//   SITE_URL        https://kumanurmatov.github.io/portfolio/
// Привязка KV (Settings → Bindings → KV namespace): имя переменной LEADS.

const clip = (v, n) => String(v ?? '').trim().slice(0, n);
const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const list = v => (Array.isArray(v) ? v : []).map(x => clip(x, 60)).filter(Boolean).slice(0, 12);
const DAY = 86400;

const CALL_SLOTS = [['today', 'Сегодня'], ['tomorrow', 'Завтра'], ['week', 'На этой неделе'], ['evening', 'Вечером после 18:00']];

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname === '/tg') return telegramUpdate(req, env);
    if (url.pathname === '/setup') return setup(req, env, url);
    return siteLead(req, env);
  },
};

// ---------- Telegram API ----------
async function tg(env, method, payload) {
  const r = await fetch(`https://api.telegram.org/bot${env.BOT_TOKEN}/${method}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
  });
  return r.json().catch(() => ({ ok: false }));
}
const say = (env, chat_id, text, extra = {}) =>
  tg(env, 'sendMessage', { chat_id, text, parse_mode: 'HTML', disable_web_page_preview: true, ...extra });

// ---------- 1. заявка с сайта ----------
async function siteLead(req, env) {
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
  if (d.website) return json({ ok: true });            // ловушка для ботов

  const lead = {
    id: crypto.randomUUID().replace(/-/g, '').slice(0, 10),
    name: clip(d.name, 80), channel: clip(d.channel, 20), contact: clip(d.contact, 120),
    services: list(d.services), detail: list(d.detail), goal: clip(d.goal, 80), sphere: clip(d.sphere, 80),
    timing: clip(d.timing, 40), budget: clip(d.budget, 40), brief: clip(d.brief, 1500), estimate: clip(d.estimate, 160),
    worksUrl: clip(d.worksUrl, 200), page: clip(d.page, 200), created: Date.now(),
  };
  if (!lead.contact) return json({ ok: false, error: 'contact' }, 400);

  const row = (k, v) => (v ? `<b>${k}:</b> ${esc(v)}` : null);
  const text = [
    `🟦 <b>Новая заявка с сайта</b>  #${lead.id}`, '',
    row('Имя', lead.name), row('Связь', `${lead.channel} ${lead.contact}`), '',
    row('Услуги', lead.services.join(', ')), row('Детали', lead.detail.join(', ')), row('Цель', lead.goal),
    row('Сфера', lead.sphere), row('Сроки', lead.timing), row('Бюджет', lead.budget), '',
    '<b>Бриф:</b>', esc(lead.brief), '',
    row('Страница', lead.page),
    env.BOT_USERNAME ? '<i>Когда клиент откроет бота, придёт уведомление.</i>' : null,
  ].filter(x => x !== null).join('\n').replace(/\n{3,}/g, '\n\n');

  const tgUser = lead.contact.match(/^@?([a-z0-9_]{5,32})$/i);
  const kb = tgUser ? { reply_markup: { inline_keyboard: [[{ text: `Написать ${lead.contact.startsWith('@') ? lead.contact : '@' + tgUser[1]}`, url: `https://t.me/${tgUser[1]}` }]] } } : {};
  const sent = await say(env, env.CHAT_ID, text, kb);
  if (!sent.ok) return json({ ok: false, error: 'telegram' }, 502);

  if (env.LEADS) {
    lead.ownerMsg = sent.result.message_id;
    await env.LEADS.put(`lead:${lead.id}`, JSON.stringify(lead), { expirationTtl: 60 * DAY });
  }
  return json({ ok: true, id: lead.id, bot: env.BOT_USERNAME || '' });
}

// ---------- 2–3. обновления от Telegram ----------
async function telegramUpdate(req, env) {
  if (req.headers.get('X-Telegram-Bot-Api-Secret-Token') !== env.WEBHOOK_SECRET) return new Response('forbidden', { status: 403 });
  const u = await req.json().catch(() => null);
  if (!u) return new Response('ok');
  try {
    if (u.callback_query) await onButton(env, u.callback_query);
    else if (u.message) await onMessage(env, u.message);
  } catch (e) { console.error(e); }
  return new Response('ok');                              // Telegram ждёт 200, иначе будет повторять
}

const kv = {
  get: async (env, k) => (env.LEADS ? JSON.parse((await env.LEADS.get(k)) || 'null') : null),
  put: (env, k, v, ttl = 60 * DAY) => env.LEADS && env.LEADS.put(k, JSON.stringify(v), { expirationTtl: ttl }),
};
const who = (m, client) => esc(client?.name || [m.from?.first_name, m.from?.last_name].filter(Boolean).join(' ') || 'Клиент')
  + (m.from?.username ? ` (@${esc(m.from.username)})` : '');

async function onMessage(env, m) {
  const chat = m.chat.id, isOwner = String(chat) === String(env.CHAT_ID);
  const text = m.text || '';

  // владелец отвечает клиенту: reply на пересланное сообщение
  if (isOwner) {
    const target = m.reply_to_message && await kv.get(env, `map:${m.reply_to_message.message_id}`);
    if (target) {
      await tg(env, 'copyMessage', { chat_id: target, from_chat_id: chat, message_id: m.message_id });
      await tg(env, 'setMessageReaction', { chat_id: chat, message_id: m.message_id, reaction: [{ type: 'emoji', emoji: '👍' }] });
    } else if (text.startsWith('/start')) {
      await say(env, chat, 'Готово ✅ Заявки с сайта будут приходить сюда.\nЧтобы ответить клиенту из бота — сделайте <b>reply</b> на его пересланное сообщение.');
    }
    return;
  }

  // клиент пришёл с сайта: /start <id>
  if (text.startsWith('/start')) {
    const id = text.split(' ')[1]?.replace(/[^a-z0-9]/gi, '');
    const lead = id && await kv.get(env, `lead:${id}`);
    if (lead) {
      await kv.put(env, `client:${chat}`, { leadId: id, name: lead.name });
      const hi = lead.name ? `Здравствуйте, ${esc(lead.name)}! 👋` : 'Здравствуйте! 👋';
      await say(env, chat, [
        hi, 'Это бот Курманбека Нурматова. Ваш бриф у меня:', '',
        `<i>${esc(lead.brief)}</i>`, '',
        lead.estimate ? `⏱ ${esc(lead.estimate)}` : null,
        '<b>Что дальше:</b>',
        '1. Изучу задачу и сегодня-завтра пришлю идеи и расчёт.',
        '2. Если удобнее голосом — выберите время для короткого созвона.', '',
        'Можно просто написать сюда: референсы, ссылки, файлы — всё сразу придёт мне.',
      ].filter(x => x !== null).join('\n'), { reply_markup: menu(env, lead) });
      await say(env, env.CHAT_ID, `🔥 <b>${who(m, lead)}</b> открыл бота по заявке #${id} — клиент на связи.\nОтвечайте reply на его сообщения здесь.`,
        lead.ownerMsg ? { reply_parameters: { message_id: lead.ownerMsg, allow_sending_without_reply: true } } : {});
    } else {
      await say(env, chat, 'Здравствуйте! 👋 Это бот Курманбека Нурматова — дизайн, моушн, ИИ и сайты.\n\nОпишите задачу сообщением или соберите бриф за минуту на сайте — так я отвечу точнее.',
        { reply_markup: { inline_keyboard: [[{ text: '📝 Собрать бриф на сайте', url: env.SITE_URL || 'https://kumanurmatov.github.io/portfolio/' }], [{ text: '📞 Созвон 15 минут', callback_data: 'call' }]] } });
    }
    return;
  }

  // любое другое сообщение клиента → владельцу
  const client = await kv.get(env, `client:${chat}`);
  const head = await say(env, env.CHAT_ID, `💬 <b>${who(m, client)}</b>${client?.leadId ? ` · заявка #${client.leadId}` : ''}`);
  const copy = await tg(env, 'copyMessage', { chat_id: env.CHAT_ID, from_chat_id: chat, message_id: m.message_id });
  for (const r of [head, copy]) if (r.ok) await kv.put(env, `map:${r.result.message_id}`, chat, 30 * DAY);

  // автоответ клиенту — не чаще раза в 3 часа
  const ackKey = `ack:${chat}`;
  if (env.LEADS && !(await env.LEADS.get(ackKey))) {
    await env.LEADS.put(ackKey, '1', { expirationTtl: 3 * 3600 });
    await say(env, chat, 'Получил ✅ Передал Курманбеку — он ответит здесь же, обычно в течение пары часов.');
  }
}

function menu(env, lead) {
  return { inline_keyboard: [
    [{ text: '📞 Созвон 15 минут', callback_data: 'call' }],
    [{ text: '✍️ Дополнить бриф', callback_data: 'add' }],
    [{ text: '🖼 Похожие работы', url: lead?.worksUrl || env.SITE_URL || 'https://kumanurmatov.github.io/portfolio/' }],
  ] };
}

async function onButton(env, q) {
  const chat = q.message.chat.id, data = q.data || '';
  await tg(env, 'answerCallbackQuery', { callback_query_id: q.id });
  const client = await kv.get(env, `client:${chat}`);

  if (data === 'call') {
    await say(env, chat, 'Когда удобно созвониться?', { reply_markup: { inline_keyboard: CALL_SLOTS.map(([k, t]) => [{ text: t, callback_data: `slot:${k}` }]) } });
  } else if (data.startsWith('slot:')) {
    const when = (CALL_SLOTS.find(s => s[0] === data.slice(5)) || [, 'В ближайшее время'])[1];
    await say(env, chat, `Записал: <b>${when.toLowerCase()}</b> 👌 Напишу сюда, чтобы подтвердить точное время.`);
    const lead = client?.leadId && await kv.get(env, `lead:${client.leadId}`);
    const r = await say(env, env.CHAT_ID, `📞 <b>${who(q, client)}</b> хочет созвон: <b>${when}</b>${lead ? `\nСвязь: ${esc(lead.channel)} ${esc(lead.contact)} · заявка #${client.leadId}` : ''}\nОтветьте reply, чтобы подтвердить время.`);
    if (r.ok) await kv.put(env, `map:${r.result.message_id}`, chat, 30 * DAY);
  } else if (data === 'add') {
    await say(env, chat, 'Напишите сообщением, что добавить: референсы, ссылки, файлы, пожелания. Всё сразу придёт Курманбеку.');
  }
}

// ---------- однократная настройка вебхука: откройте /setup?key=<WEBHOOK_SECRET> ----------
async function setup(req, env, url) {
  if (!env.WEBHOOK_SECRET || url.searchParams.get('key') !== env.WEBHOOK_SECRET) return new Response('forbidden', { status: 403 });
  const hook = await tg(env, 'setWebhook', {
    url: `${url.origin}/tg`, secret_token: env.WEBHOOK_SECRET, allowed_updates: ['message', 'callback_query'], drop_pending_updates: true,
  });
  await tg(env, 'setMyCommands', { commands: [{ command: 'start', description: 'Начать' }] });
  await tg(env, 'setMyDescription', { description: 'Бот Курманбека Нурматова: дизайн, моушн, ИИ и сайты. Пришлите задачу — отвечу с идеями и расчётом.' });
  return new Response(JSON.stringify({ webhook: hook, kv: !!env.LEADS, bot: env.BOT_USERNAME || null }, null, 2), { headers: { 'Content-Type': 'application/json' } });
}
