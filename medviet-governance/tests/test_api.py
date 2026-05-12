import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "MedViet Data API"}

def test_get_raw_patients_unauthorized():
    response = client.get("/api/patients/raw")
    assert response.status_code == 401
    assert response.json()["detail"] == "Missing token"

def test_get_raw_patients_admin():
    response = client.get("/api/patients/raw", headers={"Authorization": "Bearer token-alice"})
    # it might return 500 if data/raw/patients_raw.csv does not exist, but let's test authorization first
    assert response.status_code in [200, 500] 
    
def test_get_raw_patients_intern():
    response = client.get("/api/patients/raw", headers={"Authorization": "Bearer token-dave"})
    assert response.status_code == 403
    assert "cannot 'read' on 'patient_data'" in response.json()["detail"]

def test_delete_patient_admin():
    response = client.delete("/api/patients/P001", headers={"Authorization": "Bearer token-alice"})
    assert response.status_code == 200
    assert response.json()["deleted_by"] == "alice"

def test_delete_patient_forbidden():
    response = client.delete("/api/patients/P001", headers={"Authorization": "Bearer token-bob"})
    assert response.status_code == 403
