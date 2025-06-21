# OmnisIA Trainer Web

Sistema web open source para automatizar ingestão, pré-processamento e treinamento generativo multimodal.

## Funcionalidades
- Upload de PDFs, imagens, áudios e vídeos
- OCR e transcrição automáticos
- Armazenamento vetorial em FAISS
- Fine-tuning leve com PEFT/LoRA
- Chat simples com o modelo

## Uso rápido
```bash
cd omnisia_web/scripts
./setup.sh
uvicorn omnisia_web.backend.main:app --reload
```
Abra outro terminal para o frontend:
```bash
streamlit run omnisia_web/frontend/app.py
```

Também é possível usar `docker-compose`:
```bash
docker-compose -f omnisia_web/docker/docker-compose.yml up --build
```

Este projeto faz parte de [OmnisIA](https://github.com/robertodantasdecastro/OmnisIA/frontend/).
