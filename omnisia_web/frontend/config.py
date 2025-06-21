"""
Configurações do Frontend OmnisIA Trainer Web
"""

import os
from typing import Dict, List

# Configurações da API
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_TIMEOUT = 30  # segundos

# Configurações da interface
PAGE_TITLE = "OmnisIA Trainer Web"
PAGE_ICON = "🤖"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Configurações de upload
MAX_FILE_SIZE_MB = 100
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

# Configurações de chat
MAX_CHAT_HISTORY = 50
MAX_CONTEXT_LENGTH = 1000
CONFIDENCE_THRESHOLDS = {"high": 0.7, "medium": 0.4, "low": 0.0}

# Configurações de pré-processamento
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]
WHISPER_MODEL_DESCRIPTIONS = {
    "tiny": "Mais rápido, menos preciso",
    "base": "Equilibrado",
    "small": "Bom equilíbrio",
    "medium": "Mais preciso, mais lento",
    "large": "Mais lento, mais preciso",
}

# Configurações de treinamento
DEFAULT_TRAINING_CONFIG = {
    "output_dir": "data/models/lora_output",
    "dataset_path": "data/datasets/training_data.txt",
}

# Configurações de métricas
METRICS_REFRESH_INTERVAL = 30  # segundos
RECENT_FILES_LIMIT = 5

# Configurações de sessão
SESSION_KEYS = {
    "chat_history": "chat_history",
    "uploaded_files": "uploaded_files",
    "context_texts": "context_texts",
    "user_preferences": "user_preferences",
}

# Configurações de UI
UI_CONFIG = {
    "theme": "light",
    "primary_color": "#FF6B6B",
    "secondary_color": "#4ECDC4",
    "success_color": "#45B7D1",
    "warning_color": "#96CEB4",
    "error_color": "#FFEAA7",
}

# Configurações de navegação
NAVIGATION_PAGES = [
    "🏠 Dashboard",
    "📤 Upload",
    "🔧 Pré-processamento",
    "🎯 Treinamento",
    "💬 Chat",
    "📊 Status",
]

# Configurações de links úteis
USEFUL_LINKS = {
    "Documentação da API": "docs/API.md",
    "Exemplos de Uso": "examples/example_usage.py",
    "GitHub": "https://github.com/robertodantasdecastro/OmnisIA",
}

# Configurações de mensagens
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
}

# Configurações de placeholders
PLACEHOLDERS = {
    "pdf_path": "data/uploads/documento.pdf",
    "audio_path": "data/uploads/audio.wav",
    "video_path": "data/uploads/video.mp4",
    "image_path": "data/uploads/imagem.jpg",
    "dataset_path": "data/datasets/training_data.txt",
    "chat_message": "Faça uma pergunta...",
    "context_text": "Digite um texto por linha...",
}

# Configurações de ajuda
HELP_TEXTS = {
    "file_upload": "Arquivos suportados: PDF, TXT, imagens (JPG, PNG, GIF), áudio (MP3, WAV), vídeo (MP4, AVI, MOV)",
    "whisper_model": "Modelos maiores são mais precisos mas mais lentos",
    "lora_training": "LoRA (Low-Rank Adaptation): Treinamento eficiente com poucos parâmetros",
}
