from app.core.tts import synthesize_text

class TTSService:
    def synthesize(self, text: str) -> bytes:
        return synthesize_text(text)
