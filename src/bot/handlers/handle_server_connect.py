from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from .utils import handler
from ...config import config
from ...ssh import ssh


@handler
def handle_server_connect(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    conf = config.read_config()
    server_name = context.match.groups()[0]
    server = conf['servers'][server_name]

    ssh.connect(**server)
    context.user_data['server'] = server_name

    keyboard = [
        [InlineKeyboardButton(name, callback_data=f'command_{name}')]
        for name, _ in conf['commands'].items()
    ]

    update.effective_message.reply_text(
        text=f'{server_name}: подключён',
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
