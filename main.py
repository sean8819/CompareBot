import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler

from src.handlers import (
    about,
    beauty,
    download,
    handle_buttons,
    handle_resolution,
    service,
    start,
)
from src.logo import print_logo


def main():

    load_dotenv()

    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
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