"""
🌐 OmnisIA Frontend
Interface Web com Streamlit para o sistema OmnisIA
"""

import streamlit as st
import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="🤖 OmnisIA - Sistema de IA Multimodal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações
API_BASE_URL = "http://localhost:8000"

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    .success-message {
        color: #28a745;
        font-weight: bold;
    }
    .error-message {
        color: #dc3545;
        font-weight: bold;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_connection():
    """Verifica conexão com a API"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_system_info():
    """Obtém informações do sistema"""
    try:
        response = requests.get(f"{API_BASE_URL}/info", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_models():
    """Obtém lista de modelos disponíveis"""
    try:
        response = requests.get(f"{API_BASE_URL}/models", timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def send_chat_message(message: str, model: str = "deepseek-r1"):
    """Envia mensagem para o chat"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={
                "message": message,
                "model": model,
                "temperature": 0.7,
                "max_tokens": 2000
            },
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao enviar mensagem: {e}")
    return None

def upload_file(file):
    """Faz upload de arquivo"""
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/upload",
            files=files,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro no upload: {e}")
    return None

def start_training(model_name: str, dataset_path: str, epochs: int = 3, batch_size: int = 2):
    """Inicia treinamento de modelo"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/training/start",
            json={
                "model_name": model_name,
                "dataset_path": dataset_path,
                "epochs": epochs,
                "batch_size": batch_size
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"Erro ao iniciar treinamento: {e}")
    return None

def main():
    """Função principal da interface"""
    
    # Cabeçalho
    st.markdown('<h1 class="main-header">🤖 OmnisIA - Sistema Integrado de IA Multimodal</h1>', unsafe_allow_html=True)
    
    # Verificar conexão com API
    if not check_api_connection():
        st.error("❌ Não foi possível conectar com a API. Verifique se o servidor está rodando.")
        st.info("Execute: `python main.py api` ou `python main.py full`")
        return
    
    # Sidebar com navegação
    st.sidebar.title("🔧 Navegação")
    page = st.sidebar.selectbox(
        "Escolha uma página:",
        [
            "🏠 Dashboard",
            "💬 Chat IA",
            "📁 Arquivos",
            "🎓 Treinamento",
            "🔧 Configurações",
            "📊 Status"
        ]
    )
    
    # Roteamento de páginas
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "💬 Chat IA":
        show_chat()
    elif page == "📁 Arquivos":
        show_files()
    elif page == "🎓 Treinamento":
        show_training()
    elif page == "🔧 Configurações":
        show_settings()
    elif page == "📊 Status":
        show_status()

def show_dashboard():
    """Página do dashboard principal"""
    st.header("🏠 Dashboard Principal")
    
    # Informações do sistema
    system_info = get_system_info()
    if system_info:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Versão do Sistema",
                system_info.get("version", "N/A")
            )
        
        with col2:
            st.metric(
                "Modelos Disponíveis",
                system_info.get("models_available", 0)
            )
        
        with col3:
            st.metric(
                "Banco de Dados",
                system_info.get("database", "N/A")
            )
        
        with col4:
            st.metric(
                "Status",
                "🟢 Online" if system_info else "🔴 Offline"
            )
        
        # Gráficos de exemplo
        st.subheader("📊 Estatísticas de Uso")
        
        # Gráfico de modelos
        if "features" in system_info:
            models_data = {
                "Tipo": ["Locais", "APIs", "Treinamento"],
                "Quantidade": [5, 8, 3]
            }
            df_models = pd.DataFrame(models_data)
            fig = px.bar(df_models, x="Tipo", y="Quantidade", title="Modelos Disponíveis por Tipo")
            st.plotly_chart(fig, use_container_width=True)
    
    # Cards informativos
    st.subheader("🚀 Recursos Principais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 Modelos de IA</h4>
            <p>• DeepSeek R1 (Recomendado)</p>
            <p>• Llama 3.1 8B, Mistral 7B</p>
            <p>• OpenAI GPT-4, Claude, Gemini</p>
            <p>• AWS Bedrock, Azure OpenAI</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>💾 Bancos de Dados</h4>
            <p>• PostgreSQL (Produção)</p>
            <p>• MongoDB (NoSQL)</p>
            <p>• Redis (Cache)</p>
            <p>• SQLite (Desenvolvimento)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🎓 Treinamento</h4>
            <p>• LoRA Fine-tuning avançado</p>
            <p>• Treinamento distribuído</p>
            <p>• Datasets customizados</p>
            <p>• Integração Kaggle/SageMaker</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🌐 Protocolos</h4>
            <p>• FTP/SFTP para arquivos</p>
            <p>• HTTP/HTTPS para downloads</p>
            <p>• WebDAV para sincronização</p>
            <p>• APIs REST para integração</p>
        </div>
        """, unsafe_allow_html=True)

