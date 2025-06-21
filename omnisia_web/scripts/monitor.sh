#!/bin/bash
set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Funções de log
log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${PURPLE}🔧 $1${NC}"; }
log_metric() { echo -e "${CYAN}📊 $1${NC}"; }

# Banner
echo -e "${BLUE}"
cat << "EOF"
  ___                  _     ___   _     
 / _ \ _ __ ___  _ __ (_)___| _ \ / \    
| | | | '_ ` _ \| '_ \| / __|   // _ \   
| |_| | | | | | | | | \__ \ |_|/ ___ \  
 \___/|_| |_| |_|_| |_|___/___/_/   \_\ 
                                        
        System Monitoring Script        
EOF
echo -e "${NC}"

# Carrega configurações
if [[ -f ".env" ]]; then
    source .env
fi

# Configurações padrão
MONITOR_INTERVAL=${MONITOR_INTERVAL:-5}
DATABASE_PATH="data/omnisia.db"

# Função para verificar serviços
check_services() {
    echo ""
    log_step "🔍 Status dos Serviços"
    
    # Backend
    if curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
        log_success "Backend API: Online (http://localhost:8000)"
        
        # Pega informações detalhadas da API
        api_info=$(curl -s http://localhost:8000/health 2>/dev/null)
        if [[ -n "$api_info" ]]; then
            echo "   $(echo "$api_info" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
        fi
    else
        log_error "Backend API: Offline"
    fi
    
    # Frontend
    if curl -s -f http://localhost:8501 > /dev/null 2>&1; then
        log_success "Frontend: Online (http://localhost:8501)"
    else
        log_error "Frontend: Offline"
    fi
    
    # Systemd services (se existirem)
    if systemctl is-active --quiet omnisia-backend 2>/dev/null; then
        log_success "Systemd Backend: Ativo"
    elif systemctl list-units --type=service | grep -q omnisia-backend 2>/dev/null; then
        log_error "Systemd Backend: Inativo"
    fi
    
    if systemctl is-active --quiet omnisia-frontend 2>/dev/null; then
        log_success "Systemd Frontend: Ativo"
    elif systemctl list-units --type=service | grep -q omnisia-frontend 2>/dev/null; then
        log_error "Systemd Frontend: Inativo"
    fi
    
    # Docker containers
    if command -v docker &> /dev/null; then
        containers=$(docker ps --filter "name=omnisia" --format "{{.Names}}" 2>/dev/null)
        if [[ -n "$containers" ]]; then
            log_success "Docker Containers:"
            docker ps --filter "name=omnisia" --format "   {{.Names}}: {{.Status}}" 2>/dev/null
        fi
    fi
}

# Função para métricas do sistema
show_system_metrics() {
    echo ""
    log_step "💻 Métricas do Sistema"
    
    # CPU
    if command -v top &> /dev/null; then
        cpu_usage=$(top -l 1 -s 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' 2>/dev/null || echo "N/A")
        log_metric "CPU: ${cpu_usage}%"
    fi
    
    # Memória
    if command -v free &> /dev/null; then
        mem_info=$(free -h | grep "Mem:")
        mem_used=$(echo "$mem_info" | awk '{print $3}')
        mem_total=$(echo "$mem_info" | awk '{print $2}')
        log_metric "Memória: $mem_used / $mem_total"
    elif command -v vm_stat &> /dev/null; then
        # macOS
        pages_free=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/\.//')
        pages_active=$(vm_stat | grep "Pages active" | awk '{print $3}' | sed 's/\.//')
        if [[ -n "$pages_free" && -n "$pages_active" ]]; then
            mem_free_mb=$((pages_free * 4096 / 1024 / 1024))
            mem_active_mb=$((pages_active * 4096 / 1024 / 1024))
            log_metric "Memória: ${mem_active_mb}MB usado, ${mem_free_mb}MB livre"
        fi
    fi
    
    # Disco
    disk_info=$(df -h . | tail -1)
    disk_used=$(echo "$disk_info" | awk '{print $3}')
    disk_total=$(echo "$disk_info" | awk '{print $2}')
    disk_percent=$(echo "$disk_info" | awk '{print $5}')
    log_metric "Disco: $disk_used / $disk_total ($disk_percent)"
    
    # Load average
    if command -v uptime &> /dev/null; then
        load_avg=$(uptime | awk -F'load average:' '{print $2}' | xargs)
        log_metric "Load Average: $load_avg"
    fi
    
    # Uptime
    if command -v uptime &> /dev/null; then
        system_uptime=$(uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}')
        log_metric "Uptime: $system_uptime"
    fi
}

# Função para métricas da aplicação
show_app_metrics() {
    echo ""
    log_step "📊 Métricas da Aplicação"
    
    # Verifica se o banco existe
    if [[ -f "$DATABASE_PATH" ]]; then
        # Arquivos processados hoje
        files_today=$(sqlite3 "$DATABASE_PATH" "SELECT COUNT(*) FROM uploaded_files WHERE DATE(upload_date) = DATE('now');" 2>/dev/null || echo "0")
        log_metric "Arquivos enviados hoje: $files_today"
        
        # Total de arquivos
        total_files=$(sqlite3 "$DATABASE_PATH" "SELECT COUNT(*) FROM uploaded_files;" 2>/dev/null || echo "0")
        log_metric "Total de arquivos: $total_files"
        
        # Conversas de chat hoje
        chats_today=$(sqlite3 "$DATABASE_PATH" "SELECT COUNT(*) FROM chat_conversations WHERE DATE(created_at) = DATE('now');" 2>/dev/null || echo "0")
        log_metric "Conversas de chat hoje: $chats_today"
        
        # Treinamentos ativos
        active_trainings=$(sqlite3 "$DATABASE_PATH" "SELECT COUNT(*) FROM lora_trainings WHERE status = 'running';" 2>/dev/null || echo "0")
        log_metric "Treinamentos ativos: $active_trainings"
        
        # Tamanho do banco
        if [[ -f "$DATABASE_PATH" ]]; then
            db_size=$(du -h "$DATABASE_PATH" | cut -f1)
            log_metric "Tamanho do banco: $db_size"
        fi
    else
        log_warning "Banco de dados não encontrado"
    fi
    
    # Diretórios de dados
    if [[ -d "data/uploads" ]]; then
        upload_count=$(find data/uploads -type f | wc -l | xargs)
        upload_size=$(du -sh data/uploads 2>/dev/null | cut -f1 || echo "0B")
        log_metric "Arquivos em uploads: $upload_count ($upload_size)"
    fi
    
    if [[ -d "logs" ]]; then
        log_size=$(du -sh logs 2>/dev/null | cut -f1 || echo "0B")
        log_metric "Tamanho dos logs: $log_size"
    fi
}

# Função para processos da aplicação
show_processes() {
    echo ""
    log_step "🔄 Processos da Aplicação"
    
    # Processos Python relacionados
    python_procs=$(ps aux | grep -E "(uvicorn|streamlit|python.*omnisia)" | grep -v grep | wc -l | xargs)
    if [[ "$python_procs" -gt 0 ]]; then
        log_metric "Processos Python ativos: $python_procs"
        ps aux | grep -E "(uvicorn|streamlit|python.*omnisia)" | grep -v grep | while read line; do
            pid=$(echo "$line" | awk '{print $2}')
            cpu=$(echo "$line" | awk '{print $3}')
            mem=$(echo "$line" | awk '{print $4}')
            cmd=$(echo "$line" | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}' | cut -c1-50)
            echo "   PID $pid: CPU ${cpu}%, MEM ${mem}% - $cmd"
        done
    else
        log_warning "Nenhum processo da aplicação encontrado"
    fi
}

# Função para logs recentes
show_recent_logs() {
    echo ""
    log_step "📋 Logs Recentes"
    
    # Backend logs
    if [[ -f "logs/backend.log" ]]; then
        log_info "Últimas 3 linhas do backend:"
        tail -3 logs/backend.log | while read line; do
            echo "   $line"
        done
    fi
    
    # Frontend logs
    if [[ -f "logs/frontend.log" ]]; then
        log_info "Últimas 3 linhas do frontend:"
        tail -3 logs/frontend.log | while read line; do
            echo "   $line"
        done
    fi
    
    # System logs (journalctl)
    if command -v journalctl &> /dev/null; then
        if systemctl list-units --type=service | grep -q omnisia 2>/dev/null; then
            log_info "Últimas mensagens do systemd:"
            journalctl -u omnisia-* --no-pager -n 3 --since "5 minutes ago" 2>/dev/null | tail -3 | while read line; do
                echo "   $line"
            done
        fi
    fi
}

# Função para alertas
check_alerts() {
    echo ""
    log_step "⚠️ Verificação de Alertas"
    
    alerts=0
    
    # Verifica se os serviços estão rodando
    if ! curl -s -f http://localhost:8000/health > /dev/null 2>&1; then
        log_error "ALERTA: Backend API não está respondendo"
        ((alerts++))
    fi
    
    if ! curl -s -f http://localhost:8501 > /dev/null 2>&1; then
        log_error "ALERTA: Frontend não está respondendo"
        ((alerts++))
    fi
    
    # Verifica espaço em disco
    disk_usage=$(df . | tail -1 | awk '{print $5}' | sed 's/%//')
    if [[ "$disk_usage" -gt 90 ]]; then
        log_error "ALERTA: Uso de disco acima de 90% ($disk_usage%)"
        ((alerts++))
    elif [[ "$disk_usage" -gt 80 ]]; then
        log_warning "AVISO: Uso de disco acima de 80% ($disk_usage%)"
    fi
    
    # Verifica logs de erro recentes
    if [[ -f "logs/backend.log" ]]; then
        recent_errors=$(grep -i "error\|exception\|failed" logs/backend.log | tail -5 | wc -l | xargs)
        if [[ "$recent_errors" -gt 0 ]]; then
            log_warning "AVISO: $recent_errors erros recentes no backend"
        fi
    fi
    
    # Verifica treinamentos travados
    if [[ -f "$DATABASE_PATH" ]]; then
        stuck_trainings=$(sqlite3 "$DATABASE_PATH" "SELECT COUNT(*) FROM lora_trainings WHERE status = 'running' AND started_at < datetime('now', '-2 hours');" 2>/dev/null || echo "0")
        if [[ "$stuck_trainings" -gt 0 ]]; then
            log_error "ALERTA: $stuck_trainings treinamentos podem estar travados"
            ((alerts++))
        fi
    fi
    
    if [[ "$alerts" -eq 0 ]]; then
        log_success "Nenhum alerta ativo"
    else
        log_error "Total de alertas: $alerts"
    fi
}

# Função para monitoramento contínuo
continuous_monitor() {
    log_info "🔄 Monitoramento contínuo iniciado (intervalo: ${MONITOR_INTERVAL}s)"
    log_info "Pressione Ctrl+C para parar"
    
    while true; do
        clear
        echo -e "${BLUE}$(date '+%Y-%m-%d %H:%M:%S') - OmnisIA Monitor${NC}"
        echo "=================================="
        
        check_services
        show_system_metrics
        show_app_metrics
        check_alerts
        
        echo ""
        echo "Próxima atualização em ${MONITOR_INTERVAL}s..."
        sleep "$MONITOR_INTERVAL"
    done
}

# Função para relatório completo
full_report() {
    log_step "📋 Relatório Completo do Sistema"
    
    check_services
    show_system_metrics
    show_app_metrics
    show_processes
    show_recent_logs
    check_alerts
    
    echo ""
    log_success "Relatório concluído em $(date)"
}

# Função para mostrar ajuda
show_help() {
    echo ""
    log_info "📋 Comandos disponíveis:"
    echo "  status     - Status rápido dos serviços"
    echo "  metrics    - Métricas do sistema e aplicação"
    echo "  processes  - Processos da aplicação"
    echo "  logs       - Logs recentes"
    echo "  alerts     - Verificação de alertas"
    echo "  report     - Relatório completo"
    echo "  watch      - Monitoramento contínuo"
    echo "  help       - Esta ajuda"
    echo ""
    echo "Uso: $0 <comando>"
    echo "Exemplo: $0 watch"
}

# Processa argumentos
case "${1:-status}" in
    status)
        check_services
        ;;
    metrics)
        show_system_metrics
        show_app_metrics
        ;;
    processes)
        show_processes
        ;;
    logs)
        show_recent_logs
        ;;
    alerts)
        check_alerts
        ;;
    report)
        full_report
        ;;
    watch|monitor)
        continuous_monitor
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