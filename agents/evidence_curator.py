import os
from litellm import completion

from graph.state import ResearchState

from agents.schemas import EvidenceSelection

from prompts.evidence_curator import (
    EVIDENCE_CURATOR_PROMPT
)


def build_evidence_context(
    state: ResearchState
) -> tuple[list, str]:

    all_evidence = (
        state["rag_evidence"]
        + state["web_evidence"]
    )

    context = []

    for idx, item in enumerate(
        all_evidence
    ):

        if item.get(
            "source_type"
        ) == "rag":

            context.append(
                f"""
        Evidence {idx}

        Source Type:
        Textbook

        Chapter:
        {item.get('chapter', 'Unknown')}

        Section:
        {item.get('section', 'Unknown')}

        Page:
        {item.get('page', 'Unknown')}

        Content:
        {item.get('content', '')}
        """
        )
            
        else:

            context.append(
                f"""
        Evidence {idx}

        Source Type:
        Web

        Title:
        {item.get('title', 'Unknown')}

        URL:
        {item.get('url', 'Unknown')}

        Content:
        {item.get('content', '')}
        """
        )

    return (
        all_evidence,
        "\n".join(context)
    )


def evidence_curator(
    state: ResearchState
) -> dict:

    print(
        "\n[Evidence Curator] "
        "Filtering evidence..."
    )

    all_evidence, evidence_context = (
        build_evidence_context(state)
    )

    if not all_evidence:

        return {
            "filtered_evidence": [],
            "discarded_evidence_count": 0
        }

    query = state["query"]

    model_name = "groq/llama-3.3-70b-versatile" if os.getenv("GROQ_API_KEY") else "gemini/gemini-2.5-flash"
    response = completion(
        model=model_name,
        num_retries=3,

        messages=[
            {
                "role": "system",
                "content":
                    EVIDENCE_CURATOR_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Question:
{query}

Evidence:
{evidence_context}
"""
            }
        ],

        response_format=EvidenceSelection
    )

    selection = (
        EvidenceSelection
        .model_validate_json(
            response
            .choices[0]
            .message
            .content
        )
    )

    keep_indices = set(
        selection.keep_indices
    )

    filtered_evidence = [

        evidence

        for idx, evidence

        in enumerate(all_evidence)

        if idx in keep_indices
    ]

    discarded_count = (
        len(all_evidence)
        - len(filtered_evidence)
    )

    print(
        f"[Evidence Curator] "
        f"Total Evidence: {len(all_evidence)}"
        f"Kept: {len(filtered_evidence)} | "
        f"Discarded: {discarded_count}"
    )

    print(
        f"[Evidence Curator] "
        f"Reasoning: "
        f"{selection.reasoning}"
    )

    return {
        "filtered_evidence":
            filtered_evidence,

        "discarded_evidence_count":
            discarded_count
    }