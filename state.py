from typing import TypedDict

class ResumeState(TypedDict):
    resume: str
    ats_score: int
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

class CareerCoachState(TypedDict):
    resume: str
    review: str
    ats_score: int
    career_goal: str
    known_skills: list[str]
    interview_feedback: list[str]
    conversation_history: list[dict]
    learning_plan: list[str]
    pending_skill_update: str | None  # Tracks skill name currently being updated
    user_action: str  # Action directive: "submit_resume", "chat", "complete_skill", "mock_interview"
    user_query: str  # Holds the latest chat message/user response input
    project_recommendations: list[dict]  # Stores portfolio project recommendation objects
