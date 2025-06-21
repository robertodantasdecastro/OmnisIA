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
                                        
      Production Deployment Script      
EOF
echo -e "${NC}"

log_info "🚀 OmnisIA Trainer Web - Script de Deploy em Produção"

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
DEPLOY_HOST=${DEPLOY_HOST:-"localhost"}
DEPLOY_USER=${DEPLOY_USER:-"omnisia"}
DEPLOY_PATH=${DEPLOY_PATH:-"/opt/omnisia"}
BACKUP_DIR=${BACKUP_DIR:-"/opt/omnisia/backups"}
ENVIRONMENT=${ENVIRONMENT:-"production"}

# Menu de opções de deploy
echo ""
log_info "📋 Escolha o método de deploy:"
echo "1. 🐳 Docker Compose (Recomendado)"
echo "2. 📦 Deploy Manual no Servidor"
echo "3. ⚙️  Systemd Services"
echo "4. 🔧 Configuração de Nginx"
echo "5. 💾 Backup antes do Deploy"
echo "6. 📊 Status dos Serviços"
echo ""

read -p "Escolha uma opção (1-6): " choice

case $choice in
    1)
        log_step "🐳 Executando deploy com Docker Compose..."
        
        # Verifica se Docker está instalado
        if ! command -v docker &> /dev/null; then
            log_error "Docker não encontrado! Instale o Docker primeiro."
            exit 1
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            log_error "Docker Compose não encontrado! Instale o Docker Compose primeiro."
            exit 1
        fi
        
        # Cria arquivo docker-compose.prod.yml se não existir
        if [[ ! -f "docker/docker-compose.prod.yml" ]]; then
            log_info "Criando docker-compose.prod.yml..."
            
            cat > docker/docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  backend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - API_HOST=0.0.0.0
      - API_PORT=8000
    volumes:
      - ../data:/app/data
      - ../logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ..
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://backend:8000
      - FRONTEND_HOST=0.0.0.0
      - FRONTEND_PORT=8501
    depends_on:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  data:
  logs:
EOF
        fi
        
        # Para serviços existentes
        log_info "Parando serviços existentes..."
        docker-compose -f docker/docker-compose.prod.yml down || true
        
        # Build e start
        log_info "Construindo e iniciando containers..."
        docker-compose -f docker/docker-compose.prod.yml up -d --build
        
        # Verifica status
        sleep 10
        docker-compose -f docker/docker-compose.prod.yml ps
        
        log_success "Deploy com Docker concluído!"
        log_info "🌐 Frontend: http://localhost:8501"
        log_info "📡 Backend: http://localhost:8000"
        ;;
        
    2)
        log_step "📦 Deploy manual no servidor..."
        
        # Verifica se o usuário existe
        if ! id "$DEPLOY_USER" &>/dev/null; then
            log_info "Criando usuário $DEPLOY_USER..."
            sudo useradd -m -s /bin/bash "$DEPLOY_USER"
            sudo usermod -aG sudo "$DEPLOY_USER"
        fi
        
        # Cria diretório de deploy
        log_info "Criando diretório de deploy: $DEPLOY_PATH"
        sudo mkdir -p "$DEPLOY_PATH"
        sudo chown -R "$DEPLOY_USER:$DEPLOY_USER" "$DEPLOY_PATH"
        
        # Copia arquivos
        log_info "Copiando arquivos para $DEPLOY_PATH..."
        sudo -u "$DEPLOY_USER" cp -r . "$DEPLOY_PATH/"
        
        # Instala dependências
        log_info "Instalando dependências no servidor..."
        cd "$DEPLOY_PATH"
        sudo -u "$DEPLOY_USER" bash -c "
            cd $DEPLOY_PATH
            python3 -m venv .venv
            source .venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
        "
        
        # Configura ambiente de produção
        if [[ ! -f "$DEPLOY_PATH/.env" ]]; then
            sudo -u "$DEPLOY_USER" cp "$DEPLOY_PATH/env.example" "$DEPLOY_PATH/.env"
            sudo -u "$DEPLOY_USER" sed -i "s/ENVIRONMENT=development/ENVIRONMENT=production/" "$DEPLOY_PATH/.env"
        fi
        
        # Inicializa banco de dados
        log_info "Inicializando banco de dados..."
        sudo -u "$DEPLOY_USER" bash -c "
            cd $DEPLOY_PATH
            source .venv/bin/activate
            ./scripts/init_database.sh
        "
        
        log_success "Deploy manual concluído em $DEPLOY_PATH"
        ;;
        
    3)
        log_step "⚙️ Configurando serviços Systemd..."
        
        # Cria serviço do backend
        log_info "Criando serviço omnisia-backend.service..."
        sudo tee /etc/systemd/system/omnisia-backend.service > /dev/null << EOF
