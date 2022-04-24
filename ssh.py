from paramiko.client import AutoAddPolicy, SSHClient


def connect(**arguments) -> SSHClient:
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(**arguments)
    return client


def execute(client: SSHClient, command: str) -> (str, str, str):
    _, out, err = client.exec_command(command)
    return out.read().decode('utf8'), err.read().decode('utf8')
