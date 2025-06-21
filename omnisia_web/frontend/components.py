"""
Componentes reutilizáveis para o Frontend OmnisIA Trainer Web
"""

import streamlit as st
import requests
from typing import Dict, List, Optional
from .utils import format_file_size, get_file_icon, show_confidence_metric


def file_upload_component(api_url: str):
    """Componente de upload de arquivos"""
    st.subheader("📤 Upload de Arquivo")

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
        file_icon = get_file_icon(uploaded_file.name)

        st.info(f"{file_icon} **{uploaded_file.name}** ({file_size})")

        if st.button("🚀 Enviar arquivo", type="primary"):
            with st.spinner("Enviando arquivo..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    response = requests.post(f"{api_url}/upload/", files=files)

                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ Arquivo enviado com sucesso!")

                        # Mostrar detalhes do upload
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Nome", result["filename"])
                        with col2:
                            st.metric("Tamanho", format_file_size(result["size"]))
                        with col3:
                            st.metric("Status", "✅ Sucesso")

                        return result
                    else:
                        st.error(f"❌ Erro: {response.text}")
                        return None
                except Exception as e:
                    st.error(f"❌ Erro na conexão: {str(e)}")
                    return None

    return None


def files_list_component(api_url: str):
    """Componente de lista de arquivos"""
    st.subheader("📁 Arquivos Enviados")

    if st.button("🔄 Atualizar lista"):
        try:
            response = requests.get(f"{api_url}/upload/files")
            if response.status_code == 200:
                files = response.json()["files"]
                if files:
                    # Criar DataFrame para melhor visualização
                    import pandas as pd
                    from datetime import datetime

                    df_data = []
                    for file_info in files:
                        icon = get_file_icon(file_info["filename"])
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

                    return files
                else:
                    st.info("Nenhum arquivo encontrado")
                    return []
            else:
                st.error("Erro ao listar arquivos")
                return []
        except Exception as e:
            st.error(f"Erro na conexão: {str(e)}")
            return []

    return []


def chat_component(api_url: str):
    """Componente de chat"""
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
                        f"{api_url}/chat/", json={"text": user_input}
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
                            show_confidence_metric(result["confidence"])

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


def context_component(api_url: str):
    """Componente de adição de contexto"""
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
                    response = requests.post(f"{api_url}/chat/add-context", json=texts)
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


def status_component(api_url: str):
    """Componente de status do sistema"""
    st.subheader("📊 Status do Sistema")

    # Status da API
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌐 Status da API")
        try:
            response = requests.get(f"{api_url}/", timeout=5)
            if response.status_code == 200:
                st.success("✅ API Backend: Online")
                st.json(response.json())
            else:
                st.error("❌ API Backend: Erro")
        except:
            st.error("❌ API Backend: Offline")
            st.info("💡 Verifique se o backend está rodando em http://localhost:8000")

    with col2:
        st.subheader("📚 Informações do Contexto")
        try:
            response = requests.get(f"{api_url}/chat/context-info")
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


def metrics_component(api_url: str):
    """Componente de métricas"""
    st.subheader("📈 Estatísticas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        try:
            response = requests.get(f"{api_url}/upload/files")
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
            response = requests.get(f"{api_url}/chat/context-info")
            if response.status_code == 200:
                info = response.json()
                st.metric("Contextos", info["total_texts"])
            else:
                st.metric("Contextos", "N/A")
        except:
            st.metric("Contextos", "N/A")

    with col3:
        try:
            response = requests.get(f"{api_url}/train/models")
            if response.status_code == 200:
                models = response.json()["models"]
                st.metric("Modelos", len(models))
            else:
                st.metric("Modelos", "N/A")
        except:
            st.metric("Modelos", "N/A")

    with col4:
        st.metric("Chat History", len(st.session_state.chat_history))
