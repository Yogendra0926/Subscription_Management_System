import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("Please set MONGODB_URI in your .env file.")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    print("MongoDB connection established successfully!")
except Exception as error:
    print("MongoDB connection failed.")
    print(error)
finally:
    if "client" in locals():
        client.close()
