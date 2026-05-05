from django.core.management.base import BaseCommand
from apps.accounts.models import User, Follow
from apps.works.models import Category, Tag, Work, Album, AlbumWork, Like, Comment
from apps.orders.models import ServiceOffer, OrderRequest
from apps.notifications.models import Notification


CREATORS = [
    {
        'username': 'anna_foto', 'first_name': 'Анна', 'last_name': 'Волкова',
        'email': 'anna@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Москва', 'latitude': 55.7558, 'longitude': 37.6173,
        'bio': 'Свадебный и портретный фотограф с 8-летним опытом. Люблю живые эмоции и мягкий свет.',
        'specialization': 'Свадебная и портретная фотография',
        'instagram': 'anna_photo_msk', 'telegram': 'anna_foto',
        'avatar_url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200&h=200&fit=crop',
    },
    {
        'username': 'pavel_lens', 'first_name': 'Павел', 'last_name': 'Сидельников',
        'email': 'pavel@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Санкт-Петербург', 'latitude': 59.9311, 'longitude': 30.3609,
        'bio': 'Документальный и пейзажный фотограф. Путешествую и снимаю красоту мира.',
        'specialization': 'Пейзаж, документальная фотография',
        'instagram': 'pavel_lens', 'telegram': 'pavel_lens',
        'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&h=200&fit=crop',
    },
    {
        'username': 'ekaterina_design', 'first_name': 'Екатерина', 'last_name': 'Морозова',
        'email': 'kate@foto.ru', 'role': 'creator', 'creator_type': 'designer',
        'city': 'Москва', 'latitude': 55.7517, 'longitude': 37.6178,
        'bio': 'Графический дизайнер, специализируюсь на брендинге и айдентике для малого бизнеса.',
        'specialization': 'Брендинг, айдентика, логотипы',
        'instagram': 'kate_design_ru', 'telegram': 'kate_design',
        'avatar_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop',
    },
    {
        'username': 'igor_photo', 'first_name': 'Игорь', 'last_name': 'Петров',
        'email': 'igor@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Екатеринбург', 'latitude': 56.8389, 'longitude': 60.6057,
        'bio': 'Коммерческий фотограф. Предметная съёмка, реклама, корпоративные мероприятия.',
        'specialization': 'Коммерческая и предметная съёмка',
        'instagram': 'igor_commercial', 'telegram': 'igor_photo',
        'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=200&h=200&fit=crop',
    },
    {
        'username': 'marina_art', 'first_name': 'Марина', 'last_name': 'Казакова',
        'email': 'marina@foto.ru', 'role': 'creator', 'creator_type': 'illustrator',
        'city': 'Новосибирск', 'latitude': 54.9885, 'longitude': 82.9207,
        'bio': 'Иллюстратор детских книг и открыток. Работаю в акварельной и цифровой технике.',
        'specialization': 'Иллюстрация, акварель, детские книги',
        'instagram': 'marina_illustrations', 'telegram': 'marina_art',
        'avatar_url': 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=200&h=200&fit=crop',
    },
    {
        'username': 'dmitry_video', 'first_name': 'Дмитрий', 'last_name': 'Козлов',
        'email': 'dmitry@foto.ru', 'role': 'creator', 'creator_type': 'videographer',
        'city': 'Краснодар', 'latitude': 45.0355, 'longitude': 38.9753,
        'bio': 'Видеограф и режиссёр монтажа. Свадебное кино, рекламные ролики, клипы.',
        'specialization': 'Видеосъёмка, монтаж, аэросъёмка',
        'instagram': 'dmitry_films', 'telegram': 'dmitry_video',
        'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=200&h=200&fit=crop',
    },
    {
        'username': 'olga_photo', 'first_name': 'Ольга', 'last_name': 'Белова',
        'email': 'olga@foto.ru', 'role': 'creator', 'creator_type': 'photographer',
        'city': 'Казань', 'latitude': 55.7887, 'longitude': 49.1221,
        'bio': 'Семейный и детский фотограф. Создаю тёплые воспоминания на всю жизнь.',
        'specialization': 'Семейная и детская фотография',
        'instagram': 'olga_family_photo', 'telegram': 'olga_photo',
        'avatar_url': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop',
    },
    {
        'username': 'alexei_brand', 'first_name': 'Алексей', 'last_name': 'Новиков',
        'email': 'alexei@foto.ru', 'role': 'creator', 'creator_type': 'designer',
        'city': 'Санкт-Петербург', 'latitude': 59.9386, 'longitude': 30.3141,
        'bio': 'UX/UI дизайнер и бренд-стратег. Помогаю стартапам создать сильную визуальную идентичность.',
        'specialization': 'UX/UI дизайн, веб-интерфейсы, брендинг',
        'instagram': 'alexei_brand', 'telegram': 'alexei_ux',
        'avatar_url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=200&h=200&fit=crop',
    },
]

