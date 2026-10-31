import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConfigurationError, PyMongoError, ServerSelectionTimeoutError

load_dotenv(override=False)

uri = os.getenv("MONGODB_URI", "").strip()
database = os.getenv("MONGODB_DATABASE", "").strip()

if not uri:
    raise ValueError("Set MONGODB_URI in .env before running this check.")

client = None
try:
    client = MongoClient(
        uri,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
    )
    if database:
        client[database].command("ping")
    else:
        client.admin.command("ping")
    print("MongoDB connection established successfully!")
except ConfigurationError as error:
    print(f"MongoDB configuration error: {error}")
except ServerSelectionTimeoutError:
    print(
        "MongoDB server selection timed out. Check that the Atlas cluster is running, "
        "your current IP is in Atlas Network Access, and MONGODB_URI is current."
    )
except PyMongoError as error:
    print(f"MongoDB connection failed: {error.__class__.__name__}: {error}")
finally:
    if client is not None:
        client.close()
