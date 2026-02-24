from fastapi import  FastAPI,APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import SessionLocal
from models import Question, QuestionVariation, ExamAttempt,User
from schemas import StartExamRequest, SubmitExamRequest
from services import log_mistake, generate_variation
from auth import get_current_user
import random

router = APIRouter(prefix="/exams", tags=["Exams"])
app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/seed")
def seed_questions(db: Session = Depends(get_db)):
    if db.query(Question).first():
        return {"message": "Already seeded"}

    questions = [
        Question(
            content="What is 2 + 2?",
            options=["3", "4", "5", "6"],
            correct_option="4",
            source="Math",
            mistake_type="KNOWLEDGE"
        ),
        Question(
            content="Which is NOT prime?",
            options=["2", "3", "4", "5"],
            correct_option="4",
            source="Math",
            mistake_type="TRAP"
        ),
        Question(
            content="If x = 5, what is x²?",
            options=["10", "15", "20", "25"],
            correct_option="25",
            source="Algebra",
            mistake_type="TIME"
        )
    ]

    db.add_all(questions)
    db.commit()

    return {"message": "Seeded"}


@router.post("/start")
def start_exam(current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):

    active = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.submitted_at == None
    ).first()

    if active:
        raise HTTPException(status_code=400, detail="Active exam exists")

    start_time = datetime.utcnow()
    end_time = start_time + timedelta(minutes=2)

    exam = ExamAttempt( 
        user_id=current_user.id,
        started_at=start_time,
        end_time=end_time
    )

    db.add(exam)
    db.commit()
    db.refresh(exam)

    questions = db.query(Question).all()
    response_questions = []

    for q in questions:
        if random.random() < 0.25:
            var_data = generate_variation(q)

            variation = QuestionVariation(
                source_question_id=q.id,
                variation_content=var_data["variation_content"],
                options=var_data["options"],
                correct_option=var_data["correct_option"],
                trap_option=var_data["trap_option"],
                mistake_tag=var_data["mistake_tag"],
                explanation=var_data["explanation"]
            )

            db.add(variation)
            db.commit()
            db.refresh(variation)

            response_questions.append({
                "id": variation.id,
                "content": variation.variation_content,
                "options": variation.options
            })
        else:
            response_questions.append({
                "id": q.id,
                "content": q.content,
                "options": q.options
            })

    return {
        "exam_id": exam.id,
        "end_time": exam.end_time,
        "questions": response_questions
    }


@router.post("/submit")
def submit_exam(
    payload: SubmitExamRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    exam = db.query(ExamAttempt).filter(
        ExamAttempt.id == payload.exam_id
    ).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if exam.submitted_at:
        raise HTTPException(status_code=400, detail="Already submitted")

    if datetime.utcnow() > exam.end_time:
        exam.is_flagged = True

    score = 0

    for q_id, selected in payload.answers.items():

        question = db.query(Question).filter(
            Question.id == q_id
        ).first()

        if question:
            correct = question.correct_option
            mistake_type = question.mistake_type
        else:
            variation = db.query(QuestionVariation).filter(
                QuestionVariation.id == q_id
            ).first()
            if not variation:
                continue
            correct = variation.correct_option
            mistake_type = variation.mistake_tag

        if selected == correct:
            score += 1
        else:
            background_tasks.add_task(
                log_mistake,
                exam.user_id,
                q_id,
                selected,
                correct,
                mistake_type
            )

    exam.score = score
    exam.submitted_at = datetime.utcnow()
    exam.analysis_unlocks_at=datetime.utcnow() + timedelta(hours=2)

    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return {"score": score, "flagged": exam.is_flagged}


@router.get("/today-focus")
def today_focus(user_id: str, db: Session = Depends(get_db)):

    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == user_id,
        ExamAttempt.submitted_at != None
    ).order_by(ExamAttempt.id.desc()).limit(3).all()

    if len(attempts) < 3:
        return {"message": "Not enough data"}

    scores = [a.score for a in attempts]

    if scores[0] < scores[1] < scores[2]:
        return {
            "status": "DEATH_SPIRAL_DETECTED",
            "difficulty": "LOW"
        }
    return {"status": "STABLE"}

@router.get("/results/{exam_id}")
def get_results(exam_id: int, db: Session = Depends(get_db)):

    exam = db.query(ExamAttempt).filter(
        ExamAttempt.id == exam_id
    ).first()

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    if not exam.submitted_at:
        raise HTTPException(status_code=400, detail="Exam not submitted yet")

    if exam.analysis_unlocks_at and datetime.utcnow() < exam.analysis_unlocks_at:
        raise HTTPException(
            status_code=403,
            detail="Analysis Locked. Return later."
        )

    return {
        "score": exam.score,
        "flagged": exam.is_flagged
    }

app.include_router(router)