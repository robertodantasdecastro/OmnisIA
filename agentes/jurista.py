"""Agente de exemplo para domínio jurídico."""
from ..modelos.rag import build_rag


def criar_agente_juridico(retriever):
    return build_rag("google/flan-t5-base", retriever)
