from bson.codec_options import UuidRepresentation
from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings


class MongoClient:
    def __init__(self) -> None:
        print(f"DEBUG (mongo.py): DATABASE_URL sendo usado: {settings.DATABASE_URL}")
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL,
            uuidRepresentation="standard",
        )

    def get(self) -> AsyncIOMotorClient:
        return self.client


db_client = MongoClient()
