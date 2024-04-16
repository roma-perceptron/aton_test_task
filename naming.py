#
from dataclasses import dataclass
from random import choice, randint

NAMES = {
    'male': [
        'Фока', 'Лука', 'Фома', 'Кузьма', 'Никита', 'Глеб', 'Мирослав', 'Владислав', 'Вячеслав', 'Мстислав',
        'Святослав', 'Ростислав', 'Ярослав', 'Станислав', 'Лев', 'Яков', 'Олег', 'Давид', 'Леонид', 'Демид',
        'Всеволод', 'Эдуард', 'Николай', 'Ермолай', 'Ерофей', 'Варфоломей', 'Сергей', 'Авдей', 'Евсей', 'Фаддей',
        'Андрей', 'Алексей', 'Федосей', 'Тимофей', 'Матвей', 'Гордей', 'Евгений', 'Валерий', 'Евстафий', 'Аркадий',
        'Арсений', 'Иннокентий', 'Василий', 'Лаврентий', 'Зиновий', 'Афанасий', 'Геннадий', 'Артемий', 'Дмитрий',
        'Леонтий', 'Савелий', 'Викентий', 'Георгий', 'Виталий', 'Анатолий', 'Юрий', 'Григорий', 'Исаак',
        'Святополк', 'Марк', 'Павел', 'Самуил', 'Даниил', 'Гавриил', 'Михаил', 'Кирилл', 'Варлам', 'Ефрем',
        'Серафим', 'Максим', 'Ефим', 'Вадим', 'Герасим', 'Наум', 'Артём', 'Юлиан', 'Герман', 'Роман', 'Степан',
        'Иван', 'Руслан', 'Богдан', 'Владлен', 'Валентин', 'Антонин', 'Вениамин', 'Константин', 'Тихон',
        'Харитон', 'Родион', 'Антон', 'Валерьян', 'Емельян', 'Севастьян', 'Демьян', 'Семён', 'Потап', 'Архипп',
        'Филипп', 'Поликарп', 'Макар', 'Александр', 'Владимир', 'Егор', 'Прохор', 'Виктор', 'Фёдор', 'Федор',
        'Пётр', 'Тимур', 'Артур', 'Тарас', 'Борис', 'Денис', 'Феликс', 'Кондрат', 'Федот', 'Альберт', 'Аристарх',
        'Игорь', 'Илья'
    ],
    'female': [
        'Ольга', 'Надежда', 'Вероника', 'Анжела', 'Людмила', 'Алла', 'Алевтина', 'Валентина', 'Галина',
        'Ангелина', 'Марина', 'Алина', 'Татьяна', 'Елена', 'Екатерина', 'Катерина', 'Анна', 'Нина', 'Светлана',
        'Карина', 'Инна', 'Яна', 'Ирина', 'Антонина', 'Оксана', 'Вера', 'Александра', 'Тамара', 'Лариса',
        'Елизавета', 'Маргарита', 'Любовь', 'Юлия', 'Виктория', 'Анастасия', 'Ксения', 'Лидия', 'Евгения',
        'Мария', 'Валерия', 'Дарья', 'Наталья'
    ]
}

FAMILIES = [
    'Озеров', 'Зайцев', 'Солнцев', 'Ананасов', 'Столикин', 'Пчелов', 'Простынев', 'Билетников', 'Огурчин',
    'Анекдотов', 'Карпов', 'Лисичкин', 'Колокольчиков', 'Локтев', 'Окунев', 'Воронов', 'Гололедов', 'Пижамкин',
    'Жуков', 'Глазкин', 'Легендин', 'Сказочкин', 'Мухин', 'Бабочкин', 'Травянов', 'Веточкин', 'Палкин',
    'Морковин', 'Волков', 'Баклажанов', 'Котов', 'Воробьев', 'Баранов', 'Пенькин', 'Каменев', 'Коровьев',
    'Губкин', 'Ягодкин', 'Цветков', 'Кабачков', 'Голубев', 'Ручкин', 'Муравьев', 'Попкин', 'Карасев', 'Рыбкин',
    'Глазов', 'Взводин', 'Уткин', 'Зубов', 'Лунев', 'Лягушкин', 'Деревянкин', 'Бананов', 'Сорокин', 'Коровин',
    'Чесноков', 'Ежов', 'Щукин', 'Медведев', 'Грибов', 'Жабкин', 'Подушкин', 'Лосев', 'Козлов', 'Снежин',
    'Стулин', 'Комаров', 'Слизнев', 'Знойнов', 'Собачкин', 'Мышкин', 'Шуточкин', 'Воинов', 'Монетин',
    'Кроликов', 'Жаркин', 'Кошечкин', 'Птичкин', 'Травинкин', 'Хомяков', 'Тучкин', 'Коробкин', 'Кроваткин', 'Гусев'
]


