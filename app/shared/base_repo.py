from typing import Optional, Tuple, TypeVar, Generic, Type
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.api.deps import PaginationParameters

from app.shared.base_model import Model
from app.shared.schemas.pagination_schema import PaginationResponse

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)


class Repository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]
):
    def __init__(self, model: Type[ModelType], read_schema: ReadSchemaType):
        """
        Base repository class that provides common CRUD operations

        **Parameters**

        * `model`: The SQLAlchemy model class
        """
        self.model = model
        self.read_schema = read_schema

    def get(self, db: Session, id: str) -> Optional[ModelType]:
        """
        Get a model by id

        **Parameters**

        * `id`: The id of the model to get

        **Returns**

        The model or None if not found
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self,
        db: Session,
        paginationParameters: Optional[PaginationParameters] = None,
    ) -> PaginationResponse[ModelType]:
        """
        Get multiple models

        **Parameters**

        db: The database session
        paginationParameters: Pagination parameters


        **Returns**

        A list of models
        """

        filter = paginationParameters.filter if paginationParameters else None
        order_by = paginationParameters.order_by if paginationParameters else None
        skip = (
            (paginationParameters.page - 1) * paginationParameters.limit
            if paginationParameters
            else 0
        )
        limit = paginationParameters.limit if paginationParameters else 100

        result = db.query(self.model)
        exclude = ["password"]

        targ_cols = [x for x in result.first().__dict__.keys() if x not in exclude]

        # Filter the result
        if filter:
            for field in filter:
                operator = field["operator"]
                value = field["value"]
                name = field["field"]

                # Check if the field is valid
                if name not in targ_cols:
                    continue

                if operator == "==":
                    result = result.filter(getattr(self.model, name) == value)
                elif operator == "!=":
                    result = result.filter(getattr(self.model, name) != value)
                elif operator == ">":
                    result = result.filter(getattr(self.model, name) > value)
                elif operator == ">=":
                    result = result.filter(getattr(self.model, name) >= value)
                elif operator == "<":
                    result = result.filter(getattr(self.model, name) < value)
                elif operator == "<=":
                    result = result.filter(getattr(self.model, name) <= value)
                elif operator == "like":
                    # Case sensitive like
                    result = result.filter(getattr(self.model, name).like(value))
                elif operator == "ilike":
                    # Case insensitive like
                    result = result.filter(getattr(self.model, name).ilike(value))
                elif operator == "contains":
                    result = result.filter(getattr(self.model, name).contains(value))
                elif operator == "not_contains":
                    result = result.filter(~getattr(self.model, name).contains(value))
                elif operator == "startswith":
                    result = result.filter(getattr(self.model, name).startswith(value))
                elif operator == "endswith":
                    result = result.filter(getattr(self.model, name).endswith(value))

        # Order the result
        if order_by:
            for field in order_by:
                if field.startswith("-"):
                    result = result.order_by(desc(field[1:]))
                else:
                    result = result.order_by(asc(field))

        # # Exclude the password from the result
        # result = result.with_entities(targ_cols)

        # Apply skip and limit
        result = result.offset(skip).limit(limit)

        # Get the total count
        total = result.count()

        # Get the data
        data = result.all()

        # Calculate the number of pages
        pages = total // limit

        if total % limit > 0:
            pages += 1

        return PaginationResponse(
            total=total,
            page=paginationParameters.page,
            limit=paginationParameters.limit,
            pages=pages,
            data=[self.read_schema(**item.__dict__) for item in data],
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a model

        **Parameters**

        * `obj_in`: The model to create

        **Returns**

        The created model
        """
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        """
        Update a model

        **Parameters**

        * `db_obj`: The model to update
        * `obj_in`: The updated model data

        **Returns**

        The updated model
        """

        obj_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            setattr(db_obj, field, obj_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, db_obj: ModelType) -> ModelType:
        """
        Delete a model

        **Parameters**

        * `db_obj`: The model to delete

        **Returns**

        The deleted model
        """
        db.delete(db_obj)
        db.commit()
        return db_obj
