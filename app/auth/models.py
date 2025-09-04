from pydantic import BaseModel
from typing import Optional, List

# ----------------------------
# Authentication provider
# ----------------------------
class AuthProvider(BaseModel):
    type: str             # 'email', 'google', 'microsoft', 'phone'
    identifier: str       # email or phone or provider id
    password_hash: Optional[str] = None
    token: Optional[str] = None          # for phone OTP

# ----------------------------
# User account model
# ----------------------------
class UserAccount(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
    phone_number: Optional[str] = None
    providers: List[AuthProvider] = []
