import os

import yt_dlp

DOWNLOAD_DIR = "./tmp/downloads"


def build_ydl_opts(video_resolution: int | None, media_type: str) -> dict:
    if media_type == "mp3":
        ydl_format = "bestaudio/best"
        merge_format = "mp3"
    else:
        ydl_format = f"bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]"
        merge_format = "mp4"

    return {
        "format": ydl_format,
        "merge_output_format": merge_format,
        "ffmpeg_location": "/usr/bin/ffmpeg",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": False,
        "noplaylist": True,
    }


def get_media(video_url: str, video_resolution: int | None, media_type: str) -> str:
    ydl_opts = build_ydl_opts(video_resolution, media_type)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path
    except (yt_dlp.utils.DownloadError, yt_dlp.utils.ExtractorError):
        return "error"
