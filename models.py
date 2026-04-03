from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Transaction(Document):
    type: str
    amount: float
    category: str
    is_deleted: bool = False

    class Settings:
        collection = "transactions"

class AnalyticsEvent(Document):
    type: str
    payload: dict
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        collection = "analytics"

class User(Document):
    username: str
    password: str
    role: str = "user" # user, admin

    class Settings:
        collection = "users"
