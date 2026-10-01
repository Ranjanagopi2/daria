from graph.state import ResearchState
from memory.memory_store import (
    save_memory
)


def memory_update(
    state
):

    print(
        "\n[Memory Update] "
        "Saving research..."
    )

    memory_id = (
        save_memory(state)
    )

    print(
        f"[Memory Update] "
        f"Memory ID: {memory_id}"
    )

    return {}