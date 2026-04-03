from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from models import User
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "money_manager_secret_key"
ALGORITHM = "HS256"

router = APIRouter()

class AuthRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(data: AuthRequest):
    if not data.username or not data.password:
        return JSONResponse(status_code=400, content={"message": "Username and password required"})
        
    existing_user = await User.find_one(User.username == data.username)
    if existing_user:
        return JSONResponse(status_code=400, content={"message": "User already exists"})
    
    role = "admin" if data.username.lower() == "admin" else "user"
    new_user = User(username=data.username, password=data.password, role=role)
    await new_user.insert()
    return JSONResponse(status_code=201, content={"message": "Registered successfully", "role": role})

@router.post("/login")
async def login(data: AuthRequest):
    user = await User.find_one(User.username == data.username, User.password == data.password)
    if user:
        token = jwt.encode(
            {"sub": str(user.id), "role": user.role, "exp": datetime.utcnow() + timedelta(days=7)},
            SECRET_KEY, 
            algorithm=ALGORITHM
        )
        return JSONResponse(status_code=200, content={"message": "Login successful", "username": data.username, "token": token, "role": user.role})
    
    return JSONResponse(status_code=401, content={"message": "Invalid username or password"})
