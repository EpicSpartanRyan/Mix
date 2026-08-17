import time
import duckdb
import torch

start_time = time.time()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[*] Usando dispositivo: {device}")

TARGET = 100_000_000
limit = 200_000_000  
chunk_size = 50_000_000

primes = []
count = 0

print("[*] Ejecutando criba segmentada en paralelo (PyTorch/GPU)...")
for start in range(2, limit, chunk_size):
    end = min(start + chunk_size, limit)
    sieve = torch.ones(end - start, dtype=torch.bool, device=device)
    
    if start == 2:
        sieve[0] = sieve[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if start <= i*i < end:
            sieve[(i*i - start)::i] = False
        elif i*i < start:
            rem = start % i
            offset = (i - rem) if rem != 0 else 0
            sieve[offset::i] = False

    local_primes = torch.nonzero(sieve).squeeze() + start
    primes.append(local_primes.cpu())
    count += len(local_primes)
    if count >= TARGET:
        break

# Concatenar tensores y convertir a numpy limpio
all_primes_tensor = torch.cat(primes)[:TARGET]
primes_np = all_primes_tensor.numpy()

# Ingesta en DuckDB
con = duckdb.connect(':memory:')
con.register('primes_view', primes_np)
con.execute("CREATE TABLE primes AS SELECT * FROM primes_view")

print(f"[+] ¡{TARGET:,} primos calculados y cargados en DuckDB!")
max_prime = con.execute("SELECT MAX(column0) FROM primes").fetchone()[0]
print(f"  -> El primo número 10,000,000 es: {max_prime}")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"⏱️ Tiempo total de ejecución: {elapsed_time:.4f} segundos")