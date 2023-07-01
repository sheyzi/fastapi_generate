from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.orm import relationship

from app.shared.base_model import Model

if TYPE_CHECKING:
    from app.api.v1.items.models import Item


class User(Model):
    __tablename__ = "users"

    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)

    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User {self.email}>"
