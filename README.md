# Multi Agent Document Q&A

The code performs question and answering by performing vector search on documents inside MongoDB vector database embedded from knowledge bases such as Word Document, PDF URL or Wikipedia.

## Pull the code
```
git clone https://github.com/Sharath1036/multi-agent-document-qna.git
```

## Running the code through Python
### MongoDB Setup
Obtain `MONGO_CONNECTION_STRING` from MongoDB Atlas and create a Search Index as Vector Index Search. Set index name as `vector-search`.<br><br>
Set configuration method as JSON and paste the following JSON
```
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 1536,
      "similarity": "cosine"
    }
  ]
}
```
Our vector search index has been created.<br><br>
Open cmd and run the below commands
```
mongosh <connection-string>
```
```
use agno
```
```
db.createCollection('pdf-url-embeddings')
```
```
db.createCollection('wikipedia-embeddings')
```

### Ollama Setup
We'll be using `openhermes` model for creating embeddings. When you download Ollama in your system, it is be default hosted on `localhost:11434`
```
ollama pull openhermes
```

### Set environmental variables
Create a file `.env` and add the following secrets
```
OPENAI_API_KEY = '...'
MONGO_CONNECTION_STRING = 'mongodb+srv://<username>:<password>@cluster0.c7jzf5l.mongodb.net.......?'
QDRANT_API_KEY = '...'
QDRANT_URL = '...'
```

### Inside the code file
Activate virtual environment
```
python -m venv myenv
```
```
myenv\Scripts\activate
```
Install dependencies
```
pip install -r requirements.txt
```
Run the app through FastAPI (Uvicorn)
```
uvicorn main:app --reload
```

## Running the code through Docker (without docker-compose)
Build docker image
```
docker build -t document-agent .
```
Start MongoDB
```
docker run -d --name mongodb -p 27017:27017 mongo:latest
```
Start Ollama
```
docker run -d --name ollama -p 11434:11434 ollama/ollama:latest
```
Run the application
```
docker run -d --name document-agent -p 8000:8000 \
  -e MONGO_CONNECTION_STRING=mongodb://host.docker.internal:27017 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  document-agent
```
Pull the Ollama model
```
docker exec ollama ollama pull openhermes
```

Now the FastAPI application will be available at:
* http://localhost:8000
* API documentation at http://localhost:8000/docs

## Running the code with docker-compose (easier)
```
docker-compose up --build
```
Now the FastAPI application will be available at:
* http://localhost:8000
* API documentation at http://localhost:8000/docs

## Example parameters to try
Schema for `/initialize-pdf`
```
{
  "urls": [
    "https://www.scollingsworthenglish.com/uploads/3/8/4/2/38422447/garth_stein_-_the_art_of_racing_in_the_rain.pdf"
  ]
}
```

Schema for `/query-pdf`
```
{
  "query": "How did Denny get the custody of his daughter?",
  "markdown": true
}
```

Schema for `/initialize-wikipedia`
'''
{
  "topics": [
    "Attack on Titan", "Jujutsu Kaisen"
  ]
}
'''

Schema for `/query-wikipedia`
```
{
  "query": "Why did Levi choose Armin?",
  "markdown": true
}
```

Schema for `/initialize-docx`
'''
{
  "path": "docs/mechanical_softwares.docx"
}
'''

Schema for `/query-docx`
```
{
  "query": "What all simulation softwares are listed in the document?",
  "markdown": true
}
```
