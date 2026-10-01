from litellm import completion

from graph.state import ResearchState

from prompts.analyst import ANALYST_PROMPT

from agents.schemas import ResearchPlan

from config.rag_scope import (
    RAG_CORPUS_SCOPE
)


def build_analyst_context(
    state: ResearchState
) -> str:

    query = state["query"]

    iteration = state["iteration_count"]

    critic_feedback = (
        state["critic_feedback"]
    )

    memory_hit = (
        state["memory_hit"]
    )

    memory_report = (
        state["memory_report"]
    )

    memory_recommendations = (
        state["memory_recommendations"]
    )

    context = f"""
Query:
{query}

Iteration:
{iteration}

RAG KNOWLEDGE BASE SCOPE:

{RAG_CORPUS_SCOPE}
"""

    # ------------------------------------------
    # Memory Context
    # ------------------------------------------

    if memory_hit:

        recommendations = "\n".join(
            f"- {item}"
            for item
            in memory_recommendations
        )

        context += f"""

PREVIOUS RESEARCH INSIGHTS:

{memory_report}

PREVIOUS RESEARCH RECOMMENDATIONS:

{recommendations}

IMPORTANT:

Previous research exists for a related topic.

Reuse successful research strategies when appropriate.

Avoid repeating previously identified weaknesses.
"""

    # ------------------------------------------
    # Critic Feedback
    # ------------------------------------------

    if critic_feedback:

        context += f"""

CRITIC FEEDBACK:

{critic_feedback}

IMPORTANT:

The previous research attempt was insufficient.

Do not repeat the previous retrieval strategy.

Your goal is to identify the missing information and create a revised research plan that fills those gaps.
"""

    return context


def information_needs_analyst(
    state: ResearchState
) -> dict:

    print(
        "\n[Information Needs Analyst] Planning research..."
    )

    if state["memory_hit"]:

        print(
            "\nMemory Insights:"
        )

        print(
            state["memory_report"]
        )

        print(
            "\nMemory Recommendations:"
        )

        for item in (
            state["memory_recommendations"]
        ):

            print(
                f"- {item}"
            )

    context = build_analyst_context(
        state
    )

    response = completion(
        model="gemini/gemini-2.5-flash",
        num_retries=3,

        messages=[
            {
                "role": "system",
                "content": ANALYST_PROMPT
            },
            {
                "role": "user",
                "content": context
            }
        ],

        response_format=ResearchPlan
    )

    plan = ResearchPlan.model_validate_json(
        response.choices[0].message.content
    )

    print(
        f"Route: {plan.route}"
    )

    print(
        f"Search Query: {plan.search_query}"
    )

    print(
        "\nInformation Gaps:"
    )

    for gap in plan.information_gaps:

        print(
            f"- {gap}"
        )

    print(
        "\nResearch Plan:"
    )

    for step in plan.research_plan:

        print(
            f"- {step}"
        )

    return {
        "route": plan.route,

        "search_query":
            plan.search_query,

        "research_plan":
            plan.research_plan,

        "information_gaps":
            plan.information_gaps
    }