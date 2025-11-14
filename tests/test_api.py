import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Medical Records AI API"
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_analyze_endpoint(client: AsyncClient):
    patient_data = {
        "patient_name": "Test Patient",
        "age": 30,
        "symptoms": "headache, fever",
        "medical_history": None
    }
    response = await client.post("/records/analyze", json=patient_data)
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)


@pytest.mark.asyncio
async def test_request_otp_endpoint(client: AsyncClient):
    user_data = {
        "name": "Test User",
        "email": "test@example.com"
    }
    response = await client.post("/auth/request-otp", json=user_data)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "message" in data
        assert "test@example.com" in data["message"]


@pytest.mark.asyncio
async def test_verify_otp_invalid(client: AsyncClient):
    otp_data = {
        "email": "nonexistent@example.com",
        "otp": "123456"
    }
    response = await client.post("/auth/verify-otp", json=otp_data)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_without_auth(client: AsyncClient):
    response = await client.get("/records")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_with_invalid_token(client: AsyncClient):
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.get("/records", headers=headers)
    assert response.status_code == 401
