# Chainlit runtime for the reorganized offline pipeline.
# Build from the repository root, for example:
# docker build -f offline-pipeline/rag/Dockerfile -t nev-research-rag .

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY offline-pipeline/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Cache the default embedding dependencies during image build.
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
import chromadb; \
print('Downloading SentenceTransformer model...'); \
SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2'); \
print('Initializing ChromaDB cache...'); \
chromadb.Client(); \
print('Models cached in image.'); \
"

COPY offline-pipeline ./offline-pipeline
COPY offline-pipeline/.env.example ./offline-pipeline/.env

WORKDIR /app/offline-pipeline/rag

EXPOSE 7860

CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]
