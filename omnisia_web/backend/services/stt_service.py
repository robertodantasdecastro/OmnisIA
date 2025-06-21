from pathlib import Path
from ingestao.stt import transcribe_audio as run_transcribe


def transcribe_audio(audio: Path, model_size: str = "base") -> str:
    return run_transcribe(audio, model_size)
