# Frontend OmnisIA Trainer Web

Interface web moderna e responsiva para o sistema OmnisIA Trainer Web, construída com Streamlit.

## 🚀 Funcionalidades

### 📊 Dashboard

-   **Métricas em tempo real**: Arquivos, contextos, modelos e status da API
-   **Ações rápidas**: Acesso direto às principais funcionalidades
-   **Atividade recente**: Lista dos últimos arquivos enviados

### 📤 Upload de Arquivos

-   **Interface drag-and-drop**: Upload intuitivo de arquivos
-   **Validação visual**: Informações do arquivo antes do envio
-   **Lista organizada**: Visualização em tabela com estatísticas
-   **Suporte múltiplo**: PDF, TXT, imagens, áudio e vídeo

### 🔧 Pré-processamento

-   **OCR de PDF**: Extração de texto com interface amigável
-   **Transcrição de áudio**: Múltiplos modelos Whisper
-   **Transcrição de vídeo**: Processamento automático
-   **OCR de imagem**: Extração de texto de imagens

### 🎯 Treinamento

-   **Seleção de modelos**: Interface para escolha do modelo base
-   **Configuração LoRA**: Parâmetros de treinamento
-   **Monitoramento**: Status e progresso do treinamento

### 💬 Chat Inteligente

-   **Histórico persistente**: Conversas salvas na sessão
-   **Contexto dinâmico**: Adição e remoção de contextos
-   **Métricas de confiança**: Indicadores de qualidade da resposta
-   **Interface conversacional**: Chat natural e intuitivo

### 📊 Status do Sistema

-   **Monitoramento em tempo real**: Status da API e serviços
-   **Estatísticas detalhadas**: Métricas do sistema
-   **Logs do sistema**: Informações de debug

## 🛠️ Tecnologias

-   **Streamlit**: Framework web para aplicações de dados
-   **Pandas**: Manipulação e visualização de dados
-   **Requests**: Comunicação com a API REST
-   **Python**: Linguagem principal

## 📁 Estrutura

```
frontend/
├── app.py              # Aplicação principal
├── config.py           # Configurações centralizadas
├── utils.py            # Funções utilitárias
├── components.py       # Componentes reutilizáveis
├── test_frontend.py    # Testes automatizados
└── README.md           # Documentação
```

## 🚀 Instalação

### Pré-requisitos

-   Python 3.8+
-   Backend OmnisIA rodando em http://localhost:8000

### Instalação

```bash
# Instalar dependências
pip install streamlit pandas requests

# Executar o frontend
streamlit run app.py
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# URL da API (padrão: http://localhost:8000)
export API_URL=http://localhost:8000
```

### Configurações Personalizadas

Edite `config.py` para personalizar:

-   Tipos de arquivo suportados
-   Configurações de UI
-   Mensagens e placeholders
-   Limites e thresholds

## 📖 Uso

### 1. Dashboard

-   Acesse a página inicial para ver métricas do sistema
-   Use as ações rápidas para navegar

### 2. Upload

-   Arraste arquivos ou clique para selecionar
-   Visualize informações antes do envio
-   Acompanhe o progresso do upload

### 3. Pré-processamento

-   Selecione o tipo de processamento
-   Configure parâmetros específicos
-   Monitore o progresso

### 4. Treinamento

-   Escolha o modelo base
-   Configure dataset e saída
-   Inicie o treinamento

### 5. Chat

-   Adicione contextos relevantes
-   Faça perguntas naturalmente
-   Visualize histórico e confiança

### 6. Status

-   Monitore saúde do sistema
-   Visualize estatísticas
-   Verifique logs

## 🧪 Testes

### Executar Testes

```bash
cd frontend
python test_frontend.py
```

### Cobertura de Testes

-   ✅ Funções utilitárias
-   ✅ Configurações
-   ✅ Integração com API
-   ✅ Validações de entrada

## 🎨 Personalização

### Temas

Edite `config.py` para personalizar cores:

```python
UI_CONFIG = {
    "theme": "light",
    "primary_color": "#FF6B6B",
    "secondary_color": "#4ECDC4",
    # ...
}
```

### Componentes

Use `components.py` para criar componentes reutilizáveis:

```python
from components import file_upload_component

# Usar componente
result = file_upload_component(api_url)
```

## 🔍 Debug

### Logs

-   Verifique logs no console do Streamlit
-   Use `st.write()` para debug temporário

### Conexão com API

-   Teste conectividade: `python -c "from utils import check_api_connection; print(check_api_connection('http://localhost:8000'))"`

### Erros Comuns

1. **API offline**: Verifique se o backend está rodando
2. **Arquivo não encontrado**: Verifique caminhos no backend
3. **Timeout**: Aumente `API_TIMEOUT` em `config.py`

## 📈 Performance

### Otimizações

-   Cache de sessão para dados frequentes
-   Lazy loading de componentes pesados
-   Timeout configurável para API calls

### Monitoramento

-   Métricas de tempo de resposta
-   Uso de memória
-   Status de conectividade

## 🤝 Contribuição

### Desenvolvimento

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente com testes
4. Execute testes: `python test_frontend.py`
5. Abra um Pull Request

### Padrões

-   Use type hints
-   Documente funções
-   Siga PEP 8
-   Adicione testes para novas funcionalidades

## 📄 Licença

Este projeto está sob a licença MIT.

## 🔗 Links

-   [Streamlit Documentation](https://docs.streamlit.io/)
-   [API Documentation](../docs/API.md)
-   [Backend Repository](../backend/)
-   [Exemplos de Uso](../examples/)
