import asyncio
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes, CallbackContext

from src.downloader import getMedia

def get_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎶 Audio", callback_data="audio"),
                InlineKeyboardButton("📹 Video", callback_data="video"),
            ],
            [
                InlineKeyboardButton("❌ Annulla", callback_data="annulla"),
            ],
        ]
    )

def get_resolution_video() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("360p", callback_data="360"),
                InlineKeyboardButton("480p", callback_data="480"),
                InlineKeyboardButton("720p", callback_data="720"),
            ],
            [
                InlineKeyboardButton("❌ Annulla", callback_data="annulla"),
            ],
        ]
    )

#Qui la logica della gesione dei bottoni relativi alla scelta delle risoluzioni video.
async def handle_resolution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query:
        await query.answer()

        if query.data == "annulla":
            context.user_data.clear()
            await query.edit_message_text("Operazione annullata.")
            return

        elif query.data == "360":
            context.user_data["video_resolution"] = 360
        elif query.data == "480":
            context.user_data["video_resolution"] = 480
        elif query.data == "720":
            context.user_data["video_resolution"] = 720

        await handle_download(update, context)


#Qui la logica della gestione dei bottoni relativa alla scelta del tipo di media da scaricare.
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query :

        await query.answer()

        if query.data == "annulla":
            context.user_data.clear()
            await query.edit_message_text("Operazione annullata.")
            return

        elif query.data == "audio":
            context.user_data["download_audio"] = True
            context.user_data["download_video"] = False
            await handle_download(update, context)
            await query.edit_message_text("Scaricherai un mp3")

        elif query.data == "video":
            context.user_data["download_video"] = True
            context.user_data["download_audio"] = False
            await query.edit_message_text(
                "Scaricherai un mp4", reply_markup=get_resolution_video()
            )


async def handle_download(update: Update, context: CallbackContext) -> None:

    await update.callback_query.edit_message_text("⏳ Download in corso...")

    #Se è impostato a true facciamo iniziare il download audio e passiamo come video resolution None.
    if context.user_data.get("download_audio"):
        file_path = await asyncio.to_thread(getMedia, context.user_data["url"], None, "mp3")
    #Se è impostato a true facciamo iniziare il download video e passiamo come video resolution la risoluzione del video scelta.
    elif context.user_data.get("download_video"):
        file_path = await asyncio.to_thread(getMedia, context.user_data["url"], context.user_data["video_resolution"], "mp4")
    else :
        return

    if file_path and os.path.exists(file_path):
        try:
            await context.bot.send_message(chat_id=update.callback_query.message.chat.id, text="😎 Caricamento su Telegram in corso!")
            await context.bot.send_document(
                chat_id=update.callback_query.message.chat.id,
                document=open(file_path, 'rb')
            )
            os.remove(file_path)  # elimina dopo l'invio
        except Exception as e:
            await context.bot.send_message(chat_id=update.callback_query.message.chat.id, text="Errore invio file!")
    else:
        await context.bot.send_message(chat_id=update.callback_query.message.chat.id, text="Download fallito.")


