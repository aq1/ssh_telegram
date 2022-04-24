import io
from typing import Any

import telegram
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
    Filters,
)

from .. import config, ssh


def handler(func):
    def _f(update: Update, context: CallbackContext) -> Any:
        try:
            return func(update, context)
        except Exception as e:
            update.effective_message.reply_text(
                f'Не удалось выполнить команду\n{e}'
            )

    return _f


def get_config() -> dict:
    error, conf = config.read_config()
    if error:
        raise ValueError(error)
    return conf


@handler
def handle_server_connect(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    conf = get_config()
    server_name = context.match.groups()[0]
    server = conf['servers'][server_name]

    ssh.connect(**server)
    context.user_data['server_name'] = server_name

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'command_{name}')]
        for name, _ in conf['commands'].items()
    ]

    update.effective_message.reply_text(
        text=f'{server_name}: подключён',
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@handler
def handle_command(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if 'server_name' not in context.user_data:
        raise ValueError('Выберите на каком сервере выполнить команду.')

    conf = get_config()
    command_name = context.match.groups()[0]
    command = conf['servers'][command_name]

    ssh.connect(**server)
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'command_{name}')]
        for name, _ in conf['commands'].items()
    ]

    update.effective_message.reply_text(
        text=f'{server_name}: подключён',
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@handler
def list_servers_handle(update: Update, _: CallbackContext):
    conf = get_config()
    if not conf:
        return
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'server_{name}')]
        for name, _ in conf['servers'].items()
    ]
    update.effective_message.reply_text(
        'Доступные сервера:',
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


@handler
def handle_config_upload(update: Update, _: CallbackContext):
    if 'yaml' not in update.effective_message.effective_attachment.mime_type:
        return update.message.reply_html(
            'Неизвестный формат файла. Поддерживается только yaml',
        )

    buffer = io.BytesIO()
    update.effective_message.effective_attachment.get_file().download(out=buffer)
    config.write_config(buffer)

    get_config()
    update.effective_message.reply_text(text='Конфиг обновлен')
    list_servers_handle(update, _)


handlers = [
    telegram.ext.CallbackQueryHandler(
        handle_server_connect,
        pattern=r'server_(.+)',
    ),
    telegram.ext.CommandHandler(
        'start',
        list_servers_handle,
    ),
    telegram.ext.MessageHandler(
        filters=Filters.attachment,
        callback=handle_config_upload,
    )
]


def start_bot():
    bot = telegram.Bot(token='370803882:AAFM3_zeJzaAKyd0uTLVKn5kJDjNNdgttTc')
    print(f'{bot.first_name} started')
    updater = telegram.ext.Updater(
        bot=bot,
        use_context=True,
    )

    list(map(updater.dispatcher.add_handler, handlers))

    updater.start_polling(
        drop_pending_updates=True,
        timeout=5,
        poll_interval=0.5,
    )
