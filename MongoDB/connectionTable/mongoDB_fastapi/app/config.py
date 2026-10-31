import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILES = (
    BASE_DIR / ".env",
    BASE_DIR.parent / ".env",
    BASE_DIR.parent.parent / ".env",
    BASE_DIR.parent.parent.parent / ".env",
    BASE_DIR.parent.parent.parent.parent / ".env",
)

for env_file in ENV_FILES:
    if env_file.is_file():
        load_dotenv(env_file, override=False)

MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "brightloop")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is missing. Configure it in your .env file.")
if not JWT_SECRET or JWT_SECRET == "REPLACE_WITH_A_LONG_RANDOM_SECRET":
    raise RuntimeError("Set a strong, private JWT_SECRET in your .env file.")
