'''
First: split one page
The first function handles only text splitting:
- Accept page text, chunk size, and overlap.
- Reject invalid settings.
- Select a passage using string positions.
- Yield its start, end, and text.
- Move forward while retaining the overlap.
yield returns one result at a time to the calling loop.
'''

"""Create page-linked chunks from ingested report text."""

import hashlib
import json
from pathlib import Path

from alphadesk.contracts.chunks import EvidenceChunk
from alphadesk.contracts.documents import (AnnualReportMetadata, PageEvidence)

def split_page_text(text: str, chunk_size: int, overlap: int):
    """ Yield each passage with its source text-position """
    start = 0 # Begin at first character 

    while start < len(text):
        end = min(start + chunk_size, len(text))

        passage = text[start:end]

        if passage.strip():
            yield start, end, passage

        if end == len(text):
            break

        start = end - overlap   # Retain Context for the next passage and this will continue

'''
build_document_chunks():

What the function will do
1. Locate pages.jsonl.
2. Create a new chunk file.
3. Read and validate one page at a time.
4. Skip pages needing extraction review.
5. Pass page text to your existing splitter.
6. Save each passage with its document and page references.
7. Return the output filename.

'''
def build_document_chunks(
        document_dir: Path,
        chunk_size: int = 1200,
        overlap: int = 200,
) -> Path:
    pages_path = document_dir / "pages.jsonl"  # We crated page text during ingestion here
    output_path = document_dir / (f"chunks_simple_v1_s{chunk_size}_o{overlap}.jsonl")

    chunk_count = 0    # Track how many pages we have saved

    with pages_path.open("r", encoding="utf-8") as pages_file:
        # Reads source pages one line at a time.

        with output_path.open("x", encoding="utf-8") as chunks_file:
            # Creates a new file

            for line in pages_file:
                page = PageEvidence.model_validate_json(line)
                # converts json line into a validated page object
                if page.extraction_status == "needs_review":
                    continue

                passages = split_page_text(page.text, chunk_size, overlap)

                for chunk_number, (_, _, passage) in enumerate(
                    passages,
                    start=1,
                ):
                    # Number passages within this page.
                    # The two underscores ignore start/end offsets.

                    chunk = EvidenceChunk(
                        chunk_id=(
                            f"{page.document_id}:"
                            f"p{page.pdf_page_number}:"
                            f"s{chunk_size}:o{overlap}:"
                            f"c{chunk_number}"
                        ),
                        document_id=page.document_id,
                        pdf_page_number=page.pdf_page_number,
                        text=passage,
                    )
                    # Validate the passage and its source references.

                    chunks_file.write(
                        chunk.model_dump_json() + "\n"
                    )
                    # Save one chunk per JSONL line.

                    chunk_count += 1
                    # Count the successfully written chunk.

    if chunk_count == 0:
        # Report when no usable passages were found.
        raise ValueError("No chunks were created.")

    print(f"Created {chunk_count} chunks.")
    # Provide a simple development-time summary.

    return output_path
    # Return the generated file's location.






   
        





