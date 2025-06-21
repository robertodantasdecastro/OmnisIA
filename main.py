"""CLI principal do OmnisIA."""
import typer
from pathlib import Path
from ingestao.ocr import ocr_pdf, ocr_image
from ingestao.stt import transcribe_audio
from processamento.vetorizacao import VectorStore
from processamento.limpeza import clean_text
from modelos.treinamento import finetune

app = typer.Typer()


@app.command()
def ingest_pdf(pdf: Path, saida: Path = typer.Argument(...)):
    """Realiza OCR em um PDF."""
    ocr_pdf(pdf, saida)
    typer.echo(f"PDF processado: {saida}")


@app.command()
def transcribe(audio: Path, model_size: str = "base"):
    """Transcreve um arquivo de áudio."""
    texto = transcribe_audio(audio, model_size)
    typer.echo(texto)


@app.command()
def build_index(texto: str):
    """Exemplo simples de criação de índice."""
    store = VectorStore()
    store.add_texts([clean_text(texto)])
    typer.echo("Index criado")


@app.command()
def train(model: str, data_file: Path, output: Path):
    """Fine-tuning simples."""
    from datasets import load_dataset

    dataset = load_dataset("text", data_files=str(data_file))["train"]
    finetune(model, dataset, str(output))


if __name__ == "__main__":
    app()
