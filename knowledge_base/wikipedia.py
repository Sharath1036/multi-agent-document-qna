import os
import sys
from os import getenv
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.wikipedia import WikipediaKnowledgeBase

# Add the root directory of the project to sys.path (since it fails to identify VectorDB as a dir)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector_db.mongo import MongoVectorDB
from vector_db.qdrant import QdrantVectorDB


class WikipediaKnowledgeAgent:
    def __init__(self, vector_database: str):
        load_dotenv(override=True)
        self.collection_name = "wikipedia-embeddings"
        self.vector_db = self._init_vector_db(vector_database)
        self.knowledge_base = None
        self.agent = None

    def _init_vector_db(self, vector_database: str):
        if vector_database == 'Qdrant':
            qdrant_db = QdrantVectorDB()
            return qdrant_db.initialize_db(collection=self.collection_name)
        elif vector_database == 'MongoDb':    
            mongo_db = MongoVectorDB()
            return mongo_db.initialize_db(collection_name=self.collection_name)
        else:
            raise ValueError(f"Invalid vector database: {vector_database}")

    def set_topics(self, topics: list[str]):
        """Set the topics for the Wikipedia knowledge base"""
        self.knowledge_base = WikipediaKnowledgeBase(
            topics=topics,
            vector_db=self.vector_db,
        )
        self.agent = self._init_agent()

    def _init_agent(self) -> Agent:
        return Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            knowledge=self.knowledge_base,
            show_tool_calls=True,
            search_knowledge=True,
        )

    def load_documents(self, recreate: bool = False):
        if self.knowledge_base is None:
            raise ValueError("Topics must be set before loading documents")
        self.knowledge_base.load(recreate=recreate)

    def query(self, prompt: str, markdown: bool = True):
        response = self.agent.run(prompt, markdown=markdown) # comment out while testing
        return response.content # comment out while testing
        # self.agent.run(prompt, markdown=markdown) # uncomment while testing


# For testing
if __name__ == "__main__":
    vector_database = 'MongoDb' 
    runner = WikipediaKnowledgeAgent(vector_database=vector_database)

    # Example usage
    topics = ["Indian Cricket Team", "Australian Cricket Team"]
    runner.set_topics(topics)

    runner.load_documents(recreate=False)
    runner.query("How many ICC trophies has India won till date?", markdown=True)