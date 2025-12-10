from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from models import Token, User
from auth import (
    verify_password, create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)

from dependencies import get_user, users_db

from teams_controller import router as teams_router
from driver_performance_controller import router as driver_perf_router
from race_strategy_controller import router as race_strat_router
from engineer_management import router as engineer_router
from report_system import router as report_router

app = FastAPI()

app.include_router(teams_router)
app.include_router(driver_perf_router)
app.include_router(race_strat_router)
app.include_router(engineer_router)
app.include_router(report_router)

@app.post("/token", response_model=Token, tags=["Authentication"])
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