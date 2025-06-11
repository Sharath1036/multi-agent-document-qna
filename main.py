from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from os import getenv
from dotenv import load_dotenv

from knowledge_base.wikipedia import WikipediaKnowledgeAgent
from knowledge_base.pdf_url import PDFUrlKnowledgeAgent

# Initialize FastAPI app
app = FastAPI(title="Document Knowledge Base API")

# Load environment variables
load_dotenv(override=True)

# Initialize agents
wikipedia_agent = WikipediaKnowledgeAgent(vector_database='MongoDb')
pdf_agent = None  # Will be initialized when URLs are provided

class PDFUrlsRequest(BaseModel):
    urls: List[str]

class TopicsRequest(BaseModel):
    topics: List[str]

class QueryRequest(BaseModel):
    query: str
    markdown: bool = True

@app.post("/initialize-pdf")
async def initialize_pdf(request: PDFUrlsRequest):
    """Initialize the PDF knowledge agent with provided URLs"""
    global pdf_agent
    try:
        pdf_agent = PDFUrlKnowledgeAgent(urls=request.urls, vector_database='MongoDb')
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
    try:
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)