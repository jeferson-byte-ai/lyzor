from .models import UserSettings

def default_user_settings(user_id: str, username: str, email: str) -> UserSettings:
    return UserSettings(
        account={
            "user_id": user_id,
            "username": username,
            "email": email,
            "auth_methods": {
                "google": None,       # será preenchido com token/id se logar via Google
                "microsoft": None,    # idem
                "phone": None         # ex: número verificado
            }
        },
        preferences={
            "language": "en",
            "voice": "default",
            "theme": "dark",
            "notifications": True,
            "auto_translate": True,
            "speech_speed": 1.0
        }
    )
