from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.users_crypto import (
    create_user_oauth, get_user_by_google,
    get_user_by_microsoft, get_user_by_phone
)

router = APIRouter()

# ----------------------
# Google OAuth
# ----------------------
@router.post("/auth/google")
async def login_google(token: str = Form(...), db: AsyncSession = Depends(get_db)):
    # Simulação de extração de dados do token
    google_id = "id_from_google_token"
    email = "email_from_google_token"

    # Verifica se usuário existe
    user = await get_user_by_google(db, google_id)
    if not user:
        # Cria usuário com criptografia
        user = await create_user_oauth(
            db,
            username=email.split('@')[0],
            email=email,
            google_id=google_id
        )
    return {"user_id": str(user.id), "username": user.username}

# ----------------------
# Microsoft OAuth
# ----------------------
@router.post("/auth/microsoft")
async def login_microsoft(token: str = Form(...), db: AsyncSession = Depends(get_db)):
    microsoft_id = "id_from_microsoft_token"
    email = "email_from_microsoft_token"

    user = await get_user_by_microsoft(db, microsoft_id)
    if not user:
        user = await create_user_oauth(
            db,
            username=email.split('@')[0],
            email=email,
            microsoft_id=microsoft_id
        )
    return {"user_id": str(user.id), "username": user.username}

# ----------------------
# Phone OTP
# ----------------------
@router.post("/auth/phone/request_otp")
async def request_otp(phone_number: str = Form(...), db: AsyncSession = Depends(get_db)):
    otp = "123456"  # gerar OTP real em produção
    return {"message": f"OTP sent to {phone_number}"}

@router.post("/auth/phone/verify")
async def verify_otp(phone_number: str = Form(...), otp: str = Form(...), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_phone(db, phone_number)
    if not user:
        user = await create_user_oauth(
            db,
            username=phone_number,
            phone_number=phone_number,
            phone_verified=True
        )
    return {"user_id": str(user.id), "username": user.username}
