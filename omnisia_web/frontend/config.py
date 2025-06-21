"""
Configurações do Frontend OmnisIA Trainer Web
"""

import os
from typing import Dict, List

# ============================================================================
# CONFIGURAÇÕES DA API
# ============================================================================
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # segundos
API_RETRY_ATTEMPTS = int(os.getenv("API_RETRY_ATTEMPTS", "3"))

# ============================================================================
# CONFIGURAÇÕES DA INTERFACE
# ============================================================================
PAGE_TITLE = "OmnisIA Trainer Web"
PAGE_ICON = "🤖"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"
THEME = "light"

# ============================================================================
# CONFIGURAÇÕES DE UPLOAD
# ============================================================================
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

SUPPORTED_FILE_TYPES = {
    "pdf": "📄",
    "txt": "📝",
    "jpg": "🖼️",
    "jpeg": "🖼️",
    "png": "🖼️",
    "gif": "🖼️",
    "mp3": "🎵",
    "wav": "🎵",
    "mp4": "🎬",
    "avi": "🎬",
    "mov": "🎬",
}

SUPPORTED_FILE_EXTENSIONS = list(SUPPORTED_FILE_TYPES.keys())

# ============================================================================
# CONFIGURAÇÕES DE CHAT
# ============================================================================
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", "50"))
MAX_CONTEXT_LENGTH = int(os.getenv("MAX_CONTEXT_LENGTH", "1000"))
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))

CONFIDENCE_THRESHOLDS = {"high": 0.7, "medium": 0.4, "low": 0.0}

CHAT_REFRESH_INTERVAL = int(os.getenv("CHAT_REFRESH_INTERVAL", "5"))  # segundos

# ============================================================================
# CONFIGURAÇÕES DE PRÉ-PROCESSAMENTO
# ============================================================================
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
DEFAULT_WHISPER_MODEL = "base"

WHISPER_MODEL_DESCRIPTIONS = {
    "tiny": "Mais rápido, menos preciso",
    "base": "Equilibrado",
    "small": "Bom equilíbrio",
    "medium": "Mais preciso, mais lento",
    "large": "Mais lento, mais preciso",
}

OCR_LANGUAGES = ["por", "eng"]
DEFAULT_OCR_LANGUAGE = "por+eng"

# ============================================================================
# CONFIGURAÇÕES DE TREINAMENTO
# ============================================================================
DEFAULT_TRAINING_CONFIG = {
    "output_dir": "data/models/lora_output",
    "dataset_path": "data/datasets/training_data.txt",
    "num_epochs": 3,
    "batch_size": 4,
    "learning_rate": 2e-4,
}

DEFAULT_MODELS = [
    "gpt2",
    "gpt2-medium",
    "gpt2-large",
    "gpt2-xl",
    "microsoft/DialoGPT-small",
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
]

# ============================================================================
# CONFIGURAÇÕES DE EMBEDDINGS
# ============================================================================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
DEFAULT_QUERY_LIMIT = int(os.getenv("DEFAULT_QUERY_LIMIT", "5"))

# ============================================================================
# CONFIGURAÇÕES DE LORA
# ============================================================================
LORA_CONFIG = {
    "r": int(os.getenv("LORA_R", "16")),
    "lora_alpha": int(os.getenv("LORA_ALPHA", "32")),
    "lora_dropout": float(os.getenv("LORA_DROPOUT", "0.1")),
    "target_modules": ["q_proj", "v_proj"],
}

# ============================================================================
# CONFIGURAÇÕES DE TREINAMENTO
# ============================================================================
TRAINING_CONFIG = {
    "num_train_epochs": int(os.getenv("TRAINING_EPOCHS", "3")),
    "per_device_train_batch_size": int(os.getenv("TRAINING_BATCH_SIZE", "4")),
    "gradient_accumulation_steps": int(os.getenv("GRADIENT_ACCUMULATION_STEPS", "4")),
    "warmup_steps": int(os.getenv("WARMUP_STEPS", "100")),
    "learning_rate": float(os.getenv("TRAINING_LEARNING_RATE", "2e-4")),
    "fp16": os.getenv("FP16", "true").lower() == "true",
    "logging_steps": int(os.getenv("LOGGING_STEPS", "10")),
    "save_steps": int(os.getenv("SAVE_STEPS", "100")),
}

