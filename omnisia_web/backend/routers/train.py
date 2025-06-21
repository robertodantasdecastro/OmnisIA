from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from pathlib import Path
from ..services import lora_trainer
from ..config import SUPPORTED_MODELS
import os

router = APIRouter()


class TrainRequest(BaseModel):
    model_name: str
    dataset_path: str
    output_dir: str

    @validator("dataset_path")
    def validate_dataset_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Dataset não encontrado: {v}")
        return v

    @validator("model_name")
    def validate_model_name(cls, v):
        if v not in SUPPORTED_MODELS:
            raise ValueError(
                f"Modelo não suportado. Modelos aceitos: {SUPPORTED_MODELS}"
            )
        return v


@router.post("/")
async def train(req: TrainRequest):
    """Treina modelo usando LoRA"""
    try:
        # Cria diretório de saída se não existir
        output_path = Path(req.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        lora_trainer.train_lora(req.model_name, Path(req.dataset_path), output_path)
        return {
            "output_dir": req.output_dir,
            "status": "success",
            "message": "Treinamento concluído com sucesso",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no treinamento: {str(e)}")


@router.get("/models")
async def list_supported_models():
    """Lista modelos suportados para treinamento"""
    models = [
        {"name": "gpt2", "description": "GPT-2 Small (124M parameters)"},
        {"name": "gpt2-medium", "description": "GPT-2 Medium (355M parameters)"},
        {"name": "gpt2-large", "description": "GPT-2 Large (774M parameters)"},
        {"name": "gpt2-xl", "description": "GPT-2 XL (1.5B parameters)"},
        {"name": "microsoft/DialoGPT-small", "description": "DialoGPT Small"},
        {"name": "microsoft/DialoGPT-medium", "description": "DialoGPT Medium"},
        {"name": "microsoft/DialoGPT-large", "description": "DialoGPT Large"},
    ]
    return {"models": models}
