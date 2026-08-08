# AI Usage & Prompt Log

## 1. AI Tools Used
- **LLM API:** Google Gemini 2.5 Flash (`google-genai`)
- **Coding Assistants:** ChatGPT / GitHub Copilot
- **UI Framework:** Streamlit

---

## 2. Development Prompts (Vibe-Coding Log)

### Prompt 1: Project Architecture
> **User Prompt:** "Build a multi-turn AI interview agent using Streamlit in Python that reads curriculum and candidate details from JSON files and generates sequential technical questions."
> **Outcome:** Created the core application loop, session state handling, and layout in `app.py`.

### Prompt 2: Context & Data Handling
> **User Prompt:** "Write a Python function to safely load curriculum.json and candidates.json into Streamlit with caching."
> **Outcome:** Built the `@st.cache_data` helper function to parse synthetic cohort data.

---

## 3. System Prompts Implemented in Code

### System Prompt 1: Technical Interviewer Persona
```text
You are an expert AI Technical Interviewer for an AI Cohort.
Candidate Profile: {selected_cand}
Curriculum Context: {curriculum}

Instructions:
1. Conduct a multi-turn conversational technical interview.
2. Ask intelligent follow-up questions based on candidate responses across curriculum modules.
3. Keep questions concise and focused, asking 1 question at a time.
