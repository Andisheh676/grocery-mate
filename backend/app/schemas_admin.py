from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ---------------------------
# User schemas
# ---------------------------
class UserAdmin(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class UserStats(BaseModel):
    total_users: int
    active_users: int
    admin_users: int
    new_users_this_month: int