WORK_DATA = [
    # Свадьбы
    {'title': 'Свадьба на закате', 'creator': 'anna_foto', 'cat': 'weddings',
     'url': 'https://images.unsplash.com/photo-1519741497674-611481863552?w=800&h=600&fit=crop',
     'desc': 'Нежная свадьба на берегу озера в золотой час.', 'year': 2024, 'tags': ['свадьба', 'закат']},
    {'title': 'Первый танец', 'creator': 'anna_foto', 'cat': 'weddings',
     'url': 'https://images.unsplash.com/photo-1529636798458-92182e662485?w=800&h=1000&fit=crop',
     'desc': 'Трогательный момент первого танца молодожёнов.', 'year': 2024, 'tags': ['свадьба', 'эмоции']},
    {'title': 'Цветочная церемония', 'creator': 'anna_foto', 'cat': 'weddings',
     'url': 'https://images.unsplash.com/photo-1511285560929-80b456503681?w=800&h=600&fit=crop',
     'desc': 'Пышная флористика и белоснежные лепестки.', 'year': 2023, 'tags': ['свадьба', 'цветы']},
    {'title': 'Лесная свадьба', 'creator': 'olga_photo', 'cat': 'weddings',
     'url': 'https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800&h=1100&fit=crop',
     'desc': 'Уютная боho-свадьба в сосновом лесу.', 'year': 2024, 'tags': ['свадьба', 'природа']},
    {'title': 'Городская свадьба', 'creator': 'olga_photo', 'cat': 'weddings',
     'url': 'https://images.unsplash.com/photo-1606216794074-735e91aa2c92?w=800&h=600&fit=crop',
     'desc': 'Стильная свадьба в центре города.', 'year': 2023, 'tags': ['свадьба', 'город']},
    # Портрет
    {'title': 'Женский портрет', 'creator': 'anna_foto', 'cat': 'portrait',
     'url': 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&h=1100&fit=crop',
     'desc': 'Мягкий естественный свет, минималистичный фон.', 'year': 2024, 'tags': ['портрет', 'женщина']},
    {'title': 'Мужской портрет', 'creator': 'igor_photo', 'cat': 'portrait',
     'url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=1000&fit=crop',
     'desc': 'Студийный портрет с драматическим светом.', 'year': 2024, 'tags': ['портрет', 'студия']},
    {'title': 'Детский портрет', 'creator': 'olga_photo', 'cat': 'portrait',
     'url': 'https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?w=800&h=1000&fit=crop',
     'desc': 'Живые детские эмоции в естественной среде.', 'year': 2023, 'tags': ['портрет', 'дети']},
    {'title': 'Семейный портрет', 'creator': 'olga_photo', 'cat': 'portrait',
     'url': 'https://images.unsplash.com/photo-1511895426328-dc8714191011?w=800&h=600&fit=crop',
     'desc': 'Счастливая семья в осеннем парке.', 'year': 2024, 'tags': ['портрет', 'семья']},
    # Пейзаж
    {'title': 'Закат над Байкалом', 'creator': 'pavel_lens', 'cat': 'landscape',
     'url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
     'desc': 'Невероятный закат над великим озером.', 'year': 2024, 'tags': ['пейзаж', 'озеро', 'закат']},
    {'title': 'Горные вершины', 'creator': 'pavel_lens', 'cat': 'landscape',
     'url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&h=600&fit=crop',
     'desc': 'Рассвет в горах Алтая.', 'year': 2024, 'tags': ['пейзаж', 'горы']},
    {'title': 'Берёзовый лес', 'creator': 'pavel_lens', 'cat': 'landscape',
     'url': 'https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&h=1000&fit=crop',
     'desc': 'Туманное утро в берёзовой роще.', 'year': 2023, 'tags': ['пейзаж', 'лес']},
    {'title': 'Зимняя Москва', 'creator': 'anna_foto', 'cat': 'landscape',
     'url': 'https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800&h=600&fit=crop',
     'desc': 'Снежная Москва в ночных огнях.', 'year': 2024, 'tags': ['пейзаж', 'город', 'зима']},
    # Графический дизайн
    {'title': 'Фирменный стиль Café Nord', 'creator': 'ekaterina_design', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=600&fit=crop',
     'desc': 'Разработка полного брендбука для скандинавского кафе.', 'year': 2024, 'tags': ['брендинг', 'кафе']},
    {'title': 'Логотип TechStart', 'creator': 'ekaterina_design', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1626785774573-4b799315345d?w=800&h=600&fit=crop',
     'desc': 'Минималистичный логотип для IT-стартапа.', 'year': 2024, 'tags': ['логотип', 'IT']},
    {'title': 'Дизайн упаковки', 'creator': 'ekaterina_design', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=800&h=800&fit=crop',
     'desc': 'Экологичная упаковка для линейки косметики.', 'year': 2023, 'tags': ['упаковка', 'экология']},
    {'title': 'UI Kit мобильного приложения', 'creator': 'alexei_brand', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&h=600&fit=crop',
     'desc': 'Полный UI Kit для фитнес-приложения.', 'year': 2024, 'tags': ['UI', 'мобильный']},
    {'title': 'Дизайн-система StartFlow', 'creator': 'alexei_brand', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=800&h=600&fit=crop',
     'desc': 'Масштабируемая дизайн-система для SaaS-платформы.', 'year': 2024, 'tags': ['дизайн-система', 'SaaS']},
    # Коммерческая
    {'title': 'Предметная съёмка часов', 'creator': 'igor_photo', 'cat': 'commercial',
     'url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=800&fit=crop',
     'desc': 'Рекламная съёмка премиальных часов.', 'year': 2024, 'tags': ['предметная', 'часы']},
    {'title': 'Еда для ресторана', 'creator': 'igor_photo', 'cat': 'commercial',
     'url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&h=600&fit=crop',
     'desc': 'Аппетитная фуд-съёмка для меню ресторана.', 'year': 2024, 'tags': ['еда', 'ресторан']},
    {'title': 'Корпоративные портреты', 'creator': 'igor_photo', 'cat': 'commercial',
     'url': 'https://images.unsplash.com/photo-1560472355-536de3962603?w=800&h=600&fit=crop',
     'desc': 'Деловые портреты команды для сайта компании.', 'year': 2023, 'tags': ['корпоративная', 'бизнес']},
    {'title': 'Рекламная кампания', 'creator': 'anna_foto', 'cat': 'commercial',
     'url': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=600&fit=crop',
     'desc': 'Съёмка для рекламной кампании бренда одежды.', 'year': 2024, 'tags': ['реклама', 'мода']},
    # Иллюстрации
    {'title': 'Детская книга «Лесные друзья»', 'creator': 'marina_art', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&h=600&fit=crop',
     'desc': 'Иллюстрации акварелью для детской книги.', 'year': 2024, 'tags': ['иллюстрация', 'акварель']},
    {'title': 'Открытки к Новому году', 'creator': 'marina_art', 'cat': 'graphic',
     'url': 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=800&h=600&fit=crop',
     'desc': 'Серия праздничных открыток с авторскими иллюстрациями.', 'year': 2023, 'tags': ['открытка', 'праздник']},
    # Видео (представлено как постеры)
    {'title': 'Свадебный фильм', 'creator': 'dmitry_video', 'cat': 'weddings',
     'url': 'https://images.unsplash.com/photo-1524824267900-2b13413b8634?w=800&h=600&fit=crop',
     'desc': 'Кинематографичный свадебный фильм в 4K.', 'year': 2024, 'tags': ['видео', 'свадьба']},
    {'title': 'Рекламный ролик', 'creator': 'dmitry_video', 'cat': 'commercial',
     'url': 'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=800&h=600&fit=crop',
     'desc': 'Атмосферный рекламный ролик для ресторана.', 'year': 2024, 'tags': ['видео', 'реклама']},
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
        tag_names = ['свадьба', 'портрет', 'пейзаж', 'закат', 'природа', 'город', 'брендинг',
                     'логотип', 'иллюстрация', 'видео', 'реклама', 'семья', 'дети', 'студия',
                     'акварель', 'UI', 'мобильный', 'упаковка', 'еда', 'кафе', 'бизнес',
                     'мода', 'горы', 'озеро', 'лес', 'зима', 'предметная', 'часы', 'открытка',
                     'IT', 'корпоративная', 'эмоции', 'цветы', 'экология', 'праздник', 'SaaS']
        tag_objs = {}
        for t in tag_names:
            slug = t.lower().replace(' ', '-')
            tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': t})
            tag_objs[t] = tag

        self.stdout.write('Создаём пользователей...')
        creator_objs = {}
        for c in CREATORS:
            if User.objects.filter(username=c['username']).exists():
                u = User.objects.get(username=c['username'])
            else:
                u = User.objects.create_user(
                    username=c['username'],
                    email=c['email'],
                    password='Creator123!',
                    first_name=c['first_name'],
                    last_name=c['last_name'],
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
        for i, (uname, fname, lname, email) in enumerate([
            ('client_ivan', 'Иван', 'Семёнов', 'ivan@client.ru'),
            ('client_maria', 'Мария', 'Фролова', 'maria@client.ru'),
            ('client_sergey', 'Сергей', 'Орлов', 'sergey@client.ru'),
        ]):
            if not User.objects.filter(username=uname).exists():
                cl = User.objects.create_user(username=uname, email=email, password='Client123!',
                                              first_name=fname, last_name=lname)
                cl.role = 'client'
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
                title=wd['title'],
                creator=creator,
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
        texts = [
            'Потрясающая работа!', 'Очень красиво!', 'Вдохновляет!',
            'Мастерство на высшем уровне.', 'Супер!', 'Люблю ваш стиль.',
            'Когда-нибудь хочу заказать у вас!', 'Wow, просто wow!',
        ]
        all_users = list(creator_objs.values()) + clients
        for i, w in enumerate(work_objs[:20]):
            likers = all_users[:(i % 5 + 2)]
            for u in likers:
                if u != w.creator:
                    Like.objects.get_or_create(user=u, work=w)
            w.likes_count = Like.objects.filter(work=w).count()
            w.save(update_fields=['likes_count'])

            if i % 3 == 0:
                commenter = all_users[i % len(all_users)]
                Comment.objects.get_or_create(
                    user=commenter, work=w,
                    defaults={'text': texts[i % len(texts)]}
                )
                w.comments_count = Comment.objects.filter(work=w).count()
                w.save(update_fields=['comments_count'])

        self.stdout.write('Создаём подписки...')
        pairs = [('client_ivan', 'anna_foto'), ('client_ivan', 'pavel_lens'),
                 ('client_maria', 'ekaterina_design'), ('client_sergey', 'igor_photo'),
                 ('anna_foto', 'pavel_lens'), ('ekaterina_design', 'alexei_brand')]
        for follower_name, following_name in pairs:
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
                defaults={'project_type': 'Свадебная фотосессия', 'budget': '50 000 ₽',
                          'description': 'Планируем свадьбу в июне. Хотим естественные живые снимки.',
                          'contact_email': clients[0].email, 'status': 'discussing'}
            )
            OrderRequest.objects.get_or_create(
                client=clients[1], creator=creator_objs['ekaterina_design'],
                defaults={'project_type': 'Логотип и фирменный стиль', 'budget': '30 000 ₽',
                          'description': 'Открываем кофейню, нужен логотип и базовый брендбук.',
                          'contact_email': clients[1].email, 'status': 'new'}
            )

        self.stdout.write(self.style.SUCCESS('✅ Данные успешно инициализированы!'))
