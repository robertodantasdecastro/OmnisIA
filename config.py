"""
OMNISIA - CONFIGURAÇÃO COMPLETA / COMPLETE CONFIGURATION
Sistema Integrado de IA Multimodal / Integrated Multimodal AI System
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from dataclasses import dataclass

# ============================================================================
# CONFIGURAÇÕES DE DIRETÓRIO / DIRECTORY CONFIGURATIONS
# ============================================================================
BASE_DIR = Path(__file__).parent.absolute()
DATA_DIR = BASE_DIR / "data"

# Diretórios principais / Main directories
UPLOAD_DIR = DATA_DIR / "uploads"
MODELS_DIR = DATA_DIR / "models"
LOCAL_MODELS_DIR = MODELS_DIR / "local"
DATASETS_DIR = DATA_DIR / "datasets"
TRAINING_DIR = DATA_DIR / "training"
CHECKPOINTS_DIR = DATA_DIR / "checkpoints"
EXPORTS_DIR = DATA_DIR / "exports"
TEMP_DIR = DATA_DIR / "temp"
BACKUPS_DIR = DATA_DIR / "backups"
LOGS_DIR = BASE_DIR / "logs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SCRIPTS_DIR = BASE_DIR / "scripts"

# Criação automática de diretórios / Automatic directory creation
DIRECTORIES_TO_CREATE = [
    UPLOAD_DIR,
    MODELS_DIR,
    LOCAL_MODELS_DIR,
    DATASETS_DIR,
    TRAINING_DIR,
    CHECKPOINTS_DIR,
    EXPORTS_DIR,
    TEMP_DIR,
    BACKUPS_DIR,
    LOGS_DIR,
    NOTEBOOKS_DIR,
    SCRIPTS_DIR,
]

for directory in DIRECTORIES_TO_CREATE:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CONFIGURAÇÕES DE API E SERVIDOR / API AND SERVER CONFIGURATIONS
# ============================================================================
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "300"))
API_RETRY_ATTEMPTS = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))

# Frontend
FRONTEND_HOST = os.getenv("FRONTEND_HOST", "0.0.0.0")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8501"))

# ============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS / DATABASE CONFIGURATIONS
# ============================================================================

# PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "omnisia")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# MongoDB
MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
MONGODB_DB = os.getenv("MONGODB_DB", "omnisia")
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")
MONGODB_URL = (
    f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"
    if MONGODB_USER
    else f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"
)

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_URL = (
    f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    if REDIS_PASSWORD
    else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)

# SQLite (padrão local / default local)
SQLITE_PATH = DATA_DIR / "omnisia.db"
SQLITE_URL = f"sqlite+aiosqlite:///{SQLITE_PATH}"

# DynamoDB
DYNAMODB_REGION = os.getenv("DYNAMODB_REGION", "us-east-1")
DYNAMODB_TABLE_PREFIX = os.getenv("DYNAMODB_TABLE_PREFIX", "omnisia")

# Banco de dados ativo / Active database
DATABASE_TYPE = os.getenv(
    "DATABASE_TYPE", "sqlite"
)  # sqlite, postgresql, mongodb, redis
DATABASE_URL = {
    "sqlite": SQLITE_URL,
    "postgresql": POSTGRES_URL,
    "mongodb": MONGODB_URL,
    "redis": REDIS_URL,
}.get(DATABASE_TYPE, SQLITE_URL)

# ============================================================================
# APIS EXTERNAS / EXTERNAL APIS
# ============================================================================

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

# DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

# Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-pro")

# AWS Bedrock
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL = os.getenv("BEDROCK_MODEL", "anthropic.claude-3-sonnet-20240229-v1:0")

# Kaggle
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME", "")
KAGGLE_KEY = os.getenv("KAGGLE_KEY", "")

# SageMaker
SAGEMAKER_ENDPOINT = os.getenv("SAGEMAKER_ENDPOINT", "")
SAGEMAKER_REGION = os.getenv("SAGEMAKER_REGION", "us-east-1")

# ============================================================================
# MODELOS LOCAIS / LOCAL MODELS
# ============================================================================

LOCAL_MODELS_CONFIG = {
    "deepseek-r1": {
        "path": LOCAL_MODELS_DIR / "deepseek-r1",
        "url": "https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
        "type": "llm",
        "size": "8B",
        "quantization": "4bit",
    },
    "llama-3.1-8b": {
        "path": LOCAL_MODELS_DIR / "llama-3.1-8b",
        "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct",
        "type": "llm",
        "size": "8B",
        "quantization": "4bit",
    },
    "mistral-7b": {
        "path": LOCAL_MODELS_DIR / "mistral-7b",
        "url": "https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3",
        "type": "llm",
        "size": "7B",
        "quantization": "4bit",
    },
    "codellama": {
        "path": LOCAL_MODELS_DIR / "codellama",
        "url": "https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf",
        "type": "code",
        "size": "7B",
        "quantization": "4bit",
    },
    "whisper-large": {
        "path": LOCAL_MODELS_DIR / "whisper-large",
        "url": "https://huggingface.co/openai/whisper-large-v3",
        "type": "audio",
        "size": "1.5B",
    },
}

# Modelo padrão / Default model
DEFAULT_LOCAL_MODEL = os.getenv("DEFAULT_LOCAL_MODEL", "deepseek-r1")

# ============================================================================
# CONFIGURAÇÕES DE TREINAMENTO / TRAINING CONFIGURATIONS
# ============================================================================

# LoRA Configuration
LORA_CONFIG = {
    "r": int(os.getenv("LORA_R", "16")),
    "lora_alpha": int(os.getenv("LORA_ALPHA", "32")),
    "lora_dropout": float(os.getenv("LORA_DROPOUT", "0.1")),
    "target_modules": os.getenv(
        "LORA_TARGET_MODULES", "q_proj,v_proj,k_proj,o_proj"
    ).split(","),
    "bias": os.getenv("LORA_BIAS", "none"),
    "task_type": os.getenv("LORA_TASK_TYPE", "CAUSAL_LM"),
}

# Training Configuration
TRAINING_CONFIG = {
    "output_dir": str(TRAINING_DIR / "output"),
    "num_train_epochs": int(os.getenv("TRAINING_EPOCHS", "3")),
    "per_device_train_batch_size": int(os.getenv("TRAINING_BATCH_SIZE", "2")),
    "per_device_eval_batch_size": int(os.getenv("EVAL_BATCH_SIZE", "2")),
    "gradient_accumulation_steps": int(os.getenv("GRADIENT_ACCUMULATION_STEPS", "8")),
    "warmup_steps": int(os.getenv("WARMUP_STEPS", "100")),
    "learning_rate": float(os.getenv("TRAINING_LEARNING_RATE", "2e-4")),
    "fp16": os.getenv("TRAINING_FP16", "true").lower() == "true",
    "bf16": os.getenv("TRAINING_BF16", "false").lower() == "true",
    "logging_steps": int(os.getenv("LOGGING_STEPS", "10")),
    "save_steps": int(os.getenv("SAVE_STEPS", "500")),
    "eval_steps": int(os.getenv("EVAL_STEPS", "500")),
    "max_grad_norm": float(os.getenv("MAX_GRAD_NORM", "1.0")),
    "dataloader_num_workers": int(os.getenv("DATALOADER_NUM_WORKERS", "4")),
    "save_total_limit": int(os.getenv("SAVE_TOTAL_LIMIT", "3")),
    "load_best_model_at_end": True,
    "metric_for_best_model": "eval_loss",
    "greater_is_better": False,
    "report_to": os.getenv("REPORT_TO", "tensorboard").split(","),
}

# Distributed Training
DISTRIBUTED_TRAINING = {
    "deepspeed_config": os.getenv("DEEPSPEED_CONFIG", ""),
    "fsdp": os.getenv("FSDP", ""),
    "ddp_find_unused_parameters": os.getenv(
        "DDP_FIND_UNUSED_PARAMETERS", "false"
    ).lower()
    == "true",
}

# ============================================================================
# PROTOCOLOS REMOTOS / REMOTE PROTOCOLS
# ============================================================================

# FTP Configuration
FTP_CONFIG = {
    "host": os.getenv("FTP_HOST", ""),
    "port": int(os.getenv("FTP_PORT", "21")),
    "username": os.getenv("FTP_USERNAME", ""),
    "password": os.getenv("FTP_PASSWORD", ""),
    "passive": os.getenv("FTP_PASSIVE", "true").lower() == "true",
    "timeout": int(os.getenv("FTP_TIMEOUT", "30")),
}

# SFTP Configuration
SFTP_CONFIG = {
    "host": os.getenv("SFTP_HOST", ""),
    "port": int(os.getenv("SFTP_PORT", "22")),
    "username": os.getenv("SFTP_USERNAME", ""),
    "password": os.getenv("SFTP_PASSWORD", ""),
    "private_key_path": os.getenv("SFTP_PRIVATE_KEY_PATH", ""),
    "timeout": int(os.getenv("SFTP_TIMEOUT", "30")),
}

# HTTP/HTTPS Configuration
HTTP_CONFIG = {
    "timeout": int(os.getenv("HTTP_TIMEOUT", "30")),
    "max_retries": int(os.getenv("HTTP_MAX_RETRIES", "3")),
    "user_agent": os.getenv("HTTP_USER_AGENT", "OmnisIA/2.0"),
    "headers": {},
}

# WebDAV Configuration
WEBDAV_CONFIG = {
    "url": os.getenv("WEBDAV_URL", ""),
    "username": os.getenv("WEBDAV_USERNAME", ""),
    "password": os.getenv("WEBDAV_PASSWORD", ""),
    "timeout": int(os.getenv("WEBDAV_TIMEOUT", "30")),
}

# ============================================================================
# PROCESSAMENTO DE ARQUIVOS / FILE PROCESSING
# ============================================================================

# Upload Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "500"))
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = set(
    os.getenv(
        "ALLOWED_EXTENSIONS",
        ".pdf,.txt,.docx,.xlsx,.pptx,.jpg,.jpeg,.png,.gif,.mp3,.wav,.mp4,.avi,.mov,.py,.ipynb,.csv,.json,.xml,.html",
    ).split(",")
)

# OCR Configuration
OCR_CONFIG = {
    "languages": os.getenv("OCR_LANGUAGES", "por+eng").split("+"),
    "tesseract_config": os.getenv("TESSERACT_CONFIG", "--oem 3 --psm 6"),
    "confidence_threshold": float(os.getenv("OCR_CONFIDENCE_THRESHOLD", "0.7")),
}

# STT Configuration
STT_CONFIG = {
    "model": os.getenv("STT_MODEL", "whisper-large"),
    "language": os.getenv("STT_LANGUAGE", "pt"),
    "temperature": float(os.getenv("STT_TEMPERATURE", "0.0")),
    "beam_size": int(os.getenv("STT_BEAM_SIZE", "5")),
}

# ============================================================================
# EMBEDDINGS E BUSCA VETORIAL / EMBEDDINGS AND VECTOR SEARCH
# ============================================================================

EMBEDDING_CONFIG = {
    "model": os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
    "dimension": int(os.getenv("EMBEDDING_DIMENSION", "384")),
    "batch_size": int(os.getenv("EMBEDDING_BATCH_SIZE", "32")),
    "device": os.getenv("EMBEDDING_DEVICE", "auto"),
}

VECTOR_DB_CONFIG = {
    "type": os.getenv(
        "VECTOR_DB_TYPE", "chromadb"
    ),  # chromadb, faiss, pinecone, weaviate
    "collection_name": os.getenv("VECTOR_COLLECTION_NAME", "omnisia_docs"),
    "top_k": int(os.getenv("VECTOR_TOP_K", "5")),
    "similarity_threshold": float(os.getenv("VECTOR_SIMILARITY_THRESHOLD", "0.7")),
}

# ============================================================================
# JUPYTER E NOTEBOOKS / JUPYTER AND NOTEBOOKS
# ============================================================================

JUPYTER_CONFIG = {
    "host": os.getenv("JUPYTER_HOST", "0.0.0.0"),
    "port": int(os.getenv("JUPYTER_PORT", "8888")),
    "token": os.getenv("JUPYTER_TOKEN", ""),
    "password": os.getenv("JUPYTER_PASSWORD", ""),
    "allow_root": os.getenv("JUPYTER_ALLOW_ROOT", "true").lower() == "true",
}

# ============================================================================
# MONITORAMENTO E LOGS / MONITORING AND LOGS
# ============================================================================

LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "file": str(LOGS_DIR / "omnisia.log"),
    "max_size": int(os.getenv("LOG_MAX_SIZE_MB", "100")) * 1024 * 1024,
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5")),
    "format": os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ),
}

MONITORING_CONFIG = {
    "prometheus_enabled": os.getenv("PROMETHEUS_ENABLED", "false").lower() == "true",
    "prometheus_port": int(os.getenv("PROMETHEUS_PORT", "9090")),
    "health_check_interval": int(os.getenv("HEALTH_CHECK_INTERVAL", "30")),
}

# ============================================================================
# SEGURANÇA / SECURITY
# ============================================================================

SECURITY_CONFIG = {
    "secret_key": os.getenv("SECRET_KEY", "change-this-in-production"),
    "encryption_key": os.getenv("ENCRYPTION_KEY", ""),
    "jwt_algorithm": os.getenv("JWT_ALGORITHM", "HS256"),
    "jwt_expiration": int(os.getenv("JWT_EXPIRATION_HOURS", "24")),
    "allowed_hosts": os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(","),
    "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
}

# ============================================================================
# INFORMAÇÕES DO SISTEMA / SYSTEM INFORMATION
# ============================================================================

SYSTEM_INFO = {
    "version": os.getenv("VERSION", "2.0.0"),
    "build_date": os.getenv("BUILD_DATE", "2024-12-19"),
    "author": os.getenv("AUTHOR", "Roberto Dantas de Castro"),
    "email": os.getenv("EMAIL", "robertodantasdecastro@gmail.com"),
    "github": os.getenv("GITHUB", "https://github.com/username/omnisia"),
    "license": os.getenv("LICENSE", "MIT"),
}

# ============================================================================
# FUNÇÕES AUXILIARES / HELPER FUNCTIONS
# ============================================================================


def get_database_url(db_type: Optional[str] = None) -> str:
    """Retorna a URL do banco de dados"""
    db_type = db_type or DATABASE_TYPE
    return {
        "sqlite": SQLITE_URL,
        "postgresql": POSTGRES_URL,
        "mongodb": MONGODB_URL,
        "redis": REDIS_URL,
    }.get(db_type, SQLITE_URL)


def get_model_path(model_name: str) -> Path:
    """Retorna o caminho do modelo local"""
    if model_name in LOCAL_MODELS_CONFIG:
        return LOCAL_MODELS_CONFIG[model_name]["path"]
    return LOCAL_MODELS_DIR / model_name


def is_file_allowed(filename: str) -> bool:
    """Verifica se a extensão do arquivo é permitida"""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def get_api_config(provider: str) -> Dict[str, Any]:
    """Retorna configuração da API externa"""
    configs = {
        "openai": {
            "api_key": OPENAI_API_KEY,
            "model": OPENAI_MODEL,
            "max_tokens": OPENAI_MAX_TOKENS,
            "temperature": OPENAI_TEMPERATURE,
        },
        "deepseek": {
            "api_key": DEEPSEEK_API_KEY,
            "model": DEEPSEEK_MODEL,
            "base_url": DEEPSEEK_BASE_URL,
        },
        "anthropic": {"api_key": ANTHROPIC_API_KEY, "model": ANTHROPIC_MODEL},
        "google": {"api_key": GOOGLE_API_KEY, "model": GOOGLE_MODEL},
    }
    return configs.get(provider, {})


def setup_logging():
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, LOG_CONFIG["level"]),
        format=LOG_CONFIG["format"],
        handlers=[logging.FileHandler(LOG_CONFIG["file"]), logging.StreamHandler()],
    )
    return logging.getLogger("omnisia")


def validate_config():
    """Valida as configurações do sistema"""
    errors = []

    # Validação de APIs
    if not OPENAI_API_KEY and not DEEPSEEK_API_KEY:
        errors.append(
            "Pelo menos uma API key (OpenAI ou DeepSeek) deve ser configurada"
        )

    # Validação de diretórios
    for directory in DIRECTORIES_TO_CREATE:
        if not directory.exists():
            errors.append(f"Diretório não existe: {directory}")

    return errors


# Validação automática na importação
_validation_errors = validate_config()
if _validation_errors:
    logger = setup_logging()
    for error in _validation_errors:
        logger.warning(f"Aviso de configuração: {error}")


# ============================================================================
# CONFIGURAÇÕES DE DESENVOLVIMENTO / DEVELOPMENT CONFIGURATIONS
# ============================================================================

DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
TESTING_MODE = os.getenv("TESTING_MODE", "false").lower() == "true"

if DEVELOPMENT_MODE:
    # Configurações para desenvolvimento
    API_TIMEOUT = 600
    LOG_CONFIG["level"] = "DEBUG"
    SECURITY_CONFIG["cors_origins"] = ["*"]
