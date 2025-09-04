import os
from app.models.voice_embeddings import voice_embeddings

def create_embedding_if_not_exists(participant_id: str, audio_sample_path: str):
    if participant_id in voice_embeddings:
        return voice_embeddings[participant_id]

    if not os.path.exists(audio_sample_path):
        raise FileNotFoundError(f"Audio sample not found: {audio_sample_path}")

    os.makedirs("embeddings", exist_ok=True)
    voice_embeddings[participant_id] = audio_sample_path
    return audio_sample_path