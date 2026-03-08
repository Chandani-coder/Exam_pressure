from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import ExamAttempt


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_exam_unlocked(exam_id: int, db: Session = Depends(get_db)):
    exam = db.query(ExamAttempt).filter(ExamAttempt.id == exam_id).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if not exam.submitted_at:
        raise HTTPException(status_code=400, detail="Exam not submitted yet")

    if exam.analysis_unlocks_at and datetime.utcnow() < exam.analysis_unlocks_at:
        raise HTTPException(status_code=403, detail="Analysis locked")

    return exam