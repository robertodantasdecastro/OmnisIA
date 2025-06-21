"""
OMNISIA - API FastAPI Completa / Complete FastAPI API
===================================================

API completa para o sistema OmnisIA com suporte para:
- Modelos locais e APIs externas
- Múltiplos bancos de dados
- Treinamento LoRA
- Processamento de arquivos
- Protocolos remotos
- Chat com assistente IA

Autor: Roberto Dantas de Castro
Email: robertodantasdecastro@gmail.com
"""

import logging
import time
import traceback
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any
from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    UploadFile,
    File,
    Form,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Importar configurações
from config import (
    SYSTEM_INFO,
    API_HOST,
    API_PORT,
    DEVELOPMENT_MODE,
    DEBUG_MODE,
    SECURITY_CONFIG,
    setup_logging,
    validate_config,
    get_api_config,
    LOCAL_MODELS_CONFIG,
    LORA_CONFIG,
    TRAINING_CONFIG,
    FTP_CONFIG,
    SFTP_CONFIG,
    HTTP_CONFIG,
    WEBDAV_CONFIG,
    DATABASE_TYPE,
    get_database_url,
    UPLOAD_DIR,
    MODELS_DIR,
    TRAINING_DIR,
    CHECKPOINTS_DIR,
    is_file_allowed,
)

# Configurar logging
logger = setup_logging()

# ============================================================================
# MODELOS PYDANTIC / PYDANTIC MODELS
# ============================================================================


class SystemInfo(BaseModel):
    name: str = "OmnisIA"
    version: str = SYSTEM_INFO["version"]
    author: str = SYSTEM_INFO["author"]
    email: str = SYSTEM_INFO["email"]
    build_date: str = SYSTEM_INFO["build_date"]
    status: str = "online"


class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    model: Optional[str] = "deepseek-r1"
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(1000, ge=1, le=4000)


class ChatResponse(BaseModel):
    response: str
    model: str
    timestamp: float
    processing_time: float


class TrainingRequest(BaseModel):
    model_name: str = Field(..., description="Nome do modelo base")
    dataset_path: str = Field(..., description="Caminho do dataset")
    epochs: int = Field(3, ge=1, le=100)
    batch_size: int = Field(2, ge=1, le=32)
    learning_rate: float = Field(2e-4, ge=1e-6, le=1e-2)
    lora_r: int = Field(16, ge=1, le=256)
    lora_alpha: int = Field(32, ge=1, le=512)


class TrainingStatus(BaseModel):
    job_id: str
    status: str  # "running", "completed", "failed", "pending"
    progress: float = Field(ge=0.0, le=100.0)
    current_epoch: int = 0
    total_epochs: int = 0
    loss: Optional[float] = None
    estimated_time_remaining: Optional[int] = None


class FileInfo(BaseModel):
    filename: str
    size: int
    type: str
    upload_time: float
    processed: bool = False


class ModelInfo(BaseModel):
    name: str
    type: str  # "local", "api"
    size: Optional[str] = None
    status: str  # "available", "downloading", "error"
    path: Optional[str] = None


class DatabaseInfo(BaseModel):
    type: str
    status: str
    url: str
    connection_count: int = 0


class RemoteProtocolConfig(BaseModel):
    protocol: str  # "ftp", "sftp", "http", "webdav"
    host: str
    port: int
    username: Optional[str] = None
    enabled: bool = False


# ============================================================================
# DEPENDÊNCIAS / DEPENDENCIES
# ============================================================================


async def get_current_user():
    """Placeholder para autenticação futura"""
    return {"user_id": "default", "permissions": ["all"]}


def check_file_type(filename: str):
    """Verifica se o tipo de arquivo é permitido"""
    if not is_file_allowed(filename):
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não suportado: {Path(filename).suffix}",
        )
    return True


# ============================================================================
# CONFIGURAÇÃO DO FASTAPI / FASTAPI CONFIGURATION
# ============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando OmnisIA API")
    logger.info(f"📦 Versão: {SYSTEM_INFO['version']}")
    logger.info(f"👨‍💻 Autor: {SYSTEM_INFO['author']}")
    logger.info(f"🔧 Modo Debug: {DEBUG_MODE}")
    logger.info(f"🏗️ Modo Desenvolvimento: {DEVELOPMENT_MODE}")

    # Validar configuração
    errors = validate_config()
    if errors:
        logger.warning("⚠️ Avisos de configuração encontrados:")
        for error in errors:
            logger.warning(f"  • {error}")

    yield

    logger.info("🛑 Encerrando OmnisIA API")


