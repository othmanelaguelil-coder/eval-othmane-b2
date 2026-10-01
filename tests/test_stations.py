from fastapi.testclient import TestClient
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, Base, get_db

TEST_DATABASE_URL = "sqlite:///./test_stations.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)

def test_create_station(client):
    response = client.post(
        "/stations",
        json={
            "code": "TEST001",
            "name": "Station Test",
            "capacity": 10,
            "status": "open"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["code"] == "TEST001"
    assert data["name"] == "Station Test"
    assert data["capacity"] == 10
    assert data["status"] == "open"

def test_duplicate_code(client):
    station = {
        "code": "TEST001",
        "name": "Station Test",
        "capacity": 10,
        "status": "open"
    }

    response1 = client.post("/stations", json=station)

    assert response1.status_code == 201

    response2 = client.post("/stations", json=station)

    assert response2.status_code == 409

def test_get_station_not_found(client):
    response = client.get("/stations/999")

    assert response.status_code == 404

def test_create_station_invalid_capacity(client):
    response = client.post(
        "/stations",
        json={
            "code": "TEST002",
            "name": "Station Test",
            "capacity": 0,
            "status": "open"
        }
    )

    assert response.status_code == 422

def test_update_station(client):
    response = client.post(
        "/stations",
        json={
            "code": "TEST003",
            "name": "Ancienne Gare",
            "capacity": 20,
            "status": "open"
        }
    )

    assert response.status_code == 201

    station_id = response.json()["id"]

    response = client.patch(
        f"/stations/{station_id}",
        json={
            "name": "Nouvelle Gare"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Nouvelle Gare"
    assert data["status"] == "open"

def test_filter_stations_by_status(client):
    client.post(
        "/stations",
        json={
            "code": "TEST004",
            "name": "Station Ouverte",
            "capacity": 20,
            "status": "open"
        }
    )

    client.post(
        "/stations",
        json={
            "code": "TEST005",
            "name": "Station Fermee",
            "capacity": 15,
            "status": "closed"
        }
    )

    response = client.get("/stations?status=open")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["code"] == "TEST004"
    assert data[0]["status"] == "open"