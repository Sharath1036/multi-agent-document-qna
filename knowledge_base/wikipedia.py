import os
import sys
from os import getenv
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.wikipedia import WikipediaKnowledgeBase
from agno.embedder.ollama import OllamaEmbedder
from agno.tools.duckduckgo import DuckDuckGoTools

# Add the root directory of the project to sys.path (since it fails to identify VectorDB as a dir)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from VectorDB.MongoDB import MongoVectorDB
from VectorDB.Qdrant import QdrantVectorDB

class WikipediaKnowledgeAgent:
    def __init__(self, vector_database: str):
        load_dotenv(override=True)
        self.collection_name = "wikipedia-embeddings"
        self.embedder = OllamaEmbedder(id="openhermes", host='http://localhost:11434/', timeout=1000.0)
        self.vector_db = self._init_vector_db(vector_database)
        self.knowledge_base = None
        self.agent = None

    def _init_vector_db(self, vector_database: str):
        if vector_database == 'Qdrant':
            return QdrantVectorDB.initialize_db(collection=self.collection_name)
        else:    
            mongo_db = MongoVectorDB()
            return mongo_db.initialize_db(collection_name=self.collection_name)

    def set_topics(self, topics: list[str]):
        """Set the topics for the Wikipedia knowledge base"""
        self.knowledge_base = WikipediaKnowledgeBase(
            topics=topics,
            vector_db=self.vector_db,
            embedder=self.embedder
        )
        self.agent = self._init_agent()

    def _init_agent(self) -> Agent:
        return Agent(
            knowledge=self.knowledge_base,
            search_knowledge=True,
            tools=[DuckDuckGoTools()]
        )

    def embed_sample(self, text: str):
        embeddings = self.embedder.get_embedding(text)
        print(f"Embeddings (first 5 values): {embeddings[:5]}")
        print(f"Embedding Dimension: {len(embeddings)}")

    def load_documents(self, recreate: bool = False):
        if self.knowledge_base is None:
            raise ValueError("Topics must be set before loading documents")
        self.knowledge_base.load(recreate=recreate)

    def query(self, prompt: str, markdown: bool = True):
        if self.agent is None:
            raise ValueError("Topics must be set before querying")
        response = self.agent.run(prompt, markdown=markdown)
        print(f"Raw response from agent.run(): {response}")
        print(f"Content from response: {response.content}")
        return response.content


if __name__ == "__main__":
    vector_database = 'MongoDb' 
    runner = WikipediaKnowledgeAgent(vector_database=vector_database)

    # Example usage
    topics = ["Indian Cricket Team", "Australian Cricket Team"]
    runner.set_topics(topics)
    runner.embed_sample("The quick brown fox jumps over the lazy dog.")
    runner.load_documents(recreate=False)
    runner.query("How many ICC trophies has India won till date?", markdown=True)