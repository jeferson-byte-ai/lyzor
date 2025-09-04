from fastapi import APIRouter, Form
from app.models.voice_embeddings import voice_embeddings

router = APIRouter()

@router.post("/map_participant_voice")
async def map_participant_voice(participant_id: str = Form(...), speaker_wav: str = Form(...)):
    voice_embeddings[participant_id] = speaker_wav
    return {"status": "ok", "participant_id": participant_id}
