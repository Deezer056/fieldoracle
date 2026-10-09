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

## Measured results

9 October. 23 questions (`fieldoracle/evalset.py`) against the 59-passage
corpus, `text-embedding-3-small`, k=3. 21 answerable plus 2 that should be
refused. The rewrite path ran three times; all three were byte-identical.

| | hit@1 | hit@3 |
|---|---|---|
| **raw question** | 11/21 &nbsp;**52%** | 20/21 &nbsp;**95%** |
| **rewritten** (mean of 3) | 9/21 &nbsp;43% | 12/21 &nbsp;57% |

By question kind, raw:

| kind | n | hit@1 | hit@3 |
|---|---|---|---|
| direct | 9 | 7 | 9 |
| paraphrase | 9 | 4 | 9 |
| two-hop | 1 | 0 | 1 |
| ambiguous | 1 | 0 | 1 |
| gap | 1 | 0 | 0 |

Refusal separation - mean top score of answerable questions against the two
that should be refused:

| | answerable | should refuse | gap |
|---|---|---|---|
| raw | 0.5868 | 0.4744 | +0.1124 |
| rewritten | 0.5694 | 0.5328 | +0.0365 |

The single raw miss was `ev-14`, the question the eval set predicted would fail.


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

### 7. A merged table cell silently shifts a whole fertilizer schedule

The four DOA zone fertilizer tables render with the `Time` column merged on the
basal row. Scraped, that shifts every basal row one cell to the left, so the
basal TSP dose arrives in the urea column. The result looks entirely plausible:
a basal urea dressing followed by four top dressings.

It is wrong, and arithmetic is what catches it. The page states its own column
totals, and under the shifted reading nothing adds up - urea came to 280 against
a stated 225. Reassigning the basal figure to TSP makes all four totals
reconcile exactly, in all four tables:

| Zone / regime | Urea | TSP | MOP | ZnSO4 |
|---|---|---|---|---|
| Intermediate & dry, irrigated | 225 | 55 | 60 | 5 |
| Intermediate & dry, rainfed | 175 | 35 | 50 | 5 |
| Wet, irrigated | 140 | 35 | 50 | 5 |
| Wet, rainfed | 100 | 55 | 110 | 5 |

The RRDI phosphorous page then independently confirms 55 kg/ha TSP irrigated and
35 kg/ha rainfed, matching the reassigned basal figures.

Two things follow for the project. The small one: a scraped table needs its own
totals checked before it is trusted, and a table that publishes totals is
checkable. The larger one: had this gone into the corpus unchecked, FieldOracle
would have told a farmer to broadcast 55 kg of urea at establishment and skip
phosphorus entirely. No retrieval metric would have caught it. Hit rate at k
measures whether the right passage was found, never whether the passage is true.

### 8. A figure that survived in notes did not survive re-checking

A working note recorded Bg 750 as a 75-day drought-tolerant variety yielding
about 70 bushels per acre. On re-check, the duration and the drought-prone
recommendation are both stated on the RRDI mitigation options page. The yield
figure is on no DOA page I could reach - not the drought-tolerant varieties
page, which names Bg 251 GSR and Bg 314 instead, and not the ultra-short-age
page, which does not mention Bg 750 at all.

So the yield figure was dropped and the duration kept. This is worth recording
because of where the error would have come from: not from a model hallucinating,
but from a human note taken one step away from the source and then trusted. The
corpus rule - every passage checked against the page it claims - exists for the
notes as much as for the model.

Harvesting was left out of batch 2 for the same reason. RRDI has no harvesting
page stating moisture content or loss figures, and those numbers are easy to
half-remember. The corpus has a gap where the source has a gap.

### 9. The error in finding 7 was already in the index, shipped

Finding 7 described a misread that *would* put a wrong fertilizer rate in front
of a farmer. It turned out not to be hypothetical. An audit of the Pinecone
index against the repo (`scripts/audit_index.py`) found 61 vectors where the
repo defined 45. Sixteen were seed passages loaded by notebook 10 from the
course repo's own `scripts/corpus.py`, and two of them carried exactly the
column shift:

