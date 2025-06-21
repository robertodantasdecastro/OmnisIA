# 🤖 OmnisIA Trainer Web - Guia de Configuração e Instalação

## 📋 Visão Geral

O **OmnisIA Trainer Web** é uma aplicação completa para treinamento e processamento de IA com foco em:

-   **Upload e Processamento de Arquivos**: PDFs, imagens, áudios e vídeos
-   **OCR (Reconhecimento Óptico de Caracteres)**: Extração de texto de documentos e imagens
-   **STT (Speech-to-Text)**: Transcrição de áudios e vídeos usando Whisper
-   **Treinamento LoRA**: Fine-tuning de modelos de linguagem
-   **Sistema de Chat**: Chat inteligente com contexto baseado em embeddings
-   **Interface Web**: Frontend em Streamlit com dashboard completo

## 🏗️ Arquitetura do Sistema

```
OmnisIA Trainer Web/
├── Backend (FastAPI)
│   ├── API REST para processamento
│   ├── Serviços de IA (OCR, STT, LoRA)
│   ├── Sistema de embeddings
│   └── Gerenciamento de arquivos
├── Frontend (Streamlit)
│   ├── Interface web interativa
│   ├── Dashboard de monitoramento
│   ├── Páginas especializadas
│   └── Sistema de configuração
├── Docker
│   ├── Containerização completa
│   └── Deploy simplificado
└── Scripts
    ├── Instalação automatizada
    └── Deploy e manutenção
```

## 🔧 Pré-requisitos

### Sistema Operacional

-   **Linux**: Ubuntu 20.04+ (recomendado)
-   **macOS**: 10.15+
-   **Windows**: 10/11 com WSL2

### Software Necessário

-   **Python**: 3.8 ou superior
-   **Node.js**: 16+ (opcional, para desenvolvimento)
-   **Docker**: 20.10+ (para deploy containerizado)
-   **Git**: Para clonagem do repositório

### Dependências do Sistema

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y ffmpeg tesseract-ocr tesseract-ocr-por tesseract-ocr-eng \
                    build-essential python3-dev python3-pip python3-venv \
                    libsndfile1 libsndfile1-dev

# macOS (com Homebrew)
brew install ffmpeg tesseract tesseract-lang

# CentOS/RHEL
sudo yum install -y epel-release
sudo yum install -y ffmpeg tesseract tesseract-langpack-por tesseract-langpack-eng
```

## 📦 Instalação

### 1. Clonagem do Repositório

```bash
git clone https://github.com/seu-usuario/omnisia_web.git
cd omnisia_web
```

### 2. Configuração do Ambiente

```bash
# Copia arquivo de configuração
cp env.example .env

# Edita configurações (veja seção de Configuração)
nano .env
```

### 3. Instalação Automática

```bash
# Executa script de instalação
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 4. Instalação Manual

```bash
# Cria ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Atualiza pip
pip install --upgrade pip

# Instala dependências
pip install -r requirements.txt

# Cria diretórios necessários
mkdir -p data/{uploads,models,datasets,logs}
```

## ⚙️ Configuração

### Arquivo .env

O sistema usa um arquivo `.env` para configuração. Copie `env.example` para `.env` e ajuste:

#### Configurações Essenciais

```bash
# API
API_HOST=0.0.0.0
API_PORT=8000
API_URL=http://localhost:8000

# Frontend
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8501

# Upload
MAX_FILE_SIZE_MB=100
UPLOAD_DIR=data/uploads

# Modelos
WHISPER_MODEL_SIZE=base
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Segurança
SECRET_KEY=sua-chave-secreta-aqui
```

#### Configurações Avançadas

```bash
# LoRA Training
LORA_R=16
LORA_ALPHA=32
LORA_DROPOUT=0.1
TRAINING_EPOCHS=3
TRAINING_BATCH_SIZE=4

# Cache e Performance
CACHE_ENABLED=true
CACHE_TTL=300
MAX_CONCURRENT_REQUESTS=5

# Logging
LOG_LEVEL=INFO
ENABLE_DEBUG=false
DEVELOPMENT_MODE=false
```

