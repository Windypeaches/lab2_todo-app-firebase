from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth

from database import SessionLocal, engine
from models import TaskDB

app = FastAPI()

# tạo bảng DB
TaskDB.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Firebase init
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# model
class Task(BaseModel):
    title: str

# verify token
def verify_token(authorization: str):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        token = authorization.split(" ")[1]
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

# API test
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

# CREATE TASK
@app.post("/tasks")
def create_task(task: Task, authorization: str = Header(None)):
    user = verify_token(authorization)

    db = SessionLocal()

    new_task = TaskDB(
        title=task.title,
        user=user["uid"],
        completed=False
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    db.close()

    return {"message": "Task created"}

# GET TASKS
@app.get("/tasks")
def get_tasks(authorization: str = Header(None)):
    user = verify_token(authorization)

    db = SessionLocal()

    tasks = db.query(TaskDB).filter(TaskDB.user == user["uid"]).all()

    db.close()

    return [
        {
            "id": t.id,
            "title": t.title,
            "user": t.user,
            "completed": t.completed
        }
        for t in tasks
    ]

# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, authorization: str = Header(None)):
    user = verify_token(authorization)

    db = SessionLocal()

    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user == user["uid"]
    ).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    db.close()

    return {"message": "Task deleted"}

# UPDATE
@app.put("/tasks/{task_id}")
def update_task(task_id: int, authorization: str = Header(None)):
    user = verify_token(authorization)

    db = SessionLocal()

    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user == user["uid"]
    ).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = not task.completed

    db.commit()
    db.close()

    return {"message": "Updated"}