from pydantic import BaseModel
class User(BaseModel):
    user_id: int
    password: str
    name: str
    phone_number: str
    email: str