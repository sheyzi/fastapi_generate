from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.dialects.postgresql import UUID


@as_declarative()
class Model:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        # Generate plural table name from class name
        # e.g. User -> users
        # e.g. Category -> categories

        if cls.__name__.endswith("y"):
            return cls.__name__[:-1] + "ies"
        else:
            return cls.__name__ + "s"
