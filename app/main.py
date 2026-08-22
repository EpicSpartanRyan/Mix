import os

from celery import Celery
from fastapi import FastAPI
from tests.test_cupy import run_cupy_matrix_mult

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://dragonfly:6379/0")
RESULT_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://dragonfly:6379/0")

app = FastAPI()

celery = Celery(
    __name__,
    broker=BROKER_URL,
    backend=RESULT_URL
)

celery.autodiscover_tasks(['tests'])

@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y


@app.get("/")
async def root():
    task = divide.delay(1, 2)
    return {"message": "Hello World"}


@app.get("/run-gpu")
async def trigger_gpu_task():
    task = run_cupy_matrix_mult.delay()
    return {"message": "Tarea de GPU iniciada", "task_id": task.id}