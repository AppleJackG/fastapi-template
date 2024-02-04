from typing import NoReturn
from uuid import UUID
import jwt

from src.auth.exceptions import InactiveUser, InvalidCredentials, InvalidToken

from .models import User
from ..config import settings
from datetime import datetime, timedelta, timezone
import bcrypt
from fastapi import Depends, Form, HTTPException, status

from ..database import session_factory
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


class AuthUtilities:

    @staticmethod
    def encode_token(
        payload: dict,
        private_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM
    ) -> str:
        to_encode = payload.copy()
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({
            'exp': expire_time,
            'iat': datetime.now(timezone.utc)
        })
        encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
        return encoded
    
    @staticmethod
    def decode_token(
        token: str,
        public_key: str = settings.PUBLIC_KEY,
        algorithm: str = settings.ALGORITHM
    ) -> dict:
        # decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        # return decoded
        try:
            decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        except jwt.InvalidTokenError:
            raise InvalidToken
        return decoded

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)
    
    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password
        )
    
    @staticmethod
    def check_credentials(user: User, password: str) -> bool | NoReturn:
        if not user:
            raise InvalidCredentials
        if not auth_utils.validate_password(password, user.password):
            raise InvalidCredentials
        if not user.is_active:
            raise InactiveUser
        return True   


auth_utils = AuthUtilities()