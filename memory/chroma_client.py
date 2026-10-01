# memory/chroma_client.py

import chromadb


client = chromadb.PersistentClient(
    path="memory/memory_db"
)


collection = client.get_or_create_collection(
    name="research_memory"
)