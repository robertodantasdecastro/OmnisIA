# Configurações Centralizadas - OmnisIA Trainer Web

Este documento descreve todas as configurações centralizadas disponíveis no arquivo `config.py` e como usá-las.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Configurações da API](#configurações-da-api)
3. [Configurações da Interface](#configurações-da-interface)
4. [Configurações de Upload](#configurações-de-upload)
5. [Configurações de Chat](#configurações-de-chat)
6. [Configurações de Pré-processamento](#configurações-de-pré-processamento)
7. [Configurações de Treinamento](#configurações-de-treinamento)
8. [Configurações de Métricas](#configurações-de-métricas)
9. [Configurações de Sessão](#configurações-de-sessão)
10. [Configurações de UI](#configurações-de-ui)
11. [Configurações de Navegação](#configurações-de-navegação)
12. [Configurações de Links Úteis](#configurações-de-links-úteis)
13. [Configurações de Mensagens](#configurações-de-mensagens)
14. [Configurações de Placeholders](#configurações-de-placeholders)
15. [Configurações de Ajuda](#configurações-de-ajuda)
16. [Configurações de Log](#configurações-de-log)
17. [Configurações de Segurança](#configurações-de-segurança)
18. [Configurações de Cache](#configurações-de-cache)
19. [Configurações de Performance](#configurações-de-performance)
20. [Configurações de Versão](#configurações-de-versão)
21. [Configurações de Desenvolvimento](#configurações-de-desenvolvimento)
22. [Configurações de Banco de Dados](#configurações-de-banco-de-dados)
23. [Configurações de Redis](#configurações-de-redis)
24. [Variáveis de Ambiente](#variáveis-de-ambiente)
25. [Funções de Configuração](#funções-de-configuração)
26. [Exemplos de Uso](#exemplos-de-uso)

## 🎯 Visão Geral

O arquivo `config.py` centraliza todas as configurações da aplicação, permitindo:

-   **Flexibilidade**: Configuração via variáveis de ambiente
-   **Manutenibilidade**: Todas as configurações em um local
-   **Segurança**: Valores padrão seguros
-   **Debugging**: Configurações específicas para desenvolvimento

## 🌐 Configurações da API

### Variáveis

| Variável             | Padrão                  | Descrição                           |
| -------------------- | ----------------------- | ----------------------------------- |
| `API_URL`            | `http://localhost:8000` | URL base da API backend             |
| `API_TIMEOUT`        | `30`                    | Timeout das requisições em segundos |
| `API_RETRY_ATTEMPTS` | `3`                     | Número de tentativas de retry       |

### Uso

```python
from config import API_URL, API_TIMEOUT, get_api_url

# Acessar URL da API
api_url = get_api_url()

# Fazer requisição com timeout personalizado
import requests
response = requests.get(f"{api_url}/health", timeout=API_TIMEOUT)
```

## 🎨 Configurações da Interface

### Variáveis

| Variável                | Padrão                  | Descrição                 |
| ----------------------- | ----------------------- | ------------------------- |
| `PAGE_TITLE`            | `"OmnisIA Trainer Web"` | Título da página          |
| `PAGE_ICON`             | `"🤖"`                  | Ícone da página           |
| `LAYOUT`                | `"wide"`                | Layout do Streamlit       |
| `INITIAL_SIDEBAR_STATE` | `"expanded"`            | Estado inicial da sidebar |
| `THEME`                 | `"light"`               | Tema da interface         |

### Uso

```python
from config import PAGE_TITLE, PAGE_ICON, LAYOUT

import streamlit as st
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT
)
```

## 📤 Configurações de Upload

### Variáveis

| Variável                    | Padrão             | Descrição                           |
| --------------------------- | ------------------ | ----------------------------------- |
| `MAX_FILE_SIZE_MB`          | `100`              | Tamanho máximo de arquivo em MB     |
| `MAX_FILE_SIZE_BYTES`       | `104857600`        | Tamanho máximo em bytes (calculado) |
| `SUPPORTED_FILE_TYPES`      | Dict com tipos     | Tipos de arquivo suportados         |
| `SUPPORTED_FILE_EXTENSIONS` | Lista de extensões | Extensões suportadas                |

### Tipos Suportados

```python
SUPPORTED_FILE_TYPES = {
    "pdf": "📄",
    "txt": "📝",
    "jpg": "🖼️",
    "jpeg": "🖼️",
    "png": "🖼️",
    "gif": "🖼️",
    "mp3": "🎵",
    "wav": "🎵",
    "mp4": "🎬",
    "avi": "🎬",
    "mov": "🎬"
}
```

### Uso

```python
from config import get_supported_file_types, MAX_FILE_SIZE_BYTES

# Obter tipos suportados
file_types = get_supported_file_types()

# Validar arquivo
if uploaded_file.size > MAX_FILE_SIZE_BYTES:
    st.error("Arquivo muito grande")
```

## 💬 Configurações de Chat

### Variáveis

| Variável                | Padrão | Descrição                        |
| ----------------------- | ------ | -------------------------------- |
| `MAX_CHAT_HISTORY`      | `50`   | Máximo de mensagens no histórico |
| `MAX_CONTEXT_LENGTH`    | `1000` | Comprimento máximo do contexto   |
| `MAX_MESSAGE_LENGTH`    | `1000` | Comprimento máximo da mensagem   |
| `CONFIDENCE_THRESHOLDS` | Dict   | Limites de confiança             |
| `CHAT_REFRESH_INTERVAL` | `5`    | Intervalo de refresh em segundos |

### Limites de Confiança

```python
CONFIDENCE_THRESHOLDS = {
    "high": 0.7,    # Alta confiança
    "medium": 0.4,  # Média confiança
    "low": 0.0      # Baixa confiança
}
```

### Uso

```python
from config import MAX_CHAT_HISTORY, CONFIDENCE_THRESHOLDS

# Limitar histórico
if len(chat_history) >= MAX_CHAT_HISTORY:
    chat_history = chat_history[-MAX_CHAT_HISTORY:]

# Verificar confiança
confidence = 0.8
if confidence >= CONFIDENCE_THRESHOLDS["high"]:
    print("Alta confiança")
```

## 🔧 Configurações de Pré-processamento

### Variáveis

| Variável                     | Padrão           | Descrição                   |
| ---------------------------- | ---------------- | --------------------------- |
| `WHISPER_MODELS`             | Lista de modelos | Modelos Whisper disponíveis |
| `DEFAULT_WHISPER_MODEL`      | `"base"`         | Modelo Whisper padrão       |
| `WHISPER_MODEL_DESCRIPTIONS` | Dict             | Descrições dos modelos      |
| `OCR_LANGUAGES`              | `["por", "eng"]` | Idiomas OCR suportados      |
| `DEFAULT_OCR_LANGUAGE`       | `"por+eng"`      | Idioma OCR padrão           |

### Modelos Whisper

```python
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]

WHISPER_MODEL_DESCRIPTIONS = {
    "tiny": "Mais rápido, menos preciso",
    "base": "Equilibrado",
    "small": "Bom equilíbrio",
    "medium": "Mais preciso, mais lento",
    "large": "Mais lento, mais preciso"
}
```

### Uso

```python
from config import get_whisper_models, get_whisper_model_description

# Obter modelos disponíveis
models = get_whisper_models()

# Obter descrição
description = get_whisper_model_description("base")
```

## 🎯 Configurações de Treinamento

### Variáveis

| Variável              | Padrão               | Descrição                   |
| --------------------- | -------------------- | --------------------------- |
| `DEFAULT_MODELS`      | Lista de modelos     | Modelos base disponíveis    |
| `EMBEDDING_MODEL`     | `"all-MiniLM-L6-v2"` | Modelo de embedding         |
| `DEFAULT_QUERY_LIMIT` | `5`                  | Limite padrão de consultas  |
| `LORA_CONFIG`         | Dict                 | Configuração LoRA           |
| `TRAINING_CONFIG`     | Dict                 | Configuração de treinamento |

### Configuração LoRA

```python
LORA_CONFIG = {
    'r': 16,                    # Rank da decomposição
    'lora_alpha': 32,           # Parâmetro alpha
    'lora_dropout': 0.1,        # Taxa de dropout
    'target_modules': ["q_proj", "v_proj"]  # Módulos alvo
}
```

### Configuração de Treinamento

```python
TRAINING_CONFIG = {
    'num_train_epochs': 3,
    'per_device_train_batch_size': 4,
    'gradient_accumulation_steps': 4,
    'warmup_steps': 100,
    'learning_rate': 2e-4,
    'fp16': True,
    'logging_steps': 10,
    'save_steps': 100
}
```

### Uso

```python
from config import get_model_options, LORA_CONFIG, TRAINING_CONFIG

# Obter modelos disponíveis
models = get_model_options()

# Usar configuração LoRA
lora_r = LORA_CONFIG['r']

# Usar configuração de treinamento
epochs = TRAINING_CONFIG['num_train_epochs']
```

## 📊 Configurações de Métricas

### Variáveis

| Variável                    | Padrão | Descrição                             |
| --------------------------- | ------ | ------------------------------------- |
| `METRICS_REFRESH_INTERVAL`  | `30`   | Intervalo de refresh das métricas     |
| `RECENT_FILES_LIMIT`        | `5`    | Limite de arquivos recentes           |
| `DASHBOARD_UPDATE_INTERVAL` | `10`   | Intervalo de atualização do dashboard |

## 🔐 Configurações de Sessão

### Variáveis

| Variável       | Padrão | Descrição                  |
| -------------- | ------ | -------------------------- |
| `SESSION_KEYS` | Dict   | Chaves da sessão Streamlit |

### Chaves de Sessão

```python
SESSION_KEYS = {
    "chat_history": "chat_history",
    "uploaded_files": "uploaded_files",
    "context_texts": "context_texts",
    "user_preferences": "user_preferences",
    "last_api_check": "last_api_check",
    "cached_models": "cached_models",
    "cached_files": "cached_files"
}
```

### Uso

```python
from config import SESSION_KEYS
import streamlit as st

# Acessar dados da sessão
chat_history = st.session_state.get(SESSION_KEYS["chat_history"], [])
```

## 🎨 Configurações de UI

### Variáveis

| Variável    | Padrão | Descrição                     |
| ----------- | ------ | ----------------------------- |
| `UI_CONFIG` | Dict   | Configurações de cores e tema |

### Configuração de UI

```python
UI_CONFIG = {
    "theme": "light",
    "primary_color": "#FF6B6B",
    "secondary_color": "#4ECDC4",
    "success_color": "#45B7D1",
    "warning_color": "#96CEB4",
    "error_color": "#FFEAA7",
    "background_color": "#FFFFFF",
    "text_color": "#2C3E50"
}
```

## 🧭 Configurações de Navegação

### Variáveis

| Variável           | Padrão           | Descrição            |
| ------------------ | ---------------- | -------------------- |
| `NAVIGATION_PAGES` | Lista            | Páginas de navegação |
| `DEFAULT_PAGE`     | `"🏠 Dashboard"` | Página padrão        |

### Páginas de Navegação

```python
NAVIGATION_PAGES = [
    "🏠 Dashboard",
    "📤 Upload",
    "🔧 Pré-processamento",
    "🎯 Treinamento",
    "💬 Chat",
    "📊 Status"
]
```

### Uso

```python
from config import get_navigation_pages, DEFAULT_PAGE

# Obter páginas disponíveis
pages = get_navigation_pages()

# Usar página padrão
selected_page = st.sidebar.selectbox("Páginas", pages, index=pages.index(DEFAULT_PAGE))
```

## 🔗 Configurações de Links Úteis

### Variáveis

| Variável       | Padrão | Descrição                |
| -------------- | ------ | ------------------------ |
| `USEFUL_LINKS` | Dict   | Links úteis da aplicação |

### Links Úteis

```python
USEFUL_LINKS = {
    "Documentação da API": "docs/API.md",
    "Exemplos de Uso": "examples/example_usage.py",
    "GitHub": "https://github.com/robertodantasdecastro/OmnisIA",
    "Issues": "https://github.com/robertodantasdecastro/OmnisIA/issues",
    "Wiki": "https://github.com/robertodantasdecastro/OmnisIA/wiki"
}
```

## 💬 Configurações de Mensagens

### Variáveis

| Variável   | Padrão | Descrição            |
| ---------- | ------ | -------------------- |
| `MESSAGES` | Dict   | Mensagens do sistema |

### Mensagens do Sistema

```python
MESSAGES = {
    "api_offline": "❌ Não foi possível conectar ao backend...",
    "upload_success": "✅ Arquivo enviado com sucesso!",
    "upload_error": "❌ Erro no upload: {}",
    # ... outras mensagens
}
```

### Uso

```python
from config import get_messages

messages = get_messages()
st.error(messages["api_offline"])
```

## 📝 Configurações de Placeholders

### Variáveis

| Variável       | Padrão | Descrição                |
| -------------- | ------ | ------------------------ |
| `PLACEHOLDERS` | Dict   | Placeholders para campos |

### Placeholders

```python
PLACEHOLDERS = {
    "pdf_path": "data/uploads/documento.pdf",
    "audio_path": "data/uploads/audio.wav",
    "chat_message": "Faça uma pergunta...",
    "context_text": "Digite um texto por linha...",
    # ... outros placeholders
}
```

### Uso

```python
from config import get_placeholders

placeholders = get_placeholders()
user_input = st.text_input("Mensagem", placeholder=placeholders["chat_message"])
```

## ❓ Configurações de Ajuda

### Variáveis

| Variável     | Padrão | Descrição       |
| ------------ | ------ | --------------- |
| `HELP_TEXTS` | Dict   | Textos de ajuda |

### Textos de Ajuda

```python
HELP_TEXTS = {
    "file_upload": "Arquivos suportados: PDF, TXT, imagens...",
    "whisper_model": "Modelos maiores são mais precisos mas mais lentos",
    "lora_training": "LoRA: Treinamento eficiente com poucos parâmetros",
    # ... outros textos
}
```

### Uso

```python
from config import get_help_texts

help_texts = get_help_texts()
st.help(help_texts["file_upload"])
```

## 📝 Configurações de Log

### Variáveis

| Variável       | Padrão                | Descrição       |
| -------------- | --------------------- | --------------- |
| `LOG_LEVEL`    | `"INFO"`              | Nível de log    |
| `LOG_FILE`     | `"logs/frontend.log"` | Arquivo de log  |
| `ENABLE_DEBUG` | `false`               | Habilitar debug |

### Uso

```python
from config import LOG_LEVEL, LOG_FILE, ENABLE_DEBUG
import logging

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    filename=LOG_FILE
)
```

## 🔒 Configurações de Segurança

### Variáveis

| Variável        | Padrão                       | Descrição        |
| --------------- | ---------------------------- | ---------------- |
| `SECRET_KEY`    | `"your-secret-key-here"`     | Chave secreta    |
| `ALLOWED_HOSTS` | `["localhost", "127.0.0.1"]` | Hosts permitidos |
| `CSRF_ENABLED`  | `true`                       | Habilitar CSRF   |

## 🗄️ Configurações de Cache

### Variáveis

| Variável         | Padrão | Descrição                |
| ---------------- | ------ | ------------------------ |
| `CACHE_ENABLED`  | `true` | Habilitar cache          |
| `CACHE_TTL`      | `300`  | TTL do cache em segundos |
| `CACHE_MAX_SIZE` | `100`  | Tamanho máximo do cache  |

## ⚡ Configurações de Performance

### Variáveis

| Variável                  | Padrão | Descrição                          |
| ------------------------- | ------ | ---------------------------------- |
| `ENABLE_LAZY_LOADING`     | `true` | Habilitar lazy loading             |
| `MAX_CONCURRENT_REQUESTS` | `5`    | Máximo de requisições concorrentes |
| `REQUEST_TIMEOUT`         | `30`   | Timeout das requisições            |

## 📦 Configurações de Versão

### Variáveis

| Variável     | Padrão                              | Descrição           |
| ------------ | ----------------------------------- | ------------------- |
| `VERSION`    | `"1.0.0"`                           | Versão da aplicação |
| `BUILD_DATE` | `"2024-01-01"`                      | Data de build       |
| `AUTHOR`     | `"Roberto Dantas de Castro"`        | Autor               |
| `EMAIL`      | `"robertodantasdecastro@gmail.com"` | Email do autor      |

### Uso

```python
from config import get_version_info

version_info = get_version_info()
print(f"Versão: {version_info['version']}")
```

## 🔧 Configurações de Desenvolvimento

### Variáveis

| Variável            | Padrão  | Descrição                    |
| ------------------- | ------- | ---------------------------- |
| `DEVELOPMENT_MODE`  | `false` | Modo desenvolvimento         |
| `ENABLE_HOT_RELOAD` | `true`  | Habilitar hot reload         |
| `SHOW_DEBUG_INFO`   | `false` | Mostrar informações de debug |

### Uso

```python
from config import is_development_mode, is_debug_enabled

if is_development_mode():
    print("Modo desenvolvimento ativado")

if is_debug_enabled():
    print("Debug habilitado")
```

## 🗄️ Configurações de Banco de Dados

### Variáveis

| Variável                | Padrão                     | Descrição                   |
| ----------------------- | -------------------------- | --------------------------- |
| `DATABASE_URL`          | `"sqlite:///./omnisia.db"` | URL do banco de dados       |
| `DATABASE_POOL_SIZE`    | `10`                       | Tamanho do pool de conexões |
| `DATABASE_MAX_OVERFLOW` | `20`                       | Overflow máximo do pool     |

## 🔴 Configurações de Redis

### Variáveis

| Variável         | Padrão                     | Descrição      |
| ---------------- | -------------------------- | -------------- |
| `REDIS_URL`      | `"redis://localhost:6379"` | URL do Redis   |
| `REDIS_DB`       | `0`                        | Banco do Redis |
| `REDIS_PASSWORD` | `""`                       | Senha do Redis |

## 🌍 Variáveis de Ambiente

Para personalizar as configurações, defina as seguintes variáveis de ambiente:

### API

```bash
export API_URL="http://localhost:8000"
export API_TIMEOUT="30"
export API_RETRY_ATTEMPTS="3"
```

### Upload

```bash
export MAX_FILE_SIZE_MB="100"
```

### Log e Debug

```bash
export LOG_LEVEL="INFO"
export ENABLE_DEBUG="false"
export DEVELOPMENT_MODE="false"
```

### Segurança

```bash
export SECRET_KEY="your-secret-key-here"
export ALLOWED_HOSTS="localhost,127.0.0.1"
export CSRF_ENABLED="true"
```

### Cache

```bash
export CACHE_ENABLED="true"
export CACHE_TTL="300"
export CACHE_MAX_SIZE="100"
```

### Performance

```bash
export ENABLE_LAZY_LOADING="true"
export MAX_CONCURRENT_REQUESTS="5"
export REQUEST_TIMEOUT="30"
```

### Treinamento

```bash
export LORA_R="16"
export LORA_ALPHA="32"
export LORA_DROPOUT="0.1"
export TRAINING_EPOCHS="3"
export TRAINING_BATCH_SIZE="4"
export TRAINING_LEARNING_RATE="2e-4"
```

## 🔧 Funções de Configuração

O arquivo `config.py` também fornece funções úteis:

### Funções Disponíveis

| Função                       | Descrição                                |
| ---------------------------- | ---------------------------------------- |
| `get_api_url()`              | Retorna a URL da API                     |
| `get_supported_file_types()` | Retorna tipos de arquivo suportados      |
| `get_whisper_models()`       | Retorna modelos Whisper disponíveis      |
| `get_navigation_pages()`     | Retorna páginas de navegação             |
| `get_messages()`             | Retorna mensagens do sistema             |
| `get_placeholders()`         | Retorna placeholders                     |
| `get_help_texts()`           | Retorna textos de ajuda                  |
| `is_development_mode()`      | Verifica se está em modo desenvolvimento |
| `is_debug_enabled()`         | Verifica se debug está habilitado        |

### Uso

```python
from config import (
    get_api_url, get_supported_file_types,
    is_development_mode, is_debug_enabled
)

# Obter configurações
api_url = get_api_url()
file_types = get_supported_file_types()

# Verificar modo
if is_development_mode():
    print("Modo desenvolvimento")

if is_debug_enabled():
    print("Debug ativado")
```

## 💡 Exemplos de Uso

### Exemplo 1: Configuração de Upload

```python
from config import (
    MAX_FILE_SIZE_BYTES,
    get_supported_file_types,
    validate_file_upload
)

def handle_file_upload(uploaded_file):
    # Validar arquivo
    is_valid, error_msg = validate_file_upload(uploaded_file)

    if not is_valid:
        st.error(error_msg)
        return

    # Processar arquivo
    st.success("Arquivo válido!")
```

### Exemplo 2: Configuração de Chat

```python
from config import (
    MAX_CHAT_HISTORY,
    MAX_MESSAGE_LENGTH,
    get_messages
)

def handle_chat_message(message):
    # Validar mensagem
    if len(message) > MAX_MESSAGE_LENGTH:
        st.error("Mensagem muito longa")
        return

    # Adicionar ao histórico
    add_chat_message("user", message)

    # Limitar histórico
    history = get_chat_history()
    if len(history) > MAX_CHAT_HISTORY:
        history = history[-MAX_CHAT_HISTORY:]
```

### Exemplo 3: Configuração de API

```python
from config import (
    get_api_url,
    API_TIMEOUT,
    check_api_health
)

def make_api_call():
    # Verificar se API está online
    if not check_api_health():
        st.error("API offline")
        return

    # Fazer chamada
    api_url = get_api_url()
    response = requests.get(f"{api_url}/health", timeout=API_TIMEOUT)
```

### Exemplo 4: Configuração de Debug

```python
from config import is_debug_enabled, log_function_call

def my_function(param1, param2):
    # Log de debug
    if is_debug_enabled():
        log_function_call("my_function", {"param1": param1, "param2": param2})

    # Lógica da função
    result = param1 + param2

    return result
```

## 🚀 Executando o Exemplo

Para ver todas as configurações em ação, execute:

```bash
cd frontend
python example_usage.py
```

Este comando mostrará todas as configurações disponíveis e seus valores atuais.

## 📚 Recursos Adicionais

-   [Arquivo de Configuração](config.py) - Código fonte das configurações
-   [Exemplo de Uso](example_usage.py) - Exemplos práticos
-   [Utilitários](utils.py) - Funções que usam as configurações
-   [Componentes](components.py) - Componentes que usam as configurações

---

**Nota**: Sempre use as funções de configuração quando possível, pois elas fornecem acesso seguro e consistente aos valores de configuração.
