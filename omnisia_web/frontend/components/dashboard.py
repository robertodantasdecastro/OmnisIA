"""
Dashboard Principal do OmnisIA Trainer Web
Main Dashboard for OmnisIA Trainer Web

Dashboard moderno e responsivo com múltiplas funcionalidades
Modern and responsive dashboard with multiple features
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import asyncio
import logging

from ..utils.api_client import APIClient
from ..utils.metrics import MetricsCollector
from ..utils.notifications import NotificationManager
from .ai_assistant import AIAssistant

logger = logging.getLogger("omnisia.dashboard")


class ModernDashboard:
    """
    Dashboard principal com design moderno e responsivo
    Main dashboard with modern and responsive design
    """

    def __init__(self):
        self.api_client = APIClient()
        self.metrics = MetricsCollector()
        self.notifications = NotificationManager()
        self.ai_assistant = AIAssistant()

        # Configuração de tema
        self._setup_theme()

    def _setup_theme(self):
        """Configura tema moderno / Setup modern theme"""
        st.set_page_config(
            page_title="OmnisIA Trainer Web",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        # CSS customizado para design moderno
        st.markdown(
            """
        <style>
        /* Tema principal */
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #667eea;
            margin-bottom: 1rem;
            transition: transform 0.2s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
            display: inline-block;
        }
        
        .status-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-warning {
            background-color: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .status-error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .sidebar-section {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .action-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
            margin-bottom: 0.5rem;
        }
        
        .action-button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .main-header {
                padding: 0.75rem;
                margin-bottom: 1rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def render_header(self):
        """Renderiza cabeçalho principal / Render main header"""
        st.markdown(
            """
        <div class="main-header">
            <h1>🤖 OmnisIA Trainer Web</h1>
            <p>Plataforma Avançada de Treinamento de IA com Múltiplos Modelos</p>
            <p><em>Advanced AI Training Platform with Multiple Models</em></p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    def render_sidebar(self):
        """Renderiza barra lateral / Render sidebar"""
        with st.sidebar:
            st.markdown("### 🎛️ Painel de Controle")
            st.markdown("*Control Panel*")

            # Status do sistema
            self._render_system_status()

            # Ações rápidas
            self._render_quick_actions()

            # Configurações
            self._render_settings()

            # AI Assistant
            self._render_ai_assistant_sidebar()

    def _render_system_status(self):
        """Renderiza status do sistema / Render system status"""
        st.markdown("#### 📊 Status do Sistema")
        st.markdown("*System Status*")

        # Obter status dos serviços
        try:
            status = asyncio.run(self.api_client.get_system_status())

            # API Status
            api_status = status.get("api", {}).get("status", "unknown")
            api_badge = self._get_status_badge(api_status)
            st.markdown(f"**API:** {api_badge}", unsafe_allow_html=True)

            # Database Status
            db_status = status.get("database", {}).get("status", "unknown")
            db_badge = self._get_status_badge(db_status)
            st.markdown(f"**Database:** {db_badge}", unsafe_allow_html=True)

            # Models Status
            models_status = status.get("models", {}).get("status", "unknown")
            models_badge = self._get_status_badge(models_status)
            st.markdown(f"**Models:** {models_badge}", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Erro ao obter status: {str(e)}")

    def _get_status_badge(self, status: str) -> str:
        """Gera badge de status / Generate status badge"""
        if status == "healthy":
            return '<span class="status-badge status-success">✅ Online</span>'
        elif status == "warning":
            return '<span class="status-badge status-warning">⚠️ Atenção</span>'
        else:
            return '<span class="status-badge status-error">❌ Offline</span>'

    def _render_quick_actions(self):
        """Renderiza ações rápidas / Render quick actions"""
        st.markdown("#### ⚡ Ações Rápidas")
        st.markdown("*Quick Actions*")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📁 Upload", help="Fazer upload de arquivos"):
                st.switch_page("pages/upload.py")

            if st.button("🧠 Treinar", help="Iniciar treinamento"):
                st.switch_page("pages/training.py")

        with col2:
            if st.button("💬 Chat", help="Chat com IA"):
                st.switch_page("pages/chat.py")

            if st.button("📊 Métricas", help="Ver métricas"):
                st.switch_page("pages/metrics.py")

    def _render_settings(self):
        """Renderiza configurações / Render settings"""
        st.markdown("#### ⚙️ Configurações")
        st.markdown("*Settings*")

        # Tema
        theme = st.selectbox(
            "Tema / Theme",
            ["light", "dark", "auto"],
            help="Escolha o tema da interface",
        )

        # Idioma
        language = st.selectbox(
            "Idioma / Language",
            ["pt-BR", "en-US"],
            help="Escolha o idioma da interface",
        )

        # Notificações
        notifications = st.checkbox(
            "Notificações / Notifications",
            value=True,
            help="Ativar notificações do sistema",
        )

        # Salvar configurações
        if st.button("💾 Salvar", help="Salvar configurações"):
            self._save_settings(
                {"theme": theme, "language": language, "notifications": notifications}
            )

    def _render_ai_assistant_sidebar(self):
        """Renderiza assistente IA na sidebar / Render AI assistant in sidebar"""
        st.markdown("#### 🤖 Assistente IA")
        st.markdown("*AI Assistant*")

        if st.button("💡 Obter Ajuda", help="Conversar com assistente IA"):
            st.session_state["show_ai_assistant"] = True

    def render_main_content(self):
        """Renderiza conteúdo principal / Render main content"""
        # Métricas principais
        self._render_key_metrics()

        # Gráficos e análises
        col1, col2 = st.columns(2)

        with col1:
            self._render_training_progress()
            self._render_model_performance()

        with col2:
            self._render_usage_statistics()
            self._render_recent_activity()

        # Tabelas de dados
        self._render_data_tables()

    def _render_key_metrics(self):
        """Renderiza métricas principais / Render key metrics"""
        st.markdown("### 📈 Métricas Principais")
        st.markdown("*Key Metrics*")

        # Obter métricas
        try:
            metrics = asyncio.run(self.metrics.get_key_metrics())

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    label="Arquivos Processados",
                    value=metrics.get("files_processed", 0),
                    delta=metrics.get("files_delta", 0),
                    help="Total de arquivos processados hoje",
                )

            with col2:
                st.metric(
                    label="Modelos Treinados",
                    value=metrics.get("models_trained", 0),
                    delta=metrics.get("models_delta", 0),
                    help="Total de modelos treinados",
                )

            with col3:
                st.metric(
                    label="Conversas de Chat",
                    value=metrics.get("chat_conversations", 0),
                    delta=metrics.get("chat_delta", 0),
                    help="Total de conversas de chat",
                )

            with col4:
                st.metric(
                    label="Uso de CPU",
                    value=f"{metrics.get('cpu_usage', 0):.1f}%",
                    delta=f"{metrics.get('cpu_delta', 0):.1f}%",
                    help="Uso atual de CPU",
                )

        except Exception as e:
            st.error(f"Erro ao carregar métricas: {str(e)}")

    def _render_training_progress(self):
        """Renderiza progresso de treinamento / Render training progress"""
        st.markdown("#### 🎯 Progresso de Treinamento")
        st.markdown("*Training Progress*")

        try:
            # Dados simulados - substituir por dados reais
            progress_data = {
                "epoch": [1, 2, 3, 4, 5],
                "loss": [0.8, 0.6, 0.4, 0.3, 0.2],
                "accuracy": [0.6, 0.7, 0.8, 0.85, 0.9],
            }

            df = pd.DataFrame(progress_data)

            fig = make_subplots(
                rows=2,
                cols=1,
                subplot_titles=("Loss", "Accuracy"),
                vertical_spacing=0.1,
            )

            fig.add_trace(
                go.Scatter(x=df["epoch"], y=df["loss"], name="Loss"), row=1, col=1
            )

            fig.add_trace(
                go.Scatter(x=df["epoch"], y=df["accuracy"], name="Accuracy"),
                row=2,
                col=1,
            )

            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar progresso: {str(e)}")

    def _render_model_performance(self):
        """Renderiza performance dos modelos / Render model performance"""
        st.markdown("#### 🏆 Performance dos Modelos")
        st.markdown("*Model Performance*")

        try:
            # Dados simulados
            models_data = {
                "model": ["GPT-2", "DeepSeek", "Llama-2", "Local Model"],
                "accuracy": [0.85, 0.92, 0.88, 0.79],
                "speed": [120, 95, 110, 150],  # tokens/sec
            }

            df = pd.DataFrame(models_data)

            fig = px.scatter(
                df,
                x="speed",
                y="accuracy",
                text="model",
                size_max=60,
                title="Accuracy vs Speed",
                labels={"speed": "Speed (tokens/sec)", "accuracy": "Accuracy"},
            )

            fig.update_traces(textposition="top center")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar performance: {str(e)}")

    def _render_usage_statistics(self):
        """Renderiza estatísticas de uso / Render usage statistics"""
        st.markdown("#### 📊 Estatísticas de Uso")
        st.markdown("*Usage Statistics*")

        try:
            # Dados simulados
            usage_data = {
                "date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
                "requests": np.random.randint(50, 200, 30),
                "users": np.random.randint(10, 50, 30),
            }

            df = pd.DataFrame(usage_data)

            fig = px.line(
                df,
                x="date",
                y=["requests", "users"],
                title="Uso Diário da Plataforma",
                labels={"value": "Count", "date": "Data"},
            )

            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar estatísticas: {str(e)}")

    def _render_recent_activity(self):
        """Renderiza atividade recente / Render recent activity"""
        st.markdown("#### 🕒 Atividade Recente")
        st.markdown("*Recent Activity*")

        try:
            # Dados simulados
            activities = [
                {
                    "time": "2 min ago",
                    "action": "Arquivo processado",
                    "file": "document.pdf",
                },
                {
                    "time": "5 min ago",
                    "action": "Modelo treinado",
                    "model": "custom-gpt",
                },
                {"time": "10 min ago", "action": "Chat iniciado", "user": "user123"},
                {
                    "time": "15 min ago",
                    "action": "Upload concluído",
                    "file": "dataset.csv",
                },
                {"time": "20 min ago", "action": "Backup criado", "size": "2.3 GB"},
            ]

            for activity in activities:
                st.markdown(
                    f"""
                <div style="padding: 0.5rem; border-left: 3px solid #667eea; margin-bottom: 0.5rem; background: #f8f9fa;">
                    <strong>{activity['action']}</strong><br>
                    <small>{activity['time']}</small>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        except Exception as e:
            st.error(f"Erro ao carregar atividades: {str(e)}")

    def _render_data_tables(self):
        """Renderiza tabelas de dados / Render data tables"""
        st.markdown("### 📋 Dados Detalhados")
        st.markdown("*Detailed Data*")

        tab1, tab2, tab3 = st.tabs(["Arquivos", "Modelos", "Logs"])

        with tab1:
            self._render_files_table()

        with tab2:
            self._render_models_table()

        with tab3:
            self._render_logs_table()

    def _render_files_table(self):
        """Renderiza tabela de arquivos / Render files table"""
        try:
            # Dados simulados
            files_data = {
                "Nome": ["document1.pdf", "audio1.mp3", "image1.jpg", "dataset.csv"],
                "Tipo": ["PDF", "Audio", "Image", "CSV"],
                "Tamanho": ["2.3 MB", "15.2 MB", "1.1 MB", "45.7 MB"],
                "Status": ["Processado", "Processando", "Processado", "Pendente"],
                "Data": ["2024-01-15", "2024-01-15", "2024-01-14", "2024-01-14"],
            }

            df = pd.DataFrame(files_data)
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar arquivos: {str(e)}")

    def _render_models_table(self):
        """Renderiza tabela de modelos / Render models table"""
        try:
            # Dados simulados
            models_data = {
                "Nome": [
                    "custom-gpt-1",
                    "deepseek-fine",
                    "llama-custom",
                    "local-model",
                ],
                "Tipo": ["GPT-2", "DeepSeek", "Llama-2", "Custom"],
                "Status": ["Treinado", "Treinando", "Treinado", "Erro"],
                "Accuracy": [0.85, 0.92, 0.88, 0.0],
                "Época": [10, 5, 8, 0],
            }

            df = pd.DataFrame(models_data)
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar modelos: {str(e)}")

    def _render_logs_table(self):
        """Renderiza tabela de logs / Render logs table"""
        try:
            # Dados simulados
            logs_data = {
                "Timestamp": [
                    "2024-01-15 10:30:00",
                    "2024-01-15 10:25:00",
                    "2024-01-15 10:20:00",
                ],
                "Level": ["INFO", "WARNING", "ERROR"],
                "Message": [
                    "Arquivo processado com sucesso",
                    "Memória baixa detectada",
                    "Falha na conexão com API",
                ],
            }

            df = pd.DataFrame(logs_data)
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao carregar logs: {str(e)}")

    def _save_settings(self, settings: Dict[str, Any]):
        """Salva configurações / Save settings"""
        try:
            # Implementar salvamento de configurações
            st.success("Configurações salvas com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar configurações: {str(e)}")

    def render(self):
        """Renderiza dashboard completo / Render complete dashboard"""
        # Cabeçalho
        self.render_header()

        # Sidebar
        self.render_sidebar()

        # Conteúdo principal
        self.render_main_content()

        # AI Assistant modal
        if st.session_state.get("show_ai_assistant", False):
            self.ai_assistant.render_modal()


def main():
    """Função principal / Main function"""
    dashboard = ModernDashboard()
    dashboard.render()


if __name__ == "__main__":
    main()
