from langgraph.graph import END, StateGraph

from src.graph.nodes import build_prompt, classify_intent, generate, quality_check, retrieve_context
from src.graph.state import AgentState


def route_after_check(state: AgentState) -> str:
    check = state.get("quality_check", {}) or {}
    retry = state.get("retry_count", 0)

    if check.get("pass"):
        return "pass"
    if retry >= 2:
        print("[router] retry limit reached, returning latest result")
        return "pass"

    print(f"[router] quality check failed, retry #{retry}")
    return "retry"


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("classify", classify_intent)
    workflow.add_node("retrieve", retrieve_context)
    workflow.add_node("build_prompt", build_prompt)
    workflow.add_node("generate", generate)
    workflow.add_node("check", quality_check)

    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "retrieve")
    workflow.add_edge("retrieve", "build_prompt")
    workflow.add_edge("build_prompt", "generate")
    workflow.add_edge("generate", "check")
    workflow.add_conditional_edges("check", route_after_check, {"pass": END, "retry": "retrieve"})

    return workflow.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke(
        {
            "user_query": "Generate a dark AI tool landing page with strong interactions.",
            "domain": "web_design",
            "intent": None,
            "retrieved_chunks": None,
            "context": None,
            "built_prompt": None,
            "expanded_queries": None,
            "generation_result": None,
            "quality_check": None,
            "retry_count": 0,
        }
    )
    print(result["intent"])
    print(result["quality_check"])
