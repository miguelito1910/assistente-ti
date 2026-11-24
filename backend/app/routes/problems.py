"""
Endpoints (rotas) da API REST para o recurso 'problems'.

Responsabilidades deste módulo:
- Receber as requisições HTTP e validar a entrada com Pydantic.
- Chamar os serviços corretos (gemini_service, problem_service).
- Retornar as respostas HTTP com os códigos de status adequados.
- Tratar erros e converter em respostas HTTP padronizadas.

O que NÃO deve ficar aqui:
- Lógica de negócio (fica nos services).
- SQL direto (fica no problem_service).
- Chamadas à API externa (fica no gemini_service).
"""
from fastapi import APIRouter, HTTPException, status

from app.schemas.problem import ProblemCreateRequest, ProblemResponse
from app.services import gemini_service, problem_service

# APIRouter permite separar as rotas em módulos distintos.
# O prefixo "/problems" é adicionado ao registrar o router no main.py.
router = APIRouter(prefix="/problems", tags=["Problemas"])


@router.post(
    "",
    response_model=ProblemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar e classificar um problema técnico",
    description=(
        "Recebe a descrição de um problema em linguagem natural, "
        "encaminha para a IA, valida a resposta e persiste no banco de dados."
    ),
)
def create_problem(request: ProblemCreateRequest) -> ProblemResponse:
    """
    Fluxo completo de registro de um problema:
    1. FastAPI valida automaticamente o body via ProblemCreateRequest.
    2. Envia a descrição para o Gemini (mock nesta etapa).
    3. Persiste o resultado no PostgreSQL.
    4. Retorna os dados completos com status 201 Created.
    """
    try:
        # Etapa 2: Analisar com IA (mock por enquanto)
        analysis = gemini_service.analyze_problem(request.description)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Erro ao consultar o serviço de IA: {exc}",
        ) from exc

    try:
        # Etapa 3: Persistir no banco
        problem = problem_service.create_problem(request.description, analysis)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao salvar o problema no banco de dados: {exc}",
        ) from exc

    return problem


@router.get(
    "",
    response_model=list[ProblemResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar histórico de problemas",
    description="Retorna todos os problemas registrados, do mais recente ao mais antigo.",
)
def list_problems() -> list[ProblemResponse]:
    """Retorna o histórico completo de problemas registrados."""
    try:
        return problem_service.list_problems()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar o banco de dados: {exc}",
        ) from exc


@router.get(
    "/{problem_id}",
    response_model=ProblemResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar um problema por ID",
    description="Retorna os detalhes de um problema específico pelo seu identificador.",
)
def get_problem(problem_id: int) -> ProblemResponse:
    """
    Busca um problema pelo ID.
    Retorna 404 Not Found se o ID não existir no banco.
    """
    try:
        problem = problem_service.get_problem_by_id(problem_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao consultar o banco de dados: {exc}",
        ) from exc

    if problem is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problema com ID {problem_id} não encontrado.",
        )

    return problem