> For a THREE MONTH age class variety under irrigation in the Intermediate or
> Dry Zone, apply urea as follows [...] 55 kg/ha basal, 50 kg/ha at 2 weeks,
> 75 kg/ha at 4 weeks, 65 kg/ha at 6 weeks and 35 kg/ha at 7 weeks. Total urea
> is 225 kg/ha. TSP is 25 kg/ha at 4 weeks and 35 kg/ha at 6 weeks, total
> 55 kg/ha. MOP total is 60 kg/ha.

The passage contradicts itself twice. The urea splits sum to 280 against a
stated 225. The TSP splits sum to 60 against a stated 55 - and 60 is the MOP
total named in the next sentence. All four totals are right; every split is
attached to the wrong column. The basal urea dose does not exist: that 55 kg is
TSP, and the entire TSP dose goes on basally.

Three things are worth separating out.

**It is not a hallucination.** No model produced this. It was written into a
seed corpus by a person reading a published government table, and the table
misleads because one merged cell shifts a row. Retrieval-augmented generation is
sold as the fix for models inventing facts, and here the grounding corpus was
the thing that was wrong. Citing a source does not make an answer true; it only
makes the error traceable.

**The audit was only possible because the totals were published.** Nothing about
the passage reads as suspicious - the numbers are plausible, the units are right,
the structure is conventional. It fails arithmetic, and only arithmetic. A
corpus of prose claims with no internal redundancy would have no equivalent
check.

**The two versions were live in the same index at the same time.** After batch 2
loaded, `fert-3month` and `fert-irrigated-izdz` both sat in the index, both
answering "how much fertilizer for a three month variety", with different
numbers. Which one surfaced depended on embedding similarity to the farmer's
phrasing - effectively a coin toss, and an undetectable one, because the wrong
answer cites a real DOA page. No retrieval metric distinguishes these two
passages: both are topically correct, both are on-domain, both would score as a
hit against a question about three-month fertilizer rates.

Resolution: the two bad passages were dropped and the other fourteen seed
passages carried into this repo's `corpus.py`, so the index is reproducible from
the repo alone. `scripts/drop_stale.py` removes anything in the index that the
repo no longer defines. Index and repo now agree at 59.

A suspicion that did not survive checking, recorded because the checking is the
point. Three seed passages state a 73% figure - the 3.5 month maturity class by
extent, long grain varieties by extent, and the 3.5 month group again - and one
statistic restated three times looked more likely than two attributes landing on
the same number. The RRDI socio-economics page states both separately for 2023:
3.5 month class 73%, long grain 73%, white pericarp 80%, At 362 14.25%, Bg 352
12.84%, traditional varieties 0.41%. The coincidence is real and the passages
are right. Finding 7 was caught by arithmetic and this was cleared by arithmetic
failing to catch it, which is the same discipline producing opposite verdicts.

The same page carries a second set of figures for 2021-2023 in which the most
popular variety is Bg 300 at 16.2% rather than At 362 at 14.25%, and the 3.5
month class is 70.8% rather than 73%. So "what is the most popular rice variety"
has two defensible answers from one page depending on the period, and the corpus
currently carries only one of them without saying which period it is. That is a
retrieval ambiguity rather than an error, but it is the kind that produces a
confidently wrong answer.

A side effect worth noting: finding 3 used Q1 ("fertilizer for Bg 300") as the
acceptance test for agentic RAG, on the grounds that no single passage connects
Bg 300 to a fertilizer rate. That test is unchanged - `fert-irrigated-izdz` names
the three month class and not the variety, exactly as `fert-3month` did - but it
was being run against a passage with wrong numbers. The two-hop retrieval would
have succeeded and the answer would still have been wrong.

### 10. Query rewriting cost 38 points, and the reason was in the system prompt

Raw questions retrieved the right passage 95% of the time at k=3. Rewritten,
57%. Rewriting is the step the course calls the cheapest improvement available
in RAG, and here it destroyed more than a third of the system's accuracy.

