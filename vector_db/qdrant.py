from os import getenv
from agno.vectordb.qdrant import Qdrant
from dotenv import load_dotenv
from agno.embedder.ollama import OllamaEmbedder

class QdrantVectorDB:
    def __init__(self):
        load_dotenv(override=True)
        
        self.qdrant_url = getenv("QDRANT_URL")
        self.qdrant_api_key = getenv("QDRANT_API_KEY")
        self.embedder = OllamaEmbedder(id="openhermes", host='http://localhost:11434/', timeout=1000.0)

        
    def initialize_db(self, collection: str=None):
        return Qdrant(
            collection=collection,
            url=self.qdrant_url,
            embedder=self.embedder,
            api_key=self.qdrant_api_key
        )