# ============================================================================
# CONFIGURAÇÕES DE MÉTRICAS
# ============================================================================
METRICS_REFRESH_INTERVAL = int(os.getenv("METRICS_REFRESH_INTERVAL", "30"))  # segundos
RECENT_FILES_LIMIT = int(os.getenv("RECENT_FILES_LIMIT", "5"))
DASHBOARD_UPDATE_INTERVAL = int(
    os.getenv("DASHBOARD_UPDATE_INTERVAL", "10")
)  # segundos

# ============================================================================
# CONFIGURAÇÕES DE SESSÃO
# ============================================================================
SESSION_KEYS = {
    "chat_history": "chat_history",
    "uploaded_files": "uploaded_files",
    "context_texts": "context_texts",
    "user_preferences": "user_preferences",
    "last_api_check": "last_api_check",
    "cached_models": "cached_models",
    "cached_files": "cached_files",
}

# ============================================================================
# CONFIGURAÇÕES DE UI
# ============================================================================
UI_CONFIG = {
    "theme": THEME,
    "primary_color": "#FF6B6B",
    "secondary_color": "#4ECDC4",
    "success_color": "#45B7D1",
    "warning_color": "#96CEB4",
    "error_color": "#FFEAA7",
    "background_color": "#FFFFFF",
    "text_color": "#2C3E50",
}

# ============================================================================
# CONFIGURAÇÕES DE NAVEGAÇÃO
# ============================================================================
NAVIGATION_PAGES = [
    "🏠 Dashboard",
    "📤 Upload",
    "🔧 Pré-processamento",
    "🎯 Treinamento",
    "💬 Chat",
    "📊 Status",
]

DEFAULT_PAGE = "🏠 Dashboard"

# ============================================================================
# CONFIGURAÇÕES DE LINKS ÚTEIS
# ============================================================================
USEFUL_LINKS = {
    "Documentação da API": "docs/API.md",
    "Exemplos de Uso": "examples/example_usage.py",
    "GitHub": "https://github.com/robertodantasdecastro/OmnisIA",
    "Issues": "https://github.com/robertodantasdecastro/OmnisIA/issues",
    "Wiki": "https://github.com/robertodantasdecastro/OmnisIA/wiki",
}

# ============================================================================
# CONFIGURAÇÕES DE MENSAGENS
# ============================================================================
MESSAGES = {
    "api_offline": "❌ Não foi possível conectar ao backend. Verifique se a API está rodando em http://localhost:8000",
    "upload_success": "✅ Arquivo enviado com sucesso!",
    "upload_error": "❌ Erro no upload: {}",
    "processing_success": "✅ Processamento concluído com sucesso!",
    "processing_error": "❌ Erro no processamento: {}",
    "chat_success": "✅ Resposta recebida!",
    "chat_error": "❌ Erro no chat: {}",
    "training_success": "✅ Treinamento concluído!",
    "training_error": "❌ Erro no treinamento: {}",
    "context_added": "✅ Contexto adicionado com sucesso!",
    "context_cleared": "🗑️ Contexto limpo!",
    "history_cleared": "🗑️ Histórico limpo!",
    "connection_error": "❌ Erro na conexão: {}",
    "validation_error": "⚠️ Erro de validação: {}",
    "file_too_large": f"❌ Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE_MB}MB",
    "unsupported_file_type": f"❌ Tipo de arquivo não suportado. Tipos aceitos: {', '.join(SUPPORTED_FILE_EXTENSIONS)}",
    "no_files_found": "Nenhum arquivo encontrado",
    "no_context_found": "Nenhum contexto encontrado",
    "api_online": "✅ API Backend: Online",
    "api_offline_status": "❌ API Backend: Offline",
    "api_error": "❌ API Backend: Erro",
}

