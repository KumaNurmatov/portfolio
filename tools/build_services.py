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
         cases=[("Amanat Invest", "Брендбук: знак, палитра, типографика, носители, правила"),
                ("UMAI", "Логотип и презентация агротех-платформы"),
                ("Теплоход «Алыкул»", "Логотип, меню, грамоты и наградная продукция"),
                ("Almuratova · PR SMM", "Логотипы для бренда одежды и SMM-агентства"),
                ("Айыл Банк", "Подарочная упаковка к 30-летию банка"),
                ("Paradox", "Брендинг кинокомпании совместно с дизайнером из Канады")]),
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
         cases=[("ARCHA", "Моушн-посты и ролики для LED-экранов жилого комплекса"),
                ("Jetour · SOUEAST", "Моушн-креативы для таргета и LED в автосалоне"),
                ("MBANK", "Прероллы и LED-моушн для MIslamic и продуктов банка"),
                ("Теплоход «Алыкул»", "Анимированные афиши концертов и вечеринок"),
                ("Marjan de la Mode", "Тизер показа в двух форматах"),
                ("ADS Lab · Global Gifts", "Моушн для рекламы и ивентов")]),
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
         cases=[("ARCHA — «Две тропы»", "ИИ-фильм: барс и всадник, сценарий, 30+ сгенерированных кадров, монтаж"),
                ("ARCHA", "ИИ-посты «Баатыр» и «Олень» для Instagram"),
                ("MBANK", "ИИ-видео для ОСАГО"),
                ("Сезонные иллюстрации", "Серия «весна, лето, осень, зима» в акварельной стилистике")]),
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
         cases=[("MBANK", "50+ креативов: MIslamic, MPay, MBusiness, MTravel, ОСАГО, ипотека, автокредит, техработы"),
                ("Borsan Group", "50+ креативов для ЖК Borsan Residence, Brown, Green Line, Ivory, Loft, UNO, Рассвет"),
                ("Jetour · SOUEAST", "Акции и рассрочка: таргет, сторис, раздаточные материалы"),
                ("Pixel", "Креативы для магазина ноутбуков"),
                ("ADS Lab", "Статика, моушн, сайты в рекламном агентстве")]),
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
         cases=[("ARCHA", "Серия сторис, актуальные, посты для инвесторов"),
                ("Borsan Group", "Контент для ЖК: планировки, сервис, каталоги"),
                ("Kulikov", "Новогодняя серия сторис «Добрые истории»"),
                ("MBANK", "Сторис для продуктов, PR & Marketing"),
                ("Royal", "Креативы для соцсетей")]),
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
         cases=[("Теплоход «Алыкул»", "Меню ресторана и бара, баннеры, листовки доставки"),
                ("Jetour · SOUEAST", "Брендинг авто винилом, раздаточные материалы"),
                ("Pixel в ЦУМе", "Оформление магазина и навигация"),
                ("ARCHA", "Баннеры, роллапы, оформление отдела продаж"),
                ("Global Gifts · Misterphotobook", "Сувенирка, фотокниги, печать")]),
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
         cases=[("Freeways", "Фото и видео автомобилей для автосалона и сайта"),
                ("Florodora", "Предметная и бьюти-съёмка косметики"),
                ("Amanat City · Рабат · Fasadmaster", "Ролики с ведущими для застройщиков, монтаж"),
                ("Теплоход «Алыкул»", "Аэросъёмка с дрона"),
                ("Trio studio", "Фото, видео, монтаж клипов")]),
    dict(slug="web", n="08", tag="Web", title="Сайты и веб-сервисы", ph="ph--c",
         tagline="От лендинга до внутреннего сервиса.",
         lead="Делаю сайты, которые продают и работают: лендинги жилых комплексов, сайты с ИИ-консультантом, 3D и интерактивными картами, а также внутренние сервисы, которые заменяют хаос в WhatsApp и Excel.",
         items=[("Лендинги", "Сайты жилых комплексов, бизнес-центров и услуг под заявки."),
                ("ИИ-консультант", "Встроенный чат-ассистент, который понимает любой язык и помогает выбрать."),
                ("Интерактив и 3D", "Интерактивные карты окружения, 3D-модели и планировки прямо на сайте."),
                ("Tilda Zero Block", "Сложная вёрстка на Тильде, которую клиент может править сам."),
                ("Веб-сервисы", "Дашборды, учёт заказов, бухгалтерия — под процессы бизнеса."),
                ("Web3 и финтех", "Интерфейсы платформ с обменом фиата и криптовалюты.")],
         tools="Tilda · HTML/CSS/JS · ИИ-ассистенты · 3D/WebGL · дашборды",
         cases=[],
         sites=[
             dict(img="site-freeways", m="site-freeways-m", name="Freeways", url="https://freeways.kg", label="freeways.kg",
                  kind="Аренда авто в Бишкеке",
                  text="Прокат автомобилей от эконом до премиум. Встроенный ИИ-консультант понимает любой язык и помогает подобрать машину под поездку. Фото автомобилей для каталога тоже снимал я.",
                  tags=["Сайт", "ИИ-консультант", "Мультиязычность", "Каталог"]),
             dict(img="site-ivory", m="site-ivory-m", name="Ivory · Borsan Group", url="https://borsan.kg/ivory", label="borsan.kg/ivory",
                  kind="Лендинг ЖК премиум-класса",
                  text="Сайт жилого комплекса Ivory. По просьбе клиента добавлена интерактивная карта: объекты рядом и расположение можно «потыкать» прямо на странице.",
                  tags=["Лендинг", "Интерактивная карта", "Девелопер"]),
             dict(img="site-archa", m="site-archa-m", name="ARCHA", url="https://archaissykul.kg", label="archaissykul.kg",
                  kind="Апарт-отель на Иссык-Куле, с. Бостери",
                  text="Сайт апарт-отеля с презентацией, планировками и условиями покупки. Встроен 3D-объект: сайт готов показывать 3D-планировки и любые 3D-материалы проекта.",
                  tags=["Сайт", "3D", "Админка", "Девелопер"]),
             dict(img="site-buran", m=None, name="BURAN · PAX Group", url="https://pax-group.tilda.ws/", label="pax-group.tilda.ws",
                  kind="Бизнес-центр класса A+ в центре Бишкека",
                  text="Сайт бизнес-центра с инвестиционным предложением и 3D-планировками офисов. Проект на стадии финиша.",
                  tags=["Tilda", "Zero Block", "3D-планировки", "В работе"]),
             dict(img="site-magistral", m="site-magistral-m", name="Магистраль · PAX Group", url="https://pax-group.tilda.ws/magistral", label="pax-group.tilda.ws/magistral",
                  kind="Многопрофильный бизнес-центр",
                  text="Лендинг коммерческих помещений на первой линии для сферы услуг, кафе и ресторанов. Проект на стадии финиша.",
                  tags=["Tilda", "Лендинг", "Коммерция", "В работе"]),
             dict(img="site-agrofi", m="site-agrofi-m", name="AgroFi", url="https://agrofi.asia", label="agrofi.asia",
                  kind="Инвестиции в урожай на блокчейне",
                  text="Платформа, где инвесторы финансируют реальных фермеров, а блокчейн гарантирует прозрачность. Внутри — сервис обмена реальных денег на криптовалюту.",
                  tags=["Web3", "Финтех", "Обмен фиат ↔ крипто", "Калькулятор"]),
             dict(img="site-sewing", m=None, name="Учёт заказов", url=None, label="внутренний сервис",
                  kind="Швейное производство, работа с Россией",
                  text="Инструмент учёта заказов и бухгалтерии перевозок. Видно, на какой ступени каждый заказ: предоплата → пошив → отгрузка → приёмка → постоплата → сверка. Список дел, разбивка по месяцам, крупные долги и замечания по документам. Раньше всё велось в WhatsApp и Excel.",
                  tags=["Веб-сервис", "Дашборд", "Учёт", "Бухгалтерия"]),
         ]),
]

