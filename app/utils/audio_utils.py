import os
from pydub import AudioSegment
import io

def save_audio_bytes(file_path: str, audio_bytes: bytes):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)

def read_audio(file_path: str) -> bytes:
    with open(file_path, "rb") as f:
        return f.read()

def convert_mp3_to_wav(mp3_bytes: bytes) -> bytes:
    audio = AudioSegment.from_file(io.BytesIO(mp3_bytes), format="mp3")
    buf = io.BytesIO()
    audio.export(buf, format="wav")
    return buf.getvalue()
