import time
import warnings
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    connections,
    utility,
    PyMilvusDeprecationWarning
)

# Suprimir advertencias de deprecación
warnings.filterwarnings("ignore", category=PyMilvusDeprecationWarning)

HOST = "milvus-standalone"
PORT = "19530"

def test_milvus_connection():
    print(f"[*] Conectando a Milvus ({HOST}:{PORT})...")
    
    connected = False
    for i in range(5):
        try:
            connections.connect("default", host=HOST, port=PORT)
            connected = True
            break
        except Exception:
            time.sleep(3)
            
    if not connected:
        print("[X] Error: No se pudo conectar a Milvus.")
        return

    collection_name = "test_vector_collection"

    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=4),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=200)
    ]
    schema = CollectionSchema(fields=fields, description="Colección de prueba")
    collection = Collection(name=collection_name, schema=schema)

    vectors = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8], [0.9, 1.0, 1.1, 1.2]]
    texts = ["Primer vector", "Segundo vector", "Tercer vector"]
    
    collection.insert([vectors, texts])
    collection.flush()

    collection.create_index("vector", {"metric_type": "L2", "index_type": "IVF_FLAT", "params": {"nlist": 128}})
    collection.load()

    results = collection.search(
        data=[[0.1, 0.2, 0.3, 0.4]],
        anns_field="vector",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=2,
        output_fields=["text"]
    )

    print("[+] Conexión y operaciones exitosas.")
    print("--- Resultados de Búsqueda ---")
    for hits in results:
        for hit in hits:
            print(f"  -> Match: '{hit.entity.get('text')}' (Distancia: {hit.distance:.4f})")

    utility.drop_collection(collection_name)
    connections.disconnect("default")
    print("[+] Test completado y recursos liberados.")

if __name__ == "__main__":
    test_milvus_connection()