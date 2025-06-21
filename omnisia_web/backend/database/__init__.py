"""
Sistema de Banco de Dados OmnisIA
Database System for OmnisIA

Suporte para múltiplos bancos de dados:
- SQLite (padrão)
- PostgreSQL
- MongoDB
- DynamoDB
- Redis (cache)

Support for multiple databases:
- SQLite (default)
- PostgreSQL
- MongoDB
- DynamoDB
- Redis (cache)
"""

from .base import DatabaseManager
from .sqlite_db import SQLiteManager
from .postgres_db import PostgresManager
from .mongodb import MongoManager
from .dynamodb import DynamoDBManager
from .redis_cache import RedisManager

__all__ = [
    "DatabaseManager",
    "SQLiteManager",
    "PostgresManager",
    "MongoManager",
    "DynamoDBManager",
    "RedisManager",
]
