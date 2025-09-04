from fastapi import APIRouter
from app.models.voice_catalog import VOICE_CATALOG, VoiceOption

from typing import List

router = APIRouter()

@router.get("/voice_catalog", response_model=List[VoiceOption])
async def get_voice_catalog():
    return VOICE_CATALOG
