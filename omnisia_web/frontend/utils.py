"""
Utilitários para o Frontend OmnisIA Trainer Web
"""

import requests
import streamlit as st
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import pandas as pd
from .config import API_URL, API_TIMEOUT, MESSAGES


class APIHelper:
    """Classe para ajudar com chamadas da API"""

    @staticmethod
    def check_connection() -> bool:
        """Verifica se a API está online"""
        try:
            response = requests.get(f"{API_URL}/", timeout=5)
            return response.status_code == 200
        except:
            return False

    @staticmethod
    def get_files() -> List[Dict]:
        """Obtém lista de arquivos"""
        try:
            response = requests.get(f"{API_URL}/upload/files", timeout=API_TIMEOUT)
            if response.status_code == 200:
                return response.json()["files"]
            return []
        except:
            return []

    @staticmethod
    def upload_file(file_data: bytes, filename: str) -> Optional[Dict]:
        """Faz upload de um arquivo"""
        try:
            files = {"file": (filename, file_data)}
            response = requests.post(
                f"{API_URL}/upload/", files=files, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def get_context_info() -> Optional[Dict]:
        """Obtém informações do contexto"""
        try:
            response = requests.get(f"{API_URL}/chat/context-info", timeout=API_TIMEOUT)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def add_context(texts: List[str]) -> Optional[Dict]:
        """Adiciona contexto"""
        try:
            response = requests.post(
                f"{API_URL}/chat/add-context", json=texts, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def chat(message: str) -> Optional[Dict]:
        """Envia mensagem para o chat"""
        try:
            response = requests.post(
                f"{API_URL}/chat/", json={"text": message}, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def get_models() -> List[Dict]:
        """Obtém modelos disponíveis"""
        try:
            response = requests.get(f"{API_URL}/train/models", timeout=API_TIMEOUT)
            if response.status_code == 200:
                return response.json()["models"]
            return []
        except:
            return []

    @staticmethod
    def train_model(
        model_name: str, dataset_path: str, output_dir: str
    ) -> Optional[Dict]:
        """Inicia treinamento"""
        try:
            data = {
                "model_name": model_name,
                "dataset_path": dataset_path,
                "output_dir": output_dir,
            }
            response = requests.post(
                f"{API_URL}/train/", json=data, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def process_ocr_pdf(pdf_path: str, output_path: str) -> Optional[Dict]:
        """Processa OCR de PDF"""
        try:
            data = {"pdf_path": pdf_path, "output_path": output_path}
            response = requests.post(
                f"{API_URL}/preprocess/ocr-pdf", json=data, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def transcribe_audio(audio_path: str, model_size: str = "base") -> Optional[Dict]:
        """Transcreve áudio"""
        try:
            data = {"audio_path": audio_path, "model_size": model_size}
            response = requests.post(
                f"{API_URL}/preprocess/transcribe", json=data, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def transcribe_video(video_path: str) -> Optional[Dict]:
        """Transcreve vídeo"""
        try:
            data = {"video_path": video_path}
            response = requests.post(
                f"{API_URL}/preprocess/transcribe-video", json=data, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    @staticmethod
    def ocr_image(image_path: str) -> Optional[Dict]:
        """Extrai texto de imagem"""
        try:
            data = {"image_path": image_path}
            response = requests.post(
                f"{API_URL}/preprocess/ocr-image", json=data, timeout=API_TIMEOUT
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None


class UIHelper:
    """Classe para ajudar com a interface"""

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Formata tamanho de arquivo em formato legível"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f}{size_names[i]}"

    @staticmethod
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

    @staticmethod
    def create_files_dataframe(files: List[Dict]) -> pd.DataFrame:
        """Cria DataFrame para visualização de arquivos"""
        df_data = []
        for file_info in files:
            icon = UIHelper.get_file_icon(Path(file_info["filename"]).suffix)
            size = UIHelper.format_file_size(file_info["size"])
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
        return pd.DataFrame(df_data)

    @staticmethod
    def show_confidence_metric(confidence: float):
        """Mostra métrica de confiança com cores apropriadas"""
        if confidence > 0.7:
            st.success(f"🎯 Confiança: {confidence:.2f}")
        elif confidence > 0.4:
            st.warning(f"⚠️ Confiança: {confidence:.2f}")
        else:
            st.error(f"❌ Confiança: {confidence:.2f}")

    @staticmethod
    def show_file_info(file_info: Dict):
        """Mostra informações de um arquivo"""
        icon = UIHelper.get_file_icon(Path(file_info["filename"]).suffix)
        size = UIHelper.format_file_size(file_info["size"])
        st.info(f"{icon} **{file_info['filename']}** ({size})")

    @staticmethod
    def show_upload_metrics(result: Dict):
        """Mostra métricas de upload"""
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nome", result["filename"])
        with col2:
            st.metric("Tamanho", UIHelper.format_file_size(result["size"]))
        with col3:
            st.metric("Status", "✅ Sucesso")


class SessionHelper:
    """Classe para ajudar com o gerenciamento de sessão"""

    @staticmethod
    def init_session_state():
        """Inicializa variáveis de sessão"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
        if "context_texts" not in st.session_state:
            st.session_state.context_texts = []
        if "user_preferences" not in st.session_state:
            st.session_state.user_preferences = {}

    @staticmethod
    def add_chat_message(user_msg: str, bot_response: str):
        """Adiciona mensagem ao histórico de chat"""
        st.session_state.chat_history.append((user_msg, bot_response))
        # Manter apenas as últimas 50 mensagens
        if len(st.session_state.chat_history) > 50:
            st.session_state.chat_history = st.session_state.chat_history[-50:]

    @staticmethod
    def clear_chat_history():
        """Limpa histórico de chat"""
        st.session_state.chat_history.clear()

    @staticmethod
    def add_uploaded_file(file_info: Dict):
        """Adiciona arquivo à lista de uploads"""
        st.session_state.uploaded_files.append(file_info)

    @staticmethod
    def add_context_texts(texts: List[str]):
        """Adiciona textos ao contexto"""
        st.session_state.context_texts.extend(texts)

    @staticmethod
    def clear_context_texts():
        """Limpa textos do contexto"""
        st.session_state.context_texts.clear()


class ErrorHandler:
    """Classe para tratamento de erros"""

    @staticmethod
    def handle_api_error(error: Exception, operation: str = "operação"):
        """Trata erros da API"""
        st.error(f"❌ Erro na {operation}: {str(error)}")

    @staticmethod
    def handle_connection_error():
        """Trata erros de conexão"""
        st.error("❌ Erro na conexão com a API. Verifique se o backend está rodando.")

    @staticmethod
    def handle_validation_error(error: str):
        """Trata erros de validação"""
        st.warning(f"⚠️ {error}")

    @staticmethod
    def show_success_message(message: str):
        """Mostra mensagem de sucesso"""
        st.success(f"✅ {message}")

    @staticmethod
    def show_info_message(message: str):
        """Mostra mensagem informativa"""
        st.info(f"ℹ️ {message}")
