from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Testa se o endpoint /health responde 200 e com o formato esperado."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "app": "Assistente Inteligente de TI",
        "version": "0.1.0"
    }
