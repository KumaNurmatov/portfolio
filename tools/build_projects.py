#!/usr/bin/env python3
"""Генератор страниц проектов: projects/*.html и превью для блока «С кем работал» на главной.
Тексты правятся в PROJECTS ниже → `python3 tools/build_projects.py` из папки сайта."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_services import ARROW, DIAG, BEHANCE, EMAIL, PHONE, PHONE_HREF, SERVICES, media  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "projects"
SVC = {s["slug"]: s["title"] for s in SERVICES}

# img: файл из media/img без .jpg; видео — с .mp4 (из media/video)
PROJECTS = [
    dict(slug="mbank", name="MBANK", tag="Банк · финтех", period="фев — апр 2026", role="Графический дизайнер, PR & Marketing", fmt="В штате",
         cover="mbank-cover",
         lead="Банк и мобильное приложение MBANK. В департаменте PR & Marketing отвечал за визуал продуктовых кампаний — от сторис и баннеров для сайта до прероллов и LED-экранов.",
         did=[("MIslamic", "Кампания «Берешен Рамазан» с кешбэком 10%, карта MIslamic, мурабаха — статика, адаптации и прероллы."),
              ("MPay и MBusiness", "NFC-стикер, оплата по QR, кешбэк MPay, онлайн-переводы по Visa для бизнеса."),
              ("Кредиты и ипотека", "Онлайн-кредит за 7 секунд, цифровая ипотека, автокредит, «Бизнес без паузы», кредитный потенциал."),
              ("MTravel", "Распродажи Jazeera Airways и новые направления: сторис и баннеры."),
              ("Сервисные сообщения", "Техработы, плановые обновления, приглашения — единый узнаваемый стиль."),
              ("Моушн и ИИ", "Прероллы, LED-ролики и ИИ-видео для ОСАГО.")],
         sets=[("Сторис", "9:16 · кампании для Instagram и приложения", "9/16", 5, [("mbf-s0", "Онлайн-кредит"), ("mbf-s1", "Цифровая ипотека"), ("mbf-s2", "MIslamic"), ("mbf-s5", "MIslamic"), ("mbf-s12", "MPay"), ("mbf-s15", "АДАЛ"), ("mbf-s16", "Автокредит"), ("mbf-s18", "Бизнес без паузы"), ("mbf-s19", "MTravel"), ("mbf-s22", "MTravel"), ("mbf-s25", "MTravel"), ("mbf-s26", "ОСАГО"), ("mbf-s27", "Тонировка онлайн"), ("mbf-s28", "MBusiness × Visa"), ("mbf-s29", "кредитный потенциал"), ("mbf-s30", "онлайн ипотека"), ("mbf-s31", "онлайн ипотека"), ("mbf-s32", "онлайн ипотека"), ("mbf-s33", "Приглашения"), ("mbf-s35", "Приглашения"), ("mbf-s38", "Возврат средств"), ("mbf-s39", "Возврат средств"), ("mbf-s42", "Техработы"), ("mbf-s43", "Техработы"), ("mbf-s44", "Техработы")]),
               ("Посты", "4:5 · лента и таргет", "4/5", 4, [("mbf-p2", "MIslamic"), ("mbf-p4", "MIslamic"), ("mbf-p5", "MPay"), ("mbf-p6", "MPay"), ("mbf-p7", "MPay"), ("mbf-p8", "MPay"), ("mbf-p9", "MPay"), ("mbf-p11", "АДАЛ"), ("mbf-p14", "Автокредит"), ("mbf-p15", "Бизнес без паузы"), ("mbf-p16", "MTravel"), ("mbf-p19", "MTravel"), ("mbf-p21", "Обновление приложения"), ("mbf-p26", "Тонировка онлайн"), ("mbf-p27", "Тонировка онлайн"), ("mbf-p29", "Тонировка онлайн"), ("mbf-p31", "MBusiness × Visa"), ("mbf-p33", "Возврат средств"), ("mbf-p34", "Возврат средств"), ("mbf-p35", "Возврат средств"), ("mbf-p36", "кредитный потенциал"), ("mbf-p37", "онлайн ипотека"), ("mbf-p40", "Переводы в Турцию"), ("mbank-osago.mp4", "ОСАГО · ИИ-видео")]),
               ("Баннеры и видео", "сайт, приложение, прероллы", "1.85/1", 2, [("mbank-islamic.mp4", "MIslamic · преролл", "span"), ("mbf-w8", "MBusiness × Visa"), ("mbf-w1", "MIslamic"), ("mbf-w2", "MIslamic"), ("mbf-w18", "Возврат средств")]),
               ("Веб-баннеры", "сайт и партнёрские площадки", "3.1/1", 2, [("mbf-b0", "MIslamic"), ("mbf-b8", "MIslamic"), ("mbf-b16", "Тонировка онлайн"), ("mbf-b12", "MPay")])],
         gallery=["mbank-islamic.mp4", "mb-26", "mb-30", "mbank-osago.mp4", "mb-04", "mb-12", "mb-31", "mb-36", "mb-22", "mb-38", "mb-01",
                  "mb-07", "mb-17", "mb-28", "mb-33", "mb-41", "mb-15", "mb-24", "mbank-nfc", "mbank-adal", "mb-19", "mb-09", "mb-43", "mb-34"],
         services=["ads", "motion", "ai", "smm"], previews=["mb-26", "mbank-islamic", "mb-12", "mb-31", "mb-36"]),
    dict(slug="borsan", name="Borsan Group", tag="Девелопер", period="2025 — 2026", role="Креативы, каталоги и сайт", fmt="Фриланс",
         lead="Застройщик жилых комплексов в Бишкеке и на Иссык-Куле. Веду визуал продаж сразу по нескольким ЖК: таргет, каталоги, наружка и сайт.",
         did=[("Таргет по 7 ЖК", "50+ креативов для Borsan Residence, Brown, Green Line, Ivory, Loft, UNO и «Рассвета»: офферы, рассрочка, планировки."),
              ("Каталог Ivory", "Кадры каталога: панорамная терраса, сервис, планировки по блокам."),
              ("Старт продаж", "Анонсы Ivory, Loft и Borsan Residence — постеры и сторис."),
              ("Сайт Ivory", "Лендинг ЖК с интерактивной картой объектов рядом."),
              ("Наружка и баннеры", "Баннеры для UNO на Иссык-Куле и офиса продаж.")],
         gallery=["greenline-park", "bs-07", "bs-01", "brown-zero", "ivory-terrace", "bs-19", "bs-33", "ivory-poster", "bs-15", "bs-25",
                  "loft-poster", "bs-22", "uno-lake", "bs-36", "ivory-service", "bs-40", "brown-plan", "bs-04", "bs-29", "borsan-gold", "site-ivory"],
         services=["ads", "smm", "print", "web"], url="https://borsan.kg/ivory", previews=["greenline-park", "bs-07", "ivory-poster", "bs-19", "bs-33"]),
    dict(slug="jetour", name="Jetour", tag="Автодилер", period="2025", role="Дизайн и моушн", fmt="Фриланс",
         lead="Дилер Jetour в Бишкеке. Запуск моделей T2 и X50, акции и рассрочка без участия банка.",
         did=[("Таргет-креативы", "Статика и сторис для T2 и X50: «Выгоднее, чем ты думал», рассрочка на 36 месяцев."),
              ("Моушн X50", "Вертикальный ролик для таргета и экранов в салоне."),
              ("Раздаточные материалы", "Листовки с характеристиками и условиями покупки."),
              ("Брендирование", "Винил на автомобили и календарь Орозо для клиентов.")],
         gallery=["jetour-x50.mp4", "jetour-t2", "jetour-t2-flyer"], services=["ads", "motion", "print"],
         previews=["jetour-t2", "jetour-x50", "jetour-t2-flyer"]),
    dict(slug="soueast", name="SOUEAST", tag="Автодилер", period="2025", role="Дизайн и моушн", fmt="Фриланс",
         lead="Дилер SOUEAST. Запуск моделей S07 и S09, акции «Лёгкий старт» и «Без участия банка».",
         did=[("Креативы S07 и S09", "Ключевые визуалы, цены, рассрочка, 5 лет гарантии."),
              ("Моушн", "Ролики для таргета и LED-экрана в салоне."),
              ("Брендирование винилом", "Раскладка оклейки S07 и S09 с двух сторон."),
              ("Раздатка", "Материалы для отдела продаж.")],
         gallery=["soueast-motion.mp4", "soueast-s09", "soueast-s07-orange", "soueast-nobank", "soueast-s07", "soueast-s09-orange"],
         services=["ads", "motion", "print"], previews=["soueast-s09-orange", "soueast-s09", "soueast-nobank", "soueast-s07"]),
    dict(slug="archa", name="ARCHA", tag="Апарт-отель · Иссык-Куль", period="2026", role="Визуал, ИИ, моушн и сайт", fmt="Фриланс",
         lead="Апарт-отель на берегу Иссык-Куля в с. Бостери. Веду проект комплексно: визуал продаж, ИИ-ролики, LED-экраны, Instagram и сайт.",
         did=[("ИИ-фильм «Две тропы»", "Барс и всадник: сценарий, 30+ сгенерированных кадров, монтаж и звук."),
              ("Моушн-посты", "«Баатыр» и «Олень» для Instagram, анимация логотипа."),
              ("LED-ролики", "Ролики под нестандартные разрешения уличных экранов."),
              ("Instagram", "Серия сторис о проекте, посты для инвесторов, актуальные."),
              ("Наружка", "Баннеры и роллапы для отдела продаж."),
              ("Сайт с 3D", "archaissykul.kg: презентация, планировки, 3D-объект на странице.")],
         gallery=["archa-film.mp4", "archa-motion.mp4", "archa-investor", "archa-led.mp4", "archa-story-1", "archa-story-4", "archa-banner", "site-archa"],
         services=["ai", "motion", "smm", "web", "print"], url="https://archaissykul.kg", previews=["archa-film", "archa-investor", "archa-motion", "archa-story-1"]),
    dict(slug="pax-group", name="PAX Group", tag="Девелопер · бизнес-центры", period="2026", role="Сайты", fmt="Фриланс",
         lead="Девелопер бизнес-центров BURAN и «Магистраль». Делаю сайты для продажи и аренды коммерческих помещений.",
         did=[("BURAN", "Бизнес-центр класса A+ в центре Бишкека: инвестиционное предложение и 3D-планировки офисов."),
              ("Магистраль", "Лендинг коммерческих помещений на первой линии для сферы услуг, кафе и ресторанов."),
              ("Tilda Zero Block", "Сложная вёрстка, которую команда клиента правит сама.")],
         gallery=["site-buran", "site-magistral"], services=["web"], url="https://pax-group.tilda.ws/", previews=["site-buran", "site-magistral"]),
    dict(slug="amanat-invest", name="Amanat Invest", tag="Инвестиции · недвижимость", period="2025", role="Айдентика", fmt="Фриланс",
         lead="Инвестиционная компания в сфере недвижимости. Разработал фирменный стиль и брендбук.",
         did=[("Знак", "Основная версия, варианты начертания, охранное поле."),
              ("Палитра и типографика", "Глубокий синий, золото и Inter — правила применения."),
              ("Графический элемент", "Паттерн из знака для носителей и соцсетей."),
              ("Носители", "Визитки, презентации, соцсети, недопустимое использование.")],
         gallery=["amanat-cover", "amanat-logo", "amanat-element", "amanat-carriers", "amanat-misuse"], services=["identity"],
         previews=["amanat-cover", "amanat-logo", "amanat-element", "amanat-carriers"]),
    dict(slug="umai", name="UMAI", tag="Агротех", period="2025", role="Логотип и презентация", fmt="Фриланс",
         lead="Платформа для инвестиций в сельское хозяйство. Логотип, фирменный стиль и презентация для инвесторов.",
         did=[("Логотип", "Знак-росток и шрифтовая часть."), ("Презентация", "Деки для инвесторов: миссия, модель, цифры.")],
         gallery=["umai-logo", "umai-deck"], services=["identity", "print"], previews=["umai-deck", "umai-logo"]),
    dict(slug="alykul", name="Теплоход «Алыкул»", tag="Туризм · HoReCa · Иссык-Куль", period="с 2023", role="Дизайнер и помощник маркетолога", fmt="Сезон + фриланс",
         lead="Прогулочный теплоход «Алыкул» и яхта «Чынгыз» в Чолпон-Ате. Продвижение, меню ресторана и бара, афиши вечеринок и наградная продукция.",
         did=[("Логотип", "Обновлённый знак теплохода."), ("Меню", "Завтраки, вторые блюда, блюда на компанию, бар, круассаны."),
              ("Афиши и моушн", "Анимированные афиши концертов и вечеринок на борту."), ("Наградная продукция", "Грамоты для команды по итогам сезона."),
              ("Доставка еды", "Листовки и вертикальные баннеры."), ("Аэросъёмка", "Кадры теплохода с дрона.")],
         gallery=["alykul-beishe.mp4", "alykul-menu-company", "alykul-ship", "alykul-menu-breakfast", "alykul-motion.mp4", "alykul-menu-mains",
                  "alykul-menu-croissant", "alykul-logo"],
         services=["print", "motion", "identity", "photo-video"], previews=["alykul-menu-company", "alykul-ship", "alykul-beishe", "alykul-menu-breakfast"]),
    dict(slug="pixel", name="Pixel", tag="Магазин ноутбуков", period="2025", role="Креативы и оформление точки", fmt="Фриланс",
         lead="Магазин ноутбуков и техники в ЦУМе Бишкека. Рекламные креативы и оформление магазина.",
         did=[("Креативы", "Ноутбуки в рассрочку: статика для соцсетей."), ("Оформление магазина", "Навигация и брендирование точки в ЦУМе.")],
         gallery=["pixel-laptops", "pixel-store"], services=["ads", "print"], previews=["pixel-laptops", "pixel-store"]),
    dict(slug="freeways", name="Freeways", tag="Аренда авто", period="2026", role="Фото, видео и сайт", fmt="Фриланс",
         lead="Прокат автомобилей в Бишкеке от эконом до премиум. Снимал автопарк для каталога и соцсетей, сделал сайт с ИИ-консультантом.",
         did=[("Фотосъёмка автопарка", "Студийные и уличные фото для сайта и каталога."), ("Видео", "Вертикальные ролики для соцсетей."),
              ("Сайт", "freeways.kg с ИИ-консультантом, который понимает любой язык и помогает выбрать машину.")],
         gallery=["freeways-gls", "freeways-x5-city", "freeways-interior", "freeways-light", "freeways-x6", "freeways-x5", "site-freeways"],
         services=["photo-video", "web"], url="https://freeways.kg", previews=["freeways-gls", "site-freeways", "freeways-interior", "freeways-x5-city"]),
    dict(slug="florodora", name="Florodora", tag="Косметика", period="2025", role="Съёмка и иллюстрации", fmt="Фриланс",
         lead="Бренд уходовой косметики. Предметная и бьюти-съёмка продукта и сезонная серия иллюстраций.",
         did=[("Предметная съёмка", "Флаконы и баночки в натуральных фактурах."), ("Бьюти-съёмка", "Портреты с продуктом для соцсетей."),
              ("Сезонная серия", "Иллюстрации «весна, лето, осень, зима» для оформления.")],
         gallery=["florodora-2", "florodora-3", "florodora-4", "florodora-5", "florodora-1", "ai-autumn", "ai-winter", "ai-spring", "ai-summer"],
         services=["photo-video", "ai"], previews=["florodora-2", "florodora-3", "florodora-4", "ai-autumn"]),
    dict(slug="kulikov", name="Kulikov", tag="Кондитерская", period="2024", role="SMM", fmt="Фриланс",
         lead="Новогодняя серия сторис «Добрые истории» для кондитерской сети.",
         did=[("Серия сторис", "Несколько вариантов оформления под праздничную кампанию."), ("Шаблоны", "Фоны и рамки, которые команда наполняет сама.")],
         gallery=["kulikov-xmas", "kulikov-1", "kulikov-2", "kulikov-3", "kulikov-4", "kulikov-5"], services=["smm"],
         previews=["kulikov-xmas", "kulikov-3", "kulikov-1", "kulikov-4"]),
    dict(slug="aiyl-bank", name="Айыл Банк", tag="Банк", period="2024", role="Упаковка", fmt="Фриланс",
         lead="Подарочная упаковка к 30-летию банка.",
         did=[("Коробка", "Конструкция, раскрой и визуализация."), ("Оформление", "Юбилейная графика и логотип 30 лет.")],
         gallery=["aiylbank-box", "aiylbank-box-2"], services=["print"], previews=["aiylbank-box", "aiylbank-box-2"]),
    dict(slug="amanat-city", name="Amanat City", tag="Жилой комплекс", period="2026", role="Моушн и монтаж", fmt="Фриланс",
         lead="Жилой комплекс Amanat City. Ролики для соцсетей: моушн по рендерам и видео с ведущими.",
         did=[("Моушн по рендерам", "Пролёты по проекту, благоустройство, фасады."), ("Видео с ведущими", "Сценарий, монтаж, титры.")],
         gallery=["amanat-city.mp4", "amanatcity-3", "amanatcity-2", "amanatcity-4", "amanatcity-5", "amanatcity-1"], services=["motion", "photo-video"],
         previews=["amanatcity-3", "amanat-city", "amanatcity-4", "amanatcity-2"]),
    dict(slug="fasadmaster", name="Fasadmaster", tag="Фасадные работы", period="2026", role="Видео", fmt="Фриланс",
         lead="Компания по фасадным работам. Имиджевый ролик с ведущим о проектах компании.",
         did=[("Ролик", "Сценарий, съёмка с ведущим, монтаж и титры."), ("Графика", "Логотипы партнёров и объектов в кадре.")],
         gallery=["fasadmaster.mp4", "fasadmaster-logo"], services=["photo-video", "motion"], previews=["fasadmaster", "fasadmaster-logo"]),
    dict(slug="royal", name="Royal", tag="Гостиница · девелопер", period="ноя 2022 — мар 2023", role="Графический дизайнер", fmt="В штате",
         lead="Гостиница и строительная компания Royal. Дизайн для офсетной печати, креативы для соцсетей и наружная реклама.",
         did=[("Полиграфия", "Макеты для офсетной печати."), ("Соцсети", "Креативы для продвижения."), ("Наружка", "Баннеры и вывески."),
              ("Логотипы", "Разработка логотипов и макетов, фото и видео совместно с командой.")],
         gallery=[], services=["print", "smm"], previews=[]),
    dict(slug="ads-lab", name="ADS Lab", tag="Рекламное агентство", period="май — окт 2024", role="Графический дизайнер", fmt="В штате",
         lead="Рекламное агентство в Бишкеке. Статика, моушн, рекламные материалы, дизайн и вёрстка сайтов для клиентов агентства.",
         did=[("Креативы", "Статика для таргета разных клиентов."), ("Моушн", "Рекламные ролики и анимация."), ("Сайты", "Дизайн и вёрстка.")],
         gallery=[], services=["ads", "motion", "web"], previews=[]),
    dict(slug="global-gifts", name="Global Gifts", tag="Сувенирная продукция", period="окт 2023 — апр 2024", role="Графический дизайнер", fmt="В штате",
         lead="ОсОО «Дженерал АйТи» (Global Gifts) — корпоративные подарки и сувенирка. Векторные материалы, макеты в печать, визуализация продукции, моушн и участие в бизнес-мероприятиях.",
         did=[("Визуализация", "Как будет выглядеть мерч с логотипом клиента."), ("Печать", "Подготовка макетов под разные технологии."),
              ("Ивенты", "Оформление и моушн для бизнес-мероприятий.")],
         gallery=[], services=["print", "motion"], previews=[]),
    dict(slug="agrofi", name="AgroFi", tag="Web3 · финтех", period="2026", role="Сайт и сервис обмена", fmt="Фриланс",
         lead="Платформа, где инвесторы финансируют реальных фермеров, а блокчейн гарантирует прозрачность. Внутри — сервис обмена реальных денег на криптовалюту.",
         did=[("Лендинг", "Как это работает, калькулятор доходности, преимущества."), ("Сервис обмена", "Интерфейс обмена фиата на криптовалюту."),
              ("Кабинет", "Сценарии для инвестора и фермера.")],
         gallery=["site-agrofi", "site-agrofi-m"], services=["web"], url="https://agrofi.asia", previews=["site-agrofi", "site-agrofi-m"]),
    dict(slug="paradox", name="Paradox", tag="Кинокомпания", period="2024", role="Брендинг", fmt="Совместно с дизайнером из Канады",
         lead="Брендинг кинокомпании Paradox в паре с дизайнером из Канады.",
         did=[("Айдентика", "Поиск знака и визуального языка."), ("Носители", "Применение стиля в материалах компании.")],
         gallery=[], services=["identity"], previews=[]),
]


def preview_src(p):
    """Путь к картинке превью от корня сайта (для видео — постер)."""
    return f"media/video/{p}.jpg" if (ROOT / "media" / "video" / f"{p}.mp4").exists() else f"media/img/{p}.jpg"


def page(p, nxt):
    facts = [("Период", p["period"]), ("Роль", p["role"]), ("Формат", p["fmt"])]
    if p.get("url"):
        facts.append(("Сайт", f'<a href="{p["url"]}" target="_blank" rel="noopener">{re.sub(r"^https?://", "", p["url"]).rstrip("/")} ↗</a>'))
    facts_html = "".join(f'<div class="fact"><span class="mono">{k}</span><b>{v}</b></div>' for k, v in facts)
    did = "\n".join(f'      <div class="list__item rv"><span class="mono">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p["did"]))
    gal = "\n".join(f'      <figure class="g rv">{media(f)}<figcaption><b>{p["name"]}</b><span></span></figcaption></figure>' for f in p["gallery"])
    svc = "".join(f'<a href="../services/{s}.html">{SVC[s]} ↗</a>' for s in p["services"])
    # cover — отдельная обложка целиком, без обрезки; иначе первая работа из галереи
    hero = media(p["cover"]) if p.get("cover") else (media(p["gallery"][0]) if p["gallery"] else "")
    hero_cls = "s-media s-media--cover" if p.get("cover") else "s-media"
    if p.get("sets"):
        parts = []
        for title, note, ar, cols, items in p["sets"]:
            figs = "\n".join(f'        <figure class="g g--fix{" g--span" if opt else ""} rv">{media(f)}<figcaption><b>{c}</b></figcaption></figure>'
                             for f, c, *opt in items)
            parts.append(f'''    <div class="set">
      <h3 class="g-group"><span>{title}</span><small class="mono">{note} · {len(items)}</small></h3>
      <div class="set-grid" style="--ar:{ar};--cols:{cols}">
{figs}
      </div>
    </div>''')
        sets_html = "\n".join(parts)
    works_block = f'''<section class="section" data-ruler="Работы">
  <div class="wrap">
    <div class="eyebrow mono"><b>B</b>/ Работы</div>
{sets_html}
  </div>
</section>''' if p.get("sets") else f'''<section class="section" data-ruler="Работы">
  <div class="wrap">
    <div class="eyebrow mono"><b>B</b>/ Работы</div>
    <div class="gallery">
{gal}
    </div>
  </div>
</section>''' if p["gallery"] else f'''<section class="section" data-ruler="Работы">
  <div class="wrap">
    <div class="eyebrow mono"><b>B</b>/ Работы</div>
    <div class="nda rv"><h3>Работы по запросу</h3><p>Материалы этого проекта показываю лично — напишите, пришлю подборку.</p>
      <a href="#contact" class="btn btn--solid" data-lead>Запросить работы {ARROW}</a></div>
  </div>
</section>'''
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["name"]} — проект Курманбека Нурматова</title>
<meta name="description" content="{p["lead"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body data-service="{p["services"][0]}">
<!-- Страница сгенерирована tools/build_projects.py — правь тексты там -->

<header class="nav">
  <a href="../index.html" class="nav__logo" aria-label="На главную">
    <svg viewBox="0 0 24 24" fill="none"><path d="M3 21 12 3l9 18h-5.2L12 12.6 8.2 21z" fill="currentColor"/></svg>
  </a>
  <nav class="nav__links mono">
    <a href="../index.html">Главная</a>
    <a href="../index.html#services">Услуги</a>
    <a href="../index.html#works">Работы</a>
    <a href="../index.html#experience" class="is-active">Клиенты</a>
    <a href="#contact">Контакт</a>
  </nav>
  <div class="nav__spacer"></div>
  <span class="nav__item nav__status mono"><i class="dot"></i>Открыт к работе</span>
  <a href="{BEHANCE}" class="nav__item mono" target="_blank" rel="noopener">Behance</a>
  <a href="#contact" class="nav__cta mono" data-lead>Обсудить проект</a>
  <button class="nav__burger" aria-label="Меню" aria-expanded="false"><span></span><span></span></button>
</header>
<div class="menu" id="menu">
  <a href="../index.html">Главная</a>
  <a href="../index.html#services">Услуги</a>
  <a href="../index.html#experience">Клиенты</a>
  <a href="#contact">Контакт</a>
</div>

<div class="ruler" id="ruler" role="scrollbar" aria-label="Положение на странице" aria-orientation="vertical" aria-valuemin="0" aria-valuemax="1337" aria-valuenow="0"><div class="ruler__bg"></div><div class="ruler__scale"><div class="ruler__band"></div><div class="ruler__ptr"></div></div></div>

<main id="top">
<section class="s-hero section">
  <div class="hero__glow" id="glow"></div>
  <div class="wrap" style="position:relative">
    <div class="crumbs mono rv"><a href="../index.html#experience"><b>Клиенты</b></a><span>/</span><span>{p["tag"]}</span></div>
    <h1 class="s-title rv">{p["name"]}</h1>
    <div class="s-lead">
      <p class="rv">{p["lead"]}</p>
      <div class="hero__btns rv">
        <a href="#contact" class="btn btn--solid" data-lead>Хочу так же {ARROW}</a>
      </div>
    </div>
    <div class="facts rv">{facts_html}</div>
    {f'<div class="{hero_cls} rv">{hero}</div>' if hero else ''}
  </div>
</section>

<section class="section" data-ruler="Что сделал">
  <div class="wrap">
    <div class="eyebrow mono"><b>A</b>/ Что сделал</div>
    <div class="list">
{did}
    </div>
    <div class="tools proj-svc rv">{svc}</div>
  </div>
</section>

{works_block}

<a href="{nxt["slug"]}.html" class="wrap next">
  <div>
    <div class="next__label mono">Следующий проект · {nxt["tag"]}</div>
    <div class="next__title">{nxt["name"]}</div>
  </div>
  <span class="next__arrow">{ARROW}</span>
</a>

<section class="cta" id="contact" data-ruler="Контакт">
  <div class="hero__glow"></div>
  <div class="wrap">
    <div class="mono rv" style="color:var(--fg-3);margin-bottom:28px;position:relative">Бишкек · офис или гибрид · командировки</div>
    <h2 class="cta__big rv">Нужен<br><em>похожий проект?</em></h2>
    <p class="rv">Расскажите о задаче — предложу идею, сроки и стоимость.</p>
    <div class="hero__btns rv">
      <a href="#contact" class="btn btn--solid" data-lead>Собрать бриф {ARROW}</a>
      <a href="{PHONE_HREF}" class="btn">{PHONE}</a>
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
<script src="../assets/lead.js"></script>
</body>
</html>
'''


def clients_html():
    """Сетка клиентов для главной: ссылки на проекты + превью для ховера."""
    out = []
    for p in PROJECTS:
        prev = ",".join(preview_src(x) for x in p["previews"])
        out.append(f'      <a class="client rv" href="projects/{p["slug"]}.html" data-previews="{prev}" data-note="{p["role"]} · {p["period"]}">'
                   f'<span>{p["name"]}</span><i class="client__tag mono">{p["tag"]}</i>'
                   f'<svg class="client__arr" viewBox="0 0 16 16" fill="none"><path d="M4 12 12 4M5 4h7v7" stroke="currentColor" stroke-width="1.5"/></svg></a>')
    out.append(f'      <a class="client client--cta rv" href="#contact" data-lead><span>Ваш бренд — следующий</span><i class="client__tag mono">Обсудить проект →</i></a>')
    return "\n".join(out)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for i, p in enumerate(PROJECTS):
        for f in p["gallery"] + p["previews"]:
            path = ROOT / (f"media/video/{f}" if f.endswith(".mp4") else preview_src(f))
            if not path.exists():
                print("НЕТ ФАЙЛА:", p["slug"], path.relative_to(ROOT))
        (OUT / f'{p["slug"]}.html').write_text(page(p, PROJECTS[(i + 1) % len(PROJECTS)]), encoding="utf-8")
    # вставляем сетку клиентов в главную
    idx = ROOT / "index.html"
    html = idx.read_text(encoding="utf-8")
    html, n = re.subn(r'(<div class="clients">\n).*?(\n    </div>)', lambda m: m.group(1) + clients_html() + m.group(2), html, count=1, flags=re.S)
    idx.write_text(html, encoding="utf-8")
    print(f"projects: {len(PROJECTS)}, главная обновлена: {bool(n)}")
