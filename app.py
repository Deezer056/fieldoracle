"""FieldOracle — Hugging Face Space entry point.

Deliberately does nothing yet. The point of deploying this early is that the
URL exists, the build works and the secrets plumbing is proven, so that adding
the real retrieval in week three is an update to something healthy rather than
a first deployment under deadline.
"""
import os

import gradio as gr

PLACEHOLDER = (
    "FieldOracle is not built yet.\n\n"
    "When it is, this will answer paddy cultivation questions from Sri Lanka "
    "Department of Agriculture guidance, and cite the passage it used.\n\n"
    f"You asked: {{q}}"
)


def answer(question: str) -> str:
    if not question.strip():
        return "Ask something about paddy cultivation."
    return PLACEHOLDER.format(q=question.strip())


demo = gr.Interface(
    fn=answer,
    inputs=gr.Textbox(label="Your question", lines=3,
                      placeholder="How much urea for Bg 300 under irrigation?"),
    outputs=gr.Textbox(label="Answer", lines=8),
    title="FieldOracle",
    description="Retrieval over Sri Lanka Department of Agriculture paddy guidance. "
                "Placeholder deployment — not answering from the corpus yet.",
    flagging_mode="never",
)

if __name__ == "__main__":
    # Render (and most hosts) inject the port to bind. 7860 is Gradio's local default.
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
