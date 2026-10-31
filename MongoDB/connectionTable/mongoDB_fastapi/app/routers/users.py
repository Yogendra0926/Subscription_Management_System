from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.database import db
from app.schemas import UserCreate, UserPatch
from app.security import get_current_user, require_roles, hash_password
from app.utils import public_document

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("", status_code=201)
def create_user(payload: UserCreate, _: dict = Depends(require_roles("admin"))):
    if payload.role not in {"admin", "staff", "customer"}:
        raise HTTPException(422, "Invalid role")
    now = datetime.now(timezone.utc)
    doc = payload.model_dump(exclude={"password"})
    doc["email"] = doc["email"].lower()
    doc["password_hash"] = hash_password(payload.password)
    doc.update({"status": "active", "created_at": now, "updated_at": now})
    try:
        result = db.users.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(409, "Email already exists")
    return public_document(db.users.find_one({"_id": result.inserted_id}))

@router.get("")
def list_users(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
               _: dict = Depends(require_roles("admin", "staff"))):
    total = db.users.count_documents({})
    docs = db.users.find({}, {"password_hash": 0}).skip((page-1)*limit).limit(limit)
    return {"items": [public_document(x) for x in docs], "page": page, "limit": limit, "total": total}

@router.get("/{record_id}")
def get_user(record_id: str, _: dict = Depends(require_roles("admin", "staff"))):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(400, "Invalid ObjectId")
    doc = db.users.find_one({"_id": ObjectId(record_id)}, {"password_hash": 0})
    if not doc:
        raise HTTPException(404, "User not found")
    return public_document(doc)

@router.patch("/{record_id}")
def patch_user(record_id: str, payload: UserPatch, _: dict = Depends(require_roles("admin"))):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(400, "Invalid ObjectId")
    data = payload.model_dump(exclude_unset=True)
    if "role" in data and data["role"] not in {"admin", "staff", "customer"}:
        raise HTTPException(422, "Invalid role")
    if "email" in data:
        data["email"] = data["email"].lower()
    if "password" in data:
        data["password_hash"] = hash_password(data.pop("password"))
    data["updated_at"] = datetime.now(timezone.utc)
    try:
        result = db.users.update_one({"_id": ObjectId(record_id)}, {"$set": data})
    except DuplicateKeyError:
        raise HTTPException(409, "Email already exists")
    if result.matched_count == 0:
        raise HTTPException(404, "User not found")
    return public_document(db.users.find_one({"_id": ObjectId(record_id)}, {"password_hash": 0}))

@router.delete("/{record_id}")
def delete_user(record_id: str, current: dict = Depends(require_roles("admin"))):
    if not ObjectId.is_valid(record_id):
        raise HTTPException(400, "Invalid ObjectId")
    oid = ObjectId(record_id)
    if oid == current["_id"]:
        raise HTTPException(400, "You cannot delete your own account")
    result = db.users.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(404, "User not found")
    return {"message": "User deleted"}
