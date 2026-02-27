import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient) -> str:
    await client.post("/api/v1/auth/register", json={
        "email": "dashboard@example.com",
        "username": "dashuser",
        "password": "securepassword123",
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "dashboard@example.com",
        "password": "securepassword123",
    })
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_dashboard_overview(client: AsyncClient):
    token = await get_auth_token(client)

    response = await client.get(
        "/api/v1/dashboard/overview",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_carbon_today" in data
    assert "eco_score" in data
    assert "streak_days" in data


@pytest.mark.asyncio
async def test_dashboard_trends(client: AsyncClient):
    token = await get_auth_token(client)

    response = await client.get(
        "/api/v1/dashboard/trends",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "days" in data
    assert "total_kg" in data


@pytest.mark.asyncio
async def test_dashboard_tips(client: AsyncClient):
    token = await get_auth_token(client)

    response = await client.get(
        "/api/v1/dashboard/tips",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_dashboard_unauthorized(client: AsyncClient):
    response = await client.get("/api/v1/dashboard/overview")
    assert response.status_code in (401, 403)
