from fastapi import APIRouter, Form
from app.models import IntegrationStatus
from app.core.connectors import ZoomConnector

router = APIRouter()

# Fake user id
USER_ID = "user123"

# Status tracker
CONNECTORS = {
    "zoom": ZoomConnector(USER_ID)
}

@router.post("/connect")
def connect_platform(platform: str = Form(...)):
    if platform in CONNECTORS:
        CONNECTORS[platform].connect()
        return {"message": f"{platform} connected"}
    return {"message": "Platform not supported"}

@router.get("/status")
def status_platform(platform: str):
    if platform in CONNECTORS:
        status = CONNECTORS[platform].status()
        return IntegrationStatus(platform=platform, connected=status)
    return {"platform": platform, "connected": False}
