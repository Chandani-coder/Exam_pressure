import random
from datetime import datetime
from models import MistakeLog, QuestionVariation
from database import SessionLocal


TRAP_TYPES = ["TRAP_CONFUSION", "CONTEXT_SHIFT", "LINGUISTIC_COMPLEXITY"]


def classify_mistake(question):
    return question.mistake_type


def log_mistake(user_id, question_id, selected_option, correct_option, mistake_type):
    db = SessionLocal()
    try:
        mistake = MistakeLog(
            user_id=user_id,
            question_id=question_id,
            selected_option=selected_option,
            correct_option=correct_option,
            mistake_type=mistake_type,
            created_at=datetime.utcnow()
        )
        db.add(mistake)
        db.commit()
    finally:
        db.close()


def generate_variation(source_question):
    selected_trap = random.choice(TRAP_TYPES)

    modified_content = source_question.content + " (Read carefully.)"
    options = source_question.options.copy()

    if len(options) >= 2:
        options[0], options[1] = options[1], options[0]

    return {
        "variation_content": modified_content,
        "options": options,
        "correct_option": source_question.correct_option,
        "trap_option": options[0],
        "mistake_tag": selected_trap,
        "explanation": "Generated variation to simulate trap condition."
    }