[Unit]
Description=OmnisIA Trainer Web Backend
After=network.target

[Service]
Type=simple
User=$DEPLOY_USER
WorkingDirectory=$DEPLOY_PATH
Environment=PATH=$DEPLOY_PATH/.venv/bin
Environment=PYTHONPATH=$DEPLOY_PATH
ExecStart=$DEPLOY_PATH/.venv/bin/uvicorn backend.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

        # Cria serviço do frontend
        log_info "Criando serviço omnisia-frontend.service..."
        sudo tee /etc/systemd/system/omnisia-frontend.service > /dev/null << EOF
[Unit]
Description=OmnisIA Trainer Web Frontend
After=network.target omnisia-backend.service

[Service]
Type=simple
User=$DEPLOY_USER
WorkingDirectory=$DEPLOY_PATH
Environment=PATH=$DEPLOY_PATH/.venv/bin
ExecStart=$DEPLOY_PATH/.venv/bin/streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

        # Recarrega systemd e habilita serviços
        sudo systemctl daemon-reload
        sudo systemctl enable omnisia-backend
        sudo systemctl enable omnisia-frontend
        
        # Inicia serviços
        sudo systemctl start omnisia-backend
        sudo systemctl start omnisia-frontend
        
        # Status
        sudo systemctl status omnisia-backend --no-pager
        sudo systemctl status omnisia-frontend --no-pager
        
        log_success "Serviços Systemd configurados e iniciados!"
        ;;
        
    4)
        log_step "🔧 Configurando Nginx..."
        
        # Cria configuração do Nginx
        sudo tee /etc/nginx/sites-available/omnisia << 'EOF'
server {
    listen 80;
    server_name _;

    # Frontend (Streamlit)
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Arquivos estáticos
    location /static/ {
        alias /opt/omnisia/data/uploads/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

        # Habilita site
        sudo ln -sf /etc/nginx/sites-available/omnisia /etc/nginx/sites-enabled/
        
        # Remove site padrão
        sudo rm -f /etc/nginx/sites-enabled/default
        
        # Testa configuração
        sudo nginx -t
        
        # Recarrega Nginx
        sudo systemctl reload nginx
        
        log_success "Nginx configurado!"
        ;;
        
    5)
        log_step "💾 Criando backup antes do deploy..."
        
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BACKUP_FILE="omnisia_backup_${TIMESTAMP}.tar.gz"
        
        mkdir -p "$BACKUP_DIR"
        
        tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
            --exclude='.venv' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.git' \
            --exclude='backups' \
            .
        
        log_success "Backup criado: $BACKUP_DIR/$BACKUP_FILE"
        ls -lh "$BACKUP_DIR/$BACKUP_FILE"
        ;;
        
    6)
        log_step "📊 Verificando status dos serviços..."
        
        echo ""
        log_info "🐳 Docker Services:"
        if command -v docker &> /dev/null; then
            docker ps --filter "name=omnisia" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || echo "Nenhum container encontrado"
        else
            echo "Docker não instalado"
        fi
        
        echo ""
        log_info "⚙️ Systemd Services:"
        if systemctl is-active --quiet omnisia-backend; then
            echo "✅ omnisia-backend: Ativo"
        else
            echo "❌ omnisia-backend: Inativo"
        fi
        
        if systemctl is-active --quiet omnisia-frontend; then
            echo "✅ omnisia-frontend: Ativo"
        else
            echo "❌ omnisia-frontend: Inativo"
        fi
        
        echo ""
        log_info "🌐 Conectividade:"
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "✅ Backend: Online (http://localhost:8000)"
        else
            echo "❌ Backend: Offline"
        fi
        
        if curl -s http://localhost:8501 > /dev/null; then
            echo "✅ Frontend: Online (http://localhost:8501)"
        else
            echo "❌ Frontend: Offline"
        fi
        
        echo ""
        log_info "💾 Recursos do Sistema:"
        df -h /opt/omnisia 2>/dev/null || df -h .
        echo ""
        free -h
        ;;
        
    *)
        log_error "Opção inválida!"
        exit 1
        ;;
esac

echo ""
log_success "🎉 Deploy concluído!"

# Informações finais
echo ""
log_info "📋 Informações importantes:"
echo "• Frontend: http://localhost:8501"
echo "• Backend API: http://localhost:8000"
echo "• Documentação: http://localhost:8000/docs"
echo "• Logs: tail -f logs/omnisia.log"
echo ""
log_info "🔧 Comandos úteis:"
echo "• Status: ./scripts/deploy.sh (opção 6)"
echo "• Backup: ./scripts/deploy.sh (opção 5)"
echo "• Logs backend: sudo journalctl -u omnisia-backend -f"
echo "• Logs frontend: sudo journalctl -u omnisia-frontend -f" 