#!/bin/bash
set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ___                  _     ___   _     
 / _ \ _ __ ___  _ __ (_)___| _ \ / \    
| | | | '_ ` _ \| '_ \| / __|   // _ \   
| |_| | | | | | | | | \__ \ |_|/ ___ \  
 \___/|_| |_| |_|_| |_|___/___/_/   \_\ 
                                        
    Database Initialization Script      
EOF
echo -e "${NC}"

log_info "🗄️ Inicializando banco de dados do OmnisIA Trainer Web..."

# Verifica se está no diretório correto
if [[ ! -f "env.example" ]] || [[ ! -f "requirements.txt" ]]; then
    log_error "Execute este script a partir do diretório raiz do projeto!"
    exit 1
fi

# Carrega variáveis de ambiente
if [[ -f ".env" ]]; then
    source .env
    log_info "Arquivo .env carregado"
else
    log_warning "Arquivo .env não encontrado, usando configurações padrão"
fi

# Configurações padrão
DATABASE_URL=${DATABASE_URL:-"sqlite:///./data/omnisia.db"}
DATABASE_TYPE=$(echo "$DATABASE_URL" | cut -d':' -f1)

log_info "Tipo de banco: $DATABASE_TYPE"
log_info "URL do banco: $DATABASE_URL"

# Ativa ambiente virtual se existir
if [[ -d ".venv" ]]; then
    source .venv/bin/activate
    log_info "Ambiente virtual ativado"
fi

# Cria diretório para banco de dados
mkdir -p data/
mkdir -p data/models/
mkdir -p data/uploads/
mkdir -p data/datasets/

# Cria script Python para inicialização do banco
cat > scripts/db_init.py << 'EOF'
#!/usr/bin/env python3
"""
Script de inicialização do banco de dados OmnisIA
"""

import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime
import json

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

