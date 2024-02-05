from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserSchema(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr | None = None
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True, strict=True)


class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str