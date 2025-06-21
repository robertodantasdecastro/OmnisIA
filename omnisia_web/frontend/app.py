import streamlit as st
import requests
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
from config import USEFUL_LINKS

# Configuração da página
st.set_page_config(
    page_title="OmnisIA Trainer Web",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configuração da API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configurações de sessão
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []
if "context_texts" not in st.session_state:
    st.session_state.context_texts = []


# Funções utilitárias
def check_api_connection() -> bool:
    """Verifica se a API está online"""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False


def format_file_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo em formato legível"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    return f"{size:.1f}{size_names[i]}"


def get_file_icon(file_extension: str) -> str:
    """Retorna ícone baseado na extensão do arquivo"""
    icons = {
        ".pdf": "📄",
        ".txt": "📝",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".png": "🖼️",
        ".gif": "🖼️",
        ".mp3": "🎵",
        ".wav": "🎵",
        ".mp4": "🎬",
        ".avi": "🎬",
        ".mov": "🎬",
    }
    return icons.get(file_extension.lower(), "📁")


# Interface principal
def main():
    st.title("🤖 OmnisIA Trainer Web")
    st.markdown(
        "Sistema web para ingestão, pré-processamento e treinamento generativo multimodal"
    )

    # Verificar conexão com API
    if not check_api_connection():
        st.error(
            "❌ Não foi possível conectar ao backend. Verifique se a API está rodando em http://localhost:8000"
        )
        st.stop()

    # Sidebar
    with st.sidebar:
        st.title("🧭 Navegação")
        page = st.selectbox(
            "Escolha uma página:",
            [
                "🏠 Dashboard",
                "📤 Upload",
                "🔧 Pré-processamento",
                "🎯 Treinamento",
                "💬 Chat",
                "📊 Status",
            ],
        )

        st.markdown("---")
        st.markdown("### 🔗 Links Úteis")
        for label, url in USEFUL_LINKS.items():
            st.markdown(f"- [{label}]({url})")

    # Navegação por páginas
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📤 Upload":
        show_upload_page()
    elif page == "🔧 Pré-processamento":
        show_preprocessing_page()
    elif page == "🎯 Treinamento":
        show_training_page()
    elif page == "💬 Chat":
        show_chat_page()
    elif page == "📊 Status":
        show_status_page()


def show_dashboard():
    """Página principal do dashboard"""
    st.header("🏠 Dashboard")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        try:
            response = requests.get(f"{API_URL}/upload/files")
            if response.status_code == 200:
                files = response.json()["files"]
                st.metric("📁 Arquivos", len(files))
            else:
                st.metric("📁 Arquivos", "N/A")
        except:
            st.metric("📁 Arquivos", "N/A")

    with col2:
        try:
            response = requests.get(f"{API_URL}/chat/context-info")
            if response.status_code == 200:
                info = response.json()
                st.metric("📚 Contextos", info["total_texts"])
            else:
                st.metric("📚 Contextos", "N/A")
        except:
            st.metric("📚 Contextos", "N/A")

    with col3:
        try:
            response = requests.get(f"{API_URL}/train/models")
            if response.status_code == 200:
                models = response.json()["models"]
                st.metric("🤖 Modelos", len(models))
            else:
                st.metric("🤖 Modelos", "N/A")
        except:
            st.metric("🤖 Modelos", "N/A")

    with col4:
        api_status = "🟢 Online" if check_api_connection() else "🔴 Offline"
        st.metric("🌐 API Status", api_status)

    # Ações rápidas
    st.subheader("⚡ Ações Rápidas")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📤 Upload Rápido", use_container_width=True):
            st.switch_page("📤 Upload")

    with col2:
        if st.button("💬 Chat Rápido", use_container_width=True):
            st.switch_page("💬 Chat")

    with col3:
        if st.button("📊 Ver Status", use_container_width=True):
            st.switch_page("📊 Status")

    # Atividade recente
    st.subheader("📈 Atividade Recente")
    try:
        response = requests.get(f"{API_URL}/upload/files")
        if response.status_code == 200:
            files = response.json()["files"]
            if files:
                # Ordenar por data de modificação
                files.sort(key=lambda x: x["modified"], reverse=True)
                recent_files = files[:5]

                for file_info in recent_files:
                    icon = get_file_icon(Path(file_info["filename"]).suffix)
                    size = format_file_size(file_info["size"])
                    date = datetime.fromtimestamp(file_info["modified"]).strftime(
                        "%d/%m/%Y %H:%M"
                    )
                    st.write(f"{icon} **{file_info['filename']}** ({size}) - {date}")
            else:
                st.info("Nenhum arquivo encontrado")
    except:
        st.warning("Não foi possível carregar arquivos recentes")


def show_upload_page():
    """Página de upload de arquivos"""
    st.header("📤 Upload de Arquivos")

    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "Escolha um arquivo para upload",
        type=[
            "pdf",
            "txt",
            "jpg",
            "jpeg",
            "png",
            "gif",
            "mp3",
            "wav",
            "mp4",
            "avi",
            "mov",
        ],
        help="Arquivos suportados: PDF, TXT, imagens (JPG, PNG, GIF), áudio (MP3, WAV), vídeo (MP4, AVI, MOV)",
    )

    if uploaded_file is not None:
        # Mostrar informações do arquivo
        file_size = format_file_size(len(uploaded_file.getvalue()))
        file_icon = get_file_icon(Path(uploaded_file.name).suffix)

        st.info(f"{file_icon} **{uploaded_file.name}** ({file_size})")

        if st.button("🚀 Enviar arquivo", type="primary"):
            with st.spinner("Enviando arquivo..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{API_URL}/upload/", files=files)

                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Arquivo enviado com sucesso!")

                        # Mostrar detalhes do upload
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Nome", result["filename"])
                        with col2:
                            st.metric("Tamanho", format_file_size(result["size"]))
                        with col3:
                            st.metric("Status", "✅ Sucesso")

                        # Adicionar à lista de arquivos
                        st.session_state.uploaded_files.append(result)

                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"❌ Erro na conexão: {str(e)}")

    # Lista de arquivos
    st.subheader("📁 Arquivos Enviados")

    if st.button("🔄 Atualizar lista"):
        try:
            response = requests.get(f"{API_URL}/upload/files")
            if response.status_code == 200:
                files = response.json()["files"]
                if files:
                    # Criar DataFrame para melhor visualização
                    df_data = []
                    for file_info in files:
                        icon = get_file_icon(Path(file_info["filename"]).suffix)
                        size = format_file_size(file_info["size"])
                        date = datetime.fromtimestamp(file_info["modified"]).strftime(
                            "%d/%m/%Y %H:%M"
                        )
                        df_data.append(
                            {
                                "Arquivo": f"{icon} {file_info['filename']}",
                                "Tamanho": size,
                                "Data": date,
                            }
                        )

                    df = pd.DataFrame(df_data)
                    st.dataframe(df, use_container_width=True)

                    # Estatísticas
                    total_size = sum(file_info["size"] for file_info in files)
                    st.info(
                        f"📊 Total: {len(files)} arquivos, {format_file_size(total_size)}"
                    )
                else:
                    st.info("Nenhum arquivo encontrado")
            else:
                st.error("Erro ao listar arquivos")
        except Exception as e:
            st.error(f"Erro na conexão: {str(e)}")


