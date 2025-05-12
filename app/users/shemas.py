from pydantic import BaseModel, EmailStr, Extra


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: int
    email: EmailStr


class GoogleUserData(BaseModel):
    id: int | None = None
    email: str
    verified_email: bool = True
    name: str
    access_token: str

    class Config:
        extra = Extra.ignore  # Игнорировать дополнительные
