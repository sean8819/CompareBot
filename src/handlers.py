# pylint: disable=unused-argument
import validators
from telegram import Update
from telegram.ext import ContextTypes

from src.buttons import get_main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if update.message and update.effective_user:
        await update.message.reply_text(
            f"Ciao, {update.effective_user.first_name} il tuo compare di fiducia ti aiuta a scaricare i tuoi media!"
        )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Ciao informazioni sul progetto")


async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text('Ciao, {"Stato dei servizi"}!')


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:

        parts = update.message.text.split(" ", 1)

        if len(parts) != 2:
            await update.message.reply_text(
                "Devi fornire un messaggio così formato /download <url risorsa>"
            )
            return

        url_video = parts[1]

        # Verifico se è un url ben formato.
        if validators.url(url_video):

            context.user_data["url"] = url_video

            await update.message.reply_text(
                "Ciao, scarica il tuo contenuto!", reply_markup=get_main_menu()
            )


async def beauty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Ciao, bellezza del giorno!")
