from pathlib import Path
import whisper
import logging
from ..config import DEFAULT_WHISPER_MODEL

logger = logging.getLogger("omnisia.stt")

# Cache para modelos carregados
_loaded_models = {}


def get_model(model_size: str = None):
    """Carrega e retorna modelo Whisper (com cache)"""
    model_size = model_size or DEFAULT_WHISPER_MODEL

    if model_size not in _loaded_models:
        logger.info(f"Carregando modelo Whisper: {model_size}")
        try:
            _loaded_models[model_size] = whisper.load_model(model_size)
            logger.info(f"Modelo {model_size} carregado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo {model_size}: {str(e)}")
            raise Exception(f"Erro ao carregar modelo Whisper {model_size}: {str(e)}")

    return _loaded_models[model_size]


def transcribe_audio(
    audio_path: Path, model_size: str = None, language: str = None
) -> dict:
    """Transcreve áudio usando Whisper"""
    try:
        model_size = model_size or DEFAULT_WHISPER_MODEL
        logger.info(f"Transcrevendo áudio: {audio_path} com modelo {model_size}")

        # Carrega o modelo
        model = get_model(model_size)

        # Opções de transcrição
        options = {"fp16": False, "verbose": False}  # Melhor compatibilidade

        # Adiciona idioma se especificado
        if language:
            options["language"] = language

        # Transcreve o áudio
        result = model.transcribe(str(audio_path), **options)

        logger.info(f"Transcrição concluída. Texto: {len(result['text'])} caracteres")

        return {
            "text": result["text"].strip(),
            "language": result.get("language", language or "auto"),
            "segments": result.get("segments", []),
            "model_used": model_size,
            "audio_duration": get_audio_duration(audio_path),
        }

    except Exception as e:
        logger.error(f"Erro na transcrição de áudio: {str(e)}")
        raise Exception(f"Erro na transcrição de áudio: {str(e)}")


def transcribe_with_timestamps(
    audio_path: Path, model_size: str = None, language: str = None
) -> dict:
    """Transcreve áudio com timestamps detalhados"""
    try:
        model_size = model_size or DEFAULT_WHISPER_MODEL
        logger.info(f"Transcrevendo com timestamps: {audio_path}")

        model = get_model(model_size)

        options = {"fp16": False, "verbose": False, "word_timestamps": True}

        if language:
            options["language"] = language

        result = model.transcribe(str(audio_path), **options)

        # Processa segmentos com timestamps
        segments_with_timestamps = []
        for segment in result.get("segments", []):
            segment_data = {
                "id": segment.get("id"),
                "start": segment.get("start"),
                "end": segment.get("end"),
                "text": segment.get("text", "").strip(),
                "words": [],
            }

            # Adiciona palavras com timestamps se disponível
            if "words" in segment:
                for word in segment["words"]:
                    word_data = {
                        "word": word.get("word", "").strip(),
                        "start": word.get("start"),
                        "end": word.get("end"),
                        "probability": word.get("probability"),
                    }
                    segment_data["words"].append(word_data)

            segments_with_timestamps.append(segment_data)

        return {
            "text": result["text"].strip(),
            "language": result.get("language", language or "auto"),
            "segments": segments_with_timestamps,
            "model_used": model_size,
            "audio_duration": get_audio_duration(audio_path),
            "has_word_timestamps": True,
        }

    except Exception as e:
        logger.error(f"Erro na transcrição com timestamps: {str(e)}")
        raise Exception(f"Erro na transcrição com timestamps: {str(e)}")


def get_audio_duration(audio_path: Path) -> float:
    """Obtém duração do áudio em segundos"""
    try:
        import librosa

        duration = librosa.get_duration(filename=str(audio_path))
        return duration
    except ImportError:
        logger.warning("librosa não instalado, usando método alternativo")
        try:
            # Método alternativo usando ffprobe
            import subprocess

            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(audio_path),
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                return float(result.stdout.strip())
        except Exception:
            pass

        logger.warning("Não foi possível determinar duração do áudio")
        return 0.0
    except Exception as e:
        logger.warning(f"Erro ao obter duração do áudio: {str(e)}")
        return 0.0


def detect_language(audio_path: Path, model_size: str = None) -> dict:
    """Detecta o idioma do áudio"""
    try:
        model_size = model_size or DEFAULT_WHISPER_MODEL
        logger.info(f"Detectando idioma do áudio: {audio_path}")

        model = get_model(model_size)

        # Carrega apenas os primeiros 30 segundos para detecção
        audio = whisper.load_audio(str(audio_path))
        audio = whisper.pad_or_trim(audio)

        # Gera mel-spectrogram
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Detecta idioma
        _, probs = model.detect_language(mel)

        # Ordena por probabilidade
        detected_languages = [
            {"language": lang, "probability": float(prob)}
            for lang, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True)
        ]

        most_likely = detected_languages[0]

        logger.info(
            f"Idioma detectado: {most_likely['language']} ({most_likely['probability']:.2f})"
        )

        return {
            "detected_language": most_likely["language"],
            "confidence": most_likely["probability"],
            "all_languages": detected_languages[:5],  # Top 5
            "model_used": model_size,
        }

    except Exception as e:
        logger.error(f"Erro na detecção de idioma: {str(e)}")
        raise Exception(f"Erro na detecção de idioma: {str(e)}")


def get_model_info(model_size: str = None) -> dict:
    """Retorna informações sobre o modelo"""
    model_size = model_size or DEFAULT_WHISPER_MODEL

    model_info = {
        "tiny": {
            "parameters": "39M",
            "size": "~39 MB",
            "speed": "~32x realtime",
            "vram": "~1 GB",
            "accuracy": "Baixa",
        },
        "base": {
            "parameters": "74M",
            "size": "~74 MB",
            "speed": "~16x realtime",
            "vram": "~1 GB",
            "accuracy": "Média",
        },
        "small": {
            "parameters": "244M",
            "size": "~244 MB",
            "speed": "~6x realtime",
            "vram": "~2 GB",
            "accuracy": "Boa",
        },
        "medium": {
            "parameters": "769M",
            "size": "~769 MB",
            "speed": "~2x realtime",
            "vram": "~5 GB",
            "accuracy": "Muito boa",
        },
        "large": {
            "parameters": "1550M",
            "size": "~1550 MB",
            "speed": "~1x realtime",
            "vram": "~10 GB",
            "accuracy": "Excelente",
        },
    }

    return {
        "model": model_size,
        "info": model_info.get(model_size, {}),
        "is_loaded": model_size in _loaded_models,
    }


def clear_model_cache():
    """Limpa cache de modelos carregados"""
    global _loaded_models
    logger.info("Limpando cache de modelos Whisper")
    _loaded_models = {}
