from datetime import datetime
from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from uuid import UUID, uuid4


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    refresh_token: Mapped[list['RefreshToken']] = relationship(back_populates='user')


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    refresh_token_id: Mapped[int] = mapped_column(primary_key=True)
    refresh_key: Mapped[UUID] = mapped_column(nullable=False)
    exp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    iat: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    access_key: Mapped[UUID] = mapped_column(nullable=False)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.user_id'))

    user: Mapped['User'] = relationship(back_populates='refresh_token')