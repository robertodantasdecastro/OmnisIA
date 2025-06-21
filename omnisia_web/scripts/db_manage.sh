#!/bin/bash
set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Funções de log
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${PURPLE}🔧 $1${NC}"; }

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ___                  _     ___   _     
 / _ \ _ __ ___  _ __ (_)___| _ \ / \    
| | | | '_ ` _ \| '_ \| / __|   // _ \   
| |_| | | | | | | | | \__ \ |_|/ ___ \  
 \___/|_| |_| |_|_| |_|___/___/_/   \_\ 
                                        
     Database Management Script         
EOF
echo -e "${NC}"

# Verifica se está no diretório correto
if [[ ! -f "env.example" ]] || [[ ! -f "requirements.txt" ]]; then
    log_error "Execute este script a partir do diretório raiz do projeto!"
    exit 1
fi

# Carrega configurações
if [[ -f ".env" ]]; then
    source .env
    log_info "Arquivo .env carregado"
else
    log_warning "Arquivo .env não encontrado, usando configurações padrão"
fi

# Configurações padrão
DATABASE_URL=${DATABASE_URL:-"sqlite:///./data/omnisia.db"}
DATABASE_PATH="data/omnisia.db"
BACKUP_DIR=${BACKUP_DIR:-"backups"}

# Função para mostrar ajuda
show_help() {
    echo ""
    log_info "📋 Comandos disponíveis:"
    echo "  stats     - Estatísticas do banco de dados"
    echo "  backup    - Criar backup do banco"
    echo "  restore   - Restaurar backup"
    echo "  clean     - Limpeza de dados antigos"
    echo "  shell     - Abrir shell SQL interativo"
    echo "  schema    - Mostrar schema das tabelas"
    echo "  size      - Tamanho do banco de dados"
    echo "  vacuum    - Otimizar banco (VACUUM)"
    echo "  export    - Exportar dados para CSV"
    echo "  import    - Importar dados de CSV"
    echo ""
    echo "Uso: $0 <comando>"
}

# Verifica se o banco existe
check_database() {
    if [[ ! -f "$DATABASE_PATH" ]]; then
        log_error "Banco de dados não encontrado: $DATABASE_PATH"
        log_info "Execute primeiro: ./scripts/init_database.sh"
        exit 1
    fi
}

# Função para estatísticas
show_stats() {
    log_step "📊 Estatísticas do Banco de Dados"
    check_database
    
    sqlite3 "$DATABASE_PATH" << 'EOF'
.headers on
.mode column

SELECT 'Total de Tabelas' as Métrica, COUNT(*) as Valor 
FROM sqlite_master WHERE type='table';

SELECT 'Arquivos Enviados' as Métrica, COUNT(*) as Valor 
FROM uploaded_files;

SELECT 'Resultados OCR' as Métrica, COUNT(*) as Valor 
FROM ocr_results;

SELECT 'Transcrições' as Métrica, COUNT(*) as Valor 
FROM transcriptions;

SELECT 'Treinamentos LoRA' as Métrica, COUNT(*) as Valor 
FROM lora_trainings;

SELECT 'Embeddings' as Métrica, COUNT(*) as Valor 
FROM embeddings;

SELECT 'Conversas de Chat' as Métrica, COUNT(*) as Valor 
FROM chat_conversations;

SELECT 'Logs do Sistema' as Métrica, COUNT(*) as Valor 
FROM system_logs;

-- Estatísticas por tipo de arquivo
SELECT 'Arquivos por Tipo:' as '--- Detalhes ---', '' as '';
SELECT file_type as Tipo, COUNT(*) as Quantidade 
FROM uploaded_files 
GROUP BY file_type 
ORDER BY Quantidade DESC;

-- Status dos treinamentos
SELECT 'Status dos Treinamentos:' as '--- Detalhes ---', '' as '';
SELECT status as Status, COUNT(*) as Quantidade 
FROM lora_trainings 
GROUP BY status;

-- Atividade recente
SELECT 'Uploads Recentes (últimos 7 dias):' as '--- Detalhes ---', '' as '';
SELECT DATE(upload_date) as Data, COUNT(*) as Uploads 
FROM uploaded_files 
WHERE upload_date >= datetime('now', '-7 days') 
GROUP BY DATE(upload_date) 
ORDER BY Data DESC;
EOF
}

