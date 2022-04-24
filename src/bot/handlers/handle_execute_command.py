from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from .utils import handler, execute_command, get_arguments, clean_user_data
from ...config import config


@handler
def handle_execute_command(update: Update, context: CallbackContext):
    server, command, arguments = get_arguments(context)
    conf: dict = config.read_config()
    command_config: dict = conf['commands'][command]

    result = execute_command(
        conf=conf,
        server=server,
        command=command_config['command'],
        arguments=arguments,
    )
    clean_user_data(context)
    update.effective_message.edit_text(
        text=f'`{result.strip()}`',
        reply_markup=None,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
