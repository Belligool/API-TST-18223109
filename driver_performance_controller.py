from fastapi import APIRouter, HTTPException, Depends, status
from models import DriverPerformance, User
from dependencies import get_current_user, db_driver_performance

router = APIRouter(
    prefix="/driver_performance",
    tags=["Driver Performance"]
)

@router.post("/", response_model=DriverPerformance)
def create_driver_performance_record(record: DriverPerformance, current_user: User = Depends(get_current_user)):
    db_driver_performance[record.driver.driverID] = record
    return record

@router.get("/{driver_id}", response_model=DriverPerformance)
def get_driver_performance(driver_id: int):
    record = db_driver_performance.get(driver_id)
    if not record:
        raise HTTPException(status_code=404, detail="Driver performance data not found")
    return record