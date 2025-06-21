"""
Sistema de Banco de Dados OmnisIA
Database System for OmnisIA

Suporte para múltiplos bancos de dados:
- SQLite (planejado)
- PostgreSQL (planejado)
- MongoDB (planejado)
- DynamoDB (planejado)
- Redis (planejado)

Support for multiple databases:
- SQLite (planned)
- PostgreSQL (planned)
- MongoDB (planned)
- DynamoDB (planned)
- Redis (planned)

Atualmente implementado:
- Classe base DatabaseManager
"""

from .base import DatabaseManager

# TODO: Implementar módulos específicos de banco de dados
# from .sqlite_db import SQLiteManager
# from .postgres_db import PostgresManager
# from .mongodb import MongoManager
# from .dynamodb import DynamoDBManager
# from .redis_cache import RedisManager

__all__ = [
    "DatabaseManager",
    # "SQLiteManager",
    # "PostgresManager",
    # "MongoManager",
    # "DynamoDBManager",
    # "RedisManager",
]
