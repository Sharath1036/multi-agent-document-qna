from os import getenv
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv(override=True)

class ChromaVectorDB:
    def __init__(self):
        self.chroma_connection_string = getenv("CHROMA_CONNECTION_STRING")
        
    def initialize_db(self, collection: str):
        return ChromaDb(
            collection=collection,
            path="tmp/chromadb",
            persistent_client=True
        )