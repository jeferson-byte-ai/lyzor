from pydantic import BaseModel
from typing import Optional, Dict

class UserSettings(BaseModel):
    theme: str = "light"
    language: str = "en"
    notifications: Dict[str, bool] = {
        "messages": True,
        "calls": True,
        "meetings": True
    }

class UserInfo(BaseModel):
    username: str
    email: str

class IntegrationStatus(BaseModel):
    platform: str
    connected: bool
