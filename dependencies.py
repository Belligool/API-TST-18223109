from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Dict
import os
from dotenv import load_dotenv

from auth import SECRET_KEY, ALGORITHM, get_password_hash
from models import UserInDB, TokenData, Team, Driver, RaceStrategy, DriverPerformance

load_dotenv()

db_teams: Dict[int, Team] = {}
db_drivers: Dict[int, Driver] = {}
db_race_strategies: Dict[int, RaceStrategy] = {}
db_driver_performance: Dict[int, DriverPerformance] = {}

admin_user = os.getenv("ADMIN_USERNAME")
admin_pass = os.getenv("ADMIN_PASSWORD")
admin_email = os.getenv("ADMIN_EMAIL")
admin_fullname = os.getenv("ADMIN_FULL_NAME", "System Admin") 

users_db = {}

if admin_user and admin_pass:
    users_db[admin_user] = {
        "username": admin_user,
        "full_name": admin_fullname,
        "email": admin_email,
        "hashed_password": get_password_hash(admin_pass),
        "disabled": False,
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
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