# Função para backup
create_backup() {
    log_step "💾 Criando backup do banco de dados"
    check_database
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/omnisia_db_backup_$TIMESTAMP.sql"
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup SQL
    sqlite3 "$DATABASE_PATH" .dump > "$BACKUP_FILE"
    
    # Comprime o backup
    gzip "$BACKUP_FILE"
    BACKUP_FILE="$BACKUP_FILE.gz"
    
    log_success "Backup criado: $BACKUP_FILE"
    ls -lh "$BACKUP_FILE"
    
    # Lista backups existentes
    echo ""
    log_info "📋 Backups existentes:"
    ls -lht "$BACKUP_DIR"/omnisia_db_backup_*.sql.gz 2>/dev/null | head -10 || echo "Nenhum backup encontrado"
}

# Função para restaurar backup
restore_backup() {
    log_step "🔄 Restaurando backup do banco de dados"
    
    echo ""
    log_info "📋 Backups disponíveis:"
    ls -lht "$BACKUP_DIR"/omnisia_db_backup_*.sql.gz 2>/dev/null | head -10 || {
        log_error "Nenhum backup encontrado em $BACKUP_DIR"
        exit 1
    }
    
    echo ""
    read -p "Digite o nome do arquivo de backup: " backup_file
    
    if [[ ! -f "$backup_file" ]]; then
        log_error "Arquivo de backup não encontrado: $backup_file"
        exit 1
    fi
    
    # Confirma a restauração
    log_warning "⚠️ Esta operação irá SUBSTITUIR o banco atual!"
    read -p "Tem certeza? (digite 'CONFIRMO' para continuar): " confirm
    
    if [[ "$confirm" != "CONFIRMO" ]]; then
        log_info "Operação cancelada"
        exit 0
    fi
    
    # Backup do banco atual
    if [[ -f "$DATABASE_PATH" ]]; then
        cp "$DATABASE_PATH" "$DATABASE_PATH.backup.$(date +%Y%m%d_%H%M%S)"
        log_info "Backup do banco atual criado"
    fi
    
    # Restaura o backup
    zcat "$backup_file" | sqlite3 "$DATABASE_PATH"
    
    log_success "Backup restaurado com sucesso!"
}

# Função para limpeza
clean_database() {
    log_step "🧹 Limpeza do banco de dados"
    check_database
    
    echo ""
    log_info "📋 Opções de limpeza:"
    echo "1. Logs antigos (> 30 dias)"
    echo "2. Arquivos processados antigos (> 90 dias)"
    echo "3. Conversas de chat antigas (> 60 dias)"
    echo "4. Treinamentos falhos antigos (> 30 dias)"
    echo "5. Limpeza completa (todas as opções)"
    echo ""
    
    read -p "Escolha uma opção (1-5): " clean_option
    
    case $clean_option in
        1)
            log_info "Removendo logs antigos..."
            sqlite3 "$DATABASE_PATH" "DELETE FROM system_logs WHERE created_at < datetime('now', '-30 days');"
            ;;
        2)
            log_info "Removendo arquivos processados antigos..."
            sqlite3 "$DATABASE_PATH" "DELETE FROM uploaded_files WHERE upload_date < datetime('now', '-90 days') AND processed = 1;"
            ;;
        3)
            log_info "Removendo conversas antigas..."
            sqlite3 "$DATABASE_PATH" "DELETE FROM chat_conversations WHERE created_at < datetime('now', '-60 days');"
            ;;
        4)
            log_info "Removendo treinamentos falhos antigos..."
            sqlite3 "$DATABASE_PATH" "DELETE FROM lora_trainings WHERE status = 'failed' AND created_at < datetime('now', '-30 days');"
            ;;
        5)
            log_info "Executando limpeza completa..."
            sqlite3 "$DATABASE_PATH" << 'EOF'
DELETE FROM system_logs WHERE created_at < datetime('now', '-30 days');
DELETE FROM uploaded_files WHERE upload_date < datetime('now', '-90 days') AND processed = 1;
DELETE FROM chat_conversations WHERE created_at < datetime('now', '-60 days');
DELETE FROM lora_trainings WHERE status = 'failed' AND created_at < datetime('now', '-30 days');
EOF
            ;;
        *)
            log_error "Opção inválida!"
            exit 1
            ;;
    esac
    
    # Otimiza o banco após limpeza
    sqlite3 "$DATABASE_PATH" "VACUUM;"
    
    log_success "Limpeza concluída!"
}

# Função para shell SQL
sql_shell() {
    log_step "🐚 Abrindo shell SQL interativo"
    check_database
    
    log_info "Digite .help para ajuda, .quit para sair"
    sqlite3 "$DATABASE_PATH"
}

