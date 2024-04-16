import yaml
from dataclasses import dataclass


@dataclass
class SessionConfig:
    key: str = 'IT_COULD_BE_A_MORE_SECRET_STRING'


@dataclass
class DatabaseConfig:
    host: str = 'localhost'
    port: int = 3306
    user: str = 'user'
    password: str = 'password'
    database: str = 'database'

    def to_dict(self):
        return self.__dict__


@dataclass
class Config:
    session: SessionConfig
    database: DatabaseConfig


def get_configs(config_path: str = 'config.yml'):
    """
    Чтение и распарсинг yaml файла с данными конфига БД и секретом для сессий
    :param config_path: имя yaml файла
    :return: датакласс с данными
    """
    with open(config_path, mode='r') as f:
        raw_config = yaml.safe_load(f)

    return Config(
        session=SessionConfig(
            key=raw_config['session']['key']
        ),
        database=DatabaseConfig(
            host=raw_config['database']['host'],
            port=raw_config['database']['port'],
            user=raw_config['database']['user'],
            password=raw_config['database']['password'],
            database=raw_config['database']['database']
        )
    )

