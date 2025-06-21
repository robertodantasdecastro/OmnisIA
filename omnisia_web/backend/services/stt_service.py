from pathlib import Path
import whisper


def transcribe_audio(audio: Path, model_size: str = "base") -> str:
    """Transcreve áudio usando Whisper"""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(str(audio))
        return result["text"]
    except Exception as e:
        raise Exception(f"Erro na transcrição de áudio: {str(e)}")
