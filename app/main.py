import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException, Depends, Body, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.shield.security import encrypt_data, decrypt_data, decode_access_token, add_token_to_blacklist, is_token_blacklisted
from fastapi.security import OAuth2PasswordBearer

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
# UserSettingsManager
# =========================
from app.user_settings.manager import UserSettingsManager
settings_manager = UserSettingsManager()

# =========================
# Auth routes
# =========================
from app.routes.auth import router as auth_router
from app.db.models.users import User  # Para /me endpoint
from app.crud.users import get_user as get_user_by_id

# =========================
# FastAPI app
# =========================
app = FastAPI(title="LYZOR-Translation Hub")

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
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# =========================
# JWT Dependency
# =========================
from uuid import UUID as UUIDType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        if is_token_blacklisted(token):
            raise HTTPException(status_code=401, detail="Token has been revoked")
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_uuid = UUIDType(user_id) 
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await get_user_by_id(db, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# =========================
# New endpoint: GET /me
# =========================
@app.get("/api/auth/me", tags=["auth"])
async def read_me(current_user=Depends(get_current_user)):
    return {
        "user_id": str(current_user.id),
        "username": current_user.username,
        "email": decrypt_data(current_user.email) if current_user.email else None,
        "phone_number": decrypt_data(current_user.phone_number) if current_user.phone_number else None
    }

# =========================
# Logout endpoint com blacklist
# =========================
@app.post("/api/auth/logout", tags=["auth"])
async def logout(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    add_token_to_blacklist(token)
    return {"message": "Logout successful. Token revoked."}

# =========================
# PATCH User Settings Endpoints
# =========================
@app.patch("/settings/{user_id}/general", tags=["settings"])
async def patch_general_settings(user_id: str, updates: dict = Body(...)):
    try:
        settings_manager.update_settings(user_id, "general", updates)
        return {"message": "General settings updated."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/settings/{user_id}/notifications", tags=["settings"])
async def patch_notification_settings(user_id: str, updates: dict = Body(...)):
    try:
        settings_manager.update_settings(user_id, "notifications", updates)
        return {"message": "Notification settings updated."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

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
# Languages
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
# Existing User Settings GET/PUT
# =========================
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
async def update_notification_settings(
    user_id: str,
    meeting_transcription: bool = None,
    voice_clone_alerts: bool = None,
    platform_updates: bool = None
):
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

# =========================
# Development-only test routes
# =========================
if os.getenv("ENV") != "production":
    @app.get("/test/encrypt", tags=["test"])
    async def test_encrypt(text: str = Query(..., description="Text to encrypt")):
        encrypted = encrypt_data(text)
        return {"original": text, "encrypted": encrypted}

    @app.get("/test/decrypt", tags=["test"])
    async def test_decrypt(cipher: str = Query(..., description="Encrypted text to decrypt")):
        decrypted = decrypt_data(cipher)
        return {"encrypted": cipher, "decrypted": decrypted}
