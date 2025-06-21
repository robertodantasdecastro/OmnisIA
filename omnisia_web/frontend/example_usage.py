"""
Exemplo de Uso das Configurações Centralizadas - OmnisIA Trainer Web

Este arquivo demonstra como usar todas as configurações centralizadas
definidas no arquivo config.py
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório atual ao path para importações
sys.path.append(str(Path(__file__).parent))

from config import (
    # Configurações da API
    API_URL,
    API_TIMEOUT,
    API_RETRY_ATTEMPTS,
    # Configurações da interface
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    INITIAL_SIDEBAR_STATE,
    THEME,
    # Configurações de upload
    MAX_FILE_SIZE_MB,
    MAX_FILE_SIZE_BYTES,
    SUPPORTED_FILE_TYPES,
    SUPPORTED_FILE_EXTENSIONS,
    # Configurações de chat
    MAX_CHAT_HISTORY,
    MAX_CONTEXT_LENGTH,
    MAX_MESSAGE_LENGTH,
    CONFIDENCE_THRESHOLDS,
    CHAT_REFRESH_INTERVAL,
    # Configurações de pré-processamento
    WHISPER_MODELS,
    DEFAULT_WHISPER_MODEL,
    WHISPER_MODEL_DESCRIPTIONS,
    OCR_LANGUAGES,
    DEFAULT_OCR_LANGUAGE,
    # Configurações de treinamento
    DEFAULT_MODELS,
    EMBEDDING_MODEL,
    DEFAULT_QUERY_LIMIT,
    LORA_CONFIG,
    TRAINING_CONFIG,
    # Configurações de métricas
    METRICS_REFRESH_INTERVAL,
    RECENT_FILES_LIMIT,
    DASHBOARD_UPDATE_INTERVAL,
    # Configurações de sessão
    SESSION_KEYS,
    # Configurações de UI
    UI_CONFIG,
    # Configurações de navegação
    NAVIGATION_PAGES,
    DEFAULT_PAGE,
    # Configurações de links úteis
    USEFUL_LINKS,
    # Configurações de mensagens
    MESSAGES,
    # Configurações de placeholders
    PLACEHOLDERS,
    # Configurações de ajuda
    HELP_TEXTS,
    # Configurações de log
    LOG_LEVEL,
    LOG_FILE,
    ENABLE_DEBUG,
    # Configurações de segurança
    SECRET_KEY,
    ALLOWED_HOSTS,
    CSRF_ENABLED,
    # Configurações de cache
    CACHE_ENABLED,
    CACHE_TTL,
    CACHE_MAX_SIZE,
    # Configurações de performance
    ENABLE_LAZY_LOADING,
    MAX_CONCURRENT_REQUESTS,
    REQUEST_TIMEOUT,
    # Configurações de versão
    VERSION,
    BUILD_DATE,
    AUTHOR,
    EMAIL,
    # Configurações de desenvolvimento
    DEVELOPMENT_MODE,
    ENABLE_HOT_RELOAD,
    SHOW_DEBUG_INFO,
    # Configurações de banco de dados (futuro)
    DATABASE_URL,
    DATABASE_POOL_SIZE,
    DATABASE_MAX_OVERFLOW,
    # Configurações de cache (futuro)
    REDIS_URL,
    REDIS_DB,
    REDIS_PASSWORD,
    # Funções de configuração
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

from utils import (
    # Utilitários de sessão
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
    # Utilitários de API
    check_api_health,
    get_api_status,
    make_api_request,
    # Utilitários de validação
    validate_file_upload,
    validate_chat_message,
    validate_context_text,
    # Utilitários de formatação
    format_file_size,
    format_duration,
    format_confidence,
    format_timestamp,
    # Utilitários de UI
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
    # Utilitários de cache e performance
    get_cached_data,
    set_cached_data,
    clear_cache,
    get_cache_stats,
    # Utilitários de debug
    debug_info,
    log_function_call,
    get_version_info,
    show_version_info,
)


def example_api_configuration():
    """Exemplo de uso das configurações da API"""
    print("=== CONFIGURAÇÕES DA API ===")
    print(f"URL da API: {get_api_url()}")
    print(f"Timeout: {API_TIMEOUT} segundos")
    print(f"Tentativas de retry: {API_RETRY_ATTEMPTS}")

    # Verificar se a API está online
    if check_api_health():
        print("✅ API está online")
        status = get_api_status()
        print(f"Versão: {status['version']}")
        print(f"Uptime: {format_duration(status['uptime'])}")
    else:
        print("❌ API está offline")


def example_interface_configuration():
    """Exemplo de uso das configurações da interface"""
    print("\n=== CONFIGURAÇÕES DA INTERFACE ===")
    print(f"Título da página: {PAGE_TITLE}")
    print(f"Ícone: {PAGE_ICON}")
    print(f"Layout: {LAYOUT}")
    print(f"Estado inicial da sidebar: {INITIAL_SIDEBAR_STATE}")
    print(f"Tema: {THEME}")

    print("\nCores da UI:")
    for key, value in UI_CONFIG.items():
        print(f"  {key}: {value}")


def example_upload_configuration():
    """Exemplo de uso das configurações de upload"""
    print("\n=== CONFIGURAÇÕES DE UPLOAD ===")
    print(
        f"Tamanho máximo: {MAX_FILE_SIZE_MB}MB ({format_file_size(MAX_FILE_SIZE_BYTES)})"
    )

    print("\nTipos de arquivo suportados:")
    for extension, icon in get_supported_file_types().items():
        print(f"  {extension}: {icon}")

    print(f"\nExtensões suportadas: {', '.join(SUPPORTED_FILE_EXTENSIONS)}")


def example_chat_configuration():
    """Exemplo de uso das configurações de chat"""
    print("\n=== CONFIGURAÇÕES DE CHAT ===")
    print(f"Histórico máximo: {MAX_CHAT_HISTORY} mensagens")
    print(f"Comprimento máximo de contexto: {MAX_CONTEXT_LENGTH} caracteres")
    print(f"Comprimento máximo de mensagem: {MAX_MESSAGE_LENGTH} caracteres")
    print(f"Intervalo de refresh: {CHAT_REFRESH_INTERVAL} segundos")

    print("\nLimites de confiança:")
    for level, threshold in CONFIDENCE_THRESHOLDS.items():
        print(f"  {level}: {threshold}")


def example_preprocessing_configuration():
    """Exemplo de uso das configurações de pré-processamento"""
    print("\n=== CONFIGURAÇÕES DE PRÉ-PROCESSAMENTO ===")

    print("Modelos Whisper disponíveis:")
    for model in get_whisper_models():
        description = get_whisper_model_description(model)
        default_mark = " (padrão)" if model == DEFAULT_WHISPER_MODEL else ""
        print(f"  {model}{default_mark}: {description}")

    print(f"\nIdiomas OCR: {', '.join(get_ocr_language_options())}")
    print(f"Idioma padrão: {DEFAULT_OCR_LANGUAGE}")


def example_training_configuration():
    """Exemplo de uso das configurações de treinamento"""
    print("\n=== CONFIGURAÇÕES DE TREINAMENTO ===")

    print("Modelos disponíveis:")
    for model in get_model_options():
        print(f"  {model}")

    print(f"\nModelo de embedding: {EMBEDDING_MODEL}")
    print(f"Limite de consulta padrão: {DEFAULT_QUERY_LIMIT}")

    print("\nConfiguração LoRA:")
    for key, value in LORA_CONFIG.items():
        print(f"  {key}: {value}")

    print("\nConfiguração de treinamento:")
    for key, value in TRAINING_CONFIG.items():
        print(f"  {key}: {value}")


def example_session_configuration():
    """Exemplo de uso das configurações de sessão"""
    print("\n=== CONFIGURAÇÕES DE SESSÃO ===")
    print("Chaves de sessão:")
    for key, value in SESSION_KEYS.items():
        print(f"  {key}: {value}")


def example_navigation_configuration():
    """Exemplo de uso das configurações de navegação"""
    print("\n=== CONFIGURAÇÕES DE NAVEGAÇÃO ===")
    print("Páginas disponíveis:")
    for page in get_navigation_pages():
        default_mark = " (padrão)" if page == DEFAULT_PAGE else ""
        print(f"  {page}{default_mark}")

    print("\nLinks úteis:")
    for title, url in USEFUL_LINKS.items():
        print(f"  {title}: {url}")


def example_messages_configuration():
    """Exemplo de uso das configurações de mensagens"""
    print("\n=== CONFIGURAÇÕES DE MENSAGENS ===")
    messages = get_messages()
    print("Mensagens do sistema:")
    for key, message in messages.items():
        # Mostra apenas as primeiras 50 caracteres para não poluir a saída
        preview = message[:50] + "..." if len(message) > 50 else message
        print(f"  {key}: {preview}")


def example_placeholders_configuration():
    """Exemplo de uso das configurações de placeholders"""
    print("\n=== CONFIGURAÇÕES DE PLACEHOLDERS ===")
    placeholders = get_placeholders()
    print("Placeholders disponíveis:")
    for key, placeholder in placeholders.items():
        print(f"  {key}: {placeholder}")


def example_help_configuration():
    """Exemplo de uso das configurações de ajuda"""
    print("\n=== CONFIGURAÇÕES DE AJUDA ===")
    help_texts = get_help_texts()
    print("Textos de ajuda:")
    for key, help_text in help_texts.items():
        # Mostra apenas as primeiras 50 caracteres para não poluir a saída
        preview = help_text[:50] + "..." if len(help_text) > 50 else help_text
        print(f"  {key}: {preview}")


def example_development_configuration():
    """Exemplo de uso das configurações de desenvolvimento"""
    print("\n=== CONFIGURAÇÕES DE DESENVOLVIMENTO ===")
    print(f"Modo desenvolvimento: {is_development_mode()}")
    print(f"Debug habilitado: {is_debug_enabled()}")
    print(f"Hot reload: {ENABLE_HOT_RELOAD}")
    print(f"Mostrar info de debug: {SHOW_DEBUG_INFO}")
    print(f"Nível de log: {LOG_LEVEL}")
    print(f"Arquivo de log: {LOG_FILE}")


def example_cache_configuration():
    """Exemplo de uso das configurações de cache"""
    print("\n=== CONFIGURAÇÕES DE CACHE ===")
    print(f"Cache habilitado: {CACHE_ENABLED}")
    print(f"TTL: {CACHE_TTL} segundos")
    print(f"Tamanho máximo: {CACHE_MAX_SIZE} itens")

    # Mostrar estatísticas do cache
    stats = get_cache_stats()
    print(f"Tamanho atual: {stats['size']} itens")


def example_performance_configuration():
    """Exemplo de uso das configurações de performance"""
    print("\n=== CONFIGURAÇÕES DE PERFORMANCE ===")
    print(f"Lazy loading: {ENABLE_LAZY_LOADING}")
    print(f"Requisições concorrentes máximas: {MAX_CONCURRENT_REQUESTS}")
    print(f"Timeout de requisição: {REQUEST_TIMEOUT} segundos")


def example_version_configuration():
    """Exemplo de uso das configurações de versão"""
    print("\n=== CONFIGURAÇÕES DE VERSÃO ===")
    version_info = get_version_info()
    print(f"Versão: {version_info['version']}")
    print(f"Data de build: {version_info['build_date']}")
    print(f"Autor: {version_info['author']}")
    print(f"Email: {version_info['email']}")


def example_security_configuration():
    """Exemplo de uso das configurações de segurança"""
    print("\n=== CONFIGURAÇÕES DE SEGURANÇA ===")
    print(
        f"Chave secreta: {SECRET_KEY[:10]}..." if len(SECRET_KEY) > 10 else SECRET_KEY
    )
    print(f"Hosts permitidos: {', '.join(ALLOWED_HOSTS)}")
    print(f"CSRF habilitado: {CSRF_ENABLED}")


def example_database_configuration():
    """Exemplo de uso das configurações de banco de dados"""
    print("\n=== CONFIGURAÇÕES DE BANCO DE DADOS ===")
    print(f"URL do banco: {DATABASE_URL}")
    print(f"Tamanho do pool: {DATABASE_POOL_SIZE}")
    print(f"Overflow máximo: {DATABASE_MAX_OVERFLOW}")


def example_redis_configuration():
    """Exemplo de uso das configurações de Redis"""
    print("\n=== CONFIGURAÇÕES DE REDIS ===")
    print(f"URL do Redis: {REDIS_URL}")
    print(f"Banco: {REDIS_DB}")
    print(f"Senha: {'***' if REDIS_PASSWORD else 'Não definida'}")


def example_environment_variables():
    """Exemplo de como definir variáveis de ambiente"""
    print("\n=== VARIÁVEIS DE AMBIENTE ===")
    print(
        "Para personalizar as configurações, defina as seguintes variáveis de ambiente:"
    )

    env_vars = [
        "API_URL=http://localhost:8000",
        "API_TIMEOUT=30",
        "MAX_FILE_SIZE_MB=100",
        "LOG_LEVEL=INFO",
        "ENABLE_DEBUG=false",
        "DEVELOPMENT_MODE=false",
        "SECRET_KEY=your-secret-key-here",
        "ALLOWED_HOSTS=localhost,127.0.0.1",
        "CACHE_ENABLED=true",
        "CACHE_TTL=300",
        "CACHE_MAX_SIZE=100",
    ]

    for var in env_vars:
        print(f"  {var}")


def main():
    """Função principal que executa todos os exemplos"""
    print("🤖 EXEMPLO DE USO DAS CONFIGURAÇÕES CENTRALIZADAS")
    print("=" * 60)

    # Executar todos os exemplos
    example_api_configuration()
    example_interface_configuration()
    example_upload_configuration()
    example_chat_configuration()
    example_preprocessing_configuration()
    example_training_configuration()
    example_session_configuration()
    example_navigation_configuration()
    example_messages_configuration()
    example_placeholders_configuration()
    example_help_configuration()
    example_development_configuration()
    example_cache_configuration()
    example_performance_configuration()
    example_version_configuration()
    example_security_configuration()
    example_database_configuration()
    example_redis_configuration()
    example_environment_variables()

    print("\n" + "=" * 60)
    print("✅ Todos os exemplos foram executados com sucesso!")
    print(
        "\n💡 Dica: Use as funções de configuração para acessar os valores de forma segura"
    )
    print(
        "   e sempre verifique se as variáveis de ambiente estão definidas corretamente."
    )


if __name__ == "__main__":
    main()
