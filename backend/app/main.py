from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import close_db_pool, init_db_pool
from app.routes.problems import router as problems_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.

    O bloco antes do 'yield' executa na inicialização do servidor:
    abre o pool de conexões com o banco de dados.

    O bloco após o 'yield' executa no encerramento:
    fecha todas as conexões do pool corretamente.

    Isso evita 'connection leak' (conexões abertas esquecidas).
    """
    init_db_pool()
    yield
    close_db_pool()


app = FastAPI(
    title="Assistente Inteligente de TI",
    description="API para identificação, classificação e priorização de problemas técnicos via IA.",
    version="0.1.0",
    lifespan=lifespan,
)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que o frontend React acerte chamadas na API sem bloqueio do navegador
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção restringimos ao domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro dos routers
app.include_router(problems_router)


@app.get("/health", tags=["Status"])
def health_check():
    """
    Endpoint simples de verificação de integridade da API.
    Utilizado para monitoramento e validação de que o serviço está no ar.
    """
    return {
        "status": "healthy",
        "app": "Assistente Inteligente de TI",
        "version": "0.1.0"
    }
