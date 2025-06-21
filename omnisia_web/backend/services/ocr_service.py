from pathlib import Path
from ingestao.ocr import ocr_pdf as run_ocr_pdf, ocr_image as run_ocr_image


def ocr_pdf(pdf: Path, output: Path) -> Path:
    return run_ocr_pdf(pdf, output)


def ocr_image(image: Path) -> str:
    return run_ocr_image(image)
