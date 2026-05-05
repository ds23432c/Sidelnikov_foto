from django.core.management.base import BaseCommand
from apps.accounts.models import User, Follow
from apps.works.models import Category, Tag, Work, Album, AlbumWork, Like, Comment
from apps.orders.models import ServiceOffer, OrderRequest
from apps.notifications.models import Notification

# Аватары: randomuser.me — реальные лица людей, стабильно работает
# Фото работ: picsum.photos/id/{ID}/{w}/{h} — конкретные ID по тематике

CREATORS = [
    {
        'username': 'anna_foto', 'first_name': 'Анна', 'last_name': 'Волкова',
        'email': 'anna@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Москва', 'latitude': 55.7558, 'longitude': 37.6173,
        'bio': 'Свадебный и портретный фотограф с 8-летним опытом. Люблю живые эмоции и мягкий свет.',
        'specialization': 'Свадебная и портретная фотография',
        'instagram': 'anna_photo_msk', 'telegram': 'anna_foto',
        'avatar_url': 'https://randomuser.me/api/portraits/women/44.jpg',  # женщина ~30 лет
    },
    {
        'username': 'pavel_lens', 'first_name': 'Павел', 'last_name': 'Сидельников',
        'email': 'pavel@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Санкт-Петербург', 'latitude': 59.9311, 'longitude': 30.3609,
        'bio': 'Документальный и пейзажный фотограф. Путешествую и снимаю красоту мира.',
        'specialization': 'Пейзаж, документальная фотография',
        'instagram': 'pavel_lens', 'telegram': 'pavel_lens',
        'avatar_url': 'https://randomuser.me/api/portraits/men/32.jpg',  # мужчина ~35 лет
    },
    {
        'username': 'ekaterina_design', 'first_name': 'Екатерина', 'last_name': 'Морозова',
        'email': 'kate@foto.ru', 'role': 'creator', 'creator_type': 'designer',
        'city': 'Москва', 'latitude': 55.7517, 'longitude': 37.6178,
        'bio': 'Графический дизайнер, специализируюсь на брендинге и айдентике для малого бизнеса.',
        'specialization': 'Брендинг, айдентика, логотипы',
        'instagram': 'kate_design_ru', 'telegram': 'kate_design',
        'avatar_url': 'https://randomuser.me/api/portraits/women/68.jpg',  # молодая женщина-дизайнер
    },
    {
        'username': 'igor_photo', 'first_name': 'Игорь', 'last_name': 'Петров',
        'email': 'igor@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Екатеринбург', 'latitude': 56.8389, 'longitude': 60.6057,
        'bio': 'Коммерческий фотограф. Предметная съёмка, реклама, корпоративные мероприятия.',
        'specialization': 'Коммерческая и предметная съёмка',
        'instagram': 'igor_commercial', 'telegram': 'igor_photo',
        'avatar_url': 'https://randomuser.me/api/portraits/men/75.jpg',  # мужчина ~40 лет
    },
    {
        'username': 'marina_art', 'first_name': 'Марина', 'last_name': 'Казакова',
        'email': 'marina@foto.ru', 'role': 'creator', 'creator_type': 'illustrator',
        'city': 'Новосибирск', 'latitude': 54.9885, 'longitude': 82.9207,
        'bio': 'Иллюстратор детских книг и открыток. Работаю в акварельной и цифровой технике.',
        'specialization': 'Иллюстрация, акварель, детские книги',
        'instagram': 'marina_illustrations', 'telegram': 'marina_art',
        'avatar_url': 'https://randomuser.me/api/portraits/women/17.jpg',  # творческая женщина
    },
    {
        'username': 'dmitry_video', 'first_name': 'Дмитрий', 'last_name': 'Козлов',
        'email': 'dmitry@foto.ru', 'role': 'creator', 'creator_type': 'videographer',
        'city': 'Краснодар', 'latitude': 45.0355, 'longitude': 38.9753,
        'bio': 'Видеограф и режиссёр монтажа. Свадебное кино, рекламные ролики, клипы.',
        'specialization': 'Видеосъёмка, монтаж, аэросъёмка',
        'instagram': 'dmitry_films', 'telegram': 'dmitry_video',
        'avatar_url': 'https://randomuser.me/api/portraits/men/22.jpg',  # молодой мужчина-видеограф
    },
    {
        'username': 'olga_photo', 'first_name': 'Ольга', 'last_name': 'Белова',
        'email': 'olga@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Казань', 'latitude': 55.7887, 'longitude': 49.1221,
        'bio': 'Семейный и детский фотограф. Создаю тёплые воспоминания на всю жизнь.',
        'specialization': 'Семейная и детская фотография',
        'instagram': 'olga_family_photo', 'telegram': 'olga_photo',
        'avatar_url': 'https://randomuser.me/api/portraits/women/56.jpg',  # женщина ~28 лет
    },
    {
        'username': 'alexei_brand', 'first_name': 'Алексей', 'last_name': 'Новиков',
        'email': 'alexei@foto.ru', 'role': 'creator', 'creator_type': 'designer',
        'city': 'Санкт-Петербург', 'latitude': 59.9386, 'longitude': 30.3141,
        'bio': 'UX/UI дизайнер и бренд-стратег. Помогаю стартапам создать сильную визуальную идентичность.',
        'specialization': 'UX/UI дизайн, веб-интерфейсы, брендинг',
        'instagram': 'alexei_brand', 'telegram': 'alexei_ux',
        'avatar_url': 'https://randomuser.me/api/portraits/men/46.jpg',  # молодой мужчина-дизайнер
    },
]

