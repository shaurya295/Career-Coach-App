# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from graph import app
# pyrefly: ignore [missing-import]
from streamlit_agraph import agraph, Node, Edge, Config


# Set page configuration
st.set_page_config(
    page_title="Career Coach & Resume Reviewer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Insert Custom CSS for high-end aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="st-key"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.main-title {
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.5rem;
}

.subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 1.2rem;
    margin-bottom: 2.5rem;
    font-weight: 400;
}

.score-badge {
    border-radius: 50%;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    font-size: 2.5rem;
    font-weight: 800;
    color: white;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.score-excellent {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.score-good {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.score-poor {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

.section-card {
    background-color: #f9fafb;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
    border: 1px solid #f3f4f6;
    margin-bottom: 1.5rem;
}

.section-title {
    font-weight: 700;
    font-size: 1.2rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.skill-tag {
    display: inline-block;
    background-color: #eff6ff;
    color: #1e40af;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 4px;
    border: 1px solid #bfdbfe;
}

.gap-tag {
    display: inline-block;
    background-color: #fffbeb;
    color: #92400e;
    padding: 4px 10px;
    border-radius: 9999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 4px;
    border: 1px solid #fde68a;
}
</style>
""", unsafe_allow_html=True)

# 1. Bind LangGraph MemorySaver to st.session_state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "session_user_001"

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# Fetch latest state checkpoint from the graph checkpointer
state_snapshot = app.get_state(config)
db_state = state_snapshot.values if state_snapshot else {}

# Main UI layout
st.markdown("<h1 class='main-title'>Career Coach & Resume Reviewer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Get dynamic skill analysis, target roadmap alignment, chatbot advisors, and interactive resume updates</p>", unsafe_allow_html=True)

# Check if a resume exists in the checkpointer database
has_resume = db_state.get("resume") is not None

if not has_resume:
    st.markdown("### 📄 Welcome! Please Upload Your Resume to Start")
    resume_input = st.text_area("Paste your resume content below:", height=250, placeholder="John Doe\nSoftware Engineer...\n\nExperience:\n...")
    career_goal_input = st.text_input("Define your Career Goal (Optional):", placeholder="e.g. Senior Machine Learning Engineer, Lead Frontend Developer...")
    
    col_btn, _ = st.columns([1, 5])
    with col_btn:
        review_clicked = st.button("Evaluate Profile", use_container_width=True, type="primary")
        
    if review_clicked:
        if not resume_input.strip():
            st.warning("Please paste your resume content before proceeding.")
        else:
            with st.spinner("Analyzing candidate profile, extracting skills, mapping gaps, and scoring candidate..."):
                try:
                    # Invoke the graph pipeline
                    app.invoke({
                        "resume": resume_input,
                        "career_goal": career_goal_input.strip(),
                        "user_action": "submit_resume",
                        "conversation_history": [],
                        "known_skills": [],
                        "learning_plan": [],
                        "project_recommendations": [],
                        "ats_score": 0,
                        "review": "",
                        "pending_skill_update": None,
                        "user_query": "",
                        "interview_feedback": []
                    }, config)
                    st.success("Analysis complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                    st.info("Ensure Ollama is running (`ollama run llama3.2`) if USE_OLLAMA is true, or verify your OpenAI API keys inside .env.")
else:
    # 2. Render Tabs
    tab_dashboard, tab_chat, tab_interview = st.tabs([
        "📋 Dashboard & Roadmap", 
        "💬 Career Advisor Chat", 
        "🎙️ Mock Interview Mode"
    ])
    
    # Extract values from checkpoint database
    ats_score = db_state.get("ats_score", 0)
    known_skills = db_state.get("known_skills", [])
    learning_plan = db_state.get("learning_plan", [])
    project_recommendations = db_state.get("project_recommendations", [])
    review_report = db_state.get("review", "")
    pending_skill = db_state.get("pending_skill_update", None)
    
    # ------------------ TAB 1: DASHBOARD & ROADMAP ------------------
    with tab_dashboard:
        # Side-by-side columns: metrics on left, visual graph + checklist on right
        col_left, col_right = st.columns([2.3, 3.7])
        
        with col_left:
            # ATS Score Card
            badge_class = "score-excellent" if ats_score >= 80 else ("score-good" if ats_score >= 50 else "score-poor")
            st.markdown(f"""
            <div class='section-card' style='text-align: center; border-top: 4px solid #3b82f6;'>
                <h4 style='color: #4b5563; font-weight: 700; margin-bottom: 1.2rem;'>ATS Score</h4>
                <div class='score-badge {badge_class}'>
                    {ats_score}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Identified Known Skills Card
            st.markdown("""
            <div class='section-card' style='border-top: 4px solid #10b981;'>
                <div class='section-title' style='color: #047857;'>
                    🟢 Identified Known Skills
                </div>
            """, unsafe_allow_html=True)
            if known_skills:
                tags_html = "".join([f"<span class='skill-tag'>{s}</span>" for s in known_skills])
                st.markdown(tags_html, unsafe_allow_html=True)
            else:
                st.markdown("<p style='font-style: italic; color: #6b7280;'>No skills detected.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_right:
            with st.container(border=True):
                st.markdown("#### 🌳 Gamified Skill Tree")
                
                nodes_list = []
                edges_list = []
                
                # Root node is the Career Goal
                goal = db_state.get("career_goal", "") or "General Professional Development"
                nodes_list.append(Node(id="Root", label=goal, size=60, color="#06b6d4", shape="dot", font={"color": "white", "size": 20}))
                
                # Known skills: green completed nodes
                for skill in known_skills:
                    nodes_list.append(Node(id=skill, label=skill, size=45, color="#10b981", shape="dot", font={"color": "white", "size": 20}))
                    edges_list.append(Edge(source="Root", target=skill, color="#10b981", width=2))
                    
                # Learning plan: orange locked nodes
                for skill in learning_plan:
                    nodes_list.append(Node(id=skill, label=skill, size=45, color="#f59e0b", shape="dot", font={"color": "white", "size": 20}))
                    edges_list.append(Edge(source="Root", target=skill, color="#f59e0b", width=2, style="dashed"))
                    
                # Config options
                config_graph = Config(
                    width=900, 
                    height=800, 
                    directed=True, 
                    physics=False,
                    hierarchical=True,
                    **{
                        "layout": {
                            "hierarchical": {
                                "enabled": True,
                                "direction": "UD", 
                                "sortMethod": "directed",
                                "nodeSpacing": 200,
                                "levelSeparation": 400
                            }
                        }
                    }
                )
                
                # Render interactive graph
                agraph(nodes=nodes_list, edges=edges_list, config=config_graph)
                
                st.markdown("---")
                st.markdown("##### 🎯 Skill Checklist")
                
                # Skill Checklist loop
                if learning_plan:
                    st.write("Check off a skill once learned to collaboratively add it to your resume:")
                    for skill in learning_plan:
                        is_pending = (pending_skill == skill)
                        label = f"**{skill}** (Pending update...)" if is_pending else skill
                        
                        checked = st.checkbox(
                            label, 
                            key=f"check_{skill}", 
                            disabled=(pending_skill is not None),
                            value=is_pending
                        )
                        
                        if checked and not is_pending and pending_skill is None:
                            history = list(db_state.get("conversation_history", []))
                            history.append({
                                "role": "assistant",
                                "content": f"Great job learning {skill}! To add this to your resume, did you take a course or build a project? Briefly describe what you did."
                            })
                            
                            app.update_state(config, {
                                "pending_skill_update": skill,
                                "conversation_history": history
                            })
                            st.info(f"Checked off {skill}! Head over to the 'Career Advisor Chat' tab to describe your experience.")
                            st.rerun()
                else:
                    st.markdown("<p style='font-style: italic; color: #6b7280;'>No gaps identified.</p>", unsafe_allow_html=True)
            
        # Project Recommendations Section
        st.markdown("### 🚀 Recommended Portfolio Projects")
        if project_recommendations:
            cols_proj = st.columns(len(project_recommendations))
            for i, proj in enumerate(project_recommendations):
                with cols_proj[i]:
                    tech_tags = "".join([f"<span class='skill-tag'>{tech}</span>" for tech in proj.get("technologies", [])])
                    st.markdown(f"""
                    <div class='section-card' style='border-top: 4px solid #6366f1; height: 100%;'>
                        <h4 style='margin-bottom: 0.5rem; font-weight: 700; color: #4f46e5;'>{proj.get("title")}</h4>
                        <p style='font-size: 0.9rem; color: #4b5563; line-height: 1.5; height: 100px; overflow: auto;'>{proj.get("description")}</p>
                        <div style='margin-top: 0.8rem;'>
                            <strong>Technologies:</strong><br>
                            {tech_tags}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("💡 Complete more nodes on your skill tree to unlock tailored portfolio project recommendations!")

                    
        # Career Development Report & Resume View
        st.markdown("<br>", unsafe_allow_html=True)
        report_col, resume_col = st.columns([3, 2])
        
        with report_col:
            st.markdown("### 📋 Career Development Report")
            st.markdown(review_report)
            
        with resume_col:
            st.markdown("### 📄 Current Active Resume")
            st.code(db_state.get("resume", ""), language="text")
            
    # ------------------ TAB 2: ADVISOR CHATBOT ------------------
    with tab_chat:
        st.markdown("### 💬 Conversational Career Advisor")
        st.write("Ask questions about your learning plan, resume, or advice on transitioning to your target career goal.")
        
        # Display chat banner if there's a pending skill integration
        if pending_skill:
            st.warning(f"👉 **Pending Update**: Please describe how you learned **{pending_skill}** below (e.g., project built, course certificate, etc.) so we can format and append it to your resume using the STAR method.")
            
        # Display chat window messages
        chat_history = db_state.get("conversation_history", [])
        for msg in chat_history:
            role = msg.get("role")
            if role in ("user", "assistant"):
                with st.chat_message(role):
                    st.write(msg.get("content"))
                    
        # Chat input box
        user_msg = st.chat_input("Message your Career Coach...")
        if user_msg:
            # Display user message instantly
            with st.chat_message("user"):
                st.write(user_msg)
                
            # Process state update based on context
            with st.spinner("Thinking..."):
                if pending_skill:
                    # Route to resume_updater_node
                    app.invoke({
                        "user_action": "complete_skill",
                        "user_query": user_msg
                    }, config)
                else:
                    # Route to chat_node
                    app.invoke({
                        "user_action": "chat",
                        "user_query": user_msg
                    }, config)
                st.rerun()
                
    # ------------------ TAB 3: MOCK INTERVIEW MODE ------------------
    with tab_interview:
        st.markdown("### 🎙️ Technical Mock Interview Mode")
        st.write("Test your knowledge against technical questions custom-tailored to your resume skills.")
        
        col_start, _ = st.columns([2, 4])
        with col_start:
            start_interview = st.button("Start / Reset Interview questions", use_container_width=True)
            if start_interview:
                with st.spinner("Generating targeted questions..."):
                    app.invoke({
                        "user_action": "mock_interview",
                        "user_query": "start"
                    }, config)
                    st.rerun()
                    
        st.markdown("---")
        
        # Display latest interview question
        history = db_state.get("conversation_history", [])
        latest_question = None
        for msg in reversed(history):
            if msg.get("role") == "assistant" and ("question" in msg.get("content").lower() or "?" in msg.get("content")):
                latest_question = msg.get("content")
                break
                
        if latest_question:
            st.markdown("##### ❓ Current Question:")
            st.info(latest_question)
            
            # Form to submit answer
            st.markdown("##### 📝 Submit Your Response:")
            with st.form("answer_form", clear_on_submit=True):
                ans_text = st.text_area("Your response:", height=120)
                submit_ans = st.form_submit_button("Submit Answer", type="primary")
                
                if submit_ans and ans_text.strip():
                    with st.spinner("Evaluating response and generating critique..."):
                        app.invoke({
                            "user_action": "mock_interview",
                            "user_query": ans_text
                        }, config)
                        st.rerun()
        else:
            st.info("Click 'Start / Reset Interview questions' above to generate questions based on your resume.")
            
        # Display critique / critique feedback list
        feedbacks = db_state.get("interview_feedback", [])
        if feedbacks:
            st.markdown("#### 📝 Critique & Evaluation History")
            for i, critique in enumerate(reversed(feedbacks)):
                st.markdown(f"""
                <div class='section-card' style='border-left: 4px solid #ef4444;'>
                    <strong>Attempt {len(feedbacks) - i}: Critique & Review</strong><br><br>
                    {critique}
                </div>
                """, unsafe_allow_html=True)
