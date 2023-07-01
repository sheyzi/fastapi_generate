from enum import Enum
from typing import Generator, Optional

from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class PaginationParameters:
    def __init__(
        self,
        page: Optional[int] = 1,
        limit: Optional[int] = 10,
        filter: Optional[str] = None,
        order_by: Optional[str] = None,
    ):
        """
        This function is used to get pagination parameters from the request.

        :param page: Page number
        :param limit: Number of items per page
        :param filter: Filter string

        :return: Pagination parameters

        Example of pagination parameters:
            filter = "name:==:John;age:>:20"
            order_by = "name,age,-created_at"

        """

        # Convert filter to dict like this:
        # filter = {
        #     "name": {
        #         "operator": "==",
        #         "value": "John",
        #     },
        #     "age": {
        #         "operator": ">",
        #         "value": 20,
        #     },
        # }
        if filter:
            operators = [
                "==",
                "!=",
                "<=",
                ">=",
                "<",
                ">",
                "contains",
                "not_contains",
                "ilike",
                "like",
                "startswith",
                "endswith",
            ]
            conditions = filter.split(";")
            split_conditions = []
            for condition in conditions:
                field, operator, value = None, None, None

                try:
                    field, operator, value = condition.split(":")
                except:
                    continue

                if operator not in operators:
                    continue

                if field and operator and value:
                    field = field.strip()
                    value = value.strip()

                    if operator in ["==", "!="]:
                        value = int(value) if value.isdigit() else value
                    elif operator in ["<", ">", "<=", ">="]:
                        value = int(value)

                    split_conditions.append(
                        {"field": field, "operator": operator, "value": value}
                    )

        if order_by:
            order_by = order_by.split(",")

        self.page = page
        self.limit = limit
        self.filter = split_conditions if filter else None
        self.order_by = order_by
