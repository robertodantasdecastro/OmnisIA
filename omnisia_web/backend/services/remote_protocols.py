"""
Protocolos Remotos para OmnisIA Trainer Web
Remote Protocols for OmnisIA Trainer Web

Suporte para múltiplos protocolos de comunicação remota:
- FTP/FTPS
- SFTP/SSH
- HTTP/HTTPS
- WebDAV
- AWS S3
- Google Drive
- Dropbox

Support for multiple remote communication protocols:
- FTP/FTPS
- SFTP/SSH
- HTTP/HTTPS
- WebDAV
- AWS S3
- Google Drive
- Dropbox
"""

import os
import asyncio
import aiohttp
import aiofiles
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, BinaryIO
from pathlib import Path
import logging
from datetime import datetime
from urllib.parse import urlparse
import hashlib

# Imports condicionais para protocolos específicos
try:
    import paramiko

    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

try:
    import aioftp

    AIOFTP_AVAILABLE = True
except ImportError:
    AIOFTP_AVAILABLE = False

try:
    import boto3
    from botocore.exceptions import ClientError

    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

logger = logging.getLogger("omnisia.remote_protocols")


class RemoteProtocol(ABC):
    """
    Classe base para protocolos remotos
    Base class for remote protocols
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connected = False
        self.connection = None

    @abstractmethod
    async def connect(self) -> bool:
        """Conecta ao servidor remoto / Connect to remote server"""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Desconecta do servidor remoto / Disconnect from remote server"""
        pass

    @abstractmethod
    async def upload_file(self, local_path: Path, remote_path: str) -> bool:
        """Faz upload de arquivo / Upload file"""
        pass

    @abstractmethod
    async def download_file(self, remote_path: str, local_path: Path) -> bool:
        """Faz download de arquivo / Download file"""
        pass

    @abstractmethod
    async def list_files(self, remote_path: str = "/") -> List[Dict[str, Any]]:
        """Lista arquivos remotos / List remote files"""
        pass

    @abstractmethod
    async def delete_file(self, remote_path: str) -> bool:
        """Remove arquivo remoto / Delete remote file"""
        pass

    async def create_directory(self, remote_path: str) -> bool:
        """Cria diretório remoto / Create remote directory"""
        logger.warning(
            f"Criação de diretório não implementada para {self.__class__.__name__}"
        )
        return False

    async def get_file_info(self, remote_path: str) -> Optional[Dict[str, Any]]:
        """Obtém informações do arquivo / Get file information"""
        logger.warning(
            f"Informações de arquivo não implementadas para {self.__class__.__name__}"
        )
        return None


