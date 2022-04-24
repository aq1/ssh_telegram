import sys

import telegram
import telegram.ext

from .handlers import handlers


def start_bot():
    try:
        token = sys.argv[1]
    except IndexError:
        print('Не введён токен бота')
        return

    bot = telegram.Bot(token=token)
    print(f'{bot.first_name} started')
    updater = telegram.ext.Updater(
        bot=bot,
        use_context=True,
        persistence=telegram.ext.PicklePersistence(filename='.bot_data'),
    )

    list(map(updater.dispatcher.add_handler, handlers))

    updater.start_polling(
        drop_pending_updates=True,
        timeout=5,
        poll_interval=1,
    )
