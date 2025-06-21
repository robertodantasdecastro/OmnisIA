#!/bin/bash
set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ___                  _     ___   _     
 / _ \ _ __ ___  _ __ (_)___| _ \ / \    
| | | | '_ ` _ \| '_ \| / __|   // _ \   
| |_| | | | | | | | | \__ \ |_|/ ___ \  
 \___/|_| |_| |_|_| |_|___/___/_/   \_\ 
                                        
     Trainer Web - Setup Script         
EOF
echo -e "${NC}"

log_info "🚀 Iniciando configuração do OmnisIA Trainer Web..."

# Detecta sistema operacional
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

log_info "Sistema detectado: $OS"

# Verifica se está no diretório correto
if [[ ! -f "env.example" ]] || [[ ! -f "requirements.txt" ]]; then
    log_error "Execute este script a partir do diretório raiz do projeto!"
    exit 1
fi

# Função para verificar comandos
check_command() {
    if command -v "$1" &> /dev/null; then
        log_success "$1 está disponível"
        return 0
    else
        log_warning "$1 não encontrado"
        return 1
    fi
}

# Verifica dependências do sistema
log_info "🔍 Verificando dependências do sistema..."

# Python
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l 2>/dev/null || echo 0) -eq 1 ]]; then
        log_success "Python $PYTHON_VERSION (✓ >= 3.8)"
    else
        log_error "Python 3.8+ é necessário. Versão atual: $PYTHON_VERSION"
        exit 1
    fi
else
    log_error "Python 3 não encontrado!"
    exit 1
fi

# Git
check_command git || log_warning "Git recomendado para atualizações"

# FFmpeg
if ! check_command ffmpeg; then
    log_warning "FFmpeg não encontrado. Será necessário para processamento de vídeo/áudio."
    read -p "Deseja instalar FFmpeg automaticamente? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Instalando FFmpeg..."
        if [[ "$OS" == "linux" ]]; then
            if [[ "$DISTRO" == "Ubuntu" ]] || [[ "$DISTRO" == "Debian" ]]; then
                sudo apt update && sudo apt install -y ffmpeg
            elif [[ "$DISTRO" == "CentOS" ]] || [[ "$DISTRO" == "RedHat" ]]; then
                sudo yum install -y epel-release && sudo yum install -y ffmpeg
            fi
        elif [[ "$OS" == "macos" ]]; then
            if check_command brew; then
                brew install ffmpeg
            else
                log_error "Homebrew não encontrado. Instale FFmpeg manualmente."
            fi
        fi
    fi
fi

# Tesseract
if ! check_command tesseract; then
    log_warning "Tesseract não encontrado. Será necessário para OCR."
    read -p "Deseja instalar Tesseract automaticamente? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Instalando Tesseract..."
        if [[ "$OS" == "linux" ]]; then
            if [[ "$DISTRO" == "Ubuntu" ]] || [[ "$DISTRO" == "Debian" ]]; then
                sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-por tesseract-ocr-eng
            elif [[ "$DISTRO" == "CentOS" ]] || [[ "$DISTRO" == "RedHat" ]]; then
                sudo yum install -y tesseract tesseract-langpack-por tesseract-langpack-eng
            fi
        elif [[ "$OS" == "macos" ]]; then
            if check_command brew; then
                brew install tesseract tesseract-lang
            else
                log_error "Homebrew não encontrado. Instale Tesseract manualmente."
            fi
        fi
    fi
fi

# Verifica se já existe ambiente virtual
if [[ -d ".venv" ]]; then
    log_warning "Ambiente virtual já existe"
    read -p "Deseja recriar o ambiente virtual? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Removendo ambiente virtual existente..."
        rm -rf .venv
    fi
fi

# Cria ambiente virtual se não existir
if [[ ! -d ".venv" ]]; then
    log_info "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    log_success "Ambiente virtual criado"
fi

# Ativa ambiente virtual
log_info "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Verifica se ativação funcionou
if [[ "$VIRTUAL_ENV" != "" ]]; then
    log_success "Ambiente virtual ativado: $VIRTUAL_ENV"
else
    log_error "Falha ao ativar ambiente virtual"
    exit 1
fi

# Atualiza pip
log_info "⬆️ Atualizando pip..."
python -m pip install --upgrade pip
log_success "Pip atualizado"

# Instala wheel para compilação mais rápida
log_info "🛠️ Instalando ferramentas de build..."
pip install wheel setuptools

# Instala dependências
log_info "📚 Instalando dependências Python..."
pip install -r requirements.txt
log_success "Dependências instaladas"

# Cria arquivo .env se não existir
if [[ ! -f ".env" ]]; then
    log_info "📝 Criando arquivo de configuração .env..."
    cp env.example .env
    
    # Gera chave secreta aleatória
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Atualiza .env com valores específicos
    if [[ "$OS" == "macos" ]]; then
        sed -i '' "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    else
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
    fi
    
    log_success "Arquivo .env criado com chave secreta gerada"
else
    log_warning "Arquivo .env já existe"
fi

# Cria diretórios necessários
log_info "📁 Criando estrutura de diretórios..."
mkdir -p data/{uploads,models,datasets,huggingface_cache,torch_cache}
mkdir -p logs
mkdir -p backups

# Define permissões
chmod 755 data/
chmod 755 logs/
chmod 755 backups/

log_success "Diretórios criados"

# Testa importações críticas
log_info "🧪 Testando instalação..."

