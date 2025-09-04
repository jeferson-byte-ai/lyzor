from pydantic import BaseModel
from typing import List

class VoiceOption(BaseModel):
    name: str
    language: str
    gender: str
    sample_url: str

LANGUAGES = [
    {"code": "en", "name": "English 🇺🇸"},
    {"code": "pt", "name": "Portuguese 🇧🇷"},
    {"code": "es", "name": "Spanish 🇪🇸"},
    {"code": "fr", "name": "French 🇫🇷"},
    {"code": "de", "name": "German 🇩🇪"},
    {"code": "it", "name": "Italian 🇮🇹"},
    {"code": "ja", "name": "Japanese 🇯🇵"},
    {"code": "ko", "name": "Korean 🇰🇷"},
    {"code": "zh", "name": "Chinese 🇨🇳"},
    {"code": "ar", "name": "Arabic 🇸🇦"},
    {"code": "ru", "name": "Russian 🇷🇺"},
    {"code": "hi", "name": "Hindi 🇮🇳"},
    {"code": "bn", "name": "Bengali 🇧🇩"},
    {"code": "pa", "name": "Punjabi 🇮🇳"},
    {"code": "jv", "name": "Javanese 🇮🇩"},
    {"code": "ms", "name": "Malay 🇲🇾"},
    {"code": "ta", "name": "Tamil 🇮🇳"},
    {"code": "te", "name": "Telugu 🇮🇳"},
    {"code": "vi", "name": "Vietnamese 🇻🇳"},
    {"code": "ur", "name": "Urdu 🇵🇰"},
    {"code": "tr", "name": "Turkish 🇹🇷"},
    {"code": "fa", "name": "Persian 🇮🇷"},
    {"code": "pl", "name": "Polish 🇵🇱"},
    {"code": "nl", "name": "Dutch 🇳🇱"},
    {"code": "sw", "name": "Swahili 🇰🇪"},
]

VOICE_CATALOG: List[VoiceOption] = []
for lang in LANGUAGES:
    VOICE_CATALOG.append(VoiceOption(name=f"Male_{lang['code']}", language=lang['code'], gender="male", sample_url=f"/samples/{lang['code']}_male.mp3"))
    VOICE_CATALOG.append(VoiceOption(name=f"Female_{lang['code']}", language=lang['code'], gender="female", sample_url=f"/samples/{lang['code']}_female.mp3"))
