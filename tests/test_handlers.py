from unittest.mock import AsyncMock, MagicMock

import pytest

from src.buttons import get_main_menu
from src.handlers import about, download, service, start


@pytest.mark.asyncio
async def test_start():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user.first_name = (
        "Erika"
    )

    await start(update, context)

    update.message.reply_text.assert_called_once_with(
        "Ciao, Erika il tuo compare di fiducia ti aiuta a scaricare i tuoi media!"
    )


@pytest.mark.asyncio
async def test_about():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user.first_name = (
        "Erika"
    )

    await about(update, context)

    update.message.reply_text.assert_called_once_with(
        "Ciao, Erika informazioni sul progetto."
    )


@pytest.mark.asyncio
async def test_service():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user.first_name = "Erika"

    await service(update, context)

    update.message.reply_text.assert_called_once_with("Ciao, Erika stato dei servizi.")


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
        "Devi fornire un messaggio così formato /download <url risorsa>"
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
        "Erika, scarica il tuo contenuto!", reply_markup=get_main_menu()
    )


@pytest.mark.asyncio
async def test_about_no_user():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user = None

    await about(update, context)

    update.message.reply_text.assert_called_once_with(
        "Ciao, utente informazioni sul progetto."
    )


@pytest.mark.asyncio
async def test_service_no_user():
    update = MagicMock()
    context = MagicMock()

    update.message.reply_text = AsyncMock()
    update.effective_user = None

    await service(update, context)

    update.message.reply_text.assert_called_once_with("Ciao, utente stato dei servizi.")


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
