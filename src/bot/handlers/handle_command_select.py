from telegram import Update
from telegram.ext import CallbackContext

from .handle_command_arguments import handle_command_arguments
from .utils import handler
from ...config import config


@handler
def handle_command_select(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if 'server' not in context.user_data:
        raise ValueError('Выберите на каком сервере выполнить команду.')

    conf = config.read_config()
    command_name = context.match.groups()[0]
    try:
        conf['commands'][command_name]
    except KeyError:
        raise ValueError(f'Команда {command_name} не найдена')

    context.user_data['command'] = command_name
    context.user_data['arguments'] = []

    return handle_command_arguments(
        update,
        context,
    )
