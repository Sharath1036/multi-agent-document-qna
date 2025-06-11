# Markdown syntax guide

## Headers

# This is a Heading h1
## This is a Heading h2
###### This is a Heading h6

## Emphasis

*This text will be italic*  
_This will also be italic_

**This text will be bold**  
__This will also be bold__

_You **can** combine them_

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b
    * Item 3a
    * Item 3b

### Ordered

1. Item 1
2. Item 2
3. Item 3
    1. Item 3a
    2. Item 3b

## Images

![This is an alt text.](/image/sample.webp "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
>> Markdown is often used to format readme files, for writing messages in online discussion forums, and to create rich text using a plain text editor.

## Tables

| Left columns  | Right columns |
| ------------- |:-------------:|
| left foo      | right foo     |
| left bar      | right bar     |
| left baz      | right baz     |

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.

# Multi Agent Document Q&A

## MongoDB Setup
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

## Ollama Setup
We'll be using `openhermes` model for creating embeddings. When you download Ollama in your system, it is be default hosted on `localhost:11434`
```
ollama pull openhermes
```

## Pull the code

```
git clone https://github.com/Sharath1036/multi-agent-document-qna.git
```

## Set environmental variables
Create a file `.env` and add the following secrets
```
MONGO_CONNECTION_STRING = 'mongodb+srv://<username>:<password>@cluster0.c7jzf5l.mongodb.net.......?'
QDRANT_API_KEY = '...'
QDRANT_URL = '...'
```

## Running the code through Python
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