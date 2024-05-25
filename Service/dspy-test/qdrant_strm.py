from collections import defaultdict
from typing import Optional, Union
from qdrant_client import QdrantClient
from qdrant_client.models import SearchRequest, NamedVector
from sentence_transformers import SentenceTransformer
import dspy
from dspy.utils import dotdict
from torch import Tensor

class QdrantSTRM(dspy.Retrieve):
    def __init__(
        self,
        qdrant_collection_name: str,
        qdrant_client: QdrantClient,
        sentence_transformer: SentenceTransformer,
        payload_key: str = "document",
        k: int = 3,
    ):
        self._qdrant_collection_name = qdrant_collection_name
        self._qdrant_client = qdrant_client
        self._sentence_transformer = sentence_transformer
        self._payload_key = payload_key
        super().__init__(k=k)
    
    def forward(self, query_or_queries: Union[str, list[str]], k: Optional[int] = None, **kwargs) -> dspy.Prediction:
        queries = (
            [query_or_queries]
            if isinstance(query_or_queries, str)
            else query_or_queries
        )
        queries = [q for q in queries if q]  # Filter empty queries

        k = k if k is not None else self.k
        embeddings = self._sentence_transformer.encode(queries, normalize_embeddings=True)

        batch_results = self._qdrant_client.search_batch(
            self._qdrant_collection_name, [
                SearchRequest(vector=embedding.tolist(), limit=k, with_payload=True, **kwargs)
                for embedding in embeddings
            ]
        )

        passages_scores = defaultdict(float)
        for batch in batch_results:
            for result in batch:
                # If a passage is returned multiple times, the score is accumulated.
                passages_scores[result.payload[self._payload_key]] += result.score

        # Sort passages by their accumulated scores in descending order
        sorted_passages = sorted(
            passages_scores.items(), key=lambda x: x[1], reverse=True
        )[:k]

        # Wrap each sorted passage in a dotdict with 'long_text'
        passages = [dotdict({"long_text": passage}) for passage, _ in sorted_passages]

        return passages