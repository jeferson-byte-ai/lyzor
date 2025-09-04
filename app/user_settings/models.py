from pydantic import BaseModel, validator
from typing import Optional, Dict

# ----------------------------
# Supported platform languages
# ----------------------------
SUPPORTED_LANGUAGES = [
    "en",  # English
    "pt",  # Portuguese
    "es",  # Spanish
    "fr",  # French
    "de",  # German
    "it",  # Italian
    "zh",  # Chinese
    "ja",  # Japanese
    "ko",  # Korean
    "ru"   # Russian
]

# ----------------------------
# General Settings
# ----------------------------
class GeneralSettings(BaseModel):
    theme: str = "system"  # options: light, dark, system
    language: str = "en"   # default English

    @validator("language")
    def validate_language(cls, v):
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language '{v}'. Supported languages: {SUPPORTED_LANGUAGES}"
            )
        return v

# ----------------------------
# Notifications Settings
# ----------------------------
class NotificationSettings(BaseModel):
    meeting_transcription: bool = True
    voice_clone_alerts: bool = True
    platform_updates: bool = True

# ----------------------------
# Account Settings
# ----------------------------
class AccountSettings(BaseModel):
    user_id: str
    username: str
    email: str
    allow_data_sharing: bool = True
    auth_methods: Dict[str, Optional[str]] = {
        "google": None,       # ID ou token do Google
        "microsoft": None,    # ID ou token da Microsoft
        "phone": None         # número de telefone verificado
    }

# ----------------------------
# Complete User Settings
# ----------------------------
class UserSettings(BaseModel):
    general: GeneralSettings = GeneralSettings()
    notifications: NotificationSettings = NotificationSettings()
    account: AccountSettings