The rewrites say why:

| question | what the rewriter produced |
|---|---|
| leaves drying, plants fallen over | `sri lankan paddy cultivation database leaf drying brown fallen over` |
| something boring inside the stem, silvery tubes | `Sri Lankan paddy cultivation database symptoms` |
| which variety is grown the most | `Sri Lankan paddy cultivation database` |

The system prompt opens: *"Rewrite the farmer's message as a short search query
for a Sri Lankan paddy cultivation database."* The model is pasting that noun
phrase into its output. Finding 5 caught the same model leaking its few-shot
examples; removing the examples did not stop the leaking, it only changed what
leaked. A small model copies whatever concrete text is in front of it, and the
task description is text in front of it.

The mechanism matters more than the leak. Every query now carries the same
constant prefix, so every query vector is dragged toward the same point, and
the model stops being able to tell the questions apart. That is visible in the
results: `seasons` - the most generic passage in the corpus, and so the nearest
to its centre - becomes the top hit for three unrelated questions, including
"which variety is grown the most" and "when should I harvest". The rewriter did
not make the queries wrong. It made them all similar, which is worse.

Underneath that, specificity is stripped. "What can I spray for grass weeds and
how many days after sowing" becomes "weeds control", losing both *spray* and
*days*; it then retrieves the three weed species lists instead of the herbicide
passage, which is the only one that could answer it. In the worst case the
entire question was discarded and only the leaked phrase remained.

**An honest caveat.** The rewriter was written for messy conversational
messages - greetings, names, small talk - and the eval questions, while in a
farmer's register, are already fairly clean. So this measures the rewriter
outside the envelope it was designed for. It is a fair test of "should the app
rewrite every incoming query", and the answer to that is clearly no. It is not
a fair test of "does rewriting help on genuinely noisy input", which is still
open and needs noisy variants of these same questions.

### 11. There is no refusal threshold, and rewriting removes the chance of one

The two should-refuse questions exist to test whether the app can decline. Raw,
the separation looks workable: answerable questions average 0.5868 against
0.4744 for the refusals, a gap of 0.1124. The individual numbers kill it. "What
price will I get for my paddy this season" scores **0.5289** against
`seed-rate` - higher than several questions the corpus genuinely answers. Any
threshold low enough to let the real questions through also lets the price
question through.

Rewritten, it collapses entirely. The gap falls to 0.0365, and "when should I
harvest and at what moisture content" scores 0.5696 against `seasons` - above
the mean for answerable questions. Rewriting converts an out-of-scope question
into a generic on-domain one, and generic on-domain is exactly what scores well.

So refusal cannot be a similarity threshold, at any value, under either path.
It has to come from the generation step: structured output with a `found` flag,
where the model is shown the retrieved passages and asked whether they actually
answer the question that was asked. That is `w3-02` in the plan. This is the
evidence for why it is not optional decoration.

### 12. Retrieval is not the problem; ranking is

52% at 1 against 95% at 3 is the most actionable number here. The right passage
is nearly always retrieved - it just is not first, in almost half of cases.

Two things follow immediately. **Do not pass k=1 to the generator.** Passing the
top 3 and letting the model pick converts a 52% system into a 95% one for the
price of a few hundred tokens. And **the high-value next step is a reranker, not
a better embedding model**: swapping `text-embedding-3-small` for `-large` works
on recall, and recall is already 95%.

The gap sits almost entirely on the paraphrase questions - direct 7/9 at rank 1,
paraphrase 4/9, both 9/9 by rank 3. Asking in a farmer's words rather than the
corpus's words costs about two places of ranking, not the answer. Since real
users only ever ask in their own words, the hit@1 number is the realistic one
and the hit@3 number is the achievable one.

One correction to finding 3 falls out of this. The two-hop question retrieved
**both** needed passages inside the top 3 on the raw path. Retrieval can already
support that answer; what is missing is the step that chains them. The problem
is in the agent, not the index - which makes it a better acceptance test for
notebook 12 than it was when it looked like a retrieval failure.

