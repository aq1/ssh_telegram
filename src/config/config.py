import io

import yaml

CONFIG_PATH = 'config.yaml'


def read_config() -> (str, dict):
    with open(CONFIG_PATH) as f:
        config = yaml.load(f, yaml.Loader)

    error = ''
    if 'servers' not in config or 'commands' not in config:
        error = 'Обязательны поля servers и commands'

    return error, config


def write_config(data: io.BytesIO) -> None:
    with open(CONFIG_PATH, 'wb') as f:
        data.seek(0)
        f.write(data.read())
