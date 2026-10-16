#ResearchRequest
#ResearchTask
#ResearchState

from pydantic import BaseModel, Field

# BaseModel provides runtime validation.
# Field adds validation rules to individual fields.

from typing import TypedDict, Annotated, Any, NotRequired

# TypedDict describes the expected keys and value types of dictionaries.
# NotRequired means a particular dictionary key may be absent.

class ResearchRequest(BaseModel):
    """Validated research input."""
    
    ticker: str = Field(
        min_length=1,
        max_length=20,
        pattern = r"^[A-Z][A-Z0-9.-]*$",
    )
    question: str = Field(
        min_length= 10,
        max_length=2000,
    )

class ResearchTask(TypedDict):
    # Describe the dictionary representing one work item.
    specialist: str  # Which specialist should handle the task
    ticker: str # Which company identifier the task concerns.
    question: str  # What the specialist should investigate.
    status: str  # The current task status

class ResearchState(TypedDict):
    question: str
    ticker: str
    research_task: NotRequired[ResearchTask] 
    # Added later by prepare_task.
    # It does not need to exist when execution starts.

