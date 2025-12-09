from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Dict, List
import os

from auth import SECRET_KEY, ALGORITHM, get_password_hash
from models import User, UserInDB, TokenData, Team, Driver, RaceStrategy, DriverPerformance

db_teams: Dict[int, Team] = {}
db_drivers: Dict[int, Driver] = {}
db_race_strategies: Dict[int, RaceStrategy] = {}
db_driver_performance: Dict[int, DriverPerformance] = {}

INITIAL_USER = os.getenv("ADMIN_USERNAME", "admin")
INITIAL_PASSWORD = os.getenv("ADMIN_PASSWORD", "default_password")
INITIAL_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

users_db = {
    "jake": {
        "username": "jbenham", 
        "full_name": "Jake Benham",
        "email": "jakebenham@f1system.com",
        "hashed_password": get_password_hash("opmeersucks"),
        "disabled": False,
    }
}

if INITIAL_USER not in users_db:
    users_db[INITIAL_USER] = {
        "username": INITIAL_USER,
        "full_name": "Admin User",
        "email": INITIAL_EMAIL,
        "hashed_password": get_password_hash(INITIAL_PASSWORD),
        "disabled": False,
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