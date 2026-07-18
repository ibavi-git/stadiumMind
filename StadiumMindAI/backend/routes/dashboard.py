from fastapi import APIRouter
from data_loader import data_loader
from models.response_models import DashboardSummary
from gemini_service import gemini_service
from prompts.organizer_prompt import build_organizer_insights_prompt
from services.crowd_service import CrowdService
from services.task_service import TaskService
from services.emergency_service import EmergencyService
from datetime import datetime

router = APIRouter(prefix='/api/dashboard', tags=['Organizer Dashboard'])
crowd_service = CrowdService()
task_service = TaskService()
emergency_service = EmergencyService()

@router.get('/summary', response_model=DashboardSummary)
def get_summary():
    context = data_loader.get_full_context()
    prompt = build_organizer_insights_prompt(context)
    
    try:
        insights = gemini_service.generate_json(prompt)
    except Exception:
        insights = []
        
    c_data = data_loader.get_crowd()
    v_data = data_loader.get_volunteers()
    i_data = data_loader.get_incidents()
    
    overall_attendance = crowd_service.calculate_overall_stats(c_data).get('overall_attendance', 0)
    stadium_cap = data_loader.get_stadium().get('capacity', 80000)
    capacity_percent = (overall_attendance / stadium_cap * 100) if stadium_cap > 0 else 0
    
    active_incidents = len(emergency_service.get_active_incidents(i_data))
    
    volunteers_active = len([v for v in v_data.get('volunteers', []) if v.get('status') == 'ACTIVE'])
    volunteers_unassigned = len([v for v in v_data.get('volunteers', []) if v.get('status') == 'UNASSIGNED'])
    
    critical_zones = crowd_service.get_critical_zones(c_data)
    
    return DashboardSummary(
        overall_attendance=overall_attendance,
        overall_capacity_percent=capacity_percent,
        active_incidents=active_incidents,
        volunteers_active=volunteers_active,
        volunteers_unassigned=volunteers_unassigned,
        critical_zones=critical_zones,
        ai_insights=insights,
        top_priority_action="Review AI Insights",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@router.get('/match')
def get_match():
    return data_loader.get_match()

@router.get('/kpis')
def get_kpis():
    c_data = data_loader.get_crowd()
    v_data = data_loader.get_volunteers()
    i_data = data_loader.get_incidents()
    match = data_loader.get_match()
    
    overall_attendance = crowd_service.calculate_overall_stats(c_data).get('overall_attendance', 0)
    stadium_cap = data_loader.get_stadium().get('capacity', 80000)
    capacity_percent = (overall_attendance / stadium_cap * 100) if stadium_cap > 0 else 0
    
    return {
        "attendance": overall_attendance,
        "capacity_percent": capacity_percent,
        "active_incidents": len(emergency_service.get_active_incidents(i_data)),
        "volunteers_active": len([v for v in v_data.get('volunteers', []) if v.get('status') == 'ACTIVE']),
        "volunteers_on_break": len([v for v in v_data.get('volunteers', []) if v.get('status') == 'ON_BREAK']),
        "volunteers_unassigned": len([v for v in v_data.get('volunteers', []) if v.get('status') == 'UNASSIGNED']),
        "critical_zones_count": len(crowd_service.get_critical_zones(c_data)),
        "weather_condition": emergency_service.get_weather_advisory(i_data).get('condition', 'Clear'),
        "match_phase": match.get('match_phase', 'Pre-Match')
    }
