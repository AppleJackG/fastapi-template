from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)