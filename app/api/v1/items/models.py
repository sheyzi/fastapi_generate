from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import Column, String, Float, ForeignKey, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.shared.base_model import Model

if TYPE_CHECKING:
    from app.api.v1.users.models import User


class Item(Model):
    __tablename__ = "items"

    name: str = Column(String(50), nullable=False)
    description: str = Column(Text, nullable=False)
    price: float = Column(Float, nullable=False)
    owner_id: uuid.UUID = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")

    def __repr__(self):
        return f"<Item {self.name}>"
