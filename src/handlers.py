# pylint: disable=unused-argument

import validators
from telegram import Update
from telegram.ext import ContextTypes

from src.beauty import handle_beauty
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
    if not update.message or not update.message.text:
        return

    parts = update.message.text.split(" ", 1)

    if len(parts) != 2:
        await update.message.reply_text(
            "Devi fornire un messaggio così formato /download <url risorsa>"
        )
        return

    url_video = parts[1]

    # Verifico se è un url ben formato.
    if validators.url(url_video):

        if context.user_data is None:
            return

        context.user_data["url"] = url_video

        await update.message.reply_text(
            "Ciao, scarica il tuo contenuto!", reply_markup=get_main_menu()
        )


async def beauty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    raw_text = update.message.text.strip()
    command = raw_text.split()[0]

    if raw_text != command:
        await update.message.reply_text("Usa solo /beauty senza altri argomenti.")
        return

    await handle_beauty(update)
