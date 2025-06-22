from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os
from typing import List, Dict
from ..config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from datetime import datetime

router = APIRouter()


def validate_file(file: UploadFile) -> None:
    """Valida o arquivo enviado"""
    # Verifica extensão
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não permitido. Tipos aceitos: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Verifica se o arquivo tem conteúdo
    if not file.filename:
        raise HTTPException(status_code=400, detail="Nome do arquivo é obrigatório")


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    """Upload de arquivo com validação e retorno de metadados completos."""
    try:
        validate_file(file)

        # Verifica tamanho do arquivo
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB",
            )

        # Salva o arquivo
        dest = UPLOAD_DIR / file.filename
        dest.write_bytes(file_content)

        # Retorna o mesmo formato do endpoint de listagem
        return {
            "name": file.filename,
            "size": len(file_content),
            "path": str(dest.resolve()),
            "type": dest.suffix.lower().replace(".", ""),
            "status": "Recebido",
            "upload_date": datetime.now().isoformat(),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")


@router.get("/files", response_model=List[Dict])
async def list_uploaded_files():
    """
    Lista todos os arquivos no diretório de upload, fornecendo
    um dicionário completo de informações para cada arquivo.
    """
    try:
        files_info = []
        if not UPLOAD_DIR.exists():
            return []

        for item in UPLOAD_DIR.iterdir():
            if item.is_file():
                file_info = {
                    "name": item.name,
                    "size": item.stat().st_size,
                    "path": str(item.resolve()),
                    "type": item.suffix.lower().replace(".", ""),
                    "status": "Disponível",
                    "upload_date": datetime.fromtimestamp(
                        item.stat().st_ctime
                    ).isoformat(),
                }
                files_info.append(file_info)

        # Ordena os arquivos por data de modificação, os mais recentes primeiro
        files_info.sort(key=lambda x: x["upload_date"], reverse=True)
        return files_info

    except Exception as e:
        # Log do erro pode ser adicionado aqui
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar arquivos: {str(e)}"
        )