### Configuração de Modelos

#### Modelos Whisper Disponíveis

-   **tiny**: ~39MB, rápido, precisão baixa
-   **base**: ~74MB, balanceado (padrão)
-   **small**: ~244MB, boa precisão
-   **medium**: ~769MB, muito boa precisão
-   **large**: ~1550MB, excelente precisão

#### Modelos de Embedding

-   **all-MiniLM-L6-v2**: Leve e rápido (padrão)
-   **all-mpnet-base-v2**: Melhor qualidade
-   **all-MiniLM-L12-v2**: Intermediário

## 🚀 Execução

### Desenvolvimento Local

#### Método 1: Scripts Automáticos

```bash
# Inicia backend e frontend
./scripts/start.sh

# Ou separadamente:
./scripts/start_backend.sh
./scripts/start_frontend.sh
```

#### Método 2: Manual

```bash
# Terminal 1 - Backend
source .venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
source .venv/bin/activate
streamlit run frontend/app.py --server.port 8501
```

### Deploy com Docker

#### Docker Compose (Recomendado)

```bash
# Build e execução
docker-compose -f docker/docker-compose.yml up --build

# Em background
docker-compose -f docker/docker-compose.yml up -d --build
```

#### Docker Manual

```bash
# Backend
docker build -f docker/Dockerfile.backend -t omnisia-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data omnisia-backend

# Frontend
docker build -f docker/Dockerfile.frontend -t omnisia-frontend .
docker run -p 8501:8501 omnisia-frontend
```

## 🌐 Acesso à Aplicação

Após inicialização:

-   **Frontend**: http://localhost:8501
-   **Backend API**: http://localhost:8000
-   **Documentação API**: http://localhost:8000/docs
-   **Health Check**: http://localhost:8000/health

## 📚 Funcionalidades

### 1. Upload de Arquivos

-   **Formatos suportados**: PDF, TXT, JPG, PNG, GIF, MP3, WAV, MP4, AVI, MOV
-   **Tamanho máximo**: Configurável (padrão 100MB)
-   **Validação automática**: Tipo e tamanho

### 2. Processamento OCR

-   **PDFs**: Extração de texto com OCR
-   **Imagens**: Reconhecimento de texto
-   **Idiomas**: Português, Inglês (configurável)
-   **Pré-processamento**: Melhoria automática da imagem

### 3. Transcrição de Áudio/Vídeo

-   **Modelos Whisper**: 5 tamanhos disponíveis
-   **Formatos**: MP3, WAV, MP4, AVI, MOV
-   **Timestamps**: Suporte a marcação temporal
-   **Detecção de idioma**: Automática

### 4. Treinamento LoRA

-   **Modelos base**: GPT-2, DialoGPT
-   **Configuração flexível**: Rank, alpha, dropout
-   **Monitoramento**: Logs detalhados
-   **Checkpoints**: Salvamento automático

### 5. Sistema de Chat

-   **Contexto inteligente**: Baseado em embeddings
-   **Busca semântica**: Encontra informações relevantes
-   **Confiança**: Métricas de qualidade
-   **Histórico**: Persistente por sessão

### 6. Dashboard

-   **Métricas do sistema**: Status, uptime, arquivos
-   **Monitoramento**: Cache, performance
-   **Arquivos recentes**: Listagem e gerenciamento
-   **Chat recente**: Histórico de conversas

## 🔧 Administração

### Logs

```bash
# Backend logs
tail -f logs/backend.log

# Frontend logs
tail -f logs/frontend.log

# Sistema logs
tail -f logs/omnisia.log
```

### Limpeza de Cache

```bash
# Via API
curl -X DELETE http://localhost:8000/chat/context

# Reinicialização
./scripts/restart.sh
```

### Backup

```bash
# Backup completo
./scripts/backup.sh

# Backup apenas dados
tar -czf backup_data_$(date +%Y%m%d).tar.gz data/
```

### Monitoramento

```bash
# Status dos serviços
./scripts/status.sh

# Métricas de sistema
curl http://localhost:8000/health
```

## 🐛 Solução de Problemas

### Problemas Comuns

