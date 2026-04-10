import streamlit as st


def is_premium():
    return st.session_state.get("plan") == "premium"


def require_premium():
    if not is_premium():
        st.warning("🔒 This feature is for premium users.")
        st.stop()