# Testa imports Python
python3 -c "
import sys
try:
    import fastapi
    import streamlit
    import transformers
    import torch
    import whisper
    import sentence_transformers
    print('✅ Todas as dependências Python estão funcionando')
except ImportError as e:
    print(f'❌ Erro de importação: {e}')
    sys.exit(1)
"

if [[ $? -eq 0 ]]; then
    log_success "Teste de dependências Python passou"
else
    log_error "Falha no teste de dependências"
    exit 1
fi

# Cria scripts de conveniência
log_info "📜 Criando scripts de conveniência..."

# Script para iniciar backend
cat > scripts/start_backend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/.."
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
EOF

# Script para iniciar frontend
cat > scripts/start_frontend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/.."
source .venv/bin/activate
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
EOF

# Script para iniciar ambos
cat > scripts/start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/.."

echo "🚀 Iniciando OmnisIA Trainer Web..."

# Função para cleanup
cleanup() {
    echo "🛑 Parando serviços..."
    jobs -p | xargs -r kill
    exit 0
}

trap cleanup SIGINT SIGTERM

# Inicia backend em background
echo "📡 Iniciando backend..."
./scripts/start_backend.sh &
BACKEND_PID=$!

# Aguarda um pouco para o backend inicializar
sleep 5

# Inicia frontend
echo "🖥️ Iniciando frontend..."
./scripts/start_frontend.sh &
FRONTEND_PID=$!

echo "✅ Serviços iniciados!"
echo "📡 Backend: http://localhost:8000"
echo "🖥️ Frontend: http://localhost:8501"
echo "📚 Docs: http://localhost:8000/docs"
echo ""
echo "Pressione Ctrl+C para parar os serviços"

# Aguarda por sinal de parada
wait
EOF

# Script de status
cat > scripts/status.sh << 'EOF'
#!/bin/bash
echo "🔍 Status dos Serviços OmnisIA"
echo "================================"

# Verifica backend
if curl -s http://localhost:8000/health > /dev/null; then
    echo "📡 Backend: ✅ Online (http://localhost:8000)"
else
    echo "📡 Backend: ❌ Offline"
fi

# Verifica frontend
if curl -s http://localhost:8501 > /dev/null; then
    echo "🖥️ Frontend: ✅ Online (http://localhost:8501)"
else
    echo "🖥️ Frontend: ❌ Offline"
fi

# Verifica processos
echo ""
echo "🔍 Processos ativos:"
ps aux | grep -E "(uvicorn|streamlit)" | grep -v grep || echo "Nenhum processo encontrado"
EOF

# Script de backup
cat > scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="omnisia_backup_$TIMESTAMP.tar.gz"

echo "💾 Criando backup..."

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
    --exclude='.venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='backups' \
    .

echo "✅ Backup criado: $BACKUP_DIR/$BACKUP_FILE"
ls -lh "$BACKUP_DIR/$BACKUP_FILE"
EOF

# Script de informações do sistema
cat > scripts/system_info.sh << 'EOF'
#!/bin/bash
echo "🖥️ Informações do Sistema OmnisIA"
echo "=================================="
echo "Data: $(date)"
echo "OS: $(uname -a)"
echo "Python: $(python3 --version)"
echo "Pip: $(pip --version)"
echo ""
echo "📦 Dependências instaladas:"
pip list | grep -E "(fastapi|streamlit|torch|transformers|whisper)"
echo ""
echo "💾 Espaço em disco:"
df -h data/ logs/
echo ""
echo "🔧 Configuração:"
echo "VIRTUAL_ENV: $VIRTUAL_ENV"
echo "PYTHONPATH: $PYTHONPATH"
EOF

# Torna scripts executáveis
chmod +x scripts/*.sh

log_success "Scripts criados"

# Testa configuração básica
log_info "🔧 Testando configuração..."

# Verifica se consegue importar o backend
python3 -c "
import sys
sys.path.append('.')
try:
    from backend.main import app
    print('✅ Backend pode ser importado')
except Exception as e:
    print(f'❌ Erro ao importar backend: {e}')
    sys.exit(1)
"

if [[ $? -eq 0 ]]; then
    log_success "Teste de configuração passou"
else
    log_error "Falha no teste de configuração"
fi

# Resumo final
echo ""
echo -e "${GREEN}🎉 Configuração concluída com sucesso!${NC}"
echo ""
echo -e "${BLUE}📋 Próximos passos:${NC}"
echo "1. Configure o arquivo .env conforme necessário"
echo "2. Execute: ./scripts/start.sh"
echo "3. Acesse: http://localhost:8501"
echo ""
echo -e "${BLUE}📚 Comandos úteis:${NC}"
echo "• Iniciar serviços: ./scripts/start.sh"
echo "• Status: ./scripts/status.sh"
echo "• Backup: ./scripts/backup.sh"
echo "• Info do sistema: ./scripts/system_info.sh"
echo ""
echo -e "${BLUE}📖 Documentação:${NC}"
echo "• Setup completo: SETUP.md"
echo "• Configuração: frontend/CONFIGURATION.md"
echo "• API Docs: http://localhost:8000/docs (após iniciar)"
echo ""

# Pergunta se quer iniciar agora
read -p "Deseja iniciar os serviços agora? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    log_info "🚀 Iniciando serviços..."
    ./scripts/start.sh
fi

log_success "Setup completo! 🎉"
