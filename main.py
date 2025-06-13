from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Union
from pathlib import Path
import uvicorn
from os import getenv
from dotenv import load_dotenv

from knowledge_base.wikipedia import WikipediaKnowledgeAgent
from knowledge_base.pdf_url import PDFUrlKnowledgeAgent
from knowledge_base.website import WebsiteKnowledgeAgent

# Initialize FastAPI app
app = FastAPI(title="API for Multi Agentic RAG based Q&A")

# Load environment variables
load_dotenv(override=True)

# Initialize agents
wikipedia_agent = None
pdf_agent = None  # Will be initialized when URLs are provided
website_agent = None

# Initialize vector database
vector_database = 'Qdrant' # MongoDb

class UrlsRequest(BaseModel):
    urls: List[str]

class TopicsRequest(BaseModel):
    topics: List[str]

class DocxRequest(BaseModel):
    path: Union[str, Path]

class QueryRequest(BaseModel):
    query: str
    markdown: bool = True

@app.post("/initialize-pdf")
async def initialize_pdf(request: UrlsRequest):
    """Initialize the PDF knowledge agent with provided URLs"""
    global pdf_agent
    try:
        pdf_agent = PDFUrlKnowledgeAgent(urls=request.urls, vector_database=vector_database)
        pdf_agent.load_documents(recreate=False)
        return {"message": "PDF knowledge base initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/query-pdf")
async def query_pdf(request: QueryRequest):
    """Query the PDF knowledge base"""
    if pdf_agent is None:
        raise HTTPException(status_code=400, detail="PDF knowledge base not initialized. Please initialize it first.")
    try:
        response = pdf_agent.query(request.query, markdown=request.markdown)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

@app.post("/initialize-wikipedia")
async def initialize_wikipedia(request: TopicsRequest):
    """Initialize the Wikipedia knowledge agent"""
    global wikipedia_agent
    try:
        wikipedia_agent = WikipediaKnowledgeAgent(vector_database=vector_database)
        wikipedia_agent.set_topics(topics=request.topics)
        wikipedia_agent.load_documents(recreate=False)
        return {"message": "Wikipedia knowledge base initialized successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query-wikipedia")
async def query_wikipedia(request: QueryRequest):
    """Query the Wikipedia knowledge base"""
    try:
        response = wikipedia_agent.query(request.query, markdown=request.markdown)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/initialize-website")
async def initialize_website(request: UrlsRequest):
    """Initialize the Website knowledge agent with provided URLs"""
    global website_agent
    try:
        print(f"Initializing website agent with URLs: {request.urls}")  # Debug log
        website_agent = WebsiteKnowledgeAgent(urls=request.urls, vector_database=vector_database)
        print("Website agent created successfully")  # Debug log
        website_agent.load_documents(recreate=False)
        print("Documents loaded successfully")  # Debug log
        return {"message": "Website knowledge base initialized successfully"}
    except Exception as e:
        print(f"Error initializing website agent: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/query-website")
async def query_website(request: QueryRequest):
    """Query the Website knowledge base"""
    if website_agent is None:
        raise HTTPException(status_code=400, detail="Website knowledge base not initialized. Please initialize it first.")
    try:
        response = website_agent.query(request.query, markdown=request.markdown)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))      


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


