#!/usr/bin/env python3
"""
Teste do Frontend OmnisIA Trainer Web
Verifica se todas as importações e configurações estão corretas
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(str(Path(__file__).parent))


def test_imports():
    """Testa todas as importações"""
    try:
        print("🔍 Testando importações...")

        # Testa importações do config
        from config import (
            PAGE_TITLE,
            PAGE_ICON,
            VERSION,
            get_api_url,
            get_navigation_pages,
            is_debug_enabled,
        )

        print("✅ Config importado com sucesso")

        # Testa importações do utils
        from utils import (
            init_session_state,
            get_chat_history,
            check_api_health,
            format_file_size,
        )

        print("✅ Utils importado com sucesso")

        # Testa importações do components
        from components import setup_page_config, create_sidebar, create_dashboard

        print("✅ Components importado com sucesso")

        # Testa importação do app principal
        import app

        print("✅ App principal importado com sucesso")

        return True

    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False


def test_configuration():
    """Testa configurações"""
    try:
        print("\n🔧 Testando configurações...")

        from config import (
            VERSION,
            PAGE_TITLE,
            get_api_url,
            get_navigation_pages,
            SUPPORTED_FILE_TYPES,
        )

        print(f"📊 Versão: {VERSION}")
        print(f"📱 Título: {PAGE_TITLE}")
        print(f"🌐 API URL: {get_api_url()}")
        print(f"📄 Páginas: {len(get_navigation_pages())}")
        print(f"📁 Tipos de arquivo: {len(SUPPORTED_FILE_TYPES)}")

        # Verifica se as páginas estão configuradas
        pages = get_navigation_pages()
        expected_pages = [
            "🏠 Dashboard",
            "📤 Upload",
            "🔧 Pré-processamento",
            "🎯 Treinamento",
            "💬 Chat",
            "📊 Status",
        ]

        for page in expected_pages:
            if page not in pages:
                print(f"❌ Página faltando: {page}")
                return False

        print("✅ Todas as configurações estão corretas")
        return True

    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False


def test_utilities():
    """Testa utilitários"""
    try:
        print("\n🛠️ Testando utilitários...")

        from utils import format_file_size, format_confidence, format_duration

        # Testa formatação
        assert format_file_size(1024) == "1.0KB"
        assert format_file_size(1048576) == "1.0MB"
        print("✅ Formatação de tamanho OK")

        # Testa formatação de confiança
        confidence_str = format_confidence(0.85)
        assert "Alta" in confidence_str
        print("✅ Formatação de confiança OK")

        # Testa formatação de duração
        duration_str = format_duration(65)
        assert "1m" in duration_str
        print("✅ Formatação de duração OK")

        print("✅ Todos os utilitários funcionando")
        return True

    except Exception as e:
        print(f"❌ Erro nos utilitários: {e}")
        return False


def test_session_state():
    """Testa estado da sessão"""
    try:
        print("\n💾 Testando estado da sessão...")

        from utils import init_session_state
        from config import SESSION_KEYS

        # Verifica se as chaves de sessão estão definidas
        required_keys = [
            "chat_history",
            "uploaded_files",
            "context_texts",
            "user_preferences",
            "cached_models",
        ]

        for key in required_keys:
            if key not in SESSION_KEYS:
                print(f"❌ Chave de sessão faltando: {key}")
                return False

        print("✅ Estado da sessão configurado corretamente")
        return True

    except Exception as e:
        print(f"❌ Erro no estado da sessão: {e}")
        return False


def main():
    """Função principal do teste"""
    print("🧪 TESTE DO FRONTEND OMNISIA TRAINER WEB")
    print("=" * 50)

    tests = [
        ("Importações", test_imports),
        ("Configurações", test_configuration),
        ("Utilitários", test_utilities),
        ("Estado da Sessão", test_session_state),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Executando teste: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ Teste falhou: {test_name}")

    print("\n" + "=" * 50)
    print(f"📊 RESULTADO: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Frontend está pronto para uso!")
        return True
    else:
        print("❌ Alguns testes falharam")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
