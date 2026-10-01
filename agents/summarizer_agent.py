from litellm import completion

from graph.state import ResearchState

from agents.schemas import ResearchSummary

from prompts.summarizer import (
    SUMMARIZER_PROMPT
)


def build_evidence_context(
    evidence: list
) -> str:

    if not evidence:
        return "No evidence available."

    formatted_evidence = []

    for idx, item in enumerate(
        evidence,
        start=1
    ):

        source_type = item.get(
            "source_type",
            "unknown"
        )
        
        if source_type == "rag":

            formatted_evidence.append(
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
            
        elif source_type == "web":

            formatted_evidence.append(
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

    return "\n\n".join(
        formatted_evidence
    )


def summarizer_agent(
    state: ResearchState
) -> dict:

    print(
        "\n[Summarizer Agent] "
        "Generating report..."
    )

    query = state["query"]

    evidence = (
        state["filtered_evidence"]
    )

    critic_score = (
        state["critic_score"]
    )

    critic_feedback = (
        state["critic_feedback"]
    )

    evidence_context = (
        build_evidence_context(
            evidence
        )
    )

    user_prompt = f"""
User Query:

{query}

Research Critic Score:

{critic_score}

Research Critic Feedback:

{critic_feedback}

Validated Evidence:

{evidence_context}

"""
    
    response = completion(
        model="gemini/gemini-2.5-flash",
        num_retries=3,

        messages=[
            {
                "role": "system",
                "content":
                SUMMARIZER_PROMPT
            },
            {
                "role": "user",
                "content":
                user_prompt
            }
        ],

        response_format=
        ResearchSummary
    )

    summary = (
        ResearchSummary
        .model_validate_json(
            response
            .choices[0]
            .message
            .content
        )
    )

    final_response = f"""
# Executive Summary

{summary.executive_summary}

# Key Findings

{chr(10).join(
    f"- {item}"
    for item
    in summary.key_findings
)}

# Detailed Analysis

{summary.detailed_analysis}

# Sources

{chr(10).join(
    f"- {item}"
    for item
    in summary.source_summary
)}

# Confidence Assessment

{summary.confidence_assessment}
"""
    
    print(
        f"[Summarizer Agent] "
        f"Report generated."
    )

    return {
        "final_response": final_response,

        "research_summary":
            summary.model_dump(),

        "source_summary":
            summary.source_summary
}