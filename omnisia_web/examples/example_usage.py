#!/usr/bin/env python3
"""
Exemplo de uso da API OmnisIA Trainer Web
"""

import requests
import json
from pathlib import Path

# Configuração
API_URL = "http://localhost:8000"


def test_upload():
    """Testa upload de arquivo"""
    print("📤 Testando upload...")

    # Cria um arquivo de teste
    test_file = Path("test.txt")
    test_file.write_text("Este é um arquivo de teste para o OmnisIA Trainer Web.")

    try:
        with open(test_file, "rb") as f:
            files = {"file": ("test.txt", f, "text/plain")}
            response = requests.post(f"{API_URL}/upload/", files=files)

        if response.status_code == 200:
            print("✅ Upload bem-sucedido!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Erro no upload: {response.text}")

    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        # Remove arquivo de teste
        test_file.unlink(missing_ok=True)


def test_chat():
    """Testa funcionalidade de chat"""
    print("\n💬 Testando chat...")

    # Adiciona contexto
    context_texts = [
        "OmnisIA é um sistema de inteligência artificial multimodal.",
        "O sistema pode processar texto, áudio, vídeo e imagens.",
        "O treinamento usa técnicas de LoRA para fine-tuning eficiente.",
    ]

    try:
        # Adiciona contexto
        response = requests.post(f"{API_URL}/chat/add-context", json=context_texts)
        if response.status_code == 200:
            print("✅ Contexto adicionado!")
            print(json.dumps(response.json(), indent=2))

        # Testa chat
        chat_data = {"text": "O que é o OmnisIA?"}
        response = requests.post(f"{API_URL}/chat/", json=chat_data)

        if response.status_code == 200:
            print("✅ Chat funcionando!")
            result = response.json()
            print(f"Resposta: {result['response']}")
            print(f"Confiança: {result['confidence']}")
        else:
            print(f"❌ Erro no chat: {response.text}")

    except Exception as e:
        print(f"❌ Erro: {e}")


def test_models():
    """Testa listagem de modelos"""
    print("\n🎯 Testando listagem de modelos...")

    try:
        response = requests.get(f"{API_URL}/train/models")
        if response.status_code == 200:
            print("✅ Modelos listados!")
            models = response.json()["models"]
            for model in models:
                print(f"  - {model['name']}: {model['description']}")
        else:
            print(f"❌ Erro ao listar modelos: {response.text}")

    except Exception as e:
        print(f"❌ Erro: {e}")


def test_status():
    """Testa status da API"""
    print("\n📊 Testando status...")

    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            print("✅ API online!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ API com erro: {response.text}")

    except Exception as e:
        print(f"❌ API offline: {e}")


def main():
    """Função principal"""
    print("🤖 Testando OmnisIA Trainer Web API")
    print("=" * 50)

    # Testa status primeiro
    test_status()

    # Testa outras funcionalidades
    test_upload()
    test_chat()
    test_models()

    print("\n" + "=" * 50)
    print("✅ Testes concluídos!")


if __name__ == "__main__":
    main()
