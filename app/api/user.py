from fastapi import APIRouter
from app.models import UserInfo

router = APIRouter()

# Fake user storage
FAKE_USER = {"username": "Jeferson", "email": "jeferson@example.com"}

@router.get("/info")
def get_user_info():
    return UserInfo(**FAKE_USER)

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.delete("/")
def delete_account():
    return {"message": "Account deleted successfully"}
