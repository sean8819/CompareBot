import asyncio
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.error import TelegramError
from telegram.ext import CallbackContext, ContextTypes

from src.downloader import get_media, get_media_size
from src.i18n import get_string


def get_main_menu(user: User) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎶 Audio", callback_data="audio"),
                InlineKeyboardButton("📹 Video", callback_data="video"),
            ],
            [
                InlineKeyboardButton(
                    get_string(user, "cancel_button"), callback_data="annulla"
                ),
            ],
        ]
    )


def get_resolution_video(user: User) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("360p", callback_data="360"),
                InlineKeyboardButton("480p", callback_data="480"),
                InlineKeyboardButton("720p", callback_data="720"),
            ],
            [
                InlineKeyboardButton(
                    get_string(user, "cancel_button"), callback_data="annulla"
                ),
            ],
        ]
    )


# Qui la logica della gesione dei bottoni relativi alla scelta delle risoluzioni video.
async def handle_resolution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query:
        await query.answer()

        if query.data == "annulla":
            if context.user_data is not None:
                context.user_data.clear()
                await query.edit_message_text(
                    get_string(update.effective_user, "operation_canceled")
                )
                return

        elif query.data == "360":
            if context.user_data is not None:
                context.user_data["video_resolution"] = 360
        elif query.data == "480":
            if context.user_data is not None:
                context.user_data["video_resolution"] = 480
        elif query.data == "720":
            if context.user_data is not None:
                context.user_data["video_resolution"] = 720

        await handle_download(update, context)


# Qui la logica della gestione dei bottoni relativa alla scelta del tipo di media da scaricare.
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query:

        if query and context.user_data is not None:
            await query.answer()

            if query.data == "annulla":
                context.user_data.clear()
                await query.edit_message_text(
                    get_string(update.effective_user, "operation_canceled")
                )
                return

            if query.data == "audio":
                context.user_data["download_audio"] = True
                context.user_data["download_video"] = False
                await handle_download(update, context)
                await query.edit_message_text(
                    get_string(update.effective_user, "confirm_mp3_download")
                )

            elif query.data == "video":
                context.user_data["download_video"] = True
                context.user_data["download_audio"] = False
                user = update.effective_user
                if user is None:
                    return
                await query.edit_message_text(
                    get_string(update.effective_user, "confirm_mp4_download"),
                    reply_markup=get_resolution_video(user),
                )


async def handle_download(update: Update, context: CallbackContext) -> None:

    if not update.callback_query:
        return

    if not update.callback_query.message:
        return

    chat_id = update.callback_query.message.chat.id

    if context.user_data is not None:
        if context.user_data.get("download_audio"):
            media_type = "mp3"
            resolution = None
        elif context.user_data.get("download_video"):
            media_type = "mp4"
            resolution = context.user_data["video_resolution"]
        else:
            return

        telegram_max_upload_file = 50 * 1024 * 1024

        size = await asyncio.to_thread(
            get_media_size, context.user_data["url"], resolution, media_type
        )

        if size > telegram_max_upload_file:
            await update.callback_query.edit_message_text(
                get_string(update.effective_user, "file_too_large")
            )
            return

        await update.callback_query.edit_message_text(
            get_string(update.effective_user, "loading")
        )

        file_path = await asyncio.to_thread(
            get_media, context.user_data["url"], resolution, media_type
        )

        if file_path and os.path.exists(file_path):
            try:
                ext = os.path.splitext(file_path)

                if ext[1] == ".mp3":
                    with open(file_path, "rb") as f:
                        await context.bot.send_audio(
                            chat_id=chat_id,
                            audio=f,
                            read_timeout=300,
                            write_timeout=300,
                            connect_timeout=30,
                        )
                else:
                    with open(file_path, "rb") as f:
                        await context.bot.send_video(
                            chat_id=chat_id,
                            video=f,
                            read_timeout=300,
                            write_timeout=300,
                            connect_timeout=30,
                        )

            except TelegramError as e:
                print(e)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=get_string(update.effective_user, "error_sending_file"),
                )
            finally:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError:
                        await context.bot.send_message(
                            chat_id=chat_id,
                            text=get_string(
                                update.effective_user, "error_removing_file"
                            ),
                        )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=get_string(update.effective_user, "download_failed"),
            )
