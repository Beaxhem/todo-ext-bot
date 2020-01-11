import os

from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from handlers import start, add, add_confirm, add_task, delete, delete_id, delete_confirm, error, finish, show
from handlers_index import *

TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT", "8443")


def main():

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex("^Add task$"), add),
                MessageHandler(Filters.regex('^Delete task$'), delete),
                MessageHandler(Filters.regex("^Show tasks$"), show)
            ],
            ADD: [
                MessageHandler(Filters.text, add_task)
            ],
            ADD_CONFIRM: [
                MessageHandler(Filters.regex("^(Yes|No)$"), add_confirm)
            ],
            DELETE: [
                MessageHandler(Filters.text, delete_id)
            ],
            DELETE_CONFIRM:[MessageHandler(Filters.text, delete_confirm)]

        },
        fallbacks=[
            MessageHandler(Filters.regex("^Delete my data"), finish)
        ]
    )

    dp.add_handler(handler)
    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://todo-ext-bot.herokuapp.com/" + TOKEN)

    updater.idle()


if __name__ == "__main__":
    main()
