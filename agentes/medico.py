"""Agente de exemplo para domínio médico."""
from ..modelos.rag import build_rag


def criar_agente_medico(retriever):
    return build_rag("google/flan-t5-base", retriever)
