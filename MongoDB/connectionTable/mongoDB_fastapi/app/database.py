from pymongo import MongoClient
from pymongo.server_api import ServerApi
from app.config import MONGODB_URI, MONGODB_DATABASE

client = MongoClient(
    MONGODB_URI,
    server_api=ServerApi("1"),
    serverSelectionTimeoutMS=15000,
)
db = client[MONGODB_DATABASE]

def ping_database():
    client.admin.command("ping")

def close_database():
    client.close()
