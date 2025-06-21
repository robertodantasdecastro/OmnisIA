#!/bin/bash
# ============================================================================
# OMNISIA - SCRIPT DE INSTALAÇÃO COMPLETA / COMPLETE INSTALLATION SCRIPT
# ============================================================================
# Sistema Integrado de IA Multimodal / Integrated Multimodal AI System
# Autor: Roberto Dantas de Castro
# Email: robertodantasdecastro@gmail.com
# Versão: 2.0.0
# ============================================================================

set -e

# Cores para output / Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variáveis globais / Global variables
PYTHON_MIN_VERSION="3.8"
VENV_NAME=".venv"
LOG_FILE="logs/installation.log"

# Função para log / Logging function
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >>"$LOG_FILE" 2>/dev/null || true
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [SUCCESS] $1" >>"$LOG_FILE" 2>/dev/null || true
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARNING] $1" >>"$LOG_FILE" 2>/dev/null || true
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >>"$LOG_FILE" 2>/dev/null || true
}

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [STEP] $1" >>"$LOG_FILE" 2>/dev/null || true
}

# Banner de instalação / Installation banner
show_banner() {
    echo -e "${CYAN}"
    echo "============================================================================"
    echo "  ___  __  __ _   _ ___ ____ ___    _    "
    echo " / _ \|  \/  | \ | |_ _/ ___|_ _|  / \   "
    echo "| | | | |\/| |  \| || |\___ \| |  / _ \  "
    echo "| |_| | |  | | |\  || | ___) | | / ___ \ "
    echo " \___/|_|  |_|_| \_|___|____/___/_/   \_\\"
    echo ""
    echo "🤖 OMNISIA v2.0 - Enterprise AI Platform"
    echo "🚀 Sistema Completo de IA Multimodal"
    echo "📧 robertodantasdecastro@gmail.com"
    echo "============================================================================"
    echo -e "${NC}"
}

# Detecção do OS / OS Detection
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Verificar versão do Python / Check Python version
check_python_version() {
    log_step "Verificando versão do Python..."

    if ! command -v python3 &>/dev/null; then
        log_error "Python 3 não está instalado!"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        log_error "Python 3.8+ é necessário. Versão atual: $PYTHON_VERSION"
        exit 1
    fi

    log_success "Python $PYTHON_VERSION encontrado"
}

# Verificação de dependências / Dependencies check
check_dependencies() {
    log_step "Verificando dependências do sistema..."

    # Python
    check_python_version

    # pip
    if ! command -v pip3 &>/dev/null; then
        log_error "pip3 não está instalado!"
        exit 1
    fi
    log_success "pip3 encontrado"

    # Git (opcional)
    if command -v git &>/dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        log_success "Git $GIT_VERSION encontrado"
    else
        log_warning "Git não encontrado (recomendado)"
    fi

    # Node.js (opcional para desenvolvimento web)
    if command -v node &>/dev/null; then
        NODE_VERSION=$(node --version)
        log_success "Node.js $NODE_VERSION encontrado"
    else
        log_warning "Node.js não encontrado (opcional)"
    fi

    # Docker (opcional)
    if command -v docker &>/dev/null; then
        DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | cut -d',' -f1)
        log_success "Docker $DOCKER_VERSION encontrado"
    else
        log_warning "Docker não encontrado (opcional)"
    fi
}

