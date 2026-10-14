"""
Local transcription using faster-whisper.
No Groq account or API key is required. The model is downloaded on first use
and cached only for the lifetime of the service unless a persistent cache is
configured. On a free CPU server, transcription can be slow.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
from typing import List, TypedDict


class WordTiming(TypedDict):
    word: str
    start: float
    end: float
    probability: float | None


def _extract_audio(source_path: str, out_wav: str) -> None:
    from .render import _configured_ffmpeg

    cmd = [
        _configured_ffmpeg(), "-y", "-i", source_path,
        "-ac", "1", "-ar", "16000", "-vn", out_wav,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg audio extraction failed:\n{proc.stderr[-2000:]}")


def transcribe_words(source_path: str, language: str | None = None) -> List[WordTiming]:
    """Transcribe audio locally with faster-whisper and return word timings.

    WHISPER_MODEL defaults to 'base' to keep RAM and CPU needs more modest.
    Set WHISPER_MODEL to 'tiny' for a faster/lighter first test.
    """
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError(
            "Local transcription dependency is missing. The service needs to be rebuilt "
            "with faster-whisper installed."
        ) from exc

    model_name = os.environ.get("WHISPER_MODEL", "base")
    cache_dir = os.environ.get("WHISPER_CACHE_DIR") or None
    # CPU/int8 is suitable for CPU-only hosting; avoid downloading the model at startup.
    model = WhisperModel(
        model_name,
        device="cpu",
        compute_type="int8",
        download_root=cache_dir,
    )

    with tempfile.TemporaryDirectory() as tmp:
        wav_path = os.path.join(tmp, "audio.wav")
        _extract_audio(source_path, wav_path)
        segments, _info = model.transcribe(
            wav_path,
            language=language or None,
            word_timestamps=True,
            vad_filter=True,
            beam_size=1,
        )
        words: List[WordTiming] = []
        for segment in segments:
            for item in (segment.words or []):
                token = (item.word or "").strip()
                if not token:
                    continue
                words.append({
                    "word": token,
                    "start": round(float(item.start), 3),
                    "end": round(float(item.end), 3),
                    "probability": round(float(item.probability), 4)
                    if item.probability is not None else None,
                })
        return words
