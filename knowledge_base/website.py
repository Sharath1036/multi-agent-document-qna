import sys
import os
import requests
from os import getenv
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase

# Add the root directory of the project to sys.path (since it fails to identify VectorDB as a dir)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector_db.mongo import MongoVectorDB
from vector_db.qdrant import QdrantVectorDB

class WebsiteKnowledgeAgent:
    def __init__(self, urls: list[str], vector_database: str):
        load_dotenv(override=True)
        self.collection_name = "website-embeddings"
        self.vector_db = self._init_vector_db(vector_database)
        self.knowledge_base = self._init_knowledge_base(urls)
        self.agent = self._init_agent() 

    def _init_vector_db(self, vector_database: str):
        if vector_database == 'Qdrant':
            qdrant_db = QdrantVectorDB()
            return qdrant_db.initialize_db(collection=self.collection_name)
        elif vector_database == 'MongoDb':    
            mongo_db = MongoVectorDB()
            return mongo_db.initialize_db(collection_name=self.collection_name)
        else:
            raise ValueError(f"Invalid vector database: {vector_database}")

    def _init_knowledge_base(self, urls: list[str]) -> WebsiteKnowledgeBase:
        return WebsiteKnowledgeBase(
            urls=urls,
            vector_db=self.vector_db,
        )

    def _init_agent(self) -> Agent:
        return Agent(
            knowledge=self.knowledge_base,
            show_tool_calls=True,
            search_knowledge=True
        )

    def load_documents(self, recreate: bool = False):
        self.knowledge_base.load(recreate=recreate)

    def query(self, prompt: str, markdown: bool = True):
        response = self.agent.run(prompt, markdown=markdown)
        return response.content


# For testing
if __name__ == "__main__":
    urls = [
        "https://www.iplt20.com/teams/mumbai-indians"
    ]

    vector_database = 'MongoDb' 
    runner = WebsiteKnowledgeAgent(urls=urls, vector_database=vector_database)
    runner.load_documents(recreate=False)
    runner.query("Who is the head coach?", markdown=True)