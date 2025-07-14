from fastapi import Depends
from pymongo.database import Database

from app.core.database import get_db
from pymongo.collection import Collection


class UserRepository:
    def __init__(
        self,
        db: Database = Depends(get_db),
    ):
        self._database: Database = db

    @property
    def collection(self) -> Collection:
        return self._database.get_collection("users")

    def get_user_by_username(self, username: str):
        return self.collection.find_one({"username": username})

    def create_user(self, user_data: dict):
        self.collection.insert_one(user_data)
        return user_data