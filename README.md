### Зависимости

- Python 3.9

### Перед первым запуском

`pip install -r requirements.txt`

### Запуск
`python main.py токен_бота`

Например `python main.py 300000003:OOFM3_zeJzaA44d13T23KASkKKjXXdgSSTc`

Или `export TOKEN="300000003:OOFM3_zeJzaA44d13T23KASkKKjXXdgSSTc"; python main.py $TOKEN`


### После первого запуска
Нужно загрузить в бота файл конфига со списком серверов и команд

### Конфиг
В файле example_config.yaml представлен пример конфига.
path, servers и commands нужно обязательно заполнить.
Чтобы обновить конфиг просто отправьте боту YAML файл. Или замените файл config.yaml в корне проекта рядом с example_config.yaml
