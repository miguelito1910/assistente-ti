"""
Testes dos endpoints REST de /problems.

Usamos TestClient do FastAPI (baseado no httpx) para simular requisições HTTP
sem precisar subir um servidor de verdade.

Os testes de POST usam unittest.mock.patch para substituir:
- gemini_service.analyze_problem  → não chama a API do Gemini
- problem_service.create_problem  → não escreve no banco de dados real
Dessa forma, testamos SOMENTE a lógica das rotas de forma isolada e rápida.

Os testes de GET/listagem conectam ao banco real (que já criamos),
então validamos o comportamento completo de leitura.
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.problem import Category, GeminiAnalysisResult, Priority, ProblemResponse

client = TestClient(app)

# Fixtures: dados reutilizáveis entre os testes
MOCK_ANALYSIS = GeminiAnalysisResult(
    category=Category.REDE,
    priority=Priority.ALTA,
    summary="Sem acesso à internet.",
    initial_suggestion="Verificar DNS e renovar IP.",
)

MOCK_PROBLEM_RESPONSE = ProblemResponse(
    id=1,
    description="Meu computador não acessa nenhum site.",
    category=Category.REDE,
    priority=Priority.ALTA,
    summary="Sem acesso à internet.",
    initial_suggestion="Verificar DNS e renovar IP.",
    created_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
)


# ---- POST /problems ----

class TestCreateProblem:

    @patch("app.routes.problems.problem_service.create_problem", return_value=MOCK_PROBLEM_RESPONSE)
    @patch("app.routes.problems.gemini_service.analyze_problem", return_value=MOCK_ANALYSIS)
    def test_cria_problema_com_sucesso(self, mock_gemini, mock_service):
        """Deve retornar 201 e os dados do problema criado."""
        response = client.post(
            "/problems",
            json={"description": "Meu computador não acessa nenhum site da internet."}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["category"] == "Rede"
        assert data["priority"] == "Alta"
        # Confirma que o gemini e o service foram chamados exatamente 1 vez
        mock_gemini.assert_called_once()
        mock_service.assert_called_once()

    def test_descricao_muito_curta_retorna_422(self):
        """Descrição com menos de 10 caracteres deve retornar 422."""
        response = client.post("/problems", json={"description": "PC lento"})
        assert response.status_code == 422

    def test_descricao_vazia_retorna_422(self):
        """Descrição vazia deve retornar 422."""
        response = client.post("/problems", json={"description": ""})
        assert response.status_code == 422

    def test_body_ausente_retorna_422(self):
        """Sem body deve retornar 422."""
        response = client.post("/problems", json={})
        assert response.status_code == 422

    @patch("app.routes.problems.gemini_service.analyze_problem", side_effect=Exception("Timeout"))
    def test_erro_no_gemini_retorna_502(self, mock_gemini):
        """Se o Gemini falhar, deve retornar 502 Bad Gateway."""
        response = client.post(
            "/problems",
            json={"description": "Meu computador não acessa nenhum site."}
        )
        assert response.status_code == 502
        assert "IA" in response.json()["detail"]

    @patch("app.routes.problems.problem_service.create_problem", side_effect=Exception("DB Error"))
    @patch("app.routes.problems.gemini_service.analyze_problem", return_value=MOCK_ANALYSIS)
    def test_erro_no_banco_retorna_500(self, mock_gemini, mock_service):
        """Se o banco falhar, deve retornar 500 Internal Server Error."""
        response = client.post(
            "/problems",
            json={"description": "Meu computador não acessa nenhum site."}
        )
        assert response.status_code == 500
        assert "banco de dados" in response.json()["detail"]


# ---- GET /problems ----

class TestListProblems:

    @patch("app.routes.problems.problem_service.list_problems", return_value=[MOCK_PROBLEM_RESPONSE])
    def test_lista_problemas_retorna_200(self, mock_service):
        """GET /problems deve retornar 200 e uma lista."""
        response = client.get("/problems")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1

    @patch("app.routes.problems.problem_service.list_problems", return_value=[])
    def test_lista_vazia_retorna_200(self, mock_service):
        """GET /problems com banco vazio deve retornar 200 e lista vazia."""
        response = client.get("/problems")
        assert response.status_code == 200
        assert response.json() == []


# ---- GET /problems/{id} ----

class TestGetProblemById:

    @patch("app.routes.problems.problem_service.get_problem_by_id", return_value=MOCK_PROBLEM_RESPONSE)
    def test_busca_por_id_valido_retorna_200(self, mock_service):
        """GET /problems/1 deve retornar 200 e o problema."""
        response = client.get("/problems/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    @patch("app.routes.problems.problem_service.get_problem_by_id", return_value=None)
    def test_id_inexistente_retorna_404(self, mock_service):
        """GET /problems/999 deve retornar 404 se não existir."""
        response = client.get("/problems/999")
        assert response.status_code == 404
        assert "999" in response.json()["detail"]
