from fastapi import APIRouter

from tests.test_cupy import run_cupy_matrix_mult
from tests.test_dragonfly import test_dragonfly_connection
from tests.test_duckdb import run_duckdb_test
from tests.test_emqx import test_emqx_connection
from tests.test_milvus import test_milvus_connection
from tests.test_oceanbase import test_oceanbase_connection
from tests.test_polars import run_polars_test
from tests.test_torch import run_torch_test

router = APIRouter(tags=["tests"])


@router.get("/run-cupy")
async def trigger_cupy_task():
    task = run_cupy_matrix_mult.delay()
    return {"message": "Test cupy iniciado", "task_id": task.id}


@router.get("/run-dragonfly")
async def trigger_dragonfly_task():
    task = test_dragonfly_connection.delay()
    return {"message": "Test dragonfly iniciado", "task_id": task.id}


@router.get("/run-duckdb")
async def trigger_duckdb_task():
    task = run_duckdb_test.delay()
    return {"message": "Test DuckDB iniciado", "task_id": task.id}


@router.get("/run-emqx")
async def trigger_emqx_task():
    task = test_emqx_connection.delay()
    return {"message": "Test EMQX iniciado", "task_id": task.id}


@router.get("/run-milvus")
async def trigger_milvus_task():
    task = test_milvus_connection.delay()
    return {"message": "Test Milvus iniciado", "task_id": task.id}


@router.get("/run-oceanbase")
async def trigger_oceanbase_task():
    task = test_oceanbase_connection.delay()
    return {"message": "Test OceanBase iniciado", "task_id": task.id}


@router.get("/run-polars")
async def trigger_polars_task():
    task = run_polars_test.delay()
    return {"message": "Test Polars iniciado", "task_id": task.id}


@router.get("/run-pytorch")
async def trigger_pytorch_task():
    task = run_torch_test.delay()
    return {"message": "Test Pytorch iniciado", "task_id": task.id}
