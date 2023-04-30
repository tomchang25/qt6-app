###############################################################################
# Author: Greysuki
# License: MIT
# Description: This section of code has been modified from the original code.
###############################################################################
from __future__ import annotations

import validators
from yt_dlp import YoutubeDL
from pathlib import Path
import ffmpeg
import numpy as np

DEFAULT_DOWNLOAD_DIR = "download/"


def load_audio_from_url(url: str, verbose: bool = False, delete: bool = False) -> str:
    if not (isinstance(url, str) and validators.url(url)):
        raise ValueError(f'Invalid URL "{url}"')

    ydl_opts = {
        "format": "ba*",
        "quiet": not verbose,
        "outtmpl": str(Path(DEFAULT_DOWNLOAD_DIR) / "%(title)s.%(ext)s"),
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is None:
            raise RuntimeError(f'Failed to download media from "{url}"')

        download_filename = ydl.prepare_filename(info)

        audio = load_audio_from_file(download_filename)
        if delete:
            Path(download_filename).unlink()

        return audio


def load_audio_from_file(file: str, sr: int = 16000) -> np.ndarray:
    """
    Parameters
    ----------
    file: str
        The filepath to audio/video.
    sr: int
        The sample rate to resample the audio if necessary, hardcode from whisper.audio

    Returns
    -------
    A NumPy array containing the audio waveform, in float32 dtype.
    """

    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0


def load_audio(file_or_url: str) -> np.ndarray:
    """
    Load an audio/video file and read as mono waveform, resampling as necessary
    """
    if isinstance(file_or_url, str):
        if validators.url(file_or_url):
            return load_audio_from_url(file_or_url, delete=True)
        else:
            return load_audio_from_file(file_or_url)
    else:
        raise ValueError(f'Invalid file "{file_or_url}"')


if __name__ == "__main__":
    audio = load_audio(
        r"https://www.youtube.com/watch?v=kG8siPWHogU&ab_channel=%E8%8A%B1%E4%B8%B8%E3%81%AF%E3%82%8C%E3%82%8B%2FHareruHanamaru",
    )

    print(audio)
