"""Create the Pinecone index if needed and upsert the corpus.

    uv run python scripts/load_corpus.py

Ids are stable, so re-running updates in place rather than duplicating.
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from fieldoracle.config import EMBED_DIM, INDEX_NAME, embeddings, require
from fieldoracle.corpus import DOCS

pc = Pinecone(api_key=require("PINECONE_API_KEY"))

if not pc.has_index(INDEX_NAME):
    print(f"creating index {INDEX_NAME!r} ...")
    pc.create_index(name=INDEX_NAME, dimension=EMBED_DIM, metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"))
    for _ in range(60):                      # wait for ready, unlike notebook 10
        if pc.describe_index(INDEX_NAME).status.get("ready"):
            break
        time.sleep(1)
    print("index ready")
else:
    print(f"index {INDEX_NAME!r} already exists")

index = pc.Index(INDEX_NAME)
before = index.describe_index_stats().get("total_vector_count", 0)

docs = [Document(page_content=d["text"],
                 metadata={"source": d["source"], "category": d["category"]},
                 id=d["id"]) for d in DOCS]

PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings()).add_documents(docs)
print(f"upserted {len(docs)} passages (index held {before} before)")
