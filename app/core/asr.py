import whisper
import subprocess
import tempfile
import os

# Load Whisper model (you can change "base" to "small", "medium", "large")
_model = whisper.load_model("base")

def stream_transcribe(audio_bytes: bytes) -> str:
    """
    Transcribes audio bytes to text using Whisper.
    Input: raw audio (WebM/Opus or PCM16).
    Output: recognized text.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_webm:
        tmp_webm.write(audio_bytes)
        tmp_webm_path = tmp_webm.name

    tmp_wav_path = tmp_webm_path.replace(".webm", ".wav")

    # Convert WebM → WAV (mono, 16kHz)
    cmd = [
        "ffmpeg", "-y", "-i", tmp_webm_path,
        "-ar", "16000", "-ac", "1",
        tmp_wav_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result = _model.transcribe(tmp_wav_path, condition_on_previous_text=True)
    text = result.get("text", "").strip()

    os.remove(tmp_webm_path)
    os.remove(tmp_wav_path)

    return text
