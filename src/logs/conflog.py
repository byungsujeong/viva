from motor import motor_asyncio

from pymongo import ASCENDING
from pymongo.mongo_client import MongoClient


MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "viva"
COLLECTION_NAME = "logs"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

collection.create_index([("created_at", ASCENDING)], expireAfterSeconds=60*24*60*60)

async_client = motor_asyncio.AsyncIOMotorClient(MONGO_URL)
async_db = async_client[DB_NAME]
async_collection = async_db[COLLECTION_NAME]