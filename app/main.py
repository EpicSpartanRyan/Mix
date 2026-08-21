from celery import Celery
from fastapi import FastAPI
import os

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://dragonfly:6379/0")
RESULT_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://dragonfly:6379/0")

app = FastAPI()

celery = Celery(
    __name__,
    broker=BROKER_URL,
    backend=RESULT_URL
)


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y


@app.get("/")
async def root():
    task = divide.delay(1, 2)
    return {"message": "Hello World"}


