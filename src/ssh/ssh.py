from paramiko.client import AutoAddPolicy, SSHClient


def connect(**arguments) -> SSHClient:
    if 'password' in arguments:
        arguments['password'] = str(arguments['password'])

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(**arguments)
    return client


def execute(client: SSHClient, path: str, command: str) -> str:
    _, out, err = client.exec_command(f'cd {path}; {command}')

    err = err.read().decode('utf8').strip()
    out = out.read().decode('utf8').strip()
    if err:
        raise ValueError(err or 'Нет вывода об ошибке')

    return out or 'Нет вывода команды'
