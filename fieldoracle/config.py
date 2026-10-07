"""Models, keys and the index name. Everything configurable lives here."""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536                      # must match the Pinecone index
CHAT_MODEL = "gpt-5.6-luna"

LOCAL_BASE_URL = "http://localhost:1234/v1"   # LM Studio, for the rewrite step

INDEX_NAME = os.getenv("PINECONE_INDEX", "fieldoracle")
NTFY_TOPIC = os.getenv("NTFY_TOPIC", "")


def require(name: str) -> str:
    """Fetch an env var or fail with a message that says what to do."""
    value = os.getenv(name)
    if not value or value.endswith("..."):
        raise SystemExit(f"{name} is missing from .env — copy .env.example and fill it in")
    return value


def embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=EMBED_MODEL)
