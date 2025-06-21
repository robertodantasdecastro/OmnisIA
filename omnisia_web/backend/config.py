import os
from pathlib import Path
from typing import List

# Configurações do sistema
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / os.getenv("DATA_DIR", "data")
UPLOAD_DIR = DATA_DIR / os.getenv("UPLOAD_DIR", "uploads").replace("data/", "")
MODELS_DIR = DATA_DIR / os.getenv("MODELS_DIR", "models").replace("data/", "")
DATASETS_DIR = DATA_DIR / os.getenv("DATASETS_DIR", "datasets").replace("data/", "")
LOGS_DIR = BASE_DIR / os.getenv("LOGS_DIR", "logs")

# Cria diretórios se não existirem
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATASETS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configurações da API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
API_RETRY_ATTEMPTS = int(os.getenv("API_RETRY_ATTEMPTS", "3"))

# Configurações de upload
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # Converte para bytes
ALLOWED_EXTENSIONS = set(
    os.getenv(
        "SUPPORTED_FILE_EXTENSIONS",
        ".pdf,.txt,.jpg,.jpeg,.png,.gif,.mp3,.wav,.mp4,.avi,.mov",
    ).split(",")
)

# Configurações de modelos
DEFAULT_MODELS_STR = os.getenv(
    "DEFAULT_MODELS", "gpt2,gpt2-medium,microsoft/DialoGPT-small"
)
SUPPORTED_MODELS = DEFAULT_MODELS_STR.split(",")

# Configurações de Whisper
WHISPER_MODELS_STR = os.getenv("WHISPER_MODELS", "tiny,base,small,medium,large")
WHISPER_MODELS = WHISPER_MODELS_STR.split(",")
DEFAULT_WHISPER_MODEL = os.getenv("WHISPER_MODEL_SIZE", "base")

# Configurações de OCR
OCR_LANGUAGES_STR = os.getenv("OCR_LANGUAGES", "por,eng")
OCR_LANGUAGES = OCR_LANGUAGES_STR.split(",")
DEFAULT_OCR_LANGUAGE = os.getenv("DEFAULT_OCR_LANGUAGE", "por+eng")
TESSERACT_CONFIG = os.getenv("TESSERACT_CONFIG", "--oem 3 --psm 6")

# Configurações de embeddings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
DEFAULT_QUERY_LIMIT = int(os.getenv("DEFAULT_QUERY_LIMIT", "5"))

# Configurações de LoRA
LORA_TARGET_MODULES_STR = os.getenv("LORA_TARGET_MODULES", "q_proj,v_proj")
LORA_CONFIG = {
    "r": int(os.getenv("LORA_R", "16")),
    "lora_alpha": int(os.getenv("LORA_ALPHA", "32")),
    "lora_dropout": float(os.getenv("LORA_DROPOUT", "0.1")),
    "target_modules": LORA_TARGET_MODULES_STR.split(","),
}

# Configurações de treinamento
TRAINING_CONFIG = {
    "num_train_epochs": int(os.getenv("TRAINING_EPOCHS", "3")),
    "per_device_train_batch_size": int(os.getenv("TRAINING_BATCH_SIZE", "4")),
    "gradient_accumulation_steps": int(os.getenv("GRADIENT_ACCUMULATION_STEPS", "4")),
    "warmup_steps": int(os.getenv("WARMUP_STEPS", "100")),
    "learning_rate": float(os.getenv("TRAINING_LEARNING_RATE", "2e-4")),
    "fp16": os.getenv("TRAINING_FP16", "true").lower() == "true",
    "logging_steps": int(os.getenv("LOGGING_STEPS", "10")),
    "save_steps": int(os.getenv("SAVE_STEPS", "100")),
}

# Configurações de Chat
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", "50"))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "1000"))
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))

# Configurações de confiança
CONFIDENCE_THRESHOLDS = {
    "high": float(os.getenv("CONFIDENCE_THRESHOLD_HIGH", "0.7")),
    "medium": float(os.getenv("CONFIDENCE_THRESHOLD_MEDIUM", "0.4")),
    "low": float(os.getenv("CONFIDENCE_THRESHOLD_LOW", "0.0")),
}

# Configurações de log
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/omnisia.log")
ENABLE_DEBUG = os.getenv("ENABLE_DEBUG", "false").lower() == "true"
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALLOWED_HOSTS_STR = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1")
ALLOWED_HOSTS = ALLOWED_HOSTS_STR.split(",")
CSRF_ENABLED = os.getenv("CSRF_ENABLED", "true").lower() == "true"

# Configurações de cache
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "100"))

# Configurações de performance
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Configurações de cache de modelos
HUGGINGFACE_CACHE_DIR = os.getenv("HUGGINGFACE_CACHE_DIR", "data/huggingface_cache")
TORCH_CACHE_DIR = os.getenv("TORCH_CACHE_DIR", "data/torch_cache")

# Configurações de banco de dados (futuro)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/omnisia.db")
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

# Configurações de versão
VERSION = os.getenv("VERSION", "1.0.0")
BUILD_DATE = os.getenv("BUILD_DATE", "2024-01-01")
AUTHOR = os.getenv("AUTHOR", "Roberto Dantas de Castro")
EMAIL = os.getenv("EMAIL", "robertodantasdecastro@gmail.com")


# Funções auxiliares
def get_upload_path() -> Path:
    """Retorna o caminho de upload"""
    return UPLOAD_DIR


def get_models_path() -> Path:
    """Retorna o caminho dos modelos"""
    return MODELS_DIR


def get_datasets_path() -> Path:
    """Retorna o caminho dos datasets"""
    return DATASETS_DIR


def get_logs_path() -> Path:
    """Retorna o caminho dos logs"""
    return LOGS_DIR


def is_file_allowed(filename: str) -> bool:
    """Verifica se a extensão do arquivo é permitida"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def get_confidence_level(confidence: float) -> str:
    """Retorna o nível de confiança baseado no valor"""
    if confidence >= CONFIDENCE_THRESHOLDS["high"]:
        return "high"
    elif confidence >= CONFIDENCE_THRESHOLDS["medium"]:
        return "medium"
    else:
        return "low"
