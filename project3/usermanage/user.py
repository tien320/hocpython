class User:
    def __init__ (self, user_id: str, user_name: str, email: str, role: str):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.role = role
    def to_dict(self) -> dict:
        """Chuyển Object -> Dictionary để lưu JSON."""
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "role": self.role,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """Chuyển Dictionary -> Object User khi đọc từ JSON."""
        return cls(
            user_id=data["user_id"],
            user_name=data["user_name"],
            email=data["email"],
            role=data["role"],
        )
    def __str__ (self):
        return f"id: {self.user_id}, Tên: {self.user_name}, Email: {self.email}, Chức: {self.role}"
    