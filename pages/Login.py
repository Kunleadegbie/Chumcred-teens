import streamlit as st
from core.db import get_user_by_email, create_user
import random, string

def generate_ref_code(name="user"):
    base = name[:3].upper() if name else "USR"
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{base}-{rand}"

st.title("🔐 Login / Register")

email = st.text_input("Email")
name = st.text_input("Name (for new users)")
age = st.number_input("Age", min_value=10, max_value=25, step=1)
interest = st.text_input("Your Interest")
goal = st.text_input("Your Goal")

ref_input = st.text_input("Referral Code (Optional)")

if st.button("Continue"):

    if not email:
        st.error("Email is required")
        st.stop()

    user = get_user_by_email(email)

    if user:
        # LOGIN
        st.session_state.user = user
        st.session_state.user_id = user["id"]
        st.success("Welcome back!")
        st.switch_page("pages/1_Home.py")

    else:
        # REGISTER
        ref_code = generate_ref_code(name)

        new_user = {
            "email": email,
            "name": name,
            "age": age,
            "interest": interest,
            "goal": goal,
            "referral_code": ref_code,
            "referred_by": ref_input,
            "plan": "freemium",
            "credits": 0
        }

        res = create_user(new_user)

        st.session_state.user = new_user
        st.session_state.user_id = res.data[0]["id"]

        st.session_state.user = user_data
        st.session_state.user_id = user_data["id"]

        st.success("Account created!")
        st.switch_page("pages/1_Home.py")