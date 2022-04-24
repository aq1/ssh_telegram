import io

import telegram
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
)
from telegram.ext import (
    CallbackContext,
    Filters,
)

from ..config import read_config, write_config


def get_config(update: Update) -> dict:
    error, config = read_config()
    if error:
        update.effective_message.reply_text(
            f'Не удалось прочитать конфиг\n{error}'
        )
    return config


def handle_server_connect(update: Update, _: CallbackContext):
    query = update.callback_query
    query.answer()

    update.effective_message.reply_text(
        text=f'{query.data}: подключён',
    )


def handle_servers_response(update: Update, _: CallbackContext):
    config = get_config(update)
    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)]
        for name, _ in config['servers'].items()
    ]
    update.effective_message.reply_text(
        'Доступные сервера:',
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


def handle_config_upload(update: Update, context: CallbackContext):
    if 'yaml' not in update.effective_message.effective_attachment.mime_type:
        return update.message.reply_html(
            'Неизвестный формат файла. Поддерживается только yaml',
        )

    buffer = io.BytesIO()
    update.effective_message.effective_attachment.get_file().download(out=buffer)
    write_config(buffer)

    get_config(update)
    update.effective_message.reply_text(text='Конфиг обновлен')


handlers = [
    telegram.ext.CallbackQueryHandler(
        handle_server_connect,
    ),
    telegram.ext.CommandHandler(
        'start',
        handle_servers_response,
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
