import asyncio
import os
from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import requests

from src import beauty


def test_is_beauty_image_fresh_returns_false_when_file_does_not_exist(tmp_path):
    path = tmp_path / "missing.png"

    assert beauty.is_beauty_image_fresh(path, today=date(2026, 3, 28)) is False


def test_is_beauty_image_fresh_returns_true_for_file_from_same_day(tmp_path):
    path = tmp_path / "beauty.png"
    path.write_bytes(b"image")

    today = date.today()
    _set_file_mtime(path, datetime.combine(today, datetime.min.time()).timestamp())

    assert beauty.is_beauty_image_fresh(path, today=today) is True


def test_is_beauty_image_fresh_returns_false_for_file_from_previous_day(tmp_path):
    path = tmp_path / "beauty.png"
    path.write_bytes(b"image")

    today = date.today()
    yesterday = today - timedelta(days=1)
    _set_file_mtime(path, datetime.combine(yesterday, datetime.min.time()).timestamp())

    assert beauty.is_beauty_image_fresh(path, today=today) is False


def test_get_beauty_image_path_returns_cached_file_without_downloading(
    tmp_path, monkeypatch
):
    path = tmp_path / "beauty.png"
    path.write_bytes(b"cached")
    monkeypatch.setattr(
        beauty, "is_beauty_image_fresh", lambda candidate: candidate == path
    )

    downloader = MagicMock()
    to_thread = AsyncMock()
    monkeypatch.setattr(beauty.asyncio, "to_thread", to_thread)

    result = asyncio.run(beauty.get_beauty_image_path(str(path), downloader))

    assert result == path
    downloader.assert_not_called()
    to_thread.assert_not_awaited()


def test_get_beauty_image_path_downloads_stale_file_in_thread(tmp_path, monkeypatch):
    path = tmp_path / "beauty.png"
    monkeypatch.setattr(beauty, "is_beauty_image_fresh", lambda candidate: False)

    downloader = MagicMock(return_value=str(path))
    to_thread = AsyncMock(return_value=str(path))
    monkeypatch.setattr(beauty.asyncio, "to_thread", to_thread)

    result = asyncio.run(beauty.get_beauty_image_path(str(path), downloader))

    assert result == path
    to_thread.assert_awaited_once_with(downloader, beauty.DEFAULT_QUERY, str(path))


def test_handle_beauty_replies_with_photo(monkeypatch, tmp_path):
    path = tmp_path / "beauty.png"
    path.write_bytes(b"image-content")

    message = MagicMock()
    message.reply_photo = AsyncMock()
    update = MagicMock(message=message)

    get_path = AsyncMock(return_value=path)
    monkeypatch.setattr(beauty, "get_beauty_image_path", get_path)

    asyncio.run(beauty.handle_beauty(update))

    message.reply_photo.assert_awaited_once()
    sent_photo = message.reply_photo.await_args.kwargs["photo"]
    assert sent_photo.name == str(path)


def test_handle_beauty_returns_when_download_fails(monkeypatch):
    message = MagicMock()
    message.reply_photo = AsyncMock()
    update = MagicMock(message=message)

    monkeypatch.setattr(beauty, "get_beauty_image_path", AsyncMock(return_value=None))

    asyncio.run(beauty.handle_beauty(update))

    message.reply_photo.assert_not_awaited()


def test_handle_beauty_returns_when_update_has_no_message(monkeypatch):
    update = MagicMock(message=None)

    get_path = AsyncMock()
    monkeypatch.setattr(beauty, "get_beauty_image_path", get_path)

    asyncio.run(beauty.handle_beauty(update))

    get_path.assert_not_awaited()


def test_get_beauty_image_path_returns_none_when_downloader_fails(
    monkeypatch, tmp_path
):
    path = tmp_path / "beauty.png"
    monkeypatch.setattr(beauty, "is_beauty_image_fresh", lambda candidate: False)

    downloader = MagicMock(return_value=None)
    to_thread = AsyncMock(return_value=None)
    monkeypatch.setattr(beauty.asyncio, "to_thread", to_thread)

    result = asyncio.run(beauty.get_beauty_image_path(str(path), downloader))

    assert result is None
    to_thread.assert_awaited_once_with(downloader, beauty.DEFAULT_QUERY, str(path))


