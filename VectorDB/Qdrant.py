from os import getenv
from agno.vectordb.qdrant import Qdrant
from dotenv import load_dotenv
load_dotenv(override=True)

class QdrantVectorDB:
    def __init__(self):
        self.qdrant_url = getenv("QDRANT_URL")
        self.qdrant_api_key = getenv("QDRANT_API_KEY")
        
    def initialize_db(self, collection: str):
        return Qdrant(
            collection=collection,
            url=self.qdrant_url,
            api_key=self.qdrant_api_key
        )