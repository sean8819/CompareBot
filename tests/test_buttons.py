from unittest.mock import AsyncMock, MagicMock, mock_open, patch

import pytest
from telegram import InlineKeyboardMarkup
from telegram.error import TelegramError

from src.buttons import (
    get_main_menu,
    get_resolution_video,
    handle_buttons,
    handle_download,
    handle_resolution,
)


def test_get_main_menu():
    mock_user = MagicMock()
    mock_user.id = 12345
    menu = get_main_menu(mock_user)

    assert isinstance(menu, InlineKeyboardMarkup)
    assert len(menu.inline_keyboard) == 2
    assert menu.inline_keyboard[0][0].text == "🎶 Audio"
    assert menu.inline_keyboard[0][1].text == "📹 Video"
    assert menu.inline_keyboard[1][0].text == "❌ Cancel"


def test_get_resolution_video():
    mock_user = MagicMock()
    menu = get_resolution_video(mock_user)

    assert isinstance(menu, InlineKeyboardMarkup)
    assert len(menu.inline_keyboard) == 2
    assert menu.inline_keyboard[0][0].text == "360p"
    assert menu.inline_keyboard[0][1].text == "480p"
    assert menu.inline_keyboard[0][2].text == "720p"
    assert menu.inline_keyboard[1][0].text == "❌ Cancel"


@pytest.mark.asyncio
async def test_handle_resolution_annulla():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "annulla"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {"url": "https://youtube.com/watch?v=xxx"}

    await handle_resolution(update, context)

    assert context.user_data == {}
    update.callback_query.edit_message_text.assert_called_once_with(
        "Operation canceled."
    )


@pytest.mark.asyncio
async def test_handle_resolution_360():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "360"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}

    with patch("src.buttons.handle_download", new_callable=AsyncMock):
        await handle_resolution(update, context)
        assert context.user_data["video_resolution"] == 360


@pytest.mark.asyncio
async def test_handle_resolution_480():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "480"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}

    with patch("src.buttons.handle_download", new_callable=AsyncMock):
        await handle_resolution(update, context)
        assert context.user_data["video_resolution"] == 480


@pytest.mark.asyncio
async def test_handle_resolution_720():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "720"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}

    with patch(
        "src.buttons.handle_download", new_callable=AsyncMock
    ) as mock_handle_download:
        await handle_resolution(update, context)
        assert context.user_data["video_resolution"] == 720
        mock_handle_download.assert_called_once_with(update, context)


@pytest.mark.asyncio
async def test_handle_resolution_no_query():
    update = MagicMock()
    context = MagicMock()
    update.callback_query = None

    await handle_resolution(update, context)


@pytest.mark.asyncio
async def test_handle_buttons_no_query():
    update = MagicMock()
    context = MagicMock()
    update.callback_query = None

    await handle_buttons(update, context)


@pytest.mark.asyncio
async def test_handle_buttons_annulla():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "annulla"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {"url": "https://youtube.com/watch?v=xxx"}

    await handle_buttons(update, context)

    assert context.user_data == {}
    update.callback_query.edit_message_text.assert_called_once_with(
        "Operation canceled."
    )


@pytest.mark.asyncio
async def test_handle_buttons_audio():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "audio"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}

    with patch(
        "src.buttons.handle_download", new_callable=AsyncMock
    ) as mock_handle_download:
        await handle_buttons(update, context)
        assert context.user_data["download_audio"]
        assert not context.user_data["download_video"]
        mock_handle_download.assert_called_once_with(update, context)


@pytest.mark.asyncio
async def test_handle_buttons_video():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.data = "video"
    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {}

    await handle_buttons(update, context)

    assert context.user_data["download_video"]
    assert not context.user_data["download_audio"]
    update.callback_query.edit_message_text.assert_called_once_with(
        "You are about to download an mp4",
        reply_markup=get_resolution_video(update.effective_user),
    )


@pytest.mark.asyncio
async def test_handle_download_no_query():
    update = MagicMock()
    context = MagicMock()
    update.callback_query = None

    await handle_download(update, context)


@pytest.mark.asyncio
async def test_handle_download_no_message():
    update = MagicMock()
    context = MagicMock()
    update.callback_query.message = None

    await handle_download(update, context)


