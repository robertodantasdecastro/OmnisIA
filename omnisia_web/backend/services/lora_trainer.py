from pathlib import Path
from modelos.treinamento import finetune
from datasets import load_dataset


def train_lora(model_name: str, dataset_path: Path, output_dir: Path) -> None:
    dataset = load_dataset("text", data_files=str(dataset_path))["train"]
    finetune(model_name, dataset, str(output_dir))
