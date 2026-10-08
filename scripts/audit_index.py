"""What is actually in the index, versus what the repo defines."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pinecone import Pinecone
from fieldoracle.config import INDEX_NAME, require
from fieldoracle.corpus import DOCS

index = Pinecone(api_key=require("PINECONE_API_KEY")).Index(INDEX_NAME)

live = set()
for page in index.list():
    live.update(page)
repo = {d["id"] for d in DOCS}

print(f"in index: {len(live)}   in repo: {len(repo)}")
strangers = sorted(live - repo)
missing = sorted(repo - live)
if missing:
    print(f"\n{len(missing)} in your repo but NOT loaded: {missing}")

print(f"\n{len(strangers)} in the index but NOT in your repo:")
if not strangers:
    print("    none - index and repo agree")
else:
    for vid, v in index.fetch(ids=strangers).vectors.items():
        print(f"\n[{vid}] {v.metadata.get('text', '(no text)')[:300]}")