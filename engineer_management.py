from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict
from models import EngineerSchedule, User
from dependencies import get_current_user

router = APIRouter(
    prefix="/engineer_management",
    tags=["Engineer Management"]
)

db_engineer_schedules: Dict[int, EngineerSchedule] = {}
next_schedule_id = 1

@router.post("/schedules/", response_model=EngineerSchedule, status_code=status.HTTP_201_CREATED)
def create_engineer_schedule(schedule: EngineerSchedule, current_user: User = Depends(get_current_user)):
    global next_schedule_id
    
    if schedule.scheduleID is None:
        schedule.scheduleID = next_schedule_id
        
    if schedule.scheduleID in db_engineer_schedules:
        raise HTTPException(status_code=400, detail=f"Schedule ID {schedule.scheduleID} sudah ada")
        
    if schedule.startTime >= schedule.endTime:
         raise HTTPException(status_code=400, detail="Waktu mulai harus sebelum waktu selesai.")

    db_engineer_schedules[schedule.scheduleID] = schedule
    next_schedule_id += 1
    return schedule

@router.get("/schedules/", response_model=List[EngineerSchedule])
def get_all_schedules(current_user: User = Depends(get_current_user)):
    return list(db_engineer_schedules.values())

@router.get("/schedules/engineer/{engineer_id}", response_model=List[EngineerSchedule])
def get_schedules_by_engineer(engineer_id: int, current_user: User = Depends(get_current_user)):
    schedules = [
        schedule for schedule in db_engineer_schedules.values() 
        if schedule.engineerID == engineer_id
    ]
    return schedules

@router.put("/schedules/{schedule_id}", response_model=EngineerSchedule)
def update_engineer_schedule(schedule_id: int, updated_schedule: EngineerSchedule, current_user: User = Depends(get_current_user)):
    if schedule_id not in db_engineer_schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jadwal tidak ditemukan")

    if updated_schedule.startTime >= updated_schedule.endTime:
         raise HTTPException(status_code=400, detail="Waktu mulai harus sebelum waktu selesai.")

    updated_schedule.scheduleID = schedule_id
    db_engineer_schedules[schedule_id] = updated_schedule
    return updated_schedule