# picsum.photos/id/{ID}/{w}/{h} — стабильные ID, тематически подобраны:
# 433, 1005 — пары, люди вместе (свадьба/романтика)
# 316, 823 — цветы, флористика
# 15, 29, 37, 57, 96, 103 — природа, пейзажи
# 64, 91, 177, 338, 453, 582, 1011 — люди, портреты
# 431 — кофе/кафе
# 292, 488, 547 — еда
# 376 — часы, предмет
# 1, 26, 48, 0 — абстракция/технологии/дизайн
# 318, 412 — вид сверху/город

WORK_DATA = [
    # ===== СВАДЬБЫ =====
    {
        'title': 'Свадьба на закате',
        'creator': 'anna_foto', 'cat': 'weddings',
        'url': 'https://picsum.photos/id/433/800/600',   # пара на природе
        'desc': 'Нежная свадьба на берегу озера в золотой час.', 'year': 2024,
        'tags': ['свадьба', 'закат'],
    },
    {
        'title': 'Первый танец',
        'creator': 'anna_foto', 'cat': 'weddings',
        'url': 'https://picsum.photos/id/1005/800/1000',  # двое людей, момент
        'desc': 'Трогательный момент первого танца молодожёнов.', 'year': 2024,
        'tags': ['свадьба', 'эмоции'],
    },
    {
        'title': 'Цветочная церемония',
        'creator': 'anna_foto', 'cat': 'weddings',
        'url': 'https://picsum.photos/id/316/800/600',   # цветы
        'desc': 'Пышная флористика и белоснежные лепестки.', 'year': 2023,
        'tags': ['свадьба', 'цветы'],
    },
    {
        'title': 'Лесная свадьба',
        'creator': 'olga_photo', 'cat': 'weddings',
        'url': 'https://picsum.photos/id/218/800/1100',  # лес, деревья
        'desc': 'Уютная бохо-свадьба в сосновом лесу.', 'year': 2024,
        'tags': ['свадьба', 'природа'],
    },
    {
        'title': 'Городская свадьба',
        'creator': 'olga_photo', 'cat': 'weddings',
        'url': 'https://picsum.photos/id/396/800/600',   # городская архитектура
        'desc': 'Стильная свадьба в центре города.', 'year': 2023,
        'tags': ['свадьба', 'город'],
    },
    {
        'title': 'Свадебный фильм',
        'creator': 'dmitry_video', 'cat': 'weddings',
        'url': 'https://picsum.photos/id/823/800/600',   # букет невесты, цветы
        'desc': 'Кинематографичный свадебный фильм в 4K.', 'year': 2024,
        'tags': ['видео', 'свадьба'],
    },

    # ===== ПОРТРЕТ =====
    {
        'title': 'Женский портрет',
        'creator': 'anna_foto', 'cat': 'portrait',
        'url': 'https://picsum.photos/id/64/800/1100',   # женщина, портрет
        'desc': 'Мягкий естественный свет, минималистичный фон.', 'year': 2024,
        'tags': ['портрет', 'женщина'],
    },
    {
        'title': 'Мужской портрет',
        'creator': 'igor_photo', 'cat': 'portrait',
        'url': 'https://picsum.photos/id/91/800/1000',   # мужчина, портрет
        'desc': 'Студийный портрет с драматическим светом.', 'year': 2024,
        'tags': ['портрет', 'студия'],
    },
    {
        'title': 'Детский портрет',
        'creator': 'olga_photo', 'cat': 'portrait',
        'url': 'https://picsum.photos/id/177/800/1000',  # человек в тёплой обстановке
        'desc': 'Живые детские эмоции в естественной среде.', 'year': 2023,
        'tags': ['портрет', 'дети'],
    },
    {
        'title': 'Семейный портрет',
        'creator': 'olga_photo', 'cat': 'portrait',
        'url': 'https://picsum.photos/id/338/800/600',   # люди на природе
        'desc': 'Счастливая семья в осеннем парке.', 'year': 2024,
        'tags': ['портрет', 'семья'],
    },
    {
        'title': 'Арт-портрет',
        'creator': 'anna_foto', 'cat': 'portrait',
        'url': 'https://picsum.photos/id/582/800/1200',  # человек, художественный
        'desc': 'Художественный портрет с необычным светом.', 'year': 2024,
        'tags': ['портрет', 'арт'],
    },

    # ===== ПЕЙЗАЖ =====
    {
        'title': 'Закат над Байкалом',
        'creator': 'pavel_lens', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/15/800/600',    # озеро, закат
        'desc': 'Невероятный закат над великим озером.', 'year': 2024,
        'tags': ['пейзаж', 'озеро', 'закат'],
    },
    {
        'title': 'Горные вершины',
        'creator': 'pavel_lens', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/29/800/600',    # горы
        'desc': 'Рассвет в горах Алтая.', 'year': 2024,
        'tags': ['пейзаж', 'горы'],
    },
    {
        'title': 'Берёзовый лес',
        'creator': 'pavel_lens', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/37/800/1000',   # лес, деревья
        'desc': 'Туманное утро в берёзовой роще.', 'year': 2023,
        'tags': ['пейзаж', 'лес'],
    },
    {
        'title': 'Зимняя Москва',
        'creator': 'anna_foto', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/57/800/600',    # город, огни
        'desc': 'Снежная Москва в ночных огнях.', 'year': 2024,
        'tags': ['пейзаж', 'город', 'зима'],
    },
    {
        'title': 'Северное сияние',
        'creator': 'pavel_lens', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/96/800/500',    # небо, звёзды
        'desc': 'Полярное сияние над тундрой.', 'year': 2023,
        'tags': ['пейзаж', 'природа'],
    },
    {
        'title': 'Осенний парк',
        'creator': 'olga_photo', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/103/800/1100',  # деревья, осень
        'desc': 'Золотая осень в городском парке.', 'year': 2024,
        'tags': ['пейзаж', 'осень'],
    },
    {
        'title': 'Аэросъёмка города',
        'creator': 'dmitry_video', 'cat': 'landscape',
        'url': 'https://picsum.photos/id/318/800/500',   # вид сверху, панорама
        'desc': 'Аэросъёмка Краснодара на рассвете.', 'year': 2024,
        'tags': ['видео', 'город', 'аэро'],
    },

    # ===== ГРАФИЧЕСКИЙ ДИЗАЙН =====
    {
        'title': 'Фирменный стиль Café Nord',
        'creator': 'ekaterina_design', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/431/800/600',   # кофе, кафе
        'desc': 'Разработка полного брендбука для скандинавского кафе.', 'year': 2024,
        'tags': ['брендинг', 'кафе'],
    },
    {
        'title': 'Логотип TechStart',
        'creator': 'ekaterina_design', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/1/800/600',     # технологии, ноутбук
        'desc': 'Минималистичный логотип для IT-стартапа.', 'year': 2024,
        'tags': ['логотип', 'IT'],
    },
    {
        'title': 'Дизайн упаковки',
        'creator': 'ekaterina_design', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/26/800/800',    # продукт, упаковка
        'desc': 'Экологичная упаковка для линейки косметики.', 'year': 2023,
        'tags': ['упаковка', 'экология'],
    },
    {
        'title': 'UI Kit мобильного приложения',
        'creator': 'alexei_brand', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/0/800/600',     # технологии, экран
        'desc': 'Полный UI Kit для фитнес-приложения.', 'year': 2024,
        'tags': ['UI', 'мобильный'],
    },
    {
        'title': 'Дизайн-система StartFlow',
        'creator': 'alexei_brand', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/48/800/600',    # абстракция, цвет
        'desc': 'Масштабируемая дизайн-система для SaaS-платформы.', 'year': 2024,
        'tags': ['дизайн-система', 'SaaS'],
    },
    {
        'title': 'Детская книга «Лесные друзья»',
        'creator': 'marina_art', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/142/800/600',   # природа, мягкие цвета
        'desc': 'Иллюстрации акварелью для детской книги.', 'year': 2024,
        'tags': ['иллюстрация', 'акварель'],
    },
    {
        'title': 'Открытки к Новому году',
        'creator': 'marina_art', 'cat': 'graphic',
        'url': 'https://picsum.photos/id/118/800/600',   # зима, снег
        'desc': 'Серия праздничных открыток с авторскими иллюстрациями.', 'year': 2023,
        'tags': ['открытка', 'праздник'],
    },

    # ===== КОММЕРЧЕСКАЯ =====
    {
        'title': 'Предметная съёмка часов',
        'creator': 'igor_photo', 'cat': 'commercial',
        'url': 'https://picsum.photos/id/376/800/800',   # часы крупным планом
        'desc': 'Рекламная съёмка премиальных часов.', 'year': 2024,
        'tags': ['предметная', 'часы'],
    },
    {
        'title': 'Еда для ресторана',
        'creator': 'igor_photo', 'cat': 'commercial',
        'url': 'https://picsum.photos/id/292/800/600',   # красивая еда
        'desc': 'Аппетитная фуд-съёмка для меню ресторана.', 'year': 2024,
        'tags': ['еда', 'ресторан'],
    },
    {
        'title': 'Корпоративные портреты',
        'creator': 'igor_photo', 'cat': 'commercial',
        'url': 'https://picsum.photos/id/453/800/600',   # деловые люди
        'desc': 'Деловые портреты команды для сайта компании.', 'year': 2023,
        'tags': ['корпоративная', 'бизнес'],
    },
    {
        'title': 'Рекламная кампания',
        'creator': 'anna_foto', 'cat': 'commercial',
        'url': 'https://picsum.photos/id/1011/800/600',  # человек, стиль, мода
        'desc': 'Съёмка для рекламной кампании бренда одежды.', 'year': 2024,
        'tags': ['реклама', 'мода'],
    },
    {
        'title': 'Съёмка интерьера',
        'creator': 'igor_photo', 'cat': 'commercial',
        'url': 'https://picsum.photos/id/137/800/700',   # интерьер, помещение
        'desc': 'Интерьерная съёмка ресторана для сайта.', 'year': 2024,
        'tags': ['интерьер', 'ресторан'],
    },
    {
        'title': 'Рекламный ролик',
        'creator': 'dmitry_video', 'cat': 'commercial',
        'url': 'https://picsum.photos/id/488/800/600',   # атмосфера, стиль
        'desc': 'Атмосферный рекламный ролик для ресторана.', 'year': 2024,
        'tags': ['видео', 'реклама'],
    },
]

