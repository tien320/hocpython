class User:
    def __init__(self, user_id: int, name: str, email: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
    def __str__(self):
        return f"ID: {self.user_id}, Tên: {self.name}, Email: {self.email}, Chức vụ: {self.role}"
    
        