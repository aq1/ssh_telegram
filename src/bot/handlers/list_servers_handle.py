from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from .utils import handler
from ...config import config


@handler
def list_servers_handle(update: Update, _: CallbackContext):
    conf = config.read_config()
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
