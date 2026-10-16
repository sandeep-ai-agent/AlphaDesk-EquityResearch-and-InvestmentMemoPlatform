from alphadesk.schemas import ResearchRequest, ResearchState
from typing import TypedDict

class ValidatedRequestUpdate(TypedDict):
    ticker: str
    question: str


def validate_request(state: ResearchState) -> ValidatedRequestUpdate:
    request = ResearchState(
        ticker=state["ticker"].strip().upper(),
        question=state["question"],
    )

    return{
        "ticker": request.ticker,
        "question": request.question,
    }

