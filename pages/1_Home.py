import streamlit as st
from datetime import datetime
import random
import string

from core.session import init_session, update_streak
from components.cards import metric_card, feature_card, section_title
from core.user_profile import get_user_profile, sync_profile_from_session
from core.gamification import add_xp, init_gamification, reset_daily
from core.db import save_progress, update_leaderboard
from core.daily_missions import get_daily_mission
from core.ai_engine import generate_daily_coach
from core.block_access import ensure_user_row, enforce_block_access

st.set_page_config(
    page_title="Chumcred Teens | Home",
    page_icon="🧠",
    layout="wide"
)

# Hide default numbered sidebar nav, keep custom sidebar
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

init_session()
init_gamification()

if st.session_state.get("user"):
    ensure_user_row(st.session_state.user)
    enforce_block_access()

update_streak()
reset_daily()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

current_user = st.session_state.get("user", {}) or {}

try:
    profile = get_user_profile() or {}
except Exception:
    profile = {}

merged_user = dict(current_user)

for key in ["name", "age", "interest", "goal", "plan", "credits", "referral_code"]:
    if profile.get(key) not in [None, ""]:
        merged_user[key] = profile.get(key)

if not merged_user.get("name"):
    merged_user["name"] = (
        merged_user.get("full_name")
        or (merged_user.get("email", "").split("@")[0] if merged_user.get("email") else "Student")
    )

if merged_user.get("id") and "user_id" not in st.session_state:
    st.session_state.user_id = merged_user["id"]

st.session_state.user = merged_user

required_profile_fields = ["name", "age", "interest", "goal"]
if not all(st.session_state.user.get(k) not in [None, ""] for k in required_profile_fields):
    st.session_state.onboarded = False
    st.switch_page("pages/0_Onboarding.py")
    st.stop()

st.session_state.onboarded = True

if "coach_message" not in st.session_state:
    st.session_state.coach_message = ""

if "daily_mission" not in st.session_state:
    st.session_state.daily_mission = ""

if "daily_mission_done" not in st.session_state:
    st.session_state.daily_mission_done = False

if "selected_skill" not in st.session_state:
    st.session_state.selected_skill = ""

if "badges" not in st.session_state:
    st.session_state.badges = []

if "xp" not in st.session_state:
    st.session_state.xp = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "streak" not in st.session_state:
    st.session_state.streak = 0

# MVP Sidebar
with st.sidebar:
    st.markdown("## Chumcred Teens")
    st.caption(st.session_state.user.get("name", "Student"))

    st.page_link("pages/1_Home.py", label="🏠 Home")
    st.page_link("pages/2_Skill_Discovery.py", label="🎯 Skill Discovery")
    st.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")
    st.page_link("pages/4_Projects.py", label="🛠 Projects")
    st.page_link("pages/5_Learn_Anything.py", label="🌍 Learn Anything")
    # st.page_link("pages/7_Community.py", label="🌍 Community")
    st.page_link("pages/8_AI_Coach.py", label="🧠 AI Coach")
    st.page_link("pages/9_Daily_Missions.py", label="🎯 Daily Missions")

    # Hidden for MVP:
    # - pages/5_Progress.py
    # - pages/6_Leaderboard.py
    # - pages/10_Reward_Store.py

    if (st.session_state.user.get("email") or "").strip().lower() == "chumcred@gmail.com":
        st.page_link("pages/9_Subscription.py", label="💳 Subscription")
        st.page_link("pages/10_Admin_Payments.py", label="⚙️ Admin Payments")
        st.page_link("pages/10_Block_Unblock_Users.py", label="🚫 Block / Unblock Users")

    st.markdown("---")

    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.onboarded = False
        st.session_state.just_logged_in = False
        st.switch_page("app.py")

if not st.session_state.user.get("referral_code"):
    name = st.session_state.user.get("name", "user")
    base = name[:3].upper() if name else "USR"
    rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
    referral_code = f"{base}-{rand}"

    st.session_state.user["referral_code"] = referral_code
    st.session_state.ref_code = referral_code

    try:
        sync_profile_from_session()
    except Exception:
        pass
else:
    st.session_state.ref_code = st.session_state.user.get("referral_code")

if "user_id" in st.session_state:
    try:
        save_progress(
            st.session_state.user_id,
            st.session_state.xp,
            st.session_state.level,
            st.session_state.streak
        )

        update_leaderboard(
            st.session_state.user_id,
            st.session_state.user.get("name", "Anonymous"),
            st.session_state.xp
        )
    except Exception:
        pass

if "last_usage_date" not in st.session_state:
    st.session_state.last_usage_date = str(datetime.today().date())

