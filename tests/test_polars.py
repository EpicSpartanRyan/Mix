import polars as pl

print("Versión de Polars:", pl.__version__)
print("-" * 50)

# 1. Crear un DataFrame de prueba con 1 millón de filas simuladas
print("Generando DataFrame masivo de prueba...")
data = {
    "id": range(1_000_000),
    "categoria": ["A", "B", "C", "D"] * 250_000,
    "valor": [float(i * 1.5) for i in range(1_000_000)],
    "activo": [True, False] * 500_000
}

df = pl.DataFrame(data)
print(f"DataFrame creado con éxito. Dimensiones: {df.shape}")

# 2. Prueba de consulta usando Lazy Evaluation (Evaluación perezosa) y agregaciones
print("\nEjecutando consulta optimizada con Lazy API...")

resultado = (
    df.lazy()
    .filter(pl.col("activo") == True)
    .group_by("categoria")
    .agg([
        pl.col("valor").mean().alias("valor_promedio"),
        pl.col("valor").sum().alias("valor_total"),
        pl.count("id").alias("total_registros")
    ])
    .sort("valor_total", descending=True)
    .collect() # Aquí Polars optimiza y ejecuta todo de golpe en paralelo
)

print("\nResultados de la agregación por categoría:")
print(resultado)
print("\n¡Prueba de Polars completada con éxito!")