### 13. Determinism showed up this time

Finding 6 recorded that `temperature=0.0` was not reproducible across runs.
Across these three runs the rewrites were byte-identical and the hit rates
identical to the percentage point - 43% and 57%, three times. The small score
wobbles in the output are Pinecone's, not the model's.

Both observations are real. Non-determinism at temperature zero appeared on
three messages and not on twenty-three. The useful conclusion is not that it is
deterministic or that it is not, but that it cannot be assumed either way, which
is why the harness takes `--runs`.

---

## Limitations

- **23 questions** is small. One question moves hit@1 by about 5 points, so
  treat 52% as "about half" and do not report a trend from it.
- **The questions and the corpus have the same author.** This is the weakest
  kind of test set: I know what is in the passages, so the questions are
  unavoidably shaped by that, even written deliberately in other words. A set
  written by someone who has not read the corpus would be worth more than
  doubling this one.
- **`--k 5` initially changed nothing**, because hit@1 and hit@3 do not depend
  on how many results are fetched. The harness now also reports hit@k. The first
  k=5 numbers in the log are therefore a duplicate of k=3, not a result.
- One embedding model, one rewrite model. No comparison against
  `text-embedding-3-large` or a larger local model.
- Findings 7, 8 and 9 are about corpus correctness, not retrieval. Nothing in
  the evaluation plan below tests whether a retrieved passage is true - only
  whether it was retrieved. That gap is not closed by adding more questions, and
  finding 9 shows it is not theoretical: two passages with contradictory numbers
  would both have scored as hits.

## Next

1. ~~Build the evaluation set and measure hit rate at 1 and 3, raw versus
   rewritten, over 3 runs.~~ Done 9 October: 52% / 95% raw, 43% / 57% rewritten.
2. **Pass the top 3 to the generator, not the top 1.** Finding 12: this is a
   52% to 95% change for a few hundred tokens, and it is the cheapest fix on
   this list by a wide margin.
3. **Take the leaked phrase out of the rewrite prompt** and re-measure. The
   system prompt names "a Sri Lankan paddy cultivation database" and the model
   copies it verbatim into every query (finding 10). Describe the target
   without naming it, then see whether rewriting is merely useless or actually
   harmful.
4. **Write noisy variants of the eval questions** - greetings, names, places,
   two questions at once - and re-run both paths. The rewriter was built for
   that input and has never been measured on it.
5. **Refusal belongs in the generator, not in a threshold** (finding 11). Build
   `w3-02` with a `found` flag and add the two refuse questions to its tests.
6. **Add a district-to-zone passage.** `ev-14` fails because nothing links
   Anuradhapura to the dry zone; the district list is on the DOA page and was
   never carried across. One passage closes it, and it is the most common way a
   real farmer would phrase the question.
7. Compare `qwen3-4b` against `gemma-4-e4b` on the rewrite step.
8. Treat Q1 as the acceptance test for agentic RAG when notebook 12 ships —
   noting finding 12: retrieval already returns both passages, so what is being
   tested is the chaining, not the index.
9. Re-check Q2 at k=5 before adding a reranker; the right passage may already be
   within reach.
10. Add a corpus check step that is separate from retrieval evaluation: for every
   passage carrying a number, re-fetch the cited page and confirm the number is
   on it. Finding 7 was caught by arithmetic and finding 8 by re-fetching, and
   neither is something a hit-rate score would have surfaced.
11. Run `scripts/audit_index.py` before every demo. Finding 9 existed for days
   because nothing compared what was deployed against what was in the repo.
12. Three seed-corpus numbers are still unverified: the seed rate (100 kg/ha
   medium grain, 75-80 kg/ha Samba, 23-25 g per 1000 seeds), the 85% germination
   threshold, and the 350-400 panicles per square metre target. None appear on
   any RRDI page reachable so far. The wet seeding page does give "~400 seeds
   per square meter", which is a seed rate and not a panicle count - close
   enough in wording and number to be worth ruling out as a conflation.
