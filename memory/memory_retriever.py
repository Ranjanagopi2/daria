import json

from memory.chroma_client import (
    collection
)

MAX_MEMORY_DISTANCE = 1

def retrieve_memory(
    query: str
):
    results = collection.query(
        query_texts=[query],
        n_results=3,
        include=[
            "metadatas",
            "documents",
            "distances"
        ]
    )

    print(len(results["metadatas"][0]))
    
    if not results["ids"][0]:
        return {
            "memory_hit": False,
            "memory_distance": 1.0,
            "memory_similarity": 0.0,
            "memory_evidence": []
        }
    
    metadata = (
        results["metadatas"][0][0]
    )

    distance = (
        results["distances"][0][0]
    )

    memory_distance = distance

    print("Distance:", distance)

    print("Stored Query:", metadata["query"])

    if memory_distance > MAX_MEMORY_DISTANCE:

        return {
            "memory_hit": False,
            "memory_distance": memory_distance,
            "memory_evidence": []
        }
    
    memory = {

        "query":
            metadata["query"],

        "research_plan":
            json.loads(
                metadata["research_plan"]
            ),

        "information_gaps":
            json.loads(
                metadata["information_gaps"]
            ),

        "critic_feedback":
            metadata["critic_feedback"],

        "critic_score":
            metadata["critic_score"],

        "timestamp":
            metadata["timestamp"],

        "final_response":
            metadata.get("final_response", "")
    }

    return {

        "memory_hit": True,

        "memory_distance":
            distance,

        "memory_evidence":
            [memory]
    }