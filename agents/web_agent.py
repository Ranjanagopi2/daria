import os
from tavily import TavilyClient
from graph.state import ResearchState


def web_agent(state: ResearchState) -> dict:
    """
    LangGraph adapter for searching the web using Tavily Client.
    """

    print("\n[Web Agent] Searching web...")

    query = (
        state["search_query"]
        or state["query"]
    )

    print(
        f"[Web Agent] Query:\n{query}"
    )
    
    # --- HARD PROTECTION FOR TAVILY 400-CHARACTER LIMIT ---
    # Slice the query to 350 characters to stay safely under the API limit
    if len(query) > 350:
        print(f"[Web Agent] Warning: Query exceeded limit ({len(query)} chars). Truncating for Tavily safety.")
        query = query[:350].rsplit(' ', 1)[0] # Clean cut at the last full word
    else:
        query = query
    
    print(f"[Web Agent] Query: {query}")
    
    # Initialize TavilyClient (automatically picks up TAVILY_API_KEY from environment)
    tavily_key = os.getenv("TAVILY_API_KEY")
    client = TavilyClient(api_key=tavily_key)
    
    # Execute simple search
    response = client.search(query=query, max_results=3)
    results = response.get("results", [])

    print(f"[Web Agent] Results Found: {len(results)}")

    if not results:
        print(
            "[Web Agent] No results found."
        )

    evidence = []
    sources = []

    for item in results:
        evidence.append(
            {
                "source_type": "web",
                "title": item.get("title", "No Title"),
                "content": item.get("content", ""),
                "url": item.get("url", "")
            }
        )

        sources.append(
            {
                "title": item.get("title", "No Title"),
                "url": item.get("url", "")
            }
        )

    return {
        "web_evidence": evidence,
        "web_sources": sources
    }