"""
Serviço de persistência dos problemas no PostgreSQL.

Responsável por executar os comandos SQL de inserção e consulta.
Usa consultas parametrizadas (%s) em vez de formatar strings diretamente,
o que previne ataques de SQL Injection.

Exemplo de SQL INSEGURO (nunca fazer):
    f"INSERT INTO problems (description) VALUES ('{description}')"

Exemplo de SQL SEGURO (o que fazemos aqui):
    "INSERT INTO problems (description) VALUES (%s)", (description,)
"""
from app.database import get_db_connection
from app.schemas.problem import GeminiAnalysisResult, ProblemResponse


def create_problem(
    description: str,
    analysis: GeminiAnalysisResult,
) -> ProblemResponse:
    """
    Persiste um novo problema no banco e retorna o registro completo.

    O SQL usa RETURNING para obter todos os campos (incluindo id e created_at)
    gerados automaticamente pelo PostgreSQL em um único comando,
    sem precisar fazer uma segunda consulta.
    """
    sql = """
        INSERT INTO problems
            (description, category, priority, summary, initial_suggestion)
        VALUES
            (%s, %s, %s, %s, %s)
        RETURNING
            id, description, category, priority, summary, initial_suggestion, created_at
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (
                description,
                analysis.category.value,
                analysis.priority.value,
                analysis.summary,
                analysis.initial_suggestion,
            ))
            row = cur.fetchone()
        conn.commit()

    return ProblemResponse(
        id=row[0],
        description=row[1],
        category=row[2],
        priority=row[3],
        summary=row[4],
        initial_suggestion=row[5],
        created_at=row[6],
    )


def list_problems() -> list[ProblemResponse]:
    """
    Retorna todos os problemas registrados, do mais recente para o mais antigo.
    O índice idx_problems_created_at_desc criado no schema.sql
    torna essa consulta eficiente mesmo com muitos registros.
    """
    sql = """
        SELECT id, description, category, priority, summary, initial_suggestion, created_at
        FROM problems
        ORDER BY created_at DESC
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()

    return [
        ProblemResponse(
            id=row[0],
            description=row[1],
            category=row[2],
            priority=row[3],
            summary=row[4],
            initial_suggestion=row[5],
            created_at=row[6],
        )
        for row in rows
    ]


def get_problem_by_id(problem_id: int) -> ProblemResponse | None:
    """
    Busca um problema pelo seu ID.
    Retorna None se não encontrado (a rota decidirá o código HTTP adequado).
    """
    sql = """
        SELECT id, description, category, priority, summary, initial_suggestion, created_at
        FROM problems
        WHERE id = %s
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (problem_id,))
            row = cur.fetchone()

    if row is None:
        return None

    return ProblemResponse(
        id=row[0],
        description=row[1],
        category=row[2],
        priority=row[3],
        summary=row[4],
        initial_suggestion=row[5],
        created_at=row[6],
    )
