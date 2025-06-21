from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator
from ..services.embeddings import EmbeddingService
from typing import List, Optional

router = APIRouter()

# Instância global do serviço de embeddings
embedding_service = EmbeddingService()


class ChatRequest(BaseModel):
    text: str

    @validator("text")
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Texto não pode estar vazio")
        if len(v) > 1000:
            raise ValueError("Texto muito longo (máximo 1000 caracteres)")
        return v.strip()


class ChatResponse(BaseModel):
    response: str
    context: Optional[List[str]] = None
    confidence: Optional[float] = None


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Chat com resposta baseada em contexto"""
    try:
        # Busca contexto similar
        similar_texts = embedding_service.query(req.text, k=3)

        # Gera resposta baseada no contexto
        if similar_texts:
            context = [text for text, _ in similar_texts]
            # Simula uma resposta baseada no contexto
            response = f"Baseado no contexto encontrado, aqui está uma resposta para: '{req.text}'. "
            response += f"Encontrei {len(context)} textos relacionados."
        else:
            context = []
            response = f"Você disse: '{req.text}'. Não encontrei contexto específico para esta pergunta."

        return ChatResponse(
            response=response, context=context, confidence=0.8 if context else 0.3
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no chat: {str(e)}")


@router.post("/add-context")
async def add_context(texts: List[str]):
    """Adiciona textos ao contexto do chat"""
    try:
        if not texts:
            raise HTTPException(
                status_code=400, detail="Lista de textos não pode estar vazia"
            )

        embedding_service.add_texts(texts)
        return {
            "status": "success",
            "message": f"Adicionados {len(texts)} textos ao contexto",
            "total_texts": len(embedding_service.texts),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao adicionar contexto: {str(e)}"
        )


@router.get("/context-info")
async def get_context_info():
    """Retorna informações sobre o contexto atual"""
    try:
        return {
            "total_texts": len(embedding_service.texts),
            "index_initialized": embedding_service.index is not None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter informações: {str(e)}"
        )
