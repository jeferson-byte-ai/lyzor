from app.core.voice_clone import create_embedding_if_not_exists
from app.core.tts import synthesize_with_clone
import os

async def synthesize_participant_audio_real_time(participant_id: str, text: str, language: str, first_sample_path: str):
    speaker_wav = create_embedding_if_not_exists(participant_id, first_sample_path)
    output_path = os.path.join("temp_tts", f"{participant_id}.wav")
    synthesize_with_clone(text, output_path, speaker_wav=speaker_wav, language=language)
    with open(output_path, "rb") as f:
        return f.read()