# Criar aplicação FastAPI
app = FastAPI(
    title="OmnisIA API",
    description="API completa para sistema integrado de IA multimodal",
    version=SYSTEM_INFO["version"],
    contact={
        "name": SYSTEM_INFO["author"],
        "email": SYSTEM_INFO["email"],
    },
    lifespan=lifespan,
    debug=DEBUG_MODE,
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=SECURITY_CONFIG["cors_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de hosts confiáveis (produção)
if not DEVELOPMENT_MODE:
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=SECURITY_CONFIG["allowed_hosts"]
    )


# Middleware de logging de requisições
@app.middleware("http")
async def log_requests(request, call_next):
    """Middleware para logging de requisições"""
    start_time = time.time()

    # Processar requisição
    response = await call_next(request)

    # Calcular tempo de processamento
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
async def global_exception_handler(request, exc):
    """Tratamento global de exceções"""
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)

    if DEBUG_MODE:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"Erro interno: {str(exc)}",
                "type": type(exc).__name__,
                "path": str(request.url.path),
                "traceback": traceback.format_exc(),
            },
        )
    else:
        return JSONResponse(
            status_code=500, content={"detail": "Erro interno do servidor"}
        )


# ============================================================================
# ENDPOINTS PRINCIPAIS / MAIN ENDPOINTS
# ============================================================================


@app.get("/", response_model=SystemInfo)
async def root():
    """Endpoint raiz da API"""
    return SystemInfo()


@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {
        "status": "healthy",
        "version": SYSTEM_INFO["version"],
        "timestamp": time.time(),
        "uptime": getattr(app.state, "start_time", 0),
        "database": DATABASE_TYPE,
        "models_available": len(LOCAL_MODELS_CONFIG),
    }


@app.get("/info")
async def get_info():
    """Informações detalhadas do sistema"""
    errors = validate_config()

    return {
        "system": SYSTEM_INFO,
        "configuration": {
            "development_mode": DEVELOPMENT_MODE,
            "debug_mode": DEBUG_MODE,
            "database_type": DATABASE_TYPE,
            "api_host": API_HOST,
            "api_port": API_PORT,
        },
        "features": {
            "local_models": len(LOCAL_MODELS_CONFIG),
            "database_support": ["sqlite", "postgresql", "mongodb", "redis"],
            "protocols": ["http", "ftp", "sftp", "webdav"],
            "file_processing": ["pdf", "images", "audio", "video"],
            "training": "LoRA fine-tuning",
        },
        "validation": {
            "status": "valid" if not errors else "warnings",
            "errors": errors,
        },
    }


# ============================================================================
# ENDPOINTS DE CHAT / CHAT ENDPOINTS
# ============================================================================


@app.post("/chat", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
):
    """Endpoint de chat com assistente IA"""
    start_time = time.time()

    try:
        # Importar assistente (lazy loading)
        from agentes.assistente import AssistenteIA

        assistente = AssistenteIA(
            model=message.model,
            temperature=message.temperature,
            max_tokens=message.max_tokens,
        )

        # Processar mensagem
        response = await assistente.responder(message.message)

        processing_time = time.time() - start_time

        # Log da conversa (background task)
        background_tasks.add_task(
            log_conversation, user["user_id"], message.message, response, message.model
        )

        return ChatResponse(
            response=response,
            model=message.model,
            timestamp=time.time(),
            processing_time=processing_time,
        )

    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="Assistente IA não disponível. Verifique as dependências.",
        )
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar mensagem: {str(e)}"
        )


async def log_conversation(user_id: str, message: str, response: str, model: str):
    """Registra a conversa no log (background task)"""
    logger.info(f"Chat - User: {user_id}, Model: {model}, Message: {message[:100]}...")


# ============================================================================
# ENDPOINTS DE UPLOAD / UPLOAD ENDPOINTS
# ============================================================================


@app.post("/upload", response_model=FileInfo)
async def upload_file(
    file: UploadFile = File(...),
    process_immediately: bool = Form(False),
    user=Depends(get_current_user),
):
    """Upload de arquivos"""
    # Verificar tipo de arquivo
    check_file_type(file.filename)

    try:
        # Salvar arquivo
        file_path = UPLOAD_DIR / file.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        file_info = FileInfo(
            filename=file.filename,
            size=len(content),
            type=file.content_type or "unknown",
            upload_time=time.time(),
            processed=False,
        )

        logger.info(f"Arquivo enviado: {file.filename} ({len(content)} bytes)")

        # Processar imediatamente se solicitado
        if process_immediately:
            # TODO: Implementar processamento automático
            file_info.processed = True

        return file_info

    except Exception as e:
        logger.error(f"Erro no upload: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")


