import streamlit as st
from core.ai_engine import get_ai_coach_response
from core.session import init_session
from workflow.sidebar_menu import render_sidebar

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🧠 AI Coach")
st.write("Your personal mentor for growth, learning, and success 🚀")

user = st.session_state.get("user", {}) or {}

name = (
    user.get("name")
    or user.get("full_name")
    or st.session_state.get("name", "Student")
)
age = user.get("age", st.session_state.get("age", "Teen"))
interest = user.get("interest", st.session_state.get("interest", "Not set"))
goal = user.get("goal", st.session_state.get("goal", "Not set"))

st.markdown("### 👤 Your Profile")
st.write(f"**Name:** {name}")
st.write(f"**Interest:** {interest}")
st.write(f"**Goal:** {goal}")

st.divider()

st.markdown("### ⚡ Quick Coaching Prompts")

col1, col2 = st.columns(2)

if col1.button("📍 What should I learn next?"):
    st.session_state.coach_prompt = "What should I learn next?"

if col2.button("💰 How can I start earning?"):
    st.session_state.coach_prompt = "How can I start earning?"

if col1.button("🚀 Give me a roadmap"):
    st.session_state.coach_prompt = "Give me a roadmap based on my interest"

if col2.button("🔥 Motivate me"):
    st.session_state.coach_prompt = "Motivate me to stay consistent"

user_input = st.text_input(
    "Ask your AI Coach anything...",
    value=st.session_state.get("coach_prompt", "")
)

if st.button("Get Coaching Advice"):
    if user_input:
        with st.spinner("Thinking like a mentor..."):
            response = get_ai_coach_response(
                name, age, interest, goal, user_input
            )

        st.success("Here's your guidance:")
        st.write(response)
    else:
        st.warning("Please enter a question first.")
