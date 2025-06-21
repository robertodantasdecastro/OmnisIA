from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, validator, Field
from ..services.embeddings import EmbeddingService
from ..config import MAX_MESSAGE_LENGTH, DEFAULT_QUERY_LIMIT, CONFIDENCE_THRESHOLDS
from typing import List, Optional
import logging

router = APIRouter()
logger = logging.getLogger("omnisia.chat")

# Instância global do serviço de embeddings
embedding_service = EmbeddingService()


class ChatRequest(BaseModel):
    text: str = Field(..., description="Texto da mensagem do usuário")
    context: Optional[List[str]] = Field(
        None, description="Contexto adicional para a consulta"
    )
    query_limit: Optional[int] = Field(
        DEFAULT_QUERY_LIMIT, description="Limite de resultados de busca"
    )
    embedding_model: Optional[str] = Field(
        None, description="Modelo de embedding a usar"
    )

    @validator("text")
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError("Texto não pode estar vazio")
        if len(v) > MAX_MESSAGE_LENGTH:
            raise ValueError(
                f"Texto muito longo (máximo {MAX_MESSAGE_LENGTH} caracteres)"
            )
        return v.strip()

    @validator("query_limit")
    def validate_query_limit(cls, v):
        if v is not None and (v < 1 or v > 20):
            raise ValueError("Limite de consulta deve estar entre 1 e 20")
        return v or DEFAULT_QUERY_LIMIT


class ChatResponse(BaseModel):
    response: str = Field(..., description="Resposta do assistente")
    context: Optional[List[str]] = Field(
        None, description="Contexto usado para gerar a resposta"
    )
    confidence: Optional[float] = Field(
        None, description="Nível de confiança da resposta"
    )
    sources: Optional[List[dict]] = Field(None, description="Fontes dos dados usados")
    metadata: Optional[dict] = Field(None, description="Metadados adicionais")


class ContextRequest(BaseModel):
    texts: List[str] = Field(
        ..., description="Lista de textos para adicionar ao contexto"
    )

    @validator("texts")
    def validate_texts(cls, v):
        if not v:
            raise ValueError("Lista de textos não pode estar vazia")
        if len(v) > 100:
            raise ValueError("Máximo de 100 textos por vez")

        # Valida cada texto
        for i, text in enumerate(v):
            if not text or not text.strip():
                raise ValueError(f"Texto {i+1} não pode estar vazio")
            if len(text) > 5000:
                raise ValueError(f"Texto {i+1} muito longo (máximo 5000 caracteres)")

        return [text.strip() for text in v]


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Chat com resposta baseada em contexto"""
    try:
        logger.info(f"Nova mensagem de chat: {req.text[:100]}...")

        # Adiciona contexto extra se fornecido
        if req.context:
            embedding_service.add_texts(req.context)
            logger.info(f"Adicionado contexto extra: {len(req.context)} textos")

        # Busca contexto similar
        similar_texts = embedding_service.query(req.text, k=req.query_limit)

        # Gera resposta baseada no contexto
        if similar_texts:
            context = [text for text, _ in similar_texts]
            distances = [distance for _, distance in similar_texts]
            avg_distance = sum(distances) / len(distances)

            # Calcula confiança baseada na distância média
            confidence = max(0.0, 1.0 - (avg_distance / 2.0))  # Normaliza para 0-1

            # Determina nível de confiança
            if confidence >= CONFIDENCE_THRESHOLDS["high"]:
                confidence_level = "alta"
            elif confidence >= CONFIDENCE_THRESHOLDS["medium"]:
                confidence_level = "média"
            else:
                confidence_level = "baixa"

            response = (
                f"Baseado no contexto encontrado (confiança {confidence_level}), "
                f"aqui está uma resposta para: '{req.text}'. "
                f"Encontrei {len(context)} textos relacionados que podem ajudar a responder sua pergunta."
            )

            sources = [
                {
                    "text": text[:200] + "..." if len(text) > 200 else text,
                    "distance": float(dist),
                    "relevance": max(0.0, 1.0 - (dist / 2.0)),
                }
                for text, dist in similar_texts
            ]

        else:
            context = []
            confidence = 0.1
            response = (
                f"Você disse: '{req.text}'. "
                f"Não encontrei contexto específico para esta pergunta em minha base de conhecimento. "
                f"Você pode adicionar mais informações ao contexto para que eu possa ajudar melhor."
            )
            sources = []

        logger.info(f"Resposta gerada com confiança: {confidence:.2f}")

        return ChatResponse(
            response=response,
            context=context,
            confidence=confidence,
            sources=sources,
            metadata={
                "query_limit": req.query_limit,
                "total_context_texts": len(embedding_service.texts),
                "similar_texts_found": len(similar_texts),
            },
        )

    except Exception as e:
        logger.error(f"Erro no chat: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro no chat: {str(e)}")


@router.post("/add-context")
async def add_context(req: ContextRequest):
    """Adiciona textos ao contexto do chat"""
    try:
        logger.info(f"Adicionando {len(req.texts)} textos ao contexto")

        embedding_service.add_texts(req.texts)

        return {
            "status": "success",
            "message": f"Adicionados {len(req.texts)} textos ao contexto",
            "total_texts": len(embedding_service.texts),
            "new_texts": len(req.texts),
        }
    except Exception as e:
        logger.error(f"Erro ao adicionar contexto: {str(e)}", exc_info=True)
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
            "embedding_model": (
                embedding_service.model.get_sentence_embedding_dimension()
                if hasattr(embedding_service.model, "get_sentence_embedding_dimension")
                else "unknown"
            ),
            "index_type": (
                type(embedding_service.index).__name__
                if embedding_service.index
                else None
            ),
        }
    except Exception as e:
        logger.error(f"Erro ao obter informações: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro ao obter informações: {str(e)}"
        )


@router.delete("/context")
async def clear_context():
    """Limpa todo o contexto armazenado"""
    try:
        # Reinicializa o serviço de embeddings
        global embedding_service
        embedding_service = EmbeddingService()

        logger.info("Contexto limpo com sucesso")

        return {
            "status": "success",
            "message": "Contexto limpo com sucesso",
            "total_texts": 0,
        }
    except Exception as e:
        logger.error(f"Erro ao limpar contexto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Erro ao limpar contexto: {str(e)}"
        )


@router.get("/models")
async def list_embedding_models():
    """Lista modelos de embedding disponíveis"""
    return {
        "models": [
            {
                "name": "all-MiniLM-L6-v2",
                "description": "Modelo leve e rápido, boa performance geral",
                "dimensions": 384,
            },
            {
                "name": "all-mpnet-base-v2",
                "description": "Modelo com melhor qualidade, mais lento",
                "dimensions": 768,
            },
            {
                "name": "all-MiniLM-L12-v2",
                "description": "Modelo intermediário",
                "dimensions": 384,
            },
        ],
        "current_model": (
            embedding_service.model.get_sentence_embedding_dimension()
            if hasattr(embedding_service.model, "get_sentence_embedding_dimension")
            else "unknown"
        ),
    }
