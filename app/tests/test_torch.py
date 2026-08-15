import torch

print("Versión de PyTorch:", torch.__version__)
print("-" * 40)

# Verificar disponibilidad de CUDA (GPU)
cuda_disponible = torch.cuda.is_available()
print("¿CUDA está disponible?:", cuda_disponible)

if cuda_disponible:
    print("Nombre de la GPU:", torch.cuda.get_device_name(0))
    
    # Prueba rápida de creación y operación de tensores en GPU
    x = torch.randn(3, 3, device='cuda')
    y = torch.ones(3, 3, device='cuda')
    z = x + y
    print("\nPrueba de cálculo en GPU exitosa:")
    print(z)
else:
    print("PyTorch está funcionando en modo CPU.")