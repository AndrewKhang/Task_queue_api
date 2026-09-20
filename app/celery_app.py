from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery_app = Celery(
    "task_queue",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL"),
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
)

# Import tasks sau khi celery_app đã được tạo
import app.tasks