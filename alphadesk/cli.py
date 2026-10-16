import argparse  # Parse terminal arguments.
import json  # Convert the output dictionary into printable JSON.
from pathlib import Path

from pydantic import ValidationError

from alphadesk.graphs.research import build_reseacrh_graph

def main() -> None:
    # Define the CLI entry function.
    # -> None means it does not return a useful value to its caller

     # Construct the parser.
    parser = argparse.ArgumentParser(
        description="AlphaDesk Research Intake"
    )

    # Required Arguments
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--question", required=True)

    args = parser.parse_args()

    graph = build_reseacrh_graph()

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    diagram_path = output_dir/"reseacrh_graph.png"
    diagram_path.write_bytes(graph.get_graph().draw_mermaid_png())


    # Handle Exceptions from the Execution

    try:
        result = graph.invoke(
            {
                "ticker": args.ticker,
                "question": args.question
            }
        )
    except ValidationError as exc:
        parser.exit(
            status=2,
            message=f"Invalid Research Agent:\n{exc}\n",
        )
    print(json.dumps(result["research_task"]))


