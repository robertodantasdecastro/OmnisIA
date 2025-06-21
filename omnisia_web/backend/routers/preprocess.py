from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator, Field
from pathlib import Path
from ..services import ocr_service, stt_service, video_service
from ..config import (
    WHISPER_MODELS,
    DEFAULT_WHISPER_MODEL,
    OCR_LANGUAGES,
    DEFAULT_OCR_LANGUAGE,
    get_upload_path,
    is_file_allowed,
)
import os
import logging
from typing import Optional

router = APIRouter()
logger = logging.getLogger("omnisia.preprocess")


class OCRRequest(BaseModel):
    file_path: str = Field(..., description="Caminho do arquivo para OCR")
    output_path: Optional[str] = Field(None, description="Caminho de saída (opcional)")
    language: Optional[str] = Field(DEFAULT_OCR_LANGUAGE, description="Idioma para OCR")

    @validator("file_path")
    def validate_file_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Arquivo não encontrado: {v}")

        # Verifica se é PDF ou imagem
        file_ext = Path(v).suffix.lower()
        if file_ext not in [".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]:
            raise ValueError(
                "Arquivo deve ser PDF ou imagem (jpg, jpeg, png, gif, bmp, tiff)"
            )

        return v

    @validator("language")
    def validate_language(cls, v):
        if v and not any(lang in v for lang in OCR_LANGUAGES):
            raise ValueError(f"Idioma deve conter um dos suportados: {OCR_LANGUAGES}")
        return v or DEFAULT_OCR_LANGUAGE


class STTRequest(BaseModel):
    audio_path: str = Field(..., description="Caminho do arquivo de áudio")
    model_size: str = Field(
        DEFAULT_WHISPER_MODEL, description="Tamanho do modelo Whisper"
    )
    language: Optional[str] = Field(None, description="Idioma do áudio (opcional)")

    @validator("audio_path")
    def validate_audio_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Arquivo de áudio não encontrado: {v}")

        # Verifica extensão de áudio
        file_ext = Path(v).suffix.lower()
        if file_ext not in [".mp3", ".wav", ".m4a", ".flac", ".ogg"]:
            raise ValueError("Arquivo deve ser de áudio (mp3, wav, m4a, flac, ogg)")

        return v

    @validator("model_size")
    def validate_model_size(cls, v):
        if v not in WHISPER_MODELS:
            raise ValueError(f"Tamanho do modelo deve ser um de: {WHISPER_MODELS}")
        return v


class VideoRequest(BaseModel):
    video_path: str = Field(..., description="Caminho do arquivo de vídeo")
    extract_audio: bool = Field(True, description="Extrair áudio do vídeo")
    model_size: str = Field(
        DEFAULT_WHISPER_MODEL, description="Tamanho do modelo Whisper"
    )

    @validator("video_path")
    def validate_video_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Arquivo de vídeo não encontrado: {v}")

        # Verifica extensão de vídeo
        file_ext = Path(v).suffix.lower()
        if file_ext not in [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"]:
            raise ValueError("Arquivo deve ser de vídeo (mp4, avi, mov, mkv, wmv, flv)")

        return v


@router.post("/ocr")
async def ocr_document(req: OCRRequest):
    """Extrai texto de documento usando OCR"""
    try:
        logger.info(f"Iniciando OCR do arquivo: {req.file_path}")

        file_path = Path(req.file_path)
        file_ext = file_path.suffix.lower()

        # Define caminho de saída se não fornecido
        if not req.output_path:
            output_path = file_path.parent / f"{file_path.stem}_ocr.txt"
        else:
            output_path = Path(req.output_path)

        # Processa baseado no tipo de arquivo
        if file_ext == ".pdf":
            # Para PDFs, usa ocrmypdf
            temp_pdf = file_path.parent / f"{file_path.stem}_ocr.pdf"
            ocr_service.ocr_pdf(file_path, temp_pdf, req.language)

            # Extrai texto do PDF processado
            text = ocr_service.extract_text_from_pdf(temp_pdf)

            # Remove arquivo temporário
            if temp_pdf.exists():
                temp_pdf.unlink()
        else:
            # Para imagens, usa pytesseract diretamente
            text = ocr_service.ocr_image(file_path, req.language)

        # Salva o texto extraído
        with output_path.open("w", encoding="utf-8") as f:
            f.write(text)

        logger.info(f"OCR concluído. Texto salvo em: {output_path}")

        return {
            "status": "success",
            "output_path": str(output_path),
            "text_length": len(text),
            "text_preview": text[:200] + "..." if len(text) > 200 else text,
            "language": req.language,
        }

    except Exception as e:
        logger.error(f"Erro no OCR: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro no OCR: {str(e)}")


@router.post("/transcribe")
async def transcribe_audio(req: STTRequest):
    """Transcreve áudio para texto usando Whisper"""
    try:
        logger.info(f"Iniciando transcrição do áudio: {req.audio_path}")

        # Transcreve o áudio
        result = stt_service.transcribe_audio(
            Path(req.audio_path), req.model_size, req.language
        )

        # Se result é string, converte para dict
        if isinstance(result, str):
            text = result
            language = req.language or "auto"
        else:
            text = result.get("text", "")
            language = result.get("language", req.language or "auto")

        logger.info(f"Transcrição concluída. Texto com {len(text)} caracteres")

        return {
            "status": "success",
            "text": text,
            "language": language,
            "model_used": req.model_size,
            "text_length": len(text),
            "audio_file": req.audio_path,
        }

    except Exception as e:
        logger.error(f"Erro na transcrição: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro na transcrição: {str(e)}")


@router.post("/transcribe-video")
async def transcribe_video(req: VideoRequest):
    """Transcreve vídeo para texto extraindo o áudio"""
    try:
        logger.info(f"Iniciando transcrição do vídeo: {req.video_path}")

        # Transcreve o vídeo
        result = video_service.transcribe_video(
            Path(req.video_path), req.model_size, req.extract_audio
        )

        # Se result é string, converte para dict
        if isinstance(result, str):
            text = result
            language = "auto"
        else:
            text = result.get("text", "")
            language = result.get("language", "auto")

        logger.info(f"Transcrição de vídeo concluída. Texto com {len(text)} caracteres")

        return {
            "status": "success",
            "text": text,
            "language": language,
            "model_used": req.model_size,
            "text_length": len(text),
            "video_file": req.video_path,
            "audio_extracted": req.extract_audio,
        }

    except Exception as e:
        logger.error(f"Erro na transcrição de vídeo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro na transcrição de vídeo: {str(e)}"
        )


@router.get("/models/whisper")
async def list_whisper_models():
    """Lista modelos Whisper disponíveis"""
    models_info = {
        "tiny": {"size": "~39 MB", "speed": "~32x", "accuracy": "Baixa"},
        "base": {"size": "~74 MB", "speed": "~16x", "accuracy": "Média"},
        "small": {"size": "~244 MB", "speed": "~6x", "accuracy": "Boa"},
        "medium": {"size": "~769 MB", "speed": "~2x", "accuracy": "Muito boa"},
        "large": {"size": "~1550 MB", "speed": "~1x", "accuracy": "Excelente"},
    }

    return {
        "models": [
            {
                "name": model,
                "info": models_info.get(model, {}),
                "is_default": model == DEFAULT_WHISPER_MODEL,
            }
            for model in WHISPER_MODELS
        ],
        "default_model": DEFAULT_WHISPER_MODEL,
    }


@router.get("/languages/ocr")
async def list_ocr_languages():
    """Lista idiomas suportados para OCR"""
    languages_info = {
        "por": "Português",
        "eng": "Inglês",
        "spa": "Espanhol",
        "fra": "Francês",
        "deu": "Alemão",
        "ita": "Italiano",
    }

    return {
        "languages": [
            {
                "code": lang,
                "name": languages_info.get(lang, lang.upper()),
                "is_default": lang in DEFAULT_OCR_LANGUAGE,
            }
            for lang in OCR_LANGUAGES
        ],
        "default_language": DEFAULT_OCR_LANGUAGE,
        "combined_example": "por+eng",
    }


@router.get("/supported-formats")
async def get_supported_formats():
    """Lista formatos de arquivo suportados"""
    return {
        "ocr": {
            "pdf": ["application/pdf"],
            "images": [
                "image/jpeg",
                "image/png",
                "image/gif",
                "image/bmp",
                "image/tiff",
            ],
        },
        "audio": {
            "formats": [
                "audio/mpeg",
                "audio/wav",
                "audio/m4a",
                "audio/flac",
                "audio/ogg",
            ],
            "extensions": [".mp3", ".wav", ".m4a", ".flac", ".ogg"],
        },
        "video": {
            "formats": ["video/mp4", "video/avi", "video/quicktime", "video/x-msvideo"],
            "extensions": [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
        },
    }