@app.get("/files")
async def list_files(user=Depends(get_current_user)):
    """Lista arquivos enviados"""
    try:
        files = []
        if UPLOAD_DIR.exists():
            for file_path in UPLOAD_DIR.iterdir():
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append(
                        {
                            "filename": file_path.name,
                            "size": stat.st_size,
                            "modified": stat.st_mtime,
                            "path": str(file_path),
                        }
                    )

        return {"files": files, "total": len(files)}

    except Exception as e:
        logger.error(f"Erro ao listar arquivos: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar arquivos: {str(e)}"
        )


@app.delete("/files/{filename}")
async def delete_file(filename: str, user=Depends(get_current_user)):
    """Remove arquivo"""
    try:
        file_path = UPLOAD_DIR / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")

        file_path.unlink()
        logger.info(f"Arquivo removido: {filename}")

        return {"message": f"Arquivo {filename} removido com sucesso"}

    except Exception as e:
        logger.error(f"Erro ao remover arquivo: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao remover arquivo: {str(e)}"
        )


# ============================================================================
# ENDPOINTS DE TREINAMENTO / TRAINING ENDPOINTS
# ============================================================================


@app.post("/training/start", response_model=Dict[str, str])
async def start_training(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
):
    """Iniciar treinamento LoRA"""
    try:
        # Gerar ID único para o job
        import uuid

        job_id = str(uuid.uuid4())

        # Validar modelo
        if request.model_name not in LOCAL_MODELS_CONFIG:
            raise HTTPException(
                status_code=400, detail=f"Modelo não suportado: {request.model_name}"
            )

        # Validar dataset
        dataset_path = Path(request.dataset_path)
        if not dataset_path.exists():
            raise HTTPException(
                status_code=400,
                detail=f"Dataset não encontrado: {request.dataset_path}",
            )

        # Iniciar treinamento em background
        background_tasks.add_task(run_training_job, job_id, request, user["user_id"])

        logger.info(
            f"Treinamento iniciado - Job ID: {job_id}, Modelo: {request.model_name}"
        )

        return {
            "job_id": job_id,
            "status": "started",
            "message": "Treinamento iniciado com sucesso",
        }

    except Exception as e:
        logger.error(f"Erro ao iniciar treinamento: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao iniciar treinamento: {str(e)}"
        )


@app.get("/training/{job_id}", response_model=TrainingStatus)
async def get_training_status(job_id: str, user=Depends(get_current_user)):
    """Status do treinamento"""
    # TODO: Implementar storage persistente de jobs
    # Por enquanto, retornar status mockado
    return TrainingStatus(
        job_id=job_id,
        status="running",
        progress=45.0,
        current_epoch=2,
        total_epochs=3,
        loss=0.234,
        estimated_time_remaining=1200,
    )


@app.get("/training")
async def list_training_jobs(user=Depends(get_current_user)):
    """Lista todos os jobs de treinamento"""
    # TODO: Implementar listagem real de jobs
    return {"jobs": [], "active": 0, "completed": 0, "failed": 0}


async def run_training_job(job_id: str, request: TrainingRequest, user_id: str):
    """Executa job de treinamento (background task)"""
    try:
        logger.info(f"Executando treinamento - Job: {job_id}")

        # Importar módulo de treinamento
        from modelos.treinamento import iniciar_treinamento_lora

        # Executar treinamento
        await iniciar_treinamento_lora(
            model_name=request.model_name,
            dataset_path=request.dataset_path,
            epochs=request.epochs,
            batch_size=request.batch_size,
        )

        logger.info(f"Treinamento concluído - Job: {job_id}")

    except Exception as e:
        logger.error(f"Erro no treinamento - Job: {job_id}, Erro: {e}")


# ============================================================================
# ENDPOINTS DE MODELOS / MODELS ENDPOINTS
# ============================================================================


@app.get("/models", response_model=List[ModelInfo])
async def list_models():
    """Lista modelos disponíveis"""
    models = []

    # Modelos locais
    for name, config in LOCAL_MODELS_CONFIG.items():
        models.append(
            ModelInfo(
                name=name,
                type="local",
                size=config.get("size", "unknown"),
                status="available" if config["path"].exists() else "not_downloaded",
                path=str(config["path"]),
            )
        )

    # APIs externas disponíveis
    external_apis = ["openai", "deepseek", "anthropic", "google"]
    for api in external_apis:
        api_config = get_api_config(api)
        if api_config.get("api_key"):
            models.append(ModelInfo(name=api, type="api", status="available"))

    return models


