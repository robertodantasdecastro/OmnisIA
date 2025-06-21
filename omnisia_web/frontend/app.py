"""
Aplicação Principal do Frontend OmnisIA Trainer Web
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path para importações
sys.path.append(str(Path(__file__).parent))

from config import (
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    INITIAL_SIDEBAR_STATE,
    THEME,
    NAVIGATION_PAGES,
    DEFAULT_PAGE,
    USEFUL_LINKS,
    MESSAGES,
    PLACEHOLDERS,
    HELP_TEXTS,
    UI_CONFIG,
    SESSION_KEYS,
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
    SUPPORTED_FILE_TYPES,
    SUPPORTED_FILE_EXTENSIONS,
    MAX_FILE_SIZE_MB,
    VERSION,
    BUILD_DATE,
    AUTHOR,
    EMAIL,
    DEVELOPMENT_MODE,
    ENABLE_DEBUG,
    SHOW_DEBUG_INFO,
    get_navigation_pages,
    get_messages,
    get_placeholders,
    get_help_texts,
    is_development_mode,
    is_debug_enabled,
    get_api_url,
)

from utils import (
    init_session_state,
    get_chat_history,
    add_chat_message,
    clear_chat_history,
    get_uploaded_files,
    add_uploaded_file,
    get_context_texts,
    add_context_text,
    clear_context_texts,
    get_user_preferences,
    update_user_preferences,
    check_api_health,
    get_api_status,
    make_api_request,
    validate_file_upload,
    validate_chat_message,
    validate_context_text,
    format_file_size,
    format_duration,
    format_confidence,
    format_timestamp,
    show_success_message,
    show_error_message,
    show_warning_message,
    show_info_message,
    create_download_button,
    create_progress_bar,
    show_confidence_metric,
    show_file_info,
    create_files_dataframe,
    get_file_type_icon,
    get_whisper_model_description,
    get_model_options,
    get_whisper_model_options,
    get_ocr_language_options,
    get_cached_data,
    set_cached_data,
    clear_cache,
    get_cache_stats,
    debug_info,
    log_function_call,
    get_version_info,
    show_version_info,
)

from components import (
    setup_page_config,
    setup_custom_css,
    create_sidebar,
    create_header,
    create_dashboard,
    create_upload_page,
    create_preprocessing_page,
    create_training_page,
    create_chat_page,
    create_status_page,
)


# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================
def initialize_app():
    """Inicializa a aplicação"""
    # Configuração da página
    setup_page_config()

    # CSS customizado
    setup_custom_css()

    # Estado da sessão
    init_session_state()

    # Log de inicialização
    if is_debug_enabled():
        log_function_call("initialize_app")


# ============================================================================
# FUNÇÕES DE NAVEGAÇÃO
# ============================================================================
def handle_navigation():
    """Gerencia a navegação entre páginas"""
    # Sidebar com navegação
    selected_page = create_sidebar()

    # Roteamento baseado na seleção
    if selected_page == "🏠 Dashboard":
        create_dashboard()
    elif selected_page == "📤 Upload":
        create_upload_page()
    elif selected_page == "🔧 Pré-processamento":
        create_preprocessing_page()
    elif selected_page == "🎯 Treinamento":
        create_training_page()
    elif selected_page == "💬 Chat":
        create_chat_page()
    elif selected_page == "📊 Status":
        create_status_page()
    else:
        st.error("Página não encontrada")
        st.info(f"Páginas disponíveis: {', '.join(get_navigation_pages())}")


# ============================================================================
# FUNÇÕES DE UTILIDADE
# ============================================================================
def show_app_info():
    """Mostra informações da aplicação"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Sobre")
    st.sidebar.markdown(f"**Versão:** {VERSION}")
    st.sidebar.markdown(f"**Build:** {BUILD_DATE}")
    st.sidebar.markdown(f"**Autor:** {AUTHOR}")

    if is_debug_enabled():
        st.sidebar.markdown("### 🔧 Debug")
        st.sidebar.markdown("✅ Modo debug ativado")
        st.sidebar.markdown(f"🌐 API: {get_api_url()}")
        cache_stats = get_cache_stats()
        st.sidebar.markdown(
            f"📁 Cache: {'✅' if cache_stats.get('enabled', False) else '❌'}"
        )


def handle_errors():
    """Trata erros globais"""
    try:
        # Verifica se há erros na sessão
        if "error" in st.session_state:
            show_error_message(st.session_state["error"])
            del st.session_state["error"]
    except Exception as e:
        if is_debug_enabled():
            st.error(f"Erro na aplicação: {str(e)}")


def cleanup_session():
    """Limpa dados da sessão se necessário"""
    try:
        # Limpa histórico antigo se exceder o limite
        chat_history = get_chat_history()
        if len(chat_history) > MAX_CHAT_HISTORY:
            st.session_state[SESSION_KEYS["chat_history"]] = chat_history[
                -MAX_CHAT_HISTORY:
            ]

        # Limpa cache se necessário
        cache_stats = get_cache_stats()
        if cache_stats.get("size", 0) > cache_stats.get("max_size", 100):
            clear_cache()

    except Exception as e:
        if is_debug_enabled():
            log_function_call("cleanup_session", {"error": str(e)})


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    """Função principal da aplicação"""
    try:
        # Inicialização
        initialize_app()

        # Tratamento de erros
        handle_errors()

        # Navegação
        handle_navigation()

        # Informações da aplicação
        show_app_info()

        # Limpeza da sessão
        cleanup_session()

    except Exception as e:
        st.error(f"Erro crítico na aplicação: {str(e)}")
        if is_debug_enabled():
            st.exception(e)


# ============================================================================
# EXECUÇÃO
# ============================================================================
if __name__ == "__main__":
    main()
