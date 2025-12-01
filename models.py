from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# value objects
class LapTime(BaseModel):
    minutes: int
    seconds: int
    milliseconds: int

class TyreSet(BaseModel):
    tyreType: str
    wearLevel: float
    age: int

class TelemetryData(BaseModel):
    speed: float
    rpm: int
    temperature: float

class StrategyPlan(BaseModel):
    pitStopSchedule: List[int]
    tyreStrategy: List[str]
    fuelPlan: str

# entity
class InventoryItem(BaseModel):
    itemID: int
    partName: str
    quantity: int
    status: str

class Sponsor(BaseModel):
    sponsorID: int
    sponsorName: str
    contractValue: float

class Engineer(BaseModel):
    engineerID: int
    name: str
    role: str

class Driver(BaseModel):
    driverID: int
    name: str
    driverAbb: str
    nationality: str
    physicalCondition: str

class Race(BaseModel):
    raceID: int
    circuitName: str
    date: date
    weather: str
    result: Optional[List[str]] = []

# aggregates
class Team(BaseModel):
    teamID: int
    name: str
    members: Optional[List[str]] = []
    inventory: Optional[List[InventoryItem]] = []
    sponsors: Optional[List[Sponsor]] = []
    engineers: Optional[List[Engineer]] = []
    drivers: Optional[List[Driver]] = []

class RaceStrategy(BaseModel):
    race: Race
    strategyPlan: StrategyPlan
    liveTelemetry: TelemetryData

class DriverPerformance(BaseModel):
    driver: Driver
    lapTimes: List[LapTime]
    liveTelemetry: TelemetryData

# auth stuff
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None