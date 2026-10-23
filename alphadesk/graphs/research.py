from langgraph.graph import StateGraph,START,END
from alphadesk.schemas import ResearchState
from alphadesk.nodes.validate_request import validate_request
from alphadesk.nodes.prepare_task import prepare_task
from alphadesk.nodes.research_comapny import research_company


def build_reseacrh_graph():
    builder = StateGraph(ResearchState)

    builder.add_node("validate_request", validate_request)
    builder.add_node("prepare_task", prepare_task)
    builder.add_node("research_company", research_company)

    builder.add_edge(START, "validate_request")
    builder.add_edge("validate_request", "prepare_task")
    builder.add_edge("prepare_task", "research_company")
    builder.add_edge("research_company", END)

    # Now Let's connect to Langgraph answer node

    builder.add_edge("prepare_task", END)

    return builder.compile()