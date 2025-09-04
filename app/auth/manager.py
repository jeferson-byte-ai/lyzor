import os
import json
from .models import UserAccount, AuthProvider
from app.user_settings.manager import UserSettingsManager

class AuthManager:
    def __init__(self, storage_path="auth_data"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        self.settings_manager = UserSettingsManager()

    def save_user(self, user: UserAccount):
        file_path = os.path.join(self.storage_path, f"{user.user_id}.json")
        with open(file_path, "w") as f:
            json.dump(user.dict(), f, indent=4)
        print(f"[INFO] User '{user.user_id}' saved.")

    def load_user(self, user_id: str) -> UserAccount:
        file_path = os.path.join(self.storage_path, f"{user_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                return UserAccount(**data)
        else:
            raise Exception(f"[ERROR] User '{user_id}' not found.")

    def register_provider(self, user_id: str, provider_type: str, identifier: str, password_hash=None, token=None):
        try:
            user = self.load_user(user_id)
        except Exception:
            # Create new user if not exists
            user = UserAccount(user_id=user_id, username=identifier, providers=[])
            self.settings_manager.create_user(user_id, identifier, identifier)
            print(f"[INFO] Default settings created for user '{user_id}'.")

        # Check if provider already exists
        for p in user.providers:
            if p.type == provider_type and p.identifier == identifier:
                print(f"[WARNING] Provider already registered for user '{user_id}'.")
                return user

        new_provider = AuthProvider(
            type=provider_type,
            identifier=identifier,
            password_hash=password_hash,
            token=token
        )
        user.providers.append(new_provider)
        self.save_user(user)
        # Audit log for registration
        self.settings_manager.audit.log_action(user_id, f"register_provider_{provider_type}", new_value=new_provider.dict())
        print(f"[SUCCESS] Provider '{provider_type}' added to user '{user_id}'.")
        return user

    def delete_user(self, user_id: str):
        auth_file = os.path.join(self.storage_path, f"{user_id}.json")
        if os.path.exists(auth_file):
            os.remove(auth_file)
            print(f"[SUCCESS] User '{user_id}' deleted from auth system.")
        else:
            print(f"[ERROR] User '{user_id}' not found in auth system.")
        # Delete user settings + audit log
        self.settings_manager.delete_user(user_id)