class FTPProtocol(RemoteProtocol):
    """
    Protocolo FTP/FTPS
    FTP/FTPS Protocol
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not AIOFTP_AVAILABLE:
            raise ImportError("aioftp não está instalado. Execute: pip install aioftp")

    async def connect(self) -> bool:
        """Conecta ao servidor FTP"""
        try:
            self.connection = aioftp.Client()

            await self.connection.connect(
                host=self.config["host"], port=self.config.get("port", 21)
            )

            await self.connection.login(
                user=self.config["user"], password=self.config["password"]
            )

            # Configurar modo passivo se especificado
            if self.config.get("passive", True):
                await self.connection.command("PASV")

            self.connected = True
            logger.info(f"Conectado ao FTP: {self.config['host']}")
            return True

        except Exception as e:
            logger.error(f"Erro ao conectar FTP: {str(e)}")
            return False

    async def disconnect(self) -> bool:
        """Desconecta do servidor FTP"""
        try:
            if self.connection:
                await self.connection.quit()
                self.connected = False
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar FTP: {str(e)}")
            return False

    async def upload_file(self, local_path: Path, remote_path: str) -> bool:
        """Faz upload via FTP"""
        try:
            if not self.connected:
                await self.connect()

            await self.connection.upload(str(local_path), remote_path)
            logger.info(f"Upload FTP concluído: {local_path} -> {remote_path}")
            return True

        except Exception as e:
            logger.error(f"Erro no upload FTP: {str(e)}")
            return False

    async def download_file(self, remote_path: str, local_path: Path) -> bool:
        """Faz download via FTP"""
        try:
            if not self.connected:
                await self.connect()

            # Criar diretório local se não existir
            local_path.parent.mkdir(parents=True, exist_ok=True)

            await self.connection.download(remote_path, str(local_path))
            logger.info(f"Download FTP concluído: {remote_path} -> {local_path}")
            return True

        except Exception as e:
            logger.error(f"Erro no download FTP: {str(e)}")
            return False

    async def list_files(self, remote_path: str = "/") -> List[Dict[str, Any]]:
        """Lista arquivos via FTP"""
        try:
            if not self.connected:
                await self.connect()

            files = []
            async for path, info in self.connection.list(remote_path):
                files.append(
                    {
                        "name": path.name,
                        "path": str(path),
                        "size": info.get("size", 0),
                        "modified": info.get("modify", ""),
                        "is_directory": info.get("type") == "dir",
                    }
                )

            return files

        except Exception as e:
            logger.error(f"Erro ao listar FTP: {str(e)}")
            return []

    async def delete_file(self, remote_path: str) -> bool:
        """Remove arquivo via FTP"""
        try:
            if not self.connected:
                await self.connect()

            await self.connection.remove(remote_path)
            logger.info(f"Arquivo removido via FTP: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao remover arquivo FTP: {str(e)}")
            return False


class SFTPProtocol(RemoteProtocol):
    """
    Protocolo SFTP/SSH
    SFTP/SSH Protocol
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not PARAMIKO_AVAILABLE:
            raise ImportError(
                "paramiko não está instalado. Execute: pip install paramiko"
            )

    async def connect(self) -> bool:
        """Conecta ao servidor SFTP"""
        try:
            # Criar cliente SSH
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Configurar autenticação
            connect_kwargs = {
                "hostname": self.config["host"],
                "port": self.config.get("port", 22),
                "username": self.config["user"],
            }

            # Usar chave SSH se especificada
            if "key_file" in self.config and self.config["key_file"]:
                connect_kwargs["key_filename"] = self.config["key_file"]
            else:
                connect_kwargs["password"] = self.config["password"]

            # Conectar SSH
            ssh_client.connect(**connect_kwargs)

            # Criar cliente SFTP
            self.connection = ssh_client.open_sftp()
            self.ssh_client = ssh_client

            self.connected = True
            logger.info(f"Conectado ao SFTP: {self.config['host']}")
            return True

        except Exception as e:
            logger.error(f"Erro ao conectar SFTP: {str(e)}")
            return False

    async def disconnect(self) -> bool:
        """Desconecta do servidor SFTP"""
        try:
            if self.connection:
                self.connection.close()
            if hasattr(self, "ssh_client"):
                self.ssh_client.close()
            self.connected = False
            return True
        except Exception as e:
            logger.error(f"Erro ao desconectar SFTP: {str(e)}")
            return False

    async def upload_file(self, local_path: Path, remote_path: str) -> bool:
        """Faz upload via SFTP"""
        try:
            if not self.connected:
                await self.connect()

            # Executar upload em thread separada (paramiko é síncrono)
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, self.connection.put, str(local_path), remote_path
            )

            logger.info(f"Upload SFTP concluído: {local_path} -> {remote_path}")
            return True

        except Exception as e:
            logger.error(f"Erro no upload SFTP: {str(e)}")
            return False

    async def download_file(self, remote_path: str, local_path: Path) -> bool:
        """Faz download via SFTP"""
        try:
            if not self.connected:
                await self.connect()

            # Criar diretório local se não existir
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Executar download em thread separada
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, self.connection.get, remote_path, str(local_path)
            )

            logger.info(f"Download SFTP concluído: {remote_path} -> {local_path}")
            return True

        except Exception as e:
            logger.error(f"Erro no download SFTP: {str(e)}")
            return False

    async def list_files(self, remote_path: str = "/") -> List[Dict[str, Any]]:
        """Lista arquivos via SFTP"""
        try:
            if not self.connected:
                await self.connect()

            # Executar listagem em thread separada
            loop = asyncio.get_event_loop()
            file_attrs = await loop.run_in_executor(
                None, self.connection.listdir_attr, remote_path
            )

            files = []
            for attr in file_attrs:
                files.append(
                    {
                        "name": attr.filename,
                        "path": f"{remote_path.rstrip('/')}/{attr.filename}",
                        "size": attr.st_size or 0,
                        "modified": (
                            datetime.fromtimestamp(attr.st_mtime).isoformat()
                            if attr.st_mtime
                            else ""
                        ),
                        "is_directory": attr.st_mode
                        and (attr.st_mode & 0o170000) == 0o040000,
                    }
                )

            return files

        except Exception as e:
            logger.error(f"Erro ao listar SFTP: {str(e)}")
            return []

    async def delete_file(self, remote_path: str) -> bool:
        """Remove arquivo via SFTP"""
        try:
            if not self.connected:
                await self.connect()

            # Executar remoção em thread separada
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.connection.remove, remote_path)

            logger.info(f"Arquivo removido via SFTP: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"Erro ao remover arquivo SFTP: {str(e)}")
            return False


class HTTPProtocol(RemoteProtocol):
    """
    Protocolo HTTP/HTTPS
    HTTP/HTTPS Protocol
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.session = None

    async def connect(self) -> bool:
        """Cria sessão HTTP"""
        try:
            timeout = aiohttp.ClientTimeout(total=self.config.get("timeout", 30))

            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={"User-Agent": self.config.get("user_agent", "OmnisIA/1.0")},
            )

            self.connected = True
            logger.info("Sessão HTTP criada")
            return True

        except Exception as e:
            logger.error(f"Erro ao criar sessão HTTP: {str(e)}")
            return False

    async def disconnect(self) -> bool:
        """Fecha sessão HTTP"""
        try:
            if self.session:
                await self.session.close()
                self.connected = False
            return True
        except Exception as e:
            logger.error(f"Erro ao fechar sessão HTTP: {str(e)}")
            return False

    async def upload_file(self, local_path: Path, remote_url: str) -> bool:
        """Faz upload via HTTP POST"""
        try:
            if not self.connected:
                await self.connect()

            async with aiofiles.open(local_path, "rb") as file:
                data = await file.read()

                async with self.session.post(remote_url, data=data) as response:
                    if response.status == 200:
                        logger.info(
                            f"Upload HTTP concluído: {local_path} -> {remote_url}"
                        )
                        return True
                    else:
                        logger.error(
                            f"Erro HTTP {response.status}: {await response.text()}"
                        )
                        return False

        except Exception as e:
            logger.error(f"Erro no upload HTTP: {str(e)}")
            return False

    async def download_file(self, remote_url: str, local_path: Path) -> bool:
        """Faz download via HTTP GET"""
        try:
            if not self.connected:
                await self.connect()

            # Criar diretório local se não existir
            local_path.parent.mkdir(parents=True, exist_ok=True)

            async with self.session.get(remote_url) as response:
                if response.status == 200:
                    async with aiofiles.open(local_path, "wb") as file:
                        async for chunk in response.content.iter_chunked(8192):
                            await file.write(chunk)

                    logger.info(
                        f"Download HTTP concluído: {remote_url} -> {local_path}"
                    )
                    return True
                else:
                    logger.error(
                        f"Erro HTTP {response.status}: {await response.text()}"
                    )
                    return False

        except Exception as e:
            logger.error(f"Erro no download HTTP: {str(e)}")
            return False

    async def list_files(self, remote_url: str = "/") -> List[Dict[str, Any]]:
        """Lista arquivos via HTTP (não implementado genericamente)"""
        logger.warning("Listagem HTTP não implementada genericamente")
        return []

    async def delete_file(self, remote_url: str) -> bool:
        """Remove arquivo via HTTP DELETE"""
        try:
            if not self.connected:
                await self.connect()

            async with self.session.delete(remote_url) as response:
                if response.status in [200, 204]:
                    logger.info(f"Arquivo removido via HTTP: {remote_url}")
                    return True
                else:
                    logger.error(
                        f"Erro HTTP {response.status}: {await response.text()}"
                    )
                    return False

        except Exception as e:
            logger.error(f"Erro ao remover arquivo HTTP: {str(e)}")
            return False


class S3Protocol(RemoteProtocol):
    """
    Protocolo AWS S3
    AWS S3 Protocol
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if not BOTO3_AVAILABLE:
            raise ImportError("boto3 não está instalado. Execute: pip install boto3")

    async def connect(self) -> bool:
        """Cria cliente S3"""
        try:
            self.connection = boto3.client(
                "s3",
                aws_access_key_id=self.config["aws_access_key_id"],
                aws_secret_access_key=self.config["aws_secret_access_key"],
                region_name=self.config.get("region", "us-east-1"),
            )

            self.bucket = self.config["bucket"]
            self.prefix = self.config.get("prefix", "")

            self.connected = True
            logger.info(f"Cliente S3 criado para bucket: {self.bucket}")
            return True

        except Exception as e:
            logger.error(f"Erro ao criar cliente S3: {str(e)}")
            return False

    async def disconnect(self) -> bool:
        """Fecha cliente S3"""
        self.connected = False
        return True

    async def upload_file(self, local_path: Path, remote_key: str) -> bool:
        """Faz upload para S3"""
        try:
            if not self.connected:
                await self.connect()

            full_key = f"{self.prefix}{remote_key}".lstrip("/")

            # Executar upload em thread separada
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.connection.upload_file,
                str(local_path),
                self.bucket,
                full_key,
            )

            logger.info(
                f"Upload S3 concluído: {local_path} -> s3://{self.bucket}/{full_key}"
            )
            return True

        except Exception as e:
            logger.error(f"Erro no upload S3: {str(e)}")
            return False

    async def download_file(self, remote_key: str, local_path: Path) -> bool:
        """Faz download do S3"""
        try:
            if not self.connected:
                await self.connect()

            # Criar diretório local se não existir
            local_path.parent.mkdir(parents=True, exist_ok=True)

            full_key = f"{self.prefix}{remote_key}".lstrip("/")

            # Executar download em thread separada
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.connection.download_file,
                self.bucket,
                full_key,
                str(local_path),
            )

            logger.info(
                f"Download S3 concluído: s3://{self.bucket}/{full_key} -> {local_path}"
            )
            return True

        except Exception as e:
            logger.error(f"Erro no download S3: {str(e)}")
            return False

    async def list_files(self, remote_prefix: str = "") -> List[Dict[str, Any]]:
        """Lista objetos no S3"""
        try:
            if not self.connected:
                await self.connect()

            full_prefix = f"{self.prefix}{remote_prefix}".lstrip("/")

            # Executar listagem em thread separada
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self.connection.list_objects_v2,
                **{"Bucket": self.bucket, "Prefix": full_prefix},
            )

            files = []
            for obj in response.get("Contents", []):
                files.append(
                    {
                        "name": obj["Key"].split("/")[-1],
                        "path": obj["Key"],
                        "size": obj["Size"],
                        "modified": obj["LastModified"].isoformat(),
                        "is_directory": obj["Key"].endswith("/"),
                    }
                )

            return files

        except Exception as e:
            logger.error(f"Erro ao listar S3: {str(e)}")
            return []

    async def delete_file(self, remote_key: str) -> bool:
        """Remove objeto do S3"""
        try:
            if not self.connected:
                await self.connect()

            full_key = f"{self.prefix}{remote_key}".lstrip("/")

            # Executar remoção em thread separada
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.connection.delete_object,
                **{"Bucket": self.bucket, "Key": full_key},
            )

            logger.info(f"Objeto removido do S3: s3://{self.bucket}/{full_key}")
            return True

        except Exception as e:
            logger.error(f"Erro ao remover objeto S3: {str(e)}")
            return False


