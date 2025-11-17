from service.embedder import Embedler
from db.vector_store import VectorStores


class Retriver:
    def __init__(self):
        self.embedler = Embedler()
        self.vector_strores = VectorStores()

    def retrieve(self, query: str, top_k: int = 3, query_metadata=None):
        query_embedding = self.embedler.embed(query)

        results = self.vector_strores.search_similar(
            query_embedding=[query_embedding], top_k=top_k, query=query_metadata
        )

        retrieved_docs = []
        for i in range(len(results["documents"][0])):
            retrieved_docs.append(
                {
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                }
            )

        return retrieved_docs
