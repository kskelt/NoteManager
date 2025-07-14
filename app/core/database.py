from pymongo import MongoClient
from pymongo.database import Database
from app.core.settings import get_settings
from app.utils.auth import hash_password

_settings = get_settings()

class MongoDB:
    client: MongoClient = None
    db: Database = None

    def connect(self, url: str, db_name: str):
        if not self.client:
            self.client = MongoClient(url)
            self.db = self.client.get_database(name=db_name)
            self._create_admin_user()

    def _create_admin_user(self):
        users_collection = self.db.users
        admin_username = _settings.admin_username
        admin_password = _settings.admin_password
        
        if not users_collection.find_one({"username": admin_username}):
            admin_user = {
                "username": admin_username,
                "password": hash_password(admin_password),
                "role": "admin",
            }
            users_collection.insert_one(admin_user)

    def close(self):
        if self.client:
            self.client.close()

get_db_instance = MongoDB()

def get_db() -> Database:
    return get_db_instance.db

def get_mongo_client() -> MongoClient:
    return get_db_instance.client