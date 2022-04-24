import io

from telegram import Update
from telegram.ext import CallbackContext

from .list_servers_handle import list_servers_handle
from .utils import handler
from ...config import config


@handler
def handle_config_upload(update: Update, _: CallbackContext):
    if 'yaml' not in update.effective_message.effective_attachment.mime_type:
        return update.message.reply_html(
            'Неизвестный формат файла. Поддерживается только yaml',
        )

    buffer = io.BytesIO()
    update.effective_message.effective_attachment.get_file().download(out=buffer)
    config.write_config(buffer)

    config.read_config()

    update.effective_message.reply_text(text='Конфиг обновлен')
    list_servers_handle(update, _)
