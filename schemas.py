from pydantic import BaseModel, EmailStr, Field
from typing import Dict


# Request to start an exam
class StartExamRequest(BaseModel):
    user_id: str


# Request to submit exam answers
class SubmitExamRequest(BaseModel):
    exam_id: int
    answers: Dict[int, str]


# Register request
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=50)
    full_name: str| None=None


# Login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str= Field(..., min_length=6, max_length=50)
    full_name: str| None=None