from fastapi import APIRouter
from typing import List
from models import User
from schemas import UserCreate, UserResponse

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_users():
    users = await User.find_all().to_list()
    return [
        UserResponse(
            id=str(u.id),
            username=u.username,
            password=u.password
        ) for u in users
    ]

@router.post("/")
async def create_user(data: UserCreate):
    new_user = User(username=data.username, password=data.password)
    await new_user.insert()
    return {"id": str(new_user.id)}