@pytest.mark.asyncio
async def test_handle_download_no_user_data():
    update = MagicMock()
    context = MagicMock()
    context.user_data = None

    await handle_download(update, context)


@pytest.mark.asyncio
async def test_handle_download_no_media_type():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {"url": "https://youtube.com/watch?v=xxx"}

    await handle_download(update, context)


@pytest.mark.asyncio
async def test_handle_download_file_too_large():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {
        "url": "https://youtube.com/watch?v=xxx",
        "download_audio": True,
    }

    with patch("src.buttons.get_media_size", return_value=100 * 1024 * 1024):
        await handle_download(update, context)
        update.callback_query.edit_message_text.assert_called_once_with(
            "❌ File too large for Telegram (max 50MB)."
        )


@pytest.mark.asyncio
async def test_handle_download_audio_success():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {
        "url": "https://youtube.com/watch?v=xxx",
        "download_audio": True,
    }
    context.bot.send_audio = AsyncMock()

    with patch("src.buttons.get_media_size", return_value=10 * 1024 * 1024), patch(
        "src.buttons.get_media", return_value="/tmp/audio.mp3"
    ), patch("os.path.exists", return_value=True), patch("os.remove"), patch(
        "builtins.open", mock_open(read_data="{}")
    ):
        await handle_download(update, context)
        context.bot.send_audio.assert_called_once()


@pytest.mark.asyncio
async def test_handle_download_video_success():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {
        "url": "https://youtube.com/watch?v=xxx",
        "download_video": True,
        "video_resolution": 720,
    }
    context.bot.send_video = AsyncMock()

    with patch("src.buttons.get_media_size", return_value=10 * 1024 * 1024), patch(
        "src.buttons.get_media", return_value="/tmp/video.mp4"
    ), patch("os.path.exists", return_value=True), patch("os.remove"), patch(
        "builtins.open", mock_open(read_data="{}")
    ):
        await handle_download(update, context)
        context.bot.send_video.assert_called_once()


@pytest.mark.asyncio
async def test_handle_download_failed():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {
        "url": "https://youtube.com/watch?v=xxx",
        "download_audio": True,
    }
    context.bot.send_message = AsyncMock()

    with patch("src.buttons.get_media_size", return_value=10 * 1024 * 1024), patch(
        "src.buttons.get_media", return_value="error"
    ), patch("os.path.exists", return_value=False), patch(
        "builtins.open", mock_open(read_data="{}")
    ):
        await handle_download(update, context)
        context.bot.send_message.assert_called_once_with(
            chat_id=update.callback_query.message.chat.id, text="Download failed."
        )


@pytest.mark.asyncio
async def test_handle_download_telegram_error():

    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {
        "url": "https://youtube.com/watch?v=xxx",
        "download_audio": True,
    }
    context.bot.send_audio = AsyncMock(side_effect=TelegramError("errore"))
    context.bot.send_message = AsyncMock()

    with patch("src.buttons.get_media_size", return_value=10 * 1024 * 1024), patch(
        "src.buttons.get_media", return_value="/tmp/audio.mp3"
    ), patch("os.path.exists", return_value=True), patch("os.remove"), patch(
        "builtins.open", mock_open(read_data="{}")
    ):
        await handle_download(update, context)
        context.bot.send_message.assert_called_once_with(
            chat_id=update.callback_query.message.chat.id, text="Error sending file!"
        )


@pytest.mark.asyncio
async def test_handle_download_os_error_on_remove():
    update = MagicMock()
    context = MagicMock()

    update.callback_query.answer = AsyncMock()
    update.callback_query.edit_message_text = AsyncMock()
    context.user_data = {
        "url": "https://youtube.com/watch?v=xxx",
        "download_audio": True,
    }
    context.bot.send_audio = AsyncMock()
    context.bot.send_message = AsyncMock()

    with patch("src.buttons.get_media_size", return_value=10 * 1024 * 1024), patch(
        "src.buttons.get_media", return_value="/tmp/audio.mp3"
    ), patch("os.path.exists", return_value=True), patch(
        "os.remove", side_effect=OSError("errore")
    ), patch(
        "builtins.open", mock_open(read_data="{}")
    ):
        await handle_download(update, context)
        context.bot.send_message.assert_called_once_with(
            chat_id=update.callback_query.message.chat.id,
            text="Error removing file!",
        )
