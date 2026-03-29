# pylint: disable=unused-argument

import validators
from telegram import Update
from telegram.ext import ContextTypes

import src.messages as message
from src.buttons import get_main_menu
from src.core.beauty import handle_beauty
from src.core.i18n import get_string, set_user_language


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if update.message and user:
        set_user_language(user.id, "en")
        await update.message.reply_text(
            f"{get_string(user, 'hello')} {user.first_name} {get_string(user, 'compare')}"
        )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        user = update.effective_user

        if not user:
            await update.message.reply_text(
                "Hello user.\n\nProject info.",
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            return

        info = message.getAboutString(user)
        await update.message.reply_text(
            f"{get_string(user, 'hello')} {user.first_name}\n\n{info}",
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:

        user = update.effective_user

        if not user:
            await update.message.reply_text(
                "Hello user.\n\nServices info.",
                parse_mode="HTML",
            )
            return

        services = message.getServiceString(user)
        await update.message.reply_text(
            f"{get_string(user, 'hello')} {user.first_name}.\n\n{services}",
            parse_mode="HTML",
        )


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    if not user:
        return

    parts = update.message.text.split(" ", 1)

    if len(parts) != 2:
        await update.message.reply_text(get_string(user, "download_params_error"))
        return

    url_video = parts[1]

    if validators.url(url_video):
        if context.user_data is None:
            return

        context.user_data["url"] = url_video

        await update.message.reply_text(
            f"{user.first_name}, {get_string(user, 'download_content')}",
            reply_markup=get_main_menu(user),
        )


async def beauty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    user = update.effective_user

    raw_text = update.message.text.strip()
    command = raw_text.split()[0]

    if raw_text != command:
        await update.message.reply_text(get_string(user, "beauty_params_error"))
        return

    await handle_beauty(update)


async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    if not user:
        return

    parts = update.message.text.split(" ", 1)

    if len(parts) != 2:
        error_message = get_string(user, "lang_format_error")
        await update.message.reply_text(error_message)
        return

    requested_lang = parts[1].strip().lower()

    if requested_lang not in ["it", "en"]:
        await update.message.reply_text(get_string(user, "language_not_supported"))
        return

    set_user_language(user.id, requested_lang)

    confirmation_message = get_string(user, "lang_updated")

    await update.message.reply_text(confirmation_message)
