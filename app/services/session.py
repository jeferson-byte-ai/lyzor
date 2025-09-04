import asyncio
from app.core.asr import stream_transcribe
from app.core.tts import synthesize_with_clone
import tempfile
import os

class MeetingSession:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.tts_temp_dir = os.path.join(os.getcwd(), "temp_tts")
        os.makedirs(self.tts_temp_dir, exist_ok=True)
        self.speaker_wav = "voices/user_clone.wav"

    async def process_audio(self, audio_bytes, sender="user", target_lang="en"):
        """
        Processes audio bidirectionally with dynamic target language.
        sender: "user" or "other"
        target_lang: language code to translate to
        """
        async with self.lock:
            # 1️⃣ Transcribe
            text = stream_transcribe(audio_bytes)

            # 2️⃣ Translate
            translated_text = await self.translate_text(text, target_lang)

            # 3️⃣ Generate TTS
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=self.tts_temp_dir)
            output_path = temp_file.name
            synthesize_with_clone(
                text=translated_text,
                output_path=output_path,
                speaker_wav=self.speaker_wav,
                language=target_lang
            )

            # 4️⃣ Read bytes
            with open(output_path, "rb") as f:
                audio_out_bytes = f.read()
            os.remove(output_path)
            return audio_out_bytes

    async def translate_text(self, text, target_lang="en"):
        """
        Replace this placeholder with your real translation API or model.
        """
        return f"[TRANSLATED TO {target_lang}] {text}"
