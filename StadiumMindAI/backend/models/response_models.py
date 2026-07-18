from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class AIResponse(BaseModel):
    answer: str
    confidence: str
    sources_used: list[str]
    reasoning_summary: str
    timestamp: str

class TranslationResponse(BaseModel):
    original: str
    translated: str
    target_language: str
    context_notes: str
    timestamp: str

class EmergencyResponseModel(BaseModel):
    emergency_type: str
    zone: str
    severity: str
    volunteer_instructions: list[str]
    public_announcement: str
    organizer_recommendations: list[str]
    evacuation_guidance: Optional[str] = None
    timestamp: str

class TaskAssignment(BaseModel):
    volunteer_id: str
    volunteer_name: str
    zone: str
    task: str
    priority: str
    estimated_minutes: int
    reasoning: str
    suggested_response: str

class TaskAssignmentResponse(BaseModel):
    assignments: list[TaskAssignment]
    ai_summary: str
    total_volunteers_deployed: int
    timestamp: str

class ZoneMetric(BaseModel):
    zone_id: str
    label: str
    density_percent: float
    status: str
    congestion_risk: str
    volunteer_count: int
    recommended_volunteers: int
    gap: int
    queue_length: int
    wait_minutes: int

class DashboardSummary(BaseModel):
    overall_attendance: int
    overall_capacity_percent: float
    active_incidents: int
    volunteers_active: int
    volunteers_unassigned: int
    critical_zones: list[str]
    ai_insights: list[dict]
    top_priority_action: str
    timestamp: str

class IncidentResponse(BaseModel):
    id: str
    type: str
    severity: str
    zone: str
    description: str
    status: str
    assigned_volunteers: list[str]
    ai_recommended_actions: list[str]
    reported_at: str
