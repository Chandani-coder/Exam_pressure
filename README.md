# ExamPressure 

A backend system that simulates real exam pressure — timed tests, trap questions, and mistake tracking to help students improve performance under stress.

##  Live API
https://exam-pressure.onrender.com/docs

##  Tech Stack
| Technology | Usage |
|------------|-------|
| FastAPI | REST API framework |
| PostgreSQL | Production database |
| SQLAlchemy | ORM |
| JWT (python-jose) | Authentication |
| Passlib + Bcrypt | Password hashing |
| Render | Deployment |

## ✨ Features
-  User Registration & Login with JWT Authentication
-  Timed Exam Attempts with auto-flagging if submitted late
-  Trap Questions — 25% chance of getting a variation with misleading options
-  Mistake Logging — tracks wrong answers in background
-  Analysis Lock — results unlock after 2 hours to simulate real exam review
-  Protected Routes — all exam routes require valid JWT token

##  API Endpoints
| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login  | Login & get JWT token |
| GET | /auth/me  | Get current user info |
| POST | /exams/seed  | Seed initial questions |
| POST | /exams/start  | Start a timed exam |
| POST | /exams/submit  | Submit exam answers |
| GET | /exams/results/{id} | Get exam results |
| GET | /exams/today-focus  | Get focus recommendation |

##  Database Models
- **User** — stores registered users
- **Question** — original exam questions
- **QuestionVariation** — trap variations of questions
- **ExamAttempt** — tracks each exam session
- **MistakeLog** — logs wrong answers for analysis

##  Run Locally
```bash
# Clone the repo
git clone https://github.com/Chandani-coder/Exam_pressure
cd Exam_pressure

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload
```

##  Environment Variables
```
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://your-db-url
```
