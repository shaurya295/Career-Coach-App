import re
from state import CareerCoachState

def load_memory(state: CareerCoachState) -> dict:
    ats_score = state.get("ats_score", 0)
    career_goal = state.get("career_goal", "")
    conversation_history = state.get("conversation_history", [])
    
    # Format conversation history
    history_str = ""
    for msg in conversation_history:
        role = msg.get("role", "User")
        content = msg.get("content", "")
        history_str += f"{role.capitalize()}: {content}\n"
    
    # Create the context block
    context = (
        f"--- HISTORIC CONTEXT ---\n"
        f"ATS Score: {ats_score}\n"
        f"Career Goal: {career_goal}\n"
        f"Conversation History:\n{history_str.strip() or 'None'}\n"
        f"------------------------"
    )
    
    return {"review": context}

def update_memory(state: CareerCoachState) -> dict:
    latest_response = state.get("review", "")
    
    # 1. Parse the LLM's response to identify new skills
    new_skills = []
    # Scans the text for common programming/tech terms as skills
    common_skills = ["python", "javascript", "react", "typescript", "node", "aws", "docker", "kubernetes", "sql", "nosql", "git", "langchain", "langgraph", "llama", "openai", "rust", "go", "java", "c++", "pydantic", "streamlit"]
    for word in re.findall(r'\b[a-zA-Z0-9+#\.-]+\b', latest_response.lower()):
        if word in common_skills:
            cap_word = word.title() if word != "aws" else "AWS"
            if cap_word not in new_skills:
                new_skills.append(cap_word)
    
    # Merge with existing known_skills
    known_skills = list(state.get("known_skills", []))
    for skill in new_skills:
        if skill not in known_skills:
            known_skills.append(skill)
            
    # 2. Record the latest ATS score
    ats_score = state.get("ats_score", 0)
    score_match = re.search(r'(?:ats\s*score|score)\s*:\s*(\d+)', latest_response.lower())
    if score_match:
        ats_score = int(score_match.group(1))
        
    # 3. Append the exchange to conversation_history
    history = list(state.get("conversation_history", []))
    user_content = state.get("resume", "")
    if user_content and (not history or history[-1].get("content") != user_content):
        history.append({"role": "user", "content": user_content})
        
    if latest_response:
        history.append({"role": "assistant", "content": latest_response})
        
    return {
        "known_skills": known_skills,
        "ats_score": ats_score,
        "conversation_history": history
    }
