"""
Serviço de integração com o Google Gemini via SDK oficial google-genai.

Como funciona a integração com Structured Outputs:
- Em vez de pedir ao Gemini para "escrever um JSON", passamos o schema Pydantic
  diretamente como 'response_schema'. Isso instrui a API a retornar um JSON
  estruturado que sempre respeita o contrato definido em GeminiAnalysisResult.
- A validação Pydantic ao final garante que, mesmo que a API retorne algo
  inesperado, o erro será capturado antes de qualquer dado inválido
  chegar ao banco de dados.

Tratamento de erros:
- APIError: erros retornados pela API do Gemini (cota, chave inválida, etc.)
- ValueError: resposta recebida mas com formato inválido (schema não respeitado)
- Exception: qualquer outro erro inesperado (timeout, rede, etc.)
Todos são propagados como exceções e capturados na camada de rotas,
que os converte em respostas HTTP adequadas (502 Bad Gateway).
"""
from google import genai
from google.genai import types

from app.config import settings
from app.schemas.problem import GeminiAnalysisResult

# Prompt de sistema: define o papel e o contexto do modelo.
# Instruções claras e objetivas produzem respostas mais consistentes.
SYSTEM_PROMPT = """
Você é um especialista em suporte técnico de TI. Sua tarefa é analisar relatos
de problemas técnicos descritos por usuários e retornar uma classificação estruturada.

Categorias disponíveis:
- Hardware: problemas físicos com equipamentos (computador, impressora, mouse, etc.)
- Software: problemas com programas, aplicativos ou sistemas instalados
- Rede: problemas de conectividade, Wi-Fi, internet ou rede local
- Segurança: suspeitas de vírus, malware, acessos não autorizados ou vazamento de dados
- Sistema Operacional: problemas com Windows, Linux ou macOS
- Banco de Dados: problemas com banco de dados, consultas ou conexões
- Outros: problemas que não se enquadram nas categorias anteriores

Prioridades:
- Baixa: não compromete atividades significativamente
- Média: prejudica parcialmente as atividades
- Alta: compromete atividades importantes ou afeta vários usuários

Regras importantes:
1. Baseie a prioridade no impacto e urgência descrita pelo usuário.
2. O resumo deve ser conciso (máximo 2 frases).
3. A sugestão inicial é uma orientação técnica, não um diagnóstico definitivo.
4. Responda SEMPRE em português.
""".strip()


def analyze_problem(description: str) -> GeminiAnalysisResult:
    """
    Analisa um problema técnico usando o Google Gemini e retorna um resultado estruturado.

    Args:
        description: Descrição do problema em linguagem natural.

    Returns:
        GeminiAnalysisResult validado com categoria, prioridade, resumo e sugestão.

    Raises:
        Exception: Em caso de erro na API ou resposta inválida.
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=f"Analise o seguinte problema técnico:\n\n{description}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=GeminiAnalysisResult,
            temperature=0.2,  # Valor baixo = respostas mais consistentes e objetivas
        ),
    )

    # O SDK já faz o parse do JSON e popula o objeto diretamente.
    # Validamos via Pydantic para garantir que os valores respeitam os Enums.
    raw = response.parsed
    return GeminiAnalysisResult.model_validate(raw)
