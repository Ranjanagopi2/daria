from graph.state import ResearchState

CRITIC_THRESHOLD = 8.0


def route_after_analyst(state: ResearchState):

    route = state["route"]

    if route == "hybrid":

        print(
            "\n[Routing] Hybrid research "
            "using parallel RAG + Web..."
        )

        return [
            "rag_agent",
            "web_agent"
        ]

    return route



def route_after_critic(state: ResearchState):

    score = state["critic_score"]

    iteration = state["iteration_count"]

    max_iterations = state["max_iterations"]

    if score >= CRITIC_THRESHOLD:
        return "approved"

    if iteration >= max_iterations:
        return "max_iterations"

    return "retry"