"""Validated contracts for annual reports and extracted pages."""

from pydantic import BaseModel,Field,HttpUrl

from typing import Literal
# Literal restricts a value to explicitly listed options.

class AnnualReportMetadata(BaseModel):
    """Source details supplied when registering a Report"""

    company_name: str = Field(min_length=1, max_length=100)
    exchange: Literal["BSE", "NSE"]
    symbol: str = Field(
        min_length=1,
        max_length=100,
        pattern=r"^[A-Z0-9&.-]+$"
    )
    financial_year : str = Field(pattern=r"^FY\d{4}-\d{2}$")
    document_type: str = Literal["annual_report"]  # This pipeline currently accepts annual reports only.
   
    source_url: HttpUrl
    # Record the original source URL
    # URL validation does not prove the document's authenticity.



class PageEvidence(BaseModel):
    document_id: str  # Identify the original document by its SHA-256 fingerprint.
    evidence_id: str   # Identify this particular document/page combination
    pdf_page_number: int  # Use one-based page numbers for human-facing references.
    pdf_page_label: str | None = None # Preserve the PDF label when available.
    text: str   # Text extracted from the page; it may be empty.
    extraction_status: Literal["text_extracted", "needs_review"]   # Empty-text pages need investigation, potentially OCRs