today = str(datetime.today().date())

if st.session_state.last_usage_date != today:
    st.session_state.daily_ai_usage = 0
    st.session_state.last_usage_date = today
    st.session_state.daily_mission_done = False

st.markdown("""
<div class="hero-box">
    <div class="hero-title">🚀 Chumcred Teens</div>
    <div class="hero-subtitle">
        Discover your strengths, learn practical digital skills, complete real projects,
        and prepare for opportunities in school, work, and business.
    </div>
</div>
""", unsafe_allow_html=True)

st.caption(
    f"Welcome back, {st.session_state.user.get('name', 'Student')} • "
    f"Interest: {st.session_state.user.get('interest', 'Not set')} • "
    f"Goal: {st.session_state.user.get('goal', 'Not set')}"
)

if not st.session_state.coach_message:
    st.session_state.coach_message = generate_daily_coach(
        st.session_state.user.get("name", ""),
        st.session_state.user.get("interest", ""),
        st.session_state.user.get("goal", "")
    )

st.info(f"🧠 Coach says:\n\n{st.session_state.coach_message}")

if not st.session_state.daily_mission:
    st.session_state.daily_mission = get_daily_mission()

st.markdown("### 🎯 Daily Mission")
st.write(st.session_state.daily_mission)

if not st.session_state.daily_mission_done:
    if st.button("✅ Mark as Done", key="mark_daily_mission_done"):
        st.session_state.daily_mission_done = True
        add_xp(20)
        st.success("🔥 +20 XP earned!")
        st.rerun()
else:
    st.success("Mission completed 🎉")

st.markdown("## 🔥 Your Growth Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Level", st.session_state.level)
col2.metric("XP", st.session_state.xp)
col3.metric("Streak 🔥", st.session_state.streak)

st.progress(min(st.session_state.xp / max(st.session_state.level * 100, 1), 1.0))

col1, col2, col3 = st.columns(3)

with col1:
    metric_card("Current Level", str(st.session_state.level), "Keep growing")

with col2:
    metric_card("XP Earned", str(st.session_state.xp), "Your effort matters")

with col3:
    metric_card(
        "Skill Path",
        st.session_state.selected_skill if st.session_state.selected_skill else "Not selected",
        "Choose your direction",
    )

section_title("Your Journey", "A simple path from confusion to confidence.")

c1, c2, c3, c4 = st.columns(4)

with c1:
    feature_card("Discover Your Skill", "Find the right path.", "🎯")
with c2:
    feature_card("Learn with AI", "Ask questions.", "🤖")
with c3:
    feature_card("Build Projects", "Create things.", "💼")
with c4:
    feature_card("Track Progress", "Earn points.", "📈")

st.markdown("### ⚡ Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎯 Skill Discovery", use_container_width=True):
        add_xp(5)
        st.switch_page("pages/2_Skill_Discovery.py")

    if st.button("🤖 Ask AI", use_container_width=True):
        add_xp(10)
        st.switch_page("pages/3_AI_Assistant.py")

    if st.button("🛠 Work on Project", use_container_width=True):
        add_xp(15)
        st.switch_page("pages/4_Projects.py")

with col2:
    if st.button("🌍 Learn Anything", use_container_width=True):
        add_xp(5)
        st.switch_page("pages/5_Learn_Anything.py")

    # if st.button("📈 Progress", use_container_width=True):
        # st.switch_page("pages/5_Progress.py")

    # if st.button("🏆 Leaderboard", use_container_width=True):
        # st.switch_page("pages/6_Leaderboard.py")

# with col3:
    # if st.button("🌍 Community", use_container_width=True):
        # add_xp(5)
        # st.switch_page("pages/7_Community.py")

    if st.button("🧠 AI Coach", use_container_width=True):
        st.switch_page("pages/8_AI_Coach.py")

    if st.button("🎯 Daily Missions", use_container_width=True):
        st.switch_page("pages/9_Daily_Missions.py")

st.markdown("### 🏅 Badges")

if st.session_state.badges:
    st.write(" ".join(st.session_state.badges))
else:
    st.write("No badges yet — start learning!")

st.markdown("### 🔥 Why Chumcred Teens?")
st.write("""
Chumcred Teens helps teenagers discover real strengths, learn practical skills,
and become confident and future-ready.
""")

st.info("Use the quick action buttons above or the sidebar to explore the platform.")

st.markdown("### 🎁 Invite Friends")
st.info("Invite friends and earn bonus XP soon 🚀")

ref_code = st.session_state.user.get("referral_code", "N/A")
st.code(ref_code, language="text")

st.button("📋 Copy Invite Code", key="copy_ref")
