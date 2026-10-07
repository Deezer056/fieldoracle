"""Quick sanity check on .env — prints no secrets. Delete this file when done."""
import os, sys
from dotenv import load_dotenv

load_dotenv()
ok = True

def line(label, good, detail=""):
    global ok
    if not good: ok = False
    print(f"  {'PASS' if good else 'FAIL'}  {label}{(' — ' + detail) if detail else ''}")

print("\n.env format")
oa = os.getenv("OPENAI_API_KEY", "")
pc = os.getenv("PINECONE_API_KEY", "")
line("OPENAI_API_KEY present", oa.startswith("sk-") and "..." not in oa, f"{len(oa)} chars")
line("PINECONE_API_KEY present", pc.startswith("pcsk_") and "..." not in pc, f"{len(pc)} chars")
line("no spaces in keys", " " not in oa and " " not in pc)
print(f"  INFO  index name: {os.getenv('PINECONE_INDEX')}")
print(f"  INFO  ntfy topic: {os.getenv('NTFY_TOPIC')}")

print("\nOpenAI")
try:
    from openai import OpenAI
    models = OpenAI().models.list().data
    line("key works", True, f"{len(models)} models visible")
except Exception as e:
    line("key works", False, f"{type(e).__name__}: {str(e)[:120]}")

print("\nPinecone")
try:
    from pinecone import Pinecone
    names = [i["name"] for i in Pinecone(api_key=pc).list_indexes()]
    line("key works", True, f"indexes: {names if names else 'none yet (correct — notebook 10 makes it)'}")
except Exception as e:
    line("key works", False, f"{type(e).__name__}: {str(e)[:120]}")

print("\n" + ("All good — run notebook 10 next." if ok else "Something failed above."))
sys.exit(0 if ok else 1)
