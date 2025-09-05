import logging
from langdetect import detect

try:
    from deep_translator import GoogleTranslator
except ImportError:
    GoogleTranslator = None

def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Traduz o texto para o idioma alvo.
    Tenta usar GoogleTranslator (deep-translator) e cai para 'translate' se necessário.
    """
    if not text or not text.strip():
        return ""

    lang = target_lang.lower()
    # Normaliza variantes do chinês
    if lang in {"zh-cn", "zh-hans"}:
        lang = "zh-cn"
    elif lang in {"zh-tw", "zh-hant"}:
        lang = "zh-tw"

    # Primeiro tenta deep-translator
    if GoogleTranslator:
        try:
            translated = GoogleTranslator(source="auto", target=lang).translate(text)
            if translated and translated.strip().lower() != text.strip().lower():
                return translated
        except Exception as e:
            logging.warning(f"[MT] deep-translator failed: {e}")

    # Fallback para a biblioteca translate
    try:
        from translate import Translator
        translator = Translator(to_lang=lang)
        return translator.translate(text)
    except Exception as e:
        logging.warning(f"[MT] translate lib failed: {e}")
        return text

def detect_language(text: str) -> str:
    """
    Detecta o idioma do texto.
    """
    try:
        return detect(text)
    except Exception:
        return "unknown"
