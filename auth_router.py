from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models import User
from auth import hash_password, verify_password, create_access_token
from schemas import RegisterRequest, LoginRequest
from dependencies import get_current_user, get_db  

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "user": {
            "id": user.id,          #  was returning user.email as id, fixed to user.id
            "email": user.email,    #  added email to response
            "full_name": user.full_name,
            "created_at": user.created_at
        }
    }


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "user": {
            "id": user.id,          
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at
        },
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name
    }