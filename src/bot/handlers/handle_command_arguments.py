from telegram import Update
from telegram.ext import CallbackContext

from .utils import handler, execute_command
from ...config import config


@handler
def handle_command_arguments(update: Update, context: CallbackContext):
    try:
        server = context.user_data['server']
        command = context.user_data['command']
        arguments = context.user_data['arguments']
    except KeyError:
        raise ValueError('Выберите сервер и команду')

    conf = config.read_config()
    command_config = conf['commands'][command]
    next_index = len(context.user_data['arguments'])
    if next_index >= len(command_config.get('arguments', [])):
        result = execute_command(
            conf=conf,
            server=server,
            command=command_config['command'],
            arguments=arguments,
        )
        update.effective_message.reply_markdown_v2(text=f'`{result.strip()}`')
        return
