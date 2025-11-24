import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

import jwt
from passlib.context import CryptContext

from app.database import get_db
from app import model, schemas

import razorpay

# Config
JWT_SECRET = os.getenv("JWT_SECRET") or "CHANGE_ME_SECRET"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])



# # -------------------- (RAZORPAYX CLIENT) ----------------------------
# RAZORPAYX_KEY_ID = os.getenv("RAZORPAYX_KEY_ID")
# RAZORPAYX_KEY_SECRET = os.getenv("RAZORPAYX_KEY_SECRET")

# razorpayx = razorpay.Client(auth=(RAZORPAYX_KEY_ID, RAZORPAYX_KEY_SECRET))
# # ---------------------------------------------------------------------------




# --- helper utils -----------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.utcnow()
    exp = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": str(subject), "exp": exp, "iat": now}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# --- user CRUD helpers -------------------------------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_user_by_id(db: Session, user_id):
    return db.query(model.User).filter(model.User.id == user_id).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    existing = get_user_by_email(db, user_in.email)
    if existing:
        return None
    hashed = hash_password(user_in.password)
    user = model.User(
        email=user_in.email,
        hashed_password=hashed,
        name=user_in.name,
        phone=user_in.phone,
        upi_id=user_in.upi_id,
        is_active=True,
        is_superuser=False,
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # # ----------------------------------------------------
    # # ----------------------------------------------------
    # # ----------------------------------------------------
    # # ----------------------------------------------------
    # # Create Razorpay Contact
    # contact = razorpayx.contact.create({
    #     "name": user.name,
    #     "email": user.email,
    #     "contact": user.phone,
    #     "type": "vendor"
    # })

    # # Create Fund Account (UPI)
    # fund_account = razorpayx.fund_account.create({
    #     "contact_id": contact["id"],
    #     "account_type": "vpa",
    #     "vpa": {
    #         "address": user.upi_id
    #     }
    # })

    # # Save IDs to database
    # user.razorpay_contact_id = contact["id"]
    # user.fund_account_id = fund_account["id"]

    # db.commit()
    # db.refresh(user)
    # # ---------------------------------------------------------------------------
    # # ---------------------------------------------------------------------------
    # # ---------------------------------------------------------------------------
    # # ---------------------------------------------------------------------------
    # # ---------------------------------------------------------------------------



    return user

# --- routes -------------------------------------
@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    created = create_user(db, user)
    if created is None:
        raise HTTPException(status_code=400, detail="REGISTER_USER_ALREADY_EXISTS")
    # do NOT return password
    return created

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/jwt/login", response_model=schemas.Token)
def jwt_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 form uses "username" for email
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

# --- dependency to get current user -----------------------
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

# dependency for "active user"
def current_active_user(user = Depends(get_current_user)):
    return user


@router.get("/me", response_model=schemas.UserRead)
def me(user = Depends(current_active_user)):
    return user
