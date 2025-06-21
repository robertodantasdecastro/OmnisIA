# OmnisIA

OmnisIA é um framework multimodal open-source para criação de agentes de IA especializadas.

## Requisitos

- Python 3.10+
- Tesseract OCR
- FFmpeg

Recomenda-se hardware com 8GB de RAM e GPU com 8GB para treinar modelos pequenos.

## Instalação

```bash
./setup.sh
```

## Uso básico

- **OCR de PDF**
  ```bash
  python main.py ingest-pdf arquivo.pdf saida.pdf
  ```
- **Transcrição de áudio**
  ```bash
  python main.py transcribe audio.wav --model-size base
  ```
- **Criação de índice e Fine-tuning**
  ```bash
  python main.py build-index "texto de exemplo"
  python main.py train modelo dataset.txt saida/
  ```

A API web pode ser iniciada executando `uvicorn web.api:app` após o treinamento.
