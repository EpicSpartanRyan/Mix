import time

from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility,
)

# Configuración de conexión (usando el nombre del servicio en la red de Docker, 
# o "localhost" si lo corres directamente desde tu máquina host)
HOST = "milvus-standalone"
PORT = "19530"

def test_milvus_connection():
    print(f"[*] Conectando a Milvus en {HOST}:{PORT}...")
    
    # Intentar conectar con reintentos por si Milvus acaba de arrancar
    connected = False
    for i in range(5):
        try:
            connections.connect("default", host=HOST, port=PORT)
            connected = True
            print("[+] ¡Conexión exitosa a Milvus!")
            break
        except Exception as e:
            print(f"[-] Intento {i+1}/5 fallido. Reintentando en 3 segundos...")
            time.sleep(3)
            
    if not connected:
        print("[X] No se pudo establecer conexión con Milvus.")
        return

    collection_name = "test_vector_collection"

    # Limpiar si ya existía de una prueba anterior
    if utility.has_collection(collection_name):
        print(f"[*] Eliminando colección anterior '{collection_name}'...")
        utility.drop_collection(collection_name)

    # Definir el esquema de la colección
    print(f"[*] Creando esquema para '{collection_name}'...")
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=4), # Vector de 4 dimensiones para la prueba
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=200)
    ]
    schema = CollectionSchema(fields=fields, description="Colección de prueba para Milvus")
    
    # Crear la colección
    collection = Collection(name=collection_name, schema=schema)
    print("[+] Colección creada exitosamente.")

    # Insertar datos de prueba
    print("[*] Insertando vectores de prueba...")
    vectors = [
        [0.1, 0.2, 0.3, 0.4],
        [0.5, 0.6, 0.7, 0.8],
        [0.9, 1.0, 1.1, 1.2]
    ]
    texts = [
        "Primer vector de prueba",
        "Segundo vector de prueba",
        "Tercer vector de prueba"
    ]
    
    insert_result = collection.insert([vectors, texts])
    collection.flush()
    print(f"[+] Datos insertados. IDs generados: {insert_result.primary_keys}")

    # Crear un índice para la búsqueda vectorial
    print("[*] Creando índice vectorial...")
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="vector", index_params=index_params)
    collection.load()
    print("[+] Índice creado y colección cargada en memoria.")

    # Realizar una búsqueda de similitud
    print("[*] Realizando búsqueda vectorial...")
    search_vectors = [[0.1, 0.2, 0.3, 0.4]] # Debería coincidir altamente con el primer vector
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    
    results = collection.search(
        data=search_vectors,
        anns_field="vector",
        param=search_params,
        limit=2,
        output_fields=["text"]
    )

    print("\n--- Resultados de la Búsqueda ---")
    for hits in results:
        for hit in hits:
            print(f"ID: {hit.id} | Distancia: {hit.distance:.4f} | Texto: {hit.entity.get('text')}")

    # Limpiar al terminar la prueba
    utility.drop_collection(collection_name)
    print("\n[+] Prueba finalizada con éxito y recursos limpios.")
    connections.disconnect("default")

if __name__ == "__main__":
    test_milvus_connection()