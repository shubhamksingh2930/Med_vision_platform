from pydantic import BaseModel, ConfigDict
import uuid

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: uuid.UUID
    username: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