def show_chat():
    """Página do chat com IA"""
    st.header("💬 Chat com Assistente IA")
    
    # Configurações do chat
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("⚙️ Configurações")
        
        # Selecionar modelo
        models = get_models()
        model_names = [m.get("name", "unknown") for m in models if m.get("status") == "available"]
        
        if not model_names:
            model_names = ["deepseek-r1", "gpt-4", "claude-3"]
        
        selected_model = st.selectbox("Modelo:", model_names)
        
        temperature = st.slider("Temperatura:", 0.0, 1.0, 0.7, 0.1)
        max_tokens = st.slider("Max Tokens:", 100, 4000, 2000, 100)
        
        if st.button("🗑️ Limpar Chat"):
            st.session_state.messages = []
            st.experimental_rerun()
    
    with col1:
        # Inicializar histórico de mensagens
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Olá! Sou o assistente IA do OmnisIA. Como posso ajudá-lo hoje?"
                }
            ]
        
        # Exibir histórico de mensagens
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input de mensagem
        if prompt := st.chat_input("Digite sua mensagem..."):
            # Adicionar mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Obter resposta da IA
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = send_chat_message(prompt, selected_model)
                    
                    if response and "response" in response:
                        assistant_response = response["response"]
                        st.markdown(assistant_response)
                        
                        # Adicionar resposta ao histórico
                        st.session_state.messages.append(
                            {"role": "assistant", "content": assistant_response}
                        )
                    else:
                        error_msg = "Desculpe, não foi possível processar sua mensagem."
                        st.error(error_msg)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": error_msg}
                        )

