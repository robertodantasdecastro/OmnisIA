"""Funções utilitárias gerais."""
from pathlib import Path


def lista_arquivos(pasta: Path, ext: str = "*"):
    return list(pasta.rglob(ext))
