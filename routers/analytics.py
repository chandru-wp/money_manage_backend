from fastapi import APIRouter
from models import AnalyticsEvent
from schemas import AnalyticsCreate
from typing import Dict

router = APIRouter()

@router.post("/")
async def track_event(data: AnalyticsCreate):
    event = AnalyticsEvent(type=data.type, payload=data.payload)
    await event.insert()
    return {"ok": True}

@router.get("/summary")
async def analytics_summary() -> Dict[str, int]:
    page_views = await AnalyticsEvent.find(AnalyticsEvent.type == "page_view").count()
    adds = await AnalyticsEvent.find(AnalyticsEvent.type == "add_transaction").count()
    deletes = await AnalyticsEvent.find(AnalyticsEvent.type == "delete_transaction").count()
    total = await AnalyticsEvent.find_all().count()
    
    return {
        "page_views": page_views,
        "adds": adds,
        "deletes": deletes,
        "total_events": total
    }
