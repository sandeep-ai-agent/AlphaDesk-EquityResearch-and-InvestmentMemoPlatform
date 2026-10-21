"""Command-line entry point for annual-report ingestion."""

import argparse
from pathlib import Path

import pymupdf
from pydantic import ValidationError

from alphadesk.contracts.documents import AnnualReportMetadata
from alphadesk.services.pdf_ingestion import ingest_annual_report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Register and extract an Indian annual report."
    )
    # Create a parser with automatic --help support.

    parser.add_argument(
        "--pdf",
        required=True,
        type=Path,
    )
    # Convert the supplied PDF filename into a Path object.

    parser.add_argument(
        "--metadata",
        required=True,
        type=Path,
    )
    # Accept the source-metadata JSON file.

    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/corpus"),
    )
    # Allow storage location configuration without changing the service.

    args = parser.parse_args()

    try:
        metadata = AnnualReportMetadata.model_validate_json(
            args.metadata.read_text(encoding="utf-8")
        )
        # Read JSON and validate its values using Pydantic.

        destination = ingest_annual_report(
            pdf_path=args.pdf,
            metadata=metadata,
            output_root=args.output_root,
        )
        # Pass validated metadata and paths to the ingestion service.

    except (
        ValidationError,
        ValueError,
        OSError,
        RuntimeError,
        pymupdf.FileDataError,
    ) as exc:
        parser.exit(
            status=1,
            message=f"Ingestion failed: {exc}\n",
        )
        # Report expected input, filesystem, or PDF-processing failures.

    print(f"Ingestion completed: {destination}")
    # Print the final output location only after success.


if __name__ == "__main__":
    main()
    # Enable python -m alphadesk.ingestion.ingest_report.