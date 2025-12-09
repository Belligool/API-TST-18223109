from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict
from datetime import datetime
from models import RaceReport, Race, User
from dependencies import get_current_user, db_race_strategies, db_teams 

router = APIRouter(
    prefix="/report_system",
    tags=["Report System"]
)

db_race_reports: Dict[int, RaceReport] = {}
next_report_id = 1

def simulate_report_generation(race: Race) -> RaceReport:
    global next_report_id

    if not race.result:
        summary = f"Balapan di {race.circuitName} ({race.date}) belum memiliki hasil akhir yang terekam."
        key_incidents = ["Tidak ada insiden tercatat (balapan belum selesai/data kurang)."]
        team_analysis = {}
    else:
        winner_entry = race.result[0]
        winner = winner_entry.split(':')[1].split('(')[0].strip()
        winning_team = winner_entry.split('(')[1].strip(')')
        
        summary = f"Race Report: {winner} dari tim {winning_team} memenangkan balapan di {race.circuitName} pada {race.date}. Cuaca: {race.weather}."
        
        key_incidents = ["Start bersih tanpa insiden besar."]
        if "Rain" in race.weather or "Wet" in race.weather:
             key_incidents.append("Kondisi lintasan basah pada awal balapan memengaruhi strategi ban.")
        
        team_analysis = {}
        all_teams = db_teams.values()
        for team in all_teams:
            team_drivers_in_result = [r for r in race.result if f"({team.name})" in r]
            
            if team_drivers_in_result:
                best_pos_index = min([race.result.index(r) for r in team_drivers_in_result])
                best_driver_result = race.result[best_pos_index]
                best_driver_pos = best_pos_index + 1
                
                analysis_text = f"Performa tim **{team.name}** solid. Hasil terbaik P{best_driver_pos} dicapai oleh {best_driver_result.split(':')[1].split('(')[0].strip()}. Tim berhasil mengumpulkan poin penting."
            else:
                analysis_text = f"Tim **{team.name}** tidak tercatat di hasil akhir balapan (DNF/Di luar Poin). Perlu evaluasi strategi/kendaraan."

            team_analysis[team.name] = analysis_text


    new_report = RaceReport(
        reportID=next_report_id,
        raceID=race.raceID,
        raceSummary=summary,
        teamPerformanceAnalysis=team_analysis,
        keyIncidents=key_incidents,
        generatedDate=datetime.now()
    )
    
    return new_report

@router.post("/generate/{race_id}", response_model=RaceReport, status_code=status.HTTP_201_CREATED)
def generate_race_report(race_id: int, current_user: User = Depends(get_current_user)):
    global next_report_id

    race_strategy = db_race_strategies.get(race_id)
    if not race_strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Race dengan ID {race_id} tidak ditemukan.")
    
    race = race_strategy.race

    if any(r.raceID == race_id for r in db_race_reports.values()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Laporan untuk Race ID {race_id} sudah ada.")
        
    report = simulate_report_generation(race)
    db_race_reports[report.reportID] = report
    next_report_id += 1
    
    return report

@router.get("/{report_id}", response_model=RaceReport)
def get_race_report(report_id: int, current_user: User = Depends(get_current_user)):
    report = db_race_reports.get(report_id)
    if not report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Laporan tidak ditemukan")
    return report