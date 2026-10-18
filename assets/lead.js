// Попап-бриф: ловим интерес, задаём 6 коротких вопросов, собираем ТЗ и отправляем заявку в Telegram.
// Заявки уходят на Cloudflare Worker (см. worker/README.md). Пока ENDPOINT пустой — запасной путь через WhatsApp.
(() => {
  const ENDPOINT = '';                     // URL воркера, например https://lead.<имя>.workers.dev
  const WHATSAPP = '996709906852';
  const BASE = new URL('..', document.currentScript.src).href;   // корень сайта
  const PAGE_SERVICE = document.body.dataset.service || '';

  const safe = s => { try { return s(); } catch { return null; } };
  const ls = { get: k => safe(() => localStorage.getItem(k)), set: (k, v) => safe(() => localStorage.setItem(k, v)) };
  const ss = { get: k => safe(() => sessionStorage.getItem(k)), set: (k, v) => safe(() => sessionStorage.setItem(k, v)) };

  // ---------- вопросы ----------
  const SERVICES = [['identity', 'Айдентика'], ['motion', 'Моушн'], ['ai', 'ИИ-видео и визуалы'], ['ads', 'Креативы для таргета'],
    ['smm', 'SMM-контент'], ['web', 'Сайт'], ['print', 'Полиграфия / наружка'], ['photo-video', 'Фото / видео'], ['unsure', 'Не знаю — помогите разобраться']];
  const GOALS = ['Запуск нового продукта', 'Больше заявок и продаж', 'Обновить бренд', 'Контент на месяц', 'LED / выставка / ивент', 'Другое'];
  const SPHERES = ['Недвижимость', 'Банк / финтех', 'Авто', 'HoReCa', 'E-com / ритейл', 'Красота / здоровье', 'Другое'];
  const DETAILS = {
    web: { q: 'Какой сайт нужен?', opts: ['Лендинг', 'Многостраничный', 'Интернет-магазин', 'Веб-сервис / дашборд', 'ИИ-консультант', '3D / интерактивная карта', 'Редизайн существующего'] },
    ads: { q: 'Где будет реклама?', opts: ['Instagram / Facebook', 'TikTok', 'Google / YouTube', 'Telegram', 'Статика и видео', '5–10 креативов в месяц', '20+ креативов в месяц'] },
    motion: { q: 'Какой формат?', opts: ['Reels / Shorts', 'Ролик 15–30 сек', 'LED-экран', 'Анимация логотипа', 'Explainer', 'Прероллы'] },
    identity: { q: 'Что уже есть?', opts: ['Ничего, с нуля', 'Логотип есть — нужен стиль', 'Нужен ребрендинг', 'Нужен только логотип'], single: true },
    ai: { q: 'Что сгенерировать?', opts: ['Рекламный ролик', 'Фотосессия продукта', 'Персонаж бренда', 'Визуалы для соцсетей', 'Доработка рендеров'] },
    smm: { q: 'Что нужно для соцсетей?', opts: ['Визуальная концепция', 'Посты и карусели', 'Reels', 'Сторис и актуальные', 'Шаблоны для команды'] },
    print: { q: 'Что печатаем?', opts: ['Меню', 'Баннеры / наружка', 'Буклеты / листовки', 'Упаковка', 'Сувенирка / мерч', 'Презентация / КП'] },
    'photo-video': { q: 'Что снимаем?', opts: ['Предметка', 'Авто', 'Интерьеры / недвижимость', 'Люди / бьюти', 'Видео с ведущим', 'Аэросъёмка'] },
  };
  const DETAIL_ORDER = ['web', 'ads', 'motion', 'identity', 'ai', 'smm', 'print', 'photo-video'];
  const TIMING = ['За неделю — срочно', '2–4 недели', '1–2 месяца', 'Не горит'];
  const BUDGET = ['До $300', '$300–1000', '$1000–3000', '$3000+', 'Подскажите по бюджету'];
  const DAYS = { identity: [7, 14], motion: [3, 7], ai: [3, 7], ads: [2, 5], smm: [5, 10], web: [7, 21], print: [3, 7], 'photo-video': [2, 5] };
  const WORKS = {
    identity: ['media/img/amanat-cover.jpg', 'media/img/amanat-carriers.jpg', 'media/img/alykul-logo.jpg'],
    motion: ['media/video/archa-motion.jpg', 'media/video/jetour-x50.jpg', 'media/video/alykul-beishe.jpg'],
    ai: ['media/video/archa-film.jpg', 'media/img/ai-autumn.jpg', 'media/video/mbank-osago.jpg'],
    ads: ['media/img/mb-26.jpg', 'media/img/greenline-park.jpg', 'media/img/soueast-s09.jpg'],
    smm: ['media/img/archa-investor.jpg', 'media/img/archa-story-1.jpg', 'media/img/ivory-service.jpg'],
    web: ['media/img/site-ivory.jpg', 'media/img/site-freeways.jpg', 'media/img/site-agrofi.jpg'],
    print: ['media/img/alykul-menu-company.jpg', 'media/img/jetour-t2-flyer.jpg', 'media/img/archa-banner.jpg'],
    'photo-video': ['media/img/freeways-gls.jpg', 'media/img/florodora-2.jpg', 'media/img/alykul-ship.jpg'],
  };
  // строчная первая буква, но аббревиатуры (3D, SMM, LED) не трогаем
  const lc = t => /^[A-ZА-Я0-9]{2}/.test(t) ? t : t.charAt(0).toLowerCase() + t.slice(1);
  const label = k => (SERVICES.find(s => s[0] === k) || [k, k])[1];

  // ---------- состояние ----------
  const S = { services: PAGE_SERVICE && DETAILS[PAGE_SERVICE] ? [PAGE_SERVICE] : [], goal: '', sphere: '', sphereOther: '',
    detail: [], timing: '', budget: '', brief: '', briefEdited: false, name: '', channel: 'Telegram', contact: '', website: '' };
  const detailKey = () => DETAIL_ORDER.find(k => S.services.includes(k));
  const steps = () => ['service', 'goal', 'sphere', ...(detailKey() ? ['detail'] : []), 'timing', 'budget', 'result'];
  let step = 0, isOpen = false, mode = 'quiz';

  // ---------- разметка ----------
  const root = document.createElement('div');
  root.innerHTML = `
  <div class="lead" role="dialog" aria-modal="false" aria-labelledby="leadQ" data-lenis-prevent hidden>
    <div class="lead__head"><span class="mono lead__step"></span><button class="lead__x" type="button" aria-label="Закрыть">✕</button></div>
    <div class="lead__bar"><i></i></div>
    <div class="lead__body"></div>
    <div class="lead__foot"><button class="lead__back mono" type="button">← Назад</button><button class="btn btn--solid lead__next" type="button">Дальше</button></div>
  </div>
  <button class="lead-pill mono" type="button" hidden><i class="dot"></i>Собрать бриф за 60 сек</button>`;
  document.body.append(...root.children);
  const box = document.querySelector('.lead'), body = box.querySelector('.lead__body'), stepEl = box.querySelector('.lead__step');
  const bar = box.querySelector('.lead__bar i'), back = box.querySelector('.lead__back'), next = box.querySelector('.lead__next');
  const pill = document.querySelector('.lead-pill');

  const chips = (opts, sel, multi) => `<div class="lead__chips">${opts.map(o => {
    const [v, t] = Array.isArray(o) ? o : [o, o];
    return `<button type="button" class="lead__chip${sel.includes(v) ? ' is-on' : ''}" data-v="${v}" aria-pressed="${sel.includes(v)}">${t}</button>`;
  }).join('')}</div>${multi ? '<p class="lead__hint mono">Можно выбрать несколько</p>' : ''}`;

  function makeBrief() {
    const svc = S.services.filter(s => s !== 'unsure').map(label);
    const parts = [];
    parts.push(svc.length ? `Нужно: ${svc.map(lc).join(', ')}.` : 'Пока не понимаю, какой формат нужен — нужна консультация.');
    const dk = detailKey();
    if (dk && S.detail.length) parts.push(`${DETAILS[dk].q.replace('?', '')}: ${S.detail.map(lc).join(', ')}.`);
    if (S.goal) parts.push(`Цель — ${lc(S.goal)}.`);
    const sph = S.sphere === 'Другое' && S.sphereOther ? S.sphereOther : S.sphere;
    if (sph) parts.push(`Сфера — ${lc(sph)}.`);
    if (S.timing) parts.push(`Сроки: ${lc(S.timing)}.`);
    if (S.budget) parts.push(`Бюджет: ${S.budget}.`);
    return parts.join(' ');
  }
  function estimate() {
    const r = S.services.filter(k => DAYS[k]).map(k => DAYS[k]);
    if (!r.length) return 'Сначала короткий созвон на 15 минут — разберёмся в задаче и выберем формат.';
    const from = Math.max(...r.map(x => x[0])), to = Math.max(...r.map(x => x[1])) + (r.length - 1) * 3;
    return `Ориентировочно ${from}–${to} рабочих дней${S.timing.startsWith('За неделю') && to > 7 ? ', срочный режим обсудим' : ''}.`;
  }

  // ---------- экраны ----------
  function render() {
    const list = steps(); step = Math.min(step, list.length - 1);
    const id = list[step], total = list.length - 1;
    box.classList.toggle('is-teaser', mode === 'teaser');
    box.classList.toggle('is-done', mode === 'done');
    stepEl.textContent = mode === 'quiz' ? (id === 'result' ? 'Ваш бриф' : `${String(step + 1).padStart(2, '0')} / ${String(total).padStart(2, '0')}`) : (mode === 'done' ? 'Готово' : 'Бриф за 60 секунд');
    bar.style.transform = `scaleX(${mode === 'quiz' ? (step + 1) / list.length : mode === 'done' ? 1 : 0})`;
    back.hidden = mode !== 'quiz' || step === 0;
    next.hidden = mode !== 'quiz';
    next.disabled = false; next.textContent = 'Дальше';

    if (mode === 'teaser') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">Задача есть, но&nbsp;пока размыто?</h3>
        <p class="lead__p">Ответьте на 6 коротких вопросов — соберу из них понятное ТЗ, покажу похожие работы и сроки.</p>
        <div class="lead__row"><button type="button" class="btn btn--solid" data-act="start">Давай</button><button type="button" class="btn" data-act="later">Позже</button></div>`;
      return;
    }
    if (mode === 'done') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">Спасибо<span class="lead__name"></span>!</h3>
        <p class="lead__p">${ENDPOINT ? `Бриф у меня. Отвечу в ${S.channel} в течение дня — обычно быстрее.` : 'Открылся WhatsApp с готовым брифом — осталось нажать «Отправить». Отвечу в течение дня.'}</p>
        <div class="lead__row"><a class="btn btn--solid" href="${BASE}${S.services[0] && DETAILS[S.services[0]] ? 'services/' + S.services[0] + '.html' : '#works'}">Смотреть работы</a><button type="button" class="btn" data-act="close">Закрыть</button></div>`;
      if (S.name) body.querySelector('.lead__name').textContent = ', ' + S.name;
      return;
    }

    if (id === 'service') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">Что нужно сделать?</h3>${chips(SERVICES, S.services, true)}`;
      next.disabled = !S.services.length;
    } else if (id === 'goal') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">Какая главная цель?</h3>${chips(GOALS, [S.goal])}`;
      next.disabled = !S.goal;
    } else if (id === 'sphere') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">В какой вы сфере?</h3>${chips(SPHERES, [S.sphere])}
        <input class="lead__input" name="sphereOther" placeholder="Опишите сферу" maxlength="80" ${S.sphere === 'Другое' ? '' : 'hidden'}>`;
      body.querySelector('[name=sphereOther]').value = S.sphereOther;
      next.disabled = !S.sphere;
    } else if (id === 'detail') {
      const d = DETAILS[detailKey()];
      body.innerHTML = `<h3 class="lead__q" id="leadQ">${d.q}</h3>${chips(d.opts, S.detail, !d.single)}`;
      next.disabled = !S.detail.length;
    } else if (id === 'timing') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">Когда нужен результат?</h3>${chips(TIMING, [S.timing])}`;
      next.disabled = !S.timing;
    } else if (id === 'budget') {
      body.innerHTML = `<h3 class="lead__q" id="leadQ">На какой бюджет ориентируетесь?</h3>${chips(BUDGET, [S.budget])}
        <button type="button" class="lead__skip mono" data-act="skip">Пропустить</button>`;
      next.disabled = !S.budget;
    } else if (id === 'result') {
      if (!S.briefEdited) S.brief = makeBrief();
      const key = S.services.find(k => WORKS[k]);
      const works = key ? WORKS[key].map(src => `<img src="${BASE}${src}" alt="" loading="lazy">`).join('') : '';
      body.innerHTML = `<h3 class="lead__q" id="leadQ">Вот ваше ТЗ</h3>
        <textarea class="lead__brief" name="brief" rows="5" maxlength="1200" aria-label="Бриф"></textarea>
        <p class="lead__est mono">${estimate()}</p>
        ${works ? `<div class="lead__works">${works}</div><a class="lead__more mono" href="${BASE}services/${key}.html">Похожие работы →</a>` : ''}
        <div class="lead__form">
          <input class="lead__input" name="name" placeholder="Как к вам обращаться" maxlength="80" autocomplete="name">
          <div class="lead__chips lead__chips--sm">${['Telegram', 'WhatsApp', 'Звонок'].map(c => `<button type="button" class="lead__chip${S.channel === c ? ' is-on' : ''}" data-ch="${c}">${c}</button>`).join('')}</div>
          <input class="lead__input" name="contact" placeholder="${S.channel === 'Telegram' ? '@username или телефон' : 'Номер телефона'}" maxlength="120" autocomplete="tel">
          <input class="lead__hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p class="lead__err mono" hidden></p>
        </div>`;
      body.querySelector('[name=brief]').value = S.brief;
      body.querySelector('[name=name]').value = S.name;
      body.querySelector('[name=contact]').value = S.contact;
      next.textContent = ENDPOINT ? 'Получить расчёт' : 'Отправить в WhatsApp';
    }
  }

  // ---------- события ----------
  body.addEventListener('click', e => {
    const act = e.target.closest('[data-act]')?.dataset.act;
    if (act === 'start') { mode = 'quiz'; step = 0; render(); return; }
    if (act === 'later' || act === 'close') { close(); return; }
    if (act === 'skip') { S.budget = ''; go(1); return; }
    const ch = e.target.closest('[data-ch]');
    if (ch) { S.channel = ch.dataset.ch; saveInputs(); render(); return; }
    const chip = e.target.closest('.lead__chip[data-v]'); if (!chip) return;
    const v = chip.dataset.v, id = steps()[step];
    if (id === 'service') {
      if (v === 'unsure') S.services = S.services.includes('unsure') ? [] : ['unsure'];
      else { S.services = S.services.filter(x => x !== 'unsure'); S.services = S.services.includes(v) ? S.services.filter(x => x !== v) : [...S.services, v]; }
      S.detail = []; render(); return;
    }
    if (id === 'detail' && !DETAILS[detailKey()].single) { S.detail = S.detail.includes(v) ? S.detail.filter(x => x !== v) : [...S.detail, v]; render(); return; }
    // одиночный выбор — сразу дальше
    if (id === 'goal') S.goal = v;
    if (id === 'sphere') { S.sphere = v; if (v === 'Другое') { render(); body.querySelector('[name=sphereOther]').focus(); return; } }
    if (id === 'detail') S.detail = [v];
    if (id === 'timing') S.timing = v;
    if (id === 'budget') S.budget = v;
    render(); setTimeout(() => go(1), 220);
  });
  body.addEventListener('input', e => {
    if (e.target.name === 'sphereOther') S.sphereOther = e.target.value;
    if (e.target.name === 'brief') { S.brief = e.target.value; S.briefEdited = true; }
  });
  function saveInputs() {
    const f = n => body.querySelector(`[name=${n}]`);
    if (f('name')) S.name = f('name').value.trim();
    if (f('contact')) S.contact = f('contact').value.trim();
    if (f('website')) S.website = f('website').value;
    if (f('brief')) S.brief = f('brief').value.trim();
  }
  function go(d) { step = Math.max(0, Math.min(steps().length - 1, step + d)); render(); }
  back.addEventListener('click', () => go(-1));
  next.addEventListener('click', () => { steps()[step] === 'result' ? send() : go(1); });
  box.querySelector('.lead__x').addEventListener('click', close);
  addEventListener('keydown', e => { if (e.key === 'Escape' && isOpen) close(); });

  async function send() {
    saveInputs();
    const err = body.querySelector('.lead__err');
    if (S.contact.replace(/\D/g, '').length < 6 && !/^@?[a-z0-9_]{4,}$/i.test(S.contact)) {
      err.hidden = false; err.textContent = 'Оставьте @username или телефон, чтобы я мог ответить';
      body.querySelector('[name=contact]').focus(); return;
    }
    err.hidden = true; next.disabled = true; next.textContent = 'Отправляю…';
    const payload = { services: S.services.map(label), goal: S.goal, sphere: S.sphere === 'Другое' ? S.sphereOther || 'Другое' : S.sphere,
      detail: S.detail, timing: S.timing, budget: S.budget, brief: S.brief, name: S.name, channel: S.channel, contact: S.contact,
      website: S.website, page: location.href };
    try {
      if (!ENDPOINT) throw new Error('no endpoint');
      const r = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      ls.set('lead_sent', Date.now()); mode = 'done'; render();
    } catch {
      // запасной путь: готовый текст в WhatsApp
      const text = `Здравствуйте! Бриф с сайта:\n${S.brief}\n\n${S.name ? 'Имя: ' + S.name + '\n' : ''}Связь: ${S.channel} ${S.contact}`;
      const wa = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text)}`;
      if (!ENDPOINT) {
        // бот ещё не подключён — сразу открываем WhatsApp с готовым брифом
        ls.set('lead_sent', Date.now()); S.channel = 'WhatsApp'; mode = 'done'; render();
        window.open(wa, '_blank', 'noopener');
        return;
      }
      err.hidden = false;
      err.innerHTML = `Не получилось отправить автоматически. <a href="${wa}" target="_blank" rel="noopener">Отправить бриф в WhatsApp →</a>`;
      next.disabled = false; next.textContent = 'Попробовать ещё раз';
    }
  }

  // ---------- открыть / закрыть ----------
  function open(m) {
    mode = m; if (m === 'quiz' && step > steps().length - 1) step = 0;
    box.hidden = false; requestAnimationFrame(() => box.classList.add('is-open'));
    isOpen = true; pill.classList.add('is-hidden'); render();
  }
  function close() {
    box.classList.remove('is-open'); isOpen = false; pill.classList.remove('is-hidden');
    setTimeout(() => { if (!isOpen) box.hidden = true; }, 350);
    if (mode !== 'done') ls.set('lead_dismiss', Date.now());
  }
  document.addEventListener('click', e => {
    const t = e.target.closest('[data-lead]'); if (!t) return;
    e.preventDefault(); open(mode === 'done' ? 'done' : 'quiz');
  });
  pill.addEventListener('click', () => open(mode === 'done' ? 'done' : 'quiz'));
  setTimeout(() => { pill.hidden = false; requestAnimationFrame(() => pill.classList.add('is-in')); }, 4000);

  // ---------- когда показать сам ----------
  const t0 = Date.now();
  const canAuto = () => !ls.get('lead_sent') && Date.now() - (+ls.get('lead_dismiss') || 0) > 7 * 864e5 && !ss.get('lead_shown') && !isOpen;
  const auto = () => { if (canAuto()) { ss.set('lead_shown', 1); open('teaser'); } };
  const works = document.getElementById('works');
  if (works && !PAGE_SERVICE) {
    // главная: долистал до работ и провёл на сайте 25+ секунд
    new IntersectionObserver(([e], o) => {
      if (!e.isIntersecting) return; o.disconnect();
      setTimeout(auto, Math.max(1500, 25000 - (Date.now() - t0)));
    }, { threshold: .2 }).observe(works);
  } else {
    // страница услуги: прокрутил 40%
    const onS = () => {
      if (scrollY / (document.documentElement.scrollHeight - innerHeight || 1) < .4) return;
      removeEventListener('scroll', onS); setTimeout(auto, 1500);
    };
    addEventListener('scroll', onS, { passive: true });
  }
  // на компьютере — когда курсор уходит к вкладкам
  if (matchMedia('(pointer: fine)').matches) {
    document.addEventListener('mouseout', e => { if (!e.relatedTarget && e.clientY <= 0 && Date.now() - t0 > 8000) auto(); });
  }
})();
