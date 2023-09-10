import os
from uuid import uuid4
from asyncpg import Connection
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DB_USER = os.environ.get('POSTGRES_USER', 'username')
DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'password')
DB_NAME = os.environ.get('POSTGRES_DB', 'postgres')
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PORT = str(os.environ.get('POSTGRES_PORT', 5432))
DB_SCHEMA = os.environ.get('POSTGRES_SCHEMA', 'public')

class CConnection(Connection):
    def _get_unique_id(self, prefix):
        return f"__asyncpg_{prefix}_{uuid4()}__"

connect_args = {'prepared_statement_cache_size': 0,
                'statement_cache_size': 0,
                'connection_class': CConnection}

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?prepared_statement_cache_size=0"
DATABASE_SYNC_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = create_async_engine(DATABASE_URL, poolclass=NullPool, future=True, connect_args=connect_args)

async_session = sessionmaker(bind=database, class_=AsyncSession, expire_on_commit=False, autoflush=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session