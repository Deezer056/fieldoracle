"""Evaluation set for FieldOracle retrieval.

Twenty-two questions with the passage that should answer each one. Written
against the 59-passage corpus, deliberately in a farmer's words rather than
the corpus's own: if the question reuses the passage's vocabulary the test
measures nothing but lexical overlap.

Fields
    q      the question as someone would actually type it
    expect passage ids that count as correct; empty means nothing should match
    need   "any" (default) or "all" - "all" is for questions that genuinely
           require two passages, where retrieving one is not an answer
    kind   direct     the answer is in one passage, asked plainly
           paraphrase one passage, but described rather than named
           two-hop    needs two passages chained; retrieval alone cannot do it
           gap        the corpus should answer it but the link is missing
           ambiguous  the corpus supports more than one defensible answer
           refuse     the corpus cannot answer; the app should say so

The refuse questions are not padding. A system that answers them confidently
is worse than one that retrieves slightly less well, and no hit-rate score
will tell you which you have.
"""

QUESTIONS = [
    # ---------------------------------------------------------------- pests
    dict(id="ev-01", kind="paraphrase",
         q="the leaves in my field are drying up and going brown and some plants have fallen over",
         expect=["pest-bph-damage"]),
    dict(id="ev-02", kind="direct",
         q="how many hoppers on a plant before it is worth spraying",
         expect=["pest-bph-threshold"]),
    dict(id="ev-03", kind="direct",
         q="which rice varieties can resist the brown plant hopper",
         expect=["pest-bph-varieties"]),
    dict(id="ev-04", kind="paraphrase",
         q="something is boring inside the stem and there are silvery tubes coming out of the plant",
         expect=["pest-gallmidge-damage"]),

    # ------------------------------------------------------------- diseases
    dict(id="ev-05", kind="paraphrase",
         q="my leaves have pointed spots with ashy grey centres and brown edges",
         expect=["dis-blast-symptoms", "dis-differential-leafspots"]),
    dict(id="ev-06", kind="paraphrase",
         q="the panicles have turned white and empty but the rest of the plant is still green",
         expect=["dis-differential-whiteheads"]),
    dict(id="ev-07", kind="direct",
         q="what fungicide for blast and how much per tank",
         expect=["dis-blast-fungicides"]),
    dict(id="ev-08", kind="paraphrase",
         q="are the round spots with dark edges the same disease as the pointed ones",
         expect=["dis-differential-leafspots"]),

    # ----------------------------------------------------------- fertilizer
    dict(id="ev-09", kind="direct",
         q="how much urea per hectare for paddy in the dry zone with canal irrigation",
         expect=["fert-irrigated-izdz", "fert-zone-comparison"]),
    dict(id="ev-10", kind="direct",
         q="I only have rain, no irrigation, and I am in the wet zone - what fertiliser",
         expect=["fert-rainfed-wz"]),
    dict(id="ev-11", kind="two-hop", need="all",
         q="what fertiliser should I put for Bg 300",
         expect=["var-3month", "fert-irrigated-izdz"]),
    dict(id="ev-12", kind="paraphrase",
         q="when do I apply the TSP, is it split like the urea",
         expect=["fert-irrigated-izdz"]),
    dict(id="ev-13", kind="direct",
         q="can I use less TSP than the recommendation",
         expect=["fert-tsp-soil-test"]),
    dict(id="ev-14", kind="gap",
         q="I farm in Anuradhapura under a tank, how much fertiliser",
         expect=["fert-irrigated-izdz"],
         note="No passage links Anuradhapura to the dry zone. The district list "
              "is on the DOA page but was not carried into the corpus."),

    # ---------------------------------------------------------------- weeds
    dict(id="ev-15", kind="paraphrase",
         q="my crop is three weeks old, is it too late to bother weeding",
         expect=["weed-critical-period"]),
    dict(id="ev-16", kind="direct",
         q="what can I spray for grass weeds and how many days after sowing",
         expect=["weed-herbicide-grass"]),
    dict(id="ev-17", kind="paraphrase",
         q="there is a weed that looks exactly like my rice, I cannot tell them apart to pull it",
         expect=["weed-echinochloa-control", "weed-echinochloa-crusgalli"]),

    # ---------------------------------------------------------------- water
    dict(id="ev-18", kind="direct",
         q="how much water does a four month crop need in Maha season",
         expect=["water-maha-requirement"]),
    dict(id="ev-19", kind="paraphrase",
         q="the tank is low this year, how do I use less water without losing yield",
         expect=["water-saturated-saving", "water-mitigation-options"]),

    # -------------------------------------------------------------- general
    dict(id="ev-20", kind="direct",
         q="what is the difference between Maha and Yala",
         expect=["seasons"]),
    dict(id="ev-21", kind="ambiguous",
         q="which rice variety is grown the most in Sri Lanka",
         expect=["var-popular", "maturity-adoption"],
         note="The DOA page gives At 362 at 14.25% for 2023 and Bg 300 at 16.2% "
              "for 2021-2023. The corpus carries only the first and does not say "
              "which period, so a confident single answer is wrong."),

    # --------------------------------------------------------- should refuse
    dict(id="ev-22", kind="refuse",
         q="when should I harvest and at what moisture content",
         expect=[],
         note="Deliberately absent: RRDI publishes no harvesting figures, so "
              "nothing was invented. The app should say it does not cover this."),
    dict(id="ev-23", kind="refuse",
         q="what price will I get for my paddy this season",
         expect=[],
         note="Out of scope entirely. Nothing in an agronomy corpus should score "
              "well here."),
]
