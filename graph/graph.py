from langgraph.graph import StateGraph, START, END

from graph.state import ResearchState

from agents.memory_agent import memory_agent
from agents.information_needs_analyst import (
    information_needs_analyst
)
from agents.summarizer_agent import (
    summarizer_agent
)
from agents.research_critic import research_critic
from agents.memory_update import memory_update
from agents.rag_agent import rag_agent
from agents.web_agent import web_agent
from agents.evidence_curator import evidence_curator

from graph.routing import route_after_analyst, route_after_critic


# Create Builder
builder = StateGraph(ResearchState)

# Add Nodes
builder.add_node(
    "memory_agent",
    memory_agent
)

builder.add_node(
    "information_needs_analyst",
    information_needs_analyst
)

builder.add_node(
    "rag_agent",
    rag_agent
)

builder.add_node(
    "web_agent",
    web_agent
)

builder.add_node(
    "evidence_curator",
    evidence_curator
)

builder.add_node(
    "research_critic",
    research_critic
)

builder.add_node(
    "summarizer",
    summarizer_agent
)

builder.add_node(
    "memory_update",
    memory_update
)

# Add Start Edge
builder.add_edge(
    START,
    "memory_agent"
)

# Memory → Analyst
builder.add_edge(
    "memory_agent",
    "information_needs_analyst"
)

# Conditional Edge from Analyst
builder.add_conditional_edges(
    "information_needs_analyst",
    route_after_analyst,
    {
        "memory_only": "summarizer",

        "rag": "rag_agent",

        "web": "web_agent",

        "rag_agent": "rag_agent",

        "web_agent": "web_agent"
    }
)

# Core Execution Branches → Critic
builder.add_edge(
    "rag_agent",
    "evidence_curator"
)

builder.add_edge(
    "web_agent",
    "evidence_curator"
)

builder.add_edge(
    "evidence_curator",
    "research_critic"
)

# Adaptive Reflection Conditional Edge after Critic Evaluation
builder.add_conditional_edges(
    "research_critic",
    route_after_critic,
    {
        "approved": "summarizer",
        "retry": "information_needs_analyst",
        "max_iterations": "summarizer"
    }
)

# Summarizer → Memory Update
builder.add_edge(
    "summarizer",
    "memory_update"
)

# Memory Update → END
builder.add_edge(
    "memory_update",
    END
)

# Compile Graph
graph = builder.compile()