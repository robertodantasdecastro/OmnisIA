from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from pathlib import Path
from ..services import ocr_service, stt_service, video_service
from ..config import WHISPER_MODELS
import os

router = APIRouter()


class OCRRequest(BaseModel):
    pdf_path: str
    output_path: str

    @validator("pdf_path")
    def validate_pdf_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Arquivo PDF não encontrado: {v}")
        if not v.lower().endswith(".pdf"):
            raise ValueError("Arquivo deve ser um PDF")
        return v


@router.post("/ocr-pdf")
async def ocr_pdf(req: OCRRequest):
    """Extrai texto de PDF usando OCR"""
    try:
        output_path = ocr_service.ocr_pdf(Path(req.pdf_path), Path(req.output_path))
        return {"output": str(output_path), "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no OCR: {str(e)}")


class STTRequest(BaseModel):
    audio_path: str
    model_size: str = "base"

    @validator("audio_path")
    def validate_audio_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Arquivo de áudio não encontrado: {v}")
        return v

    @validator("model_size")
    def validate_model_size(cls, v):
        if v not in WHISPER_MODELS:
            raise ValueError(f"Tamanho do modelo deve ser um de: {WHISPER_MODELS}")
        return v


@router.post("/transcribe")
async def transcribe(req: STTRequest):
    """Transcreve áudio para texto"""
    try:
        text = stt_service.transcribe_audio(Path(req.audio_path), req.model_size)
        return {"text": text, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na transcrição: {str(e)}")


class VideoRequest(BaseModel):
    video_path: str

    @validator("video_path")
    def validate_video_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Arquivo de vídeo não encontrado: {v}")
        return v


@router.post("/transcribe-video")
async def transcribe_video(req: VideoRequest):
    """Transcreve vídeo para texto"""
    try:
        text = video_service.transcribe_video(Path(req.video_path))
        return {"text": text, "status": "success"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro na transcrição de vídeo: {str(e)}"
        )


@router.post("/ocr-image")
async def ocr_image(image_path: str):
    """Extrai texto de imagem usando OCR"""
    try:
        if not os.path.exists(image_path):
            raise HTTPException(
                status_code=400, detail=f"Imagem não encontrada: {image_path}"
            )

        text = ocr_service.ocr_image(Path(image_path))
        return {"text": text, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no OCR da imagem: {str(e)}")
