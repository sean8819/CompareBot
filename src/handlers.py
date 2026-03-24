# pylint: disable=unused-argument

from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu()-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
            InlineKeyboardButton("🎶 Audio", callback_data="audio"),
            InlineKeyboardButton("📹 Video", callback_data="video"),
        ],
        [
            InlineKeyboardButton("❌ Annulla", callback_data="annulla"),
        ],
    ])

def get_resolution_video()-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
            InlineKeyboardButton("360p", callback_data="360"),
            InlineKeyboardButton("480p", callback_data="480"),
            InlineKeyboardButton("720p", callback_data="720"),
        ],
        [
            InlineKeyboardButton("❌ Annulla", callback_data="annulla"),
        ],
    ])

# la logica vera sta qui
async def handle_resolution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "annulla":
        await query.edit_message_text("Operazione annullata.")

    elif query.data == "360":
        await query.edit_message_text("Scaricherai un video a 360p")

    elif query.data == "480":
        await query.edit_message_text("Scaricherai un video a 480p")

    elif query.data == "720":
        await query.edit_message_text("Scaricherai un video a 720p")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "annulla":
        await query.edit_message_text("Operazione annullata.")

    elif query.data == "audio":
        await query.edit_message_text("Scaricherai un mp3")

    elif query.data == "video":
        await query.edit_message_text("Scaricherai un mp4", reply_markup=get_resolution_video())

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
        await update.message.reply_text("Ciao, scarica il tuo contenuto!", reply_markup=get_main_menu())


async def beauty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("Ciao, bellezza del giorno!")
