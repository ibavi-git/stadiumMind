from fastapi import APIRouter, HTTPException
from data_loader import data_loader
from services.crowd_service import CrowdService

router = APIRouter(prefix='/api/crowd', tags=['Crowd Intelligence'])
crowd_service = CrowdService()

@router.get('/')
def get_crowd():
    return crowd_service.get_heatmap_data(
        data_loader.get_crowd(),
        data_loader.get_stadium(),
        data_loader.get_volunteers()
    )

@router.get('/heatmap')
def get_heatmap():
    return get_crowd()

@router.get('/zone/{zone_id}')
def get_zone(zone_id: str):
    res = crowd_service.get_zone_summary(zone_id, data_loader.get_crowd())
    if not res:
        raise HTTPException(status_code=404, detail="Zone not found")
    return res

@router.get('/alerts')
def get_alerts():
    return data_loader.get_crowd().get('congestion_alerts', [])

@router.get('/stats')
def get_stats():
    return crowd_service.calculate_overall_stats(data_loader.get_crowd())
