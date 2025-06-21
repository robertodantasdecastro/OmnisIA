from pathlib import Path
import ocrmypdf
from PIL import Image
import pytesseract


def ocr_pdf(pdf: Path, output: Path) -> Path:
    """Extrai texto de um PDF usando OCR"""
    try:
        ocrmypdf.ocr(str(pdf), str(output), skip_text=True)
        return output
    except Exception as e:
        raise Exception(f"Erro no OCR do PDF: {str(e)}")


def ocr_image(image: Path) -> str:
    """Extrai texto de uma imagem usando OCR"""
    try:
        img = Image.open(image)
        text = pytesseract.image_to_string(img, lang="por+eng")
        return text
    except Exception as e:
        raise Exception(f"Erro no OCR da imagem: {str(e)}")
