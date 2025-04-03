from flask_app.celery_config import celery


@celery.task
def task(x, y):
    return x + y