import cupy as cp

print("Versión de CuPy:", cp.__version__)
print("-" * 50)

# Multiplicación de matrices usando datos fijos (Evita totalmente 'curand')
print("Ejecutando multiplicación de matrices en GPU...")
A_gpu = cp.ones((2000, 2000), dtype=cp.float32) * 2.0
B_gpu = cp.ones((2000, 2000), dtype=cp.float32) * 3.0

C_gpu = cp.dot(A_gpu, B_gpu)

print("Resultado parcial (esquina superior 3x3):")
print(C_gpu[:3, :3])
print("¡Operación matricial en GPU completada con éxito!")