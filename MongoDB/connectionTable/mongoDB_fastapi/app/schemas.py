from pydantic import BaseModel, EmailStr, Field, ConfigDict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "customer"
    phone: str | None = None

class UserPatch(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    role: str | None = None
    phone: str | None = None
    status: str | None = None

class GenericDocument(BaseModel):
    model_config = ConfigDict(extra="allow")
