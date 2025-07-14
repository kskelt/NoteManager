from typing import Annotated
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from bson import ObjectId


oid_pattern = r"^[a-f\d]{24}$"


def validate_objectid(value: str) -> str:
    if not ObjectId.is_valid(value):
        raise ValueError(f"{value} is not a valid ObjectId")
    return str(value)


PyObjectId = Annotated[str, BeforeValidator(validate_objectid)]


class BaseUser(BaseModel):
    username: str = Field(..., max_length=50)
    role: str = "user"


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=3)


class User(BaseUser):
    id: PyObjectId = Field(
        alias="_id",
        serialization_alias="id",
    )
    username: str = Field(..., max_length=50)
    role: str = "user"

    
