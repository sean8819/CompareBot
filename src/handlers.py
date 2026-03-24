# pylint: disable=unused-argument

from telegram import Update
from telegram.ext import ContextTypes


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
        await update.message.reply_text("Ciao, scarica il tuo contenuto!")


async def beauty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Ciao, bellezza del giorno!")
