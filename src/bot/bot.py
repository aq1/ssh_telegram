import telegram
import telegram.ext

from .handlers import handlers


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
        poll_interval=1,
    )
