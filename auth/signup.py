import time
import streamlit as st
from db.supabase_client import supabase

ADMIN_EMAIL = "chumcred@gmail.com"


def signup_page():
    st.subheader("Create Your Account")

    if "signup_in_progress" not in st.session_state:
        st.session_state.signup_in_progress = False

    if "last_signup_attempt" not in st.session_state:
        st.session_state.last_signup_attempt = 0.0

    full_name = st.text_input("Full Name", key="signup_full_name").strip()
    email = st.text_input("Email Address", key="signup_email").strip().lower()
    password = st.text_input("Password", type="password", key="signup_password").strip()
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password").strip()

    if st.button(
        "Sign Up",
        key="signup_button",
        use_container_width=True,
        disabled=st.session_state.signup_in_progress,
    ):
        now = time.time()

        # Prevent rapid repeated clicks / retries
        if now - st.session_state.last_signup_attempt < 8:
            st.warning("Please wait a few seconds before trying again.")
            return

        st.session_state.last_signup_attempt = now
        st.session_state.signup_in_progress = True

        try:
            if not full_name:
                st.error("Full name is required.")
                return

            if not email:
                st.error("Email is required.")
                return

            if "@" not in email or "." not in email:
                st.error("Please enter a valid email address.")
                return

            if not password:
                st.error("Password is required.")
                return

            if len(password) < 6:
                st.error("Password must be at least 6 characters.")
                return

            if password != confirm_password:
                st.error("Passwords do not match.")
                return

            role = "super_admin" if email == ADMIN_EMAIL.lower() else "student"

            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "full_name": full_name,
                            "app": "chumcred_teens",
                            "role": role,
                        }
                    },
                }
            )

            if response.user:
                st.success("Account created successfully. You can now continue.")
            else:
                st.success("Signup submitted successfully. Please try logging in.")

        except Exception as e:
            error_text = str(e).lower()

            if "rate limit" in error_text or "email rate limit exceeded" in error_text:
                st.error("Too many signup attempts were made recently. Please wait a few minutes and try again.")
            elif "user already registered" in error_text or "already been registered" in error_text:
                st.warning("This email is already registered. Please use Login instead.")
            else:
                st.error(f"Signup failed: {e}")

        finally:
            st.session_state.signup_in_progress = False