import os
from app.core.tts import synthesize_with_clone

VOICE_CLONE_DIR = os.path.join(os.getcwd(), "clones")
os.makedirs(VOICE_CLONE_DIR, exist_ok=True)

class VoiceCloneService:
    def __init__(self):
        self.voice_dir = VOICE_CLONE_DIR

    def save_voice_sample(self, user_id: str, audio_bytes: bytes) -> str:
        file_path = os.path.join(self.voice_dir, f"{user_id}.wav")
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        return file_path

    def synthesize_speech(self, user_id: str, text: str) -> bytes:
        voice_path = os.path.join(self.voice_dir, f"{user_id}.wav")
        if not os.path.exists(voice_path):
            raise FileNotFoundError("Voice sample not found")
        return synthesize_with_clone(text, voice_path)
