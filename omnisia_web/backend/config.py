import os
from pathlib import Path

# Configurações do sistema
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
MODELS_DIR = DATA_DIR / "models"
DATASETS_DIR = DATA_DIR / "datasets"

# Cria diretórios se não existirem
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# Configurações de upload
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".mp3",
    ".wav",
    ".mp4",
    ".avi",
    ".mov",
}

# Configurações de modelos
SUPPORTED_MODELS = [
    "gpt2",
    "gpt2-medium",
    "gpt2-large",
    "gpt2-xl",
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
]

# Configurações de Whisper
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

# Configurações de embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Configurações de LoRA
LORA_CONFIG = {
    "r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.1,
    "target_modules": ["q_proj", "v_proj"],
}

# Configurações de treinamento
TRAINING_CONFIG = {
    "num_train_epochs": 3,
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "warmup_steps": 100,
    "learning_rate": 2e-4,
    "fp16": True,
    "logging_steps": 10,
    "save_steps": 100,
}
