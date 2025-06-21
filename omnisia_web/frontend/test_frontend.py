#!/usr/bin/env python3
"""
Testes para o Frontend OmnisIA Trainer Web
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adicionar o diretório frontend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import format_file_size, get_file_icon, check_api_connection
from config import API_URL, SUPPORTED_FILE_TYPES


class TestUtils(unittest.TestCase):
    """Testes para as funções utilitárias"""

    def test_format_file_size(self):
        """Testa formatação de tamanho de arquivo"""
        self.assertEqual(format_file_size(0), "0B")
        self.assertEqual(format_file_size(1024), "1.0KB")
        self.assertEqual(format_file_size(1024 * 1024), "1.0MB")
        self.assertEqual(format_file_size(1024 * 1024 * 1024), "1.0GB")
        self.assertEqual(format_file_size(1500), "1.5KB")

    def test_get_file_icon(self):
        """Testa obtenção de ícones de arquivo"""
        self.assertEqual(get_file_icon(".pdf"), "📄")
        self.assertEqual(get_file_icon(".txt"), "📝")
        self.assertEqual(get_file_icon(".jpg"), "🖼️")
        self.assertEqual(get_file_icon(".mp3"), "🎵")
        self.assertEqual(get_file_icon(".mp4"), "🎬")
        self.assertEqual(get_file_icon(".unknown"), "📁")

    @patch("utils.requests.get")
    def test_check_api_connection_success(self, mock_get):
        """Testa verificação de conexão com API - sucesso"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = check_api_connection("http://localhost:8000")
        self.assertTrue(result)

    @patch("utils.requests.get")
    def test_check_api_connection_failure(self, mock_get):
        """Testa verificação de conexão com API - falha"""
        mock_get.side_effect = Exception("Connection error")

        result = check_api_connection("http://localhost:8000")
        self.assertFalse(result)


class TestConfig(unittest.TestCase):
    """Testes para as configurações"""

    def test_api_url(self):
        """Testa URL da API"""
        self.assertIsInstance(API_URL, str)
        self.assertIn("localhost", API_URL)

    def test_supported_file_types(self):
        """Testa tipos de arquivo suportados"""
        self.assertIsInstance(SUPPORTED_FILE_TYPES, dict)
        self.assertIn("pdf", SUPPORTED_FILE_TYPES)
        self.assertIn("txt", SUPPORTED_FILE_TYPES)
        self.assertIn("jpg", SUPPORTED_FILE_TYPES)
        self.assertIn("mp3", SUPPORTED_FILE_TYPES)
        self.assertIn("mp4", SUPPORTED_FILE_TYPES)


class TestIntegration(unittest.TestCase):
    """Testes de integração"""

    def test_config_consistency(self):
        """Testa consistência das configurações"""
        from config import SUPPORTED_FILE_TYPES, WHISPER_MODELS

        # Verifica se os tipos de arquivo têm ícones
        for file_type in SUPPORTED_FILE_TYPES:
            icon = get_file_icon(f".{file_type}")
            self.assertIsInstance(icon, str)
            self.assertNotEqual(icon, "📁")  # Não deve ser o ícone padrão

        # Verifica se os modelos Whisper são válidos
        valid_models = ["tiny", "base", "small", "medium", "large"]
        for model in WHISPER_MODELS:
            self.assertIn(model, valid_models)


def run_frontend_tests():
    """Executa todos os testes do frontend"""
    print("🧪 Executando testes do Frontend...")

    # Criar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adicionar testes
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Resumo
    print(f"\n📊 Resumo dos Testes:")
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"⚠️ Erros: {len(result.errors)}")

    if result.failures:
        print("\n❌ Falhas:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ Erros:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_frontend_tests()
    sys.exit(0 if success else 1)