class RemoteProtocolManager:
    """
    Gerenciador de múltiplos protocolos remotos
    Manager for multiple remote protocols
    """

    def __init__(self):
        self.protocols: Dict[str, RemoteProtocol] = {}

    def add_protocol(self, name: str, protocol: RemoteProtocol):
        """Adiciona protocolo / Add protocol"""
        self.protocols[name] = protocol
        logger.info(f"Protocolo adicionado: {name}")

    def get_protocol(self, name: str) -> Optional[RemoteProtocol]:
        """Obtém protocolo / Get protocol"""
        return self.protocols.get(name)

    async def connect_all(self) -> Dict[str, bool]:
        """Conecta todos os protocolos / Connect all protocols"""
        results = {}
        for name, protocol in self.protocols.items():
            try:
                results[name] = await protocol.connect()
            except Exception as e:
                logger.error(f"Erro ao conectar {name}: {str(e)}")
                results[name] = False
        return results

    async def disconnect_all(self) -> Dict[str, bool]:
        """Desconecta todos os protocolos / Disconnect all protocols"""
        results = {}
        for name, protocol in self.protocols.items():
            try:
                results[name] = await protocol.disconnect()
            except Exception as e:
                logger.error(f"Erro ao desconectar {name}: {str(e)}")
                results[name] = False
        return results

    async def health_check(self) -> Dict[str, Dict[str, Any]]:
        """Verifica saúde dos protocolos / Check protocols health"""
        health = {}
        for name, protocol in self.protocols.items():
            health[name] = {
                "connected": protocol.connected,
                "protocol_type": protocol.__class__.__name__,
                "config": {
                    k: v
                    for k, v in protocol.config.items()
                    if "password" not in k.lower()
                },
            }
        return health


