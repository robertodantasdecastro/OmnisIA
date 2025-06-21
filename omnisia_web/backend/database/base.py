"""
Classe Base para Gerenciamento de Bancos de Dados
Base Class for Database Management

Fornece interface comum para todos os tipos de banco de dados
Provides common interface for all database types
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
import logging
import os
from enum import Enum

logger = logging.getLogger("omnisia.database")


class DatabaseType(Enum):
    """Tipos de banco de dados suportados / Supported database types"""

    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MONGODB = "mongodb"
    DYNAMODB = "dynamodb"
    REDIS = "redis"


class DatabaseManager(ABC):
    """
    Classe base para gerenciamento de bancos de dados
    Base class for database management
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connected = False
        self.connection = None

    @abstractmethod
    async def connect(self) -> bool:
        """
        Conecta ao banco de dados
        Connect to database
        """
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """
        Desconecta do banco de dados
        Disconnect from database
        """
        pass

    @abstractmethod
    async def create_tables(self) -> bool:
        """
        Cria as tabelas necessárias
        Create necessary tables
        """
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """
        Verifica a saúde da conexão
        Check connection health
        """
        pass

    @abstractmethod
    async def insert(self, table: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Insere dados na tabela
        Insert data into table
        """
        pass

    @abstractmethod
    async def find(self, table: str, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Busca dados na tabela
        Find data in table
        """
        pass

    @abstractmethod
    async def update(
        self, table: str, query: Dict[str, Any], data: Dict[str, Any]
    ) -> int:
        """
        Atualiza dados na tabela
        Update data in table
        """
        pass

    @abstractmethod
    async def delete(self, table: str, query: Dict[str, Any]) -> int:
        """
        Remove dados da tabela
        Delete data from table
        """
        pass

    async def backup(self, backup_path: str) -> bool:
        """
        Cria backup do banco de dados
        Create database backup
        """
        logger.warning(f"Backup não implementado para {self.__class__.__name__}")
        return False

    async def restore(self, backup_path: str) -> bool:
        """
        Restaura backup do banco de dados
        Restore database backup
        """
        logger.warning(f"Restore não implementado para {self.__class__.__name__}")
        return False


class DatabaseFactory:
    """
    Factory para criação de gerenciadores de banco de dados
    Factory for creating database managers
    """

    @staticmethod
    def create_manager(
        db_type: DatabaseType, config: Dict[str, Any]
    ) -> DatabaseManager:
        """
        Cria gerenciador de banco de dados baseado no tipo
        Create database manager based on type
        """
        if db_type == DatabaseType.SQLITE:
            from .sqlite_db import SQLiteManager

            return SQLiteManager(config)

        elif db_type == DatabaseType.POSTGRESQL:
            from .postgres_db import PostgresManager

            return PostgresManager(config)

        elif db_type == DatabaseType.MONGODB:
            from .mongodb import MongoManager

            return MongoManager(config)

        elif db_type == DatabaseType.DYNAMODB:
            from .dynamodb import DynamoDBManager

            return DynamoDBManager(config)

        elif db_type == DatabaseType.REDIS:
            from .redis_cache import RedisManager

            return RedisManager(config)

        else:
            raise ValueError(f"Tipo de banco de dados não suportado: {db_type}")


def get_database_config() -> Dict[str, Any]:
    """
    Obtém configuração do banco de dados das variáveis de ambiente
    Get database configuration from environment variables
    """
    return {
        # SQLite
        "sqlite": {
            "database_url": os.getenv("DATABASE_URL", "sqlite:///./data/omnisia.db"),
            "pool_size": int(os.getenv("DATABASE_POOL_SIZE", "10")),
            "max_overflow": int(os.getenv("DATABASE_MAX_OVERFLOW", "20")),
            "echo": os.getenv("DATABASE_ECHO", "false").lower() == "true",
        },
        # PostgreSQL
        "postgresql": {
            "host": os.getenv("POSTGRES_HOST", "localhost"),
            "port": int(os.getenv("POSTGRES_PORT", "5432")),
            "database": os.getenv("POSTGRES_DB", "omnisia"),
            "user": os.getenv("POSTGRES_USER", "omnisia"),
            "password": os.getenv("POSTGRES_PASSWORD", ""),
            "url": os.getenv("POSTGRES_URL", ""),
            "enabled": os.getenv("ENABLE_POSTGRES", "false").lower() == "true",
        },
        # MongoDB
        "mongodb": {
            "host": os.getenv("MONGO_HOST", "localhost"),
            "port": int(os.getenv("MONGO_PORT", "27017")),
            "database": os.getenv("MONGO_DB", "omnisia"),
            "user": os.getenv("MONGO_USER", ""),
            "password": os.getenv("MONGO_PASSWORD", ""),
            "url": os.getenv("MONGO_URL", ""),
            "enabled": os.getenv("ENABLE_MONGODB", "false").lower() == "true",
        },
        # DynamoDB
        "dynamodb": {
            "region": os.getenv("DYNAMODB_REGION", "us-east-1"),
            "table_prefix": os.getenv("DYNAMODB_TABLE_PREFIX", "omnisia"),
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID", ""),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY", ""),
            "enabled": os.getenv("ENABLE_DYNAMODB", "false").lower() == "true",
        },
        # Redis
        "redis": {
            "url": os.getenv("REDIS_URL", "redis://localhost:6379"),
            "db": int(os.getenv("REDIS_DB", "0")),
            "password": os.getenv("REDIS_PASSWORD", ""),
            "max_connections": int(os.getenv("REDIS_MAX_CONNECTIONS", "10")),
            "enabled": os.getenv("ENABLE_REDIS", "false").lower() == "true",
        },
    }
