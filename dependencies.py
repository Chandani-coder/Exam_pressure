from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime
from jose import JWTError, jwt
import os

from database import SessionLocal
from models import User, ExamAttempt

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("RAW TOKEN:", token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("DECODED PAYLOAD:", payload)

        email: str = payload.get("sub")
        print("EMAIL FROM TOKEN:", email)

        if email is None:
            print("EMAIL IS NONE — token has no 'sub' field")
            raise credentials_exception

    except JWTError as e:
        print("JWT ERROR:", e)
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    print("USER FOUND:", user)

    if user is None:
        print("USER NOT FOUND IN DB for email:", email)
        raise credentials_exception

    return user


def check_exam_unlocked(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(ExamAttempt).filter(ExamAttempt.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if not exam.submitted_at:
        raise HTTPException(status_code=400, detail="Exam not submitted yet")

    if exam.analysis_unlocks_at and datetime.utcnow() < exam.analysis_unlocks_at:
        raise HTTPException(status_code=403, detail="Analysis locked")

    return exam