import json
import re
from litellm import completion

from graph.state import ResearchState
from prompts.critic import CRITIC_PROMPT
from agents.schemas import CriticEvaluation


def build_evidence_context(evidence: list) -> str:
    if not evidence:
        return "No evidence available."

    formatted_evidence = []

    for idx, item in enumerate(evidence, start=1):
        source_type = item.get("source_type", "unknown")
        
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

    return "\n\n".join(formatted_evidence)


def research_critic(state: ResearchState) -> dict:
    print("\n[Research Critic] Evaluating Filtered evidence...")

    query = state["query"]

    # Future-proof evidence collection combining all sources
    all_evidence = (
        state.get("memory_evidence", [])
        + state.get("filtered_evidence", [])
    )

    evidence_text = build_evidence_context(all_evidence)
    print(f"Evidence Count: {len(all_evidence)}")
    print(f"Compiled Evidence Context:\n{evidence_text}")

    response = completion(
        model="gemini/gemini-2.5-flash",
        num_retries=3,
        messages=[
            {
                "role": "system",
                "content": CRITIC_PROMPT
            },
            {
                "role": "user",
                "content": f"Question:\n{query}\n\nEvidence:\n{evidence_text}"
            }
        ],
        response_format=CriticEvaluation
    )

    # --- BULLETPROOF CLEANUP PATCH FOR PYDANTIC JSON PARSING SAFETY ---
    raw_content = response.choices[0].message.content
    cleaned_content = raw_content.strip()
    
    # 1. Strip markdown code block wrappers if present
    if cleaned_content.startswith("```json"):
        cleaned_content = cleaned_content.split("```json")[1].rsplit("```", 1)[0].strip()
    elif cleaned_content.startswith("```"):
        cleaned_content = cleaned_content.split("```")[1].rsplit("```", 1)[0].strip()

    # 2. Convert raw literal escaped single quotes back to standard format
    cleaned_content = cleaned_content.replace("\\'", "'")

    # 3. Clean illegal backslashes that do not match valid JSON control characters
    # (Valid control escapes: ", \, /, b, f, n, r, t, u)
    cleaned_content = re.sub(r'\\([^"\\\/bfnrtu])', r'\1', cleaned_content)

    # 4. Safely validate structural compliance
    try:
        # Pass through standard python json validation first to catch anomalies
        parsed_dict = json.loads(cleaned_content)
        evaluation = CriticEvaluation.model_validate(parsed_dict)
    except Exception as e:
        print(f"\n[Parser Emergency Alert] Falling back to direct string parser due to: {e}")
        # Secondary fallback layer if the structure was already clean
        evaluation = CriticEvaluation.model_validate_json(cleaned_content)

    print(f"Score: {evaluation.critic_score}")
    print(f"Feedback: {evaluation.critic_feedback}")

    return {
        "critic_score": evaluation.critic_score,
        "critic_feedback": evaluation.critic_feedback,
        "iteration_count": state["iteration_count"] + 1
    }