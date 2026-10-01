# =====================================================
# EMBEDDINGS
# =====================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


# =====================================================
# CHROMADB
# =====================================================

CHROMA_PATH = "./rag/outputs/chroma_db"


COLLECTION_NAME = "engineering_mechanics_knowledge_base"


# =====================================================
# RETRIEVAL
# =====================================================

INITIAL_RETRIEVAL_K = 10

FINAL_EVIDENCE_K = 3


# =====================================================
# FILES
# =====================================================

KNOWLEDGE_OBJECTS_PATH = (
    "./rag/outputs/knowledge_objects.pkl"
)