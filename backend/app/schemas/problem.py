"""
Schemas Pydantic para validação de dados de problemas técnicos.

Conceitos importantes:
- Enum: Define um conjunto fixo de valores permitidos. Usando str + Enum,
  os valores são serializados como strings no JSON (e não como inteiros).
- BaseModel: Classe base do Pydantic que valida automaticamente os dados
  recebidos (tipos, obrigatoriedade, restrições) e gera erros claros.
- Field: Permite adicionar validações extras (min_length, max_length, etc.)
  e documentação para o Swagger do FastAPI.
"""
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    """
    Categorias de problemas técnicos.

    Herdar de 'str' junto com 'Enum' garante que o valor serializado no JSON
    seja a string ("Hardware", "Rede", etc.) e não um índice numérico.
    Isso também permite comparação direta com strings.
    """
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    REDE = "Rede"
    SEGURANCA = "Segurança"
    SISTEMA_OPERACIONAL = "Sistema Operacional"
    BANCO_DE_DADOS = "Banco de Dados"
    OUTROS = "Outros"


class Priority(str, Enum):
    """
    Níveis de prioridade dos problemas.
    - Baixa: não compromete atividades significativamente.
    - Média: prejudica parcialmente as atividades.
    - Alta: compromete atividades importantes ou afeta vários usuários.
    """
    BAIXA = "Baixa"
    MEDIA = "Média"
    ALTA = "Alta"


# ---- Schemas de Entrada (Request) ----

class ProblemCreateRequest(BaseModel):
    """
    Schema de entrada para criação de um novo problema.
    Enviado pelo frontend no corpo do POST /problems.

    Validações:
    - description: obrigatória, mínimo de 10 caracteres.
      A IA precisa de contexto suficiente para fazer uma boa classificação.
    """
    description: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Descrição do problema técnico em linguagem natural.",
        examples=["Meu computador está conectado ao Wi-Fi, mas não consigo acessar nenhum site."],
    )


# ---- Schemas de Resposta da IA ----

class GeminiAnalysisResult(BaseModel):
    """
    Schema que define o formato exato esperado na resposta do Gemini.

    Ao enviar este schema como 'response_schema' para a API do Gemini,
    forçamos a IA a retornar exatamente neste formato JSON.

    Se a IA retornar algo fora deste contrato, o Pydantic rejeita
    automaticamente com um erro de validação — evitando dados corrompidos
    no banco de dados.
    """
    category: Category = Field(
        ...,
        description="Categoria do problema identificado."
    )
    priority: Priority = Field(
        ...,
        description="Prioridade de atendimento baseada no impacto e urgência."
    )
    summary: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Resumo conciso do problema identificado."
    )
    initial_suggestion: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Sugestão inicial de solução para o problema."
    )


# ---- Schemas de Saída (Response) ----

class ProblemResponse(BaseModel):
    """
    Schema de saída retornado pela API ao frontend.
    Inclui todos os campos persistidos no banco de dados.

    O 'model_config' com from_attributes=True permite criar uma instância
    diretamente de uma Row/tupla nomeada do banco de dados,
    sem precisar converter manualmente campo por campo.
    """
    id: int = Field(..., description="Identificador único do problema.")
    description: str = Field(..., description="Descrição original do usuário.")
    category: Category = Field(..., description="Categoria classificada pela IA.")
    priority: Priority = Field(..., description="Prioridade classificada pela IA.")
    summary: str = Field(..., description="Resumo gerado pela IA.")
    initial_suggestion: str = Field(..., description="Sugestão inicial da IA.")
    created_at: datetime = Field(..., description="Data e horário do registro.")

    model_config = {"from_attributes": True}
