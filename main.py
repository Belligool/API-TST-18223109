from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta
import os
from jose import JWTError, jwt

from models import (
    Driver, Team, Race, StrategyPlan, RaceStrategy, 
    DriverPerformance, LapTime, TelemetryData,
    User, UserInDB, Token, TokenData
)

from auth import (
    verify_password, get_password_hash, create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES, JWTError, SECRET_KEY, ALGORITHM
)

INITIAL_USER = os.getenv("ADMIN_USERNAME", "admin")
INITIAL_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_password")
INITIAL_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

app = FastAPI()

db_teams = {}
db_drivers = {}
db_race_strategies = {}
db_driver_performance = {}
users_db = {
    "jake": {
        "username": INITIAL_USER,
        "full_name": "Jake Benham",
        "email": INITIAL_EMAIL,
        "hashed_password": get_password_hash(INITIAL_PASSWORD),
        "disabled": False,
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    for user_data in db.values():
        if user_data["username"] == username:
            return UserInDB(**user_data)
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


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