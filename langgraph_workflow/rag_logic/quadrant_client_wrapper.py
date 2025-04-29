# quadrant_client_wrapper.py

from typing import List, Optional
from qdrant_client import QdrantClient
from langgraph_workflow.models import SearchResult  # Import your structured model
import logging

logger = logging.getLogger(__name__)


class QuadrantWrapper:
    def __init__(self, host: str = "localhost", port: int = 6333, collection_name: str = ""):
        self.collection_name = collection_name
        self.quadrant_client = QdrantClient(host=host, port=port)
        print('➡ self.quadrant_client:', self.quadrant_client)

    def query_quadrant(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        collection_name: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Search similar documents using vector similarity (Quadrant Vector DB).
        """
        collection = collection_name or self.collection_name

        try:
            scored_points = self.quadrant_client.search(
                collection_name=collection,
                query_vector=query_embedding,
                with_payload=True,
                limit=top_k
            )
            logger.debug(f"Results from Quadrant: {scored_points}")

            search_results = []
            for point in scored_points:
                metadata = point.payload.get("metadata", {})
                result = SearchResult(
                    document_id=metadata.get("document_id", ""),
                    chunk_id=str(metadata.get("chunk_index", "")),
                    content=point.payload.get("page_content", ""),
                    similarity=float(point.score) if point.score is not None else 0.0,
                    metadata=metadata
                )
                search_results.append(result)

            return search_results

        except Exception as e:
            logger.error(f"Error querying Quadrant: {str(e)}")
            return []
