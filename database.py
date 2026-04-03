from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import Transaction, AnalyticsEvent, User
import os
import certifi
from dotenv import load_dotenv

load_dotenv()

async def init_db():
    MONGO_URI = os.getenv("databaseurl")
    if not MONGO_URI:
        raise ValueError("No database URL provided in .env")
        
    client = AsyncIOMotorClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    database = client.money_manager
    
    await init_beanie(database, document_models=[Transaction, AnalyticsEvent, User])
