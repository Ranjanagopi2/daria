import chromadb

from sentence_transformers import SentenceTransformer

from rag.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    INITIAL_RETRIEVAL_K
)

from rag.retrieval.rerank import rerank


# =====================================================
# LOAD MODELS
# =====================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print("Embedding model loaded")


# =====================================================
# LOAD CHROMA
# =====================================================

print("Loading Chroma collection...")

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

try:
    collection = client.get_collection(
        COLLECTION_NAME
    )
except Exception:
    collection = client.get_or_create_collection(
        COLLECTION_NAME
    )

print(
    f"Collection loaded: "
    f"{COLLECTION_NAME}"
)


# =====================================================
# RETRIEVE
# =====================================================

def retrieve(query: str):

    if collection.count() == 0:
        print("[RAG Retrieval] Vector database collection is empty.")
        return []

    # ------------------------------------------
    # Embed Query
    # ------------------------------------------

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    # ------------------------------------------
    # Chroma Search
    # ------------------------------------------

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=INITIAL_RETRIEVAL_K
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    # ------------------------------------------
    # Build Evidence Objects
    # ------------------------------------------

    retrieved_docs = []

    for doc, metadata in zip(
        documents,
        metadatas
    ):

        retrieved_docs.append(
            {
                "source_type": "rag",
                
                "content": doc,

                "chapter": metadata.get(
                    "chapter"
                ),

                "section": metadata.get(
                    "section"
                ),

                "subsection": metadata.get(
                    "subsection"
                ),

                "page": metadata.get(
                    "page"
                ),

                "content_type": metadata.get(
                    "content_type"
                ),

                "source_file": metadata.get(
                    "source_file"
                )
            }
        )

    # ------------------------------------------
    # Rerank
    # ------------------------------------------

    reranked_docs = rerank(
        query,
        retrieved_docs
    )

    return reranked_docs
