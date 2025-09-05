import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

# =========================
# Import routers existentes
# =========================
from app.api import stream
from app.api.routes_session import router as session_router
from app.api.routes_voice import router as voice_router
from app.api.routes_translate import router as translate_router
from app.api.routes_integrations import router as integrations_router
from app.api import voice_catalog_routes, voice_mapping_routes

# =========================
# Import UserSettingsManager
# =========================
from app.user_settings.manager import UserSettingsManager

# =========================
# Import Auth routes seguros
# =========================
from app.routes.auth_crypto import router as auth_router  # Atualizado para CRUD criptografado

# =========================
# FastAPI app
# =========================
app = FastAPI(title="LYZOR Realtime Translation + Voice Clone")

# =========================
# Middleware
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Routers existentes
# =========================
app.include_router(stream.router, prefix="/ws")
app.include_router(session_router, prefix="/api/session", tags=["session"])
app.include_router(voice_router, prefix="/api/voice", tags=["voice"])
app.include_router(translate_router, prefix="/api/translate", tags=["translate"])
app.include_router(integrations_router, prefix="/api/integration", tags=["integration"])
app.include_router(voice_catalog_routes.router, prefix="/api/voice_catalog", tags=["voice_catalog"])
app.include_router(voice_mapping_routes.router, prefix="/api/voice_mapping", tags=["voice_mapping"])

# =========================
# Auth routes seguros (Google/Microsoft/Phone)
# =========================
app.include_router(auth_router, prefix="/api", tags=["auth"])

# =========================
# Voice directory
# =========================
VOICE_DIR = os.path.join(os.path.dirname(__file__), "voices")
os.makedirs(VOICE_DIR, exist_ok=True)
default_speaker_wav = os.path.join(VOICE_DIR, "default_clone.wav")

def get_user_voice(user_id: str):
    path = os.path.join(VOICE_DIR, f"{user_id}_clone.wav")
    return path if os.path.exists(path) else default_speaker_wav

# =========================
# Languages (25 idiomas)
# =========================
LANGUAGES = [
    {"code": "en", "name": "English 🇺🇸"}, {"code": "pt", "name": "Portuguese 🇧🇷"}, {"code": "es", "name": "Spanish 🇪🇸"},
    {"code": "fr", "name": "French 🇫🇷"}, {"code": "de", "name": "German 🇩🇪"}, {"code": "it", "name": "Italian 🇮🇹"},
    {"code": "ja", "name": "Japanese 🇯🇵"}, {"code": "ko", "name": "Korean 🇰🇷"}, {"code": "zh", "name": "Chinese 🇨🇳"},
    {"code": "ar", "name": "Arabic 🇸🇦"}, {"code": "ru", "name": "Russian 🇷🇺"}, {"code": "hi", "name": "Hindi 🇮🇳"},
    {"code": "bn", "name": "Bengali 🇧🇩"}, {"code": "pa", "name": "Punjabi 🇮🇳"}, {"code": "jv", "name": "Javanese 🇮🇩"},
    {"code": "ms", "name": "Malay 🇲🇾"}, {"code": "ta", "name": "Tamil 🇮🇳"}, {"code": "te", "name": "Telugu 🇮🇳"},
    {"code": "vi", "name": "Vietnamese 🇻🇳"}, {"code": "ur", "name": "Urdu 🇵🇰"}, {"code": "tr", "name": "Turkish 🇹🇷"},
    {"code": "fa", "name": "Persian 🇮🇷"}, {"code": "pl", "name": "Polish 🇵🇱"}, {"code": "nl", "name": "Dutch 🇳🇱"},
    {"code": "sw", "name": "Swahili 🇰🇪"}
]

@app.get("/api/languages")
async def get_languages():
    return {"languages": LANGUAGES}

# =========================
# Health check
# =========================
@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}

# =========================
# Upload voice
# =========================
@app.post("/upload_voice/", tags=["media"])
async def upload_voice(file: UploadFile = File(...), user_id: str = Form(...)):
    voice_path = os.path.join(VOICE_DIR, f"{user_id}_clone.wav")
    with open(voice_path, "wb") as f:
        f.write(await file.read())
    return {"status": "success", "voice_path": voice_path}

# =========================
# Serve frontend
# =========================
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

# =========================
# User Settings Manager
# =========================
settings_manager = UserSettingsManager()

@app.get("/settings/{user_id}", tags=["settings"])
async def get_user_settings(user_id: str):
    try:
        settings = settings_manager.get_settings(user_id)
        return settings.dict()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.put("/settings/{user_id}/general", tags=["settings"])
async def update_general_settings(user_id: str, theme: str = None, language: str = None):
    updates = {}
    if theme:
        updates["theme"] = theme
    if language:
        updates["language"] = language
    try:
        settings_manager.update_settings(user_id, "general", updates)
        return {"message": "General settings updated."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/settings/{user_id}/notifications", tags=["settings"])
async def update_notification_settings(user_id: str, meeting_transcription: bool = None, voice_clone_alerts: bool = None, platform_updates: bool = None):
    updates = {}
    if meeting_transcription is not None:
        updates["meeting_transcription"] = meeting_transcription
    if voice_clone_alerts is not None:
        updates["voice_clone_alerts"] = voice_clone_alerts
    if platform_updates is not None:
        updates["platform_updates"] = platform_updates
    try:
        settings_manager.update_settings(user_id, "notifications", updates)
        return {"message": "Notification settings updated."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
