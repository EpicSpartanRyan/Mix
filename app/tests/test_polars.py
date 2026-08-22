import polars as pl
from celery import shared_task

@shared_task
def run_polars_test():
    print("Generando DataFrame masivo de prueba...")
    data = {
        "id": range(1_000_000),
        "categoria": ["A", "B", "C", "D"] * 250_000,
        "valor": [float(i * 1.5) for i in range(1_000_000)],
        "activo": [True, False] * 500_000
    }

    df = pl.DataFrame(data)
    print(f"DataFrame creado con éxito. Dimensiones: {df.shape}")

    # Prueba de consulta usando Lazy Evaluation (Evaluación perezosa) y agregaciones
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
        .collect()
    )

    print("\nResultados de la agregación por categoría:")
    print(resultado)
    print("\n¡Prueba de Polars completada con éxito!")

    # Convertimos el DataFrame de Polars a un diccionario serializable para Celery
    return {
        "shape": list(df.shape),
        "result": resultado.to_dicts(),
        "status": "¡Prueba de Polars completada con éxito!"
    }