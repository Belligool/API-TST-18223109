from fastapi import FastAPI, HTTPException
from typing import List

from models import (
    Driver, Team, Race, StrategyPlan, RaceStrategy, 
    DriverPerformance, LapTime, TelemetryData
)

app = FastAPI()

db_teams = {}
db_drivers = {}
db_race_strategies = {}
db_driver_performance = {}

@app.post("/teams/", response_model=Team)
def create_team(team: Team):
    db_teams[team.teamID] = team
    return team

@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    team = db_teams.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.post("/driver_performance/", response_model=DriverPerformance)
def create_driver_performance_record(record: DriverPerformance):
    db_driver_performance[record.driver.driverID] = record
    return record

@app.get("/driver_performance/{driver_id}", response_model=DriverPerformance)
def get_driver_performance(driver_id: int):
    record = db_driver_performance.get(driver_id)
    if not record:
        raise HTTPException(status_code=404, detail="Driver performance data not found")
    return record

@app.post("/race_strategy/", response_model=RaceStrategy)
def create_race_strategy(strategy: RaceStrategy):
    db_race_strategies[strategy.race.raceID] = strategy
    return strategy

@app.get("/race_strategy/{race_id}", response_model=RaceStrategy)
def get_race_strategy(race_id: int):
    strategy = db_race_strategies.get(race_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Race strategy not found")
    return strategy

@app.put("/race_strategy/{race_id}/plan", response_model=RaceStrategy)
def update_strategy_plan(race_id: int, plan: StrategyPlan):
    strategy = db_race_strategies.get(race_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Race strategy not found")
    
    strategy.strategyPlan = plan
    db_race_strategies[race_id] = strategy
    return strategy