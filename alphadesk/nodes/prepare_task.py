from alphadesk.schemas import ResearchState,ResearchTask
from typing import TypedDict

def prepare_task(state: ResearchState):
    # Receive the normalized state.
    task: ResearchTask = {   # Construct a dictionary matching the ResearchTask contract.
        "specialist": "fundamental Agents",
         # Assign this initial task to the Fundamentals Agent.
        "ticker": state["ticker"],
        # Reuse the normalized company ticker.
        "question": state["question"],
        # Reuse the validated question.

        "status": "pending_research"
        # State explicitly that research has not started.
    }

    return {"research_task": task}
    # Return only the field this node adds.


