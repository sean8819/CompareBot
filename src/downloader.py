import yt_dlp
import os


def getMedia(video_url: str, video_resolution: int, media_type: str) -> str | None:

    if media_type == "mp3":
        ydl_format = "bestaudio/best"
        merge_format = "mp3"
    else:
        ydl_format = f"bestvideo[height<={video_resolution}]+bestaudio/best[height<={video_resolution}]"
        merge_format = "mp4"

    ydl_opts = {
        "format": ydl_format,
        "merge_output_format": merge_format,  # Output format after merging
        "ffmpeg_location": "/usr/bin/ffmpeg",  # Path to ffmpeg executable
        "outtmpl": os.path.join(
            "/home/gianmarco/PycharmProjects/CompareBot/downloads", "%(title)s.%(ext)s"
        ),  # Output file naming template
        "quiet": False,  # Show download progress
        "noplaylist": True,  # Download only one video if playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            file_path = ydl.prepare_filename(info)
        return file_path  # restituisce il path reale del file
    except Exception as e:
        print(f"Errore durante il download!")
        return None
