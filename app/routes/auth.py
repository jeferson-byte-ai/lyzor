from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.users import create_user_oauth, get_user_by_google, get_user_by_microsoft, get_user_by_phone
import random

# Twilio
from twilio.rest import Client
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Google OAuth2
from google.oauth2 import id_token
from google.auth.transport import requests
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"

# Microsoft OAuth2
from msal import ConfidentialClientApplication
MICROSOFT_CLIENT_ID = "YOUR_MICROSOFT_APP_ID"
MICROSOFT_CLIENT_SECRET = "YOUR_MICROSOFT_SECRET"
MICROSOFT_AUTHORITY = "https://login.microsoftonline.com/common"

# OTP cache simples
otp_store = {}

router = APIRouter()

# ===== OTP SMS =====
def send_otp(phone_number: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[phone_number] = otp
    twilio_client.messages.create(
        body=f"Seu código OTP é {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp

def verify_otp_value(phone_number: str, otp: str) -> bool:
    valid = otp_store.get(phone_number) == otp
    if valid:
        del otp_store[phone_number]
    return valid

@router.post("/auth/phone/request_otp")
async def request_otp(phone_number: str):
    send_otp(phone_number)
    return {"message": f"OTP enviado para {phone_number}"}

@router.post("/auth/phone/verify")
async def verify_phone_otp(phone_number: str, otp: str, db: AsyncSession = Depends(get_db)):
    if not verify_otp_value(phone_number, otp):
        raise HTTPException(status_code=400, detail="OTP inválido")
    user = await get_user_by_phone(db, phone_number)
    if not user:
        user = await create_user_oauth(db, username=phone_number, phone_number=phone_number, phone_verified=True)
    return {"user_id": str(user.id), "username": user.username}

# ===== Google OAuth2 =====
@router.post("/auth/google")
async def login_google(token: str, db: AsyncSession = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        google_id = idinfo['sub']
        email = idinfo['email']
    except ValueError:
        raise HTTPException(status_code=400, detail="Token inválido")
    user = await get_user_by_google(db, google_id)
    if not user:
        user = await create_user_oauth(db, username=email.split('@')[0], email=email, google_id=google_id)
    return {"user_id": str(user.id), "username": user.username}

# ===== Microsoft OAuth2 =====
@router.post("/auth/microsoft")
async def login_microsoft(token: str, db: AsyncSession = Depends(get_db)):
    app_msal = ConfidentialClientApplication(
        MICROSOFT_CLIENT_ID,
        authority=MICROSOFT_AUTHORITY,
        client_credential=MICROSOFT_CLIENT_SECRET
    )
    result = app_msal.acquire_token_on_behalf_of(token, scopes=["User.Read"])
    if "error" in result:
        raise HTTPException(status_code=400, detail="Token inválido")
    microsoft_id = result["id_token_claims"]["oid"]
    email = result["id_token_claims"]["preferred_username"]
    user = await get_user_by_microsoft(db, microsoft_id)
    if not user:
        user = await create_user_oauth(db, username=email.split('@')[0], email=email, microsoft_id=microsoft_id)
    return {"user_id": str(user.id), "username": user.username}
