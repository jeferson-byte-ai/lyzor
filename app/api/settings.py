from fastapi import APIRouter
from app.models import UserSettings

router = APIRouter()

# Fake storage
CURRENT_SETTINGS = UserSettings()

@router.get("/")
def get_settings():
    return CURRENT_SETTINGS

@router.post("/")
def update_settings(settings: UserSettings):
    global CURRENT_SETTINGS
    CURRENT_SETTINGS = settings
    return {"message": "Settings updated successfully"}
