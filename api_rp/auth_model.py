from pydantic import BaseModel


class AuthModel(BaseModel):
    user: str
    password: str