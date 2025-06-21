from pathlib import Path
import subprocess
from .stt_service import transcribe_audio


def transcribe_video(video_path: Path) -> str:
    audio_path = video_path.with_suffix('.wav')
    subprocess.run([
        'ffmpeg', '-y', '-i', str(video_path), str(audio_path)
    ], check=True)
    return transcribe_audio(audio_path)
