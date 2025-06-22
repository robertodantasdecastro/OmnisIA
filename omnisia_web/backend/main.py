import logging
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from .config import (
    VERSION,
    AUTHOR,
    EMAIL,
    ALLOWED_HOSTS,
    LOGS_DIR,
    LOG_LEVEL,
    ENABLE_DEBUG,
    DEVELOPMENT_MODE,
    get_logs_path,
    API_HOST,
    API_PORT,
)
from .routers import upload, preprocess, train, chat


# Configuração de logging
def setup_logging():
    """Configura o sistema de logging"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Cria diretório de logs se não existir
    get_logs_path().mkdir(parents=True, exist_ok=True)

    # Configuração básica
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper()),
        format=log_format,
        handlers=[
            logging.FileHandler(get_logs_path() / "backend.log"),
            logging.StreamHandler(),
        ],
    )

    # Logger específico da aplicação
    logger = logging.getLogger("omnisia")
    return logger


# Configuração de startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    logger = logging.getLogger("omnisia")
    logger.info("🚀 Iniciando OmnisIA Trainer Web Backend")
    logger.info(f"📦 Versão: {VERSION}")
    logger.info(f"👨‍💻 Autor: {AUTHOR} ({EMAIL})")
    logger.info(f"🔧 Modo Debug: {ENABLE_DEBUG}")
    logger.info(f"🏗️ Modo Desenvolvimento: {DEVELOPMENT_MODE}")
    
    # Inicialização do timestamp de startup
    app.state.start_time = time.time()
    logger.info("✅ Backend inicializado com sucesso")

    yield

    logger.info("🛑 Encerrando OmnisIA Trainer Web Backend")
    logger.info("✅ Backend encerrado com sucesso")


# Inicialização do logging
logger = setup_logging()

# Criação da aplicação FastAPI
app = FastAPI(
    title="OmnisIA Trainer Web API",
    description="API para treinamento e processamento de IA com LoRA",
    version=VERSION,
    contact={
        "name": AUTHOR,
        "email": EMAIL,
    },
    lifespan=lifespan,
    debug=ENABLE_DEBUG,
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        ["*"]
        if DEVELOPMENT_MODE
        else ["http://localhost:8501", "http://127.0.0.1:8501", "http://frontend:8501"]
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiáveis
if not DEVELOPMENT_MODE:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)


# Middleware de logging de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requisições"""
    start_time = time.time()

    # Processa a requisição
    response = await call_next(request)

    # Calcula tempo de processamento
    process_time = time.time() - start_time

    # Log da requisição
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Tempo: {process_time:.3f}s - "
        f"Cliente: {request.client.host if request.client else 'unknown'}"
    )

    return response


# Tratamento global de exceções
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Tratamento global de exceções"""
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)

    if DEVELOPMENT_MODE:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Erro interno do servidor: {str(exc)}",
                "type": type(exc).__name__,
                "path": str(request.url.path),
            },
        )
    else:
        return JSONResponse(
            status_code=500, content={"detail": "Erro interno do servidor"}
        )


# Inclusão dos routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(preprocess.router, prefix="/preprocess", tags=["preprocess"])
app.include_router(train.router, prefix="/train", tags=["train"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


# Endpoints principais
@app.get("/")
async def root():
    """Endpoint raiz da API"""
    return {
        "message": "OmnisIA Trainer Web API",
        "version": VERSION,
        "author": AUTHOR,
        "status": "online",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {
        "status": "healthy",
        "version": VERSION,
        "timestamp": time.time(),
        "uptime": (
            time.time() - app.state.start_time
            if hasattr(app.state, "start_time")
            else 0
        ),
    }


@app.get("/info")
async def get_info():
    """Endpoint com informações da aplicação"""
    return {
        "name": "OmnisIA Trainer Web API",
        "version": VERSION,
        "author": AUTHOR,
        "email": EMAIL,
        "debug": ENABLE_DEBUG,
        "development": DEVELOPMENT_MODE,
        "endpoints": [
            "/upload - Gerenciamento de arquivos",
            "/preprocess - Processamento (OCR, STT, etc.)",
            "/train - Treinamento de modelos LoRA",
            "/chat - Sistema de chat com contexto",
        ],
    }


# Execução do servidor
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"🚀 Iniciando servidor na porta {API_PORT}")
    uvicorn.run(
        "backend.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEVELOPMENT_MODE,
        log_level=LOG_LEVEL.lower(),
    )