# Галереи: (файл, подпись, клиент). .mp4 — видео из media/video, остальное — media/img/*.jpg
GALLERY = {
    "identity": [("amanat-cover", "Брендбук", "Amanat Invest"), ("amanat-logo", "Знак", "Amanat Invest"), ("amanat-element", "Графический элемент", "Amanat Invest"),
                 ("amanat-carriers", "Носители", "Amanat Invest"), ("amanat-misuse", "Правила", "Amanat Invest"), ("umai-logo", "Знак", "UMAI"),
                 ("umai-deck", "Презентация", "UMAI"), ("alykul-logo", "Логотип", "Теплоход «Алыкул»"), ("almuratova-logo", "Логотип", "Almuratova"),
                 ("prsmm-logo", "Логотип", "PR SMM"), ("aiylbank-box", "Упаковка к 30-летию", "Айыл Банк")],
    "motion": [("archa-motion.mp4", "Моушн-пост", "ARCHA"), ("jetour-x50.mp4", "Таргет", "Jetour X50"), ("archa-led.mp4", "LED-экран", "ARCHA"),
               ("alykul-beishe.mp4", "Афиша", "Теплоход «Алыкул»"), ("soueast-motion.mp4", "Таргет", "SOUEAST"), ("mbank-islamic.mp4", "Преролл", "MBANK"),
               ("alykul-motion.mp4", "Афиша", "Теплоход «Алыкул»"), ("marjan.mp4", "Тизер показа", "Marjan de la Mode")],
    "ai": [("archa-film.mp4", "ИИ-фильм «Две тропы»", "ARCHA"), ("mbank-osago.mp4", "ИИ-видео", "MBANK"), ("ai-autumn", "Осень", "Сезонная серия"),
           ("ai-winter", "Зима", "Сезонная серия"), ("ai-spring", "Весна", "Сезонная серия"), ("ai-summer", "Лето", "Сезонная серия"),
           ],
    "ads": [("#", "MBANK", "50+ креативов: MTravel, MPay, MBusiness, MIslamic, кредиты, ипотека"),
            ("mbank-islamic", "MIslamic · Рамазан", "MBANK"), ("mbank-business", "Visa to account", "MBANK"), ("mbank-nfc", "NFC-стикер", "MBANK"),
            ("mbank-refund", "Возврат средств", "MBANK"), ("mbank-tint", "Тонировка", "MBANK"), ("mbank-mortgage", "Ипотека", "MBANK"),
            ("mbank-adal", "АДАЛ 0-0-4", "MBANK"), ("mbank-autocredit", "Автокредит", "MBANK"), ("mbank-bizpause", "Бизнес без паузы", "MBANK"),
            ("mbank-mtravel", "MTravel", "MBANK"),
            ("mb-01", "MTravel", "MBANK"),
            ("mb-02", "MTravel", "MBANK"),
            ("mb-03", "MTravel", "MBANK"),
            ("mb-04", "MPay · MBusiness", "MBANK"),
            ("mb-05", "MPay · MBusiness", "MBANK"),
            ("mb-06", "MPay · MBusiness", "MBANK"),
            ("mb-07", "MPay · MBusiness", "MBANK"),
            ("mb-08", "MPay · MBusiness", "MBANK"),
            ("mb-09", "ОСАГО", "MBANK"),
            ("mb-10", "ОСАГО", "MBANK"),
            ("mb-11", "Обновление", "MBANK"),
            ("mb-12", "Тонировка онлайн", "MBANK"),
            ("mb-13", "Тонировка онлайн", "MBANK"),
            ("mb-14", "Тонировка онлайн", "MBANK"),
            ("mb-15", "Возврат средств", "MBANK"),
            ("mb-16", "Возврат средств", "MBANK"),
            ("mb-17", "Переводы в Турцию", "MBANK"),
            ("mb-18", "Техработы", "MBANK"),
            ("mb-19", "MPay кешбэк", "MBANK"),
            ("mb-20", "MPay кешбэк", "MBANK"),
            ("mb-21", "MPay кешбэк", "MBANK"),
            ("mb-22", "MBusiness · Visa", "MBANK"),
            ("mb-23", "MBusiness · Visa", "MBANK"),
            ("mb-24", "Приглашение", "MBANK"),
            ("mb-25", "Приглашение", "MBANK"),
            ("mb-26", "Онлайн-кредит · ипотека", "MBANK"),
            ("mb-27", "Онлайн-кредит · ипотека", "MBANK"),
            ("mb-28", "Мурабаха", "MBANK"),
            ("mb-29", "MIslamic · Рамазан", "MBANK"),
            ("mb-30", "MIslamic · Рамазан", "MBANK"),
            ("mb-31", "MIslamic · карта", "MBANK"),
            ("mb-32", "MIslamic · карта", "MBANK"),
            ("mb-33", "MIslamic · кешбэк", "MBANK"),
            ("mb-34", "MIslamic · кешбэк", "MBANK"),
            ("mb-35", "Мурабаха", "MBANK"),
            ("mb-36", "Автокредит", "MBANK"),
            ("mb-37", "Автокредит", "MBANK"),
            ("mb-38", "Бизнес без паузы", "MBANK"),
            ("mb-39", "Бизнес без паузы", "MBANK"),
            ("mb-40", "Кредитный потенциал", "MBANK"),
            ("mb-41", "Онлайн-ипотека", "MBANK"),
            ("mb-42", "Онлайн-ипотека", "MBANK"),
            ("mb-43", "Онлайн-ипотека", "MBANK"),
            ("#", "Borsan Group", "Borsan Residence, Brown, Green Line, Ivory, Loft, UNO, Рассвет"),
            ("greenline-park", "Green Line", "Borsan Group"), ("brown-zero", "Brown", "Borsan Group"), ("borsan-residence", "Borsan Residence", "Borsan Group"),
            ("ivory-poster", "Ivory", "Borsan Group"), ("loft-poster", "Loft", "Borsan Group"), ("brown-30", "Brown", "Borsan Group"),
            ("uno-lake", "UNO", "Borsan Group"), ("borsan-gold", "Borsan Residence", "Borsan Group"), ("greenline-2k", "Green Line", "Borsan Group"),
            ("bs-01", "Borsan Residence", "Borsan Group"),
            ("bs-02", "Borsan Residence", "Borsan Group"),
            ("bs-03", "Borsan Residence", "Borsan Group"),
            ("bs-04", "Borsan Residence", "Borsan Group"),
            ("bs-05", "Borsan Residence", "Borsan Group"),
            ("bs-06", "Brown", "Borsan Group"),
            ("bs-07", "Brown", "Borsan Group"),
            ("bs-08", "Brown", "Borsan Group"),
            ("bs-09", "Brown", "Borsan Group"),
            ("bs-10", "Brown", "Borsan Group"),
            ("bs-11", "Brown", "Borsan Group"),
            ("bs-12", "Brown", "Borsan Group"),
            ("bs-13", "Brown", "Borsan Group"),
            ("bs-14", "Рассвет", "Borsan Group"),
            ("bs-15", "Green Line", "Borsan Group"),
            ("bs-16", "Green Line", "Borsan Group"),
            ("bs-17", "Green Line", "Borsan Group"),
            ("bs-18", "Green Line", "Borsan Group"),
            ("bs-19", "UNO", "Borsan Group"),
            ("bs-20", "UNO", "Borsan Group"),
            ("bs-21", "UNO", "Borsan Group"),
            ("bs-22", "UNO", "Borsan Group"),
            ("bs-23", "UNO", "Borsan Group"),
            ("bs-24", "UNO", "Borsan Group"),
            ("bs-25", "Borsan Residence", "Borsan Group"),
            ("bs-26", "Borsan Residence", "Borsan Group"),
            ("bs-27", "Borsan Residence", "Borsan Group"),
            ("bs-28", "Brown", "Borsan Group"),
            ("bs-29", "Green Line", "Borsan Group"),
            ("bs-30", "Green Line", "Borsan Group"),
            ("bs-31", "Green Line", "Borsan Group"),
            ("bs-32", "Ivory · Loft", "Borsan Group"),
            ("bs-33", "Ivory · Loft", "Borsan Group"),
            ("bs-34", "Ivory · Loft", "Borsan Group"),
            ("bs-35", "Ivory · Loft", "Borsan Group"),
            ("bs-36", "Ivory · Loft", "Borsan Group"),
            ("bs-37", "Ivory · Loft", "Borsan Group"),
            ("bs-38", "UNO", "Borsan Group"),
            ("bs-39", "UNO", "Borsan Group"),
            ("bs-40", "Borsan Group", "Borsan Group"),
            ("bs-41", "Borsan Group", "Borsan Group"),
            ("bs-42", "Borsan Group", "Borsan Group"),
            ("bs-43", "Borsan Group", "Borsan Group"),
            ("bs-44", "Borsan Group", "Borsan Group"),
            ("bs-45", "Borsan Group", "Borsan Group"),
            ("#", "Jetour · SOUEAST · Pixel", "Автодилер и магазин техники"),
            ("soueast-s09", "S09", "SOUEAST"), ("jetour-t2", "T2", "Jetour"), ("soueast-nobank", "Без банка", "SOUEAST"),
            ("soueast-s07", "S07", "SOUEAST"), ("soueast-s09-orange", "S09", "SOUEAST"), ("soueast-s07-orange", "S07", "SOUEAST"),
            ("pixel-laptops", "Ноутбуки", "Pixel")],
    "smm": [("archa-investor", "Пост", "ARCHA"), ("archa-story-1", "Сторис", "ARCHA"), ("archa-story-4", "Сторис", "ARCHA"),
            ("brown-plan", "Планировка", "Borsan · Brown"), ("ivory-service", "Сервис", "Borsan · Ivory"),
            ("ivory-terrace", "Каталог", "Borsan · Ivory"), ("kulikov-xmas", "Сторис", "Kulikov"), ("mbank-mtravel", "Сторис", "MBANK · MTravel"),
            ("brown-premium", "Пост", "Borsan · Brown"), ("uno-lake", "Пост", "Borsan · UNO"), ("borsan-gold", "Пост", "Borsan Residence"), ("mb-24", "Приглашение", "MBANK"), ("mb-18", "Техработы", "MBANK"), ("bs-44", "Пост", "Borsan Group"), ("mb-02", "MTravel", "MBANK")],
    "print": [("alykul-menu-company", "Меню", "Теплоход «Алыкул»"), ("alykul-menu-breakfast", "Меню", "Теплоход «Алыкул»"),
              ("alykul-menu-croissant", "Меню", "Теплоход «Алыкул»"), ("alykul-menu-mains", "Меню", "Теплоход «Алыкул»"), ("jetour-t2-flyer", "Раздатка", "Jetour T2"), ("archa-banner", "Баннер", "ARCHA"),
              ("pixel-store", "Оформление магазина", "Pixel · ЦУМ"), ("aiylbank-box", "Упаковка", "Айыл Банк"), ("uno-issykkul", "Наружка", "Borsan · UNO")],
    "photo-video": [("freeways-gls", "Фото для сайта", "Freeways"), ("florodora-2", "Предметка", "Florodora"), ("suyun-rabat.mp4", "Ролик с ведущим", "Рабат"),
                    ("freeways-x5-city", "Фото", "Freeways"), ("florodora-3", "Бьюти", "Florodora"), ("alykul-ship", "Аэросъёмка", "Теплоход «Алыкул»"),
                    ("freeways-interior", "Интерьер", "Freeways"), ("florodora-4", "Предметка", "Florodora"), ("amanat-city.mp4", "Ролик", "Amanat City"),
                    ("freeways-light", "Детали", "Freeways"), ("florodora-5", "Бьюти", "Florodora"), ("freeways-x6", "Фото", "Freeways"),
                    ("florodora-1", "Предметка", "Florodora"), ("freeways-x5", "Фото", "Freeways")],
}


