"""Processamento de imagens com CLIP."""
from pathlib import Path
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel


class CLIPEncoder:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)

    def encode(self, image_path: Path) -> torch.Tensor:
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            emb = self.model.get_image_features(**inputs)
        return emb
