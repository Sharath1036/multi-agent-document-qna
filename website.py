import asyncio
from agno.agent import Agent
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.vectordb.mongodb import MongoDb
from os import getenv
from dotenv import load_dotenv
from agno.embedder.ollama import OllamaEmbedder

load_dotenv(override=True)


vector_db = MongoDb(
    db_url=getenv("MONGO_CONNECTION_STRING"),
    database="agno",
    search_index_name="vector-search",
    collection_name="website-embeddings"
)

# Create a knowledge base with the seed URLs
knowledge_base = WebsiteKnowledgeBase(
    urls=["https://www.iplt20.com/teams/mumbai-indians"],
    # Number of links to follow from the seed URLs
    max_links=5,
    # Table name: ai.website_documents
    vector_db=vector_db,
    embedder=OllamaEmbedder(id="openhermes", host='http://localhost:11434/', timeout=1000.0)
)

# Create an agent with the knowledge base
agent = Agent(knowledge=knowledge_base, search_knowledge=True, debug_mode=True)

if __name__ == "__main__":
    # Comment out after first run
    asyncio.run(knowledge_base.aload(recreate=False))

    # Create and use the agent
    asyncio.run(agent.aprint_response("Who is the coach of Mumbai Indians", markdown=True))