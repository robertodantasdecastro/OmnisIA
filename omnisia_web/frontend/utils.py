"""
Utilitários do Frontend OmnisIA Trainer Web
"""

import streamlit as st
import requests
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
import os
import pandas as pd
from pathlib import Path

from config import (
    API_URL,
    API_TIMEOUT,
    API_RETRY_ATTEMPTS,
    MAX_FILE_SIZE_BYTES,
    SUPPORTED_FILE_EXTENSIONS,
    SUPPORTED_FILE_TYPES,
    MAX_CHAT_HISTORY,
    MAX_CONTEXT_LENGTH,
    MAX_MESSAGE_LENGTH,
    CONFIDENCE_THRESHOLDS,
    CHAT_REFRESH_INTERVAL,
    WHISPER_MODELS,
    DEFAULT_WHISPER_MODEL,
    WHISPER_MODEL_DESCRIPTIONS,
    OCR_LANGUAGES,
    DEFAULT_OCR_LANGUAGE,
    DEFAULT_MODELS,
    EMBEDDING_MODEL,
    DEFAULT_QUERY_LIMIT,
    LORA_CONFIG,
    TRAINING_CONFIG,
    METRICS_REFRESH_INTERVAL,
    RECENT_FILES_LIMIT,
    DASHBOARD_UPDATE_INTERVAL,
    SESSION_KEYS,
    MESSAGES,
    PLACEHOLDERS,
    HELP_TEXTS,
    LOG_LEVEL,
    LOG_FILE,
    ENABLE_DEBUG,
    CACHE_ENABLED,
    CACHE_TTL,
    CACHE_MAX_SIZE,
    MAX_CONCURRENT_REQUESTS,
    REQUEST_TIMEOUT,
    VERSION,
    BUILD_DATE,
    AUTHOR,
    EMAIL,
    DEVELOPMENT_MODE,
    ENABLE_HOT_RELOAD,
    SHOW_DEBUG_INFO,
    get_api_url,
    get_supported_file_types,
    get_whisper_models,
    get_navigation_pages,
    get_messages,
    get_placeholders,
    get_help_texts,
    is_development_mode,
    is_debug_enabled,
)


# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================
def setup_logging():
    """Configura o sistema de logging"""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

    # Criar diretório de logs se não existir
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler() if is_debug_enabled() else logging.NullHandler(),
        ],
    )

    return logging.getLogger(__name__)


logger = setup_logging()


