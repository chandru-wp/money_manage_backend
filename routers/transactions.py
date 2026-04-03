from fastapi import APIRouter, HTTPException
from typing import List
from models import Transaction
from schemas import TransactionCreate, TransactionResponse
from beanie import PydanticObjectId

router = APIRouter()

@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(username: Optional[str] = None):
    query = {"$or": [{"is_deleted": False}, {"is_deleted": {"$exists": False}}]}
    if username and username != "admin":
        query["username"] = username
    
    transactions = await Transaction.find(query).sort("-id").to_list()
    return [
        TransactionResponse(
            id=str(t.id),
            type=t.type,
            amount=t.amount,
            category=t.category,
            username=t.username,
            date=t.id.generation_time.isoformat() if hasattr(t.id, 'generation_time') else None
        ) for t in transactions
    ]

@router.post("/")
async def add_transaction(data: TransactionCreate):
    new_t = Transaction(type=data.type, amount=data.amount, category=data.category, username=data.username)
    await new_t.insert()
    return {"id": str(new_t.id)}

@router.put("/{t_id}")
async def edit_transaction(t_id: str, data: TransactionCreate):
    t = await Transaction.get(PydanticObjectId(t_id))
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    t.amount = data.amount
    t.category = data.category
    t.type = data.type
    await t.save()
    return {"message": "Updated"}

@router.delete("/{t_id}")
async def delete_transaction(t_id: str):
    obj_id = PydanticObjectId(t_id)
    t = await Transaction.get(obj_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    t.is_deleted = True
    await t.save()
    return {"message": "Deleted"}