def create_protocol_from_config(
    protocol_type: str, config: Dict[str, Any]
) -> RemoteProtocol:
    """
    Cria protocolo baseado na configuração
    Create protocol based on configuration
    """
    if protocol_type.lower() == "ftp":
        return FTPProtocol(config)
    elif protocol_type.lower() == "sftp":
        return SFTPProtocol(config)
    elif protocol_type.lower() == "http":
        return HTTPProtocol(config)
    elif protocol_type.lower() == "s3":
        return S3Protocol(config)
    else:
        raise ValueError(f"Protocolo não suportado: {protocol_type}")


def get_remote_protocols_config() -> Dict[str, Dict[str, Any]]:
    """
    Obtém configuração dos protocolos remotos das variáveis de ambiente
    Get remote protocols configuration from environment variables
    """
    return {
        "ftp": {
            "enabled": os.getenv("ENABLE_FTP", "false").lower() == "true",
            "host": os.getenv("FTP_HOST", ""),
            "port": int(os.getenv("FTP_PORT", "21")),
            "user": os.getenv("FTP_USER", ""),
            "password": os.getenv("FTP_PASSWORD", ""),
            "passive": os.getenv("FTP_PASSIVE", "true").lower() == "true",
        },
        "sftp": {
            "enabled": os.getenv("ENABLE_SFTP", "false").lower() == "true",
            "host": os.getenv("SFTP_HOST", ""),
            "port": int(os.getenv("SFTP_PORT", "22")),
            "user": os.getenv("SFTP_USER", ""),
            "password": os.getenv("SFTP_PASSWORD", ""),
            "key_file": os.getenv("SFTP_KEY_FILE", ""),
        },
        "http": {
            "enabled": os.getenv("ENABLE_HTTP_DOWNLOAD", "true").lower() == "true",
            "timeout": int(os.getenv("HTTP_TIMEOUT", "30")),
            "max_retries": int(os.getenv("HTTP_MAX_RETRIES", "3")),
            "user_agent": os.getenv("HTTP_USER_AGENT", "OmnisIA/1.0"),
        },
        "s3": {
            "enabled": os.getenv("ENABLE_S3_STORAGE", "false").lower() == "true",
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            "region": os.getenv("AWS_REGION", "us-east-1"),
            "bucket": os.getenv("S3_BUCKET", ""),
            "prefix": os.getenv("S3_PREFIX", "omnisia/"),
        },
    }
