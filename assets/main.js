// Общий скрипт для главной и страниц услуг
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

// ---------- Плавный скролл (Lenis, как у ArtCraft) ----------
let lenis = null;
if (window.Lenis && !reduce) {
  lenis = window.lenis = new Lenis({ duration: 1.15, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)) });
  const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
  requestAnimationFrame(raf);
  document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href');
    const el = id === '#top' ? 0 : document.querySelector(id);
    if (el === null) return;
    e.preventDefault(); lenis.scrollTo(el, { offset: -56 });
  }));
}

// ---------- Логотип: буквы по одной + подгонка под ширину ----------
document.querySelectorAll('[data-split]').forEach(el => {
  const t = el.textContent.trim(); el.textContent = ''; el.setAttribute('aria-label', t);
  [...t].forEach((ch, i) => {
    const s = document.createElement('span'); s.textContent = ch;
    s.style.animationDelay = (.15 + i * .06) + 's'; s.setAttribute('aria-hidden', 'true'); el.appendChild(s);
  });
});
function fitWordmark() {
  document.querySelectorAll('.wordmark').forEach(el => {
    const max = el.parentElement.clientWidth * .92;
    el.style.fontSize = '100px';
    const w = [...el.children].reduce((a, s) => a + s.offsetWidth, 0) || 1;
    el.style.fontSize = Math.min(220, 100 * max / w) + 'px';
  });
}
fitWordmark();
document.fonts && document.fonts.ready.then(fitWordmark);
addEventListener('resize', fitWordmark);

// ---------- Бегущая строка ----------
const mq = document.getElementById('marquee');
if (mq) mq.innerHTML += mq.innerHTML;

