import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient) -> str:
    await client.post("/api/v1/auth/register", json={
        "email": "activity@example.com",
        "username": "activityuser",
        "password": "securepassword123",
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "activity@example.com",
        "password": "securepassword123",
    })
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_activity(client: AsyncClient):
    token = await get_auth_token(client)

    response = await client.post(
        "/api/v1/activities",
        json={
            "category": "transport",
            "sub_category": "car",
            "quantity": 50,
            "unit": "km",
            "date": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "transport"
    assert data["sub_category"] == "car"
    assert "carbon_kg" in data


@pytest.mark.asyncio
async def test_list_activities(client: AsyncClient):
    token = await get_auth_token(client)

    await client.post(
        "/api/v1/activities",
        json={
            "category": "food",
            "sub_category": "beef",
            "quantity": 1,
            "unit": "kg",
            "date": "2024-01-15",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    response = await client.get(
        "/api/v1/activities",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_activity_summary(client: AsyncClient):
    token = await get_auth_token(client)

    response = await client.get(
        "/api/v1/activities/summary",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_carbon" in data
    assert "activity_count" in data


@pytest.mark.asyncio
async def test_create_activity_unauthorized(client: AsyncClient):
    response = await client.post("/api/v1/activities", json={
        "category": "transport",
        "sub_category": "car",
        "quantity": 50,
        "unit": "km",
        "date": "2024-01-15",
    })
    assert response.status_code in (401, 403)