# Instalação de dependências do sistema / System dependencies installation
install_system_dependencies() {
    log_step "Instalando dependências do sistema..."

    OS=$(detect_os)
    log_info "Sistema operacional detectado: $OS"

    case $OS in
    "linux")
        # Ubuntu/Debian
        if command -v apt-get &>/dev/null; then
            log_info "Detectado sistema baseado em Debian/Ubuntu"
            sudo apt-get update -qq
            sudo apt-get install -y \
                tesseract-ocr \
                tesseract-ocr-por \
                tesseract-ocr-eng \
                ffmpeg \
                libgl1-mesa-glx \
                libglib2.0-0 \
                libsm6 \
                libxext6 \
                libxrender-dev \
                libgomp1 \
                build-essential \
                curl \
                wget \
                unzip \
                git \
                postgresql-client \
                redis-tools

        # CentOS/RHEL/Fedora
        elif command -v yum &>/dev/null; then
            log_info "Detectado sistema baseado em Red Hat"
            sudo yum update -y -q
            sudo yum install -y \
                tesseract \
                tesseract-langpack-por \
                tesseract-langpack-eng \
                ffmpeg \
                gcc \
                gcc-c++ \
                make \
                curl \
                wget \
                unzip \
                git \
                postgresql \
                redis

        elif command -v dnf &>/dev/null; then
            log_info "Detectado sistema Fedora"
            sudo dnf update -y -q
            sudo dnf install -y \
                tesseract \
                tesseract-langpack-por \
                tesseract-langpack-eng \
                ffmpeg \
                gcc \
                gcc-c++ \
                make \
                curl \
                wget \
                unzip \
                git \
                postgresql \
                redis
        fi
        ;;

    "macos")
        log_info "Detectado macOS"
        if command -v brew &>/dev/null; then
            log_info "Usando Homebrew para instalação"
            brew update
            brew install \
                tesseract \
                tesseract-lang \
                ffmpeg \
                postgresql \
                redis \
                wget \
                curl
        else
            log_warning "Homebrew não encontrado. Instalando Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            log_success "Homebrew instalado. Execute o script novamente."
            exit 0
        fi
        ;;

    "windows")
        log_warning "Windows detectado. Dependências do sistema devem ser instaladas manualmente:"
        log_warning "- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki"
        log_warning "- FFmpeg: https://ffmpeg.org/download.html"
        log_warning "- PostgreSQL: https://www.postgresql.org/download/windows/"
        log_warning "- Redis: https://redis.io/download"
        ;;

    *)
        log_warning "Sistema operacional não reconhecido. Instale as dependências manualmente."
        ;;
    esac

    log_success "Dependências do sistema instaladas"
}

# Criar diretórios necessários / Create necessary directories
create_directories() {
    log_step "Criando estrutura de diretórios..."

    # Criar diretório de logs primeiro
    mkdir -p logs

    # Lista de diretórios necessários
    directories=(
        "data"
        "data/uploads"
        "data/models"
        "data/models/local"
        "data/datasets"
        "data/training"
        "data/training/output"
        "data/checkpoints"
        "data/exports"
        "data/temp"
        "data/backups"
        "notebooks"
        "scripts"
        "web/static"
        "web/templates"
        "tests"
    )

    for dir in "${directories[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_info "Criado: $dir"
        else
            log_info "Existe: $dir"
        fi
    done

    log_success "Estrutura de diretórios criada"
}

# Criação do ambiente virtual / Virtual environment creation
create_virtual_environment() {
    log_step "Configurando ambiente virtual Python..."

    if [ -d "$VENV_NAME" ]; then
        log_warning "Ambiente virtual já existe. Removendo..."
        rm -rf "$VENV_NAME"
    fi

    log_info "Criando ambiente virtual..."
    python3 -m venv "$VENV_NAME"
    log_success "Ambiente virtual criado em $VENV_NAME"

    # Ativação do ambiente virtual / Virtual environment activation
    log_info "Ativando ambiente virtual..."
    source "$VENV_NAME/bin/activate"
    log_success "Ambiente virtual ativado"

    # Verificar se a ativação funcionou
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        log_success "Ambiente virtual confirmado: $VIRTUAL_ENV"
    else
        log_error "Falha ao ativar ambiente virtual"
        exit 1
    fi
}

# Atualização do pip / pip upgrade
upgrade_pip() {
    log_step "Atualizando pip e ferramentas básicas..."

    pip install --upgrade pip setuptools wheel
    log_success "pip, setuptools e wheel atualizados"
}

# Instalação das dependências Python / Python dependencies installation
install_python_dependencies() {
    log_step "Instalando dependências Python..."

    if [ ! -f "requirements.txt" ]; then
        log_error "Arquivo requirements.txt não encontrado!"
        exit 1
    fi

    # Contar número de pacotes
    TOTAL_PACKAGES=$(grep -v '^#' requirements.txt | grep -v '^$' | wc -l)
    log_info "Instalando $TOTAL_PACKAGES pacotes Python..."

    # Instalar PyTorch primeiro (pode levar tempo)
    log_info "Instalando PyTorch (pode levar alguns minutos)..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

    # Instalar outras dependências
    log_info "Instalando outras dependências..."
    pip install -r requirements.txt

    log_success "Dependências Python instaladas"
}

