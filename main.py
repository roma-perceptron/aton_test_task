# main
import routes
import config
import manager
from flask import Flask


class Application(Flask):
    """
    Переопределяю базовый класс чтобы хранить внутри дополнительные объекты
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manager = None


def setup_app():
    """
    Создание экземпляра приложения и его настройка
    :return:
    """
    app = Application('ATON')

    # маршруты + представления
    routes.setup_routes(app=app)

    # загрузка параметров конфигураций
    configs = config.get_configs()

    # сессии
    app.secret_key = configs.session.key

    # настройка и подключение к БД
    app.manager = manager.Manager(app, configs.database)
    #
    return app


if __name__ == '__main__':
    print('New Version 1.8')
    flask_app = setup_app()
    flask_app.run(host='0.0.0.0', port=5000)
