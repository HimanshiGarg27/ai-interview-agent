import sys
import os
import json
import time
import streamlit as st
from google import genai

# Force UTF-8 environment settings for Windows
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

st.set_page_config(page_title="AI Cohort Technical Interviewer")
st.title("AI Cohort Technical Interviewer")

# Strict ASCII sanitizer
def sanitize(text):
    if isinstance(text, str):
        return text.encode("ascii", "ignore").decode("ascii")
    return text

def sanitize_obj(obj):
    if isinstance(obj, str):
        return sanitize(obj)
    elif isinstance(obj, list):
        return [sanitize_obj(i) for i in obj]
    elif isinstance(obj, dict):
        return {sanitize(k): sanitize_obj(v) for k, v in obj.items()}
    return obj

# Load curriculum and candidate JSON files safely
def load_data():
    curr_data = {}
    cand_data = []
    
    if os.path.exists("curriculum.json"):
        try:
            with open("curriculum.json", "r", encoding="utf-8") as f:
                curr_data = json.load(f)
        except Exception:
            curr_data = {}

    if os.path.exists("candidates.json"):
        try:
            with open("candidates.json", "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, dict):
                    cand_data = raw.get("candidates") or raw.get("profiles") or list(raw.values())
                elif isinstance(raw, list):
                    cand_data = raw
        except Exception:
            cand_data = []

    if not cand_data or not isinstance(cand_data, list):
        cand_data = [{"name": "Default Candidate", "completed_missions": []}]

    return sanitize_obj(curr_data), sanitize_obj(cand_data)

curriculum, candidates = load_data()

# Safe API caller with built-in retry and model fallback
def generate_response(client, prompt_text):
    models = ["gemini-2.0-flash", "gemini-1.5-flash"]
    for model_name in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_text
                )
                return response.text
            except Exception as e:
                err_msg = str(e)
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                    time.sleep(4)  # Pause briefly for free tier quota window to reset
                else:
                    break
    raise Exception("Free tier rate limit hit. Please wait 15 seconds and try again.")

# Sidebar Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if st.sidebar.button("Reset Interview Session"):
    st.session_state.clear()
    st.rerun()

cand_names = [c.get("name", f"Candidate {i+1}") for i, c in enumerate(candidates)]
selected_idx = st.sidebar.selectbox("Select Candidate", range(len(cand_names)), format_func=lambda x: cand_names[x])
selected_cand = candidates[selected_idx]

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Main Logic
if api_key:
    client = genai.Client(api_key=sanitize(api_key))

    # Initial Question
    if len(st.session_state.messages) == 0:
        prompt = f"""You are an expert AI Technical Interviewer for an AI Cohort.
Candidate Profile: {json.dumps(selected_cand, ensure_ascii=True)}
Curriculum Context: {json.dumps(curriculum, ensure_ascii=True)}

Instructions:
1. Introduce yourself briefly and ask Question 1 based on candidate completed topics.
2. Do not use any emojis in your response.
"""
        try:
            reply = generate_response(client, sanitize(prompt))
            st.session_state.messages.append({"role": "assistant", "content": sanitize(reply)})
            st.session_state.question_count = 1
            st.rerun()
        except Exception as e:
            st.warning(f"Rate Limit Pause: {e}")

    # Subsequent Questions (Up to 8)
    if st.session_state.question_count < 8:
        user_input = st.chat_input("Type your answer here...")
        if user_input:
            clean_input = sanitize(user_input)
            st.session_state.messages.append({"role": "user", "content": clean_input})

            prompt = f"""You are an AI Technical Interviewer.
Current Question: {st.session_state.question_count}/8.
Curriculum Context: {json.dumps(curriculum, ensure_ascii=True)}
Candidate Profile: {json.dumps(selected_cand, ensure_ascii=True)}

Instructions:
1. Evaluate previous response briefly.
2. Ask Question {st.session_state.question_count + 1}. Do not use emojis.
Transcript: {json.dumps(sanitize_obj(st.session_state.messages), ensure_ascii=True)}
"""
            try:
                reply = generate_response(client, sanitize(prompt))
                st.session_state.messages.append({"role": "assistant", "content": sanitize(reply)})
                st.session_state.question_count += 1
                st.rerun()
            except Exception as e:
                st.warning(f"Rate Limit Pause: {e}")
    else:
        st.success("Technical Interview Completed!")
        if st.button("Generate Structured Feedback Report"):
            prompt = f"Analyze interview transcript and output structured feedback (Strengths, Weaknesses, Concepts Covered, Score /10):\n\n{json.dumps(sanitize_obj(st.session_state.messages), ensure_ascii=True)}"
            try:
                feedback = generate_response(client, sanitize(prompt))
                st.markdown(sanitize(feedback))
            except Exception as e:
                st.warning(f"Rate Limit Pause: {e}")
else:
    st.info("Enter your Gemini API Key in the sidebar to start the AI Interview.")