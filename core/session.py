# core/session.py

import streamlit as st
from datetime import datetime


# ---------------------------
# 🚀 INITIALIZE SESSION
# ---------------------------
def init_session():

    # ---------------------------
    # USER PROFILE (STRUCTURED)
    # ---------------------------
    if "user" not in st.session_state:
        st.session_state.user = {
            "name": "",
            "age": "",
            "interest": "",
            "goal": "",
            "plan": "freemium",
            "credits": 0,
            "is_premium": False,
            "trial_start": str(datetime.today().date()),
        }

    # ---------------------------
    # CORE DEFAULTS (FIXED BUG HERE)
    # ---------------------------
    defaults = {
        "xp": 0,
        "level": 1,
        "streak": 0,
        "coins": 0,
        "daily_ai_usage": 0,
        "last_usage_date": str(datetime.today().date()),
        "points": 0,

        # Activity
        "projects": [],
        "skills": [],
        "selected_skill": None,

        # Addictive system
        "last_active": str(datetime.today().date()),
        "daily_mission_done": False,
        "daily_mission": "",
        "coach_message": "",
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ---------------------------
    # DAILY USAGE RESET
    # ---------------------------
    today = str(datetime.today().date())

    if st.session_state.last_usage_date != today:
        st.session_state.daily_ai_usage = 0
        st.session_state.last_usage_date = today


# ---------------------------
# 🔥 STREAK SYSTEM
# ---------------------------
def update_streak():
    today = str(datetime.today().date())

    if st.session_state.last_active != today:
        st.session_state.streak += 1
        st.session_state.last_active = today
        st.session_state.daily_mission_done = False


# ---------------------------
# 🎯 XP SYSTEM
# ---------------------------
def add_xp(points):
    st.session_state.xp += points

    # Level progression
    if st.session_state.xp >= st.session_state.level * 100:
        st.session_state.level += 1


# ---------------------------
# ⏳ TRIAL EXPIRY
# ---------------------------
def check_trial_expiry():
    start = datetime.fromisoformat(st.session_state.user["trial_start"])
    today = datetime.today()

    if (today - start).days > 7:
        st.session_state.user["plan"] = "expired"