import streamlit as st
from core.gamification import add_xp
from core.session import init_session
from core.ai_engine import teen_ai, get_ai_response
from core.user_profile import add_project, set_active_project, sync_profile_from_session
from core.credits import can_use, deduct, show_upgrade
from workflow.sidebar_menu import render_sidebar

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🚀 Build Your Project")

project = st.text_input(
    "What project do you want to build?",
    placeholder="e.g. Build a website, start a YouTube channel, create a fashion brand..."
)

if st.button("Start Project"):
    if project:
        add_project(project)
        set_active_project(project)
        sync_profile_from_session()
        st.success(f"Awesome! Let's build: {project}")
    else:
        st.warning("Please enter a project")

# -------------------------
# AI PROJECT GUIDE
# -------------------------
if project:
    st.markdown("### 📌 Your Project Plan")

    plan = teen_ai(
        prompt=f"I want to build this project: {project}. Break it into simple steps for a teenager.",
        mode="learn"
    )

    st.write(plan)

    if st.button("Mark Project Step Complete"):
        add_xp(10, "Project work")
        st.success("🎉 You earned 10 points!")

if st.button("Generate Project Help"):
    if not project:
        st.warning("Please enter a project first.")
    else:
        allowed, msg = can_use("project")

        if not allowed:
            st.error(msg)
            show_upgrade()
        else:
            result = get_ai_response(f"Help me build this project: {project}")
            deduct("project")
            st.success(result)
