from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.agents.verifier import verify_intelligence

from app.services.intelligence_service import IntelligenceService

intelligence_service = IntelligenceService()

async def analyse_node(state: AgentState):

    try:

        intelligence = await intelligence_service.analyse(
            state["profile"]
        )

        return {
            "intelligence": intelligence,
        }

    except Exception as exc:

        return {
            "errors": [
                *state.get("errors", []),
                str(exc),
            ]
        }

def verification_node(state: AgentState):

    intelligence = state.get("intelligence")

    if intelligence is None:

        return {
            "errors": [
                *state.get("errors", []),
                "No intelligence available for verification.",
            ]
        }

    verified, summary = verify_intelligence(
        intelligence=intelligence,
        profile=state["profile"],
    )

    return {
        "intelligence": verified,
        "verification_summary": summary,
    }

def route_after_analysis(state: AgentState):

    if state.get("errors"):
        return "end"

    if not state.get("intelligence"):
        return "end"

    return "verify"

def build_intelligence_graph():

    workflow = StateGraph(AgentState)

    workflow.add_node(
        "analyse",
        analyse_node,
    )

    workflow.add_node(
        "verify",
        verification_node,
    )

    workflow.add_edge(START, "analyse")

    workflow.add_conditional_edges(
        "analyse",
        route_after_analysis,
        {
            "verify": "verify",
            "end": END,
        },
    )

    workflow.add_edge("verify", END)

    return workflow.compile()

intelligence_graph = build_intelligence_graph()