import sys
import os
import json
import time
import streamlit as st
import google.generativeai as genai

# Force UTF-8 environment settings for Windows
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONLEGACYWINDOWSSTDIO"] = "utf-8"

# Page Configuration
st.set_page_config(
    page_title="AI Cohort Technical Interviewer",
    page_icon="💻",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }
    div[data-testid="stSidebar"] {
        background-color: #161b22;
    }
    </style>
""", unsafe_allow_html=True)

# Strict ASCII Sanitizers
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

# Load Curriculum & Candidate JSON Files Safely
@st.cache_data
def load_data():
    try:
        with open("curriculum.json", "r", encoding="utf-8") as f:
            curriculum = sanitize_obj(json.load(f))
        with open("candidates.json", "r", encoding="utf-8") as f:
            candidates = sanitize_obj(json.load(f))
        return curriculum, candidates
    except Exception as e:
        st.error(f"Error loading JSON data files: {e}")
        return {}, {}

curriculum_data, candidates_data = load_data()

# Safe API Response Generator with Retry Logic for Rate Limits
def generate_response(prompt, api_key, model_name="gemini-3.6-flash", max_retries=4):
    if not api_key:
        return "Please enter a valid Gemini API Key in the sidebar."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # Retry loop to handle 429 Rate Limit errors smoothly
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "ResourceExhausted" in err_msg:
                sleep_time = (2 ** attempt) + 3  # Exponential delay: 5s, 7s, 11s, 19s
                time.sleep(sleep_time)
            else:
                return f"API Error: {err_msg}"
                
    return "Rate limit reached. Please wait 15–20 seconds before submitting another prompt."

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_key = st.text_input("Enter Gemini API Key", type="password")
    
    if st.button("Reset Interview Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    
    # Candidate Selection
    cand_names = list(candidates_data.keys()) if isinstance(candidates_data, dict) else []
    selected_cand = st.selectbox("Select Candidate", cand_names if cand_names else ["Default Candidate"])
    
    # Role Selection
    curr_roles = list(curriculum_data.keys()) if isinstance(curriculum_data, dict) else []
    selected_role = st.selectbox("Select Role / Topic", curr_roles if curr_roles else ["General Software Engineer"])

# Main Chat Interface
st.title("💻 AI Cohort Technical Interviewer")
st.caption(f"Active Candidate: **{selected_cand}** | Role: **{selected_role}**")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello {selected_cand}! Ready to begin your technical interview for the {selected_role} position?"}
    ]

# Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle User Input
if user_input := st.chat_input("Type your response here..."):
    # Render User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Build Prompt Context
    system_context = (
        f"You are an expert technical interviewer evaluating candidate '{selected_cand}' "
        f"for the role of '{selected_role}'. Ask relevant technical follow-up questions, "
        f"assess code quality, and provide constructive feedback. Keep responses clear and structured."
    )
    
    # Combine system context with recent messages
    full_prompt = f"{system_context}\n\nCandidate Answer: {user_input}"

    # Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Evaluating response..."):
            ai_reply = generate_response(full_prompt, api_key)
            st.write(ai_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
