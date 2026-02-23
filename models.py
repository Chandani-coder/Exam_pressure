from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)
    source = Column(String, nullable=False)
    mistake_type = Column(String, nullable=False)


class QuestionVariation(Base):
    __tablename__ = "question_variations"

    id = Column(Integer, primary_key=True, index=True)
    source_question_id = Column(Integer, nullable=False, index=True)
    variation_content = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)
    trap_option = Column(String, nullable=False)
    mistake_tag = Column(String, nullable=False)
    explanation = Column(String, nullable=False)


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    analysis_unlocks_at=Column(DateTime,nullable=True)
    score = Column(Integer, nullable=True)
    is_flagged = Column(Boolean, default=False)


class MistakeLog(Base):
    __tablename__ = "mistake_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, index=True)
    question_id = Column(Integer, nullable=False, index=True)
    selected_option = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    mistake_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)