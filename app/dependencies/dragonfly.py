import os
from contextlib import contextmanager
from functools import wraps
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

# For celery tasks, we need a way to get a session without using Depends.
def with_dragonfly(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        with dragonfly_context() as client:
            return function(client, *args, **kwargs)

    return wrapper


def get_dragonfly():
    with dragonfly_context() as client:
        yield client

# For FastAPI routes, we can use Depends to inject the session.
DragonflyDep = Annotated[redis.Redis, Depends(get_dragonfly)]
