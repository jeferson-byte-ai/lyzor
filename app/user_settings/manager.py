# app/user_settings/manager.py

import os
import json
from .models import UserSettings
from .defaults import default_user_settings
from app.audit.manager import AuditManager

class UserSettingsManager:
    def __init__(self, storage_path="user_data"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        self.audit = AuditManager()

    def get_settings(self, user_id: str) -> UserSettings:
        file_path = os.path.join(self.storage_path, f"{user_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                print(f"[INFO] Settings loaded for user '{user_id}'.")
                return UserSettings(**data)
        else:
            raise Exception(f"[ERROR] User '{user_id}' not found.")

    def create_user(self, user_id: str, username: str, email: str) -> UserSettings:
        file_path = os.path.join(self.storage_path, f"{user_id}.json")
        if os.path.exists(file_path):
            print(f"[WARNING] User '{user_id}' already exists. Loading existing settings.")
            return self.get_settings(user_id)

        # Cria UserSettings padrão incluindo métodos de login
        settings = default_user_settings(user_id, username, email)
        self.save_settings(settings)
        self.audit.log_action(user_id, "create_user", new_value=settings.dict())
        print(f"[SUCCESS] User '{user_id}' created successfully with default settings.")
        return settings

    def save_settings(self, settings: UserSettings):
        file_path = os.path.join(self.storage_path, f"{settings.account.user_id}.json")
        with open(file_path, "w") as f:
            json.dump(settings.dict(), f, indent=4)
        print(f"[INFO] Settings saved for user '{settings.account.user_id}'.")

    def update_settings(self, user_id: str, section: str, updates: dict):
        try:
            settings = self.get_settings(user_id)
        except Exception as e:
            print(e)
            return

        if hasattr(settings, section):
            section_obj = getattr(settings, section)
            old_values = section_obj.dict()
            updated = False
            for key, value in updates.items():
                if hasattr(section_obj, key):
                    setattr(section_obj, key, value)
                    updated = True
            if updated:
                self.save_settings(settings)
                self.audit.log_action(
                    user_id,
                    f"update_{section}",
                    old_value=old_values,
                    new_value=section_obj.dict()
                )
                print(f"[SUCCESS] Section '{section}' updated for user '{user_id}'.")
            else:
                print(f"[WARNING] No valid fields found in section '{section}'.")
        else:
            print(f"[ERROR] Section '{section}' does not exist in user settings.")

    def delete_user(self, user_id: str):
        file_path = os.path.join(self.storage_path, f"{user_id}.json")
        if os.path.exists(file_path):
            os.remove(file_path)
            self.audit.log_action(user_id, "delete_user")
            print(f"[SUCCESS] User '{user_id}' deleted successfully.")
        else:
            print(f"[ERROR] User '{user_id}' not found for deletion.")
