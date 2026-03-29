from unittest.mock import AsyncMock, MagicMock

import pytest

from src.buttons import get_main_menu
from src.handlers import about, download, service, start


@pytest.mark.asyncio
async def test_start():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user.first_name = "Erika"

    await start(update, context)

    update.message.reply_text.assert_called_once_with(
        "Hello Erika your trusty buddy is here to help you download your media!"
    )


@pytest.mark.asyncio
async def test_about():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()

    mock_user = MagicMock()
    mock_user.first_name = "Erika"
    update.effective_user = mock_user

    await about(update, context)

    expected_text = (
        "Hello Erika\n\n"
        "⚡️ <b>Video Downloader Bot</b>\n"
        "Download your favorite videos from YouTube and other services in seconds.\n\n"
        "Created and maintained by the team:\n"
        "👨‍💻 Gianmarco [<a href='https://github.com/sean8819'>@sean8819</a>]\n"
        "👨‍💻 Marce [<a href='https://github.com/Marss08'>@Marss08</a>]\n"
        "👨‍💻 Enzo [<a href='https://github.com/enzobarba'>@enzobarba</a>]\n\n"
        "❤️ Thank you for choosing our bot!"
    )

    update.message.reply_text.assert_called_once_with(
        expected_text, parse_mode="HTML", disable_web_page_preview=True
    )


@pytest.mark.asyncio
async def test_service():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user.first_name = "Erika"

    await service(update, context)

    expected_text = (
        "Hello Erika.\n\n"
        "🛠 <b>My services</b>\n\n"
        "📥 <b>Media Download:</b> Send a link to easily download videos or audio tracks from YouTube and other supported services.\n\n"
        "🌍 <b>Multilingual (i18n):</b> Native support for Italian and English.\n\n"
        "🌅 <b>Daily Inspiration:</b> Receive the <i>beauty photo of the day</i> for a daily touch of wonder.\n\n"
    )

    update.message.reply_text.assert_called_once_with(expected_text, parse_mode="HTML")


@pytest.mark.asyncio
async def test_download_no_message():
    update = MagicMock()
    context = MagicMock()
    update.message = None

    await download(update, context)


@pytest.mark.asyncio
async def test_download_no_url():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.message.text = "/download"

    await download(update, context)

    update.message.reply_text.assert_called_once_with(
        "You need to format your message like this: /download <url>"
    )


@pytest.mark.asyncio
async def test_download_invalid_url():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.message.text = "/download url-non-valido"

    await download(update, context)

    update.message.reply_text.assert_not_called()


@pytest.mark.asyncio
async def test_download_valid_url():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.message.text = "/download https://www.youtube.com/watch?v=xxx"
    update.effective_user.first_name = "Erika"
    context.user_data = {}

    await download(update, context)

    assert context.user_data["url"] == "https://www.youtube.com/watch?v=xxx"
    update.message.reply_text.assert_called_once_with(
        "Erika, download your content!",
        reply_markup=get_main_menu(update.effective_user),
    )


@pytest.mark.asyncio
async def test_about_no_user():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user = None

    await about(update, context)

    update.message.reply_text.assert_called_once_with(
        "Hello user.\n\nProject info.", parse_mode="HTML", disable_web_page_preview=True
    )


@pytest.mark.asyncio
async def test_service_no_user():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user = None

    await service(update, context)

    update.message.reply_text.assert_called_once_with(
        "Hello user.\n\nServices info.", parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_download_no_user():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.message.text = "/download https://www.youtube.com/watch?v=xxx"
    update.effective_user = None
    context.user_data = {}

    await download(update, context)

    update.message.reply_text.assert_not_called()
