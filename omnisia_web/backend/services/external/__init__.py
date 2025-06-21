"""
Serviços Externos para APIs de Modelos
External Services for Model APIs

Suporte planejado para múltiplas APIs de modelos:
- OpenAI GPT (planejado)
- DeepSeek (planejado)
- Anthropic Claude (planejado)
- Google Gemini (planejado)
- AWS Bedrock (planejado)
- Modelos locais (planejado)
- Kaggle API (planejado)

Support planned for multiple model APIs:
- OpenAI GPT (planned)
- DeepSeek (planned)
- Anthropic Claude (planned)
- Google Gemini (planned)
- AWS Bedrock (planned)
- Local models (planned)
- Kaggle API (planned)

Atualmente implementado:
- Classe base ModelProvider
"""

from .base import ModelProvider

# TODO: Implementar provedores específicos
# from .openai_api import OpenAIProvider
# from .deepseek_api import DeepSeekProvider
# from .anthropic_api import AnthropicProvider
# from .google_api import GoogleProvider
# from .aws_bedrock import BedrockProvider
# from .local_models import LocalModelProvider
# from .kaggle_api import KaggleProvider

__all__ = [
    "ModelProvider",
    # "OpenAIProvider",
    # "DeepSeekProvider",
    # "AnthropicProvider",
    # "GoogleProvider",
    # "BedrockProvider",
    # "LocalModelProvider",
    # "KaggleProvider",
]
