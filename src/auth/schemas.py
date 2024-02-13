from datetime import datetime
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


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None

    model_config = ConfigDict(from_attributes=True)


class AccessTokenPayload(BaseModel):
    sub: str
    username: str
    email: EmailStr
    exp: datetime
    iat: datetime
    access_key: str

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenPayload(BaseModel):
    sub: str
    refresh_key: str
    exp: datetime
    iat: datetime
    access_key: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)