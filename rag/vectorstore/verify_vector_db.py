import chromadb

from rag.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
)


# =====================================================
# LOAD COLLECTION
# =====================================================

print("\nLoading Chroma collection...")

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

print(
    f"Documents: "
    f"{collection.count()}"
)


# =====================================================
# TEST QUERIES
# =====================================================

TEST_QUERIES = [
    "What is statics?",
    "What is Newton's First Law?",
    "What is torque?",
    "What is a scalar quantity?"
]


# =====================================================
# RUN TESTS
# =====================================================

for query in TEST_QUERIES:

    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for rank, (doc, meta) in enumerate(
        zip(documents, metadatas),
        start=1
    ):

        print(f"\nResult #{rank}")

        print(
            f"Chapter   : "
            f"{meta.get('chapter')}"
        )

        print(
            f"Section   : "
            f"{meta.get('section')}"
        )

        print(
            f"Subsection: "
            f"{meta.get('subsection')}"
        )

        print(
            f"Page      : "
            f"{meta.get('page')}"
        )

        print("\nContent:")
        print("-" * 40)

        print(doc[:500])

        print("-" * 40)