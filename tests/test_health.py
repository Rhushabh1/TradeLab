from fastapi.testclient import TestClient 

from app.main import app


client = TestClient(app)

# establish a runnable application before introducing dependencies
def test_health():
	response = client.get("health")
	assert response.status_code == 200
	assert response.json()["status"] == "healthy"

def test_root():
	response = client.get("/")
	assert response.status_code == 200

def test_error():
	response = client.get("/error")
	assert response.status_code == 400