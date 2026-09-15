class User:
    def __init__(self,user_id: int, password: str,name: str,phone_number: str, email: str):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.phone_number = phone_number
        self.email = email