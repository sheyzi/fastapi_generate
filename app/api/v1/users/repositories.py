from .models import User
from .schemas import UserCreate, UserUpdate, UserRead

from app.shared.base_repo import Repository
from app.shared.helpers import hash_password


class UserRepo(Repository[User, UserCreate, UserUpdate, UserRead]):
    def create(self, db, *, obj_in: UserCreate) -> UserRead:
        hashed_password = hash_password(obj_in.password)
        obj_in_data = obj_in.dict(exclude={"password"})

        db_obj = self.model(
            **obj_in_data,
            password=hashed_password,
        )

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        user = UserRead.from_orm(db_obj)
        return user

    def get_by_email(self, db, email):
        return db.query(self.model).filter(self.model.email == email).first()


user_repo = UserRepo(User, UserRead)
