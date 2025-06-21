"""
Classe Base para Provedores de Modelos
Base Class for Model Providers

Define interface comum para todos os provedores de modelos
Defines common interface for all model providers
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, AsyncGenerator
from enum import Enum
import logging

logger = logging.getLogger("omnisia.models")


class ModelType(Enum):
    """Tipos de modelos suportados / Supported model types"""

    CHAT = "chat"
    COMPLETION = "completion"
    EMBEDDING = "embedding"
    IMAGE = "image"
    AUDIO = "audio"
    CODE = "code"


class ModelProvider(ABC):
    """
    Classe base para provedores de modelos
    Base class for model providers
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        self.models = {}

    @abstractmethod
    async def initialize(self) -> bool:
        """
        Inicializa o provedor
        Initialize the provider
        """
        pass

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Gera resposta de chat
        Generate chat response
        """
        pass

    @abstractmethod
    async def text_completion(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Gera completação de texto
        Generate text completion
        """
        pass

    async def stream_completion(
        self,
        prompt: str,
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """
        Gera completação de texto em stream
        Generate streaming text completion
        """
        # Implementação padrão (não streaming)
        result = await self.text_completion(
            prompt, model, temperature, max_tokens, **kwargs
        )
        yield result.get("text", "")

    async def generate_embedding(
        self, text: str, model: str = None, **kwargs
    ) -> List[float]:
        """
        Gera embedding do texto
        Generate text embedding
        """
        raise NotImplementedError(f"Embeddings não implementado para {self.name}")

    async def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de modelos disponíveis
        Return list of available models
        """
        return list(self.models.values())

    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica saúde do provedor
        Check provider health
        """
        return {
            "provider": self.name,
            "status": "healthy",
            "models_count": len(self.models),
        }

    def get_model_info(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtém informações do modelo
        Get model information
        """
        return self.models.get(model_name)

    def estimate_cost(
        self, input_tokens: int, output_tokens: int, model: str = None
    ) -> Dict[str, float]:
        """
        Estima custo da requisição
        Estimate request cost
        """
        return {
            "input_cost": 0.0,
            "output_cost": 0.0,
            "total_cost": 0.0,
            "currency": "USD",
        }


class ModelManager:
    """
    Gerenciador de múltiplos provedores de modelos
    Manager for multiple model providers
    """

    def __init__(self):
        self.providers: Dict[str, ModelProvider] = {}
        self.default_provider = None

    async def add_provider(self, name: str, provider: ModelProvider) -> bool:
        """
        Adiciona provedor
        Add provider
        """
        try:
            await provider.initialize()
            self.providers[name] = provider

            if self.default_provider is None:
                self.default_provider = name

            logger.info(f"Provedor {name} adicionado com sucesso")
            return True

        except Exception as e:
            logger.error(f"Erro ao adicionar provedor {name}: {str(e)}")
            return False

    def get_provider(self, name: str = None) -> Optional[ModelProvider]:
        """
        Obtém provedor
        Get provider
        """
        if name is None:
            name = self.default_provider

        return self.providers.get(name)

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        provider: str = None,
        model: str = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Gera resposta de chat usando provedor especificado
        Generate chat response using specified provider
        """
        provider_instance = self.get_provider(provider)
        if not provider_instance:
            raise ValueError(f"Provedor não encontrado: {provider}")

        return await provider_instance.chat_completion(messages, model, **kwargs)

    async def get_all_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtém todos os modelos de todos os provedores
        Get all models from all providers
        """
        all_models = {}

        for name, provider in self.providers.items():
            try:
                models = await provider.get_available_models()
                all_models[name] = models
            except Exception as e:
                logger.error(f"Erro ao obter modelos do provedor {name}: {str(e)}")
                all_models[name] = []

        return all_models

    async def health_check_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Verifica saúde de todos os provedores
        Check health of all providers
        """
        health_status = {}

        for name, provider in self.providers.items():
            try:
                health_status[name] = await provider.health_check()
            except Exception as e:
                health_status[name] = {
                    "provider": name,
                    "status": "unhealthy",
                    "error": str(e),
                }

        return health_status
