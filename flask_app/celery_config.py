import os

from celery import Celery
# from app import app

celery = Celery("task", backend="redis://localhost:6379/0", broker="redis://localhost:6379/0", include=["tasks"])   #os.getenv("CELERY_BROKER_URL"))