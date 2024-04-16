# различные вспомогательные функции
from datetime import date
from hashlib import sha256
from random import randint, choice


def hash_it(secret: str):
    """ Получение хэша строки (для хранения и прверки паролей) """
    hash_object = sha256(bytes(secret, 'utf=8'))
    hex_dig = hash_object.hexdigest()
    return hex_dig


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


def get_initial_tables(status_constants: dict):
    """
    Генерация SQL запросов для создания демо-таблиц
    :return: кортеж из строк-таблиц
    """

    managers_table = """
        CREATE TABLE IF NOT EXISTS managers (
            manager_id INT AUTO_INCREMENT PRIMARY KEY,
            manager_fio VARCHAR(32) UNIQUE,
            login VARCHAR(32),
            password VARCHAR(128)
        )
    """

    customers_table = f"""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT UNSIGNED NOT NULL,
            last_name VARCHAR(32),
            first_name VARCHAR(32),
            middle_name VARCHAR(32),
            birth DATE,
            taxpayer_id BIGINT UNSIGNED,
            manager_fio VARCHAR(32),
            status ENUM{tuple(status_constants.values())},
            FOREIGN KEY (manager_fio) REFERENCES managers(manager_fio)
        )
    """
    return managers_table, customers_table


def get_sql_for_insert_rows():
    """
    Генерация SQL-запросов для массовой вставки данных в созданные таблицы
    :return: кортеж из 4 строк с запросами
    """
    managers = "INSERT INTO managers (manager_fio, login, password) VALUES (%s, %s, %s)"
    customers = "INSERT INTO customers (account_id, last_name, first_name, middle_name, birth, taxpayer_id, manager_fio, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    return managers, customers


def get_initial_data(status_constants, lim: int = 10):
    """
    Генерация демо данных для наполнения таблиц
    :param lim: лимит объема генерации
    :return: 2 кортежа с демо-данными
    """
    # отдельно генерация менеджеров
    managers = [{'fio': f'{get_random_name(3, 6)} {get_random_name(5, 10)}'} for _ in range(1, 4)]

    # Генерация данных для таблицы с менеджерами
    managers_data = [
        (
            manager['fio'],                                             # manager_fio
            f"aton.{manager['fio'].split()[1]}",     # login
            hash_it('admin')                                            # password (хэш)
        )
        for manager in managers
    ]

    # Генерация данных для таблицы с клиентами
    customers_data = [
        (
            randint(10**8, 10**9),                                      # account_id
            get_random_name(5, 10),                                     # last_name
            get_random_name(3, 6),                                      # first_name
            get_random_name(3, 6),                                      # middle_name
            date(randint(1950, 2005), randint(1, 12), randint(1, 28)),  # birth
            randint(10**11, 10**12),                                    # taxpayer_id
            manager['fio'],                                             # manager_fio
            # choice(tuple(status_constants.values())),                 # status
            status_constants['running'],                                # status
        )
        for manager in managers
        for _ in range(randint(3, lim))
    ]
    #
    return managers_data, customers_data
