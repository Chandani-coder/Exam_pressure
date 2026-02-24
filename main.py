from fastapi import FastAPI
from database import engine
from models import Base
from routers.exams import router as exams_router
from auth_router import router as auth_router

app = FastAPI(title="ExamPressure")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(exams_router)


@app.get("/")
def home():
    return {
        "service": "ExamPressure",
        "status": "live",
        "docs": "/docs"
    }