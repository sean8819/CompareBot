from unittest.mock import MagicMock, patch

import yt_dlp

from src.downloader import build_ydl_opts, get_media


def test_mp3_format():
    opts = build_ydl_opts(720, "mp3")
    assert opts["format"] == "bestaudio/best"


def test_mp3_merge_format():
    opts = build_ydl_opts(720, "mp3")
    assert opts["merge_output_format"] == "mp3"


def test_mp4_format_contiene_risoluzione():
    opts = build_ydl_opts(1080, "mp4")
    assert "1080" in opts["format"]


def test_mp4_merge_format():
    opts = build_ydl_opts(1080, "mp4")
    assert opts["merge_output_format"] == "mp4"


def test_mp4_risoluzione_720():
    opts = build_ydl_opts(720, "mp4")
    assert "720" in opts["format"]


def test_mp4_risoluzione_480():
    opts = build_ydl_opts(480, "mp4")
    assert "480" in opts["format"]


def test_noplaylist_sempre_attivo():
    opts = build_ydl_opts(720, "mp4")
    assert opts["noplaylist"] is True


def test_ffmpeg_path():
    opts = build_ydl_opts(720, "mp4")
    assert opts["ffmpeg_location"] == "/usr/bin/ffmpeg"


def test_outtmpl_contiene_download_dir():
    opts = build_ydl_opts(720, "mp4")
    assert "downloads" in opts["outtmpl"]


def test_outtmpl_contiene_template_titolo():
    opts = build_ydl_opts(720, "mp4")
    assert "%(title)s" in opts["outtmpl"]


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
    mock_ydl_class.return_value.__enter__.side_effect = yt_dlp.utils.DownloadError("Network error")
    result = get_media("https://url-non-valido.com", 720, "mp4")
    assert result == "error"
