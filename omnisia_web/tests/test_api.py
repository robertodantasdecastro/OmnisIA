#!/usr/bin/env python3
"""
Testes básicos para a API OmnisIA Trainer Web
"""

import pytest
import requests
import json
from pathlib import Path
import tempfile
import os

# Configuração
API_URL = "http://localhost:8000"


class TestAPI:
    """Testes da API"""

    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        try:
            response = requests.get(f"{API_URL}/")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            print("✅ Endpoint raiz funcionando")
        except requests.exceptions.ConnectionError:
            pytest.skip("API não está rodando")

    def test_upload_endpoint(self):
        """Testa endpoint de upload"""
        try:
            # Cria arquivo temporário
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False
            ) as f:
                f.write("Teste de upload")
                temp_file = f.name

            try:
                with open(temp_file, "rb") as f:
                    files = {"file": ("test.txt", f, "text/plain")}
                    response = requests.post(f"{API_URL}/upload/", files=files)

                assert response.status_code == 200
                data = response.json()
                assert "filename" in data
                assert "size" in data
                print("✅ Upload funcionando")

            finally:
                os.unlink(temp_file)

        except requests.exceptions.ConnectionError:
            pytest.skip("API não está rodando")

    def test_chat_endpoint(self):
        """Testa endpoint de chat"""
        try:
            # Adiciona contexto
            context = ["Este é um teste do sistema OmnisIA."]
            response = requests.post(f"{API_URL}/chat/add-context", json=context)
            assert response.status_code == 200

            # Testa chat
            chat_data = {"text": "Teste de chat"}
            response = requests.post(f"{API_URL}/chat/", json=chat_data)
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            print("✅ Chat funcionando")

        except requests.exceptions.ConnectionError:
            pytest.skip("API não está rodando")

    def test_models_endpoint(self):
        """Testa endpoint de modelos"""
        try:
            response = requests.get(f"{API_URL}/train/models")
            assert response.status_code == 200
            data = response.json()
            assert "models" in data
            assert len(data["models"]) > 0
            print("✅ Listagem de modelos funcionando")

        except requests.exceptions.ConnectionError:
            pytest.skip("API não está rodando")

    def test_context_info_endpoint(self):
        """Testa endpoint de informações do contexto"""
        try:
            response = requests.get(f"{API_URL}/chat/context-info")
            assert response.status_code == 200
            data = response.json()
            assert "total_texts" in data
            assert "index_initialized" in data
            print("✅ Informações do contexto funcionando")

        except requests.exceptions.ConnectionError:
            pytest.skip("API não está rodando")


def test_validation():
    """Testa validações da API"""
    try:
        # Testa upload de arquivo inválido
        response = requests.post(f"{API_URL}/upload/", files={})
        assert response.status_code == 422  # Validation error

        # Testa chat com texto vazio
        response = requests.post(f"{API_URL}/chat/", json={"text": ""})
        assert response.status_code == 422  # Validation error

        print("✅ Validações funcionando")

    except requests.exceptions.ConnectionError:
        pytest.skip("API não está rodando")


if __name__ == "__main__":
    # Executa testes básicos
    print("🧪 Executando testes da API...")

    test_api = TestAPI()
    test_api.test_root_endpoint()
    test_api.test_upload_endpoint()
    test_api.test_chat_endpoint()
    test_api.test_models_endpoint()
    test_api.test_context_info_endpoint()
    test_validation()

    print("✅ Todos os testes passaram!")
