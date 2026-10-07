# FieldOracle — retrieval findings, 7 October 2026

A record of what was measured on day one, before the Gradio app exists. Move
this into the FieldOracle repo when that is created; it is the raw material for
the evaluation section of the final write-up.

---

## Setup

| | |
|---|---|
| index | Pinecone `fieldoracle`, serverless aws us-east-1 |
| embedder | `text-embedding-3-small`, 1536 dimensions, cosine |
| passages | 35 — 16 from `scripts/corpus.py`, 19 added in `scripts/corpus_extra.py` |
| rewrite model | `qwen3-4b-instruct-2507`, Q4_K_S, local via LM Studio |
| retrieval | `similarity_search_with_score`, k=3 |

The 19 added passages cover pests and diseases, which the course corpus does not
touch at all. Every one was taken from a Department of Agriculture / RRDI page
and checked against it. Where a page does not state something — a scientific
name, a spray rate — it was left out rather than filled in from elsewhere.

## Method

Three farmer messages, written in the register a real message arrives in. Each
run twice: the raw message embedded directly, and a version rewritten by the
local model. Same index, same embedder, same k. **Only the embedded string
changes.**

---

## Results

### Q1 — fertiliser timing
> *"Hi, quick one — I'm the guy with the plot near the tank in Polonnaruwa, put
> Bg 300 in about three weeks back. Wife says I should put something down again?"*

| | top 3 |
|---|---|
| raw | `var-3.5month` 0.3702 · `var-3month` 0.3373 · `water-seeding-varieties` 0.3039 |
| rewritten | `water-seeding-varieties` 0.5214 · `maturity-adoption` 0.5213 · `seed-quality` 0.5177 |

**Neither is correct.** The right answer is `fert-3month`, and it appears in
neither list.

### Q2 — disease identification
> *"machan my leaves got these grey spots with brown edges and some panicles
> went white, whole field looking bad, what to spray??"*

| | top 3 |
|---|---|
| raw | **`dis-differential-whiteheads` 0.5536** · `dis-narrowbrownspot-management` 0.5258 · `dis-brownspot-symptoms` 0.5243 |
| rewritten | `dis-brownspot-management` 0.6248 · `dis-common-practice` 0.6101 · `dis-narrowbrownspot-management` 0.6080 |

**Raw is correct, rewritten is wrong.** The rewrite scores higher on every row
and retrieves nothing useful.

### Q3 — pest decision
> *"the hoppers are back at the bottom of the plants, last year whole thing
> burned, is it worth spraying now or wait"*

| | top 3 |
|---|---|
| raw | `pest-bph-control` 0.5114 · `pest-bph-threshold` 0.4878 · `pest-bph-damage` 0.4712 |
| rewritten | `pest-bph-control` 0.6189 · `pest-bph-threshold` 0.6052 · `pest-bph-damage` 0.5222 |

**Both correct, rewritten is better.** `pest-bph-threshold` carries the answer to
what was actually asked — 2 insects per hill at booting, 5 at heading.

### Scorecard

| | raw | rewritten |
|---|---|---|
| Q1 fertiliser | wrong | wrong |
| Q2 disease | **right** | wrong |
| Q3 pest | right | **right, stronger** |

Query rewriting helped once, hurt once, and could not help once.

---

## Findings

### 1. A higher similarity score is not a better answer

The clearest case is Q2: every rewritten result scores above every raw result,
and the raw set contains the right passage while the rewritten set does not.
Across Q1 the rewrite lifted the top score from 0.3702 to 0.5214 while making
the result less relevant.

Short, on-domain queries match many passages strongly. Score measures how
confidently the index matched something, not whether that something answers the
question. **Cosine score is not a quality metric and should never be reported as
one.**

### 2. Query rewriting is not a free improvement

The Lesson 1 deck calls rewriting "the cheapest improvement available in RAG".
On this corpus it was 1 win, 1 loss, 1 no-change. The loss is instructive: the
farmer wrote *"what to spray"*, the model wrote *"paddy crop treatment"*, and
"treatment" pulled the three *management* passages above the *symptom* passage
that identified the disease. A reasonable-looking paraphrase changed which
**kind** of passage won.

Rewriting is a component to be measured, not assumed.

### 3. Q1 cannot be fixed by retrieval at all

`fert-3month` describes "a three month age class variety under irrigation". It
never contains the string **Bg 300**. The fact that Bg 300 *is* a three-month
variety lives in a different passage, `var-3month`.

Answering therefore needs two lookups: establish the age class, then fetch that
age class's schedule. One search cannot do it, however the query is phrased and
however large the corpus grows. This is the Bg 352 problem from the deck,
reproduced independently on different data.

**Implication: Q1 is the justification for agentic RAG in this project.** Not an
accuracy improvement — a class of question that single-shot retrieval cannot
reach.

### 4. Embeddings average, so a decisive detail gets diluted

Q2 originally failed. The farmer's *"grey spots with brown edges"* matches the
brown spot passage almost word for word ("dark brown margin and a light
reddish-brown or grey centre"). The single phrase that settles it — *"panicles
went white"*, i.e. blast neck rot producing whiteheads — was one clause inside a
passage full of competing detail, and the embedding averages across the whole
passage.

Two fixes were tried:

- **Vocabulary.** Changed the blast passage from "ashy centres" to "ashy grey
  centres". Moved blast up, not enough to win.
- **A dedicated passage.** Added `dis-differential-whiteheads`, whose entire
  subject is distinguishing the two. It took first place at 0.5536.

The second worked because the decisive fact became the passage's whole meaning
rather than one sentence in it. **Chunking is not just about size; it is about
making sure each retrievable unit has one subject.**

### 5. Few-shot examples leak on a small model

Prompt v2 instructed the model to keep symptom words and listed examples:
*spots, white panicles, burned, dried, lodged, hoppers, galls*. The 4B model
emitted that list verbatim as its output. A fertiliser question was rewritten to
`spots white panicles burned dried lodged hoppers galls Bg 300` and retrieved
brown planthopper passages.

Prompt v3 names no examples and states the rule abstractly — *use only words and
facts from the message, never add a symptom the farmer did not mention* — and
the leak stopped completely.

**On a 4B model, an illustrative list in the prompt is output, not guidance.**
This may not reproduce on a larger model, which is itself worth testing.

### 6. `temperature=0.0` is not deterministic

The same message produced `paddy cultivation bg 300 follow up application` on
one run and `paddy cultivation bg 300 follow up planting` on the next, with
temperature pinned at 0. Any evaluation of the rewrite step has to average over
several runs or it is measuring noise.

---

## Limitations

- **Three questions.** Far too few to support a number. These are observations
  about mechanisms, not a measured hit rate. The eval set of ~20 questions in
  week 3 is what produces a figure worth reporting.
- One embedding model, one k, one rewrite model. No comparison against
  `text-embedding-3-large`, k=5, or a larger local model.
- The questions were written by the person building the system, which is the
  weakest kind of test set.

## Next

1. Build the 20-question evaluation set with known-correct passages, and measure
   hit rate at 1 and 3 — raw versus rewritten, averaged over 3 runs.
2. Compare `qwen3-4b` against `gemma-4-e4b` on the rewrite step.
3. Treat Q1 as the acceptance test for agentic RAG when notebook 12 ships.
4. Re-check Q2 at k=5 before adding a reranker; the right passage may already be
   within reach.
