import os
import threading
import torch
from functools import partial
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig

torch.load = partial(torch.load, weights_only=False)
torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig])

_model = None
_model_lock = threading.Lock()

def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    return _model

def _normalize_xtts_lang(lang: str) -> str:
    if not lang:
        return "en"
    l = lang.lower()
    # XTTS entende 'zh'; então normaliza variantes pra 'zh'
    if l in {"zh-cn", "zh-hans", "zh-tw", "zh-hant", "zh"}:
        return "zh"
    return l

def synthesize_with_clone(text: str, output_path: str, speaker_wav: str, language: str):
    if not text:
        raise ValueError("Text can not be empty.")
    if not os.path.exists(speaker_wav):
        raise FileNotFoundError(f"File not found: {speaker_wav}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    model = _get_model()
    model.tts_to_file(
        text=text,
        file_path=output_path,
        speaker_wav=speaker_wav,
        language=_normalize_xtts_lang(language),
    )
    return output_path