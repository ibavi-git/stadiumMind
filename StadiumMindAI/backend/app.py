from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from data_loader import data_loader
from routes.crowd import router as crowd_router
from routes.volunteers import router as volunteer_router
from routes.incidents import router as incident_router
from routes.dashboard import router as dashboard_router

from models.request_models import AskRequest, TranslateRequest, EmergencyRequest
from models.response_models import AIResponse, TranslationResponse, EmergencyResponseModel
from gemini_service import gemini_service
from prompts.volunteer_prompt import build_volunteer_prompt
from prompts.translation_prompt import build_translation_prompt
from prompts.emergency_prompt import build_emergency_prompt

@asynccontextmanager
async def lifespan(app: FastAPI):
    data_loader.get_full_context()
    yield

app = FastAPI(title='StadiumMind AI', version='1.0.0', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173','http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ai_router = APIRouter(prefix='/api/ai', tags=['AI Services'])

@ai_router.post('/ask', response_model=AIResponse)
def ask_question(req: AskRequest):
    prompt = build_volunteer_prompt(data_loader.get_full_context(), req.question, req.volunteer_id, req.language)
    try:
        ans = gemini_service.generate(prompt)
        return AIResponse(
            answer=ans,
            confidence="High",
            sources_used=["Stadium", "Crowd", "Volunteers"],
            reasoning_summary="Based on real-time stadium context.",
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@ai_router.post('/translate', response_model=TranslationResponse)
def translate(req: TranslateRequest):
    prompt = build_translation_prompt(req.text, req.target_language, req.context_type, data_loader.get_full_context())
    res = gemini_service.generate_json(prompt)
    return TranslationResponse(
        original=req.text,
        translated=res.get("translated", ""),
        target_language=req.target_language,
        context_notes=res.get("context_notes", ""),
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@ai_router.get('/health')
def ai_health():
    return {"status": "ok"}

app.include_router(ai_router)
app.include_router(crowd_router)
app.include_router(volunteer_router)
app.include_router(incident_router)
app.include_router(dashboard_router)

@app.get('/')
def read_root():
    return {
        "name": "StadiumMind AI",
        "version": "1.0.0",
        "tagline": "AI Backend for FIFA 2026",
        "status": "online",
        "docs": "/docs"
    }

@app.get('/health')
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": "gemini-2.5-flash",
        "context_sources": ["stadium", "crowd", "transport", "volunteers", "incidents", "match"]
    }