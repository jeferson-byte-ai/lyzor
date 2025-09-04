from app.core.translate import translate_text, detect_language

class TranslationService:
    def detect(self, text: str) -> str:
        return detect_language(text)

    def translate(self, text: str, target_lang: str) -> str:
        return translate_text(text, target_lang)
