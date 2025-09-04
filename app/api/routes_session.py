from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

sessions = {}

@router.post("/session/start")
async def start_session(user_id: str):
    if user_id in sessions:
        return JSONResponse({"message": "Session already started."}, status_code=400)
    sessions[user_id] = {"status": "active"}
    return {"message": f"Session started for user {user_id}"}

@router.post("/session/stop")
async def stop_session(user_id: str):
    if user_id not in sessions:
        return JSONResponse({"message": "No active session found."}, status_code=404)
    del sessions[user_id]
    return {"message": f"Session stopped for user {user_id}"}
