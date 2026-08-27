from pymilvus import DataType
from celery import shared_task

from dependencies.milvus import MILVUS_HOST, MILVUS_PORT, MilvusDep, milvus_context


def run_milvus_check(client: MilvusDep):
    collection_name = "test_vector_collection"

    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    schema = client.create_schema(auto_id=True, enable_dynamic_field=False)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=4)
    schema.add_field("text", DataType.VARCHAR, max_length=200)

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="vector",
        index_type="IVF_FLAT",
        metric_type="L2",
        params={"nlist": 128},
    )
    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params,
    )

    vectors = [[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8], [0.9, 1.0, 1.1, 1.2]]
    texts = ["Primer vector", "Segundo vector", "Tercer vector"]
    
    client.insert(
        collection_name,
        [{"vector": vector, "text": text} for vector, text in zip(vectors, texts)],
    )

    results = client.search(
        collection_name=collection_name,
        data=[[0.1, 0.2, 0.3, 0.4]],
        anns_field="vector",
        search_params={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=2,
        output_fields=["text"],
    )

    print("[+] Conexión y operaciones exitosas.")
    print("--- Resultados de Búsqueda ---")
    
    search_results = []
    for hit in results[0]:
        match_text = hit["entity"].get("text")
        distance = float(hit["distance"])
        print(f"  -> Match: '{match_text}' (Distancia: {distance:.4f})")
        search_results.append({"text": match_text, "distance": distance})

    client.drop_collection(collection_name)

    return {
        "host": MILVUS_HOST,
        "results": search_results,
        "status": "¡Prueba Milvus completada con éxito!"
    }


@shared_task
def test_milvus_connection():
    print(f"[*] Conectando a Milvus ({MILVUS_HOST}:{MILVUS_PORT})...")
    try:
        with milvus_context() as client:
            result = run_milvus_check(client)
        print("[+] Test completado y recursos liberados.")
        return result
    except Exception as error:
        print(f"[X] Error al conectar o interactuar con Milvus: {error}")
        return {"status": "Error: No se pudo conectar a Milvus."}