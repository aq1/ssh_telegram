import io

import yaml

CONFIG_PATH = 'config.yaml'


def read_config() -> dict:
    try:
        with open(CONFIG_PATH) as f:
            config = yaml.load(f, yaml.Loader)
    except FileNotFoundError:
        raise ValueError('Конфиг не найден. Загрузите файл.')

    if 'servers' not in config or 'commands' not in config:
        raise ValueError('Обязательны поля servers и commands')

    return config


def write_config(data: io.BytesIO) -> None:
    with open(CONFIG_PATH, 'wb') as f:
        data.seek(0)
        f.write(data.read())
