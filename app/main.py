from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import Task
from app.tasks import process_task, send_email_task
import uuid

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Queue API")

@app.post("/tasks/")
def create_task(name: str, db: Session = Depends(get_db)):
    # Tạo task record trong DB với status pending
    task = Task(name=name)
    db.add(task)
    db.commit()
    db.refresh(task)

    # Gửi task vào Celery — không chờ, trả về ngay
    process_task.delay(name, str(task.id))

    return {"task_id": str(task.id), "status": task.status}

@app.get("/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return {"error": "Task not found"}
    return {"task_id": str(task.id), "name": task.name, "status": task.status, "result": task.result}

@app.post("/send-email/")
def send_email(to: str, subject: str, body: str, db: Session = Depends(get_db)):
    # Tạo task record trong DB với status pending
    task = Task(name=f"Send email to {to}")
    db.add(task)
    db.commit()
    db.refresh(task)

    # Gửi task vào Celery — không chờ, trả về ngay  
    send_email_task.delay(to, subject, body, str(task.id))

    return {"task_id": str(task.id), "status": task.status}