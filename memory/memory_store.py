from datetime import datetime
import uuid
import json

from memory.chroma_client import (
    collection
)


def build_memory_record(state):

    timestamp = (
        datetime.now()
        .isoformat()
    )

    return {

        "query":
            state["query"],

        "research_plan":
            state["research_plan"],

        "information_gaps":
            state["information_gaps"],

        "critic_feedback":
            state["critic_feedback"],

        "critic_score":
            state["critic_score"],

        "final_response":
            state["final_response"],

        "timestamp":
            timestamp
    }


def build_memory_document(
    record: dict
) -> str:

    return f"""
Query:

{record['query']}

Research Summary:

{record['final_response']}
"""


def save_memory(
    state
):

    record = (
        build_memory_record(
            state
        )
    )

    document = (
        build_memory_document(
            record
        )
    )

    memory_id = (
        str(uuid.uuid4())
    )

    collection.add(

        ids=[
            memory_id
        ],

        documents=[
            document
        ],

        metadatas=[
            {

                "query":
                    record["query"],

                "research_plan":
                    json.dumps(
                        record[
                            "research_plan"
                        ]
                    ),

                "information_gaps":
                    json.dumps(
                        record[
                            "information_gaps"
                        ]
                    ),

                "critic_feedback":
                    record[
                        "critic_feedback"
                    ],

                "critic_score":
                    float(
                        record[
                            "critic_score"
                        ]
                    ),

                "timestamp":
                    record[
                        "timestamp"
                    ],

                "final_response":
                    record[
                        "final_response"
                        ]
            }
        ]
    )

    return memory_id