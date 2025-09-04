from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.session import MeetingSession

router = APIRouter()
session = MeetingSession()

@router.websocket("/ws/meeting")
async def meeting_ws(ws: WebSocket):
    """
    WebSocket bidirectional with dynamic target language.
    Client sends JSON: { audio: [...], sender: "user"/"other", target_lang: "en" }
    """
    await ws.accept()
    try:
        while True:
            msg = await ws.receive_json()
            audio_bytes = bytes(msg["audio"])
            sender = msg.get("sender", "user")
            target_lang = msg.get("target_lang", "en")

            audio_out = await session.process_audio(audio_bytes, sender, target_lang)
            await ws.send_bytes(audio_out)

    except WebSocketDisconnect:
        print("User disconnected.")
    except Exception as e:
        print(f"Error in session: {e}")
        await ws.close()
