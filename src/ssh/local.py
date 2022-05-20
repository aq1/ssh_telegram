import io
import subprocess


def execute(path: str, command: list[str]):
    session = subprocess.Popen(command, cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = session.communicate()

    if err:
        raise ValueError(err.decode('utf8'))

    out_file = io.BytesIO()
    out_file.write(out)
    out_file.seek(0)
    return out_file
