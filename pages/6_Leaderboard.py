# pages/6_Leaderboard.py

import streamlit as st
from core.session import init_session

init_session()

st.title("🏆 Leaderboard")
st.caption("See how you rank among other learners 🚀")

# ---------------------------
# Ensure required state
# ---------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "name" not in st.session_state:
    st.session_state.name = "Guest"

# ---------------------------
# Simulated leaderboard data
# ---------------------------
leaderboard = [
    {"name": "Alex", "xp": 120},
    {"name": "Maya", "xp": 95},
    {"name": "John", "xp": 80},
]

# Add current user
leaderboard.append({
    "name": st.session_state.name,
    "xp": st.session_state.xp
})

# Sort
leaderboard = sorted(leaderboard, key=lambda x: x["xp"], reverse=True)

# ---------------------------
# DISPLAY
# ---------------------------
for i, user in enumerate(leaderboard, start=1):

    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"

    if user["name"] == st.session_state.name:
        st.markdown(
            f"### {medal} YOU — {user['xp']} XP 🔥"
        )
    else:
        st.markdown(
            f"{medal} {user['name']} — {user['xp']} XP"
        )

# ---------------------------
# USER POSITION MESSAGE
# ---------------------------
rank = next(
    (i for i, u in enumerate(leaderboard, start=1)
     if u["name"] == st.session_state.name),
    None
)

if rank:
    st.info(f"📊 You are ranked #{rank}. Keep going!")