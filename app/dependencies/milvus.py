import os
import time
from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from pymilvus import MilvusClient

MILVUS_HOST = os.getenv("MILVUS_HOST", "milvus-standalone")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")


@contextmanager
def milvus_context():
    for attempt in range(5):
        try:
            client = MilvusClient(uri=f"http://{MILVUS_HOST}:{MILVUS_PORT}")
            try:
                yield client
            finally:
                client.close()
            return
        except Exception:
            if attempt == 4:
                raise
            time.sleep(3)


def get_milvus():
    with milvus_context() as client:
        yield client


MilvusDep = Annotated[MilvusClient, Depends(get_milvus)]
