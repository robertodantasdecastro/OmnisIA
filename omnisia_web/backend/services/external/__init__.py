"""
Serviços Externos para APIs de Modelos
External Services for Model APIs

Suporte para múltiplas APIs de modelos:
- OpenAI GPT
- DeepSeek
- Anthropic Claude
- Google Gemini
- AWS Bedrock
- Modelos locais (DeepSeek R1, Llama, etc.)

Support for multiple model APIs:
- OpenAI GPT
- DeepSeek
- Anthropic Claude
- Google Gemini
- AWS Bedrock
- Local models (DeepSeek R1, Llama, etc.)
"""

from .base import ModelProvider
from .openai_api import OpenAIProvider
from .deepseek_api import DeepSeekProvider
from .anthropic_api import AnthropicProvider
from .google_api import GoogleProvider
from .aws_bedrock import BedrockProvider
from .local_models import LocalModelProvider
from .kaggle_api import KaggleProvider

__all__ = [
    "ModelProvider",
    "OpenAIProvider",
    "DeepSeekProvider",
    "AnthropicProvider",
    "GoogleProvider",
    "BedrockProvider",
    "LocalModelProvider",
    "KaggleProvider",
]
