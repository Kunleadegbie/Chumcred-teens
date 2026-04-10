# core/leaderboard.py

import streamlit as st

# ---------------------------
# INIT LEADERBOARD
# ---------------------------
def init_leaderboard():
    if "leaderboard" not in st.session_state:
        st.session_state.leaderboard = []


# ---------------------------
# UPDATE LEADERBOARD
# ---------------------------
def update_leaderboard(name, xp):
    leaderboard = st.session_state.leaderboard

    # Check if user already exists
    user_found = False
    for user in leaderboard:
        if user["name"] == name:
            user["xp"] = xp
            user_found = True
            break

    if not user_found:
        leaderboard.append({"name": name, "xp": xp})

    # Sort by XP descending
    leaderboard.sort(key=lambda x: x["xp"], reverse=True)

    st.session_state.leaderboard = leaderboard


# ---------------------------
# GET TOP USERS
# ---------------------------
def get_top_users(limit=10):
    return st.session_state.leaderboard[:limit]