SERVICES = [
    {'creator': 'anna_foto', 'title': 'Свадебная фотосессия', 'desc': 'Полный день съёмки, 300+ обработанных фото', 'price_from': 35000, 'price_to': 80000, 'days': 14},
    {'creator': 'anna_foto', 'title': 'Портретная фотосессия', 'desc': '2 часа съёмки, 50 обработанных фото', 'price_from': 8000, 'price_to': 15000, 'days': 5},
    {'creator': 'anna_foto', 'title': 'Love story', 'desc': 'Романтическая фотосессия для пар', 'price_from': 12000, 'price_to': 20000, 'days': 7},
    {'creator': 'pavel_lens', 'title': 'Пейзажная экспедиция', 'desc': 'Фотоэкспедиция по заповедным местам', 'price_from': 50000, 'price_to': None, 'days': 30},
    {'creator': 'ekaterina_design', 'title': 'Разработка логотипа', 'desc': '3 концепции, правки включены', 'price_from': 15000, 'price_to': 30000, 'days': 7},
    {'creator': 'ekaterina_design', 'title': 'Фирменный стиль', 'desc': 'Логотип + брендбук + носители', 'price_from': 40000, 'price_to': 90000, 'days': 21},
    {'creator': 'igor_photo', 'title': 'Предметная съёмка', 'desc': 'Студийная съёмка товаров для интернет-магазина', 'price_from': 500, 'price_to': 1500, 'days': 3},
    {'creator': 'dmitry_video', 'title': 'Свадебный клип', 'desc': 'Кинематографичный фильм до 10 минут', 'price_from': 45000, 'price_to': 90000, 'days': 30},
    {'creator': 'alexei_brand', 'title': 'UI/UX дизайн приложения', 'desc': 'Прототип + финальный дизайн', 'price_from': 60000, 'price_to': 150000, 'days': 30},
    {'creator': 'marina_art', 'title': 'Иллюстрации для книги', 'desc': 'Авторские иллюстрации в акварельной технике', 'price_from': 3000, 'price_to': 8000, 'days': 14},
]


