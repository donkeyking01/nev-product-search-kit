"""
API configuration and client initialization.
"""

import os
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from neo4j import GraphDatabase
from openai import OpenAI
from sentence_transformers import SentenceTransformer


ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_FILE)


class DeepSeekClient:
    """DeepSeek API client using the OpenAI-compatible interface."""

    def __init__(self):
        self.api_base = (
            os.getenv("DEEPSEEK_API_BASE")
            or os.getenv("SILICONFLOW_API_BASE")
            or "https://api.deepseek.com"
        )
        self.api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("SILICONFLOW_API_KEY")

        if not self.api_key:
            raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base,
        )

        self.model_reasoning = os.getenv("MODEL_REASONING", "deepseek-v4-pro")
        self.model_routing = os.getenv("MODEL_ROUTING", "deepseek-v4-flash")
        self.model_reranker = os.getenv("MODEL_RERANKER", "BAAI/bge-reranker-v2-m3")

    def chat(self, messages: list, model: Optional[str] = None, **kwargs):
        model = model or self.model_reasoning
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs,
        )
        return response


class VectorDBClient:
    """ChromaDB client."""

    def __init__(self):
        self.db_path = os.getenv("VECTOR_DB_PATH", "offline-pipeline/data/Vector")

        self.client = chromadb.PersistentClient(
            path=self.db_path,
            settings=Settings(anonymized_telemetry=False),
        )

        embedding_model_name = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-MiniLM-L12-v2")
        self.embedding_model = SentenceTransformer(embedding_model_name)

        self.ugc_collection = self.client.get_collection("ugc_reviews")
        self.specs_collection = self.client.get_collection("vehicle_specs")
        self.persona_collection = self.client.get_collection("user_personas")

    def query(self, collection_name: str, query_texts: list, n_results: int = 5, **kwargs):
        collection = self.client.get_collection(collection_name)
        results = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            **kwargs,
        )
        return results


class GraphDBClient:
    """Neo4j client."""

    def __init__(self):
        self.uri = os.getenv("NEO4J_URI")
        self.username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD")

        if not self.uri or not self.password:
            raise ValueError("NEO4J_URI or NEO4J_PASSWORD not found in environment variables")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password),
        )

    def query(self, cypher: str, parameters: Optional[dict] = None):
        with self.driver.session() as session:
            result = session.run(cypher, parameters or {})
            return [record.data() for record in result]

    def close(self):
        self.driver.close()


_deepseek_client: Optional[DeepSeekClient] = None
_vector_client: Optional[VectorDBClient] = None
_graph_client: Optional[GraphDBClient] = None


def get_deepseek_client() -> DeepSeekClient:
    global _deepseek_client
    if _deepseek_client is None:
        _deepseek_client = DeepSeekClient()
    return _deepseek_client


def get_siliconflow_client() -> DeepSeekClient:
    """Backward-compatible alias for older imports."""
    return get_deepseek_client()


def get_vector_client() -> VectorDBClient:
    global _vector_client
    if _vector_client is None:
        _vector_client = VectorDBClient()
    return _vector_client


def get_graph_client() -> GraphDBClient:
    global _graph_client
    if _graph_client is None:
        _graph_client = GraphDBClient()
    return _graph_client
