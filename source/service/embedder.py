from api.config.base import settings
import requests


class Embedler:
    def __init__(self):
        self.embeding_api = settings.EMBEDDING_BASE_URL
        self.embeding_size = settings.EMBEDDING_SIZE
        self.embeding_model = settings.EMBEDING_MODEL

    def embed_documents(self, texts:list[str]):

        embedings = []

        for text in texts:
            request = requests.post(
                self.embeding_api, json={"input": text, "model": self.embeding_model}
            )

            response = request.json()
            embedings.append(response["data"][0]["embedding"])


        return embedings
    
    def embed(self, text:str):

        # embedings = []

        # for text in texts:
        request = requests.post(
            self.embeding_api, json={"input": text, "model": self.embeding_model}
        )
        response = request.json()
        
        # embedings.append(response["data"][0]["embedding"])
        return response["data"][0]["embedding"]