import duckdb
import polars as pl

print("Versión de DuckDB:", duckdb.__version__)
print("-" * 50)

# 1. Crear un dataset de prueba rápido usando Polars y guardarlo en formato Parquet
print("Generando archivo Parquet de prueba ('datos_prueba.parquet')...")
df_temp = pl.DataFrame({
    "id": range(500_000),
    "departamento": ["Ventas", "IT", "Finanzas", "Marketing"] * 125_000,
    "salario": [float(30000 + (i % 50000)) for i in range(500_000)],
    "experiencia_anios": [i % 15 for i in range(500_000)]
})
df_temp.write_parquet("datos_prueba.parquet")
print("¡Archivo Parquet creado con éxito!\n")

# 2. Conectar a DuckDB (modo en memoria local) y consultar el archivo Parquet usando SQL
print("Ejecutando consulta analítica con SQL directamente sobre el archivo Parquet...")

query = """
    SELECT 
        departamento,
        COUNT(*) AS total_empleados,
        ROUND(AVG(salario), 2) AS salario_promedio,
        MAX(experiencia_anios) AS max_experiencia
    FROM 'datos_prueba.parquet'
    WHERE experiencia_anios > 3
    GROUP BY departamento
    ORDER BY salario_promedio DESC;
"""

# DuckDB ejecuta la consulta optimizada directamente sobre el motor columnar
resultado_duckdb = duckdb.sql(query).fetchall()
column_names = [desc[0] for desc in duckdb.sql(query).description]

print("\nResultados de la consulta analítica en DuckDB:")
print(" | ".join(column_names))
print("-" * 55)
for row in resultado_duckdb:
    print(row)

print("\n¡Prueba de DuckDB y Parquet completada con éxito!")