def sites_block(sites):
    out = []
    for i, x in enumerate(sites):
        link = (f'<a class="site__link mono" href="{x["url"]}" target="_blank" rel="noopener">{x["label"]} ↗</a>' if x["url"]
                else f'<span class="site__link mono">{x["label"]}</span>')
        mob = f'<img class="site__phone" src="../media/img/{x["m"]}.jpg" alt="" loading="lazy">' if x["m"] else ""
        tags = "".join(f"<span>{t}</span>" for t in x["tags"])
        out.append(f'''      <article class="site rv">
        <div class="site__shot">
          <div class="site__browser"><i></i><i></i><i></i><span class="mono">{x["label"]}</span></div>
          <div class="site__scroll"><img src="../media/img/{x["img"]}-tall.jpg" onerror="this.src='../media/img/{x["img"]}.jpg'" alt="{x["name"]}" loading="lazy"></div>
          {mob}
        </div>
        <div class="site__info">
          <span class="mono site__n">{i + 1:02d} · {x["kind"]}</span>
          <h3>{x["name"]}</h3>
          <p>{x["text"]}</p>
          <div class="tools">{tags}</div>
          {link}
        </div>
      </article>''')
    return "\n".join(out)


def media(name, cls=""):
    if name.endswith(".mp4"):
        b = name[:-4]
        return f'<video class="autovid {cls}" src="../media/video/{name}" poster="../media/video/{b}.jpg" muted loop playsinline preload="none"></video>'
    try:
        from PIL import Image
        w, h = Image.open(ROOT / "media" / "img" / f"{name}.jpg").size
        wh = f' width="{w}" height="{h}"'
    except Exception:
        wh = ""
    return f'<img class="{cls}" src="../media/img/{name}.jpg"{wh} alt="" loading="lazy">'


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
    gal = GALLERY.get(s["slug"], [])
    gallery = "\n".join(
        (f'      <h3 class="g-group" id="{t.split()[0].lower()}"><span>{t}</span><small class="mono">{c}</small></h3>' if f == "#" else
         f'      <figure class="g rv">{media(f)}<figcaption><b>{c}</b><span>{t}</span></figcaption></figure>')
        for f, t, c in gal)
    works_inner = (f'    <div class="sites">\n{sites_block(s["sites"])}\n    </div>' if s.get("sites")
                   else f'    <div class="gallery">\n{gallery}\n    </div>')
    first = next((f for f, _, _ in gal if f != "#"), None)
    hero_media = media(first) if first else f'<div class="ph {s["ph"]}"></div>'
    cases = "\n".join(
        f'      <div class="exp__row rv"><span class="mono">клиент {i + 1:02d}</span><h4>{t}</h4><p>{d}</p>{DIAG}</div>'
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
    <div class="s-media rv">{hero_media}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow mono"><b>A</b>/ Работы</div>
    <div class="head">
      <h2 class="h2 rv">Избранные<br><em>работы.</em></h2>
      <p class="rv">{"Наведите на скриншот — страница прокрутится. Ссылки ведут на живые сайты." if s.get("sites") else "Нажмите на работу, чтобы открыть её крупно."}</p>
    </div>
{works_inner}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow mono"><b>B</b>/ Что входит</div>
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
    <div class="eyebrow mono"><b>C</b>/ Как работаю</div>
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
    <div class="eyebrow mono"><b>D</b>/ Клиенты и инструменты</div>
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
