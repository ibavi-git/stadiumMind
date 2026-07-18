from fastapi import APIRouter, HTTPException
from data_loader import data_loader
from services.task_service import TaskService
from models.request_models import TaskAssignRequest
from models.response_models import TaskAssignmentResponse
from gemini_service import gemini_service
import json
from datetime import datetime

router = APIRouter(prefix='/api/volunteers', tags=['Volunteers'])
task_service = TaskService()

@router.get('/')
def get_volunteers():
    return data_loader.get_volunteers()

@router.get('/gaps')
def get_gaps():
    return task_service.get_deployment_gaps(data_loader.get_volunteers())

@router.get('/zone/{zone_id}')
def get_zone_volunteers(zone_id: str):
    return [v for v in data_loader.get_volunteers().get('volunteers', []) if v.get('zone') == zone_id]

@router.get('/{volunteer_id}')
def get_volunteer(volunteer_id: str):
    vol = next((v for v in data_loader.get_volunteers().get('volunteers', []) if v.get('id') == volunteer_id), None)
    if not vol:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return vol

@router.post('/tasks', response_model=TaskAssignmentResponse)
def assign_tasks(request: TaskAssignRequest):
    v_data = data_loader.get_volunteers()
    c_data = data_loader.get_crowd()
    unassigned = task_service.get_available_volunteers(v_data)
    critical = task_service.get_priority_zones(c_data)
    
    prompt = f"""Assign the following unassigned volunteers to the critical zones.
Unassigned Volunteers: {json.dumps(unassigned)}
Critical Zones: {json.dumps(critical)}

Return a JSON array of assignment objects with keys: volunteer_id, zone, task, priority, estimated_minutes, reasoning, suggested_response
Do not use markdown fences.
"""
    try:
        ai_assignments = gemini_service.generate_json(prompt)
    except Exception:
        ai_assignments = []
        
    assignments = task_service.build_task_assignments(
        c_data, v_data, data_loader.get_incidents(), ai_assignments
    )
    
    return TaskAssignmentResponse(
        assignments=assignments,
        ai_summary="Generated assignments based on crowd density",
        total_volunteers_deployed=len(assignments),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
