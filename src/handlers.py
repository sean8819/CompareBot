# pylint: disable=unused-argument
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import yt_dlp
import validators
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

def getMedia(video_url: str, video_resolution: int, media_type: str) -> str | None:

    if media_type == "mp3":
        ydl_format = "bestaudio/best"
        merge_format = "mp3"
    else:
        ydl_format = f'bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]'
        merge_format = "mp4"

    ydl_opts = {
        'format': ydl_format,
        'merge_output_format': merge_format,  # Output format after merging
        'ffmpeg_location': "/usr/bin/ffmpeg",  # Path to ffmpeg executable
        'outtmpl': os.path.join("/home/gianmarco/PycharmProjects/CompareBot/downloads", '%(title)s.%(ext)s'),  # Output file naming template
        'quiet': False,  # Show download progress
        'noplaylist': True  # Download only one video if playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path  # restituisce il path reale del file
    except Exception as e:
        print(f'Errore durante il download!')
        return None

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

        await query.edit_message_text("⏳ Download in corso...")

        chat_id = query.message.chat.id
        file_path = getMedia(context.user_data["url"], context.user_data["video_resolution"], "mp4")

        if file_path and os.path.exists(file_path):
            try:
                await context.bot.send_message(chat_id=chat_id, text="Ecco il tuo file!")
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=open(file_path, 'rb')
                )
                os.remove(file_path)  # elimina dopo l'invio
            except Exception as e:
                await context.bot.send_message(chat_id=chat_id, text="Errore invio file!")
        else:
            await context.bot.send_message(chat_id=chat_id, text="Download fallito.")

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
            await query.edit_message_text("Scaricherai un mp3")

            #Todo Refactor

            await query.edit_message_text("⏳ Download in corso...")

            chat_id = query.message.chat.id
            file_path = getMedia(context.user_data["url"], None, "mp3")

            if file_path and os.path.exists(file_path):
                try:
                    await context.bot.send_message(chat_id=chat_id, text="Ecco il tuo file!")
                    await context.bot.send_document(
                        chat_id=chat_id,
                        document=open(file_path, 'rb')
                    )
                    os.remove(file_path)  # elimina dopo l'invio
                except Exception as e:
                    await context.bot.send_message(chat_id=chat_id, text="Errore invio file!")
            else:
                await context.bot.send_message(chat_id=chat_id, text="Download fallito.")

        elif query.data == "video":
            context.user_data["download_video"] = True
            await query.edit_message_text(
                "Scaricherai un mp4", reply_markup=get_resolution_video()
            )


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

        chat_id = update.effective_chat.id

        # Leggo il messaggio ed estraggo l'url dalla richiesta.
        #url_video = update.message.text.split(" ", 1)[1]

        parts = update.message.text.split(" ", 1)

        if len(parts) != 2:
            await update.message.reply_text("Devi fornire un messaggio così formato /download <url risorsa>")
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