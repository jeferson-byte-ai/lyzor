import os, json, base64, asyncio, time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.core.asr import stream_transcribe
from app.core.translate import translate_text, detect_language
from app.core.tts import synthesize_with_clone

router = APIRouter()

VOICE_DIR = os.path.join(os.path.dirname(__file__), "..", "voices")
os.makedirs(VOICE_DIR, exist_ok=True)
default_speaker = os.path.join(VOICE_DIR, "default_clone.wav")

def get_user_voice(user_id: str):
    path = os.path.join(VOICE_DIR, f"{user_id}_clone.wav")
    return path if os.path.exists(path) else default_speaker

async def safe_send(ws: WebSocket, data: dict):
    """Send JSON safely over WebSocket."""
    if ws.client_state == WebSocketState.CONNECTED:
        try:
            await ws.send_text(json.dumps(data))
        except RuntimeError:
            pass

async def process_audio_buffer(buffer: bytes, target_lang: str, user_id: str):
    """Transcribe, translate, synthesize audio, and return base64."""
    text = stream_transcribe(buffer)
    if not text.strip():
        return None, None, None

    translated = translate_text(text, target_lang)
    speaker_wav = get_user_voice(user_id)

    out_dir = os.path.join(VOICE_DIR, "realtime")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{user_id}_{int(time.time() * 1000)}.wav")

    synthesize_with_clone(translated, out_path, speaker_wav, target_lang)

    # Wait up to 5s for file
    t0 = time.time()
    while not os.path.exists(out_path) and time.time() - t0 < 5:
        await asyncio.sleep(0.05)

    audio_b64 = None
    if os.path.exists(out_path):
        with open(out_path, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    return text, translated, audio_b64

@router.websocket("/ws/translate")
async def websocket_translate(ws: WebSocket):
    await ws.accept()
    buffer_audio = b""
    user_id = None

    try:
        while ws.client_state == WebSocketState.CONNECTED:
            try:
                message = await ws.receive()
                
                # Audio bytes
                if "bytes" in message:
                    buffer_audio += message["bytes"] or b""
                
                # Text messages (init / stop)
                elif "text" in message:
                    payload = json.loads(message["text"])

                    if not user_id and payload.get("user_id"):
                        user_id = payload["user_id"]

                    # Stop command triggers translation + TTS
                    if payload.get("action") == "stop":
                        target_lang = payload.get("target_lang", "en")
                        if buffer_audio:
                            orig_text, translated, audio_b64 = await process_audio_buffer(
                                buffer_audio, target_lang, user_id or "default"
                            )
                            buffer_audio = b""
                            if orig_text and translated:
                                await safe_send(ws, {
                                    "status": "success",
                                    "transcript": orig_text,
                                    "detected_lang": detect_language(orig_text),
                                    "translation": translated,
                                    "audio_base64": audio_b64,
                                    "partial": False
                                })

            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break

            await asyncio.sleep(0.005)

    finally:
        if ws.client_state == WebSocketState.CONNECTED:
            await ws.close()
