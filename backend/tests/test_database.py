from app.database import init_db_pool, close_db_pool, get_db_connection


def test_database_connection_pool():
    """Testa se o pool de conexões inicializa e consegue executar uma query simples."""
    pool = init_db_pool()
    assert pool is not None
    assert not pool.closed

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_name = 'problems';")
            result = cur.fetchone()
            assert result is not None
            assert result[0] == "problems"

    close_db_pool()
    assert pool.closed