def test_download_beauty_image_returns_none_without_api_key(monkeypatch):
    monkeypatch.setattr(beauty, "load_dotenv", MagicMock())
    monkeypatch.setattr(beauty.os, "getenv", lambda key: None)

    result = beauty.download_beauty_image()

    assert result is None


def test_download_beauty_image_returns_none_when_no_results(monkeypatch):
    monkeypatch.setattr(beauty, "load_dotenv", MagicMock())
    monkeypatch.setattr(beauty.os, "getenv", lambda key: "token")
    monkeypatch.setattr(beauty, "cerca_immagini_pixabay", lambda query, api_key: [])

    result = beauty.download_beauty_image()

    assert result is None


def test_download_beauty_image_returns_output_path_on_success(monkeypatch, tmp_path):
    output_path = tmp_path / "beauty.png"

    monkeypatch.setattr(beauty, "load_dotenv", MagicMock())
    monkeypatch.setattr(beauty.os, "getenv", lambda key: "token")
    monkeypatch.setattr(
        beauty,
        "cerca_immagini_pixabay",
        lambda query, api_key: ["https://img/1.png", "https://img/2.png"],
    )
    monkeypatch.setattr(beauty.random, "choice", lambda items: items[1])
    monkeypatch.setattr(beauty, "scarica_risorsa", lambda url, path: True)

    result = beauty.download_beauty_image(output_path=str(output_path))

    assert result == str(output_path)


def test_download_beauty_image_returns_none_when_resource_download_fails(monkeypatch):
    monkeypatch.setattr(beauty, "load_dotenv", MagicMock())
    monkeypatch.setattr(beauty.os, "getenv", lambda key: "token")
    monkeypatch.setattr(
        beauty, "cerca_immagini_pixabay", lambda query, api_key: ["https://img/1.png"]
    )
    monkeypatch.setattr(beauty.random, "choice", lambda items: items[0])
    monkeypatch.setattr(beauty, "scarica_risorsa", lambda url, path: False)

    result = beauty.download_beauty_image()

    assert result is None


def test_cerca_immagini_pixabay_returns_urls_on_success(monkeypatch):
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {"hits": [{"webformatURL": "https://img/1.png"}]}
    monkeypatch.setattr(beauty.requests, "get", lambda *args, **kwargs: response)

    result = beauty.cerca_immagini_pixabay("flowers", "token")

    assert result == ["https://img/1.png"]


def test_cerca_immagini_pixabay_returns_empty_list_on_error(monkeypatch):
    response = MagicMock()
    response.status_code = 500
    monkeypatch.setattr(beauty.requests, "get", lambda *args, **kwargs: response)

    result = beauty.cerca_immagini_pixabay("flowers", "token")

    assert result == []


def test_scarica_risorsa_writes_file_contents(monkeypatch, tmp_path):
    output_path = tmp_path / "downloads" / "beauty.png"

    response = MagicMock()
    response.__enter__.return_value = response
    response.iter_content.return_value = [b"chunk-1", b"", b"chunk-2"]
    response.raise_for_status.return_value = None
    monkeypatch.setattr(beauty.requests, "get", lambda *args, **kwargs: response)

    result = beauty.scarica_risorsa("https://img/1.png", str(output_path))

    assert result is True
    assert output_path.read_bytes() == b"chunk-1chunk-2"


def test_scarica_risorsa_returns_false_on_request_exception(monkeypatch, tmp_path):
    output_path = tmp_path / "downloads" / "beauty.png"

    monkeypatch.setattr(
        beauty.requests,
        "get",
        MagicMock(side_effect=requests.RequestException("network error")),
    )

    result = beauty.scarica_risorsa("https://img/1.png", str(output_path))

    assert result is False


def _set_file_mtime(path, timestamp: float) -> None:
    os.utime(path, (timestamp, timestamp))
