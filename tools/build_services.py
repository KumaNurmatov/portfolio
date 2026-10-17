#!/usr/bin/env python3
"""Генератор страниц услуг: services/*.html.
Правишь тексты в SERVICES ниже → запускаешь `python3 tools/build_services.py` из папки сайта."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "services"

PHONE = "+996 709 906 852"
PHONE_HREF = "tel:+996709906852"
EMAIL = "k.nurmatov10.02@gmail.com"
BEHANCE = "https://www.behance.net/nkurmanbek"

SERVICES = [
    dict(slug="identity", n="01", tag="Брендинг", title="Айдентика", ph="ph--e",
         tagline="Узнаётся с первого кадра.",
         lead="Логотип — это только вход. Делаю систему: знак, цвета, шрифты, носители и правила, по которым бренд одинаково выглядит в соцсетях, на вывеске и на сувенирке.",
         items=[("Логотип", "Поиск идеи, эскизы, 2–3 концепции, доводка выбранной."),
                ("Фирменный стиль", "Палитра, типографика, графические элементы, паттерны."),
                ("Гайдбук", "Правила использования, чтобы стиль не разваливался у подрядчиков."),
                ("Носители", "Визитки, бланки, мерч, упаковка, вывески."),
                ("Ребрендинг", "Аккуратное обновление без потери узнаваемости."),
                ("Анимация знака", "Логотип в движении для роликов и соцсетей.")],
         tools="Illustrator · Photoshop · After Effects",
         cases=[("Брендинг кинокомпании", "Paradox · совместно с дизайнером из Канады"),
                ("Логотипы и брендинг", "Trio studio, Royal")]),
    dict(slug="motion", n="02", tag="Моушн", title="Моушн-графика", ph="ph--d",
         tagline="Статика, которая ожила.",
         lead="Анимирую то, что раньше просто висело: логотипы, инфографику, рекламу. Движение удерживает внимание и объясняет быстрее текста.",
         items=[("Анимация логотипа", "Интро и аутро для роликов, заставки."),
                ("Рекламные ролики", "Моушн-реклама для таргета и наружных экранов."),
                ("Explainer-видео", "Сложный продукт простым языком за 30–60 секунд."),
                ("Reels и сторис", "Анимированные шаблоны для регулярного контента."),
                ("LED и digital-экраны", "Ролики под нестандартные разрешения."),
                ("Титры и инфографика", "Цифры и факты, которые двигаются.")],
         tools="After Effects · Premiere Pro · Photoshop",
         cases=[("Моушн и рекламные материалы", "ADS Lab"),
                ("Моушн для ивентов", "Global Gifts")]),
    dict(slug="ai", n="03", tag="Generative AI", title="ИИ-видео и визуалы", ph="ph--a",
         tagline="Съёмка без съёмочной группы.",
         lead="Рекламные ролики, персонажи и предметка, сгенерированные нейросетями — но с режиссурой, раскадровкой и монтажом, а не «как получится». Быстрее и дешевле продакшна, когда нужно много вариантов.",
         items=[("ИИ-ролики", "Рекламные видео по сценарию и раскадровке."),
                ("ИИ-фотосессии", "Продукт или персонаж в любой локации."),
                ("Персонажи", "Единый герой бренда, узнаваемый от кадра к кадру."),
                ("Доработка рендеров", "Атмосфера, свет и люди поверх 3D или фото."),
                ("Ключевые визуалы", "Kv для кампаний и наружки."),
                ("Монтаж и звук", "Сборка генераций в цельный ролик.")],
         tools="Генеративные нейросети · Photoshop · After Effects · Premiere Pro",
         cases=[("ИИ-креативы для рекламы", "кейсы скоро появятся здесь")]),
    dict(slug="ads", n="04", tag="Performance", title="Креативы для таргета", ph="ph--c",
         tagline="Дизайн, который считают в CPL.",
         lead="Понимаю, как работает реклама изнутри, поэтому делаю креативы под гипотезы и метрики, а не просто «красивые баннеры». Пачки вариантов под A/B-тесты, адаптации под все форматы.",
         items=[("Статика", "Баннеры для Instagram, Facebook, TikTok, Google."),
                ("Видеокреативы", "Короткие ролики с хуком в первые 3 секунды."),
                ("A/B-пачки", "Варианты офферов, заголовков и визуалов для тестов."),
                ("Адаптации", "Один креатив — все размеры и площадки."),
                ("Лендинги", "Дизайн и вёрстка посадочных страниц."),
                ("Анализ", "Смотрю на результаты и предлагаю следующие гипотезы.")],
         tools="Photoshop · Illustrator · After Effects · Битрикс24",
         cases=[("Статика, моушн, сайты", "рекламное агентство ADS Lab"),
                ("Продвижение теплохода и яхты", "«Алыкул» и «Чынгыз», Чолпон-Ата")]),
    dict(slug="smm", n="05", tag="SMM", title="Контент для соцсетей", ph="ph--b",
         tagline="Лента, которая держит стиль.",
         lead="Визуальная концепция аккаунта и регулярный контент: посты, карусели, Reels, сторис. Шаблоны, с которыми команда сможет работать сама.",
         items=[("Визуальная концепция", "Стиль ленты под позиционирование бренда."),
                ("Посты и карусели", "Регулярный контент по контент-плану."),
                ("Reels", "Съёмка, монтаж, моушн-оформление."),
                ("Сторис", "Шаблоны, обложки актуальных, интерактив."),
                ("Шаблоны", "Редактируемые макеты для команды."),
                ("Фото", "Собственная съёмка для контента.")],
         tools="Photoshop · Illustrator · Premiere Pro · камера",
         cases=[("Креативы для соцсетей", "Royal"),
                ("Банк, департамент PR & Marketing", "mbank")]),
    dict(slug="print", n="06", tag="Print & Digital", title="Полиграфия и наружка", ph="ph--g",
         tagline="От макета до тиража.",
         lead="Готовлю макеты, которые не стыдно отдавать в типографию: с вылетами, правильным цветом и проверкой. Плюс наружная реклама, сувенирная продукция и её визуализация.",
         items=[("Офсетная печать", "Буклеты, листовки, каталоги, фотокниги."),
                ("Наружная реклама", "Билборды, баннеры, вывески, брендирование."),
                ("Сувенирная продукция", "Макеты и визуализация мерча для клиентов."),
                ("Вектор", "Отрисовка и подготовка векторных материалов."),
                ("Презентации", "КП и презентации, в которых читаются цифры."),
                ("Вёрстка сайтов", "Дизайн и вёрстка простых сайтов.")],
         tools="Illustrator · Photoshop",
         cases=[("Сувенирка и визуализация", "Global Gifts"),
                ("Дизайн фотокниг", "Misterphotobook"),
                ("Офсет и наружка", "Royal")]),
    dict(slug="photo-video", n="07", tag="Фото / видео", title="Съёмка и монтаж", ph="ph--f",
         tagline="Свой исходник — свой контроль.",
         lead="3 года в фотографии и опыт на съёмочной площадке. Снимаю и монтирую сам, поэтому креатив не зависит от стоковых картинок и чужих сроков.",
         items=[("Фотосъёмка", "Предметка, портреты, репортаж, контент для соцсетей."),
                ("Видеосъёмка", "Ролики для рекламы и Reels."),
                ("Монтаж", "Клипы, рекламные и имиджевые ролики."),
                ("Цветокоррекция", "Единый цвет для серии фото и видео."),
                ("Ассистирование", "Опыт работы на больших съёмках."),
                ("Ретушь", "Обработка фото под печать и digital.")],
         tools="Камера · Premiere Pro · Photoshop",
         cases=[("Фото, видео, монтаж клипов", "Trio studio"),
                ("Фото и видео для бренда", "Royal")]),
]

ARROW = '<svg viewBox="0 0 16 16" fill="none"><path d="M2 8h11M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5"/></svg>'
DIAG = '<svg viewBox="0 0 16 16" fill="none"><path d="M4 12 12 4M5 4h7v7" stroke="currentColor" stroke-width="1.5"/></svg>'

STEPS = [("Бриф", "Созваниваемся, разбираем задачу, аудиторию и цель. Фиксируем сроки и бюджет."),
         ("Идея", "Предлагаю концепцию или несколько направлений с референсами."),
         ("Производство", "Делаю, показываю промежуточные этапы, вношу правки."),
         ("Сдача", "Отдаю все исходники и адаптации под нужные площадки.")]


def page(s, nxt):
    items = "\n".join(
        f'      <div class="list__item rv"><span class="mono">{s["n"]}.{i + 1}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(s["items"]))
    steps = "\n".join(
        f'      <div class="step rv"><span class="step__n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(STEPS))
    cases = "\n".join(
        f'      <div class="exp__row rv"><span class="mono">кейс {i + 1:02d}</span><h4>{t}</h4><p>{d}</p>{DIAG}</div>'
        for i, (t, d) in enumerate(s["cases"]))
    tools = "".join(f"<span>{t.strip()}</span>" for t in s["tools"].split("·"))
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{s["title"]} — Курманбек Нурматов</title>
<meta name="description" content="{s["lead"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Inter:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="preload" href="../assets/fonts/RoadRadio-Black.ttf" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<!-- Страница сгенерирована tools/build_services.py — правь тексты там -->

<header class="nav">
  <a href="../index.html" class="nav__logo" aria-label="На главную">
    <svg viewBox="0 0 24 24" fill="none"><path d="M3 21 12 3l9 18h-5.2L12 12.6 8.2 21z" fill="currentColor"/></svg>
  </a>
  <nav class="nav__links mono">
    <a href="../index.html">Главная</a>
    <a href="../index.html#services" class="is-active">Услуги</a>
    <a href="../index.html#works">Работы</a>
    <a href="../index.html#experience">Опыт</a>
    <a href="#contact">Контакт</a>
  </nav>
  <div class="nav__spacer"></div>
  <span class="nav__item nav__status mono"><i class="dot"></i>Открыт к работе</span>
  <a href="{BEHANCE}" class="nav__item mono" target="_blank" rel="noopener">Behance</a>
  <a href="#contact" class="nav__cta mono">Обсудить проект</a>
  <button class="nav__burger" aria-label="Меню" aria-expanded="false"><span></span><span></span></button>
</header>
<div class="menu" id="menu">
  <a href="../index.html">Главная</a>
  <a href="../index.html#services">Услуги</a>
  <a href="../index.html#works">Работы</a>
  <a href="#contact">Контакт</a>
</div>

<div class="ruler" aria-hidden="true"><div class="ruler__scale" id="rulerScale"><div class="ruler__mark"></div></div></div>

<main id="top">
<section class="s-hero section">
  <div class="hero__glow" id="glow"></div>
  <div class="wrap" style="position:relative">
    <div class="crumbs mono rv"><a href="../index.html#services"><b>{s["n"]}</b> / Услуги</a><span>/</span><span>{s["tag"]}</span></div>
    <h1 class="s-title rv">{s["title"]}</h1>
    <p class="s-tagline rv">{s["tagline"]}</p>
    <div class="s-lead">
      <p class="rv">{s["lead"]}</p>
      <div class="hero__btns rv">
        <a href="#contact" class="btn btn--solid">Обсудить задачу {ARROW}</a>
        <a href="{BEHANCE}" class="btn" target="_blank" rel="noopener">Работы на Behance</a>
      </div>
    </div>
    <!-- Замени заглушку на <img src="../media/{s["slug"]}.jpg" alt=""> или <video src="../media/{s["slug"]}.mp4" autoplay muted loop playsinline></video> -->
    <div class="s-media rv"><div class="ph {s["ph"]}">{'<span class="shape"></span><span class="shape"></span>' if s["ph"] == "ph--e" else ""}</div></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow mono"><b>A</b>/ Что входит</div>
    <div class="head">
      <h2 class="h2 rv">Что я<br><em>делаю.</em></h2>
      <p class="rv">Можно взять услугу целиком или отдельные пункты — соберу под задачу и бюджет.</p>
    </div>
    <div class="list">
{items}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow mono"><b>B</b>/ Как работаю</div>
    <div class="head">
      <h2 class="h2 rv">Четыре шага<br><em>до результата.</em></h2>
      <p class="rv">Прозрачно на каждом этапе: вы видите промежуточные версии, а не только финал.</p>
    </div>
    <div class="steps">
{steps}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow mono"><b>C</b>/ Опыт и инструменты</div>
    <div class="exp">
{cases}
    </div>
    <div class="tools rv">{tools}</div>
  </div>
</section>

<a href="{nxt["slug"]}.html" class="wrap next">
  <div>
    <div class="next__label mono">Следующая услуга · {nxt["n"]}</div>
    <div class="next__title">{nxt["title"]}</div>
  </div>
  <span class="next__arrow">{ARROW}</span>
</a>

<section class="cta" id="contact">
  <div class="hero__glow"></div>
  <div class="wrap">
    <div class="mono rv" style="color:var(--fg-3);margin-bottom:28px;position:relative">Бишкек · офис или гибрид · командировки</div>
    <h2 class="cta__big rv">Нужна<br><em>{s["title"].lower()}?</em></h2>
    <p class="rv">Расскажите о задаче — предложу идею, сроки и стоимость.</p>
    <div class="hero__btns rv">
      <a href="{PHONE_HREF}" class="btn btn--solid">{PHONE} {ARROW}</a>
      <a href="mailto:{EMAIL}" class="btn">{EMAIL}</a>
    </div>
  </div>
</section>
</main>

<footer class="foot mono">
  <span>© 2026 Курманбек Нурматов</span>
  <nav>
    <a href="{BEHANCE}" target="_blank" rel="noopener">Behance</a>
    <a href="mailto:{EMAIL}">Email</a>
    <a href="{PHONE_HREF}">{PHONE}</a>
  </nav>
  <a href="#top">Наверх ↑</a>
</footer>

<script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
<script src="../assets/main.js"></script>
</body>
</html>
'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for i, s in enumerate(SERVICES):
        (OUT / f'{s["slug"]}.html').write_text(page(s, SERVICES[(i + 1) % len(SERVICES)]), encoding="utf-8")
        print("services/" + s["slug"] + ".html")
