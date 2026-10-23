"""Connect the research graph to our RAG answering service."""

from alphadesk.schemas import ResearchState
from alphadesk.services.answering import answer_question

def research_company(state: ResearchState):
    """Generate an answer and update the task status."""

    answer = answer_question(state["question"])

    # Copy the task given already so that we do not modify the input state instead this way
    task = state["research_task"].copy()

    # Record , that we have generated answer for this task
    task["status"] = "completed"

    # Return the two fields that Langgraph should Update
    return{
        "answer": answer,
        "research_task": task
    }
