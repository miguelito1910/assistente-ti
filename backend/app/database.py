"""
Gerenciamento de conexões com o PostgreSQL usando Psycopg 3.
Utiliza ConnectionPool para reutilizar conexões abertas de forma thread-safe e eficiente.
"""
from contextlib import contextmanager
from typing import Generator
from psycopg_pool import ConnectionPool
from psycopg import Connection
from app.config import settings

# Pool de conexões global
# min_size=2: mantém pelo menos 2 conexões abertas prontas para uso
# max_size=10: permite até 10 conexões simultâneas sob carga
pool: ConnectionPool | None = None


def init_db_pool() -> ConnectionPool:
    """Inicializa o pool de conexões com o banco de dados."""
    global pool
    if pool is None or pool.closed:
        pool = ConnectionPool(
            conninfo=settings.database_url,
            min_size=2,
            max_size=10,
            timeout=10.0,
            open=True,
        )
    return pool


def close_db_pool() -> None:
    """Fecha todas as conexões do pool no encerramento da aplicação."""
    global pool
    if pool is not None and not pool.closed:
        pool.close()
        pool = None


@contextmanager
def get_db_connection() -> Generator[Connection, None, None]:
    """
    Context manager que entrega uma conexão segura retirada do pool.
    Garante o retorno automático da conexão ao pool e commit/rollback em caso de erro.
    """
    if pool is None or pool.closed:
        init_db_pool()

    with pool.connection() as conn:
        yield conn
