"""Rotinas simples de limpeza de texto."""

def clean_text(text: str) -> str:
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text
