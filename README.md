
# 🚀 Career Coach and Resume Reviewer App

### 👥 Creators
* **Souryaneel Pal**
* **Shaurya Kakkar**



## ⚡ Quick Start: How to Run the App

*Supposing you have already downloaded the project files to your machine, follow these direct steps to launch the application:*

### 1. Open Terminal & Navigate to the Project
Open your terminal app and change your directory to the folder containing the project files:
```bash
cd /path/to/your/downloaded/career-coach

```

### 2. Activate Your Environment & Install Dependencies

Ensure you have the required libraries installed:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Start your Local LLM Server

Since the backend runs completely locally, ensure **Ollama** is active and running the model in the background:

```bash
ollama run llama3.2

```

### 4. Launch the Dashboard

Run the Streamlit server to open the application in your browser:

```bash
streamlit run app.py

```

*Your browser will automatically open `http://localhost:8501/` with the active application!*

---

## 📋 Project Description & Purpose

The **Career Coach and Resume Reviewer App** is an enterprise-grade, agentic AI career development ecosystem designed to move beyond traditional, static resume keyword matching. The primary purpose of the application is to act as a live, interactive career advisor that tracks a professional's growth, simulates recruitment hurdles, and dynamically optimizes their resume layout as they master new skills.

Rather than treating resume reviews as a one-time evaluation, this platform provides a continuous, gamified feedback loop that visualizes career progression, bridges technical skill gaps, and prepares candidates for competitive designation transitions.

---

## 🧠 Technical Architecture & Core Concepts

This application utilizes modern AI agent patterns and reactive user interface configurations to achieve automated, high-fidelity profile generation:

* **🤖 Stateful Agentic Workflows (LangGraph):** The core intelligence engine is built using a LangGraph `StateGraph`. Instead of executing rigid, linear prompts, the graph implements conditional routing based on user intent. It shifts state seamlessly between automated profile extraction, free-form career counseling chat loops, interactive resume rewrites, and mock technical evaluation streams.


* **🌳 Gamified Skill Tree Visualization (`streamlit-agraph`):** To make skill gaps actionable, the app uses an interactive network graph powered by the `vis.js` engine via `streamlit-agraph`. It structurally maps the target role as a root node and positions master skills (colored green) alongside pending competencies (colored orange), providing an organic, visual hierarchy of user progression.
* **🔄 Closed-Loop Resume Co-Authoring:** Features an automated, non-hallucinatory update flow. When a user checks off a target skill, a transactional chat node interviews them about their practical application. A specialized **STAR-method (Situation, Task, Action, Result)** resume updater node compiles the description, refactors the source markdown text, appends it, and pushes the state back through the ATS calculator.


* **🎙️ Tailored Mock Interview Engine:** Dynamically generates technical interview questions generated contextually from the user's `known_skills` list and unique career goals. A multi-step feedback graph analyzes the candidate's answers textually to provide persistent, graded critique histories.


* **🎯 Deterministic Schema Enforcement:** Utilizes `Pydantic` v2 structured data models combined with LangChain's `.with_structured_output()` utility. This prevents formatting hallucinations and guarantees strict JSON payload generation for ATS scoring matrices and bespoke portfolio project recommendations.



---

## 📄 License

Distributed under the MIT License.

