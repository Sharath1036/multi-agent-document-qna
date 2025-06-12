import sys
import os
from os import getenv
from dotenv import load_dotenv
from agno.agent import Agent
from agno.knowledge.docx import DocxKnowledgeBase
from agno.embedder.ollama import OllamaEmbedder
from pathlib import Path
from typing import Union


# Add the root directory of the project to sys.path (since it fails to identify VectorDB as a dir)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector_db.mongo import MongoVectorDB
from vector_db.qdrant import QdrantVectorDB

class DocxKnowledgeAgent:
    def __init__(self, path: Union[str,Path], vector_database: str):
        load_dotenv(override=True)
        self.collection_name = "docx-embeddings"
        self.embedder = OllamaEmbedder(id="openhermes", host='http://localhost:11434/', timeout=1000.0)
        self.vector_db = self._init_vector_db(vector_database)
        self.knowledge_base = self._init_knowledge_base(path)
        self.agent = self._init_agent()

    def _init_vector_db(self, vector_database: str):
        if vector_database == 'Qdrant':
            return QdrantVectorDB.initialize_db(collection=self.collection_name)
        else:    
            return MongoVectorDB().initialize_db(collection_name=self.collection_name)

    def _init_knowledge_base(self, path: Union[str,Path]) -> DocxKnowledgeBase:
        return DocxKnowledgeBase(
            path= Path(path) if isinstance(path, str) else path,
            vector_db=self.vector_db,
            embedder=self.embedder
        )

    def _init_agent(self) -> Agent:
        return Agent(
            knowledge=self.knowledge_base,
            show_tool_calls=True,
            search_knowledge=True
        )

    def embed_sample(self, text: str):
        embeddings = self.embedder.get_embedding(text)
        print(f"Embeddings (first 5 values): {embeddings[:5]}")
        print(f"Embedding Dimension: {len(embeddings)}")

    def load_documents(self, recreate: bool = False):
        self.knowledge_base.load(recreate=recreate)

    def query(self, prompt: str, markdown: bool = True):
        response = self.agent.run(prompt, markdown=markdown) # comment out while testing
        return response.content # comment out while testing
        # self.agent.run(prompt, markdown=markdown) # uncomment while testing

# For testing
if __name__ == "__main__":
    path = 'docs/mechanical_softwares.docx'
    vector_database = 'MongoDb' 
    runner = DocxKnowledgeAgent(path=path, vector_database=vector_database)

    runner.embed_sample("The quick brown fox jumps over the lazy dog.")
    runner.load_documents(recreate=False)
    runner.query("What all simulation softwares are mentioned in the document?", markdown=True)