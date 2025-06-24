from agno.storage.mongodb import MongoDbStorage
from dotenv import load_dotenv
from os import getenv

class MongoDBStorage:
    def __init__(self):
        self.mongo_connection_string = getenv("MONGO_CONNECTION_STRING")
        self.database_name = "agno"
        self.storage_collection = "agent_sessions"
        self.storage = self.initialize_storage
        
    def initialize_storage(self, collection_name: str = None):
        return MongoDbStorage(
            db_url=self.mongo_connection_string,
            db_name=self.database_name,
            collection_name=self.storage_collection
        )