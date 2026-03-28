import os
from unittest.mock import MagicMock, patch

import yt_dlp

from src.downloader import DOWNLOAD_DIR, build_ydl_opts, get_media, get_media_size


# N.B Utilizzo il prefisso di un uid 05adfd95 ... perchè ogni download avrà come prefisso un identificativo univoco.
def test_mp3_format():
    opts = build_ydl_opts(720, "mp3", "05adfd95 ...")
    assert opts["format"] == "bestaudio/best"


def test_mp3_merge_format():
    opts = build_ydl_opts(720, "mp3", "05adfd95 ...")
    assert opts["merge_output_format"] == "mp3"


def test_mp4_format_contain_resolution():
    opts = build_ydl_opts(1080, "mp4", "05adfd95 ...")
    assert "1080" in opts["format"]


def test_mp4_merge_format():
    opts = build_ydl_opts(1080, "mp4", "05adfd95 ...")
    assert opts["merge_output_format"] == "mp4"


def test_mp4_resolution_720():
    opts = build_ydl_opts(720, "mp4", "05adfd95 ...")
    assert "720" in opts["format"]


def test_mp4_resolution_480():
    opts = build_ydl_opts(480, "mp4", "05adfd95 ...")
    assert "480" in opts["format"]


def test_no_playlist_always_active():
    opts = build_ydl_opts(720, "mp4", "05adfd95 ...")
    assert opts["noplaylist"] is True


def test_ffmpeg_path():
    opts = build_ydl_opts(720, "mp4", "05adfd95 ...")
    assert opts["ffmpeg_location"] == "/usr/bin/ffmpeg"


def test_outtmpl_contains_download_dir():
    opts = build_ydl_opts(720, "mp4", "05adfd95 ...")
    assert "downloads" in opts["outtmpl"]


def test_outtmpl_contains_template_titolo():
    opts = build_ydl_opts(720, "mp4", "05adfd95 ...")
    assert (
        os.path.join(DOWNLOAD_DIR, f"{"05adfd95 ..."}.%(title)s.%(ext)s")
        in opts["outtmpl"]
    )


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_getMedia_get_filepath(mock_ydl_class):
    mock_ydl = MagicMock()
    mock_ydl.extract_info.return_value = {"title": "video", "ext": "mp4"}
    mock_ydl.prepare_filename.return_value = "/downloads/video.mp4"
    mock_ydl_class.return_value.__enter__.return_value = mock_ydl

    result = get_media("https://youtube.com/watch?v=xxx", 720, "mp4")
    assert result == "/downloads/video.mp4"


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_getMedia_extract_info(mock_ydl_class):
    mock_ydl = MagicMock()
    mock_ydl.extract_info.return_value = {"title": "video", "ext": "mp4"}
    mock_ydl.prepare_filename.return_value = "/downloads/video.mp4"
    mock_ydl_class.return_value.__enter__.return_value = mock_ydl

    get_media("https://youtube.com/watch?v=xxx", 720, "mp4")
    mock_ydl.extract_info.assert_called_once_with(
        "https://youtube.com/watch?v=xxx", download=True
    )


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_getMedia_get_error_on_exception(mock_ydl_class):
    mock_ydl_class.return_value.__enter__.return_value.extract_info.side_effect = (
        yt_dlp.utils.DownloadError("Network error")
    )

    result = get_media("https://luoutube.com/watch?v=xxx", 720, "mp4")
    assert result == "error"


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_get_media_size_returns_zero_on_error(mock_ydl_class):
    mock_ydl_class.return_value.__enter__.return_value.extract_info.side_effect = (
        yt_dlp.utils.DownloadError("errore")
    )

    result = get_media_size("https://youtube.com/watch?v=xxx", 720, "mp4")
    assert result == 0


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_get_media_size_returns_correct_size(mock_ydl_class):

    fileSize = 1024 * 1024 * 10

    mock_ydl_class.return_value.__enter__.return_value.extract_info.return_value = {
        "filesize": fileSize,
        "filesize_approx": None,
    }

    result = get_media_size("https://youtube.com/watch?v=xxx", 720, "mp4")
    assert result == fileSize


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_get_media_size_returns_zero_when_filesize_not_int(mock_ydl_class):
    mock_ydl_class.return_value.__enter__.return_value.extract_info.return_value = {
        "filesize": None,
        "filesize_approx": None,
    }

    result = get_media_size("https://youtube.com/watch?v=xxx", 720, "mp4")
    assert result == 0


@patch("src.downloader.yt_dlp.YoutubeDL")
def test_get_media_size_returns_zero_when_info_is_none(mock_ydl_class):
    mock_ydl_class.return_value.__enter__.return_value.extract_info.return_value = None

    result = get_media_size("https://youtube.com/watch?v=xxx", 720, "mp4")
    assert result == 0
