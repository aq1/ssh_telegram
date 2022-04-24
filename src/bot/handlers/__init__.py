import telegram.ext
from telegram.ext import Filters

from .handle_command_arguments import handle_command_arguments
from .handle_command_select import handle_command_select
from .handle_config_upload import handle_config_upload
from .handle_server_connect import handle_server_connect
from .list_servers_handle import list_servers_handle
from .handle_execute_command import handle_execute_command

handlers = [
    telegram.ext.CallbackQueryHandler(
        handle_server_connect,
        pattern=r'server_(.+)',
    ),
    telegram.ext.CallbackQueryHandler(
        handle_command_select,
        pattern=r'command_(.+)',
    ),
    telegram.ext.CallbackQueryHandler(
        handle_execute_command,
        pattern=r'execute',
    ),
    telegram.ext.CallbackQueryHandler(
        handle_command_arguments,
        pattern=r'arguments_(.+)',
    ),
    telegram.ext.CommandHandler(
        'start',
        list_servers_handle,
    ),
    telegram.ext.MessageHandler(
        filters=Filters.attachment,
        callback=handle_config_upload,
    ),
    telegram.ext.MessageHandler(
        filters=Filters.text,
        callback=handle_command_arguments,
    ),
]
