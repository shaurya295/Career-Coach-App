# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from state import CareerCoachState
from llm import get_llm
from prompts import (
    EXTRACT_FIELDS_PROMPT,
    ANALYZE_SKILLS_PROMPT,
    CALCULATE_ATS_PROMPT,
    GENERATE_RECOMMENDATIONS_PROMPT,
    CHAT_PROMPT,
    RESUME_UPDATER_PROMPT,
    MOCK_INTERVIEW_START_PROMPT,
    MOCK_INTERVIEW_EVALUATE_PROMPT
)

# 1. Pydantic Models for Structured Output
class ExtractedSkills(BaseModel):
    known_skills: list[str] = Field(
        description="Key technical skills, frameworks, languages, and tools found in the resume."
    )

class ProjectRecommendation(BaseModel):
    title: str = Field(description="Title of the recommended project.")
    description: str = Field(description="Detailed description of what the project does and how it bridges the skill gap.")
    technologies: list[str] = Field(description="Key technologies and tools to use in the project.")

class SkillGapAnalysis(BaseModel):
    learning_plan: list[str] = Field(
        description="Recommended skills, languages, or tools the candidate should learn to resolve gaps."
    )
    project_recommendations: list[ProjectRecommendation] = Field(
        description="2-3 specific, actionable portfolio project ideas that bridge the gap to their career goal."
    )

class ATSScore(BaseModel):
    ats_score: int = Field(
        description="A calculated ATS optimization score from 0 to 100."
    )

# 2. Node Functions
def extract_fields(state: CareerCoachState) -> dict:
    llm = get_llm()
    structured_llm = llm.with_structured_output(ExtractedSkills)
    prompt_text = EXTRACT_FIELDS_PROMPT.format(resume=state.get("resume", ""))
    result: ExtractedSkills = structured_llm.invoke(prompt_text)
    return {"known_skills": result.known_skills}

def analyze_skills(state: CareerCoachState) -> dict:
    llm = get_llm()
    structured_llm = llm.with_structured_output(SkillGapAnalysis)
    prompt_text = ANALYZE_SKILLS_PROMPT.format(
        known_skills=", ".join(state.get("known_skills", [])) if state.get("known_skills") else "None",
        career_goal=state.get("career_goal", "") or "General Professional Development"
    )
    try:
        result: SkillGapAnalysis = structured_llm.invoke(prompt_text)
        return {
            "learning_plan": result.learning_plan,
            "project_recommendations": [p.dict() for p in result.project_recommendations]
        }
    except Exception as e:
        # Fallback to prevent crash if local LLM fails to output valid JSON for the Pydantic schema
        return {
            "learning_plan": ["PyTorch", "TensorFlow", "Docker", "Kubernetes", "AWS"],
            "project_recommendations": [
                {
                    "title": "Machine Learning Model Deployment Pipeline",
                    "description": "Build and containerize a predictive model using Docker and PyTorch, deploying it to AWS.",
                    "technologies": ["PyTorch", "Docker", "AWS"]
                },
                {
                    "title": "Collaborative Filtering Recommendation System",
                    "description": "Develop a movie or product recommendation engine using TensorFlow and matrix factorization algorithms.",
                    "technologies": ["TensorFlow", "Matrix Factorization", "Python"]
                }
            ]
        }


def calculate_ats(state: CareerCoachState) -> dict:
    llm = get_llm()
    structured_llm = llm.with_structured_output(ATSScore)
    prompt_text = CALCULATE_ATS_PROMPT.format(
        resume=state.get("resume", ""),
        known_skills=", ".join(state.get("known_skills", [])) if state.get("known_skills") else "None",
        learning_plan=", ".join(state.get("learning_plan", [])) if state.get("learning_plan") else "None"
    )
    result: ATSScore = structured_llm.invoke(prompt_text)
    return {"ats_score": result.ats_score}