# ============================================================================
# CACHE SIMPLES EM MEMÓRIA
# ============================================================================
class SimpleCache:
    """Cache simples em memória"""

    def __init__(self, max_size: int = CACHE_MAX_SIZE, ttl: int = CACHE_TTL):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}

    def get(self, key: str) -> Optional[Any]:
        """Obtém valor do cache"""
        if not CACHE_ENABLED:
            return None

        if key in self.cache:
            if time.time() - self.timestamps[key] < self.ttl:
                return self.cache[key]
            else:
                del self.cache[key]
                del self.timestamps[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Define valor no cache"""
        if not CACHE_ENABLED:
            return

        if len(self.cache) >= self.max_size:
            # Remove o item mais antigo
            oldest_key = min(self.timestamps.keys(), key=lambda k: self.timestamps[k])
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]

        self.cache[key] = value
        self.timestamps[key] = time.time()

    def clear(self) -> None:
        """Limpa o cache"""
        self.cache.clear()
        self.timestamps.clear()


# Instância global do cache
cache = SimpleCache()


# ============================================================================
# UTILITÁRIOS DE SESSÃO
# ============================================================================
def init_session_state():
    """Inicializa o estado da sessão e busca arquivos existentes."""

    # Previne múltiplas execuções, verificando diretamente o st.session_state
    if st.session_state.get("app_initialized", False):
        return

    # Inicializa as chaves da sessão
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    if "context_texts" not in st.session_state:
        st.session_state["context_texts"] = []

    if "user_preferences" not in st.session_state:
        st.session_state["user_preferences"] = {
            "whisper_model": DEFAULT_WHISPER_MODEL,
            "ocr_language": DEFAULT_OCR_LANGUAGE,
            "embedding_model": EMBEDDING_MODEL,
            "query_limit": DEFAULT_QUERY_LIMIT,
            "theme": "light",
        }

    # Busca arquivos existentes na API
    try:
        if check_api_health():
            success, files, error = make_api_request("upload/files")
            if success and isinstance(files, list):
                st.session_state["uploaded_files"] = files
            else:
                logger.error(
                    f"Erro ao buscar arquivos iniciais: {error or 'Resposta inválida'}"
                )
                st.session_state["uploaded_files"] = []
    except Exception as e:
        logger.error(f"Falha crítica ao buscar arquivos da API: {e}")
        st.session_state["uploaded_files"] = []

    # Marca a sessão como inicializada
    st.session_state["app_initialized"] = True


def get_chat_history() -> List[Dict[str, Any]]:
    """Obtém o histórico de chat"""
    return st.session_state.get("chat_history", [])


def add_chat_message(
    role: str,
    content: str,
    confidence: float = 1.0,
    sources: Optional[List[str]] = None,
):
    """Adiciona mensagem ao histórico de chat"""
    history = get_chat_history()

    # Limita o histórico
    if len(history) >= MAX_CHAT_HISTORY:
        history = history[-MAX_CHAT_HISTORY + 1 :]

    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
        "confidence": confidence,
        "sources": sources or [],
    }

    history.append(message)
    st.session_state["chat_history"] = history


def clear_chat_history():
    """Limpa o histórico de chat"""
    st.session_state["chat_history"] = []


def get_uploaded_files() -> List[Dict[str, Any]]:
    """Obtém lista de arquivos enviados"""
    return st.session_state.get("uploaded_files", [])


def add_uploaded_file(file_info: Dict[str, Any]):
    """Adiciona arquivo à lista de uploads"""
    files = get_uploaded_files()
    files.append(file_info)
    st.session_state["uploaded_files"] = files


def get_context_texts() -> List[str]:
    """Obtém textos de contexto"""
    return st.session_state.get("context_texts", [])


def add_context_text(text: str):
    """Adiciona texto de contexto"""
    texts = get_context_texts()
    if text.strip() and text not in texts:
        texts.append(text.strip())
        st.session_state["context_texts"] = texts


def clear_context_texts():
    """Limpa textos de contexto"""
    st.session_state["context_texts"] = []


def get_user_preferences() -> Dict[str, Any]:
    """Obtém preferências do usuário"""
    return st.session_state.get("user_preferences", {})


def update_user_preferences(preferences: Dict[str, Any]):
    """Atualiza preferências do usuário"""
    current = get_user_preferences()
    current.update(preferences)
    st.session_state["user_preferences"] = current


# ============================================================================
# UTILITÁRIOS DE API
# ============================================================================
def make_api_request(
    endpoint: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None,
) -> Tuple[bool, Dict[str, Any], str]:
    """
    Faz requisição para a API

    Returns:
        Tuple[bool, Dict, str]: (success, response_data, error_message)
    """
    if timeout is None:
        timeout = API_TIMEOUT

    url = f"{get_api_url()}/{endpoint.lstrip('/')}"

    try:
        headers = {"Content-Type": "application/json"} if data and not files else {}

        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout, headers=headers)
        elif method.upper() == "POST":
            if files:
                response = requests.post(url, files=files, timeout=timeout)
            else:
                response = requests.post(
                    url, json=data, timeout=timeout, headers=headers
                )
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, timeout=timeout, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, timeout=timeout, headers=headers)
        else:
            return False, {}, f"Método HTTP não suportado: {method}"

        if response.status_code == 200:
            return True, response.json(), ""
        else:
            error_msg = f"Erro {response.status_code}: {response.text}"
            logger.error(f"API Error: {error_msg}")
            return False, {}, error_msg

    except requests.exceptions.Timeout:
        error_msg = f"Timeout na requisição para {url}"
        logger.error(error_msg)
        return False, {}, error_msg
    except requests.exceptions.ConnectionError:
        error_msg = f"Não foi possível conectar ao backend em {get_api_url()}"
        logger.error(error_msg)
        return False, {}, error_msg
    except Exception as e:
        error_msg = f"Erro inesperado: {str(e)}"
        logger.error(f"Unexpected error: {error_msg}")
        return False, {}, error_msg


def check_api_health() -> bool:
    """Verifica se a API está online"""
    cache_key = "api_health"
    cached_result = cache.get(cache_key)

    if cached_result is not None:
        return cached_result

    success, _, _ = make_api_request("health", timeout=5)
    cache.set(cache_key, success)
    return success


def get_api_status() -> Dict[str, Any]:
    """Obtém o status da API (online/offline)."""
    success, data, error = make_api_request("health")

    if success and data.get("status") == "healthy":
        return {
            "online": True,
            "version": data.get("version", "unknown"),
            "error": None,
        }
    else:
        return {
            "online": False,
            "error": error or "A API não respondeu como esperado.",
            "version": "unknown",
        }


# ============================================================================
# UTILITÁRIOS DE VALIDAÇÃO
# ============================================================================
def validate_file_upload(uploaded_file) -> Tuple[bool, str]:
    """Valida arquivo enviado"""
    if uploaded_file is None:
        return False, "Nenhum arquivo selecionado"

    # Verifica tamanho
    if uploaded_file.size > MAX_FILE_SIZE_BYTES:
        return False, get_messages()["file_too_large"]

    # Verifica extensão
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension not in SUPPORTED_FILE_EXTENSIONS:
        return False, get_messages()["unsupported_file_type"]

    return True, ""


def validate_chat_message(message: str) -> Tuple[bool, str]:
    """Valida mensagem de chat"""
    if not message or not message.strip():
        return False, "Mensagem não pode estar vazia"

    if len(message) > MAX_MESSAGE_LENGTH:
        return False, f"Mensagem muito longa. Máximo: {MAX_MESSAGE_LENGTH} caracteres"

    return True, ""


def validate_context_text(text: str) -> Tuple[bool, str]:
    """Valida texto de contexto"""
    if not text or not text.strip():
        return False, "Texto não pode estar vazio"

    if len(text) > MAX_CONTEXT_LENGTH:
        return False, f"Texto muito longo. Máximo: {MAX_CONTEXT_LENGTH} caracteres"

    return True, ""


# ============================================================================
# UTILITÁRIOS DE FORMATAÇÃO
# ============================================================================
def format_file_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo"""
    if size_bytes == 0:
        return "0B"

    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    float_size = float(size_bytes)
    while float_size >= 1024 and i < len(size_names) - 1:
        float_size /= 1024.0
        i += 1

    return f"{float_size:.1f}{size_names[i]}"


def format_duration(seconds: int) -> str:
    """Formata duração em segundos"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def format_confidence(confidence: float) -> str:
    """Formata nível de confiança"""
    if confidence >= CONFIDENCE_THRESHOLDS["high"]:
        return "🟢 Alta"
    elif confidence >= CONFIDENCE_THRESHOLDS["medium"]:
        return "🟡 Média"
    else:
        return "🔴 Baixa"


def format_timestamp(timestamp: str) -> str:
    """Formata timestamp"""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return timestamp


# ============================================================================
# UTILITÁRIOS DE UI
# ============================================================================
def show_success_message(message: str):
    """Mostra mensagem de sucesso"""
    st.success(message)


def show_error_message(message: str):
    """Mostra mensagem de erro"""
    st.error(message)


def show_warning_message(message: str):
    """Mostra mensagem de aviso"""
    st.warning(message)


def show_info_message(message: str):
    """Mostra mensagem informativa"""
    st.info(message)


def create_download_button(data: bytes, filename: str, label: str = "Download"):
    """Cria botão de download"""
    st.download_button(
        label=label, data=data, file_name=filename, mime="application/octet-stream"
    )


def create_progress_bar(progress: float, text: str = "Progresso"):
    """Cria barra de progresso"""
    st.progress(progress)
    st.write(f"{text}: {progress:.1%}")


def show_confidence_metric(confidence: float):
    """Mostra métrica de confiança"""
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Confiança", f"{confidence:.1%}")
    with col2:
        st.write(format_confidence(confidence))


def show_file_info(file_info: Dict[str, Any]):
    """Mostra informações do arquivo"""
    st.write(f"**Nome:** {file_info.get('name', 'N/A')}")
    st.write(f"**Tamanho:** {format_file_size(file_info.get('size', 0))}")
    st.write(f"**Tipo:** {file_info.get('type', 'N/A')}")
    st.write(f"**Status:** {file_info.get('status', 'N/A')}")


def create_files_dataframe(files: List[Dict]) -> pd.DataFrame:
    """Cria DataFrame com informações dos arquivos"""
    if not files:
        return pd.DataFrame()

    data = []
    for file in files:
        data.append(
            {
                "Nome": file.get("name", ""),
                "Tamanho": format_file_size(file.get("size", 0)),
                "Tipo": file.get("type", ""),
                "Status": file.get("status", ""),
                "Data": format_timestamp(file.get("upload_date", "")),
            }
        )

    return pd.DataFrame(data)


# ============================================================================
# UTILITÁRIOS DE DADOS
# ============================================================================
def get_file_type_icon(filename: str) -> str:
    """Obtém ícone baseado no tipo de arquivo"""
    extension = filename.split(".")[-1].lower()
    return get_supported_file_types().get(extension, "📄")


def get_whisper_model_description(model: str) -> str:
    """Obtém descrição do modelo Whisper"""
    return WHISPER_MODEL_DESCRIPTIONS.get(model, "Modelo desconhecido")


def get_model_options() -> List[str]:
    """Obtém opções de modelos disponíveis"""
    return DEFAULT_MODELS.copy()


def get_whisper_model_options() -> List[str]:
    """Obtém opções de modelos Whisper"""
    return get_whisper_models()


def get_ocr_language_options() -> List[str]:
    """Obtém opções de idiomas OCR"""
    return OCR_LANGUAGES.copy()


# ============================================================================
# UTILITÁRIOS DE CACHE E PERFORMANCE
# ============================================================================
def get_cached_data(key: str) -> Optional[Any]:
    """Obtém dados do cache"""
    return cache.get(key)


def set_cached_data(key: str, value: Any) -> None:
    """Define dados no cache"""
    cache.set(key, value)


def clear_cache() -> None:
    """Limpa o cache"""
    cache.clear()


def get_cache_stats() -> Dict[str, Any]:
    """Obtém estatísticas do cache"""
    return {
        "enabled": CACHE_ENABLED,
        "size": len(cache.cache),
        "max_size": cache.max_size,
        "ttl": cache.ttl,
    }


# ============================================================================
# UTILITÁRIOS DE DEBUG
# ============================================================================
def debug_info():
    """Mostra informações de debug"""
    if not is_debug_enabled():
        return

    with st.expander("🔧 Debug Info"):
        st.write("**Configurações:**")
        st.json(
            {
                "api_url": get_api_url(),
                "version": VERSION,
                "development_mode": is_development_mode(),
                "debug_enabled": is_debug_enabled(),
                "cache_enabled": CACHE_ENABLED,
            }
        )

        st.write("**Cache Stats:**")
        st.json(get_cache_stats())

        st.write("**Session State Keys:**")
        st.json(list(st.session_state.keys()))


def log_function_call(func_name: str, args: Optional[Dict[str, Any]] = None):
    """Log de chamada de função"""
    if is_debug_enabled():
        logger.debug(f"Function call: {func_name}, Args: {args}")


# ============================================================================
# UTILITÁRIOS DE VERSÃO E METADADOS
# ============================================================================
def get_version_info() -> Dict[str, str]:
    """Obtém informações de versão"""
    return {
        "version": VERSION,
        "build_date": BUILD_DATE,
        "author": AUTHOR,
        "email": EMAIL,
    }


def show_version_info():
    """Mostra informações de versão"""
    version_info = get_version_info()

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Informações da Versão:**")
    st.sidebar.markdown(f"📦 v{version_info['version']}")
    st.sidebar.markdown(f"📅 {version_info['build_date']}")
    st.sidebar.markdown(f"👨‍💻 {version_info['author']}")

    if is_debug_enabled():
        st.sidebar.markdown(f"🔧 Debug: Ativado")
        st.sidebar.markdown(f"🌐 API: {get_api_url()}")


# ============================================================================
# CLASSES DE AJUDA (MANTIDAS PARA COMPATIBILIDADE)
# ============================================================================
class APIHelper:
    """Classe para ajudar com chamadas da API (mantida para compatibilidade)"""

    @staticmethod
    def check_connection() -> bool:
        """Verifica se a API está online"""
        return check_api_health()

    @staticmethod
    def get_files() -> List[Dict]:
        """Obtém lista de arquivos"""
        success, data, _ = make_api_request("upload/files")
        if success:
            return data.get("files", [])
        return []

    @staticmethod
    def upload_file(file_data: bytes, filename: str) -> Optional[Dict]:
        """Faz upload de um arquivo"""
        files = {"file": (filename, file_data)}
        success, data, _ = make_api_request("upload/", method="POST", files=files)
        return data if success else None

    @staticmethod
    def get_context_info() -> Optional[Dict]:
        """Obtém informações do contexto"""
        success, data, _ = make_api_request("chat/context-info")
        return data if success else None

    @staticmethod
    def add_context(texts: List[str]) -> Optional[Dict]:
        """Adiciona contexto"""
        success, data, _ = make_api_request(
            "chat/add-context", method="POST", data={"texts": texts}
        )
        return data if success else None

    @staticmethod
    def chat(message: str) -> Optional[Dict]:
        """Envia mensagem para o chat"""
        success, data, _ = make_api_request(
            "chat/", method="POST", data={"text": message}
        )
        return data if success else None

    @staticmethod
    def get_models() -> List[Dict]:
        """Obtém modelos disponíveis"""
        success, data, _ = make_api_request("train/models")
        if success:
            return data.get("models", [])
        return []

    @staticmethod
    def train_model(
        model_name: str, dataset_path: str, output_dir: str
    ) -> Optional[Dict]:
        """Inicia treinamento"""
        data = {
            "model_name": model_name,
            "dataset_path": dataset_path,
            "output_dir": output_dir,
        }
        success, result, _ = make_api_request("train/", method="POST", data=data)
        return result if success else None

    @staticmethod
    def process_ocr_pdf(pdf_path: str, output_path: str) -> Optional[Dict]:
        """Processa OCR de PDF"""
        data = {"pdf_path": pdf_path, "output_path": output_path}
        success, result, _ = make_api_request(
            "preprocess/ocr-pdf", method="POST", data=data
        )
        return result if success else None

    @staticmethod
    def transcribe_audio(audio_path: str, model_size: str = "base") -> Optional[Dict]:
        """Transcreve áudio"""
        data = {"audio_path": audio_path, "model_size": model_size}
        success, result, _ = make_api_request(
            "preprocess/transcribe", method="POST", data=data
        )
        return result if success else None

    @staticmethod
    def transcribe_video(video_path: str) -> Optional[Dict]:
        """Transcreve vídeo"""
        data = {"video_path": video_path}
        success, result, _ = make_api_request(
            "preprocess/transcribe-video", method="POST", data=data
        )
        return result if success else None

    @staticmethod
    def ocr_image(image_path: str) -> Optional[Dict]:
        """Extrai texto de imagem"""
        data = {"image_path": image_path}
        success, result, _ = make_api_request(
            "preprocess/ocr-image", method="POST", data=data
        )
        return result if success else None


class UIHelper:
    """Classe para ajudar com a interface (mantida para compatibilidade)"""

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Formata tamanho de arquivo em formato legível"""
        return format_file_size(size_bytes)

    @staticmethod
    def get_file_icon(file_extension: str) -> str:
        """Retorna ícone baseado na extensão do arquivo"""
        return get_file_type_icon(f"file.{file_extension}")

    @staticmethod
    def create_files_dataframe(files: List[Dict]) -> pd.DataFrame:
        """Cria DataFrame com informações dos arquivos"""
        return create_files_dataframe(files)

    @staticmethod
    def show_confidence_metric(confidence: float):
        """Mostra métrica de confiança"""
        show_confidence_metric(confidence)

    @staticmethod
    def show_file_info(file_info: Dict):
        """Mostra informações do arquivo"""
        show_file_info(file_info)

    @staticmethod
    def show_upload_metrics(result: Dict):
        """Mostra métricas de upload"""
        if result:
            st.success("✅ Upload realizado com sucesso!")
            st.write(f"**Arquivo:** {result.get('filename', 'N/A')}")
            st.write(f"**Tamanho:** {format_file_size(result.get('size', 0))}")
            st.write(f"**Status:** {result.get('status', 'N/A')}")


class SessionHelper:
    """Classe para ajudar com sessão (mantida para compatibilidade)"""

    @staticmethod
    def init_session_state():
        """Inicializa o estado da sessão"""
        init_session_state()

    @staticmethod
    def add_chat_message(user_msg: str, bot_response: str):
        """Adiciona mensagem de chat"""
        add_chat_message("user", user_msg)
        add_chat_message("assistant", bot_response)

    @staticmethod
    def clear_chat_history():
        """Limpa histórico de chat"""
        clear_chat_history()

    @staticmethod
    def add_uploaded_file(file_info: Dict):
        """Adiciona arquivo enviado"""
        add_uploaded_file(file_info)

    @staticmethod
    def add_context_texts(texts: List[str]):
        """Adiciona textos de contexto"""
        for text in texts:
            add_context_text(text)

    @staticmethod
    def clear_context_texts():
        """Limpa textos de contexto"""
        clear_context_texts()


class ErrorHandler:
    """Classe para tratamento de erros (mantida para compatibilidade)"""

    @staticmethod
    def handle_api_error(error: Exception, operation: str = "operação"):
        """Trata erro da API"""
        show_error_message(f"Erro na {operation}: {str(error)}")

    @staticmethod
    def handle_connection_error():
        """Trata erro de conexão"""
        show_error_message(get_messages()["api_offline"])

    @staticmethod
    def handle_validation_error(error: str):
        """Trata erro de validação"""
        show_warning_message(f"Erro de validação: {error}")

    @staticmethod
    def show_success_message(message: str):
        """Mostra mensagem de sucesso"""
        show_success_message(message)

    @staticmethod
    def show_info_message(message: str):
        """Mostra mensagem informativa"""
        show_info_message(message)
