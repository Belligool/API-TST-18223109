from fastapi import status
import pytest

# ==========================================
# 1. AUTHENTICATION & SECURITY TESTS
# ==========================================

def test_login_success(client):
    """Test login dengan kredensial benar."""
    response = client.post(
        "/token",
        data={"username": "jbenham", "password": "opmeersucks"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure(client):
    """Test login dengan password salah."""
    response = client.post(
        "/token",
        data={"username": "jbenham", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_access_without_token(client):
    """Security: Akses endpoint terlindungi tanpa token."""
    response = client.get("/teams/1")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

# ==========================================
# 2. TEAM MANAGEMENT TESTS
# ==========================================

def test_create_team(client, auth_headers):
    """Test membuat tim baru (Happy Path)."""
    payload = {
        "teamID": 1,
        "name": "Ferrari",
        "members": ["Leclerc"],
        "inventory": [],
        "sponsors": []
    }
    response = client.post("/teams/", json=payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Ferrari"
    assert response.json()["teamID"] == 1

def test_get_team_success(client, auth_headers):
    """Test mengambil data tim yang ada."""
    # Create first
    client.post("/teams/", json={"teamID": 1, "name": "Ferrari"}, headers=auth_headers)
    # Get
    response = client.get("/teams/1", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Ferrari"

def test_get_team_not_found(client, auth_headers):
    """Error: Mengambil tim yang tidak ada (404)."""
    response = client.get("/teams/999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Team not found"

# ==========================================
# 3. ENGINEER MANAGEMENT TESTS
# ==========================================

def test_create_schedule_success(client, auth_headers):
    """Test membuat jadwal engineer (Happy Path)."""
    payload = {
        "engineerID": 101,
        "taskDescription": "Check Tyres",
        "date": "2025-10-10",
        "startTime": "09:00:00",
        "endTime": "10:00:00",
        "location": "Garage",
        "raceID": 1
    }
    response = client.post("/engineer_management/schedules/", json=payload, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["taskDescription"] == "Check Tyres"
    assert response.json()["scheduleID"] is not None

def test_create_schedule_invalid_time(client, auth_headers):
    """Edge Case: Waktu mulai lebih besar dari waktu selesai."""
    payload = {
        "engineerID": 101,
        "taskDescription": "Error Task",
        "date": "2025-10-10",
        "startTime": "12:00:00",
        "endTime": "11:00:00", # Error disini
        "location": "Garage"
    }
    response = client.post("/engineer_management/schedules/", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert "Waktu mulai harus sebelum waktu selesai" in response.json()["detail"]

def test_create_duplicate_schedule_id(client, auth_headers):
    """Edge Case: ID Jadwal duplikat (Manual ID input)."""
    payload = {
        "scheduleID": 1,
        "engineerID": 101,
        "taskDescription": "Task 1",
        "date": "2025-10-10",
        "startTime": "09:00:00",
        "endTime": "10:00:00",
        "location": "Garage"
    }
    client.post("/engineer_management/schedules/", json=payload, headers=auth_headers)
    # Post lagi dengan ID sama
    response = client.post("/engineer_management/schedules/", json=payload, headers=auth_headers)
    assert response.status_code == 400
    assert "sudah ada" in response.json()["detail"]

def test_update_schedule_success(client, auth_headers):
    """Test update jadwal."""
    # Create
    payload = {
        "engineerID": 101, "taskDescription": "Old Task", 
        "date": "2025-10-10", "startTime": "09:00:00", "endTime": "10:00:00", "location": "Garage"
    }
    create_res = client.post("/engineer_management/schedules/", json=payload, headers=auth_headers)
    sch_id = create_res.json()["scheduleID"]

    # Update
    update_payload = payload.copy()
    update_payload["taskDescription"] = "New Task"
    response = client.put(f"/engineer_management/schedules/{sch_id}", json=update_payload, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["taskDescription"] == "New Task"

def test_update_schedule_not_found(client, auth_headers):
    """Error: Update jadwal yang tidak ada."""
    payload = {
        "engineerID": 101, "taskDescription": "Task", 
        "date": "2025-10-10", "startTime": "09:00:00", "endTime": "10:00:00", "location": "Garage"
    }
    response = client.put("/engineer_management/schedules/999", json=payload, headers=auth_headers)
    assert response.status_code == 404

def test_update_schedule_invalid_time(client, auth_headers):
    """Error: Update jadwal dengan waktu invalid."""
    # Create
    payload = {
        "engineerID": 101, "taskDescription": "Task", 
        "date": "2025-10-10", "startTime": "09:00:00", "endTime": "10:00:00", "location": "Garage"
    }
    create_res = client.post("/engineer_management/schedules/", json=payload, headers=auth_headers)
    sch_id = create_res.json()["scheduleID"]
    
    # Update Invalid
    payload["startTime"] = "13:00:00"
    payload["endTime"] = "12:00:00"
    response = client.put(f"/engineer_management/schedules/{sch_id}", json=payload, headers=auth_headers)
    assert response.status_code == 400

def test_get_schedules_by_engineer(client, auth_headers):
    """Test filter jadwal berdasarkan engineer ID."""
    # Create for Eng 101
    client.post("/engineer_management/schedules/", json={
        "engineerID": 101, "taskDescription": "Task A", 
        "date": "2025-10-10", "startTime": "09:00:00", "endTime": "10:00:00", "location": "Garage"
    }, headers=auth_headers)
    # Create for Eng 102
    client.post("/engineer_management/schedules/", json={
        "engineerID": 102, "taskDescription": "Task B", 
        "date": "2025-10-10", "startTime": "09:00:00", "endTime": "10:00:00", "location": "Garage"
    }, headers=auth_headers)

    response = client.get("/engineer_management/schedules/engineer/101", headers=auth_headers)
    data = response.json()
    assert len(data) == 1
    assert data[0]["engineerID"] == 101

# ==========================================
# 4. RACE STRATEGY & REPORT TESTS
# ==========================================

def test_race_strategy_workflow(client, auth_headers):
    """Workflow: Create Strategy -> Get Strategy -> Update Plan."""
    # 1. Create
    payload = {
        "race": {
            "raceID": 50, "circuitName": "Spa", "date": "2025-08-01", "weather": "Rain",
            "result": ["P1: Max (RedBull)"]
        },
        "strategyPlan": {
            "pitStopSchedule": [10], "tyreStrategy": ["Wet"], "fuelPlan": "Conservative"
        },
        "liveTelemetry": {"speed": 300, "rpm": 12000, "temperature": 90}
    }
    res_create = client.post("/race_strategy/", json=payload, headers=auth_headers)
    assert res_create.status_code == 200

    # 2. Get
    res_get = client.get("/race_strategy/50", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.json()["race"]["circuitName"] == "Spa"

    # 3. Update Plan
    new_plan = {
        "pitStopSchedule": [15, 30], "tyreStrategy": ["Inter", "Slick"], "fuelPlan": "Push"
    }
    res_put = client.put("/race_strategy/50/plan", json=new_plan, headers=auth_headers)
    assert res_put.status_code == 200
    assert res_put.json()["strategyPlan"]["fuelPlan"] == "Push"

def test_get_race_strategy_not_found(client, auth_headers):
    res = client.get("/race_strategy/999", headers=auth_headers)
    assert res.status_code == 404

def test_update_race_strategy_not_found(client, auth_headers):
    plan = {"pitStopSchedule": [], "tyreStrategy": [], "fuelPlan": "X"}
    res = client.put("/race_strategy/999/plan", json=plan, headers=auth_headers)
    assert res.status_code == 404

def test_report_generation_success(client, auth_headers):
    """Test Generate Report Otomatis (Happy Path)."""
    # Setup: Harus ada Team dan Race Strategy dulu
    client.post("/teams/", json={"teamID": 1, "name": "RedBull"}, headers=auth_headers)
    
    race_payload = {
        "race": {
            "raceID": 50, "circuitName": "Spa", "date": "2025-08-01", "weather": "Rain",
            "result": ["P1: Max (RedBull)"]
        },
        "strategyPlan": {"pitStopSchedule": [], "tyreStrategy": [], "fuelPlan": ""},
        "liveTelemetry": {"speed": 0, "rpm": 0, "temperature": 0}
    }
    client.post("/race_strategy/", json=race_payload, headers=auth_headers)

    # Generate Report
    response = client.post("/report_system/generate/50", headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert "RedBull" in data["raceSummary"]
    assert "RedBull" in data["teamPerformanceAnalysis"]

def test_report_generation_race_not_found(client, auth_headers):
    """Error: Generate report untuk race yang belum dibuat."""
    response = client.post("/report_system/generate/999", headers=auth_headers)
    assert response.status_code == 404

def test_report_generation_duplicate(client, auth_headers):
    """Error: Generate report dua kali untuk race yang sama."""
    # Setup
    race_payload = {
        "race": {"raceID": 50, "circuitName": "Spa", "date": "2025-08-01", "weather": "Rain", "result": []},
        "strategyPlan": {"pitStopSchedule": [], "tyreStrategy": [], "fuelPlan": ""},
        "liveTelemetry": {"speed": 0, "rpm": 0, "temperature": 0}
    }
    client.post("/race_strategy/", json=race_payload, headers=auth_headers)
    
    # 1st Generate
    client.post("/report_system/generate/50", headers=auth_headers)
    # 2nd Generate (Should Fail)
    response = client.post("/report_system/generate/50", headers=auth_headers)
    assert response.status_code == 400
    assert "sudah ada" in response.json()["detail"]

def test_get_report_success(client, auth_headers):
    """Test mengambil report yang sudah digenerate."""
    # Setup
    race_payload = {
        "race": {"raceID": 50, "circuitName": "Spa", "date": "2025-08-01", "weather": "Rain", "result": []},
        "strategyPlan": {"pitStopSchedule": [], "tyreStrategy": [], "fuelPlan": ""},
        "liveTelemetry": {"speed": 0, "rpm": 0, "temperature": 0}
    }
    client.post("/race_strategy/", json=race_payload, headers=auth_headers)
    res_gen = client.post("/report_system/generate/50", headers=auth_headers)
    report_id = res_gen.json()["reportID"]

    # Get
    response = client.get(f"/report_system/{report_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["raceID"] == 50

def test_get_report_not_found(client, auth_headers):
    response = client.get("/report_system/999", headers=auth_headers)
    assert response.status_code == 404

# ==========================================
# 5. DRIVER PERFORMANCE TESTS
# ==========================================
def test_driver_performance_workflow(client, auth_headers):
    # Create
    payload = {
        "driver": {"driverID": 1, "name": "Lewis", "driverAbb": "HAM", "nationality": "UK", "physicalCondition": "Fit"},
        "lapTimes": [{"minutes": 1, "seconds": 30, "milliseconds": 500}],
        "liveTelemetry": {"speed": 320, "rpm": 11000, "temperature": 100}
    }
    res = client.post("/driver_performance/", json=payload, headers=auth_headers)
    assert res.status_code == 200
    
    # Get
    res_get = client.get("/driver_performance/1", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.json()["driver"]["name"] == "Lewis"

def test_get_driver_performance_not_found(client, auth_headers):
    res = client.get("/driver_performance/999", headers=auth_headers)
    assert res.status_code == 404

