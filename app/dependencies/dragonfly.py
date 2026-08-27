import os
from contextlib import contextmanager
from typing import Annotated

import redis
from fastapi import Depends

DRAGONFLY_HOST = os.getenv("DRAGONFLY_HOST", "dragonfly")
DRAGONFLY_PORT = int(os.getenv("DRAGONFLY_PORT", 6379))


@contextmanager
def dragonfly_context():
    client = redis.Redis(
        host=DRAGONFLY_HOST,
        port=DRAGONFLY_PORT,
        decode_responses=True,
    )
    try:
        yield client
    finally:
        client.close()


def get_dragonfly():
    with dragonfly_context() as client:
        yield client


DragonflyDep = Annotated[redis.Redis, Depends(get_dragonfly)]
