import streamlit as st
from core.session import init_session
from core.user_profile import get_user_profile, sync_profile_from_session

st.set_page_config(
    page_title="Chumcred Teens | Onboarding",
    page_icon="🧠",
    layout="wide"
)

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

current_user = st.session_state.get("user", {}) or {}

try:
    saved_profile = get_user_profile() or {}
except Exception:
    saved_profile = {}

default_name = (
    saved_profile.get("name")
    or current_user.get("name")
    or current_user.get("full_name")
    or ""
)

default_age = saved_profile.get("age") or current_user.get("age") or 15
try:
    default_age = int(default_age)
except Exception:
    default_age = 15
default_age = max(13, min(19, default_age))

default_interest = (
    saved_profile.get("interest")
    or current_user.get("interest")
    or ""
)

saved_goal = (
    saved_profile.get("goal")
    or current_user.get("goal")
    or ""
)

goal_options = [
    "Learn a skill",
    "Earn money",
    "Get a job",
    "Start a business",
    "Others"
]

if saved_goal in goal_options[:-1]:
    default_goal_index = goal_options.index(saved_goal)
    default_custom_goal = ""
else:
    default_goal_index = goal_options.index("Others") if saved_goal else 0
    default_custom_goal = saved_goal

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
[data-testid="stSidebarNav"] {display: none;}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero-box {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
    padding: 2rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
}
.form-card {
    background: white;
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <h1 style="margin-bottom:0.5rem;">🎯 Welcome to Chumcred Teens</h1>
    <p style="font-size:1.05rem; margin-bottom:0;">
        Let’s personalize your journey so the platform can guide you better.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-card">', unsafe_allow_html=True)

name = st.text_input("Your Name", value=default_name)
age = st.slider("Your Age", 13, 19, value=default_age)
interest = st.text_input(
    "What interests you most? (e.g. Tech, Sports, Music, Business)",
    value=default_interest
)

goal_option = st.selectbox(
    "What do you want to achieve?",
    goal_options,
    index=default_goal_index
)

custom_goal = ""
if goal_option == "Others":
    custom_goal = st.text_input("Specify your goal", value=default_custom_goal)

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Start My Journey 🚀", use_container_width=True):
    if not name.strip():
        st.warning("Please enter your name.")
        st.stop()

    if not interest.strip():
        st.warning("Please tell us your interest.")
        st.stop()

    final_goal = custom_goal.strip() if goal_option == "Others" else goal_option

    if not final_goal:
        st.warning("Please choose or enter your goal.")
        st.stop()

    updated_user = dict(current_user)
    updated_user.update({
        "name": name.strip(),
        "full_name": current_user.get("full_name") or name.strip(),
        "age": age,
        "interest": interest.strip(),
        "goal": final_goal,
        "plan": updated_user.get("plan", "freemium"),
        "credits": updated_user.get("credits", 0),
    })

    st.session_state.user = updated_user
    st.session_state.onboarded = True

    if updated_user.get("id"):
        st.session_state.user_id = updated_user["id"]

    sync_profile_from_session()

    st.success(f"Welcome {name.strip()}! 🚀")
    st.switch_page("pages/1_Home.py")
