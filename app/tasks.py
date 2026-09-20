import time
from app.celery_app import celery_app
from app.database import SessionLocal
from app.models import Task
import uuid

@celery_app.task
def process_task(task_name: str, task_id: str) -> str:
    db = SessionLocal()
    try:
        # Update status → processing
        task = db.query(Task).filter(Task.id == uuid.UUID(task_id)).first()
        task.status = "processing"
        db.commit()

        # Giả lập task tốn thời gian
        time.sleep(5)
        result = f"Task '{task_name}' completed successfully"

        # Update status → done
        task.status = "done"
        task.result = result
        db.commit()

        return result
    except Exception as e:
        task.status = "failed"
        task.result = str(e)
        db.commit()
        raise
    finally:
        db.close()

@celery_app.task
def send_email_task(to: str, subject: str, body: str, task_id: str) -> str:
    db = SessionLocal()
    try:
        # Update status → processing
        task = db.query(Task).filter(Task.id == uuid.UUID(task_id)).first()
        task.status = "processing"
        db.commit()

        email_data = {
            "to": to,
            "subject": subject,
            "body": body
        }

        # Update status → done
        result = f"Email sent to {to} with subject '{subject}'"
        task.status = "done"
        task.result = result
        db.commit()

        return result
    except Exception as e:
        task.status = "failed"
        task.result = str(e)
        db.commit()
        raise
    finally:
        db.close()