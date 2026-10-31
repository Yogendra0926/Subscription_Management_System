from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db
from app.schemas import LoginRequest
from app.security import verify_password, create_access_token, get_current_user
from app.utils import public_document

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends()):
    # OAuth2 form uses "username"; clients should put their email in this field.
    user = db.users.find_one({"email": form.username.lower(), "status": "active"})
    if not user or not verify_password(form.password, user.get("password_hash", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return {
        "access_token": create_access_token(user),
        "token_type": "bearer",
        "user": public_document(user),
    }

@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return public_document(user)
