from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from app.database import db
from app.security import require_roles
from app.utils import prepare_document, serialize, public_document

PROTECTED_FIELDS = {"_id", "sample_data", "password", "password_hash"}

def build_crud_router(collection_name: str, tag: str):
    router = APIRouter(prefix=f"/api/{collection_name.replace('_', '-')}", tags=[tag])
    collection = db[collection_name]

    @router.post("", status_code=201)
    def create_record(payload: dict, _: dict = Depends(require_roles("admin", "staff"))):
        if not isinstance(payload, dict) or not payload:
            raise HTTPException(422, "Request body must be a non-empty JSON object")
        forbidden = PROTECTED_FIELDS.intersection(payload)
        if forbidden:
            raise HTTPException(422, f"These fields cannot be supplied: {', '.join(sorted(forbidden))}")
        doc = prepare_document(payload)
        doc.setdefault("created_at", datetime.now(timezone.utc))
        try:
            result = collection.insert_one(doc)
        except DuplicateKeyError:
            raise HTTPException(409, "A record with a unique value already exists")
        return public_document(collection.find_one({"_id": result.inserted_id}))

    @router.get("")
    def list_records(page: int = Query(1, ge=1), limit: int = Query(20, ge=1, le=100),
                     _: dict = Depends(require_roles("admin", "staff", "customer"))):
        total = collection.count_documents({})
        docs = collection.find({}).skip((page - 1) * limit).limit(limit)
        return {"items": [public_document(x) for x in docs], "page": page, "limit": limit, "total": total}

    @router.get("/{record_id}")
    def get_record(record_id: str, _: dict = Depends(require_roles("admin", "staff", "customer"))):
        if not ObjectId.is_valid(record_id):
            raise HTTPException(400, "Invalid ObjectId")
        doc = collection.find_one({"_id": ObjectId(record_id)})
        if not doc:
            raise HTTPException(404, "Record not found")
        return public_document(doc)

    @router.patch("/{record_id}")
    def patch_record(record_id: str, payload: dict, _: dict = Depends(require_roles("admin", "staff"))):
        if not ObjectId.is_valid(record_id):
            raise HTTPException(400, "Invalid ObjectId")
        if not isinstance(payload, dict) or not payload:
            raise HTTPException(422, "Request body must be a non-empty JSON object")
        forbidden = PROTECTED_FIELDS.intersection(payload)
        if forbidden:
            raise HTTPException(422, f"These fields cannot be updated: {', '.join(sorted(forbidden))}")
        data = prepare_document(payload)
        data["updated_at"] = datetime.now(timezone.utc)
        try:
            result = collection.update_one({"_id": ObjectId(record_id)}, {"$set": data})
        except DuplicateKeyError:
            raise HTTPException(409, "A record with a unique value already exists")
        if result.matched_count == 0:
            raise HTTPException(404, "Record not found")
        return public_document(collection.find_one({"_id": ObjectId(record_id)}))

    @router.delete("/{record_id}")
    def delete_record(record_id: str, _: dict = Depends(require_roles("admin"))):
        if not ObjectId.is_valid(record_id):
            raise HTTPException(400, "Invalid ObjectId")
        result = collection.delete_one({"_id": ObjectId(record_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "Record not found")
        return {"message": f"{tag} record deleted"}

    return router
