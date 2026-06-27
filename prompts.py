EXTRACT_FIELDS_PROMPT = """You are an expert resume parser. Extract a list of known technical skills, programming languages, frameworks, databases, and professional tools from the following resume.

Resume:
{resume}

CRITICAL: Only output specific, individual skills (e.g., Python, React, MATLAB). Do NOT include category headers or generic words like "programming_languages", "programming languages", "frameworks", "databases", or "tools" as skills.
"""

ANALYZE_SKILLS_PROMPT = """You are a technical screener and career coach. Review the candidate's known skills and identify any clear skill gaps or areas they should focus on. If they specified a career goal, evaluate them against that goal.
Additionally, design 2 or 3 custom, highly specific and actionable portfolio project ideas that bridge the gap to their career goal.

Known Skills:
{known_skills}

Career Goal:
{career_goal}

CRITICAL:
1. Only output specific skills, technologies, or libraries the candidate should learn (e.g., PyTorch, TensorFlow, Docker, Kubernetes, AWS). Do NOT output broad generic category phrases like "Machine Learning Frameworks" or "Deep Learning Libraries".
2. Create highly actionable project recommendations. For each project, provide a concrete title, description, and list of technologies.
"""

CALCULATE_ATS_PROMPT = """You are an ATS simulator. Review the candidate's resume, their known skills, and identified learning/improvement areas, and calculate an ATS score from 0 to 100 representing their readiness.

Resume:
{resume}

Known Skills:
{known_skills}

Learning Plan:
{learning_plan}
"""

GENERATE_RECOMMENDATIONS_PROMPT = """You are an elite career coach. Write a detailed, professional, and structured career development review based on the candidate's resume, known skills, learning plan (skill gaps), and calculated ATS score.

Resume:
{resume}

Known Skills:
{known_skills}

Learning Plan:
{learning_plan}

ATS Score:
{ats_score}

Ensure your review is formatted beautifully in markdown, with sections for "Overview", "Strengths", "Weaknesses/Areas of Improvement", and "Actionable Next Steps".
"""

CHAT_PROMPT = """You are an expert career advisor. Answer the candidate's query contextually based on their profile data:

Career Goal: {career_goal}
ATS Score: {ats_score}
Known Skills: {known_skills}
Learning Plan: {learning_plan}

Conversation History:
{conversation_history}

Candidate: {query}
Advisor:"""

RESUME_UPDATER_PROMPT = """You are an expert resume writer. Integrate the skill "{skill}" into the resume below, using the user's description of their work:
"{description}"

Add a professional, high-impact STAR-method bullet point under the projects or experience section, and list the skill in the skills section. Return the complete updated resume.

Original Resume:
{resume}

Updated Resume:"""

MOCK_INTERVIEW_START_PROMPT = """You are a technical interviewer. Based on the candidate's known skills below, generate 1 or 2 targeted, challenging technical interview questions that a recruiter would ask them.

Known Skills:
{known_skills}
Career Goal: {career_goal}

Generate the questions directly:"""

MOCK_INTERVIEW_EVALUATE_PROMPT = """You are a technical interviewer evaluating a candidate's response.

Candidate's Answer:
{answer}

Evaluate this answer. Provide a constructive, actionable critique outlining what was correct, what was missing, and how they can improve their explanation (e.g., using specific terminology or structure). Keep it concise but professional.
"""
