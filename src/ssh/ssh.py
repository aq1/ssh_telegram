from paramiko.client import AutoAddPolicy, SSHClient


def connect(**arguments) -> SSHClient:
    if 'password' in arguments:
        arguments['password'] = str(arguments['password'])

    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(**arguments)
    return client


def execute(client: SSHClient, command: str) -> (str, str, str):
    _, out, err = client.exec_command(command)
    return out.read().decode('utf8'), err.read().decode('utf8')
