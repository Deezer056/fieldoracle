"""Measure retrieval quality against the evaluation set.

    uv run python scripts/evaluate.py                # raw questions, k=3
    uv run python scripts/evaluate.py --k 5          # does a bigger k rescue the misses
    uv run python scripts/evaluate.py --rewrite      # also run the LM Studio rewrite path
    uv run python scripts/evaluate.py --rewrite --runs 3   # rewriting is not deterministic

Reports hit at 1, hit at 3 and (when --k is larger) hit at k, overall and
split by question kind, then lists
every miss with what came back instead. The refuse questions are scored
separately: there is no right passage, so what matters is whether their best
score sits below the answerable ones. The gap between those two numbers is the
only honest basis for a refusal threshold.
"""
import argparse, statistics, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from langchain_pinecone import PineconeVectorStore
from fieldoracle.config import INDEX_NAME, embeddings
from fieldoracle.evalset import QUESTIONS

ap = argparse.ArgumentParser()
ap.add_argument("--k", type=int, default=3)
ap.add_argument("--rewrite", action="store_true")
ap.add_argument("--runs", type=int, default=1)
args = ap.parse_args()

K = max(args.k, 3)
store = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings())

rewrite = None
if args.rewrite:
    try:
        from fieldoracle.rewrite import rewrite
        rewrite("test message about leaf spots")
    except Exception as e:
        sys.exit(f"--rewrite needs LM Studio running at localhost:1234 with the "
                 f"server toggle on.\n  {type(e).__name__}: {e}")


def retrieve(q):
    hits = store.similarity_search_with_score(q, k=K)
    return [(d.id, s) for d, s in hits]


def scored(question, got):
    """Return (hit@1, hit@3, hit@K, top_score). Nones for refuse questions."""
    ids = [i for i, _ in got]
    gold, need = question["expect"], question.get("need", "any")
    if not gold:
        return None, None, None, got[0][1] if got else 0.0
    test = all if need == "all" else any
    return (test(g in ids[:1] for g in gold),
            test(g in ids[:3] for g in gold),
            test(g in ids[:K] for g in gold),
            got[0][1] if got else 0.0)


def run_once(use_rewrite):
    rows = []
    for question in QUESTIONS:
        q = question["q"]
        if use_rewrite:
            try:
                q = rewrite(q)
            except Exception as e:
                print(f"  rewrite failed on {question['id']}: {e}")
        got = retrieve(q)
        h1, h3, hk, top = scored(question, got)
        rows.append(dict(question=question, query=q, got=got,
                         h1=h1, h3=h3, hk=hk, top=top))
    return rows


def report(rows, label):
    answerable = [r for r in rows if r["h1"] is not None]
    refuse = [r for r in rows if r["h1"] is None]
    n = len(answerable)
    h1 = sum(r["h1"] for r in answerable)
    h3 = sum(r["h3"] for r in answerable)
    hk = sum(r["hk"] for r in answerable)

    print(f"\n{'=' * 74}\n{label}   k={K}   {n} answerable + {len(refuse)} refuse\n{'=' * 74}")
    print(f"  hit@1   {h1}/{n}   {h1 / n:.0%}")
    print(f"  hit@3   {h3}/{n}   {h3 / n:.0%}")
    if K != 3:
        print(f"  hit@{K}   {hk}/{n}   {hk / n:.0%}")

    kinds = sorted({r["question"]["kind"] for r in answerable})
    print("\n  by kind")
    for kind in kinds:
        sub = [r for r in answerable if r["question"]["kind"] == kind]
        a = sum(r["h1"] for r in sub)
        b = sum(r["h3"] for r in sub)
        print(f"    {kind:<11} {len(sub):>2}q   hit@1 {a}/{len(sub)}   hit@3 {b}/{len(sub)}")

    if refuse:
        ans_top = statistics.mean(r["top"] for r in answerable)
        ref_top = statistics.mean(r["top"] for r in refuse)
        print(f"\n  refusal separation")
        print(f"    mean top score, answerable  {ans_top:.4f}")
        print(f"    mean top score, should-refuse {ref_top:.4f}")
        print(f"    gap {ans_top - ref_top:+.4f}"
              f"{'   <- too small to threshold on' if ans_top - ref_top < 0.05 else ''}")
        for r in refuse:
            print(f"      {r['question']['id']}  top {r['top']:.4f}  {r['got'][0][0]}")

    misses = [r for r in answerable if not r["hk"]]
    if misses:
        print(f"\n  missed at k={K} ({len(misses)})")
        for r in misses:
            qn = r["question"]
            print(f"\n    {qn['id']} [{qn['kind']}] {qn['q']}")
            if r["query"] != qn["q"]:
                print(f"      rewritten: {r['query']!r}")
            print(f"      wanted:    {', '.join(qn['expect'])}"
                  f"{'  (all of them)' if qn.get('need') == 'all' else ''}")
            for i, (vid, s) in enumerate(r["got"][:K], 1):
                print(f"      got {i}:     {s:.4f}  {vid}")
            if qn.get("note"):
                print(f"      note:      {qn['note']}")

    partial = [r for r in answerable
               if not r["hk"] and any(g in [i for i, _ in r["got"]] for g in r["question"]["expect"])]
    if partial:
        print(f"\n  partial: {len(partial)} two-hop question(s) retrieved one of the two needed passages")
    return h1 / n, h3 / n


print(f"index {INDEX_NAME!r}   {len(QUESTIONS)} questions")
report(run_once(False), "RAW QUESTIONS")

if args.rewrite:
    results = []
    for i in range(args.runs):
        rows = run_once(True)
        results.append(report(rows, f"REWRITTEN  (run {i + 1} of {args.runs})"))
    if args.runs > 1:
        print(f"\n  across {args.runs} runs:"
              f"  hit@1 {statistics.mean(r[0] for r in results):.0%}"
              f"  (spread {min(r[0] for r in results):.0%}-{max(r[0] for r in results):.0%})"
              f"   hit@3 {statistics.mean(r[1] for r in results):.0%}")