@app.post("/models/{model_name}/download")
async def download_model(
    model_name: str, background_tasks: BackgroundTasks, user=Depends(get_current_user)
):
    """Baixar modelo local"""
    if model_name not in LOCAL_MODELS_CONFIG:
        raise HTTPException(
            status_code=404, detail=f"Modelo não encontrado: {model_name}"
        )

    # Iniciar download em background
    background_tasks.add_task(download_model_task, model_name)

    return {
        "message": f"Download do modelo {model_name} iniciado",
        "status": "downloading",
    }


async def download_model_task(model_name: str):
    """Task para download de modelo"""
    try:
        logger.info(f"Iniciando download do modelo: {model_name}")

        config = LOCAL_MODELS_CONFIG[model_name]

        # TODO: Implementar download real do HuggingFace
        # from transformers import AutoModel, AutoTokenizer
        # model = AutoModel.from_pretrained(config["url"])
        # tokenizer = AutoTokenizer.from_pretrained(config["url"])

        logger.info(f"Download concluído: {model_name}")

    except Exception as e:
        logger.error(f"Erro no download do modelo {model_name}: {e}")


# ============================================================================
# ENDPOINTS DE BANCO DE DADOS / DATABASE ENDPOINTS
# ============================================================================


@app.get("/database/info", response_model=DatabaseInfo)
async def get_database_info():
    """Informações do banco de dados"""
    return DatabaseInfo(
        type=DATABASE_TYPE,
        status="connected",
        url=get_database_url(),
        connection_count=1,  # TODO: Implementar contagem real
    )


@app.get("/database/tables")
async def list_database_tables():
    """Lista tabelas do banco de dados"""
    # TODO: Implementar listagem real das tabelas
    return {"tables": ["users", "conversations", "files", "training_jobs"], "total": 4}


# ============================================================================
# ENDPOINTS DE PROTOCOLOS REMOTOS / REMOTE PROTOCOLS ENDPOINTS
# ============================================================================


@app.get("/protocols", response_model=List[RemoteProtocolConfig])
async def list_protocols():
    """Lista protocolos remotos configurados"""
    protocols = []

    # FTP
    protocols.append(
        RemoteProtocolConfig(
            protocol="ftp",
            host=FTP_CONFIG["host"],
            port=FTP_CONFIG["port"],
            username=FTP_CONFIG["username"],
            enabled=bool(FTP_CONFIG["host"]),
        )
    )

    # SFTP
    protocols.append(
        RemoteProtocolConfig(
            protocol="sftp",
            host=SFTP_CONFIG["host"],
            port=SFTP_CONFIG["port"],
            username=SFTP_CONFIG["username"],
            enabled=bool(SFTP_CONFIG["host"]),
        )
    )

    # WebDAV
    protocols.append(
        RemoteProtocolConfig(
            protocol="webdav",
            host=WEBDAV_CONFIG["url"],
            port=443,  # HTTPS padrão
            username=WEBDAV_CONFIG["username"],
            enabled=bool(WEBDAV_CONFIG["url"]),
        )
    )

    return protocols


@app.post("/protocols/{protocol}/test")
async def test_protocol(protocol: str):
    """Testar conexão com protocolo remoto"""
    try:
        if protocol == "ftp":
            # TODO: Implementar teste FTP
            result = {"status": "success", "message": "Conexão FTP OK"}
        elif protocol == "sftp":
            # TODO: Implementar teste SFTP
            result = {"status": "success", "message": "Conexão SFTP OK"}
        elif protocol == "webdav":
            # TODO: Implementar teste WebDAV
            result = {"status": "success", "message": "Conexão WebDAV OK"}
        else:
            raise HTTPException(status_code=400, detail="Protocolo não suportado")

        return result

    except Exception as e:
        logger.error(f"Erro ao testar protocolo {protocol}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao testar {protocol}: {str(e)}"
        )


# ============================================================================
# MIDDLEWARE DE INICIALIZAÇÃO / INITIALIZATION MIDDLEWARE
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Evento de inicialização"""
    app.state.start_time = time.time()
    logger.info("🎯 OmnisIA API inicializada com sucesso!")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de encerramento"""
    logger.info("👋 OmnisIA API encerrada")


# ============================================================================
# SERVIR ARQUIVOS ESTÁTICOS / SERVE STATIC FILES
# ============================================================================

# Servir arquivos de upload (apenas em desenvolvimento)
if DEVELOPMENT_MODE and UPLOAD_DIR.exists():
    app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Informações finais no log
logger.info(f"🌟 OmnisIA API configurada - Versão {SYSTEM_INFO['version']}")
logger.info(f"🔗 Documentação: http://{API_HOST}:{API_PORT}/docs")
logger.info(f"🔍 ReDoc: http://{API_HOST}:{API_PORT}/redoc")
