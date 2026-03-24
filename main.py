import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler

from src.handlers import about, beauty, download, service, start, handle_resolution
from src.logo import print_logo

from telegram.ext import CallbackQueryHandler
from src.handlers import handle_buttons


def main():

    load_dotenv()

    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("service", service))
    app.add_handler(CommandHandler("beauty", beauty))
    app.add_handler(CallbackQueryHandler(handle_buttons, pattern="^(audio|video|annulla)$"))
    app.add_handler(CallbackQueryHandler(handle_resolution, pattern="^(360|480|720|annulla)$"))


    print_logo()
    print("Bot avviato correttamente...\nIn attesa di messagg...!")

    app.run_polling()


if __name__ == "__main__":
    main()
