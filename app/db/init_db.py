import inspect
import os
from sqlalchemy.orm import Session

from app.shared.helpers import import_models


def init_db(db: Session) -> None:
    this_file_directory = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))
    )

    root_directory = os.path.abspath(os.path.join(this_file_directory, "../.."))

    import_models(root_directory)
