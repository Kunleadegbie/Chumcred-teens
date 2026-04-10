# core/gamification.py

import streamlit as st
from datetime import datetime

# ---------------------------
# INIT GAMIFICATION STATE
# ---------------------------
def init_gamification():
    defaults = {
        "xp": 0,
        "level": 1,
        "streak": 0,
        "last_active": None,
        "badges": [],
        "coins": 0,
        "reward_claimed": False,
        "reward_date": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------
# ADD XP
# ---------------------------
def add_xp(amount, reason=""):
    st.session_state.xp += amount

    # Level up check
    new_level = calculate_level(st.session_state.xp)

    if new_level > st.session_state.level:
        st.session_state.level = new_level
        st.session_state.coins += 20  # reward coins
        st.success(f"🎉 Level Up! You are now Level {new_level} (+20 coins)")

    # Optional logging
    if reason:
        print(f"XP +{amount} ({reason})")


# ---------------------------
# LEVEL CALCULATION
# ---------------------------
def calculate_level(xp):
    return (xp // 100) + 1


# ---------------------------
# STREAK SYSTEM
# ---------------------------
def update_streak():
    today = datetime.now().date()

    if st.session_state.last_active:
        last_day = datetime.strptime(
            st.session_state.last_active, "%Y-%m-%d"
        ).date()

        diff = (today - last_day).days

        if diff == 1:
            st.session_state.streak += 1
        elif diff > 1:
            st.session_state.streak = 1
    else:
        st.session_state.streak = 1

    st.session_state.last_active = today.strftime("%Y-%m-%d")


# ---------------------------
# DAILY REWARD
# ---------------------------
def daily_reward():
    today = datetime.now().date().strftime("%Y-%m-%d")

    if st.session_state.reward_date != today:
        st.session_state.reward_claimed = False
        st.session_state.reward_date = today

    if not st.session_state.reward_claimed:
        st.session_state.coins += 10
        st.session_state.reward_claimed = True
        st.success("🎁 Daily reward: +10 coins!")


# ---------------------------
# BADGES SYSTEM
# ---------------------------
def check_badges():
    xp = st.session_state.xp

    badges = []

    if xp >= 100:
        badges.append("🔥 Beginner")
    if xp >= 300:
        badges.append("🚀 Explorer")
    if xp >= 600:
        badges.append("💡 Achiever")
    if xp >= 1000:
        badges.append("🏆 Master")

    st.session_state.badges = badges


# ---------------------------
# RESET DAILY (FOR HOME PAGE)
# ---------------------------
def reset_daily():
    today = datetime.now().strftime("%Y-%m-%d")

    if st.session_state.get("reward_date") != today:
        st.session_state.reward_claimed = False
        st.session_state.reward_date = today