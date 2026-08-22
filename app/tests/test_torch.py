import torch
from celery import shared_task

@shared_task
def run_torch_test():
    cuda_disponible = torch.cuda.is_available()
    print("¿CUDA está disponible?:", cuda_disponible)

    device_name = "CPU"
    tensor_result = None

    if cuda_disponible:
        device_name = torch.cuda.get_device_name(0)
        print("Nombre de la GPU:", device_name)
        
        # Prueba rápida de creación y operación de tensores en GPU
        x = torch.randn(3, 3, device='cuda')
        y = torch.ones(3, 3, device='cuda')
        z = x + y
        print("\nPrueba de cálculo en GPU exitosa:")
        print(z)
        
        # Pasamos el tensor a la CPU y lo convertimos a lista para que sea serializable en Celery
        tensor_result = z.cpu().tolist()
    else:
        print("PyTorch está funcionando en modo CPU.")
        x = torch.randn(3, 3)
        y = torch.ones(3, 3)
        z = x + y
        tensor_result = z.tolist()

    return {
        "cuda_available": cuda_disponible,
        "device_name": device_name,
        "tensor_result": tensor_result,
        "status": "¡Prueba PyTorch completada con éxito!"
    }