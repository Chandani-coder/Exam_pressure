from pydantic import BaseModel,EmailStr,Field
from typing import Dict


class StartExamRequest(BaseModel):
    user_id: str


class SubmitExamRequest(BaseModel):
    exam_id: int
    answers: Dict[int, str]

class RegisterRequest(BaseModel):
    email:EmailStr
    password:str =Field(...,min_lenth=6,max_length=50)