# Configuração do arquivo .env / .env file setup
setup_environment_file() {
    log_step "Configurando arquivo de ambiente..."

    if [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            cp env.example .env
            log_success "Arquivo .env criado a partir de env.example"
            log_warning "IMPORTANTE: Configure as variáveis em .env antes de usar o sistema"
        else
            log_error "Arquivo env.example não encontrado!"
            exit 1
        fi
    else
        log_info "Arquivo .env já existe"
    fi
}

# Teste da instalação / Installation test
test_installation() {
    log_step "Testando instalação..."

    # Testar importações Python críticas
    python3 -c "
import sys
import os
try:
    import torch
    import transformers
    import fastapi
    import streamlit
    import typer
    import rich
    print('✅ Todas as importações críticas funcionando')
except ImportError as e:
    print(f'❌ Erro na importação: {e}')
    sys.exit(1)
"

    if [ $? -eq 0 ]; then
        log_success "Teste de importações passou"
    else
        log_error "Teste de importações falhou"
        exit 1
    fi

    # Testar configuração
    python3 -c "
try:
    from config import validate_config
    errors = validate_config()
    if errors:
        print('⚠️ Avisos de configuração:')
        for error in errors:
            print(f'  • {error}')
    else:
        print('✅ Configuração válida')
except Exception as e:
    print(f'❌ Erro na configuração: {e}')
"

    log_success "Testes de instalação concluídos"
}

# Exibir próximos passos / Show next steps
show_next_steps() {
    echo ""
    echo -e "${GREEN}"
    echo "============================================================================"
    echo "🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! / INSTALLATION COMPLETED SUCCESSFULLY!"
    echo "============================================================================"
    echo -e "${NC}"

    echo -e "${CYAN}📋 PRÓXIMOS PASSOS / NEXT STEPS:${NC}"
    echo ""
    echo -e "${YELLOW}1. Ativar ambiente virtual / Activate virtual environment:${NC}"
    echo "   source $VENV_NAME/bin/activate"
    echo ""
    echo -e "${YELLOW}2. Configurar variáveis de ambiente / Configure environment variables:${NC}"
    echo "   nano .env"
    echo ""
    echo -e "${YELLOW}3. Testar o sistema / Test the system:${NC}"
    echo "   python main.py info"
    echo ""
    echo -e "${YELLOW}4. Iniciar interface web / Start web interface:${NC}"
    echo "   python main.py web"
    echo ""
    echo -e "${YELLOW}5. Iniciar API / Start API:${NC}"
    echo "   python main.py api"
    echo ""
    echo -e "${YELLOW}6. Ver todos os comandos / See all commands:${NC}"
    echo "   python main.py --help"
    echo ""
    echo -e "${CYAN}📚 DOCUMENTAÇÃO / DOCUMENTATION:${NC}"
    echo "   • README.md - Visão geral / Overview"
    echo "   • ANALYSIS_REPORT.md - Relatório completo / Complete report"
    echo "   • http://localhost:8000/docs - API documentation"
    echo ""
    echo -e "${CYAN}📧 SUPORTE / SUPPORT:${NC}"
    echo "   Email: robertodantasdecastro@gmail.com"
    echo ""
}

# Função de limpeza em caso de erro / Cleanup function for errors
cleanup_on_error() {
    log_error "Instalação falhou. Limpando arquivos temporários..."

    # Remover ambiente virtual se criado
    if [ -d "$VENV_NAME" ]; then
        rm -rf "$VENV_NAME"
        log_info "Ambiente virtual removido"
    fi

    exit 1
}

# Trap para limpeza em caso de erro / Trap for error cleanup
trap cleanup_on_error ERR

# Função principal / Main function
main() {
    show_banner

    # Verificar se está sendo executado do diretório correto
    if [ ! -f "main.py" ]; then
        log_error "Execute este script a partir do diretório raiz do projeto OmnisIA"
        exit 1
    fi

    log_info "Iniciando instalação do OmnisIA v2.0..."

    # Criar diretório de logs
    mkdir -p logs

    # Executar etapas de instalação
    check_dependencies
    install_system_dependencies
    create_directories
    create_virtual_environment
    upgrade_pip
    install_python_dependencies
    setup_environment_file
    test_installation

    log_success "🎉 Instalação concluída com sucesso!"
    show_next_steps
}

# Verificar se o script está sendo executado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
