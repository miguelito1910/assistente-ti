"""
Testes de validação dos Schemas Pydantic.
Garantem que as regras de entrada e saída estão funcionando corretamente.
"""
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas.problem import (
    Category,
    GeminiAnalysisResult,
    Priority,
    ProblemCreateRequest,
    ProblemResponse,
)


# ---- Testes do ProblemCreateRequest ----

class TestProblemCreateRequest:
    """Testes de validação da entrada do usuário."""

    def test_descricao_valida(self):
        """Descrição com tamanho adequado deve ser aceita."""
        request = ProblemCreateRequest(
            description="Meu computador não liga quando aperto o botão de power."
        )
        assert request.description == "Meu computador não liga quando aperto o botão de power."

    def test_descricao_vazia_rejeita(self):
        """Descrição vazia deve ser rejeitada pelo Pydantic."""
        with pytest.raises(ValidationError) as exc_info:
            ProblemCreateRequest(description="")
        # Verifica que o erro menciona o campo 'description'
        assert "description" in str(exc_info.value)

    def test_descricao_curta_demais_rejeita(self):
        """Descrição com menos de 10 caracteres deve ser rejeitada."""
        with pytest.raises(ValidationError):
            ProblemCreateRequest(description="PC lento")  # 8 caracteres

    def test_descricao_ausente_rejeita(self):
        """Sem campo description deve gerar erro."""
        with pytest.raises(ValidationError):
            ProblemCreateRequest()


# ---- Testes do GeminiAnalysisResult ----

class TestGeminiAnalysisResult:
    """Testes de validação do JSON retornado pela IA."""

    def test_resposta_valida(self):
        """JSON com todos os campos válidos deve ser aceito."""
        result = GeminiAnalysisResult(
            category="Rede",
            priority="Alta",
            summary="Computador conectado ao Wi-Fi, mas sem acesso à internet.",
            initial_suggestion="Verificar configurações de DNS e renovar IP.",
        )
        assert result.category == Category.REDE
        assert result.priority == Priority.ALTA

    def test_categoria_invalida_rejeita(self):
        """Categoria fora do Enum deve ser rejeitada."""
        with pytest.raises(ValidationError):
            GeminiAnalysisResult(
                category="Impressora",  # Não existe no Enum
                priority="Baixa",
                summary="Impressora não imprime.",
                initial_suggestion="Verificar cabo USB.",
            )

    def test_prioridade_invalida_rejeita(self):
        """Prioridade fora do Enum deve ser rejeitada."""
        with pytest.raises(ValidationError):
            GeminiAnalysisResult(
                category="Hardware",
                priority="Urgente",  # Não existe no Enum
                summary="Notebook superaquecendo.",
                initial_suggestion="Limpar cooler.",
            )

    def test_resumo_vazio_rejeita(self):
        """Resumo vazio deve ser rejeitado."""
        with pytest.raises(ValidationError):
            GeminiAnalysisResult(
                category="Software",
                priority="Média",
                summary="",
                initial_suggestion="Reinstalar o programa.",
            )


# ---- Testes dos Enums ----

class TestEnums:
    """Testes de que os Enums cobrem as categorias e prioridades especificadas."""

    def test_todas_categorias_existem(self):
        """Verifica que todas as 7 categorias do projeto estão no Enum."""
        categorias_esperadas = {
            "Hardware", "Software", "Rede", "Segurança",
            "Sistema Operacional", "Banco de Dados", "Outros"
        }
        categorias_enum = {c.value for c in Category}
        assert categorias_enum == categorias_esperadas

    def test_todas_prioridades_existem(self):
        """Verifica que os 3 níveis de prioridade estão no Enum."""
        prioridades_esperadas = {"Baixa", "Média", "Alta"}
        prioridades_enum = {p.value for p in Priority}
        assert prioridades_enum == prioridades_esperadas

    def test_enum_category_e_string(self):
        """Enums do tipo str permitem comparação direta com strings."""
        assert Category.REDE == "Rede"
        assert Priority.ALTA == "Alta"


# ---- Testes do ProblemResponse ----

class TestProblemResponse:
    """Testes do schema de saída da API."""

    def test_response_valido(self):
        """Verifica que o schema de saída aceita dados completos."""
        response = ProblemResponse(
            id=1,
            description="Meu computador não liga.",
            category="Hardware",
            priority="Alta",
            summary="Computador não liga ao pressionar botão power.",
            initial_suggestion="Verificar fonte de alimentação e cabos.",
            created_at=datetime.now(timezone.utc),
        )
        assert response.id == 1
        assert response.category == Category.HARDWARE
