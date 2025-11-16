from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# value object

class LapTime(BaseModel):
    minutes: int
    seconds: int
    milliseconds: int

class TyreSet(BaseModel):
    tyreType: str
    wearLevel: float
    age: int

class FuelStatus(BaseModel):
    fuelLevel: float
    fuelEfficiency: float

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
    sponsorName: int
    contractValue: float

class Driver(BaseModel):
    driverID: int
    name: str
    driverAbb: str
    nationality: str
    physicalCondition: str

class Car(BaseModel):
    carID: int
    model: str
    engineManufacturer: str
    telemetryData: TelemetryData

class Race(BaseModel):
    raceID: int
    circuitName: str
    date: date
    weather: str
    result: Optional[List[str]] = []

class Team(BaseModel):
    teamID: int
    name: str
    members: Optional[List[str]] = []
    inventory: Optional[List[InventoryItem]] = []
    sponsors: Optional[List[Sponsor]] = []
    drivers: Optional[List[Driver]] = []

# model buat aggregates
class RaceStrategy(BaseModel):
    race: Race
    strategyPlan: StrategyPlan
    liveTelemetry: TelemetryData

class DriverPerformance(BaseModel):
    driver: Driver
    lapTimes: List[LapTime]
    liveTelemetry: TelemetryData