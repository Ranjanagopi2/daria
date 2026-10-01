from rag.retrieval.retrieve import retrieve


# =====================================================
# RAG SEARCH
# =====================================================

def search(query: str):

    evidence = retrieve(query)

    sources = []

    for item in evidence:

        source = {
            "chapter": item.get(
                "chapter"
            ),

            "section": item.get(
                "section"
            ),

            "subsection": item.get(
                "subsection"
            ),

            "page": item.get(
                "page"
            )
        }

        sources.append(source)

    return {
        "query": query,

        "retrieval_metadata": {
            "initial_candidates": 10,
            "final_evidence": 3,
            "retrieval_method":
                "bge+chroma+cross_encoder"
        },

        "evidence": evidence,

        "sources": sources
}
