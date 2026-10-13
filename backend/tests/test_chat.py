from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_blank_input():
    assert client.post("/chat", json={"message": "   "}).status_code == 422

def test_too_long():
    assert client.post("/chat", json={"message": "x" * 1001}).status_code == 422

def test_unknown_fallback():
    response = client.post("/chat", json={"message": "quantum submarine timetable"})
    assert response.status_code == 200
    assert response.json()["sources"] == []
    assert "verified information" in response.json()["answer"]

def test_grounded_sources():
    with patch("app.main.generate_answer", new_callable=AsyncMock, return_value="Contact admissions." ):
        response = client.post("/chat", json={"message": "How do I apply for admission?"})
    assert response.status_code == 200
    assert response.json()["sources"][0]["id"] == "FAQ-001"
