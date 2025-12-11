import pytest
from fastapi.testclient import TestClient
from main import app
from dependencies import (
    db_teams, db_drivers, db_race_strategies, 
    db_driver_performance, users_db, get_password_hash
)
from engineer_management import db_engineer_schedules
from report_system import db_race_reports

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def reset_db():
    db_teams.clear()
    db_drivers.clear()
    db_race_strategies.clear()
    db_driver_performance.clear()
    db_engineer_schedules.clear()
    db_race_reports.clear()
    
    users_db.clear()
    users_db["jbenham"] = {
        "username": "jbenham",
        "full_name": "Jake Benham",
        "email": "jakebenham@f1system.com",
        "hashed_password": get_password_hash("opmeersucks"),
        "disabled": False,
    }

@pytest.fixture
def auth_headers(client):
    response = client.post(
        "/token",
        data={"username": "jbenham", "password": "opmeersucks"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}