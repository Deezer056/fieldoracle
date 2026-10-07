---
title: FieldOracle
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: gradio
app_file: app.py
pinned: false
short_description: Paddy cultivation answers from Sri Lanka DOA guidance
---

# FieldOracle

A retrieval assistant for Sri Lankan paddy farmers. It answers cultivation
questions from Department of Agriculture guidance, cites the passage it used,
and says so plainly when the guidance does not cover the question.

STEMLink AI Engineer Bootcamp, Level 4 capstone.

## The problem

Asked the same fertiliser question three times, a language model gives three
different confident schedules, none of them matching the published figures. The
answers are fluent, specific and formatted like real agronomic advice, which is
what makes them dangerous — a farmer cannot tell a guess from a fact.

Pasting the whole corpus into the prompt works at 16 passages and stops working
well before a real one. So the facts live in a vector store and the system
retrieves what it needs.

## Status

| | |
|---|---|
| corpus | 19 passages, pests and diseases, sourced from doa.gov.lk |
| index | Pinecone, 1536 dimensions, cosine |
| query rewriting | local model via LM Studio, measured — see FINDINGS.md |
| interface | not built yet |
| evaluation | 3 questions by hand; a 20-question set is the next step |

## Setup

```bash
uv sync
cp .env.example .env     # then fill in both keys
uv run python scripts/check_keys.py
uv run python scripts/load_corpus.py
```

`OPENAI_API_KEY` is issued by STEMLink. `PINECONE_API_KEY` is a free account at
app.pinecone.io. Do not create the index by hand — `load_corpus.py` creates it
with the right dimension and metric.

## Layout

```
fieldoracle/
  config.py     models, keys, index name
  corpus.py     the passages, each one id / category / source / text
  rewrite.py    turns a farmer's message into a search query, locally
scripts/
  check_keys.py    verifies .env without printing secrets
  load_corpus.py   creates the index and upserts the corpus
FINDINGS.md     what has actually been measured
```

## On the corpus

Every passage comes from a Department of Agriculture or RRDI page and was
checked against it. Where a page does not state something — a scientific name, a
spray rate, a threshold — it is left out rather than filled in from elsewhere or
from a model.

**No passage in this corpus was written by a language model.** A generated
agronomic figure, retrieved and then cited, is worse than no system at all: it
looks checked. That failure is the thing this project exists to prevent.

## Credits

Course material and the teaching corpus are STEMLink's. The pest and disease
passages, the rewrite step, the evaluation and the findings are mine.
