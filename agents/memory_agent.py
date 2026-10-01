# agents/memory_agent.py

from unittest import result

from graph.state import ResearchState

from litellm import completion

from agents.schemas import (
    MemoryInsight
)

from prompts.memory import (
    MEMORY_ANALYST_PROMPT
)

from memory.memory_retriever import (
    retrieve_memory
)


def build_memory_context(
    memories: list
) -> str:
    context = []

    for idx, memory in enumerate(
        memories,
        start=1
    ):

        context.append(
            f"""
        Memory {idx}

        Query:
        {memory['query']}

        Research Plan:
        {memory['research_plan']}

        Information Gaps:
        {memory['information_gaps']}

        Critic Feedback:
        {memory['critic_feedback']}

        Final Response:
        {memory['final_response']}
        """
        )

    return "\n\n".join(context)


def memory_agent(
    state: ResearchState
) -> dict:

    print(
        "\n[Memory Agent] Checking memory..."
    )

    result = retrieve_memory(
        state["query"]
    )

    print(
        f"Memory Hit: "
        f"{result['memory_hit']}"
    )

    dist = result.get("memory_distance", 1.0)
    print(
        f"Distance: "
        f"{dist:.3f}"
    )

    memory_context = (
        build_memory_context(
            result["memory_evidence"]
        )
    )

    if not result["memory_hit"]:

        return {

            **result,

            "memory_report": "",

            "memory_recommendations": []
        }

    user_prompt = f"""
    Current Query:

    {state["query"]}

    Retrieved Research Memories:

    {memory_context}
    """

    response = completion(
        model="gemini/gemini-2.5-flash",
        num_retries=3,

        messages=[

            {
                "role": "system",
                "content":
                MEMORY_ANALYST_PROMPT
            },

            {
                "role": "user",
                "content":
                user_prompt
            }
        ],

        response_format=
     MemoryInsight
    )

    insight = (
        MemoryInsight
        .model_validate_json(
            response
            .choices[0]
            .message
            .content
        )
    )

    print(
        "\n[Memory Agent] "
        "Memory Analysis Complete"
    )

    print(
        f"Summary: "
        f"{insight.summary}"
    )

    print(
        "\nRecommendations:"
    )

    for item in (
        insight.recommendations
    ):
        print(
            f"- {item}"
        )

    return {

        "memory_hit":
            result["memory_hit"],

        "memory_distance":
            result[
                "memory_distance"
            ],

        "memory_evidence":
            result[
                "memory_evidence"
            ],

        "memory_report":
            insight.summary,

        "memory_recommendations":
            insight.recommendations
    }
