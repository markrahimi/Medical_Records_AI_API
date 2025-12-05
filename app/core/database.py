from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.logging import logger

client = None
db = None


async def connect_to_mongo():
    global client, db
    logger.debug(f"Attempting to connect to MongoDB at {settings.mongodb_db_name}")
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        db = client[settings.mongodb_db_name]
        logger.info(f"Successfully connected to MongoDB database: {settings.mongodb_db_name}")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    global client
    if client:
        logger.debug("Closing MongoDB connection")
        client.close()
        logger.info("MongoDB connection closed")


def get_database():
    if db is None:
        logger.warning("Database connection not initialized, returning None")
    return db
