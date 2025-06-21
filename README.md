# OmnisIA – Universal Multimodal AI Framework

**OmnisIA** é uma plataforma open-source para criação, treinamento e personalização de agentes de Inteligência Artificial generativa com capacidade **multimodal e orientada a domínio**.

> Conecte dados brutos (textos, PDFs, vídeos, imagens, áudios) com modelos de linguagem open-source e crie IAs especializadas para saúde, direito, finanças, educação, engenharia, e muito mais.

---

## 🚀 Funcionalidades

- 🔎 Ingestão automática de dados via OCR, STT, RAG, embeddings e crawlers inteligentes
- 🧠 Treinamento leve com LoRA/QLoRA e suporte a RAG com FAISS ou Qdrant
- 🖼️ Multimodal: suporte a imagem, texto, áudio, vídeo, tabelas e gráficos
- 🧑‍⚖️ Domínios customizáveis: crie sua IA para direito, medicina, mercado, etc.
- 🧩 Modular e extensível: construa agentes autônomos via LangChain e CrewAI
- 💻 Otimizado para hardware básico

---

## 🔧 Tecnologias utilizadas

- [`transformers`](https://github.com/huggingface/transformers)
- [`peft`](https://github.com/huggingface/peft) / `QLoRA`
- [`LangChain`](https://github.com/langchain-ai/langchain)
- [`CrewAI`](https://github.com/joaomdmoura/crewAI)
- [`FAISS`](https://github.com/facebookresearch/faiss)
- [`Whisper`](https://github.com/openai/whisper)
- [`ocrmypdf`](https://github.com/ocrmypdf/OCRmyPDF)
- [`LLaVA`](https://github.com/haotian-liu/LLaVA) (imagem + texto)
- [`SentenceTransformers`](https://github.com/UKPLab/sentence-transformers)

---

## 📁 Estrutura inicial

```bash
omnisia/
├── ingestao/
│   ├── ocr.py
│   ├── stt.py
│   └── imagem.py
├── processamento/
│   ├── vetorizacao.py
│   └── limpeza.py
├── modelos/
│   ├── treinamento.py
│   └── rag.py
├── agentes/
│   ├── jurista.py
│   └── medico.py
├── web/
│   └── api.py
├── utils/
├── Dockerfile
├── requirements.txt
└── README.md

## ▶️ Uso rápido

1. Instale as dependências:
   ```bash
   ./setup.sh
   ```
2. Execute um comando de exemplo:
   ```bash
   python main.py ingest-pdf entrada.pdf saida.pdf
   ```

Mais detalhes em [docs/README.md](docs/README.md).