class Command(BaseCommand):
    help = 'Инициализация тестовых данных'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаём категории...')
        cats = {}
        for name, slug, icon in [
            ('Свадьбы', 'weddings', 'bi-heart'),
            ('Портрет', 'portrait', 'bi-person'),
            ('Пейзаж', 'landscape', 'bi-image'),
            ('Графический дизайн', 'graphic', 'bi-palette'),
            ('Коммерческая', 'commercial', 'bi-bag'),
        ]:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={'name': name, 'icon': icon})
            cats[slug] = cat

        self.stdout.write('Создаём теги...')
        tag_names = [
            'свадьба', 'портрет', 'пейзаж', 'закат', 'природа', 'город', 'брендинг',
            'логотип', 'иллюстрация', 'видео', 'реклама', 'семья', 'дети', 'студия',
            'акварель', 'UI', 'мобильный', 'упаковка', 'еда', 'кафе', 'бизнес',
            'мода', 'горы', 'озеро', 'лес', 'зима', 'предметная', 'часы', 'открытка',
            'IT', 'корпоративная', 'эмоции', 'цветы', 'экология', 'праздник', 'SaaS',
            'арт', 'женщина', 'аэро', 'осень', 'интерьер', 'ресторан', 'дизайн-система',
        ]
        tag_objs = {}
        for t in tag_names:
            slug_t = t.lower().replace(' ', '-')
            tag, _ = Tag.objects.get_or_create(slug=slug_t, defaults={'name': t})
            tag_objs[t] = tag

        self.stdout.write('Создаём пользователей-создателей...')
        creator_objs = {}
        for c in CREATORS:
            if User.objects.filter(username=c['username']).exists():
                u = User.objects.get(username=c['username'])
            else:
                u = User.objects.create_user(
                    username=c['username'], email=c['email'], password='Creator123!',
                    first_name=c['first_name'], last_name=c['last_name'],
                )
            u.role = c['role']
            u.creator_type = c['creator_type']
            u.city = c['city']
            u.latitude = c['latitude']
            u.longitude = c['longitude']
            u.bio = c['bio']
            u.specialization = c['specialization']
            u.instagram = c.get('instagram', '')
            u.telegram = c.get('telegram', '')
            u.avatar_url = c['avatar_url']
            u.is_verified = True
            u.save()
            creator_objs[c['username']] = u

        self.stdout.write('Создаём клиентов...')
        clients = []
        for uname, fname, lname, email, avatar in [
            ('client_ivan', 'Иван', 'Семёнов', 'ivan@client.ru', 'https://randomuser.me/api/portraits/men/11.jpg'),
            ('client_maria', 'Мария', 'Фролова', 'maria@client.ru', 'https://randomuser.me/api/portraits/women/29.jpg'),
            ('client_sergey', 'Сергей', 'Орлов', 'sergey@client.ru', 'https://randomuser.me/api/portraits/men/55.jpg'),
        ]:
            if not User.objects.filter(username=uname).exists():
                cl = User.objects.create_user(
                    username=uname, email=email, password='Client123!',
                    first_name=fname, last_name=lname,
                )
                cl.role = 'client'
                cl.avatar_url = avatar
                cl.save()
            else:
                cl = User.objects.get(username=uname)
            clients.append(cl)

        self.stdout.write('Создаём работы...')
        work_objs = []
        for wd in WORK_DATA:
            creator = creator_objs.get(wd['creator'])
            if not creator:
                continue
            cat = cats.get(wd['cat'])
            w, created = Work.objects.get_or_create(
                title=wd['title'], creator=creator,
                defaults={
                    'description': wd.get('desc', ''),
                    'image_url': wd['url'],
                    'category': cat,
                    'year': wd.get('year'),
                    'is_published': True,
                    'is_featured': True,
                }
            )
            for tname in wd.get('tags', []):
                if tname in tag_objs:
                    w.tags.add(tag_objs[tname])
            work_objs.append(w)

        self.stdout.write('Обновляем счётчики работ...')
        for u in creator_objs.values():
            u.works_count = Work.objects.filter(creator=u).count()
            u.save()

        self.stdout.write('Создаём лайки и комментарии...')
        comment_texts = [
            'Потрясающая работа!', 'Очень красиво, вдохновляет!', 'Мастерство на высшем уровне.',
            'Когда-нибудь хочу заказать у вас!', 'Просто wow!', 'Люблю ваш стиль.',
            'Такой атмосферный кадр!', 'Профессионально и со вкусом.',
        ]
        all_users = list(creator_objs.values()) + clients
        for i, w in enumerate(work_objs[:20]):
            likers = [u for u in all_users[:(i % 5 + 2)] if u != w.creator]
            for u in likers:
                Like.objects.get_or_create(user=u, work=w)
            w.likes_count = Like.objects.filter(work=w).count()
            w.save(update_fields=['likes_count'])
            if i % 3 == 0:
                commenter = all_users[(i + 1) % len(all_users)]
                if commenter != w.creator:
                    Comment.objects.get_or_create(
                        user=commenter, work=w,
                        defaults={'text': comment_texts[i % len(comment_texts)]}
                    )
                    w.comments_count = Comment.objects.filter(work=w).count()
                    w.save(update_fields=['comments_count'])

        self.stdout.write('Создаём подписки...')
        for follower_name, following_name in [
            ('client_ivan', 'anna_foto'), ('client_ivan', 'pavel_lens'),
            ('client_maria', 'ekaterina_design'), ('client_sergey', 'igor_photo'),
            ('anna_foto', 'pavel_lens'), ('ekaterina_design', 'alexei_brand'),
            ('client_ivan', 'olga_photo'), ('client_maria', 'marina_art'),
        ]:
            follower = User.objects.filter(username=follower_name).first()
            following = User.objects.filter(username=following_name).first()
            if follower and following:
                Follow.objects.get_or_create(follower=follower, following=following)
        for u in User.objects.all():
            u.followers_count = Follow.objects.filter(following=u).count()
            u.save(update_fields=['followers_count'])

        self.stdout.write('Создаём услуги...')
        for s in SERVICES:
            creator = creator_objs.get(s['creator'])
            if creator:
                ServiceOffer.objects.get_or_create(
                    creator=creator, title=s['title'],
                    defaults={
                        'description': s['desc'],
                        'price_from': s['price_from'],
                        'price_to': s['price_to'],
                        'delivery_days': s['days'],
                    }
                )

        self.stdout.write('Создаём заявки...')
        if clients and creator_objs:
            OrderRequest.objects.get_or_create(
                client=clients[0], creator=creator_objs['anna_foto'],
                defaults={
                    'project_type': 'Свадебная фотосессия', 'budget': '50 000 ₽',
                    'description': 'Планируем свадьбу в июне. Хотим естественные живые снимки.',
                    'contact_email': clients[0].email, 'status': 'discussing',
                }
            )
            OrderRequest.objects.get_or_create(
                client=clients[1], creator=creator_objs['ekaterina_design'],
                defaults={
                    'project_type': 'Логотип и фирменный стиль', 'budget': '30 000 ₽',
                    'description': 'Открываем кофейню, нужен логотип и базовый брендбук.',
                    'contact_email': clients[1].email, 'status': 'new',
                }
            )

        self.stdout.write(self.style.SUCCESS(f'✅ Готово! Создателей: {len(creator_objs)}, Работ: {len(work_objs)}, Клиентов: {len(clients)}'))
