from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get(
        "/", headers={"content-type": "text/html; charset=utf-8"})
    assert response.status_code == 200
    assert b"ChatBot" in response.content
    response = client.get("/static/css/chatbot.css")
    assert response.status_code == 200

