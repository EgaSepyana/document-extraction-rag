from service.retriever import Retriver
from api.config.base import settings
from service.memory_saver import Memory
import requests


class LLM:
    def __init__(self):
        self.llm_api = settings.LLM_BASE_URL
        self.llm_api_key = settings.LLM_API_KEY
        self.llm_model = settings.MODEL_NAME
        self.retriver = Retriver()
        self.memory_saver = Memory()
        self.api_url = settings.LLM_BASE_URL

    def generate(self, prompt):
        payload = {
            "text": prompt,
            "generate_params": {
                "model_name": self.llm_model,
                "system_prompt": "You are an AI assistant that follows instruction extremely well. Help as much as you can.",
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.llm_api_key}",
        }

        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["result"]

    def generate_answer(
        self, query, top_k=3, relevance_threshold=0.9, chatId=None, query_metadata=None
    ):
        retrieved_docs = self.retriver.retrieve(
            query=query, top_k=top_k, query_metadata=query_metadata
        )

        memory_messages = None

        if chatId:
            memory_messages = self.memory_saver.load_memory(chatId)

        # for i in retrieved_docs:
        #     print(i["distance"])
        #     print(relevance_threshold)
        #     print(i["distance"] < relevance_threshold)

        # print(retrieved_docs)

        relevant_docs = [
            doc for doc in retrieved_docs if doc["distance"] < relevance_threshold
        ]

        if not relevant_docs:

            answer = "I cannot find relevant information in the documents to answer this question."

            # Save memory
            if chatId:
                self.memory_saver.save_message(chatId, "user", query)
                self.memory_saver.save_message(chatId, "assistant", answer)

            return {
                "query": query,
                "answer": "I cannot find relevant information in the documents to answer this question.",
                "retrieved_documents": retrieved_docs,
                "is_relevant": False,
                "reason": "No documents found below relevance threshold",
            }

        memory_text = ""

        if memory_messages:
            memory_text = "\n".join(
                [f"{m['role'].upper()}: {m['content']}" for m in memory_messages]
            )

        context = "\n\n".join(
            [
                f"Document {i+1}: {doc['document']}"
                for i, doc in enumerate(relevant_docs)
            ]
        )

        prompt = f"""Based ONLY Memory and context, answer the question. If the context does not contain information to answer the question, respond with "I cannot answer this question based on the provided documents.

conversation history Memory:
{memory_text}

Context:
{context}

Question:
{query}

Answer:"""

        answer = self.generate(prompt)

        if chatId:
            self.memory_saver.save_message(chatId, "user", query)
            self.memory_saver.save_message(chatId, "assistant", answer)

        print(answer)

        return {
            "query": query,
            "answer": answer,
            "retrieved_documents": relevant_docs,
            "relevance_scores": [doc["distance"] for doc in relevant_docs],
            "num_relevant_docs": len(relevant_docs),
        }
