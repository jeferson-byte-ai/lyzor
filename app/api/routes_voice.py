from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

router = APIRouter()

voices = {}

@router.post("/voice/clone")
async def clone_voice(user_id: str = Form(...), voice_file: UploadFile = File(...)):
    # Placeholder for voice cloning logic
    voices[user_id] = {"voice_file": voice_file.filename}
    return {"message": f"Voice cloned for user {user_id}"}

@router.post("/voice/select")
async def select_ai_voice(user_id: str = Form(...), ai_voice: str = Form(...)):
    if user_id not in voices:
        return JSONResponse({"message": "User has no cloned voice."}, status_code=404)
    voices[user_id]["ai_voice"] = ai_voice
    return {"message": f"AI voice '{ai_voice}' selected for user {user_id}"}
