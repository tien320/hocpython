import json
import os
from user import User

class UserRepository:
    def __init__(self, file_path: str = "users.json"):
        self.file_path = file_path
        self._storage = []
        self._load_from_file()

    def _load_from_file(self):
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self._storage = [User.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, KeyError):
            self._storage = []

    def _save_to_file(self):
        """Lưu toàn bộ danh sách hiện tại vào file JSON."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            data = [user.to_dict() for user in self._storage]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add(self, user: User) -> None:
        self._storage.append(user)
        self._save_to_file() 

    def list_all(self):
        return list(self._storage)

    def find_by_id(self, user_id: str):
        user_id = user_id.strip()
        for u in self._storage:
            if u.user_id == user_id:
                return u
        return None

    def find_by_role(self, role: str):
        role = role.strip().lower()
        result = []
        for s in self._storage:
            if role == s.role.lower():
                result.append(s)
        return result 

    def find_by_email(self, email: str):
        email = email.strip().lower()
        result = []
        for s in self._storage:
            if email in s.email.lower():
                result.append(s)
        return result

    def update(self, user_id: str, new_name: str, new_email: str, new_role: str) -> bool:
        user = self.find_by_id(user_id)
        if not user:
            return False

        if new_name.strip():
            user.user_name = new_name.strip()
        if new_email.strip():
            user.email = new_email.strip()
        if new_role.strip():
            user.role = new_role.strip()

        self._save_to_file()
        return True

    def delete(self, user_id: str):
        user = self.find_by_id(user_id)
        if not user: 
            return False

        self._storage.remove(user)
        self._save_to_file() 
        return True