def init_sqlite_database():
    """Inicializa banco SQLite com tabelas básicas"""
    db_path = Path("data/omnisia.db")
    
    print(f"🗄️ Criando banco SQLite: {db_path}")
    
    # Cria conexão
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Tabela de usuários (futuro)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de arquivos enviados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS uploaded_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename VARCHAR(255) NOT NULL,
            original_filename VARCHAR(255) NOT NULL,
            file_path VARCHAR(500) NOT NULL,
            file_size INTEGER NOT NULL,
            file_type VARCHAR(50) NOT NULL,
            mime_type VARCHAR(100),
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed BOOLEAN DEFAULT 0,
            user_id INTEGER,
            metadata TEXT,  -- JSON
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
        
        # Tabela de processamentos OCR
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ocr_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            extracted_text TEXT,
            language VARCHAR(10),
            confidence REAL,
            processing_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES uploaded_files (id)
        )
        """)
        
        # Tabela de transcrições de áudio/vídeo
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transcriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            transcribed_text TEXT,
            language VARCHAR(10),
            model_used VARCHAR(50),
            confidence REAL,
            duration REAL,
            processing_time REAL,
            segments TEXT,  -- JSON com timestamps
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES uploaded_files (id)
        )
        """)
        
        # Tabela de treinamentos LoRA
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lora_trainings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name VARCHAR(100) NOT NULL,
            dataset_path VARCHAR(500) NOT NULL,
            output_dir VARCHAR(500) NOT NULL,
            config TEXT,  -- JSON com configuração LoRA
            status VARCHAR(20) DEFAULT 'pending',  -- pending, running, completed, failed
            progress REAL DEFAULT 0.0,
            loss REAL,
            epochs_completed INTEGER DEFAULT 0,
            total_epochs INTEGER NOT NULL,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error_message TEXT
        )
        """)
        
        # Tabela de embeddings/contexto
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text_content TEXT NOT NULL,
            embedding_vector BLOB,  -- Vetor serializado
            model_used VARCHAR(100),
            source_file_id INTEGER,
            chunk_index INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_file_id) REFERENCES uploaded_files (id)
        )
        """)
        
        # Tabela de conversas de chat
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id VARCHAR(100) NOT NULL,
            user_message TEXT NOT NULL,
            assistant_response TEXT NOT NULL,
            confidence REAL,
            context_used TEXT,  -- JSON com contexto usado
            sources TEXT,  -- JSON com fontes
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de configurações do sistema
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_key VARCHAR(100) UNIQUE NOT NULL,
            config_value TEXT,
            config_type VARCHAR(20) DEFAULT 'string',  -- string, integer, float, boolean, json
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de logs do sistema
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level VARCHAR(10) NOT NULL,  -- DEBUG, INFO, WARNING, ERROR, CRITICAL
            message TEXT NOT NULL,
            module VARCHAR(100),
            function VARCHAR(100),
            line_number INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            extra_data TEXT  -- JSON
        )
        """)
        
        # Índices para performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_files_type ON uploaded_files(file_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_files_date ON uploaded_files(upload_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_conversations(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_date ON chat_conversations(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trainings_status ON lora_trainings(status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_level ON system_logs(level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON system_logs(timestamp)")
        
        print("✅ Tabelas criadas com sucesso")
        
        # Insere configurações padrão
        default_configs = [
            ('app_version', '1.0.0', 'string', 'Versão da aplicação'),
            ('max_file_size_mb', '100', 'integer', 'Tamanho máximo de arquivo em MB'),
            ('default_whisper_model', 'base', 'string', 'Modelo Whisper padrão'),
            ('default_embedding_model', 'all-MiniLM-L6-v2', 'string', 'Modelo de embedding padrão'),
            ('enable_chat_history', 'true', 'boolean', 'Habilitar histórico de chat'),
            ('max_chat_history', '50', 'integer', 'Máximo de mensagens no histórico'),
            ('enable_file_processing', 'true', 'boolean', 'Habilitar processamento de arquivos'),
            ('enable_training', 'true', 'boolean', 'Habilitar treinamento LoRA'),
            ('auto_cleanup_days', '30', 'integer', 'Dias para limpeza automática de arquivos'),
            ('supported_file_types', '["pdf", "txt", "jpg", "png", "mp3", "wav", "mp4"]', 'json', 'Tipos de arquivo suportados')
        ]
        
        for key, value, type_, desc in default_configs:
            cursor.execute("""
            INSERT OR IGNORE INTO system_config (config_key, config_value, config_type, description)
            VALUES (?, ?, ?, ?)
            """, (key, value, type_, desc))
        
        print("✅ Configurações padrão inseridas")
        
        # Dados de exemplo para desenvolvimento
        if os.getenv('DEVELOPMENT_MODE', 'false').lower() == 'true':
            print("🔧 Inserindo dados de exemplo (modo desenvolvimento)...")
            
            # Exemplo de arquivo processado
            cursor.execute("""
            INSERT OR IGNORE INTO uploaded_files 
            (filename, original_filename, file_path, file_size, file_type, mime_type, processed, metadata)
            VALUES 
            ('example_doc.pdf', 'Documento Exemplo.pdf', 'data/uploads/example_doc.pdf', 
             1024000, 'pdf', 'application/pdf', 1, '{"pages": 5, "language": "pt"}')
            """)
            
            # Exemplo de resultado OCR
            cursor.execute("""
            INSERT OR IGNORE INTO ocr_results 
            (file_id, extracted_text, language, confidence, processing_time)
            VALUES 
            (1, 'Este é um texto de exemplo extraído de um documento PDF usando OCR.', 
             'por', 0.95, 2.5)
            """)
            
            # Exemplo de conversa
            cursor.execute("""
            INSERT OR IGNORE INTO chat_conversations 
            (session_id, user_message, assistant_response, confidence, context_used)
            VALUES 
            ('demo_session', 'O que é processamento de linguagem natural?',
             'Processamento de linguagem natural (PLN) é uma área da inteligência artificial que se concentra na interação entre computadores e linguagem humana.',
             0.9, '["exemplo de contexto"]')
            """)
            
            print("✅ Dados de exemplo inseridos")
        
        # Commit das mudanças
        conn.commit()
        print("✅ Banco de dados inicializado com sucesso!")
        
        # Estatísticas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📊 {len(tables)} tabelas criadas: {', '.join([t[0] for t in tables])}")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar banco: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def create_database_backup():
    """Cria backup do banco atual se existir"""
    db_path = Path("data/omnisia.db")
    if db_path.exists():
        backup_path = Path(f"data/omnisia_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"💾 Backup criado: {backup_path}")

def main():
    print("🗄️ Inicializando banco de dados OmnisIA...")
    
    # Cria backup se banco já existir
    if Path("data/omnisia.db").exists():
        create_database_backup()
    
    # Inicializa banco SQLite
    init_sqlite_database()
    
    print("🎉 Inicialização do banco concluída!")

if __name__ == "__main__":
    main()
EOF

# Executa script de inicialização
log_info "🐍 Executando script de inicialização..."
python3 scripts/db_init.py

# Cria script de gerenciamento do banco
log_info "📜 Criando scripts de gerenciamento..."

cat > scripts/db_manage.sh << 'EOF'
#!/bin/bash

DB_PATH="data/omnisia.db"

case "$1" in
    backup)
        BACKUP_FILE="data/omnisia_backup_$(date +%Y%m%d_%H%M%S).db"
        cp "$DB_PATH" "$BACKUP_FILE"
        echo "✅ Backup criado: $BACKUP_FILE"
        ;;
    
    restore)
        if [[ -z "$2" ]]; then
            echo "❌ Uso: $0 restore <arquivo_backup>"
            exit 1
        fi
        if [[ ! -f "$2" ]]; then
            echo "❌ Arquivo de backup não encontrado: $2"
            exit 1
        fi
        cp "$2" "$DB_PATH"
        echo "✅ Banco restaurado de: $2"
        ;;
    
    stats)
        echo "📊 Estatísticas do Banco de Dados"
        echo "================================="
        sqlite3 "$DB_PATH" << 'SQL'
.headers on
.mode column

SELECT 'Arquivos enviados' as Tabela, COUNT(*) as Total FROM uploaded_files
UNION ALL
SELECT 'Resultados OCR', COUNT(*) FROM ocr_results
UNION ALL
SELECT 'Transcrições', COUNT(*) FROM transcriptions
UNION ALL
SELECT 'Treinamentos LoRA', COUNT(*) FROM lora_trainings
UNION ALL
SELECT 'Embeddings', COUNT(*) FROM embeddings
UNION ALL
SELECT 'Conversas de chat', COUNT(*) FROM chat_conversations
UNION ALL
SELECT 'Configurações', COUNT(*) FROM system_config
UNION ALL
SELECT 'Logs do sistema', COUNT(*) FROM system_logs;
SQL
        ;;
    
    clean)
        echo "🧹 Limpando dados antigos..."
        sqlite3 "$DB_PATH" << 'SQL'
-- Remove logs antigos (mais de 30 dias)
DELETE FROM system_logs WHERE timestamp < datetime('now', '-30 days');

-- Remove conversas antigas (mais de 90 dias)
DELETE FROM chat_conversations WHERE created_at < datetime('now', '-90 days');

-- Vacuum para liberar espaço
VACUUM;
SQL
        echo "✅ Limpeza concluída"
        ;;
    
    shell)
        echo "🐚 Abrindo shell SQLite..."
        sqlite3 "$DB_PATH"
        ;;
    
    schema)
        echo "📋 Schema do Banco de Dados"
        echo "=========================="
        sqlite3 "$DB_PATH" ".schema"
        ;;
    
    reset)
        echo "⚠️  ATENÇÃO: Isso irá apagar todos os dados!"
        read -p "Tem certeza? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f "$DB_PATH"
            echo "✅ Banco de dados removido"
            echo "Execute './scripts/init_database.sh' para recriar"
        else
            echo "Operação cancelada"
        fi
        ;;
    
    *)
        echo "🗄️ Gerenciador do Banco de Dados OmnisIA"
        echo "========================================"
        echo "Uso: $0 {backup|restore|stats|clean|shell|schema|reset}"
        echo ""
        echo "Comandos:"
        echo "  backup          - Cria backup do banco"
        echo "  restore <file>  - Restaura banco do backup"
        echo "  stats           - Mostra estatísticas"
        echo "  clean           - Remove dados antigos"
        echo "  shell           - Abre shell SQLite"
        echo "  schema          - Mostra schema das tabelas"
        echo "  reset           - Remove banco (cuidado!)"
        echo ""
        echo "Banco atual: $DB_PATH"
        if [[ -f "$DB_PATH" ]]; then
            SIZE=$(du -h "$DB_PATH" | cut -f1)
            echo "Tamanho: $SIZE"
        else
            echo "Status: Não existe"
        fi
        ;;
esac
EOF

chmod +x scripts/db_manage.sh

# Remove script temporário
rm -f scripts/db_init.py

# Resumo final
echo ""
log_success "🎉 Inicialização do banco de dados concluída!"
echo ""
echo -e "${BLUE}📋 Informações:${NC}"
echo "• Tipo: $DATABASE_TYPE"
echo "• Localização: $DATABASE_URL"
echo "• Arquivo: data/omnisia.db"

if [[ -f "data/omnisia.db" ]]; then
    SIZE=$(du -h data/omnisia.db | cut -f1)
    echo "• Tamanho: $SIZE"
fi

echo ""
echo -e "${BLUE}🔧 Comandos úteis:${NC}"
echo "• Estatísticas: ./scripts/db_manage.sh stats"
echo "• Backup: ./scripts/db_manage.sh backup"
echo "• Shell SQL: ./scripts/db_manage.sh shell"
echo "• Limpeza: ./scripts/db_manage.sh clean"
echo "• Schema: ./scripts/db_manage.sh schema"

log_success "Banco de dados pronto para uso! 🗄️" 