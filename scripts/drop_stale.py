"""Delete index vectors that the repo no longer defines.

    uv run python scripts/drop_stale.py          # dry run, lists them
    uv run python scripts/drop_stale.py --yes    # actually delete

Written for fert-3month and fert-3.5month, which state a basal urea dose that
does not exist in the DOA recommendation (finding 9). Deleting is permanent,
so the default is a dry run.
"""
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

stale = sorted(live - {d["id"] for d in DOCS})
print(f"index: {len(live)}   repo: {len(DOCS)}   stale: {len(stale)}")

if not stale:
    print("nothing to do")
elif "--yes" in sys.argv:
    index.delete(ids=stale)
    print("deleted:", stale)
else:
    print("would delete:", stale)
    print("\nre-run with --yes to delete")
