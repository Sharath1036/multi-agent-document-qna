from os import getenv
from agno.vectordb.mongodb import MongoDb
from dotenv import load_dotenv
from agno.embedder.ollama import OllamaEmbedder

load_dotenv(override=True)

class MongoVectorDB:
    def __init__(self):
        self.mongo_connection_string = getenv("MONGO_CONNECTION_STRING")
        self.database_name = "agno"
        self.search_index_name = "vector-search"
        self.embedder = OllamaEmbedder(id="openhermes", host='http://localhost:11434/', timeout=1000.0)
        
    def initialize_db(self, collection_name: str = None):
        return MongoDb(
            db_url=self.mongo_connection_string,
            database=self.database_name,
            search_index_name=self.search_index_name,
            embedder=self.embedder,
            collection_name=collection_name
        )