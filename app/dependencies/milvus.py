import os
import time
from contextlib import contextmanager
from functools import wraps
from typing import Annotated

from fastapi import Depends
from pymilvus import MilvusClient

MILVUS_HOST = os.getenv("MILVUS_HOST", "milvus-standalone")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
MILVUS_MAX_RETRIES = int(os.getenv("MILVUS_MAX_RETRIES", 5))
MILVUS_RETRY_DELAY = float(os.getenv("MILVUS_RETRY_DELAY", 3))


@contextmanager
def milvus_context():
    for attempt in range(MILVUS_MAX_RETRIES):
        try:
            client = MilvusClient(uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}")
            try:
                yield client
            finally:
                client.close()
            return
        except Exception:
            if attempt == MILVUS_MAX_RETRIES - 1:
                raise
            time.sleep(MILVUS_RETRY_DELAY)

# For celery tasks, we need a way to get a session without using Depends.
def with_milvus(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        with milvus_context() as client:
            return function(client, *args, **kwargs)

    return wrapper


def get_milvus():
    with milvus_context() as client:
        yield client

# For FastAPI routes, we can use Depends to inject the session.
MilvusDep = Annotated[MilvusClient, Depends(get_milvus)]
