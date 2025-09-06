# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.users import create_user_oauth, get_user_by_google, get_user_by_microsoft, get_user_by_phone
from app.db.models.users import User
from app.shield.security import hash_password, create_access_token, create_refresh_token, encrypt_data  # <- corrigido
import random, os, jwt, smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from sqlalchemy.future import select

# ----------------------
# Twilio for OTP SMS
# ----------------------
from twilio.rest import Client
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ----------------------
# Google OAuth2
# ----------------------
from google.oauth2 import id_token
from google.auth.transport import requests
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# ----------------------
# Microsoft OAuth2
# ----------------------
from msal import ConfidentialClientApplication
MICROSOFT_CLIENT_ID = os.getenv("MICROSOFT_APP_ID")
MICROSOFT_CLIENT_SECRET = os.getenv("MICROSOFT_SECRET")
MICROSOFT_AUTHORITY = "https://login.microsoftonline.com/common"

# ----------------------
# Email (SMTP Gmail / SendGrid)
# ----------------------
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# ----------------------
# JWT reset password
# ----------------------
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30

# ----------------------
# OTP cache
# ----------------------
otp_store = {}

router = APIRouter()

# ======================
# Phone OTP
# ======================
def send_otp(phone_number: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[phone_number] = otp
    twilio_client.messages.create(
        body=f"Your OTP code is {otp}",
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
    return {"message": f"OTP sent to {phone_number}"}

@router.post("/auth/phone/verify")
async def verify_phone_otp(phone_number: str, otp: str, db: AsyncSession = Depends(get_db)):
    if not verify_otp_value(phone_number, otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user = await get_user_by_phone(db, phone_number)
    if not user:
        encrypted_phone = encrypt_data(phone_number)
        user = await create_user_oauth(
            db,
            username=phone_number,
            phone_number=encrypted_phone,
            phone_verified=True
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "user_id": str(user.id),
        "username": user.username,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# ======================
# Google OAuth2
# ======================
@router.post("/auth/google")
async def login_google(token: str, db: AsyncSession = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        google_id = idinfo['sub']
        email = idinfo['email']
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await get_user_by_google(db, google_id)
    if not user:
        encrypted_email = encrypt_data(email)
        user = await create_user_oauth(
            db,
            username=email.split('@')[0],
            email=encrypted_email,
            google_id=google_id
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "user_id": str(user.id),
        "username": user.username,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# ======================
# Microsoft OAuth2
# ======================
@router.post("/auth/microsoft")
async def login_microsoft(token: str, db: AsyncSession = Depends(get_db)):
    app_msal = ConfidentialClientApplication(
        MICROSOFT_CLIENT_ID,
        authority=MICROSOFT_AUTHORITY,
        client_credential=MICROSOFT_CLIENT_SECRET
    )
    result = app_msal.acquire_token_on_behalf_of(token, scopes=["User.Read"])
    if "error" in result:
        raise HTTPException(status_code=400, detail="Invalid token")

    microsoft_id = result["id_token_claims"]["oid"]
    email = result["id_token_claims"]["preferred_username"]

    user = await get_user_by_microsoft(db, microsoft_id)
    if not user:
        encrypted_email = encrypt_data(email)
        user = await create_user_oauth(
            db,
            username=email.split('@')[0],
            email=encrypted_email,
            microsoft_id=microsoft_id
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "user_id": str(user.id),
        "username": user.username,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

# ======================
# Password Reset via Email
# ======================
def create_reset_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def send_reset_email(email: str, token: str):
    reset_link = f"https://lyzor.com/reset-password?token={token}"  # real frontend URL
    msg = MIMEText(f"Click here to reset your password: {reset_link}")
    msg["Subject"] = "Lyzor - Password Reset"
    msg["From"] = SMTP_USER
    msg["To"] = email

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [email], msg.as_string())
    except Exception as e:
        print("Error sending email:", e)
        raise HTTPException(status_code=500, detail="Error sending email")

@router.post("/auth/forgot-password")
async def forgot_password(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(user.id)
    send_reset_email(email, token)
    return {"msg": "If the email exists, a reset link has been sent."}

@router.post("/auth/reset-password")
async def reset_password(token: str, new_password: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(new_password)  # <- corrigido
    await db.commit()
    return {"msg": "Password successfully reset"}
