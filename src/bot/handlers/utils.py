from typing import Any

from paramiko.channel import ChannelFile
from telegram import Update
from telegram.ext import CallbackContext

from ... import ssh
from ...ssh import local


def handler(func):
    def _f(update: Update, context: CallbackContext) -> Any:
        try:
            query = update.callback_query
            if query:
                query.answer()
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
):
    if server == 'local':
        return local.execute(
            path=conf['path'],
            command=[command] + arguments,
        )

    client = ssh.connect(**conf['servers'][server])
    return ssh.execute(
        client=client,
        path=conf['path'],
        command=' '.join([command] + arguments),
    )


def clean_user_data(context: CallbackContext):
    for key in 'command', 'arguments':
        context.user_data.pop(key, None)


def get_arguments(context: CallbackContext) -> (str, str, list[str]):
    try:
        server = context.user_data['server']
        command = context.user_data['command']
        arguments = context.user_data['arguments']
    except KeyError:
        raise ValueError('Выберите сервер и команду')

    return server, command, arguments
