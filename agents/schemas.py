from typing import Literal
from pydantic import BaseModel, Field


class ResearchPlan(BaseModel):

    route: Literal[
        "memory_only",
        "rag",
        "web",
        "hybrid"
    ]

    search_query: str

    research_plan: list[str]

    information_gaps: list[str]

    corpus_relevance: str


class MemoryInsight(BaseModel):

    summary: str

    reusable_knowledge: list[str]

    previous_gaps: list[str]

    recommendations: list[str]


class EvidenceSelection(BaseModel):

    keep_indices: list[int]

    reasoning: str


class CriticEvaluation(BaseModel):
    critic_score: float = Field(
        description=(
            "Score between 0 and 10 indicating how well "
            "the evidence answers the user's query."
        )
    )

    critic_feedback: str = Field(
        description=(
            "Evaluation of evidence quality, coverage, "
            "strengths and missing information."
        )
    )


class ResearchSummary(BaseModel):

    executive_summary: str

    key_findings: list[str]

    detailed_analysis: str

    confidence_assessment: str

    source_summary: list[str]


