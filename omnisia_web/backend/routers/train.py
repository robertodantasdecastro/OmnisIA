from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from ..services import lora_trainer

router = APIRouter()


class TrainRequest(BaseModel):
    model_name: str
    dataset_path: str
    output_dir: str


@router.post("/")
async def train(req: TrainRequest):
    lora_trainer.train_lora(req.model_name, Path(req.dataset_path), Path(req.output_dir))
    return {"output_dir": req.output_dir}
