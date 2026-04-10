# core/credits.py

import streamlit as st
from datetime import datetime

# ---------------------------------------
# CREDIT COST CONFIG
# ---------------------------------------
CREDIT_COSTS = {
    "ask_ai": 5,
    "coach": 5,
    "translate": 2,
    "speak": 5,
    "long_explain": 10,
    "project": 5,
}

def get_cost(action):
    return CREDIT_COSTS.get(action, 0)

# ---------------------------------------
# DAILY LIMIT FOR FREEMIUM
# ---------------------------------------
FREE_DAILY_LIMIT = 1


# ---------------------------------------
# CHECK ACCESS
# ---------------------------------------
def can_use(feature):
    """
    Check if user can use a feature
    """

    plan = st.session_state.get("plan", "freemium")
    credits = st.session_state.get("credits", 0)

    # ---------------------------
    # FREEMIUM LOGIC
    # ---------------------------
    if plan == "freemium":
        today = str(datetime.today().date())

        if "last_usage_date" not in st.session_state:
            st.session_state.last_usage_date = today
            st.session_state.daily_ai_usage = 0

        if st.session_state.last_usage_date != today:
            st.session_state.daily_ai_usage = 0
            st.session_state.last_usage_date = today

        if st.session_state.daily_ai_usage >= FREE_DAILY_LIMIT:
            return False, "Free limit reached. Upgrade to continue."

        return True, ""

    # ---------------------------
    # PREMIUM LOGIC
    # ---------------------------
    cost = COSTS.get(feature, 0)

    if credits < cost:
        return False, "Insufficient credits. Please top up."

    return True, ""


# ---------------------------------------
# DEDUCT CREDITS
# ---------------------------------------
def deduct(feature):
    """
    Deduct credits after usage
    """

    plan = st.session_state.get("plan", "freemium")

    # FREEMIUM → increment usage
    if plan == "freemium":
        st.session_state.daily_ai_usage += 1
        return

    # PREMIUM → deduct credits
    cost = COSTS.get(feature, 0)
    st.session_state.credits -= cost


# ---------------------------------------
# SHOW UPGRADE MESSAGE
# ---------------------------------------
def show_upgrade():
    st.warning("🚀 Upgrade to Premium to unlock unlimited access!")
    if st.button("Upgrade Now"):
        st.switch_page("pages/8_Subscription.py")