# Função para mostrar schema
show_schema() {
    log_step "🏗️ Schema das tabelas"
    check_database
    
    sqlite3 "$DATABASE_PATH" << 'EOF'
.headers on
.mode column

SELECT name as Tabela, sql as Definição 
FROM sqlite_master 
WHERE type='table' 
ORDER BY name;

.separator " | "
SELECT '--- Índices ---' as '', '';
SELECT name as Índice, tbl_name as Tabela, sql as Definição 
FROM sqlite_master 
WHERE type='index' AND name NOT LIKE 'sqlite_%'
ORDER BY tbl_name, name;
EOF
}

# Função para mostrar tamanho
show_size() {
    log_step "📏 Tamanho do banco de dados"
    check_database
    
    # Tamanho do arquivo
    size_bytes=$(stat -f%z "$DATABASE_PATH" 2>/dev/null || stat -c%s "$DATABASE_PATH" 2>/dev/null)
    size_mb=$(echo "scale=2; $size_bytes / 1024 / 1024" | bc -l 2>/dev/null || echo "N/A")
    
    echo "Arquivo: $DATABASE_PATH"
    echo "Tamanho: $size_bytes bytes ($size_mb MB)"
    
    echo ""
    log_info "📊 Estatísticas detalhadas:"
    sqlite3 "$DATABASE_PATH" << 'EOF'
.headers on
.mode column

-- Páginas do banco
PRAGMA page_count;
PRAGMA page_size;
PRAGMA freelist_count;

-- Tamanho por tabela (aproximado)
SELECT 'Tamanho por Tabela:' as '--- Detalhes ---', '' as '';
SELECT 
    name as Tabela,
    (SELECT COUNT(*) FROM pragma_table_info(name)) as Colunas,
    (SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name=name) as Índices
FROM sqlite_master 
WHERE type='table' 
ORDER BY name;
EOF
}

# Função para otimizar (VACUUM)
vacuum_database() {
    log_step "🔧 Otimizando banco de dados (VACUUM)"
    check_database
    
    log_info "Executando VACUUM..."
    sqlite3 "$DATABASE_PATH" "VACUUM;"
    
    log_success "Otimização concluída!"
    show_size
}

# Função para exportar dados
export_data() {
    log_step "📤 Exportando dados para CSV"
    check_database
    
    EXPORT_DIR="exports/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$EXPORT_DIR"
    
    # Lista de tabelas para exportar
    tables=("uploaded_files" "ocr_results" "transcriptions" "lora_trainings" "embeddings" "chat_conversations" "system_logs")
    
    for table in "${tables[@]}"; do
        log_info "Exportando tabela: $table"
        sqlite3 "$DATABASE_PATH" << EOF
.headers on
.mode csv
.output $EXPORT_DIR/$table.csv
SELECT * FROM $table;
.output stdout
EOF
    done
    
    log_success "Dados exportados para: $EXPORT_DIR"
    ls -la "$EXPORT_DIR"
}

# Função para importar dados
import_data() {
    log_step "📥 Importando dados de CSV"
    
    log_warning "⚠️ Esta funcionalidade deve ser usada com cuidado!"
    log_info "Certifique-se de que os arquivos CSV estão no formato correto"
    
    read -p "Digite o diretório com os arquivos CSV: " import_dir
    
    if [[ ! -d "$import_dir" ]]; then
        log_error "Diretório não encontrado: $import_dir"
        exit 1
    fi
    
    # Lista arquivos CSV disponíveis
    csv_files=$(find "$import_dir" -name "*.csv" -type f)
    
    if [[ -z "$csv_files" ]]; then
        log_error "Nenhum arquivo CSV encontrado em: $import_dir"
        exit 1
    fi
    
    log_info "📋 Arquivos CSV encontrados:"
    echo "$csv_files"
    
    read -p "Continuar com a importação? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Importação cancelada"
        exit 0
    fi
    
    # Importa cada arquivo
    for csv_file in $csv_files; do
        table_name=$(basename "$csv_file" .csv)
        log_info "Importando: $table_name"
        
        sqlite3 "$DATABASE_PATH" << EOF
.mode csv
.import $csv_file $table_name
EOF
    done
    
    log_success "Importação concluída!"
}

# Verifica argumentos
if [[ $# -eq 0 ]]; then
    show_help
    exit 1
fi

# Executa comando
case $1 in
    stats)
        show_stats
        ;;
    backup)
        create_backup
        ;;
    restore)
        restore_backup
        ;;
    clean)
        clean_database
        ;;
    shell)
        sql_shell
        ;;
    schema)
        show_schema
        ;;
    size)
        show_size
        ;;
    vacuum)
        vacuum_database
        ;;
    export)
        export_data
        ;;
    import)
        import_data
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Comando desconhecido: $1"
        show_help
        exit 1
        ;;
esac 