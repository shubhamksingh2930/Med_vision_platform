from pydantic import BaseModel, EmailStr, ConfigDict
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
