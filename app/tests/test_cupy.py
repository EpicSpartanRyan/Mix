import cupy as cp
from celery import shared_task


@shared_task
def run_cupy_matrix_mult():
    A_gpu = cp.ones((2000, 2000), dtype=cp.float32) * 2.0
    B_gpu = cp.ones((2000, 2000), dtype=cp.float32) * 3.0

    C_gpu = cp.dot(A_gpu, B_gpu)
    corner_result = C_gpu[:3, :3].get().tolist()

    return {
        "cupy_version": cp.__version__,
        "corner_result": corner_result,
        "status": "¡Operación matricial en GPU completada con éxito!"
    }