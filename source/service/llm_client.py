from service.retriever import Retriver
from api.config.base import settings
import requests

class LLM:
    def __init__(self):
        self.llm_api = settings.LLM_BASE_URL
        self.llm_api_key = settings.LLM_API_KEY
        self.llm_model = settings.MODEL_NAME
        self.retriver = Retriver()
        self.api_url= settings.LLM_BASE_URL

    def generate(self, prompt):
        payload = {
            "text": prompt,
            "generate_params": {
                "model_name": self.llm_model,
                "system_prompt": "You are an AI assistant that follows instruction extremely well. Help as much as you can.",
            },
        }

        headers = {"Content-Type": "application/json", "Authorization" : f"Bearer {self.llm_api_key}"}

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["result"]

    def generate_answer(self , query, top_k=3, relevance_threshold=0.9, query_metadata=None):
        retrieved_docs = self.retriver.retrieve(query=query , top_k=top_k , query_metadata=query_metadata)

        # for i in retrieved_docs:
        #     print(i["distance"])
        #     print(relevance_threshold)
        #     print(i["distance"] < relevance_threshold)

        # print(retrieved_docs)

        relevant_docs = [
            doc for doc in retrieved_docs if doc["distance"] < relevance_threshold
        ]

        if not relevant_docs:
            return {
                "query": query,
                "answer": "I cannot find relevant information in the documents to answer this question.",
                "retrieved_documents": retrieved_docs,
                "is_relevant": False,
                "reason": "No documents found below relevance threshold",
            }
        
        context = "\n\n".join(
            [
                f"Document {i+1}: {doc['document']}"
                for i, doc in enumerate(relevant_docs)
            ]
        )

        prompt = f"""Based ONLY on the following context, answer the question. If the context does not contain information to answer the question, respond with "I cannot answer this question based on the provided documents.

Context:
{context}

Question:
{query}

Answer:"""
        
        answer = self.generate(prompt)

        print(answer)

        return {
            "query": query,
            "answer": answer,
            "retrieved_documents": relevant_docs,
            "relevance_scores": [doc["distance"] for doc in relevant_docs],
            "num_relevant_docs": len(relevant_docs),
        }