def show_files():
    """Página de gerenciamento de arquivos"""
    st.header("📁 Gerenciamento de Arquivos")
    
    # Upload de arquivos
    st.subheader("📤 Upload de Arquivos")
    
    uploaded_file = st.file_uploader(
        "Escolha um arquivo:",
        type=['pdf', 'txt', 'docx', 'xlsx', 'jpg', 'jpeg', 'png', 'mp3', 'wav', 'mp4', 'py', 'ipynb'],
        help="Formatos suportados: PDF, TXT, DOCX, XLSX, imagens, áudio, vídeo, código"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        process_immediately = st.checkbox("Processar imediatamente", value=True)
    
    with col2:
        if st.button("📤 Fazer Upload", disabled=not uploaded_file):
            if uploaded_file:
                with st.spinner("Fazendo upload..."):
                    result = upload_file(uploaded_file)
                    if result:
                        st.success(f"✅ Arquivo '{uploaded_file.name}' enviado com sucesso!")
                        if process_immediately:
                            st.info("🔄 Processamento iniciado automaticamente.")
                    else:
                        st.error("❌ Erro ao fazer upload do arquivo.")
    
    # Lista de arquivos
    st.subheader("📋 Arquivos Enviados")
    
    try:
        response = requests.get(f"{API_BASE_URL}/files", timeout=5)
        if response.status_code == 200:
            files_data = response.json()
            files = files_data.get("files", [])
            
            if files:
                # Criar DataFrame para exibição
                df_files = pd.DataFrame(files)
                df_files['size_mb'] = (df_files['size'] / 1024 / 1024).round(2)
                df_files['modified'] = pd.to_datetime(df_files['modified'], unit='s')
                
                # Exibir tabela
                st.dataframe(
                    df_files[['filename', 'size_mb', 'modified']],
                    column_config={
                        "filename": "Nome do Arquivo",
                        "size_mb": "Tamanho (MB)",
                        "modified": "Modificado"
                    },
                    use_container_width=True
                )
                
                # Estatísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Arquivos", len(files))
                with col2:
                    total_size_mb = df_files['size_mb'].sum()
                    st.metric("Tamanho Total (MB)", f"{total_size_mb:.2f}")
                with col3:
                    avg_size_mb = df_files['size_mb'].mean()
                    st.metric("Tamanho Médio (MB)", f"{avg_size_mb:.2f}")
            else:
                st.info("📂 Nenhum arquivo encontrado. Faça upload de arquivos acima.")
        else:
            st.error("❌ Erro ao carregar lista de arquivos.")
    except Exception as e:
        st.error(f"❌ Erro ao conectar com a API: {e}")

def show_training():
    """Página de treinamento de modelos"""
    st.header("🎓 Treinamento de Modelos LoRA")
    
    # Formulário de treinamento
    st.subheader("🚀 Iniciar Novo Treinamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Selecionar modelo base
        models = get_models()
        local_models = [m.get("name", "unknown") for m in models if m.get("type") == "local"]
        
        if not local_models:
            local_models = ["deepseek-r1", "llama-3.1-8b", "mistral-7b"]
        
        selected_model = st.selectbox("Modelo Base:", local_models)
        
        # Configurações de treinamento
        epochs = st.slider("Épocas:", 1, 10, 3)
        batch_size = st.selectbox("Batch Size:", [1, 2, 4, 8], index=1)
        learning_rate = st.number_input("Learning Rate:", 0.0001, 0.01, 0.0002, format="%.4f")
    
    with col2:
        # Dataset
        st.write("**Dataset:**")
        dataset_option = st.radio(
            "Origem do Dataset:",
            ["Upload Manual", "Caminho Local", "URL Remota"]
        )
        
        dataset_path = ""
        if dataset_option == "Upload Manual":
            dataset_file = st.file_uploader("Selecione o dataset:", type=['json', 'jsonl', 'csv', 'txt'])
            if dataset_file:
                dataset_path = f"/tmp/{dataset_file.name}"
        elif dataset_option == "Caminho Local":
            dataset_path = st.text_input("Caminho do Dataset:", placeholder="/path/to/dataset.json")
        else:
            dataset_path = st.text_input("URL do Dataset:", placeholder="https://example.com/dataset.json")
    
    # Botão de iniciar treinamento
    if st.button("🎯 Iniciar Treinamento", type="primary"):
        if not dataset_path:
            st.error("❌ Por favor, selecione um dataset.")
        else:
            with st.spinner("Iniciando treinamento..."):
                result = start_training(
                    model_name=selected_model,
                    dataset_path=dataset_path,
                    epochs=epochs,
                    batch_size=batch_size
                )
                
                if result:
                    st.success(f"✅ Treinamento iniciado! Job ID: {result.get('job_id', 'N/A')}")
                    st.info("🔄 O treinamento está rodando em background. Monitore o progresso abaixo.")
                else:
                    st.error("❌ Erro ao iniciar treinamento.")
    
    # Status dos treinamentos
    st.divider()
    st.subheader("📊 Status dos Treinamentos")
    
    try:
        response = requests.get(f"{API_BASE_URL}/training", timeout=5)
        if response.status_code == 200:
            training_data = response.json()
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Ativos", training_data.get("active", 0))
            with col2:
                st.metric("Completos", training_data.get("completed", 0))
            with col3:
                st.metric("Falhos", training_data.get("failed", 0))
            with col4:
                total_jobs = sum([training_data.get("active", 0), training_data.get("completed", 0), training_data.get("failed", 0)])
                st.metric("Total", total_jobs)
            
            # Lista de jobs (simulado para demonstração)
            if total_jobs == 0:
                st.info("📝 Nenhum treinamento em andamento. Inicie um novo treinamento acima.")
            else:
                # Simular alguns jobs para demonstração
                jobs_demo = [
                    {"job_id": "job_001", "model": "deepseek-r1", "status": "running", "progress": 65, "epoch": "2/3"},
                    {"job_id": "job_002", "model": "llama-3.1-8b", "status": "completed", "progress": 100, "epoch": "3/3"},
                ]
                
                for job in jobs_demo:
                    with st.expander(f"Job {job['job_id']} - {job['model']} ({job['status']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Status:** {job['status']}")
                            st.write(f"**Época:** {job['epoch']}")
                        with col2:
                            st.progress(job['progress'] / 100)
                            st.write(f"**Progresso:** {job['progress']}%")
        else:
            st.error("❌ Erro ao carregar status dos treinamentos.")
    except Exception as e:
        st.error(f"❌ Erro ao conectar com a API: {e}")

def show_settings():
    """Página de configurações"""
    st.header("🔧 Configurações do Sistema")
    
    # Configurações de API
    st.subheader("🔑 Configurações de API")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**APIs Externas:**")
        
        # OpenAI
        openai_key = st.text_input("OpenAI API Key:", type="password", help="Sua chave da OpenAI")
        
        # Anthropic
        anthropic_key = st.text_input("Anthropic API Key:", type="password", help="Sua chave da Anthropic")
        
        # Google
        google_key = st.text_input("Google API Key:", type="password", help="Sua chave do Google AI")
    
    with col2:
        st.write("**Cloud Services:**")
        
        # AWS
        aws_access_key = st.text_input("AWS Access Key:", help="Chave de acesso AWS")
        aws_secret_key = st.text_input("AWS Secret Key:", type="password", help="Chave secreta AWS")
        aws_region = st.selectbox("AWS Region:", ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"])
        
        # Kaggle
        kaggle_username = st.text_input("Kaggle Username:", help="Seu username do Kaggle")
        kaggle_key = st.text_input("Kaggle API Key:", type="password", help="Sua chave da API do Kaggle")
    
    # Configurações de banco de dados
    st.divider()
    st.subheader("💾 Configurações de Banco de Dados")
    
    database_type = st.selectbox(
        "Tipo de Banco:",
        ["sqlite", "postgresql", "mongodb", "redis"],
        help="Selecione o tipo de banco de dados"
    )
    
    if database_type == "postgresql":
        col1, col2 = st.columns(2)
        with col1:
            pg_host = st.text_input("Host:", value="localhost")
            pg_port = st.number_input("Porta:", value=5432)
            pg_database = st.text_input("Database:", value="omnisia")
        with col2:
            pg_user = st.text_input("Usuário:")
            pg_password = st.text_input("Senha:", type="password")
    
    elif database_type == "mongodb":
        col1, col2 = st.columns(2)
        with col1:
            mongo_host = st.text_input("Host:", value="localhost")
            mongo_port = st.number_input("Porta:", value=27017)
            mongo_database = st.text_input("Database:", value="omnisia")
        with col2:
            mongo_user = st.text_input("Usuário:")
            mongo_password = st.text_input("Senha:", type="password")
    
    # Botão salvar configurações
    if st.button("💾 Salvar Configurações", type="primary"):
        st.success("✅ Configurações salvas! (Funcionalidade em desenvolvimento)")
        st.info("ℹ️ As configurações serão aplicadas na próxima reinicialização do sistema.")

def show_status():
    """Página de status do sistema"""
    st.header("📊 Status do Sistema")
    
    # Status da API
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔌 Status da API")
        
        api_status = check_api_connection()
        if api_status:
            st.success("✅ API Online")
            
            # Obter informações detalhadas
            system_info = get_system_info()
            if system_info:
                st.json(system_info)
        else:
            st.error("❌ API Offline")
            st.info("Execute: `python main.py api`")
    
    with col2:
        st.subheader("💾 Status do Banco")
        
        try:
            response = requests.get(f"{API_BASE_URL}/database/status", timeout=5)
            if response.status_code == 200:
                db_status = response.json()
                st.success("✅ Banco Online")
                st.json(db_status)
            else:
                st.error("❌ Banco Offline")
        except:
            st.error("❌ Erro ao conectar com banco")
    
    # Modelos disponíveis
    st.divider()
    st.subheader("🤖 Modelos Disponíveis")
    
    models = get_models()
    if models:
        # Criar DataFrame
        df_models = pd.DataFrame(models)
        
        # Contadores por status
        status_counts = df_models['status'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Métricas
            for status, count in status_counts.items():
                st.metric(f"Modelos {status}", count)
        
        with col2:
            # Gráfico de pizza
            if len(status_counts) > 0:
                fig = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    title="Distribuição de Status dos Modelos"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Tabela detalhada
        st.dataframe(
            df_models,
            column_config={
                "name": "Nome",
                "type": "Tipo",
                "status": "Status",
                "size": "Tamanho"
            },
            use_container_width=True
        )
    else:
        st.info("ℹ️ Nenhum modelo encontrado ou API indisponível.")
    
    # Logs do sistema (simulado)
    st.divider()
    st.subheader("📋 Logs Recentes")
    
    logs_demo = [
        {"timestamp": "2024-12-19 17:25:48", "level": "INFO", "message": "🚀 OmnisIA API iniciada"},
        {"timestamp": "2024-12-19 17:25:49", "level": "INFO", "message": "💾 Banco de dados conectado"},
        {"timestamp": "2024-12-19 17:25:50", "level": "INFO", "message": "🤖 Modelos carregados"},
        {"timestamp": "2024-12-19 17:26:00", "level": "INFO", "message": "👤 Nova conexão de usuário"},
        {"timestamp": "2024-12-19 17:26:15", "level": "DEBUG", "message": "📤 Upload de arquivo processado"},
    ]
    
    for log in logs_demo:
        timestamp = log["timestamp"]
        level = log["level"]
        message = log["message"]
        
        if level == "ERROR":
            st.error(f"[{timestamp}] {message}")
        elif level == "WARNING":
            st.warning(f"[{timestamp}] {message}")
        elif level == "DEBUG":
            st.info(f"[{timestamp}] {message}")
        else:
            st.text(f"[{timestamp}] {message}")

if __name__ == "__main__":
    main()