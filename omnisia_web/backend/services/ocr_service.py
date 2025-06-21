from pathlib import Path
import ocrmypdf
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import logging
from ..config import DEFAULT_OCR_LANGUAGE, TESSERACT_CONFIG

logger = logging.getLogger("omnisia.ocr")


def ocr_pdf(pdf_path: Path, output_path: Path, language: str = None) -> Path:
    """Extrai texto de um PDF usando OCR"""
    try:
        lang = language or DEFAULT_OCR_LANGUAGE
        logger.info(f"Processando PDF {pdf_path} com idioma {lang}")

        # Configura opções do OCR
        ocr_options = {
            "language": lang,
            "output_type": "pdf",
            "deskew": True,
            "remove_background": True,
            "clean": True,
            "force_ocr": True,
        }

        ocrmypdf.ocr(str(pdf_path), str(output_path), **ocr_options)
        logger.info(f"OCR concluído: {output_path}")

        return output_path
    except Exception as e:
        logger.error(f"Erro no OCR do PDF: {str(e)}")
        raise Exception(f"Erro no OCR do PDF: {str(e)}")


def ocr_image(image_path: Path, language: str = None) -> str:
    """Extrai texto de uma imagem usando OCR"""
    try:
        lang = language or DEFAULT_OCR_LANGUAGE
        logger.info(f"Processando imagem {image_path} com idioma {lang}")

        # Abre e processa a imagem
        img = Image.open(image_path)

        # Converte para RGB se necessário
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Configura o Tesseract
        config = TESSERACT_CONFIG

        # Extrai texto
        text = pytesseract.image_to_string(img, lang=lang, config=config)

        logger.info(f"OCR concluído. Texto extraído: {len(text)} caracteres")
        return text.strip()

    except Exception as e:
        logger.error(f"Erro no OCR da imagem: {str(e)}")
        raise Exception(f"Erro no OCR da imagem: {str(e)}")


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrai texto de um PDF (sem OCR, apenas texto já presente)"""
    try:
        logger.info(f"Extraindo texto existente do PDF: {pdf_path}")

        text = ""
        doc = fitz.open(str(pdf_path))

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            text += f"\n--- Página {page_num + 1} ---\n{page_text}\n"

        doc.close()

        logger.info(f"Texto extraído: {len(text)} caracteres")
        return text.strip()

    except Exception as e:
        logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")


def preprocess_image_for_ocr(image_path: Path, output_path: Path = None) -> Path:
    """Pré-processa imagem para melhorar OCR"""
    try:
        from PIL import ImageEnhance, ImageFilter

        logger.info(f"Pré-processando imagem: {image_path}")

        # Abre imagem
        img = Image.open(image_path)

        # Converte para escala de cinza
        img = img.convert("L")

        # Aumenta contraste
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        # Aumenta nitidez
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.5)

        # Aplica filtro para reduzir ruído
        img = img.filter(ImageFilter.MedianFilter())

        # Define caminho de saída
        if not output_path:
            output_path = (
                image_path.parent / f"{image_path.stem}_processed{image_path.suffix}"
            )

        # Salva imagem processada
        img.save(output_path, optimize=True, quality=95)

        logger.info(f"Imagem pré-processada salva em: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Erro no pré-processamento: {str(e)}")
        raise Exception(f"Erro no pré-processamento: {str(e)}")


def get_supported_languages() -> list:
    """Retorna lista de idiomas suportados pelo Tesseract"""
    try:
        langs = pytesseract.get_languages(config="")
        return sorted(langs)
    except Exception as e:
        logger.warning(f"Não foi possível obter idiomas do Tesseract: {str(e)}")
        return ["eng", "por"]  # Fallback


def validate_language(language: str) -> bool:
    """Valida se o idioma é suportado"""
    try:
        supported = get_supported_languages()

        # Verifica idiomas combinados (ex: por+eng)
        if "+" in language:
            langs = language.split("+")
            return all(lang in supported for lang in langs)
        else:
            return language in supported

    except Exception:
        return True  # Em caso de erro, assume que é válido
