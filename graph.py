# pyrefly: ignore [missing-import]
from langgraph.graph import StateGraph, START, END
from state import CareerCoachState
from nodes import (
    extract_fields,
    analyze_skills,
    calculate_ats,
    generate_recommendations,
    chat_node,
    resume_updater_node,
    mock_interview_node
)
from checkpointer import get_checkpointer

# 1. Initialize StateGraph with CareerCoachState
workflow = StateGraph(CareerCoachState)

# 2. Add all nodes
workflow.add_node("extract_fields", extract_fields)
workflow.add_node("analyze_skills", analyze_skills)
workflow.add_node("calculate_ats", calculate_ats)
workflow.add_node("generate_recommendations", generate_recommendations)
workflow.add_node("chat_node", chat_node)
workflow.add_node("resume_updater_node", resume_updater_node)
workflow.add_node("mock_interview_node", mock_interview_node)

# 3. Define action routing
def route_action(state: CareerCoachState) -> str:
    action = state.get("user_action", "chat")
    if action == "submit_resume":
        return "extract_fields"
    elif action == "chat":
        return "chat_node"
    elif action == "complete_skill":
        return "resume_updater_node"
    elif action == "mock_interview":
        return "mock_interview_node"
    else:
        return "chat_node"

# 4. Connect transitions
workflow.add_conditional_edges(
    START,
    route_action,
    {
        "extract_fields": "extract_fields",
        "chat_node": "chat_node",
        "resume_updater_node": "resume_updater_node",
        "mock_interview_node": "mock_interview_node"
    }
)

# Sequential pipeline flow
workflow.add_edge("extract_fields", "analyze_skills")
workflow.add_edge("analyze_skills", "calculate_ats")

# Resume update flow loops back to calculation and report generation
workflow.add_edge("resume_updater_node", "calculate_ats")

# Final calculation step goes to recommendations, then to END
workflow.add_edge("calculate_ats", "generate_recommendations")
workflow.add_edge("generate_recommendations", END)

# Chat and mock interview turns end directly after execution
workflow.add_edge("chat_node", END)
workflow.add_edge("mock_interview_node", END)

# 5. Compile with checkpointer
checkpointer = get_checkpointer()
app = workflow.compile(checkpointer=checkpointer)
