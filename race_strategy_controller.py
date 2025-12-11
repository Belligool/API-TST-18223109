from fastapi import APIRouter, HTTPException, Depends, status
from models import RaceStrategy, StrategyPlan, User
from dependencies import get_current_user, db_race_strategies

router = APIRouter(
    prefix="/race_strategy",
    tags=["Race Strategy"]
)

@router.post("/", response_model=RaceStrategy)
def create_race_strategy(strategy: RaceStrategy, current_user: User = Depends(get_current_user)):
    db_race_strategies[strategy.race.raceID] = strategy
    return strategy

@router.get("/{race_id}", response_model=RaceStrategy)
def get_race_strategy(race_id: int, current_user: User = Depends(get_current_user)):
    strategy = db_race_strategies.get(race_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Race strategy not found")
    return strategy

@router.put("/{race_id}/plan", response_model=RaceStrategy)
def update_strategy_plan(race_id: int, plan: StrategyPlan, current_user: User = Depends(get_current_user)):
    strategy = db_race_strategies.get(race_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Race strategy not found")
    
    strategy.strategyPlan = plan
    db_race_strategies[race_id] = strategy
    return strategy