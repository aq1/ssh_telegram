from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext

from .utils import handler, clean_user_data, get_arguments
from ...config import config


@handler
def handle_command_arguments(update: Update, context: CallbackContext):
    query_data = ''
    if update.callback_query:
        query_data = update.callback_query.data

    server, command, arguments = get_arguments(context)

    conf: dict = config.read_config()
    command_config: dict = conf['commands'][command]
    arguments_config: list[str] = command_config.get('arguments', [])

    if query_data == 'arguments_empty':
        arguments.append('')

    if query_data == 'arguments_back':
        arguments.pop()

    if query_data == 'arguments_cancel':
        clean_user_data(context)
        update.effective_message.edit_text(text='Выполнение команды отменено')
        return

    if not query_data and update.effective_message.text:
        arguments.append(update.effective_message.text)

    if len(arguments) >= len(arguments_config):
        command = ' '.join([command_config['command']] + arguments)
        keyboard = [
            [InlineKeyboardButton(f'Выполнить {command_config["command"]}', callback_data='execute')],
            [InlineKeyboardButton('Отменить выполнение команды', callback_data='arguments_cancel')],
        ]
        update.effective_message.edit_text(
            f'Выполнить команду `{command}`\nна сервере `{server}`?',
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return

    keyboard = [
        [InlineKeyboardButton('Оставить пустым', callback_data='arguments_empty')],
        [InlineKeyboardButton('Отменить выполнение команды', callback_data='arguments_cancel')],
    ]

    if len(arguments) != 0:
        keyboard.append([
            InlineKeyboardButton('Изменить предыдущий параметр', callback_data='arguments_back'),
        ])

    update.effective_message.edit_text(
        f'Введите значение аргумента *{arguments_config[len(arguments)]}*',
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
