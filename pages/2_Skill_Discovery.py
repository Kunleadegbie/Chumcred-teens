import streamlit as st
from core.skill_engine import recommend_skill
from core.session import init_session
from core.ai_engine import teen_ai
from core.user_profile import add_skill, set_selected_skill, sync_profile_from_session
from workflow.sidebar_menu import render_sidebar

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🔍 Discover Your Skill")

skill = st.text_input(
    "What do you want to learn?",
    placeholder="e.g. Graphic design, football, coding, YouTube, fashion..."
)

if st.button("Explore Skill"):
    if skill:
        add_skill(skill)
        set_selected_skill(skill)
        sync_profile_from_session()
        st.success(f"Great choice! Let's explore {skill} 🚀")

        response = teen_ai(
            prompt=f"I want to learn {skill}. Guide me step by step like a beginner teenager.",
            mode="learn"
        )
        st.write(response)
    else:
        st.warning("Please enter a skill")

interest = st.text_input(
    "Optional: Tell us your interest (we can suggest a path)",
    placeholder="e.g. I like tech, business, art..."
)

if st.button("Find My Skill Path", use_container_width=True):
    if not interest:
        st.warning("Please enter your interest first.")
    else:
        result = recommend_skill({"interest": interest})
        st.session_state.selected_skill = result
        st.success(f"Recommended Skill Path: {result}")
