from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os
from typing import List
from ..config import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

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
    """Upload de arquivo com validação"""
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
        with dest.open("wb") as f:
            f.write(file_content)

        return {"filename": file.filename, "size": len(file_content), "path": str(dest)}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")


@router.get("/files")
async def list_files():
    """Lista arquivos enviados"""
    try:
        files = []
        for file_path in UPLOAD_DIR.iterdir():
            if file_path.is_file():
                files.append(
                    {
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                    }
                )
        return {"files": files}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar arquivos: {str(e)}"
        )