def show_preprocessing_page():
    """Página de pré-processamento"""
    st.header("🔧 Pré-processamento")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 OCR PDF", "🎵 Transcrição Áudio", "🎬 Transcrição Vídeo", "🖼️ OCR Imagem"]
    )

    with tab1:
        st.subheader("📄 OCR de PDF")
        col1, col2 = st.columns(2)

        with col1:
            pdf_path = st.text_input(
                "Caminho do PDF:", placeholder="data/uploads/documento.pdf"
            )
            output_path = st.text_input(
                "Caminho de saída:", value="data/output/documento_ocr.pdf"
            )

        with col2:
            st.info("💡 **Dica:** Use arquivos PDF que foram enviados via upload")
            if st.button("📋 Listar PDFs disponíveis"):
                try:
                    response = requests.get(f"{API_URL}/upload/files")
                    if response.status_code == 200:
                        files = response.json()["files"]
                        pdf_files = [
                            f for f in files if f["filename"].lower().endswith(".pdf")
                        ]
                        if pdf_files:
                            st.write("**PDFs disponíveis:**")
                            for pdf in pdf_files:
                                st.write(f"📄 {pdf['filename']}")
                        else:
                            st.warning("Nenhum PDF encontrado")
                except:
                    st.error("Erro ao listar arquivos")

        if st.button("🔍 Processar PDF", type="primary") and pdf_path:
            with st.spinner("Processando PDF com OCR..."):
                try:
                    response = requests.post(
                        f"{API_URL}/preprocess/ocr-pdf",
                        json={"pdf_path": pdf_path, "output_path": output_path},
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ PDF processado com sucesso!")
                        st.json(result)
                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")

    with tab2:
        st.subheader("🎵 Transcrição de Áudio")
        col1, col2 = st.columns(2)

        with col1:
            audio_path = st.text_input(
                "Caminho do áudio:", placeholder="data/uploads/audio.wav"
            )
            model_size = st.selectbox(
                "Tamanho do modelo:",
                ["tiny", "base", "small", "medium", "large"],
                help="Modelos maiores são mais precisos mas mais lentos",
            )

        with col2:
            st.info(
                "💡 **Modelos Whisper:**\n- tiny: Mais rápido, menos preciso\n- base: Equilibrado\n- large: Mais lento, mais preciso"
            )

        if st.button("🎤 Transcrever áudio", type="primary") and audio_path:
            with st.spinner(f"Transcrevendo áudio com modelo {model_size}..."):
                try:
                    response = requests.post(
                        f"{API_URL}/preprocess/transcribe",
                        json={"audio_path": audio_path, "model_size": model_size},
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Transcrição concluída!")

                        # Mostrar resultado
                        st.text_area("📝 Texto transcrito:", result["text"], height=200)

                        # Estatísticas
                        word_count = len(result["text"].split())
                        char_count = len(result["text"])
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Palavras", word_count)
                        with col2:
                            st.metric("Caracteres", char_count)
                        with col3:
                            st.metric("Modelo", model_size)
                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")

    with tab3:
        st.subheader("🎬 Transcrição de Vídeo")
        video_path = st.text_input(
            "Caminho do vídeo:", placeholder="data/uploads/video.mp4"
        )

        if st.button("🎬 Transcrever vídeo", type="primary") and video_path:
            with st.spinner("Extraindo áudio e transcrevendo vídeo..."):
                try:
                    response = requests.post(
                        f"{API_URL}/preprocess/transcribe-video",
                        json={"video_path": video_path},
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Transcrição de vídeo concluída!")
                        st.text_area("📝 Texto transcrito:", result["text"], height=200)
                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")

    with tab4:
        st.subheader("🖼️ OCR de Imagem")
        image_path = st.text_input(
            "Caminho da imagem:", placeholder="data/uploads/imagem.jpg"
        )

        if st.button("🔍 Extrair texto da imagem", type="primary") and image_path:
            with st.spinner("Processando imagem com OCR..."):
                try:
                    response = requests.post(
                        f"{API_URL}/preprocess/ocr-image",
                        json={"image_path": image_path},
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Texto extraído com sucesso!")
                        st.text_area("📝 Texto extraído:", result["text"], height=200)
                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")


def show_training_page():
    """Página de treinamento"""
    st.header("🎯 Treinamento LoRA")

    # Carregar modelos disponíveis
    models = []
    model_names = ["gpt2", "gpt2-medium", "gpt2-large"]
    model_descriptions = {}
    try:
        response = requests.get(f"{API_URL}/train/models")
        if response.status_code == 200:
            models = response.json()["models"]
            model_names = [model["name"] for model in models]
            model_descriptions = {
                model["name"]: model["description"] for model in models
            }
    except Exception:
        pass

    # Configurações de treinamento
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚙️ Configurações")
        model_name = st.selectbox("Modelo base:", model_names)
        if model_name in model_descriptions:
            st.info(f"📝 {model_descriptions[model_name]}")

        dataset_path = st.text_input(
            "Caminho do dataset:", placeholder="data/datasets/training_data.txt"
        )
        output_dir = st.text_input(
            "Diretório de saída:", value="data/models/lora_output"
        )

    with col2:
        st.subheader("📊 Informações")
        st.info(
            "💡 **LoRA (Low-Rank Adaptation):**\n- Treinamento eficiente\n- Poucos parâmetros\n- Rápido e leve"
        )

        if st.button("📋 Ver modelos disponíveis"):
            st.json(models)

    # Iniciar treinamento
    if st.button("🚀 Iniciar treinamento", type="primary") and dataset_path:
        with st.spinner("Iniciando treinamento LoRA..."):
            try:
                response = requests.post(
                    f"{API_URL}/train/",
                    json={
                        "model_name": model_name,
                        "dataset_path": dataset_path,
                        "output_dir": output_dir,
                    },
                )
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Treinamento concluído!")

                    # Mostrar resultados
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Modelo", model_name)
                    with col2:
                        st.metric("Status", "✅ Concluído")
                    with col3:
                        st.metric("Saída", output_dir)

                    st.json(result)
                else:
                    st.error(f"❌ Erro: {response.text}")
            except Exception as e:
                st.error(f"Erro na conexão: {str(e)}")


def show_chat_page():
    """Página de chat"""
    st.header("💬 Chat Inteligente")

    # Adicionar contexto
    with st.expander("📚 Adicionar Contexto", expanded=False):
        context_text = st.text_area(
            "Digite textos para adicionar ao contexto:",
            placeholder="Digite um texto por linha...",
            height=150,
        )

        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("➕ Adicionar contexto", type="primary") and context_text:
                texts = [
                    text.strip() for text in context_text.split("\n") if text.strip()
                ]
                try:
                    response = requests.post(f"{API_URL}/chat/add-context", json=texts)
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ {result['message']}")
                        st.session_state.context_texts.extend(texts)
                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")

        with col2:
            if st.button("🗑️ Limpar contexto"):
                st.session_state.context_texts.clear()
                st.success("Contexto limpo!")

    # Chat principal
    st.subheader("💭 Conversar")

    # Histórico de chat
    if st.session_state.chat_history:
        st.write("**Histórico da conversa:**")
        for i, (user_msg, bot_response) in enumerate(
            st.session_state.chat_history[-5:]
        ):
            st.write(f"👤 **Você:** {user_msg}")
            st.write(f"🤖 **IA:** {bot_response}")
            st.write("---")

    # Input do usuário
    user_input = st.text_input(
        "Digite sua mensagem:", placeholder="Faça uma pergunta..."
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("📤 Enviar", type="primary") and user_input:
            with st.spinner("Processando..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat/", json={"text": user_input}
                    )
                    if response.status_code == 200:
                        result = response.json()

                        # Adicionar ao histórico
                        st.session_state.chat_history.append(
                            (user_input, result["response"])
                        )

                        st.success("✅ Resposta recebida!")

                        # Mostrar resposta
                        st.write(f"🤖 **Resposta:** {result['response']}")

                        # Mostrar contexto usado
                        if result.get("context"):
                            with st.expander("📚 Contexto usado"):
                                for i, ctx in enumerate(result["context"], 1):
                                    st.write(f"{i}. {ctx[:200]}...")

                        # Mostrar confiança
                        if result.get("confidence"):
                            confidence = result["confidence"]
                            if confidence > 0.7:
                                st.success(f"🎯 Confiança: {confidence:.2f}")
                            elif confidence > 0.4:
                                st.warning(f"⚠️ Confiança: {confidence:.2f}")
                            else:
                                st.error(f"❌ Confiança: {confidence:.2f}")

                        # Rerun para atualizar o histórico
                        st.rerun()
                    else:
                        st.error(f"❌ Erro: {response.text}")
                except Exception as e:
                    st.error(f"Erro na conexão: {str(e)}")

    with col2:
        if st.button("🗑️ Limpar histórico"):
            st.session_state.chat_history.clear()
            st.success("Histórico limpo!")
            st.rerun()


def show_status_page():
    """Página de status do sistema"""
    st.header("📊 Status do Sistema")

    # Status da API
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌐 Status da API")
        api_status = check_api_connection()
        if api_status:
            st.success("✅ API Backend: Online")
            try:
                response = requests.get(f"{API_URL}/")
                if response.status_code == 200:
                    st.json(response.json())
            except:
                pass
        else:
            st.error("❌ API Backend: Offline")
            st.info("💡 Verifique se o backend está rodando em http://localhost:8000")

    with col2:
        st.subheader("📚 Informações do Contexto")
        try:
            response = requests.get(f"{API_URL}/chat/context-info")
            if response.status_code == 200:
                info = response.json()
                st.metric("Textos carregados", info["total_texts"])
                st.metric(
                    "Índice inicializado",
                    "✅ Sim" if info["index_initialized"] else "❌ Não",
                )
            else:
                st.warning("⚠️ Não foi possível obter informações do contexto")
        except:
            st.warning("⚠️ Não foi possível conectar ao contexto")

    # Estatísticas do sistema
    st.subheader("📈 Estatísticas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        try:
            response = requests.get(f"{API_URL}/upload/files")
            if response.status_code == 200:
                files = response.json()["files"]
                total_size = sum(file_info["size"] for file_info in files)
                st.metric("Arquivos", len(files))
                st.metric("Tamanho total", format_file_size(total_size))
            else:
                st.metric("Arquivos", "N/A")
        except:
            st.metric("Arquivos", "N/A")

    with col2:
        try:
            response = requests.get(f"{API_URL}/chat/context-info")
            if response.status_code == 200:
                info = response.json()
                st.metric("Contextos", info["total_texts"])
            else:
                st.metric("Contextos", "N/A")
        except:
            st.metric("Contextos", "N/A")

    with col3:
        try:
            response = requests.get(f"{API_URL}/train/models")
            if response.status_code == 200:
                models = response.json()["models"]
                st.metric("Modelos", len(models))
            else:
                st.metric("Modelos", "N/A")
        except:
            st.metric("Modelos", "N/A")

    with col4:
        st.metric("Chat History", len(st.session_state.chat_history))

    # Logs do sistema
    st.subheader("📋 Logs do Sistema")
    if st.button("🔄 Atualizar logs"):
        st.info("Logs atualizados em " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


# Executar aplicação
if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Desenvolvido com ❤️ para OmnisIA**")
with col2:
    st.markdown("**Versão:** 1.0.0")
with col3:
    st.markdown("**API:** " + API_URL)
