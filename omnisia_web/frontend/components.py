"""
Componentes reutilizáveis para o Frontend OmnisIA Trainer Web
"""

import streamlit as st
import requests
from typing import Dict, List, Optional, Any, Callable
import pandas as pd
from datetime import datetime

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


# ============================================================================
# CONFIGURAÇÃO INICIAL
# ============================================================================
def setup_page_config():
    """Configura a página do Streamlit"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    )


def setup_custom_css():
    """Configura CSS customizado"""
    st.markdown(
        """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #34495E;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #007BFF;
    }
    .success-card {
        background-color: #D4EDDA;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28A745;
    }
    .warning-card {
        background-color: #FFF3CD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FFC107;
    }
    .error-card {
        background-color: #F8D7DA;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #DC3545;
    }
    .info-card {
        background-color: #D1ECF1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17A2B8;
    }
    .sidebar-section {
        margin-bottom: 2rem;
    }
    .file-upload-area {
        border: 2px dashed #007BFF;
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        background-color: #F8F9FA;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.5rem;
    }
    .user-message {
        background-color: #007BFF;
        color: white;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #F8F9FA;
        border: 1px solid #DEE2E6;
        margin-right: 2rem;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# ============================================================================
# COMPONENTES DE NAVEGAÇÃO
# ============================================================================
def create_sidebar():
    """Cria a barra lateral com navegação"""
    st.sidebar.title("🤖 OmnisIA Trainer")

    # Navegação principal
    st.sidebar.markdown("### 📱 Navegação")
    selected_page = st.sidebar.selectbox(
        "Selecione uma página:", get_navigation_pages(), index=0
    )

    # Status da API
    st.sidebar.markdown("### 🌐 Status da API")
    api_online = check_api_health()
    if api_online:
        st.sidebar.success(get_messages()["api_online"])
    else:
        st.sidebar.error(get_messages()["api_offline_status"])

    # Links úteis
    st.sidebar.markdown("### 🔗 Links Úteis")
    for title, url in USEFUL_LINKS.items():
        if st.sidebar.button(title, key=f"link_{title}"):
            st.markdown(f"[{title}]({url})")

    # Informações de versão
    show_version_info()

    # Debug info (se habilitado)
    if is_debug_enabled():
        debug_info()

    return selected_page


def create_header(title: str, subtitle: str = ""):
    """Cria cabeçalho da página"""
    st.markdown(f"<h1 class='main-header'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='sub-header'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")


# ============================================================================
# COMPONENTES DE DASHBOARD
# ============================================================================
def create_dashboard():
    """Cria página do dashboard"""
    create_header("🏠 Dashboard", "Visão geral do sistema")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📁 Arquivos", len(get_uploaded_files()))

    with col2:
        st.metric("💬 Mensagens", len(get_chat_history()))

    with col3:
        st.metric("📝 Contextos", len(get_context_texts()))

    with col4:
        api_status = get_api_status()
        st.metric("🤖 Modelos", api_status.get("models_loaded", 0))

    # Status da API
    st.markdown("### 🌐 Status do Sistema")
    api_status = get_api_status()

    if api_status["online"]:
        st.markdown(
            """
        <div class="success-card">
            <h4>✅ Sistema Online</h4>
            <p><strong>Versão:</strong> {}</p>
            <p><strong>Uptime:</strong> {}</p>
            <p><strong>Modelos Carregados:</strong> {}</p>
            <p><strong>Arquivos Processados:</strong> {}</p>
        </div>
        """.format(
                api_status["version"],
                format_duration(api_status["uptime"]),
                api_status["models_loaded"],
                api_status["files_processed"],
            ),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
        <div class="error-card">
            <h4>❌ Sistema Offline</h4>
            <p><strong>Erro:</strong> {}</p>
        </div>
        """.format(
                api_status.get("error", "Desconhecido")
            ),
            unsafe_allow_html=True,
        )

    # Arquivos recentes
    st.markdown("### 📁 Arquivos Recentes")
    files = get_uploaded_files()
    if files:
        recent_files = files[-RECENT_FILES_LIMIT:]
        df = create_files_dataframe(recent_files)
        st.dataframe(df, use_container_width=True)
    else:
        st.info(get_messages()["no_files_found"])

    # Histórico de chat recente
    st.markdown("### 💬 Conversa Recente")
    chat_history = get_chat_history()
    if chat_history:
        recent_messages = chat_history[-5:]  # Últimas 5 mensagens
        for message in recent_messages:
            role = message["role"]
            content = message["content"]
            timestamp = format_timestamp(message["timestamp"])

            if role == "user":
                st.markdown(
                    f"""
                <div class="chat-message user-message">
                    <strong>Você:</strong> {content}<br>
                    <small>{timestamp}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                confidence = message.get("confidence", 1.0)
                st.markdown(
                    f"""
                <div class="chat-message bot-message">
                    <strong>Assistente:</strong> {content}<br>
                    <small>{timestamp} - {format_confidence(confidence)}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("Nenhuma conversa ainda")


# ============================================================================
# COMPONENTES DE UPLOAD
# ============================================================================
def create_upload_page():
    """Cria página de upload"""
    create_header("📤 Upload de Arquivos", "Envie arquivos para processamento")

    # Área de upload
    st.markdown("### 📁 Selecionar Arquivo")

    uploaded_file = st.file_uploader(
        "Escolha um arquivo para enviar:",
        type=SUPPORTED_FILE_EXTENSIONS,
        help=get_help_texts()["file_upload"],
    )

    if uploaded_file:
        # Validação
        is_valid, error_msg = validate_file_upload(uploaded_file)

        if is_valid:
            st.success(f"✅ Arquivo válido: {uploaded_file.name}")
            st.write(f"**Tamanho:** {format_file_size(uploaded_file.size)}")
            st.write(f"**Tipo:** {uploaded_file.type}")

            # Botão de upload
            if st.button("🚀 Enviar Arquivo"):
                with st.spinner("Enviando arquivo..."):
                    success, data, error = make_api_request(
                        "upload/",
                        method="POST",
                        files={"file": (uploaded_file.name, uploaded_file.getvalue())},
                    )

                    if success:
                        show_success_message(get_messages()["upload_success"])
                        add_uploaded_file(data)
                        st.json(data)
                    else:
                        show_error_message(f"Erro no upload: {error}")
        else:
            show_error_message(error_msg)

    # Lista de arquivos enviados
    st.markdown("### 📋 Arquivos Enviados")
    files = get_uploaded_files()
    if files:
        df = create_files_dataframe(files)
        st.dataframe(df, use_container_width=True)

        # Botão para limpar lista
        if st.button("🗑️ Limpar Lista"):
            st.session_state[SESSION_KEYS["uploaded_files"]] = []
            st.rerun()
    else:
        st.info(get_messages()["no_files_found"])


# ============================================================================
# COMPONENTES DE PRÉ-PROCESSAMENTO
# ============================================================================
def create_preprocessing_page():
    """Cria página de pré-processamento"""
    create_header("🔧 Pré-processamento", "Processe arquivos para extrair texto")

    # Seleção de arquivo
    files = get_uploaded_files()
    if not files:
        st.warning("Nenhum arquivo disponível. Faça upload primeiro.")
        return

    selected_file = st.selectbox(
        "Selecione um arquivo para processar:",
        [f["name"] for f in files],
        format_func=lambda x: f"{get_file_type_icon(x)} {x}",
    )

    if selected_file:
        file_info = next((f for f in files if f["name"] == selected_file), None)

        if file_info:
            st.markdown("### 📄 Informações do Arquivo")
            show_file_info(file_info)

            # Opções de processamento
            st.markdown("### ⚙️ Opções de Processamento")

            # OCR para PDFs e imagens
            if file_info["type"] in ["pdf", "jpg", "jpeg", "png", "gif"]:
                st.markdown("#### 🔍 OCR (Reconhecimento de Texto)")

                col1, col2 = st.columns(2)
                with col1:
                    ocr_language = st.selectbox(
                        "Idioma:",
                        get_ocr_language_options(),
                        index=0,
                        help="Idioma para reconhecimento de texto",
                    )

                with col2:
                    output_path = st.text_input(
                        "Arquivo de saída:",
                        value=get_placeholders()["output_path"],
                        help="Caminho para salvar o resultado",
                    )

                if st.button("🔍 Processar OCR"):
                    with st.spinner("Processando OCR..."):
                        data = {
                            "file_path": file_info["path"],
                            "output_path": output_path,
                            "language": ocr_language,
                        }
                        success, result, error = make_api_request(
                            "preprocess/ocr", method="POST", data=data
                        )

                        if success:
                            show_success_message(get_messages()["processing_success"])
                            st.json(result)
                        else:
                            show_error_message(f"Erro no OCR: {error}")

            # Transcrição para áudio
            if file_info["type"] in ["mp3", "wav"]:
                st.markdown("#### 🎵 Transcrição de Áudio")

                whisper_model = st.selectbox(
                    "Modelo Whisper:",
                    get_whisper_model_options(),
                    index=get_whisper_model_options().index(DEFAULT_WHISPER_MODEL),
                    format_func=lambda x: f"{x} - {get_whisper_model_description(x)}",
                    help=get_help_texts()["whisper_model"],
                )

                if st.button("🎵 Transcrever Áudio"):
                    with st.spinner("Transcrevendo áudio..."):
                        data = {"file_path": file_info["path"], "model": whisper_model}
                        success, result, error = make_api_request(
                            "preprocess/transcribe", method="POST", data=data
                        )

                        if success:
                            show_success_message(get_messages()["processing_success"])
                            st.json(result)
                        else:
                            show_error_message(f"Erro na transcrição: {error}")

            # Transcrição para vídeo
            if file_info["type"] in ["mp4", "avi", "mov"]:
                st.markdown("#### 🎬 Transcrição de Vídeo")

                if st.button("🎬 Transcrever Vídeo"):
                    with st.spinner("Transcrevendo vídeo..."):
                        data = {"file_path": file_info["path"]}
                        success, result, error = make_api_request(
                            "preprocess/transcribe-video", method="POST", data=data
                        )

                        if success:
                            show_success_message(get_messages()["processing_success"])
                            st.json(result)
                        else:
                            show_error_message(f"Erro na transcrição: {error}")


# ============================================================================
# COMPONENTES DE TREINAMENTO
# ============================================================================
def create_training_page():
    """Cria página de treinamento"""
    create_header("🎯 Treinamento de Modelos", "Treine modelos LoRA personalizados")

    # Configurações de treinamento
    st.markdown("### ⚙️ Configurações de Treinamento")

    col1, col2 = st.columns(2)

    with col1:
        model_name = st.selectbox(
            "Modelo Base:", get_model_options(), help="Modelo base para fine-tuning"
        )

        dataset_path = st.text_input(
            "Caminho do Dataset:",
            value=get_placeholders()["dataset_path"],
            help="Caminho para o arquivo de dados de treinamento",
        )

        output_dir = st.text_input(
            "Diretório de Saída:",
            value=TRAINING_CONFIG.get("output_dir", "data/models/lora_output"),
            help="Diretório para salvar o modelo treinado",
        )

    with col2:
        num_epochs = st.number_input(
            "Épocas:",
            min_value=1,
            max_value=100,
            value=TRAINING_CONFIG.get("num_train_epochs", 3),
            help="Número de épocas de treinamento",
        )

        batch_size = st.number_input(
            "Batch Size:",
            min_value=1,
            max_value=32,
            value=TRAINING_CONFIG.get("per_device_train_batch_size", 4),
            help="Tamanho do batch",
        )

        learning_rate = st.number_input(
            "Learning Rate:",
            min_value=1e-6,
            max_value=1e-2,
            value=TRAINING_CONFIG.get("learning_rate", 2e-4),
            format="%.6f",
            help="Taxa de aprendizado",
        )

    # Configurações LoRA
    st.markdown("### 🔧 Configurações LoRA")

    col1, col2, col3 = st.columns(3)

    with col1:
        lora_r = st.number_input(
            "Rank (r):",
            min_value=1,
            max_value=128,
            value=LORA_CONFIG.get("r", 16),
            help="Rank da decomposição LoRA",
        )

    with col2:
        lora_alpha = st.number_input(
            "Alpha:",
            min_value=1,
            max_value=128,
            value=LORA_CONFIG.get("lora_alpha", 32),
            help="Parâmetro alpha do LoRA",
        )

    with col3:
        lora_dropout = st.slider(
            "Dropout:",
            min_value=0.0,
            max_value=1.0,
            value=LORA_CONFIG.get("lora_dropout", 0.1),
            step=0.1,
            help="Taxa de dropout",
        )

    # Botão de treinamento
    if st.button("🚀 Iniciar Treinamento", type="primary"):
        if not model_name or not dataset_path or not output_dir:
            show_error_message("Preencha todos os campos obrigatórios")
        else:
            with st.spinner("Iniciando treinamento..."):
                training_config = {
                    "model_name": model_name,
                    "dataset_path": dataset_path,
                    "output_dir": output_dir,
                    "num_epochs": num_epochs,
                    "batch_size": batch_size,
                    "learning_rate": learning_rate,
                    "lora_config": {
                        "r": lora_r,
                        "lora_alpha": lora_alpha,
                        "lora_dropout": lora_dropout,
                        "target_modules": LORA_CONFIG.get(
                            "target_modules", ["q_proj", "v_proj"]
                        ),
                    },
                }

                success, result, error = make_api_request(
                    "train/", method="POST", data=training_config
                )

                if success:
                    show_success_message(get_messages()["training_success"])
                    st.json(result)
                else:
                    show_error_message(f"Erro no treinamento: {error}")

    # Status do treinamento
    st.markdown("### 📊 Status do Treinamento")

    if st.button("🔄 Atualizar Status"):
        success, status, error = make_api_request("train/status")

        if success:
            st.json(status)
        else:
            show_error_message(f"Erro ao obter status: {error}")


# ============================================================================
# COMPONENTES DE CHAT
# ============================================================================
def create_chat_page():
    """Cria página de chat"""
    create_header("💬 Chat com IA", "Converse com o modelo treinado")

    # Configurações do chat
    st.markdown("### ⚙️ Configurações")

    col1, col2 = st.columns(2)

    with col1:
        query_limit = st.number_input(
            "Limite de Resultados:",
            min_value=1,
            max_value=20,
            value=get_user_preferences().get("query_limit", DEFAULT_QUERY_LIMIT),
            help="Número máximo de resultados para busca",
        )

    with col2:
        embedding_model = st.selectbox(
            "Modelo de Embedding:",
            ["all-MiniLM-L6-v2", "all-mpnet-base-v2", "all-MiniLM-L12-v2"],
            index=0,
            help="Modelo para gerar embeddings",
        )

    # Contexto
    st.markdown("### 📝 Contexto")

    context_text = st.text_area(
        "Adicionar texto ao contexto:",
        placeholder=get_placeholders()["context_text"],
        help=get_help_texts()["chat_context"],
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Adicionar Contexto"):
            if context_text.strip():
                is_valid, error_msg = validate_context_text(context_text)
                if is_valid:
                    add_context_text(context_text)
                    show_success_message(get_messages()["context_added"])
                    st.rerun()
                else:
                    show_error_message(error_msg)
            else:
                show_error_message("Texto não pode estar vazio")

    with col2:
        if st.button("🗑️ Limpar Contexto"):
            clear_context_texts()
            show_success_message(get_messages()["context_cleared"])
            st.rerun()

    # Lista de contextos
    context_texts = get_context_texts()
    if context_texts:
        st.markdown("**Contextos ativos:**")
        for i, text in enumerate(context_texts):
            st.write(f"{i+1}. {text[:100]}{'...' if len(text) > 100 else ''}")
    else:
        st.info(get_messages()["no_context_found"])

    # Chat
    st.markdown("### 💬 Conversa")

    # Histórico de chat
    chat_history = get_chat_history()
    if chat_history:
        for message in chat_history:
            role = message["role"]
            content = message["content"]
            timestamp = format_timestamp(message["timestamp"])
            confidence = message.get("confidence", 1.0)

            if role == "user":
                st.markdown(
                    f"""
                <div class="chat-message user-message">
                    <strong>Você:</strong> {content}<br>
                    <small>{timestamp}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                <div class="chat-message bot-message">
                    <strong>Assistente:</strong> {content}<br>
                    <small>{timestamp} - {format_confidence(confidence)}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

    # Input de mensagem
    user_message = st.text_input(
        "Sua mensagem:",
        placeholder=get_placeholders()["chat_message"],
        key="chat_input",
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("💬 Enviar", type="primary"):
            if user_message.strip():
                is_valid, error_msg = validate_chat_message(user_message)
                if is_valid:
                    # Adiciona mensagem do usuário
                    add_chat_message("user", user_message)

                    # Envia para API
                    with st.spinner("Processando..."):
                        data = {
                            "text": user_message,
                            "context": context_texts,
                            "query_limit": query_limit,
                            "embedding_model": embedding_model,
                        }

                        success, response, error = make_api_request(
                            "chat/", method="POST", data=data
                        )

                        if success:
                            bot_response = response.get("response", "Sem resposta")
                            confidence = response.get("confidence", 1.0)
                            sources = response.get("sources", [])

                            add_chat_message(
                                "assistant", bot_response, confidence, sources
                            )
                            show_success_message(get_messages()["chat_success"])
                            st.rerun()
                        else:
                            show_error_message(f"Erro no chat: {error}")
                else:
                    show_error_message(error_msg)
            else:
                show_error_message("Mensagem não pode estar vazia")

    with col2:
        if st.button("🗑️ Limpar"):
            clear_chat_history()
            show_success_message(get_messages()["history_cleared"])
            st.rerun()


# ============================================================================
# COMPONENTES DE STATUS
# ============================================================================
def create_status_page():
    """Cria página de status"""
    create_header("📊 Status do Sistema", "Monitoramento e métricas")

    # Status da API
    st.markdown("### 🌐 Status da API")

    if st.button("🔄 Atualizar Status"):
        st.rerun()

    api_status = get_api_status()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if api_status["online"]:
            st.success("✅ Online")
        else:
            st.error("❌ Offline")

    with col2:
        st.metric("Versão", api_status["version"])

    with col3:
        st.metric("Uptime", format_duration(api_status["uptime"]))

    with col4:
        st.metric("Modelos", api_status["models_loaded"])

    # Detalhes do status
    if api_status["online"]:
        st.markdown(
            """
        <div class="success-card">
            <h4>✅ Sistema Funcionando</h4>
            <p>O backend está online e respondendo normalmente.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div class="error-card">
            <h4>❌ Sistema Offline</h4>
            <p><strong>Erro:</strong> {api_status.get("error", "Desconhecido")}</p>
            <p>Verifique se o backend está rodando em {get_api_url()}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Métricas do sistema
    st.markdown("### 📈 Métricas do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📁 Arquivos")
        files = get_uploaded_files()
        st.metric("Total", len(files))

        if files:
            file_types = {}
            for file in files:
                file_type = file.get("type", "unknown")
                file_types[file_type] = file_types.get(file_type, 0) + 1

            st.write("**Por tipo:**")
            for file_type, count in file_types.items():
                st.write(f"- {file_type}: {count}")

    with col2:
        st.markdown("#### 💬 Chat")
        chat_history = get_chat_history()
        st.metric("Mensagens", len(chat_history))

        if chat_history:
            user_messages = len([m for m in chat_history if m["role"] == "user"])
            bot_messages = len([m for m in chat_history if m["role"] == "assistant"])

            st.write(f"**Usuário:** {user_messages}")
            st.write(f"**Assistente:** {bot_messages}")

    # Cache stats
    st.markdown("### 🗄️ Cache")
    cache_stats = get_cache_stats()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Status", "✅ Ativo" if cache_stats["enabled"] else "❌ Inativo")

    with col2:
        st.metric("Itens", cache_stats["size"])

    with col3:
        st.metric("TTL", f"{cache_stats['ttl']}s")

    if st.button("🗑️ Limpar Cache"):
        clear_cache()
        show_success_message("Cache limpo!")
        st.rerun()

    # Informações de debug
    if is_debug_enabled():
        st.markdown("### 🔧 Debug Info")
        debug_info()


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================
def main():
    """Função principal da aplicação"""
    # Configuração inicial
    setup_page_config()
    setup_custom_css()
    init_session_state()

    # Sidebar
    selected_page = create_sidebar()

    # Navegação
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


if __name__ == "__main__":
    main()
