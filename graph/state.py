from typing import TypedDict, List, Dict, Any


class ResearchState(TypedDict):
    """
    Shared state passed between all LangGraph nodes.
    """

    # ==================================================
    # User Layer
    # ==================================================

    query: str
    thread_id: str

    # ==================================================
    # Memory Layer
    # ==================================================

    memory_hit: bool
    memory_distance: float
    memory_evidence: List[Dict[str, Any]]

    # ==================================================
    # Planning Layer
    # ==================================================

    route: str
    search_query: str
    research_plan: List[str]
    information_gaps: List[str]

    # ==================================================
    # Research Layer
    # ==================================================

    rag_evidence: List[Dict[str, Any]]
    rag_sources: List[Dict[str, Any]]

    web_evidence: List[Dict[str, Any]]
    web_sources: List[Dict[str, Any]]

    # ==================================================
    # Evidence Filtering Layer
    # ==================================================

    filtered_evidence: list
    discarded_evidence_count: int

    # ==================================================
    # Critic Layer
    # ==================================================

    critic_score: float
    critic_feedback: str
    critic_history: List[Dict[str, Any]]

    # ==================================================
    # Loop Control
    # ==================================================

    iteration_count: int
    max_iterations: int

    # ==================================================
    # Output Layer
    # ==================================================

    confidence_score: float
    final_response: str

    # ==================================================
    # Output Layer
    # ==================================================

    confidence_score: float
    final_response: str
    research_summary: dict | None

    # ==================================================
    # Memory Layer
    # ==================================================

    memory_report: str
    memory_recommendations: List[str]

def create_initial_state(
    query: str,
    thread_id: str = "default"
) -> ResearchState:
    """
    Creates an empty ResearchState.
    """

    return {
        # User
        "query": query,
        "thread_id": thread_id,

        # Memory
        "memory_hit": False,
        "memory_distance": 0.0,
        "memory_evidence": [],

        # Memory Reasoning
        "memory_report": "",
        "memory_recommendations": [],

        # Planning
        "route": "",
        "search_query": "",
        "research_plan": [],
        "information_gaps": [],

        # Research
        "rag_evidence": [],
        "rag_sources": [],
        "web_evidence": [],
        "web_sources": [],

        # Evidence Filtering
        "filtered_evidence": [],
        "discarded_evidence_count": 0,

        # Critic
        "critic_score": 0.0,
        "critic_feedback": "",
        "critic_history": [],

        # Loop
        "iteration_count": 0,
        "max_iterations": 2,

        # Output
        "confidence_score": 0.0,
        "final_response": "",
        "research_summary": None
    }