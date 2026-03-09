from fastapi import FastAPI
from database import engine
from models import Base
from routers.exams import router as exams_router
from auth_router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ExamPressure")
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://exam-pressure.onrender.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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