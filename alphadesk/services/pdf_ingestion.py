"""Preserve an annual report and extract page-level evidence."""

import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pymupdf

from alphadesk.contracts.documents import (
    AnnualReportMetadata,
    PageEvidence,
)


MAX_PDF_BYTES = 50 * 1024 * 1024
MAX_PAGES = 1000

# Change this when extraction behavior changes.
PIPELINE_VERSION = "pdf-text_version_1"


def ingest_annual_report(
    pdf_path: Path,
    metadata: AnnualReportMetadata,
    output_root: Path,
) -> Path:
    """Extract one local PDF and return its completed output folder."""

    # is_file is a method: parentheses execute the check.
    if not pdf_path.is_file():
        raise ValueError(f"PDF file not found: {pdf_path}")

    # stat() returns file information; st_size is an integer attribute.
    if pdf_path.stat().st_size > MAX_PDF_BYTES:
        raise ValueError("PDF file exceeds the 50 MiB limit.")

    pdf_bytes = pdf_path.read_bytes()

    # Recheck in case the file changed after the initial size check.
    if len(pdf_bytes) > MAX_PDF_BYTES:
        raise ValueError("PDF file exceeds the 50 MiB limit.")

    document_id = hashlib.sha256(pdf_bytes).hexdigest()

    output_root.mkdir(parents=True, exist_ok=True)

    destination = output_root / f"{document_id}_{PIPELINE_VERSION}"

    if destination.exists():
        raise ValueError(f"Output already exists: {destination}")

    # Everything using staging must remain inside this block.
    with tempfile.TemporaryDirectory(
        prefix=".ingest-",
        dir=output_root,
    ) as temporary_directory:
        staging = Path(temporary_directory) / "report"

        # Call mkdir() to actually create the folder.
        staging.mkdir()

        (staging / "source.pdf").write_bytes(pdf_bytes)

        empty_pages: list[int] = []

        # This block is nested INSIDE TemporaryDirectory.
        with pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf",
        ) as document:
            if document.needs_pass:
                raise ValueError(
                    "Password-protected PDFs are not supported."
                )

            page_count = document.page_count

            if not 1 <= page_count <= MAX_PAGES:
                raise ValueError(
                    "PDF page count is outside the supported range."
                )

            pages_path = staging / "pages.jsonl"

            with pages_path.open("w", encoding="utf-8") as output:
                for page_index in range(page_count):
                    page = document.load_page(page_index)
                    page_number = page_index + 1

                    text = page.get_text(
                        "text",
                        sort=True,
                    ).strip()

                    if not text:
                        empty_pages.append(page_number)

                    evidence = PageEvidence(
                        document_id=document_id,
                        evidence_id=(
                            f"{document_id}:page:{page_number}"
                        ),
                        pdf_page_number=page_number,
                        pdf_page_label=page.get_label() or None,
                        text=text,
                        extraction_status=(
                            "text_extracted"
                            if text
                            else "needs_review"
                        ),
                    )

                    output.write(
                        evidence.model_dump_json() + "\n"
                    )

        # The PDF is closed, but the staging directory still exists.
        manifest = {
            "manifest_version": "1",
            "pipeline_version": PIPELINE_VERSION,
            "parser": "pymupdf",
            "parser_version": pymupdf.VersionBind,
            "document_id": document_id,
            "source_metadata": metadata.model_dump(mode="json"),
            "acquisition_method": "local_pdf_import",
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "size_bytes": len(pdf_bytes),
            "page_count": page_count,
            "empty_text_pages": empty_pages,
            "raw_file": "source.pdf",
            "pages_file": "pages.jsonl",
        }

        (staging / "manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8",
        )

        # Move completed output before TemporaryDirectory cleans up.
        staging.rename(destination)

    return destination