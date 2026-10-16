from alphadesk.schemas import ResearchRequest, ResearchState

from typing import TypedDict
# yahan se Input modify karke bhejenge. like aapl daala toh AAPL ho jayega

def validate_request(state: ResearchState):
     # Receive the current state.
     # The return annotation describes this node's output

    request = ResearchRequest(  # Constructing this object runs Pydantic validation.
        ticker = state["ticker"].strip().upper(),
        question=state["question"],
    )

    return {  # Return state updates as a dictionary.
        "ticker": request.ticker, # Read the validated ticker from the Pydantic object.
        "question": request.question,  # Read the validated question from the Pydantic object.
    }

