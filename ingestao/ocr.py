"""Modulos de OCR usando Tesseract e ocrmypdf."""
from pathlib import Path
import subprocess


def ocr_pdf(pdf_path: Path, output_path: Path) -> Path:
    """Executa OCR em um PDF utilizando o `ocrmypdf`."""
    subprocess.run(["ocrmypdf", str(pdf_path), str(output_path)], check=True)
    return output_path


def ocr_image(image_path: Path) -> str:
    """Executa OCR em uma imagem com Tesseract."""
    result = subprocess.run(["tesseract", str(image_path), "stdout"], capture_output=True, check=True, text=True)
    return result.stdout
