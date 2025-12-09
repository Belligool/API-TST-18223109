from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import List

from auth import (
    verify_password, create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from models import (
    Driver, Team, Race, StrategyPlan, RaceStrategy,
    DriverPerformance, User, Token
)

from dependencies import (
    get_current_user, get_user, 
    db_teams, db_drivers, db_race_strategies, db_driver_performance, users_db,
    INITIAL_USER
)

from engineer_management import router as engineer_router
from report_system import router as report_router

app = FastAPI()

app.include_router(engineer_router)
app.include_router(report_router)

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/teams/", response_model=Team)
def create_team(team: Team, current_user: User = Depends(get_current_user)):
    db_teams[team.teamID] = team
    return team

@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    team = db_teams.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.post("/driver_performance/", response_model=DriverPerformance)
def create_driver_performance_record(record: DriverPerformance, current_user: User = Depends(get_current_user)):
    db_driver_performance[record.driver.driverID] = record
    return record

@app.get("/driver_performance/{driver_id}", response_model=DriverPerformance)
def get_driver_performance(driver_id: int):
    record = db_driver_performance.get(driver_id)
    if not record:
        raise HTTPException(status_code=404, detail="Driver performance data not found")
    return record

@app.post("/race_strategy/", response_model=RaceStrategy)
def create_race_strategy(strategy: RaceStrategy, current_user: User = Depends(get_current_user)):
    db_race_strategies[strategy.race.raceID] = strategy
    return strategy

@app.get("/race_strategy/{race_id}", response_model=RaceStrategy)
def get_race_strategy(race_id: int):
    strategy = db_race_strategies.get(race_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Race strategy not found")
    return strategy

@app.put("/race_strategy/{race_id}/plan", response_model=RaceStrategy)
def update_strategy_plan(race_id: int, plan: StrategyPlan, current_user: User = Depends(get_current_user)):
    strategy = db_race_strategies.get(race_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Race strategy not found")
    
    strategy.strategyPlan = plan
    db_race_strategies[race_id] = strategy
    return strategy