import streamlit as st
from core.session import init_session
from core.gamification import add_xp
from workflow.sidebar_menu import render_sidebar

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🎯 Daily Missions")

missions = [
    {"task": "Ask AI a question", "xp": 10},
    {"task": "Translate a word", "xp": 5},
    {"task": "Complete a project step", "xp": 15},
]

if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = []

for i, m in enumerate(missions):
    done = i in st.session_state.completed_missions

    if done:
        st.success(f"✅ {m['task']} (+{m['xp']} XP)")
    else:
        if st.button(f"Do: {m['task']}", key=f"mission_{i}"):
            add_xp(m["xp"])
            st.session_state.completed_missions.append(i)
            st.rerun()
