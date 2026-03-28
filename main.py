import logging
import os

from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from src.buttons import handle_buttons, handle_resolution
from src.handlers import about, beauty, download, service, start
from src.logo import print_logo


# Altro modo per ignorare gli argomenti quando eseguiamo test del codice.
async def error_handler(_: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error("Eccezione:", exc_info=context.error)


async def post_init(application):
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Avvia il bot"),
            BotCommand("download", "Scarica un media"),
            BotCommand("service", "Servizi disponibili"),
            BotCommand("beauty", "Bellezza del giorno"),
            BotCommand("about", "Info sul progetto"),
        ]
    )


def main():

    load_dotenv()

    logging.basicConfig(level=logging.ERROR)

    app = (
        ApplicationBuilder()
        .token(os.getenv("BOT_TOKEN"))
        .concurrent_updates(256)
        .post_init(post_init)
        .build()
    )

    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("service", service))
    app.add_handler(CommandHandler("beauty", beauty))
    app.add_handler(
        CallbackQueryHandler(handle_buttons, pattern="^(audio|video|annulla)$")
    )
    app.add_handler(
        CallbackQueryHandler(handle_resolution, pattern="^(360|480|720|annulla)$")
    )

    print_logo()
    print("Bot avviato correttamente...\nIn attesa di messaggi ;) ...!")

    app.run_polling()


if __name__ == "__main__":
    main()