#### 1. Erro de Dependências

```bash
# Reinstala dependências
pip install --upgrade -r requirements.txt

# Limpa cache pip
pip cache purge
```

#### 2. FFmpeg não encontrado

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Verifica instalação
ffmpeg -version
```

#### 3. Tesseract não encontrado

```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-por

# Verifica idiomas
tesseract --list-langs
```

#### 4. Erro de Permissões

```bash
# Corrige permissões dos diretórios
chmod -R 755 data/
chmod -R 755 logs/
```

#### 5. Porta em Uso

```bash
# Verifica processos usando as portas
lsof -i :8000
lsof -i :8501

# Mata processos se necessário
kill -9 <PID>
```

### Logs de Debug

Para ativar logs detalhados:

```bash
# No .env
ENABLE_DEBUG=true
LOG_LEVEL=DEBUG
DEVELOPMENT_MODE=true
```

## 🔒 Segurança

### Configurações de Produção

```bash
# .env para produção
DEVELOPMENT_MODE=false
ENABLE_DEBUG=false
SECRET_KEY=chave-super-secreta-complexa
ALLOWED_HOSTS=seu-dominio.com,localhost
```

### Firewall

```bash
# Ubuntu/Debian
sudo ufw allow 8000/tcp
sudo ufw allow 8501/tcp
sudo ufw enable
```

### SSL/HTTPS

Para produção, use um proxy reverso (nginx) com SSL:

```nginx
server {
    listen 443 ssl;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## 📊 Performance

### Otimizações Recomendadas

#### Hardware

-   **CPU**: 4+ cores para processamento paralelo
-   **RAM**: 8GB+ (16GB+ para modelos grandes)
-   **GPU**: CUDA compatível (opcional, para aceleração)
-   **Storage**: SSD para melhor I/O

#### Software

```bash
# Cache de modelos
CACHE_ENABLED=true
HUGGINGFACE_CACHE_DIR=data/huggingface_cache

# Processamento paralelo
MAX_CONCURRENT_REQUESTS=5
```

### Monitoramento de Recursos

```bash
# CPU e memória
htop

# Espaço em disco
df -h

# Uso de GPU (se disponível)
nvidia-smi
```

## 🔄 Atualizações

### Atualização do Sistema

```bash
# Pull das mudanças
git pull origin main

# Atualiza dependências
pip install --upgrade -r requirements.txt

# Reinicia serviços
./scripts/restart.sh
```

### Migração de Dados

```bash
# Backup antes da atualização
./scripts/backup.sh

# Migração de configuração
./scripts/migrate_config.sh
```

## 📞 Suporte

### Documentação

-   **API Docs**: http://localhost:8000/docs
-   **Configuração**: [CONFIGURATION.md](frontend/CONFIGURATION.md)
-   **Exemplos**: [examples/](examples/)

### Contato

-   **Autor**: Roberto Dantas de Castro
-   **Email**: robertodantasdecastro@gmail.com
-   **GitHub**: [Issues](https://github.com/seu-usuario/omnisia_web/issues)

### Logs para Suporte

Ao reportar problemas, inclua:

```bash
# Informações do sistema
./scripts/system_info.sh > system_info.txt

# Logs relevantes
tail -n 100 logs/backend.log > backend_logs.txt
tail -n 100 logs/frontend.log > frontend_logs.txt
```

---

## 📝 Notas de Versão

### v1.0.0 (2024-01-01)

-   ✅ Sistema completo de upload e processamento
-   ✅ OCR para PDFs e imagens
-   ✅ Transcrição de áudio/vídeo com Whisper
-   ✅ Treinamento LoRA
-   ✅ Sistema de chat com embeddings
-   ✅ Interface web completa
-   ✅ Containerização Docker
-   ✅ Sistema de configuração centralizado

---

**🎉 OmnisIA Trainer Web está pronto para uso!**

Para começar rapidamente:

1. Execute `./scripts/setup.sh`
2. Configure o arquivo `.env`
3. Execute `./scripts/start.sh`
4. Acesse http://localhost:8501

Boa sorte com seu projeto de IA! 🚀
