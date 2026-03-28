import asyncio
import os
from datetime import date, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

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


def _set_file_mtime(path, timestamp: float) -> None:
    os.utime(path, (timestamp, timestamp))
