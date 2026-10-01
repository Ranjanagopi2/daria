from graph.state import ResearchState
from rag.retrieval.rag_agent import search


def rag_agent(state: ResearchState) -> dict:
    """
    LangGraph adapter for the RAG subsystem.
    """

    print("\n[RAG Agent] Retrieving knowledge...")

    base_query = (
        state["search_query"]
        or state["query"]
    )

    gaps = " ".join(
        state["information_gaps"]
    )

    query = f"""
    {base_query}

    {gaps}
    """

    print(
        f"[RAG Agent] Query:\n{query}"
    )

    result = search(query)

    return {
        "rag_evidence": result["evidence"],
        "rag_sources": result["sources"]
    }