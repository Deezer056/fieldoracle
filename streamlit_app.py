"""FieldOracle — deployed entry point (Streamlit Community Cloud).

Deliberately answers nothing yet. Deployed early on purpose: the URL exists,
the build works, and the secrets plumbing is proven, so adding real retrieval
in week three is an update to something healthy rather than a first deployment
against a deadline.

Why Streamlit and not Gradio, which the course teaches: as of October 2026
Hugging Face requires a PRO subscription for Gradio Spaces, and Render, Railway
and Fly all require a card on file. Streamlit Community Cloud is free with no
payment method. The retrieval layer underneath is framework-independent, so
this is a UI decision, not an architectural one.
"""
import streamlit as st

st.set_page_config(page_title="FieldOracle", page_icon="🌾", layout="centered")

st.title("🌾 FieldOracle")
st.caption(
    "Paddy cultivation answers from Sri Lanka Department of Agriculture guidance. "
    "Placeholder deployment — not answering from the corpus yet."
)

with st.sidebar:
    st.subheader("Status")
    st.write("**Corpus** — 19 passages indexed")
    st.write("**Retrieval** — built, not wired to this page")
    st.write("**Answering** — week 3")
    st.divider()
    st.caption("Source: Department of Agriculture / RRDI, doa.gov.lk")

question = st.text_area(
    "Your question",
    placeholder="How much urea for Bg 300 under irrigation, and when?",
    height=100,
)

if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Ask something about paddy cultivation.")
    else:
        st.info(
            "FieldOracle is not answering yet.\n\n"
            "When it is, this will retrieve the relevant Department of Agriculture "
            "passage, answer only from it, cite the source, and say plainly when the "
            "guidance does not cover the question."
        )
        st.caption(f"You asked: {question.strip()}")

st.divider()
st.caption(
    "Free hosting sleeps after a period of inactivity, so the first visit after a "
    "quiet spell takes a moment to wake."
)