# ============================================================================
# CONFIGURAÇÕES DE PLACEHOLDERS
# ============================================================================
PLACEHOLDERS = {
    "pdf_path": "data/uploads/documento.pdf",
    "audio_path": "data/uploads/audio.wav",
    "video_path": "data/uploads/video.mp4",
    "image_path": "data/uploads/imagem.jpg",
    "dataset_path": "data/datasets/training_data.txt",
    "output_path": "data/output/resultado.pdf",
    "chat_message": "Faça uma pergunta...",
    "context_text": "Digite um texto por linha...",
    "search_query": "Digite sua busca...",
}

# ============================================================================
# CONFIGURAÇÕES DE AJUDA
# ============================================================================
HELP_TEXTS = {
    "file_upload": f"Arquivos suportados: {', '.join([ext.upper() for ext in SUPPORTED_FILE_EXTENSIONS])}. Tamanho máximo: {MAX_FILE_SIZE_MB}MB",
    "whisper_model": "Modelos maiores são mais precisos mas mais lentos",
    "lora_training": "LoRA (Low-Rank Adaptation): Treinamento eficiente com poucos parâmetros",
    "ocr_processing": "OCR extrai texto de imagens e PDFs. Suporta português e inglês",
    "chat_context": "Adicione textos relevantes para melhorar as respostas do chat",
    "training_config": "Configure parâmetros de treinamento para otimizar performance",
}

# ============================================================================
# CONFIGURAÇÕES DE LOG
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/frontend.log")
ENABLE_DEBUG = os.getenv("ENABLE_DEBUG", "false").lower() == "true"

# ============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# ============================================================================
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
CSRF_ENABLED = os.getenv("CSRF_ENABLED", "true").lower() == "true"

# ============================================================================
# CONFIGURAÇÕES DE CACHE
# ============================================================================
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", "300"))  # segundos
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "100"))

# ============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================================
ENABLE_LAZY_LOADING = os.getenv("ENABLE_LAZY_LOADING", "true").lower() == "true"
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# ============================================================================
# CONFIGURAÇÕES DE VERSÃO
# ============================================================================
VERSION = "1.0.0"
BUILD_DATE = "2024-01-01"
AUTHOR = "Roberto Dantas de Castro"
EMAIL = "robertodantasdecastro@gmail.com"

# ============================================================================
# CONFIGURAÇÕES DE DESENVOLVIMENTO
# ============================================================================
DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
ENABLE_HOT_RELOAD = os.getenv("ENABLE_HOT_RELOAD", "true").lower() == "true"
SHOW_DEBUG_INFO = os.getenv("SHOW_DEBUG_INFO", "false").lower() == "true"

# ============================================================================
# CONFIGURAÇÕES DE BANCO DE DADOS (FUTURO)
# ============================================================================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./omnisia.db")
DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

# ============================================================================
# CONFIGURAÇÕES DE CACHE (FUTURO)
# ============================================================================
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")


# ============================================================================
# FUNÇÕES DE CONFIGURAÇÃO
# ============================================================================
def get_api_url() -> str:
    """Retorna a URL da API"""
    return API_URL


def get_supported_file_types() -> Dict[str, str]:
    """Retorna tipos de arquivo suportados"""
    return SUPPORTED_FILE_TYPES.copy()


def get_whisper_models() -> List[str]:
    """Retorna modelos Whisper disponíveis"""
    return WHISPER_MODELS.copy()


def get_navigation_pages() -> List[str]:
    """Retorna páginas de navegação"""
    return NAVIGATION_PAGES.copy()


def get_messages() -> Dict[str, str]:
    """Retorna mensagens do sistema"""
    return MESSAGES.copy()


def get_placeholders() -> Dict[str, str]:
    """Retorna placeholders"""
    return PLACEHOLDERS.copy()


def get_help_texts() -> Dict[str, str]:
    """Retorna textos de ajuda"""
    return HELP_TEXTS.copy()


def is_development_mode() -> bool:
    """Verifica se está em modo desenvolvimento"""
    return DEVELOPMENT_MODE


def is_debug_enabled() -> bool:
    """Verifica se debug está habilitado"""
    return ENABLE_DEBUG or DEVELOPMENT_MODE