@dataclass
class Fio():
    first_name: str = ''
    middle_name: str = ''
    last_name: str = ''

    def to_string(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'


def make_middle_name(sex):
    """ Генерация отчества """
    base = choice(NAMES['male'])
    if base in ['Федор', 'Пётр', 'Святополк']:
        middle_name = ''
    elif base.endswith('а') or base.endswith('я'):  # Лука, Фома.. Илья
        middle_name = base[:-1] + 'ич' if sex == 'male' else base[:-1] + 'инишна'
    elif base.endswith('слав'): # Вячеслав
        middle_name = base + 'ович' if sex == 'male' else base + 'овна'
    elif base.endswith('eв'): # Лев
        middle_name = base[:-2] + 'ьвович' if sex == 'male' else base[:-2] + 'ьвовна'
    elif base.endswith('ов'):   # Яков
        middle_name = base + 'левич' if sex == 'male' else base + 'левна'
    elif base.endswith('вел'):   # Павел
        middle_name = base[:-2] + 'лович' if sex == 'male' else base[:-2] + 'ловна'
    # Олег, Эдуард, Марк, Кирилл, Герасим, Роман, Потап, Макар, Кондрат, Аристарх
    elif any([True for char in ['б', 'г', 'д', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 'х'] if base.endswith(char)]):
        middle_name = base + 'ович' if sex == 'male' else base + 'овна'
    elif base.endswith('ь'):    # Игорь
        middle_name = base[:-1] + 'евич' if sex == 'male' else base[:-1] + 'евна'
    elif base.endswith('ий'):  # Василий
        middle_name = base[:-2] + 'ьевич' if sex == 'male' else base[:-2] + 'ьевна'
    elif base.endswith('й'):   # Николай, Сергей
        middle_name = base[:-1] + 'евич' if sex == 'male' else base[:-1] + 'евна'
    else:
        middle_name = ''
    #
    return middle_name


def make_fio():
    """ Генерация случайного ФИО """
    sex = choice(['male', 'female'])
    fio = Fio(
        first_name=choice(NAMES[sex]),
        middle_name=make_middle_name(sex),
        last_name=choice(FAMILIES) if sex == 'male' else choice(FAMILIES) + 'а'
    )
    #
    return fio


def show_examples():
    for i in range(10):
        fio = make_fio()
        print(f'{fio.last_name} {fio.first_name} {fio.middle_name}')


def get_next_char():
    """
    Генератор следующего символа для создания случайных имен
    Выдает гласную после согласной и наоборот в 80% случаев
    :return:
    """
    first = 'aeiou'
    second = 'bcdfghjklmnpqrstvwxyz'

    if choice([True, False]):
        first, second = second, first

    while True:
        yield choice(first)
        if choice((True, True, True, True, False)):
            first, second = second, first


# Создание генератора
next_char = get_next_char()


def get_random_name(min_chars=3, max_chars=9):
    """
    Генерация случайного человекоподобного имени из комбинации чередующихся гласных и согласных букв
    :param min_chars: минимальная длина имени
    :param max_chars: максимальная длина имени
    :return: строка с именем с большой буквы
    """
    name = ''.join([
        next(next_char) for i in range(randint(min_chars, max_chars))
    ])
    return name.capitalize()