def generate_recommendations(state: CareerCoachState) -> dict:
    llm = get_llm()
    prompt_text = GENERATE_RECOMMENDATIONS_PROMPT.format(
        resume=state.get("resume", ""),
        known_skills=", ".join(state.get("known_skills", [])) if state.get("known_skills") else "None",
        learning_plan=", ".join(state.get("learning_plan", [])) if state.get("learning_plan") else "None",
        ats_score=state.get("ats_score", 0)
    )
    result = llm.invoke(prompt_text)
    return {"review": result.content}

def chat_node(state: CareerCoachState) -> dict:
    llm = get_llm()
    
    # Format conversation history
    history = list(state.get("conversation_history", []))
    history_str = ""
    for msg in history:
        role = msg.get("role", "User")
        content = msg.get("content", "")
        history_str += f"{role.capitalize()}: {content}\n"
        
    prompt_text = CHAT_PROMPT.format(
        career_goal=state.get("career_goal", "") or "General",
        ats_score=state.get("ats_score", 0),
        known_skills=", ".join(state.get("known_skills", [])) if state.get("known_skills") else "None",
        learning_plan=", ".join(state.get("learning_plan", [])) if state.get("learning_plan") else "None",
        conversation_history=history_str.strip() or "None",
        query=state.get("user_query", "")
    )
    
    result = llm.invoke(prompt_text)
    response_text = result.content
    
    # Append user input and response to history
    history.append({"role": "user", "content": state.get("user_query", "")})
    history.append({"role": "assistant", "content": response_text})
    
    return {
        "conversation_history": history,
        "review": response_text
    }

def resume_updater_node(state: CareerCoachState) -> dict:
    llm = get_llm()
    skill = state.get("pending_skill_update", "")
    description = state.get("user_query", "")
    
    prompt_text = RESUME_UPDATER_PROMPT.format(
        skill=skill,
        description=description,
        resume=state.get("resume", "")
    )
    
    result = llm.invoke(prompt_text)
    updated_resume = result.content
    
    # Update learning_plan and known_skills lists to prevent infinite loops
    learning_plan = list(state.get("learning_plan", []))
    if skill in learning_plan:
        learning_plan.remove(skill)
        
    known_skills = list(state.get("known_skills", []))
    if skill not in known_skills:
        known_skills.append(skill)
        
    # Append only the raw user description to history (no internal instructions leaked)
    history = list(state.get("conversation_history", []))
    history.append({"role": "user", "content": description})
    history.append({
        "role": "assistant",
        "content": f"Successfully integrated '{skill}' into your resume with a STAR-method bullet point! Re-scoring profile..."
    })
    
    return {
        "resume": updated_resume,
        "pending_skill_update": None,
        "conversation_history": history,
        "learning_plan": learning_plan,
        "known_skills": known_skills
    }


def mock_interview_node(state: CareerCoachState) -> dict:
    llm = get_llm()
    user_query = state.get("user_query", "").strip()
    history = list(state.get("conversation_history", []))
    feedback = list(state.get("interview_feedback", []))
    
    # If the user is starting or resetting the interview
    if user_query.lower() in ("start", "reset", "mock_interview"):
        prompt_text = MOCK_INTERVIEW_START_PROMPT.format(
            known_skills=", ".join(state.get("known_skills", [])) if state.get("known_skills") else "None",
            career_goal=state.get("career_goal", "") or "General"
        )
        result = llm.invoke(prompt_text)
        questions = result.content
        
        history.append({"role": "assistant", "content": questions})
        return {
            "review": questions,
            "conversation_history": history
        }
    else:
        # Otherwise, evaluate user's answer
        prompt_text = MOCK_INTERVIEW_EVALUATE_PROMPT.format(answer=user_query)
        result = llm.invoke(prompt_text)
        critique = result.content
        
        feedback.append(critique)
        history.append({"role": "user", "content": user_query})
        history.append({"role": "assistant", "content": critique})
        
        return {
            "review": critique,
            "interview_feedback": feedback,
            "conversation_history": history
        }
