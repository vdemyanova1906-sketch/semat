# app.py — internal prep tool for CeMAT booth duty
# run: streamlit run app.py

import random
import streamlit as st
import pandas as pd

# page config + theme
st.set_page_config(
    page_title="IT Vectura — подготовка к CeMAT",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

BRAND_NAVY = "#0B2A3D"
BRAND_BLUE = "#01426A"
BRAND_AMBER = "#E8952E"
BRAND_AMBER_LIGHT = "#FCEBD3"
INK = "#1B2530"
MUTED = "#5B6B78"
LINE = "#E1E6EA"

st.markdown(f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif; color: {BRAND_BLUE}; letter-spacing: -0.01em; }}

    .stApp {{ background-color: #F3F5F7; }}
    .block-container {{ padding-top: 2.2rem; max-width: 1080px; }}

    section[data-testid="stSidebar"] {{ background-color: {BRAND_NAVY}; }}
    section[data-testid="stSidebar"] * {{ color: #E7EEF3; }}
    section[data-testid="stSidebar"] .stMarkdown h2 {{
        font-family: 'Space Grotesk', sans-serif; color: #fff; letter-spacing: 0.02em;
        border-bottom: 1px solid rgba(255,255,255,0.14); padding-bottom: 14px;
    }}
    section[data-testid="stSidebar"] [role="radiogroup"] label {{
        border-radius: 8px; padding: 2px 6px; transition: background 0.12s ease;
    }}
    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {{
        background: rgba(255,255,255,0.06);
    }}

    /* content blocks */
    .pitch-box {{
        background: {BRAND_BLUE}; color: #fff; padding: 26px 30px;
        border-radius: 4px; border-left: 4px solid {BRAND_AMBER};
        font-size: 16.5px; line-height: 1.65;
    }}
    .tip-box {{
        background: {BRAND_AMBER_LIGHT}; border-left: 3px solid {BRAND_AMBER};
        padding: 14px 18px; font-size: 14px; color: #5A4319; margin-top: 14px;
    }}
    .fact-card {{
        background: #fff; border: 1px solid {LINE}; border-left: 3px solid {BRAND_BLUE};
        padding: 13px 18px; margin-bottom: 9px;
    }}
    .fact-card .k {{
        font-size: 11px; color: {MUTED}; font-weight: 600; letter-spacing: 0.06em;
    }}
    .fact-card .v {{ font-size: 15px; margin-top: 3px; color: {INK}; }}
    .case-card {{
        background: #fff; border: 1px solid {LINE}; padding: 18px 22px 20px; margin-bottom: 14px;
    }}
    .case-role {{
        font-size: 11px; color: {BRAND_AMBER}; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.08em;
    }}

    /* buttons: flatten the default Streamlit look */
    .stButton button {{
        border-radius: 4px; border: 1px solid {LINE}; font-weight: 500;
    }}
    .stButton button:hover {{ border-color: {BRAND_BLUE}; color: {BRAND_BLUE}; }}

    div[data-testid="stExpander"] {{ border: 1px solid {LINE}; border-radius: 4px; }}

    /* hide default Streamlit chrome — looks like a real product, not a template */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ display: none; }}
    .stAppDeployButton {{ display: none; }}

    /* mobile */
    @media (max-width: 640px) {{
        .block-container {{ padding-left: 1rem; padding-right: 1rem; padding-top: 1.4rem; }}
        .pitch-box {{ padding: 18px 20px; font-size: 15px; }}
        .case-card {{ padding: 14px 16px; }}
        h1 {{ font-size: 1.5rem !important; }}
    }}
</style>
""", unsafe_allow_html=True)


# --- data ---
PRODUCTS = [
    {"name": "TMS — управление транспортом", "tag": "Флагман, готов к продаже",
     "desc": "Заказ → планирование → исполнение → расчёты. Любые виды перевозок.",
     "features": [
         "Собственный оптимизатор маршрутов и тарифный калькулятор",
         "Автораспределение заказов между перевозчиками, торги",
         "Личный кабинет перевозчика, ЭДО из коробки (ЭТрН, ЭПЭ, ЭЭР)",
         "Автоинвойсинг и сверка счетов",
         "Планировщик парка: график ТС/водителей, режим РТиО",
     ]},
    {"name": "WMS — управление складом", "tag": "В активной разработке",
     "desc": "Приёмка → размещение → отгрузка на low-code платформе.",
     "features": [
         "Подъём любых терминалов: бортовые, сухие, любой объём",
         "Интеграция с регистрационным и весовым оборудованием",
         "Low-code настройка новых процессов и форм",
     ]},
    {"name": "YL — управление двором", "tag": "Часть единой платформы",
     "desc": "Автоматизация въезда/выезда и слотирования территории склада.",
     "features": [
         "Ручное и автоматическое бронирование окон (слотов)",
         "Горизонтальное/вертикальное/смешанное планирование на воротах",
         "Саморегистрация водителей, мобильная версия PWA",
         "Интеграция с терминалами, весами, шлагбаумами, светофорами",
         "Cloud или On-premise — функционал одинаковый",
     ]},
    {"name": "TOS — управление терминалом", "tag": "Единый контур",
     "desc": "Склад + двор + транспортные потоки терминала в одном окне.",
     "features": [
         "Целостная картина работы терминала",
         "Строится на тех же модулях TMS/WMS/YL",
         "Актуально для портов, крупных хабов",
     ]},
    {"name": "Routing — маршрутизация", "tag": "ИИ-планирование",
     "desc": "Внешний маршрутизатор с учётом всех ограничений.",
     "features": [
         "Геокодирование адресов",
         "Учёт временных окон, вместимости и совместимости ТС",
         "Собственный солвер и матрица расстояний OSM",
         "Сокращение пробега, гарантия сроков",
     ]},
    {"name": "FrameWork — конструктор", "tag": "Уникальное преимущество",
     "desc": "Платформа, на которой построены все продукты линейки.",
     "features": [
         "Low-code: настройка без разработчиков",
         "Глубина параметризации под клиента",
         "API-first: интеграция за дни, не месяцы",
     ]},
    {"name": "Tasks — управление проектами", "tag": "Новый продукт",
     "desc": "Контроль сроков, бюджета и загрузки команды.",
     "features": [
         "Единая система для управления проектом внедрения",
         "Контроль ресурсов в реальном времени",
     ]},
]

COMPANY_FACTS = [
    ("Название", "ООО «ИТ Вектура», ИНН 9701217858"),
    ("Опыт", "Команда — 15+ лет опыта в отрасли"),
    ("R&D", "25+ разработчиков в собственной лаборатории"),
    ("Объём", "15 000+ заказов ежедневно обрабатывает система у клиентов"),
    ("Проекты", "15+ успешных проектов в ритейле и дистрибуции"),
    ("Локация / статус", "Резидент Сколково, Большой бульвар, 42, стр. 1, Москва"),
    ("Реестр ПО", "Все продукты — в Едином реестре российского ПО и Роспатенте"),
    ("Совместимость", "RedSoft, Astra Linux, 1С, «Альт», PostgreSQL"),
]

TECH_STACK = [
    ("БД", "PostgreSQL"),
    ("API и backend-логика", "WebSockets / GraphQL / REST API — Golang"),
    ("AI и моделирование", "Python, LLM / PyTorch, OR-Tools"),
    ("Оркестратор задач", "Redis / Kafka / RabbitMQ — события, подписки"),
    ("Web-фронтенд", "React, TypeScript"),
    ("Мобильные приложения", "PWA, Flutter (Android, iOS)"),
    ("DevOps", "GitLab, Docker / Docker Compose, k8s"),
]

TECH_SECURITY = [
    "Web и API — по HTTPS",
    "Аутентификация: JWT, с возможностью интеграции в Active Directory",
    "Авторизация с правами на уровне экранов и полей UI, типов объектов, "
    "экземпляров объектов и полей объектов",
]

CASES = [
    ("Кейс 1", "Крупный российский fashion-холдинг (среди клиентов — «Детский мир»)",
     "Задача: заявки, распределение рейсов по ТК, обмен данными, полный цикл электронных "
     "экспедиторских документов.\n\n"
     "Сложность: высокая частота доставок, коробочный учёт, LTL, 100% привлечённый транспорт.\n\n"
     "Залог успеха: гибкие настройки под разные схемы доставки, собственный маршрутизатор, "
     "учёт по грузовым местам."),
    ("Кейс 2", "Ведущая российская продуктовая розничная компания",
     "Задача: снизить затраты цепочки поставок, импортозаместить прежнее ПО.\n\n"
     "Настроено: ручное и авто-планирование, кустовое планирование с карты, попутная логистика, "
     "схемы РЦ-РЦ, ТТ-ТТ.\n\n"
     "Результат: экономия на маршрутизации, управление несколькими РЦ с одного рабочего места."),
    ("Референс", "X5 и другие",
     "X5 — реализованный референсный проект. В процессе: алкогольный производитель, "
     "Melon Fashion Group, DIY-ритейл, химический холдинг, Hoff. Есть и «быстрая сделка» — "
     "экспедитор, который сам пришёл с сайта."),
]

OBJECTIONS = [
    ("«Молодой продукт, страшно внедрять»",
     "Команда — 15+ лет опыта в отрасли, продукт строится на опыте SAP/Oracle. Уже 15 000+ заказов "
     "в день у действующих клиентов. Есть эталонное внедрение с полным enterprise-циклом."),
    ("«Дорого»",
     "Не называть цены на стенде. «Стоимость считается индивидуально под объём и модули — "
     "оставьте контакт, посчитаем предложение» + взять контакт."),
    ("«Требования по информационной безопасности»",
     "Реестр отечественного ПО, резидент Сколково, совместимость с Astra Linux, RedSoft, «Альт». "
     "RLS, JWT + интеграция с Active Directory."),
    ("«У нас уже SAP/Oracle»",
     "Прямой функциональный аналог SAP TM/Oracle TM на независимом стеке — актуально именно для "
     "замены после ухода западных вендоров. Интеграция по API — дни, не месяцы."),
    ("«У нас очень специфичные процессы»",
     "Именно для этого FrameWork — low-code конструктор в основе всех продуктов. Специфика "
     "параметризуется без кастомной разработки."),
    ("«Сколько занимает внедрение»",
     "Анализ и проектирование — 2 мес., реализация — 3 мес., подготовка к ОПЭ — 1 мес., "
     "промышленная эксплуатация — 2 мес. Итого ориентир ~8 месяцев на полный цикл."),
    ("«А что с WMS — можно уже покупать?»",
     "Честно: WMS в активной разработке. Не выдавать за полностью готовый продукт, как TMS."),
    ("«Чем вы лучше Solvo / LogistiX / других на этой выставке»",
     "Не сравнивать резко негативно. «Мы решаем эту задачу вот так — а дальше вам сравнивать». "
     "Упор на low-code, единый контур TMS+WMS+YL+TOS на одной архитектуре, реестр ПО."),
]

GLOSSARY = [
    ("TMS/WMS/YL/TOS", "Transportation/Warehouse Management, Yard Logistic, Terminal Operating System — модули платформы"),
    ("VRP", "Vehicle Routing Problem — задача маршрутизации с ограничениями"),
    ("JSSP", "Job Shop Scheduling Problem — расстановка событий и пересчёт таймингов на рейсах"),
    ("OSM", "OpenStreetMap — картографическая база для матрицы расстояний"),
    ("РЦ / ТТ", "Распределительный центр / Торговая точка"),
    ("ЭТрН / ЭПЭ / ЭЭР", "Электронные транспортные/экспедиторские документы в ЭДО"),
    ("RLS", "Role Level Security — права на уровне полей и объектов"),
    ("ОПЭ", "Опытно-промышленная эксплуатация — этап перед полным запуском"),
    ("NFR", "Нефункциональные требования — нагрузка, отказоустойчивость, безопасность"),
    ("CAPEX / OPEX", "Капитальные / операционные затраты"),
]

FLASHCARDS = [
    ("Сколько лет опыта у команды IT Vectura?", "15+ лет опыта команды в отрасли."),
    ("Сколько заказов в день обрабатывает система?", "15 000+ заказов ежедневно у действующих клиентов."),
    ("В каком реестре зарегистрированы продукты?", "В Едином реестре российского ПО (Минцифры РФ) и в Роспатенте."),
    ("Какой продукт самый готовый к продаже прямо сейчас?", "TMS — управление транспортом."),
    ("Какой продукт ещё в активной разработке?", "WMS — управление складом."),
    ("Что такое FrameWork и почему это главное преимущество?",
     "Low-code конструктор в основе всех продуктов: клиент сам настраивает поля, статусы, "
     "формы без программиста — быстрее и дешевле доработки кодом у конкурентов."),
    ("Что уникально в TMS по сравнению с рынком РФ?",
     "Динамическое транспортное планирование — пересчёт плана на лету при изменениях."),
    ("Кто главный конкурент компании в целом?", "Axelot."),
    ("Каких конкурентов ожидать именно на CeMAT?",
     "Solvo, SEVCO, ANT Technologies, LogistiX, InStock Technologies, EME WMS."),
    ("Сколько занимает полный цикл внедрения?",
     "Ориентир ~8 месяцев: анализ 2 мес + реализация 3 мес + подготовка к ОПЭ 1 мес + "
     "промышленная эксплуатация 2 мес."),
    ("На чём написана backend-логика платформы?", "Golang, API через WebSockets/GraphQL/REST API."),
    ("Какая СУБД используется?", "PostgreSQL."),
    ("На чём сделан веб-фронтенд?", "React с TypeScript."),
    ("Как устроены мобильные приложения?", "PWA и Flutter — под Android и iOS."),
    ("Что используется для оркестрации задач и событий между сервисами?",
     "Redis, Kafka, RabbitMQ — события и подписки."),
    ("Какой стек используется в AI-модуле?", "Python, PyTorch/LLM, OR-Tools."),
    ("Как аутентифицируются пользователи в системе?",
     "JWT, с возможностью интеграции в Active Directory."),
]

QUIZ_QUESTIONS = [
    {"q": "Сколько лет опыта у команды IT Vectura в отрасли?",
     "opts": ["15+ лет", "20+ лет", "10+ лет", "5+ лет"], "correct": 0,
     "exp": "Команда — 15+ лет опыта в отрасли."},
    {"q": "Какой продукт сейчас в активной разработке и НЕ готов как завершённый?",
     "opts": ["TMS", "Routing", "WMS", "FrameWork"], "correct": 2,
     "exp": "WMS в активной разработке — не выдавать за полностью готовый продукт."},
    {"q": "В каком реестре зарегистрированы все продукты IT Vectura?",
     "opts": ["Реестр ФСТЕК", "Единый реестр российского ПО (Минцифры РФ)", "Реестр Сколково", "Международный реестр SaaS"],
     "correct": 1, "exp": "Единый реестр Минцифры РФ + Роспатент. Сертификации ФСТЕК отдельно нет."},
    {"q": "Гость спрашивает точную цену внедрения. Что вы делаете?",
     "opts": ["Называю вилку цен", "Прошу оставить контакт для индивидуального расчёта",
              "Говорю, что не знаю", "Называю цену конкурента"], "correct": 1,
     "exp": "Цены на стенде не называются — задача взять контакт."},
    {"q": "Что именно делает YL (Yard Logistic)?",
     "opts": ["Считает зарплату водителям", "Управляет двором: окна, ворота, регистрация водителей",
              "Формирует ЭТрН", "Оптимизирует маршруты"], "correct": 1,
     "exp": "YL — про территорию склада, не про сам склад (WMS) и не про маршрут (Routing)."},
    {"q": "Что такое «динамическое транспортное планирование»?",
     "opts": ["Смена цвета интерфейса", "Пересчёт плана на лету при изменениях",
              "Автогенерация счетов", "Голосовое управление"], "correct": 1,
     "exp": "Редкая на рынке РФ функция — система пересчитывает последствия каскадно."},
    {"q": "Кто главный конкурент IT Vectura в целом?",
     "opts": ["Solvo", "Axelot", "1С", "SAP"], "correct": 1,
     "exp": "Axelot — главный конкурент в целом. На CeMAT в зале будут скорее Solvo, LogistiX и другие складские игроки."},
    {"q": "Сколько занимает полный цикл внедрения по дорожной карте?",
     "opts": ["~2 месяца", "~1 месяц", "~8 месяцев", "~2 года"], "correct": 2,
     "exp": "2 + 3 + 1 + 2 месяца по четырём этапам = ~8 месяцев."},
    {"q": "На каком языке написана backend-логика платформы?",
     "opts": ["Java", "Golang", "PHP", "C#"], "correct": 1,
     "exp": "Backend и API (WebSockets/GraphQL/REST) — на Golang."},
    {"q": "Какая СУБД используется в платформе?",
     "opts": ["MySQL", "MongoDB", "PostgreSQL", "Oracle DB"], "correct": 2,
     "exp": "База данных — PostgreSQL."},
    {"q": "Как аутентифицируются пользователи, и что поддерживается для корпоративной интеграции?",
     "opts": ["OAuth без интеграций", "JWT с возможностью интеграции в Active Directory",
              "Только логин/пароль без токенов", "Kerberos"], "correct": 1,
     "exp": "JWT-аутентификация с возможностью интеграции в Active Directory."},
    {"q": "Что используется для оркестрации задач и событий между сервисами?",
     "opts": ["Redis/Kafka/RabbitMQ", "Celery", "Только прямые REST-запросы", "Cron-задачи"],
     "correct": 0, "exp": "События и подписки идут через Redis/Kafka/RabbitMQ."},
]


# --- session state ---
if "fc_index" not in st.session_state:
    st.session_state.fc_index = 0
if "fc_flipped" not in st.session_state:
    st.session_state.fc_flipped = False
if "fc_order" not in st.session_state:
    st.session_state.fc_order = list(range(len(FLASHCARDS)))
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}


# --- sidebar nav ---
st.sidebar.markdown("## IT VECTURA")

page = st.sidebar.radio(
    label="Разделы",
    options=[
        "01 · Питч",
        "02 · О компании",
        "03 · Продукты",
        "04 · Архитектура процесса",
        "05 · Кейсы",
        "06 · Возражения",
        "07 · Глоссарий",
        "08 · Проверь себя",
        "09 · Тест",
        "10 · Технологии",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("CeMAT RUSSIA · тема стенда: IT-решения для складской и производственной логистики")


# --- pages ---
if page == "01 · Питч":
    st.title("Питч на 30 секунд")
    st.markdown("""
    <div class="pitch-box">
    <b>Что сказать:</b><br><br>
    «IT Vectura — российская платформа для управления логистикой: транспорт, склад, двор и терминал
    в одной системе. Команда с опытом 15+ лет в отрасли, входим в реестр отечественного ПО, система
    уже обрабатывает 15 000+ заказов ежедневно у клиентов из ритейла и дистрибуции. Расскажите, как
    у вас сейчас устроена логистика — подскажу, какой модуль закроет вашу задачу.»
    </div>
    """, unsafe_allow_html=True)

elif page == "02 · О компании":
    st.title("О компании — факты")
    col1, col2 = st.columns(2)
    for i, (k, v) in enumerate(COMPANY_FACTS):
        target = col1 if i % 2 == 0 else col2
        target.markdown(f'<div class="fact-card"><div class="k">{k.upper()}</div>'
                         f'<div class="v">{v}</div></div>', unsafe_allow_html=True)
    st.info("Контакты компании: 8 800 101-26-96 · info@itvectura.com · itvectura.ru")

elif page == "03 · Продукты":
    st.title("Продукты экосистемы")
    cols = st.columns(2)
    for i, p in enumerate(PRODUCTS):
        with cols[i % 2]:
            with st.expander(f"{p['name']}  —  {p['tag']}"):
                st.write(p["desc"])
                for f in p["features"]:
                    st.markdown(f"- {f}")

elif page == "04 · Архитектура процесса":
    st.title("Архитектура процесса")
    steps = [
        ("1. Заказ появляется → TMS решает, как везти",
         "Заказ создаётся в учётной системе клиента и прилетает в TMS. Routing строит маршрут "
         "с учётом временных окон и вместимости — задача VRP, а не просто «путь по карте»."),
        ("2. Машина подъезжает к складу → включается YL",
         "YL бронирует слот под конкретную машину и ворота, водитель регистрируется сам через "
         "мобильное приложение. Убирает боль склада — фуры, которые стоят часами без координации."),
        ("3. Погрузка/разгрузка → работает WMS",
         "WMS знает, что и куда положить, что отгрузить на конкретную машину. После завершения "
         "сообщает в TMS: «погрузка завершена, можно ехать»."),
        ("4. Машина в пути → TMS пересчитывает план на лету",
         "Опоздание может каскадно сдвинуть следующий рейс того же водителя. Система показывает "
         "диспетчеру пересчитанные последствия — это «динамическое транспортное планирование»."),
        ("5. Терминал/порт → TOS ведёт весь цикл",
         "TOS — это TMS + WMS + YL, но заточенные под грузовой терминал: единая картина в одном окне."),
        ("6. Рейс закрыт → автоматические деньги и документы",
         "TMS считает оплату перевозчику, сверяет со счётом и формирует документы (ЭТрН и др.) "
         "через ЭДО — автоинвойсинг вместо ручной сверки в Excel."),
    ]
    for title, body in steps:
        with st.expander(title, expanded=(title.startswith("1."))):
            st.write(body)
    st.markdown("""
    <div class="tip-box">
    <b>Зачем нужен FrameWork:</b> у каждого клиента свои нюансы (коробки вместо паллет, возврат тары,
    многоплечевая доставка). FrameWork — инструмент, которым это настраивают под клиента: новое поле,
    статус, документ — без программиста.
    </div>
    """, unsafe_allow_html=True)

elif page == "05 · Кейсы":
    st.title("Кейсы — если спросят «а у кого уже работает»")
    for role, name, body in CASES:
        st.markdown(f"""
        <div class="case-card">
            <div class="case-role">{role}</div>
            <h4>{name}</h4>
            <div>{body.replace(chr(10), "<br>")}</div>
        </div>
        """, unsafe_allow_html=True)

elif page == "06 · Возражения":
    st.title("Частые вопросы — нажмите, чтобы раскрыть")
    for q, a in OBJECTIONS:
        with st.expander(q):
            st.write(a)

elif page == "07 · Глоссарий":
    st.title("Глоссарий")
    df = pd.DataFrame(GLOSSARY, columns=["Термин", "Расшифровка"])
    st.table(df)

elif page == "08 · Проверь себя":
    st.title("Проверь себя — флеш-карты")

    idx = st.session_state.fc_order[st.session_state.fc_index]
    question, answer = FLASHCARDS[idx]

    st.markdown(f"**Карточка {st.session_state.fc_index + 1} / {len(FLASHCARDS)}**")
    st.markdown(f"""
    <div class="pitch-box" style="min-height:100px;display:flex;align-items:center;">
    <div style="font-size:18px;font-weight:600;">{question}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.fc_flipped:
        st.success(answer)

    c1, c2, c3 = st.columns(3)
    if c1.button("Показать ответ" if not st.session_state.fc_flipped else "Скрыть ответ"):
        st.session_state.fc_flipped = not st.session_state.fc_flipped
        st.rerun()
    if c2.button("Следующая карточка →"):
        st.session_state.fc_index = (st.session_state.fc_index + 1) % len(FLASHCARDS)
        st.session_state.fc_flipped = False
        st.rerun()
    if c3.button("Перемешать"):
        random.shuffle(st.session_state.fc_order)
        st.session_state.fc_index = 0
        st.session_state.fc_flipped = False
        st.rerun()

elif page == "09 · Тест":
    st.title("Тест на знание продуктов")

    with st.form("quiz_form"):
        for i, item in enumerate(QUIZ_QUESTIONS):
            st.markdown(f"**Вопрос {i + 1}. {item['q']}**")
            st.session_state.quiz_answers[i] = st.radio(
                label=f"q{i}", options=list(range(len(item["opts"]))),
                format_func=lambda x, i=i: item["opts"][x],
                key=f"quiz_radio_{i}", label_visibility="collapsed", index=None,
            )
            st.markdown("")
        submitted = st.form_submit_button("Проверить результат")

    if submitted:
        st.session_state.quiz_submitted = True

    if st.session_state.quiz_submitted:
        score = sum(
            1 for i, item in enumerate(QUIZ_QUESTIONS)
            if st.session_state.quiz_answers.get(i) == item["correct"]
        )
        total = len(QUIZ_QUESTIONS)
        st.markdown("---")
        if score == total:
            st.success(f"Результат: {score}/{total}. Готовы к стенду.")
        elif score >= total * 0.7:
            st.warning(f"Результат: {score}/{total} — хороший результат, повторите темы с ошибками.")
        else:
            st.error(f"Результат: {score}/{total} — стоит вернуться к материалу перед выставкой.")

        for i, item in enumerate(QUIZ_QUESTIONS):
            user_answer = st.session_state.quiz_answers.get(i)
            is_correct = user_answer == item["correct"]
            icon = "✔" if is_correct else "✘"
            with st.expander(f"{icon} Вопрос {i + 1}: {item['q']}"):
                st.write(f"Правильный ответ: **{item['opts'][item['correct']]}**")
                st.write(item["exp"])

elif page == "10 · Технологии":
    st.title("Технологический стек")
    st.write("Полностью импортозамещённый стек, без привязки к иностранным вендорам.")
    col1, col2 = st.columns(2)
    for i, (k, v) in enumerate(TECH_STACK):
        target = col1 if i % 2 == 0 else col2
        target.markdown(f'<div class="fact-card"><div class="k">{k.upper()}</div>'
                         f'<div class="v">{v}</div></div>', unsafe_allow_html=True)

    st.subheader("Информационная безопасность")
    for line in TECH_SECURITY:
        st.markdown(f"- {line}")
