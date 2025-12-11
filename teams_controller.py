from fastapi import APIRouter, HTTPException, Depends, status
from models import Team, User
from dependencies import get_current_user, db_teams

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.post("/", response_model=Team)
def create_team(team: Team, current_user: User = Depends(get_current_user)):
    db_teams[team.teamID] = team
    return team

@router.get("/{team_id}", response_model=Team)
def get_team(team_id: int, current_user: User = Depends(get_current_user)):
    team = db_teams.get(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team