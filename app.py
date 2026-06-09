"""
Generation + interface for the Unofficial Guide (Milestone 5).

Pipeline (see planning.md):
    User query (Gradio)
      -> retrieve() top-k chunks from ChromaDB        (retriever.py)
      -> generate_response(): Groq llama-3.3-70b, grounded ONLY in those chunks
      -> answer + programmatically-built source list   (Gradio)

Grounding is ENFORCED, not merely requested:
  1. If retrieval finds nothing relevant enough (top similarity < MIN_SIMILARITY),
     the LLM is never called — a fixed refusal is returned. The model gets no
     chance to answer from its own parametric knowledge.
  2. The system prompt restricts the model to the supplied context and runs at
     low temperature.
  3. Source attribution is built in Python from the retrieved chunks' metadata and
     appended unconditionally. It does NOT depend on the LLM remembering to cite —
     the Sources list is guaranteed and maps 1:1 to the numbered context blocks.

Run: python app.py   (opens the Gradio UI)
"""

import os
from typing import List, Dict, Tuple

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve, N_RESULTS

# --- Config -----------------------------------------------------------------
load_dotenv()
GROQ_MODEL = "llama-3.3-70b-versatile"   # per planning.md Generation stage
# A query must have at least one retrieved chunk this similar, or we refuse to
# answer rather than let the model guess. Relevant eval queries scored ~0.70+;
# this floor mainly rejects off-topic queries. Tunable after seeing real results.
MIN_SIMILARITY = 0.35

REFUSAL = "I don't have enough information on that."

SYSTEM_PROMPT = """You are the Unofficial Guide to organic chemistry, answering \
strictly from real student discussions and blog posts.

GROUNDING RULES (non-negotiable):
- Answer ONLY using the numbered context passages provided in the user message.
- Do NOT use any outside or prior knowledge, even if you are confident.
- If the context does not contain enough information to answer, reply exactly: \
"I don't have enough information on that." Do not guess.
- Cite the source(s) you use inline with their bracketed label, e.g. [Reddit], [Blog 2].
- When sources disagree, present both perspectives instead of merging them.
- Be concise and specific; quote or paraphrase the actual student/blog voices."""


def _client() -> Groq:
    key = os.getenv("GROQ_API_KEY")
    if not key or key == "your_key_here":
        raise RuntimeError(
            "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
            "from https://console.groq.com"
        )
    return Groq(api_key=key)


def _source_labels(chunks: List[Dict]) -> Dict[str, str]:
    """
    Map each distinct source document to a readable citation label.

    Labels come from the source type (e.g. "Reddit", "Blog"). Chunks from the
    same document share one label; when several different documents share a type,
    they are numbered to stay distinguishable ("Blog 1", "Blog 2").
    """
    docs_by_type: Dict[str, List[str]] = {}
    for c in chunks:
        st = c.get("source_type") or "source"
        dn = c.get("doc_name", "")
        docs_by_type.setdefault(st, [])
        if dn not in docs_by_type[st]:
            docs_by_type[st].append(dn)

    labels: Dict[str, str] = {}
    for st, docs in docs_by_type.items():
        base = st.capitalize()
        for i, dn in enumerate(docs, 1):
            labels[dn] = base if len(docs) == 1 else f"{base} {i}"
    return labels


def _format_context(chunks: List[Dict], labels: Dict[str, str]) -> str:
    """Render retrieved chunks as passages tagged with their source-name label."""
    blocks = []
    for c in chunks:
        label = labels[c.get("doc_name", "")]
        title = c.get("title") or c.get("doc_name") or "unknown source"
        blocks.append(f"[{label}] ({title})\n{c['text']}")
    return "\n\n".join(blocks)


def _build_sources(chunks: List[Dict], labels: Dict[str, str]) -> str:
    """
    Build the Sources section in code from chunk metadata.

    This is the programmatic attribution guarantee: it is produced from the actual
    retrieved chunks, not from anything the LLM wrote, and it uses the same source
    labels the model was told to cite. One line per distinct source document.
    """
    lines = ["", "---", "**Sources** (this answer is grounded only in these):"]
    seen = set()
    for c in chunks:
        dn = c.get("doc_name", "")
        if dn in seen:
            continue
        seen.add(dn)
        label = labels[dn]
        title = c.get("title") or dn or "unknown source"
        url = c.get("source_url", "")
        url_part = f" — {url}" if url else ""
        lines.append(f"- **[{label}]** {title}{url_part}")
    return "\n".join(lines)


def generate_response(query: str, k: int = N_RESULTS) -> Tuple[str, List[Dict]]:
    """
    Retrieve, ground, and answer.

    Returns (answer_markdown, chunks). The answer already has the code-built
    Sources list appended. `chunks` is returned too for testing/inspection.
    """
    query = (query or "").strip()
    if not query:
        return "Please enter a question.", []

    chunks = retrieve(query, k=k)

    # --- Enforcement gate: refuse before the model can invent an answer --------
    top_sim = max((c.get("similarity", 0) for c in chunks), default=0.0)
    if not chunks or top_sim < MIN_SIMILARITY:
        return REFUSAL, chunks

    # --- Grounded generation ---------------------------------------------------
    labels = _source_labels(chunks)
    user_message = (
        f"Question: {query}\n\n"
        f"Context passages:\n\n{_format_context(chunks, labels)}\n\n"
        f"Answer the question using ONLY the passages above, citing them by their "
        f"bracketed source label."
    )

    completion = _client().chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.2,            # low temperature keeps it close to the context
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    answer = completion.choices[0].message.content.strip()

    # Source attribution is appended by code — guaranteed regardless of the LLM.
    return answer + "\n" + _build_sources(chunks, labels), chunks


# --- Gradio interface -------------------------------------------------------
EXAMPLE_QUESTIONS = [
    "What specific reasons do students mention for finding organic chemistry difficult?",
    "What study strategies do successful students recommend for organic chemistry?",
    "Does how hard organic chemistry feels depend more on the course or the instructor?",
    "What emotional challenges do students name about organic chemistry?",
]


def _chat_fn(query: str) -> str:
    answer, _ = generate_response(query)
    return answer


def build_interface() -> gr.Blocks:
    with gr.Blocks(title="The Unofficial Guide — Organic Chemistry") as demo:
        gr.Markdown(
            "# The Unofficial Guide — Organic Chemistry\n"
            "Answers are grounded **only** in real student discussions and blog posts. "
            "Every answer lists the exact sources it was built from. If the sources "
            "don't cover your question, the guide will say so rather than guess."
        )
        query_box = gr.Textbox(
            label="Your question",
            placeholder="e.g. Why do students find organic chemistry so hard?",
            lines=2,
        )
        ask_btn = gr.Button("Ask", variant="primary")
        answer_box = gr.Markdown(label="Answer")

        gr.Examples(examples=EXAMPLE_QUESTIONS, inputs=query_box)

        ask_btn.click(fn=_chat_fn, inputs=query_box, outputs=answer_box)
        query_box.submit(fn=_chat_fn, inputs=query_box, outputs=answer_box)

    return demo


if __name__ == "__main__":
    build_interface().launch()