// ---------- Появление: размытие + подъём, линии разделов, счётчики ----------
document.querySelectorAll('.eyebrow').forEach(e => e.classList.add('rv'));
document.querySelectorAll('.section').forEach(sec => {
  sec.insertAdjacentHTML('beforeend', '<i class="tick tick--l"></i><i class="tick tick--r"></i>');
});
const io = new IntersectionObserver(es => es.forEach(e => {
  if (!e.isIntersecting) return;
  e.target.classList.add(e.target.classList.contains('section') ? 'line-in' : 'in');
  e.target.querySelectorAll('[data-count]').forEach(n => {
    const end = +n.dataset.count, sup = n.querySelector('sup').outerHTML, t0 = performance.now();
    const step = t => {
      const p = Math.min((t - t0) / 1600, 1), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
      n.innerHTML = v + sup; if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
  io.unobserve(e.target);
}), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
// задержка «лесенкой» внутри одного родителя
document.querySelectorAll('.rv').forEach(el => {
  const sib = [...el.parentElement.children].filter(c => c.classList.contains('rv'));
  el.style.transitionDelay = Math.min(sib.indexOf(el), 6) * 90 + 'ms';
  io.observe(el);
});
document.querySelectorAll('.section').forEach(s => io.observe(s));

// ---------- Геометрия страницы: считаем один раз, а не на каждом кадре скролла ----------
const geo = { H: 1, vh: innerHeight, scaleH: 1, tops: new Map() };
const measured = new Set();
const track = el => el && measured.add(el);
function measure() {
  geo.H = document.documentElement.scrollHeight; geo.vh = innerHeight;
  measured.forEach(el => geo.tops.set(el, el.getBoundingClientRect().top + scrollY));
  const sc = document.querySelector('.ruler__scale'); if (sc) geo.scaleH = sc.clientHeight;
  onLayout.forEach(f => f());
}
const onLayout = [];
let measureTimer;
const remeasure = () => { clearTimeout(measureTimer); measureTimer = setTimeout(measure, 120); };
addEventListener('resize', remeasure); addEventListener('load', measure);
if (window.ResizeObserver) new ResizeObserver(remeasure).observe(document.body);

// ---------- Линейка-скроллбар 0–1337 мм (по мотивам ArtCraft) ----------
// Вся страница = 0…1337 мм. Рамка показывает видимую часть, голубая черта — где вы, разделы подписаны.
// Клик или перетаскивание по линейке прокручивает страницу.
const RULER_MM = 1337, ruler = document.getElementById('ruler');
let setRuler = () => {};
if (ruler) {
  const scale = ruler.querySelector('.ruler__scale');
  const band = ruler.querySelector('.ruler__band'), ptr = ruler.querySelector('.ruler__ptr');
  const f = document.createDocumentFragment();
  for (let mm = 0, i = 0; mm <= RULER_MM; mm += 10, i++) {
    const long = mm % 50 === 0, y = (mm / RULER_MM * 100) + '%';
    const t = document.createElement('i');
    t.className = 'ruler__t' + (long ? ' ruler__t--l' : ''); t.style.top = y; t.style.transitionDelay = (i * 6) + 'ms';
    f.appendChild(t);
    if (mm % 100 === 0) {
      const n = document.createElement('span'); n.className = 'ruler__n'; n.textContent = mm; n.style.top = y;
      n.style.transitionDelay = (i * 6 + 200) + 'ms'; f.appendChild(n);
    }
  }
  scale.prepend(f);
  // счётчик-одометр
  const digits = '0123456789'.split('').map(d => `<span>${d}</span>`).join('');
  ptr.innerHTML = `<span class="ruler__read"><span class="odo">${`<span class="odo__col">${digits}</span>`.repeat(4)}</span><em>мм</em></span>`;
  const cols = [...ptr.querySelectorAll('.odo__col')];
  // подписи разделов
  const secEls = [...document.querySelectorAll('[data-ruler]')];
  const secs = secEls.map(el => {
    const d = document.createElement('div'); d.className = 'ruler__sec';
    d.innerHTML = `<span>${el.dataset.ruler}</span><i></i>`;
    d.addEventListener('click', e => { e.stopPropagation(); lenis ? lenis.scrollTo(el, { offset: -56 }) : el.scrollIntoView({ behavior: 'smooth' }); });
    scale.appendChild(d); return { el, d };
  });
  secs.forEach(({ el }) => track(el));
  onLayout.push(() => {
    secs.forEach(({ el, d }) => d.style.top = geo.tops.get(el) / geo.H * 100 + '%');
    band.style.height = geo.vh / geo.H * 100 + '%';
  });
  setTimeout(() => ruler.classList.add('on'), 300);
  let lastV = '', lastCur = -2;

  // только transform — без пересчёта раскладки
  setRuler = top => {
    const { H, vh, scaleH } = geo;
    const bTop = top / H, bH = vh / H, p = Math.min(1, Math.max(0, top / (H - vh || 1)));
    band.style.transform = `translate3d(0,${bTop * scaleH}px,0)`;
    ptr.style.transform = `translate3d(0,${(bTop + bH * p) * scaleH}px,0)`;
    const v = String(Math.round(p * RULER_MM)).padStart(4, '0');
    if (v !== lastV) {
      for (let i = 0; i < 4; i++) if (v[i] !== lastV[i]) cols[i].style.transform = `translateY(${-11 * +v[i]}px)`;
      lastV = v; ruler.setAttribute('aria-valuenow', +v);
    }
    let cur = -1; secs.forEach(({ el }, i) => { if (geo.tops.get(el) - top < vh * .45) cur = i; });
    if (cur !== lastCur) { secs.forEach(({ d }, i) => d.classList.toggle('is-active', i === cur)); lastCur = cur; }
  };
  // клик и перетаскивание
  let drag = false;
  const seek = (e, immediate) => {
    const r = scale.getBoundingClientRect(), H = geo.H;
    const k = Math.min(1, Math.max(0, (e.clientY - r.top) / r.height));
    const target = Math.max(0, k * H - innerHeight / 2);
    lenis ? lenis.scrollTo(target, { immediate }) : scrollTo({ top: target, behavior: immediate ? 'auto' : 'smooth' });
  };
  ruler.addEventListener('pointerdown', e => { drag = true; ruler.setPointerCapture(e.pointerId); ruler.classList.add('is-drag'); seek(e, false); });
  ruler.addEventListener('pointermove', e => drag && seek(e, true));
  const stop = () => { drag = false; ruler.classList.remove('is-drag'); };
  ruler.addEventListener('pointerup', stop); ruler.addEventListener('pointercancel', stop);
}

// ---------- Активный пункт меню ----------
const links = [...document.querySelectorAll('.nav__links a')].filter(a => a.getAttribute('href').startsWith('#'));
const secs = links.map(a => document.querySelector(a.getAttribute('href')));
secs.forEach(track);
const pageLinks = [...document.querySelectorAll('.nav__links a.is-active:not([href^="#"])')];   // «Услуги»/«Клиенты» на подстраницах
let navCur = -2, ticking = false;
function onScroll() {
  ticking = false;
  const top = scrollY;
  setRuler(top);
  if (!links.length) return;
  // на подстраницах якорная ссылка в меню одна («Контакт») — подсвечиваем её, только когда дошли до раздела
  let cur = -1; secs.forEach((s, i) => { if (s && geo.tops.get(s) - top < geo.vh * .4) cur = i; });
  if (cur !== navCur) {
    links.forEach((a, i) => a.classList.toggle('is-active', i === cur));
    pageLinks.forEach(a => a.classList.toggle('is-active', cur === -1));
    navCur = cur;
  }
}
// не чаще одного раза за кадр
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
measure(); onScroll();

// ---------- Свечение за курсором ----------
const glow = document.getElementById('glow');
let mx = 0, my = 0;
addEventListener('pointermove', e => {
  mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5;
  if (glow && scrollY < innerHeight) glow.style.transform = `translate(calc(-50% + ${mx * 80}px),calc(-50% + ${my * 80}px))`;
});
document.querySelectorAll('.card').forEach(c => c.addEventListener('pointermove', e => {
  const r = c.getBoundingClientRect();
  c.style.setProperty('--mx', e.clientX - r.left + 'px'); c.style.setProperty('--my', e.clientY - r.top + 'px');
}));

// ---------- Туннель летящих кадров (фон hero) ----------
// Чтобы вместо градиентов летели работы: window.TUNNEL_IMAGES = ['media/1.jpg', ...] до подключения main.js
const cvs = document.getElementById('tunnel');
if (cvs && !cvs.dataset.gl) {
  const ctx = cvs.getContext('2d');
  const palette = [['#2d81ff', '#0b1a33'], ['#ff5a36', '#2a0f08'], ['#6b3cff', '#120a2a'], ['#00d1b2', '#04221d'], ['#f2f1ee', '#3a3b40'], ['#ffcf36', '#2b2106']];
  const tex = palette.map(([a, b], i) => {
    const c = document.createElement('canvas'); c.width = 320; c.height = 200; const g = c.getContext('2d');
    const lg = g.createLinearGradient(0, 0, 320, 200); lg.addColorStop(0, b); lg.addColorStop(1, '#0c0d0f');
    g.fillStyle = lg; g.fillRect(0, 0, 320, 200);
    const rg = g.createRadialGradient(80 + i * 30 % 160, 70 + i * 23 % 80, 0, 120, 100, 200);
    rg.addColorStop(0, a); rg.addColorStop(1, 'transparent'); g.globalAlpha = .75; g.fillStyle = rg; g.fillRect(0, 0, 320, 200);
    g.globalAlpha = .08; g.fillStyle = '#fff'; for (let y = 0; y < 200; y += 3) g.fillRect(0, y, 320, 1);
    return c;
  });
  // реальные работы: как только загрузились — летят они, а градиенты остаются запасом
  const photos = [];
  (window.TUNNEL_IMAGES || []).forEach(src => { const im = new Image(); im.onload = () => photos.push(im); im.src = src; });
  const pick = () => photos.length ? photos[Math.random() * photos.length | 0] : tex[Math.random() * tex.length | 0];

  let W, H, dpr;
  const resize = () => {
    dpr = Math.min(devicePixelRatio || 1, 2); W = cvs.clientWidth; H = cvs.clientHeight;
    cvs.width = W * dpr; cvs.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  resize(); addEventListener('resize', resize);

  const spawn = (c, z) => {
    let x, y;
    do { x = (Math.random() * 2 - 1) * 1.5; y = (Math.random() * 2 - 1) * 1.1; } while (Math.abs(x) < .5 && Math.abs(y) < .38);
    Object.assign(c, { x, y, z: z ?? 3 + Math.random() * .6, im: pick(), r: (Math.random() - .5) * .12 });
  };
  const cards = Array.from({ length: 22 }, (_, i) => { const c = {}; spawn(c, .4 + i / 22 * 3); return c; });
  const streaks = Array.from({ length: 90 }, () => ({ a: Math.random() * Math.PI * 2, d: .2 + Math.random(), z: Math.random() * 3 }));

  const rr = (x, y, w, h, r) => { ctx.beginPath(); ctx.roundRect ? ctx.roundRect(x, y, w, h, r) : ctx.rect(x, y, w, h); };
  let last = performance.now(), cx = 0, cy = 0, running = true;
  const frame = now => {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    cx += (mx * 60 - cx) * .05; cy += (my * 40 - cy) * .05;
    ctx.clearRect(0, 0, W, H);
    const ox = W / 2 - cx, oy = H / 2 - cy, F = Math.min(W, H) * .55;

    // шлейфы-искры
    ctx.lineWidth = 1;
    streaks.forEach(s => {
      s.z -= dt * .9; if (s.z < .15) { s.z = 3; s.a = Math.random() * Math.PI * 2; }
      const r1 = s.d * F / s.z, r2 = s.d * F / (s.z + .25);
      ctx.strokeStyle = `rgba(116,170,255,${Math.min(.35, (3 - s.z) * .12)})`;
      ctx.beginPath(); ctx.moveTo(ox + Math.cos(s.a) * r2, oy + Math.sin(s.a) * r2); ctx.lineTo(ox + Math.cos(s.a) * r1, oy + Math.sin(s.a) * r1); ctx.stroke();
    });

    // кадры — от дальних к ближним
    cards.sort((a, b) => b.z - a.z).forEach(c => {
      c.z -= dt * .32; if (c.z < .22) spawn(c);
      const k = F / c.z, w = .62 * k, h = w * .62;
      const x = ox + c.x * k - w / 2, y = oy + c.y * k - h / 2;
      const alpha = Math.min(1, (3.4 - c.z) / 1.4) * Math.min(1, (c.z - .22) / .3);
      if (alpha <= 0) return;
      ctx.save(); ctx.globalAlpha = alpha * .9;
      ctx.translate(x + w / 2, y + h / 2); ctx.rotate(c.r); ctx.translate(-w / 2, -h / 2);
      rr(0, 0, w, h, Math.max(4, w * .03)); ctx.clip();
      if (photos.length && tex.includes(c.im) && c.z > 2.6) c.im = pick();
      const im = c.im, iw = im.naturalWidth || im.width, ih = im.naturalHeight || im.height, sc = Math.max(w / iw, h / ih);
      ctx.drawImage(im, (w - iw * sc) / 2, (h - ih * sc) / 2, iw * sc, ih * sc);
      ctx.restore();
      ctx.save(); ctx.globalAlpha = alpha * .35; ctx.strokeStyle = '#f2f1ee';
      ctx.translate(x + w / 2, y + h / 2); ctx.rotate(c.r); rr(-w / 2, -h / 2, w, h, Math.max(4, w * .03)); ctx.stroke(); ctx.restore();
    });
    if (running && !reduce) requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
  new IntersectionObserver(([e]) => {
    const was = running; running = e.isIntersecting;
    if (running && !was && !reduce) { last = performance.now(); requestAnimationFrame(frame); }
  }).observe(cvs);
}

// ---------- Видео: играют, только когда видны ----------
const vio = new IntersectionObserver(es => es.forEach(e => {
  const v = e.target;
  if (e.isIntersecting) { v.preload = 'auto'; v.play().catch(() => {}); } else v.pause();
}), { threshold: .25 });
document.querySelectorAll('video.autovid').forEach(v => vio.observe(v));

// ---------- Лайтбокс для галерей ----------
const lb = document.createElement('div'); lb.className = 'lb';
lb.innerHTML = '<button class="lb__close" aria-label="Закрыть">ЗАКРЫТЬ ✕</button><div class="lb__body"></div>';
document.body.appendChild(lb);
const lbBody = lb.querySelector('.lb__body');
const closeLb = () => { lb.classList.remove('is-open'); lbBody.innerHTML = ''; lenis && lenis.start(); };
lb.addEventListener('click', e => { if (e.target === lb || e.target.closest('.lb__close')) closeLb(); });
addEventListener('keydown', e => { if (e.key === 'Escape') closeLb(); });
document.querySelectorAll('.g').forEach(g => g.addEventListener('click', () => {
  const v = g.querySelector('video'), i = g.querySelector('img');
  lbBody.innerHTML = v ? `<video src="${v.getAttribute('src')}" controls autoplay playsinline></video>` : `<img src="${i.getAttribute('src')}" alt="">`;
  lb.classList.add('is-open'); lenis && lenis.stop();
}));

// ---------- Скриншоты сайтов: высота окна для прокрутки при наведении ----------
const setSh = () => document.querySelectorAll('.site__scroll').forEach(b => b.style.setProperty('--sh', b.clientHeight + 'px'));
setSh(); addEventListener('resize', setSh);

// ---------- Клиенты: превью работ за курсором ----------
if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
  const cells = document.querySelectorAll('a.client[data-previews]');
  if (cells.length) {
    const box = document.createElement('div'); box.className = 'cprev'; box.setAttribute('aria-hidden', 'true');
    document.body.appendChild(box);
    let tx = 0, ty = 0, x = 0, y = 0, raf = 0, timer = 0, active = null;
    const loop = () => {
      x += (tx - x) * .18; y += (ty - y) * .18;
      box.style.transform = `translate3d(${x + 22}px,${y - 140}px,0) rotate(${Math.max(-6, Math.min(6, (tx - x) * .05))}deg)`;
      raf = active ? requestAnimationFrame(loop) : 0;
    };
    cells.forEach(cell => {
      cell.addEventListener('pointerenter', e => {
        active = cell; clearInterval(timer);
        const list = cell.dataset.previews.split(',').filter(Boolean);
        if (list.length) {
          box.innerHTML = list.map((src, i) => `<img src="${src}" alt=""${i ? '' : ' class="is-cur"'}>`).join('') +
            (list.length > 1 ? `<span class="cprev__count">1 / ${list.length}</span>` : '');
          let i = 0;
          if (list.length > 1) timer = setInterval(() => {
            const imgs = box.querySelectorAll('img'); imgs[i].classList.remove('is-cur');
            i = (i + 1) % imgs.length; imgs[i].classList.add('is-cur');
            box.querySelector('.cprev__count').textContent = `${i + 1} / ${imgs.length}`;
          }, 850);
        } else {
          box.innerHTML = `<div class="cprev__note"><small></small><span></span></div>`;
          box.querySelector('small').textContent = cell.dataset.note || '';
          box.querySelector('span').textContent = cell.querySelector('span').textContent;
        }
        if (!raf) { x = tx = e.clientX; y = ty = e.clientY; raf = requestAnimationFrame(loop); }
        box.classList.add('is-on'); box.style.scale = '1';
      });
      cell.addEventListener('pointermove', e => { tx = e.clientX; ty = e.clientY; });
      cell.addEventListener('pointerleave', () => {
        if (active === cell) { active = null; clearInterval(timer); box.classList.remove('is-on'); box.style.scale = '.85'; }
      });
    });
    addEventListener('scroll', () => { if (active) { active = null; clearInterval(timer); box.classList.remove('is-on'); } }, { passive: true });
  }
}

// ---------- Мобильное меню ----------
const burger = document.querySelector('.nav__burger'), menu = document.getElementById('menu');
if (burger && menu) {
  burger.addEventListener('click', () => { const o = menu.classList.toggle('is-open'); burger.setAttribute('aria-expanded', o); });
  menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.classList.remove('is-open'); burger.setAttribute('aria-expanded', false); }));
}

// ---------- Видео в работах: data-video="media/file.mp4" ----------
document.querySelectorAll('.work[data-video]').forEach(w => w.addEventListener('click', () => {
  const src = w.dataset.video; if (!src) return;
  w.querySelector('.media').innerHTML = `<video src="${src}" autoplay controls playsinline></video>`;
  w.querySelector('.work__play')?.remove();
}));
