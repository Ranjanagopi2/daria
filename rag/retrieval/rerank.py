from sentence_transformers import CrossEncoder

from rag.config import (
    RERANKER_MODEL,
    FINAL_EVIDENCE_K
)

# =====================================================
# LOAD MODEL ONCE
# =====================================================

print("Loading reranker...")

reranker = CrossEncoder(
    RERANKER_MODEL
)

print("Reranker loaded")


# =====================================================
# RERANK
# =====================================================

def rerank(
    query: str,
    retrieved_docs: list
):

    if not retrieved_docs:
        return []

    pairs = [
        (
            query,
            doc["content"]
        )
        for doc in retrieved_docs
    ]

    scores = reranker.predict(
        pairs
    )

    for doc, score in zip(
        retrieved_docs,
        scores
    ):
        doc["rerank_score"] = float(score)

    reranked_docs = sorted(
        retrieved_docs,
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked_docs[
        :FINAL_EVIDENCE_K
    ]