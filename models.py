from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    exam_attempts = relationship("ExamAttempt", back_populates="user")
    mistake_logs = relationship("MistakeLog", back_populates="user")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)
    source = Column(String, nullable=False)
    mistake_type = Column(String, nullable=False)

    variations = relationship("QuestionVariation", back_populates="source_question")
    mistake_logs = relationship("MistakeLog", back_populates="question")


class QuestionVariation(Base):
    __tablename__ = "question_variations"

    id = Column(Integer, primary_key=True, index=True)
    source_question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    variation_content = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    correct_option = Column(String, nullable=False)
    trap_option = Column(String, nullable=False)
    mistake_tag = Column(String, nullable=False)
    explanation = Column(String, nullable=False)

    source_question = relationship("Question", back_populates="variations")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    analysis_unlocks_at = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=True)
    is_flagged = Column(Boolean, default=False)

    user = relationship("User", back_populates="exam_attempts")


class MistakeLog(Base):
    __tablename__ = "mistake_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_option = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    mistake_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mistake_logs")
    question = relationship("Question", back_populates="mistake_logs")