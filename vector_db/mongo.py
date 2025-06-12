from os import getenv
from agno.vectordb.mongodb import MongoDb
from dotenv import load_dotenv

load_dotenv(override=True)

class MongoVectorDB:
    def __init__(self):
        self.mongo_connection_string = getenv("MONGO_CONNECTION_STRING")
        self.database_name = "agno"
        self.search_index_name = "vector-search"
        
    def initialize_db(self, collection_name: str = None):
        return MongoDb(
            db_url=self.mongo_connection_string,
            database=self.database_name,
            search_index_name=self.search_index_name,
            collection_name=collection_name
        )