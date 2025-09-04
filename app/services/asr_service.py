from app.core.asr import stream_transcribe

class ASRService:
    async def transcribe(self, audio_bytes: bytes) -> str:
        return await stream_transcribe(audio_bytes)
