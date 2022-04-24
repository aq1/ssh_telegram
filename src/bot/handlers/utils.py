from typing import Any

from telegram import Update
from telegram.ext import CallbackContext

from ... import ssh


def handler(func):
    def _f(update: Update, context: CallbackContext) -> Any:
        try:
            return func(update, context)
        except Exception as e:
            update.effective_message.reply_text(
                f'Не удалось выполнить команду\n{e}'
            )

    return _f


def execute_command(
        conf: dict,
        server: str,
        command: str,
        arguments: list[str],
) -> str:
    client = ssh.connect(**conf['servers'][server])
    return ssh.execute(
        client=client,
        path=conf['path'],
        command=' '.join([command] + arguments),
    )
