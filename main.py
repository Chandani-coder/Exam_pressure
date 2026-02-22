from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from database import engine
from models import Base
from routers import exams

app = FastAPI(
    title="ExamPressure API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def lock_middleware(request: Request, call_next):
    response = await call_next(request)
    return response


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(exams.router)