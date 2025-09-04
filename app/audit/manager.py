import os
import json
from datetime import datetime

class AuditManager:
    def __init__(self, storage_path="audit_logs"):
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def log_action(self, user_id: str, action: str, old_value=None, new_value=None, metadata=None):
        log_entry = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "old_value": old_value,
            "new_value": new_value,
            "metadata": metadata or {}
        }
        file_path = os.path.join(self.storage_path, f"{user_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_entry)
        with open(file_path, "w") as f:
            json.dump(logs, f, indent=4)
        print(f"[AUDIT] Action logged for user '{user_id}'.")
