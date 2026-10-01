import pickle
import chromadb

from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from rag.config import (
    KNOWLEDGE_OBJECTS_PATH,
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)


# =====================================================
# LOAD KNOWLEDGE OBJECTS
# =====================================================

print("\nLoading knowledge objects...")

with open(KNOWLEDGE_OBJECTS_PATH, "rb") as f:
    knowledge_objects = pickle.load(f)

print(f"Loaded {len(knowledge_objects)} objects")


# =====================================================
# BUILD EMBEDDING TEXT
# =====================================================

print("\nBuilding embedding text...")

for obj in knowledge_objects:

    obj["embedding_text"] = f"""
Chapter: {obj.get("chapter", "")}

Section: {obj.get("section", "")}

Subsection: {obj.get("subsection", "")}

Content:
{obj.get("content", "")}
""".strip()


# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

print("\nLoading embedding model...")

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded")


# =====================================================
# GENERATE EMBEDDINGS
# =====================================================

texts = [
    obj["embedding_text"]
    for obj in knowledge_objects
]

print("\nGenerating embeddings...")

embeddings = model.encode(
    texts,
    normalize_embeddings=True,
    show_progress_bar=True
)

print("Embeddings generated")


# =====================================================
# CREATE CHROMA CLIENT
# =====================================================

print("\nCreating Chroma database...")

Path(CHROMA_PATH).mkdir(
    parents=True,
    exist_ok=True
)

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# =====================================================
# REMOVE OLD COLLECTION
# =====================================================

try:
    client.delete_collection(
        COLLECTION_NAME
    )

    print(
        f"Deleted existing collection: "
        f"{COLLECTION_NAME}"
    )

except Exception:
    print("No existing collection found")


# =====================================================
# CREATE COLLECTION
# =====================================================

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


# =====================================================
# PREPARE RECORDS
# =====================================================

ids = []
documents = []
metadatas = []
embedding_list = []

print("\nPreparing records...")

for obj, emb in zip(
    knowledge_objects,
    embeddings
):

    ids.append(
        obj["chunk_id"]
    )

    documents.append(
        obj["content"]
    )

    embedding_list.append(
        emb.tolist()
    )

    metadata = {
        "chunk_id": str(
            obj.get("chunk_id", "")
        ),

        "chapter": str(
            obj.get("chapter", "")
        ),

        "section": str(
            obj.get("section", "")
        ),

        "subsection": str(
            obj.get("subsection", "")
        ),

        "page": int(
            obj.get("page", -1)
        ),

        "content_type": str(
            obj.get("content_type", "")
        ),

        "source_file": str(
            obj.get("source_file", "")
        )
    }

    metadatas.append(metadata)


# =====================================================
# INSERT INTO CHROMA
# =====================================================

BATCH_SIZE = 100

print("\nAdding documents...")

for i in tqdm(
    range(
        0,
        len(ids),
        BATCH_SIZE
    )
):

    collection.add(
        ids=ids[i:i+BATCH_SIZE],

        documents=documents[
            i:i+BATCH_SIZE
        ],

        embeddings=embedding_list[
            i:i+BATCH_SIZE
        ],

        metadatas=metadatas[
            i:i+BATCH_SIZE
        ]
    )


# =====================================================
# VERIFY
# =====================================================

print("\n" + "=" * 50)

print("VECTOR DATABASE BUILD COMPLETE")

print("=" * 50)

print(
    f"Collection : {COLLECTION_NAME}"
)

print(
    f"Documents  : {collection.count()}"
)

print(
    f"Location   : {CHROMA_PATH}"
)

print("=" * 50)