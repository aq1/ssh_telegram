import datetime
import io

from paramiko.channel import ChannelFile
from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from .utils import handler, execute_command, get_arguments, clean_user_data
from ...config import config


@handler
def handle_execute_command(update: Update, context: CallbackContext):
    server, command, arguments = get_arguments(context)
    conf: dict = config.read_config()
    command_config: dict = conf['commands'][command]

    result: ChannelFile = execute_command(
        conf=conf,
        server=server,
        command=command_config['command'],
        arguments=arguments,
    )
    clean_user_data(context)

    buffer = io.BytesIO()
    buffer.write(result.read())
    buffer.seek(0)

    now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
    update.effective_chat.send_document(
        document=buffer,
        filename=f'{server}_{command_config["command"]}_{now}.txt',
        reply_markup=None,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
