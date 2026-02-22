from pydantic import BaseModel
from typing import Dict


class StartExamRequest(BaseModel):
    user_id: str


class SubmitExamRequest(BaseModel):
    exam_id: int
    answers: Dict[int, str]