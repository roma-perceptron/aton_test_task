import utils
import mysql.connector
from flask import Flask
from typing import Union
from config import DatabaseConfig


class BaseManager:
    """ Базовый класс менеджера БД с общим функционалом для управления БД """
    def __init__(self, app: Flask, db_config: DatabaseConfig):
        self.app = app
        self.config = db_config.to_dict()
        self.connection = None
        self.cursor = None
        self.table_names = None
        self.status_constants = {'running': 'В работе', 'declined': 'Отказ', 'closed': 'Сделка закрыта'}
        self.status_constants_rus = {v: k for k, v in self.status_constants.items()}
        #
        self.connect()
        if self.connection:
            self.get_tables()

    def connect(self):
        """ Подключение к базе данных """
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor()

            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print(f"Успешное подключение к серверу MySQL ({db_info}): {self.connection.database}")
        except mysql.connector.Error as exp:
            print(f"Ошибка при подключении к базе данных: {exp}")

    def disconnect(self):
        """ Закрытие соединения """
        bd_name = self.connection.database
        if self.connection.is_connected():
            self.connection.close()
            print(f"Соединение с базой данных {bd_name} закрыто")

    def check_connections(self):
        """ Проверка соединения """
        if not self.connection:
            self.connect()

    def get_tables(self, silent=False):
        """
        Получение списка всех таблиц в базе данных
        :param silent: Отключение уведомлений в консоли
        :return: Список имен таблиц
        """
        self.check_connections()
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        tables = [table[0] for table in tables]
        self.table_names = tables

        if not silent:
            if tables:
                print(f'В Базе Данных {self.connection.database} существуют следующие таблицы:')
                for table in tables:
                    print('\t', table)
            else:
                print(f'База Данных {self.connection.database} пуста, нет ни одной таблицы..')
                self.make_initial_tables()
        #
        return tables

    def _drop_table(self, table_name):
        """
        Формирование SQL-запроса для удаления таблицы
        :param table_name: имя таблицы
        :return: Кортеж с флагом итога операции и выброшенным исключением (при возникновении)
        """
        try:
            query = f"DROP TABLE {table_name}"
            self.write_to_db(query)
            self.get_tables(silent=True)
            return True, None
        except Exception as exp:
            return False, exp

    def drop_tables(self):
        """ Удаление всех таблиц - очистка БД """
        self.check_connections()
        existing_tables = self.get_tables(silent=True)

        # удаляю в while цикле поочередно пробуя каждую таблицу (из-за связей и ограничений)
        # можно было просто в обратном порядке, но это не дает 100% гарантии
        while existing_tables:
            is_dropped, exp = self._drop_table(existing_tables[0])
            if is_dropped:
                existing_tables.pop(0)
            elif isinstance(exp, mysql.connector.errors.DatabaseError) and exp.errno == 3730:
                # это ошибка из-за неверной очереди удаления таблиц
                existing_tables.append(existing_tables.pop(0))
            else:
                # иная ошибка, пробрасываю наверх
                raise exp
            #
            self.connection.commit()

    def write_to_db__many(self, query: str, params: Union[None, list] = None):
        """
        Выполнение SQL для массовой записи строк
        :param query: Строка со SQL-запросом
        :param params: Параметры для массовой записи
        """
        self.check_connections()
        self.cursor.executemany(query, params)

    def write_to_db(self, query: str, params: Union[None, list, tuple] = None):
        """
        Выполнение SQL запроса и закрепление результата
        :param query: Строка со SQL-запросом
        :param params: Параметры (опционально)
        """
        self.check_connections()
        self.cursor.execute(query, params)
        self.connection.commit()

    def read_from_db(self, query: str, params: Union[None, list, tuple] = None):
        """
        Выполнение SQL запроса на выборку и возврат этих значений
        :param query: Строка со SQL-запросом
        :param params: Параметры запроса (при наличии)
        :return: список словарей с полученными данными в формате column:value
        """
        self.check_connections()
        self.cursor.execute(query, params)
        columns = [column[0] for column in self.cursor.description]
        data = self.cursor.fetchall()
        if data:
            data = [{col: val for col, val in zip(columns, row)} for row in data]
        return data

    def make_initial_tables(self):
        """ Наполнение БД первичными данными """
        self.check_connections()
        print('Создаю и наполняю демо-таблицы')
        for table, insert, data in zip(utils.get_initial_tables(self.status_constants),
                                       utils.get_sql_for_insert_rows(),
                                       utils.get_initial_data(self.status_constants)):
            self.write_to_db(table)
            self.write_to_db__many(insert, data)
        self.get_tables()


class Manager(BaseManager):
    """ Класс с верхнеуровневым функционалом для внесения """
    def __init__(self, app: Flask, db_config: DatabaseConfig):
        super().__init__(app, db_config)

    def get_customers(self, manager_fio: str = None):
        """ Выборка клиентов заданного менеджера / всех клиентов """
        if manager_fio:
            query = """
                SELECT * FROM customers
                WHERE manager_fio = %s
            """
            data = self.read_from_db(query, (manager_fio,))
        else:
            query = "SELECT * FROM customers"
            data = self.read_from_db(query)
        return data

    def update_status(self, customer_id, status):
        """ Перезапись значения статуса """
        query = """
            UPDATE customers
            SET status = %s
            WHERE customer_id = %s
        """
        try:
            self.write_to_db(query, (self.status_constants[status], customer_id))
        except mysql.connector.errors.DatabaseError:
            return {'ok': False}
        return {'ok': True, 'status_rus': self.status_constants[status]}

    def get_managers(self):
        """ Получение данных всех менеджеров """
        query = "SELECT * FROM managers"
        managers = self.read_from_db(query)
        return managers

    def authentication(self, login, password):
        """ Аутентификация по логину и паролю"""
        query = """
            SELECT * FROM managers
            WHERE login = %s
            AND password = %s
        """
        user = self.read_from_db(query, (login, password))
        if user:
            return user[0]
        else:
            return False
