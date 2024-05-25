import json
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

client = QdrantClient(path="bce_base_no_chunking")
encoder = SentenceTransformer("maidalun1020/bce-embedding-base_v1", token="")

logfile = open("output_log.txt", mode="w", encoding="utf-8")

while True:
    query = input("Query: ")
    print()

    hits = client.search(
        collection_name="test_0424",
        query_vector=encoder.encode(query, normalize_embeddings=True).tolist(),
        limit=10,
    )

    output = json.dumps([hit.payload for hit in hits], ensure_ascii=False)

    print(output)
    print()
    
    print(query, file=logfile)
    print(output, file=logfile, flush=True)
    print(file=logfile, flush=True)
