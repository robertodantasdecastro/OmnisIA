# OmnisIA Trainer Web

Sistema web open source para automatizar ingestão, pré-processamento e treinamento generativo multimodal.

## 🚀 Funcionalidades

-   **Upload de arquivos**: PDFs, imagens, áudios e vídeos com validação
-   **OCR automático**: Extração de texto de PDFs e imagens
-   **Transcrição**: Áudio e vídeo para texto usando Whisper
-   **Armazenamento vetorial**: FAISS para busca semântica
-   **Fine-tuning**: Treinamento leve com PEFT/LoRA
-   **Chat inteligente**: Baseado em contexto e embeddings

## 📋 Pré-requisitos

-   Python 3.8+
-   FFmpeg (para processamento de vídeo)
-   Tesseract OCR (para extração de texto de imagens)

### Instalação de dependências do sistema

**Ubuntu/Debian:**

```bash
sudo apt-get update
sudo apt-get install ffmpeg tesseract-ocr tesseract-ocr-por tesseract-ocr-eng
```

**macOS:**

```bash
brew install ffmpeg tesseract
```

**Windows:**

-   Instale FFmpeg: https://ffmpeg.org/download.html
-   Instale Tesseract: https://github.com/UB-Mannheim/tesseract/wiki

## 🛠️ Instalação

### Método 1: Setup automático

```bash
cd omnisia_web/scripts
chmod +x setup.sh
./setup.sh
```

### Método 2: Instalação manual

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p data/uploads data/models data/datasets
```

## 🚀 Uso

### Iniciar o backend

```bash
source .venv/bin/activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Iniciar o frontend (em outro terminal)

```bash
source .venv/bin/activate
streamlit run frontend/app.py --server.port 8501
```

### Usar Docker

```bash
cd docker
docker-compose up --build
```

## 📖 API Endpoints

### Upload

-   `POST /upload/` - Upload de arquivos
-   `GET /upload/files` - Listar arquivos enviados

### Pré-processamento

-   `POST /preprocess/ocr-pdf` - OCR de PDF
-   `POST /preprocess/transcribe` - Transcrição de áudio
-   `POST /preprocess/transcribe-video` - Transcrição de vídeo
-   `POST /preprocess/ocr-image` - OCR de imagem

### Treinamento

-   `POST /train/` - Treinar modelo LoRA
-   `GET /train/models` - Listar modelos suportados

### Chat

-   `POST /chat/` - Chat com contexto
-   `POST /chat/add-context` - Adicionar contexto
-   `GET /chat/context-info` - Informações do contexto

## 🔧 Configuração

As configurações estão centralizadas em `backend/config.py`:

-   **Upload**: Tipos de arquivo permitidos, tamanho máximo
-   **Modelos**: Lista de modelos suportados para treinamento
-   **LoRA**: Configurações de fine-tuning
-   **Embeddings**: Modelo de embeddings padrão

## 🐛 Correções Implementadas

### Problemas Corrigidos:

1. **Importações quebradas**: Implementados serviços reais em vez de importar módulos inexistentes
2. **Dockerfiles**: Corrigidos caminhos e adicionadas dependências do sistema
3. **Validação**: Adicionada validação de arquivos e tratamento de erros
4. **Dependências**: Adicionadas todas as dependências necessárias
5. **Segurança**: Validação de tipos de arquivo e tamanhos
6. **Configuração**: Centralizada em arquivo de configuração
7. **Frontend**: Interface completa e funcional
8. **Scripts**: Corrigidos caminhos e melhorada usabilidade

### Melhorias:

-   Tratamento de erros robusto
-   Validação de entrada
-   Interface web moderna
-   Documentação completa
-   Configuração centralizada
-   Suporte a Docker

## 📁 Estrutura do Projeto

```
omnisia_web/
├── backend/
│   ├── main.py              # Aplicação FastAPI
│   ├── config.py            # Configurações centralizadas
│   ├── routers/             # Endpoints da API
│   └── services/            # Lógica de negócio
├── frontend/
│   └── app.py               # Interface Streamlit
├── docker/                  # Configurações Docker
├── scripts/                 # Scripts de setup
└── data/                    # Dados e modelos (criado automaticamente)
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🔗 Links

-   [OmnisIA](https://github.com/robertodantasdecastro/OmnisIA/frontend/)
-   [FastAPI](https://fastapi.tiangolo.com/)
-   [Streamlit](https://streamlit.io/)
-   [Hugging Face](https://huggingface.co/)
