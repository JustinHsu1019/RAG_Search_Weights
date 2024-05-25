import json
import re
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

with open("knowledge.json", encoding="utf-8") as file:
    knowledge_list = json.load(file)

client = QdrantClient(path="bce_base_no_chunking")
encoder = SentenceTransformer("maidalun1020/bce-embedding-base_v1", token="")

client.recreate_collection(
    collection_name="test_0424",
    vectors_config=models.VectorParams(
        size=encoder.get_sentence_embedding_dimension(),  # Vector size is defined by used model
        distance=models.Distance.DOT,
    ),
)

for idx, doc in enumerate(knowledge_list):
    print(doc["name"])
    content = doc["name"] + "\n\n" + doc["content"]
    encode_content = re.sub("\\[IMG\\].*? \\[/IMG\\]", "\\[IMG/\\]", content)
    client.upload_points(
        collection_name="test_0424",
        points=[
            models.PointStruct(
                id=idx, vector=encoder.encode(encode_content, normalize_embeddings=True).tolist(), payload={"document": content}
            ),
        ],
    )
