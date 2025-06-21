#!/bin/bash
set -e

echo "🚀 Configurando ambiente OmnisIA..."

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.8+"
    exit 1
fi

# Cria ambiente virtual
echo "📦 Criando ambiente virtual..."
python3 -m venv .venv

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Atualiza pip
echo "⬆️ Atualizando pip..."
pip install --upgrade pip

# Instala dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p data/uploads
mkdir -p data/models
mkdir -p data/datasets

echo "✅ Configuração concluída!"
echo ""
echo "Para iniciar o backend:"
echo "  source .venv/bin/activate"
echo "  uvicorn backend.main:app --reload"
echo ""
echo "Para iniciar o frontend (em outro terminal):"
echo "  source .venv/bin/activate"
echo "  streamlit run frontend/app.py"
