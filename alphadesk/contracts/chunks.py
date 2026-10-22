from typing import Literal
from pydantic import BaseModel, Field

class EvidenceChunk(BaseModel):
    chunk_id: str
    document_id: str
    pdf_page_number: int = Field(ge=1)
    text: str = Field(min_length=1)



    # symbol: str
    # exchange: Literal["BSE","NSE"]
    # financial_year: str
    
    # text_start: str = Field(ge=0)
    # text_end: str = Field(ge=0)
    