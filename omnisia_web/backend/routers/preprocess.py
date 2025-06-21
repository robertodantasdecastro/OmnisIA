from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from ..services import ocr_service, stt_service, video_service

router = APIRouter()


class OCRRequest(BaseModel):
    pdf_path: str
    output_path: str


@router.post("/ocr-pdf")
async def ocr_pdf(req: OCRRequest):
    ocr_service.ocr_pdf(Path(req.pdf_path), Path(req.output_path))
    return {"output": req.output_path}


class STTRequest(BaseModel):
    audio_path: str
    model_size: str = "base"


@router.post("/transcribe")
async def transcribe(req: STTRequest):
    text = stt_service.transcribe_audio(Path(req.audio_path), req.model_size)
    return {"text": text}


class VideoRequest(BaseModel):
    video_path: str


@router.post("/transcribe-video")
async def transcribe_video(req: VideoRequest):
    text = video_service.transcribe_video(Path(req.video_path))
    return {"text": text}
