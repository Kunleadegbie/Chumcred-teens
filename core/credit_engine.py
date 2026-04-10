import streamlit as st
from core.db import update_user

def get_user_credits():
    return st.session_state.user.get("credits", 0)

def is_premium():
    return st.session_state.user.get("plan") == "premium"

def can_use(action_cost):
    return True, None

# def can_use(action_cost):
    # Freemium rule
    # if not is_premium():
        # allow only 1 AI usage per day
        # if st.session_state.daily_ai_usage >= 1:
            # return False, "Free limit reached. Upgrade to continue."

        # return True, None

    # Premium rule
    if get_user_credits() < action_cost:
        return False, "Not enough credits."

    return True, None

def consume_credits(action_cost):
    return True

# def consume_credits(action_cost):
    # FREEMIUM
    # if not is_premium():
        # st.session_state.daily_ai_usage += 1
        # return True

    # PREMIUM
    st.session_state.user["credits"] -= action_cost

    # Persist to DB
    update_user(
        st.session_state.user_id,
        {"credits": st.session_state.user["credits"]}
    )

    return True