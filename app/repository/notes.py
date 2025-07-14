from typing import Optional, List
from fastapi import Depends
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime, timezone
from pymongo.database import Database
from app.database import get_db


class NoteRepository:
    def __init__(self, db: Database = Depends(get_db)):
        self._database: Database = db

    @property
    def collection(self) -> Collection:
        return self._database.get_collection("notes")

    def create_note(self, note_data: dict) -> ObjectId:
        note_data["user_id"] = ObjectId(note_data["user_id"])
        result = self.collection.insert_one(note_data)
        return result.inserted_id

    def get_note_by_id(self, note_id: str, user_id: str, 
                      is_admin: bool = False) -> dict | None:
        query = {"_id": ObjectId(note_id)}
        if not is_admin:
            query["user_id"] = ObjectId(user_id)
            query["deleted"] = False
            
        return self.collection.find_one(query)

    def update_note(self, note_id: str, user_id: str, update_data: dict) -> bool:
        query = {"_id": ObjectId(note_id), "user_id":  ObjectId(user_id), "deleted": False}
            
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = self.collection.update_one(
            query,
            {"$set": update_data}
        )
        return result.modified_count > 0

    def delete_note(self, note_id: str, user_id: str) -> bool:
        query = {"_id": ObjectId(note_id), "user_id":  ObjectId(user_id), "deleted": False}
        result = self.collection.update_one(
            query,
            {"$set": {
                "deleted": True,
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        return result.modified_count > 0

    def restore_note(self, note_id: str) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(note_id), "deleted": True},
            {"$set": {
                "deleted": False,
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        return result.modified_count > 0

    def get_user_notes(self, user_id: str, is_admin: bool = False) -> List[dict]:
        query = {}
        if not is_admin:
            query["user_id"] = ObjectId(user_id)
            query["deleted"] = False
        return list(self.collection.find(query))

    def get_all_notes(self) -> List[dict]:
        return list(self.collection.find())