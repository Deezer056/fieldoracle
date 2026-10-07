"""Query rewriting for FieldOracle, running on a local model via LM Studio.

Turns a messy farmer message into a search string, then shows what that
changes about retrieval against your real index. Costs nothing to run.

Start LM Studio, load a model, and turn the server on in the Developer tab
(it is a toggle — loading the model alone is not enough). Then:

    uv run python rewrite.py
"""
import sys, textwrap

from openai import OpenAI
from langchain_pinecone import PineconeVectorStore
from fieldoracle.config import INDEX_NAME, LOCAL_BASE_URL, embeddings

LM = OpenAI(base_url=LOCAL_BASE_URL, api_key="not-needed")

SYSTEM = (
    "Rewrite the farmer's message as a short search query for a Sri Lankan "
    "paddy cultivation database.\n"
    "Use ONLY words and facts that appear in the message itself. Never add a "
    "symptom, variety, pest or problem the farmer did not mention.\n"
    "Remove greetings, names, places and small talk. Keep everything that "
    "describes what the farmer can see or wants to know.\n"
    "Reply with the query only: 4 to 10 words, no punctuation, no explanation."
)

MESSAGES = [
    "Hi, quick one — I'm the guy with the plot near the tank in Polonnaruwa, "
    "put Bg 300 in about three weeks back. Wife says I should put something down again?",

    "machan my leaves got these grey spots with brown edges and some panicles "
    "went white, whole field looking bad, what to spray??",

    "the hoppers are back at the bottom of the plants, last year whole thing "
    "burned, is it worth spraying now or wait",
]


def rewrite(message: str) -> str:
    model_id = LM.models.list().data[0].id
    r = LM.chat.completions.create(
        model=model_id,
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": message}],
        temperature=0.0,
        max_tokens=40,
    )
    return r.choices[0].message.content.strip().strip('"').replace("\n", " ")


def show(label, query, store):
    print(f"  {label}: {query!r}")
    for doc, score in store.similarity_search_with_score(query, k=3):
        print(f"      {score:.4f}  {doc.id:<28} [{doc.metadata['category']}]")


if __name__ == "__main__":
    try:
        model_id = LM.models.list().data[0].id
    except Exception as e:
        sys.exit(f"Can't reach LM Studio at localhost:1234 — is the server toggle on "
                 f"in the Developer tab?\n  {type(e).__name__}: {e}")
    print(f"local model: {model_id}\n")

    store = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings())

    for msg in MESSAGES:
        print("=" * 78)
        print(textwrap.fill(msg, 78, initial_indent="  ", subsequent_indent="  "))
        print()
        show("raw message ", msg, store)
        print()
        show("rewritten   ", rewrite(msg), store)
        print()
