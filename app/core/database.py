from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = None
db = None


async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db_name]
    print("✅ Connected to MongoDB Atlas")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("❌ Closed MongoDB connection")


def get_database():
    return db
