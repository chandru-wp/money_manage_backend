from pydantic import BaseModel
from typing import Optional, Dict, Any

class TransactionCreate(BaseModel):
    type: str
    amount: float
    category: str
    username: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    type: str
    amount: float
    category: str
    username: Optional[str] = None
    date: Optional[str] = None

class AnalyticsCreate(BaseModel):
    type: str
    payload: Optional[Dict[str, Any]] = {}

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    password: str
