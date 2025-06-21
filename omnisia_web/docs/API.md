# OmnisIA Trainer Web - Documentação da API

## Visão Geral

A API OmnisIA Trainer Web fornece endpoints para upload, pré-processamento, treinamento e chat com modelos de IA.

**URL Base:** `http://localhost:8000`

## Endpoints

### 1. Status da API

#### GET /

Retorna informações básicas sobre a API.

**Resposta:**

```json
{
	"message": "OmnisIA Trainer Web API"
}
```

### 2. Upload de Arquivos

#### POST /upload/

Faz upload de um arquivo para o sistema.

**Parâmetros:**

-   `file` (multipart/form-data): Arquivo a ser enviado

**Tipos de arquivo suportados:**

-   PDF: `.pdf`
-   Imagens: `.jpg`, `.jpeg`, `.png`, `.gif`
-   Áudio: `.mp3`, `.wav`
-   Vídeo: `.mp4`, `.avi`, `.mov`
-   Texto: `.txt`

**Limite de tamanho:** 100MB

**Resposta de sucesso (200):**

```json
{
	"filename": "documento.pdf",
	"size": 1024000,
	"path": "data/uploads/documento.pdf"
}
```

**Resposta de erro (400):**

```json
{
	"detail": "Tipo de arquivo não permitido. Tipos aceitos: .pdf, .txt, .jpg, .jpeg, .png, .gif, .mp3, .wav, .mp4, .avi, .mov"
}
```

#### GET /upload/files

Lista todos os arquivos enviados.

**Resposta (200):**

```json
{
	"files": [
		{
			"filename": "documento.pdf",
			"size": 1024000,
			"modified": 1640995200.0
		}
	]
}
```

### 3. Pré-processamento

#### POST /preprocess/ocr-pdf

Extrai texto de um PDF usando OCR.

**Corpo da requisição:**

```json
{
	"pdf_path": "data/uploads/documento.pdf",
	"output_path": "data/output/documento_ocr.pdf"
}
```

**Resposta (200):**

```json
{
	"output": "data/output/documento_ocr.pdf",
	"status": "success"
}
```

#### POST /preprocess/transcribe

Transcreve áudio para texto usando Whisper.

**Corpo da requisição:**

```json
{
	"audio_path": "data/uploads/audio.wav",
	"model_size": "base"
}
```

**Tamanhos de modelo disponíveis:** `tiny`, `base`, `small`, `medium`, `large`

**Resposta (200):**

```json
{
	"text": "Texto transcrito do áudio...",
	"status": "success"
}
```

#### POST /preprocess/transcribe-video

Transcreve vídeo para texto.

**Corpo da requisição:**

```json
{
	"video_path": "data/uploads/video.mp4"
}
```

**Resposta (200):**

```json
{
	"text": "Texto transcrito do vídeo...",
	"status": "success"
}
```

#### POST /preprocess/ocr-image

Extrai texto de uma imagem usando OCR.

**Corpo da requisição:**

```json
{
	"image_path": "data/uploads/imagem.jpg"
}
```

**Resposta (200):**

```json
{
	"text": "Texto extraído da imagem...",
	"status": "success"
}
```

### 4. Treinamento

#### GET /train/models

Lista modelos suportados para treinamento.

**Resposta (200):**

```json
{
	"models": [
		{
			"name": "gpt2",
			"description": "GPT-2 Small (124M parameters)"
		},
		{
			"name": "gpt2-medium",
			"description": "GPT-2 Medium (355M parameters)"
		}
	]
}
```

#### POST /train/

Treina um modelo usando LoRA.

**Corpo da requisição:**

```json
{
	"model_name": "gpt2",
	"dataset_path": "data/datasets/training_data.txt",
	"output_dir": "data/models/lora_output"
}
```

**Resposta (200):**

```json
{
	"output_dir": "data/models/lora_output",
	"status": "success",
	"message": "Treinamento concluído com sucesso"
}
```

### 5. Chat

#### POST /chat/add-context

Adiciona textos ao contexto do chat.

**Corpo da requisição:**

```json
["Texto 1 para adicionar ao contexto", "Texto 2 para adicionar ao contexto"]
```

**Resposta (200):**

```json
{
	"status": "success",
	"message": "Adicionados 2 textos ao contexto",
	"total_texts": 5
}
```

#### POST /chat/

Realiza uma conversa com o sistema.

**Corpo da requisição:**

```json
{
	"text": "Qual é a função do OmnisIA?"
}
```

**Resposta (200):**

```json
{
	"response": "Baseado no contexto encontrado, aqui está uma resposta para: 'Qual é a função do OmnisIA?'. Encontrei 3 textos relacionados.",
	"context": [
		"OmnisIA é um sistema de inteligência artificial multimodal.",
		"O sistema pode processar texto, áudio, vídeo e imagens."
	],
	"confidence": 0.8
}
```

#### GET /chat/context-info

Retorna informações sobre o contexto atual.

**Resposta (200):**

```json
{
	"total_texts": 5,
	"index_initialized": true
}
```

## Códigos de Erro

### 400 Bad Request

-   Validação de entrada falhou
-   Tipo de arquivo não suportado
-   Arquivo muito grande

### 422 Unprocessable Entity

-   Dados de entrada inválidos
-   Campos obrigatórios ausentes

### 500 Internal Server Error

-   Erro interno do servidor
-   Problemas de processamento

## Exemplos de Uso

### Python

```python
import requests

# Upload de arquivo
with open('documento.pdf', 'rb') as f:
    files = {'file': ('documento.pdf', f, 'application/pdf')}
    response = requests.post('http://localhost:8000/upload/', files=files)
    print(response.json())

# Chat
response = requests.post('http://localhost:8000/chat/',
                        json={'text': 'Olá, como você está?'})
print(response.json())
```

### cURL

```bash
# Upload
curl -X POST "http://localhost:8000/upload/" \
     -F "file=@documento.pdf"

# Chat
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"text": "Olá, como você está?"}'
```

## Configuração

As configurações da API podem ser ajustadas no arquivo `backend/config.py`:

-   Tipos de arquivo permitidos
-   Tamanho máximo de upload
-   Modelos suportados
-   Configurações de LoRA
-   Configurações de embeddings

## Limitações

-   Tamanho máximo de arquivo: 100MB
-   Modelos de Whisper: tiny, base, small, medium, large
-   Modelos de treinamento: GPT-2 e DialoGPT
-   Embeddings: all-MiniLM-L6-v2
