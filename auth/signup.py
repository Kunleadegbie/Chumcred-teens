import streamlit as st
from db.supabase_client import supabase

ADMIN_EMAIL = "chumcred@gmail.com"


def signup_page():
    st.subheader("Create Your Account")

    full_name = st.text_input("Full Name", key="signup_full_name").strip()
    email = st.text_input("Email Address", key="signup_email").strip().lower()
    password = st.text_input("Password", type="password", key="signup_password").strip()
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password").strip()

    if st.button("Sign Up", key="signup_button", use_container_width=True):
        if not full_name:
            st.error("Full name is required.")
            return

        if not email:
            st.error("Email is required.")
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

        try:
            role = "super_admin" if email == ADMIN_EMAIL.lower() else "student"

            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "full_name": full_name,
                            "app": "chumcred_teens",
                            "role": role
                        }
                    }
                }
            )

            if response.user:
                if role == "super_admin":
                    st.success("Super admin account created successfully. Please check your email to confirm your account.")
                else:
                    st.success("Account created successfully. Please check your email to confirm your account.")
            else:
                st.warning("Signup request submitted. Please check your email for confirmation.")

        except Exception as e:
            st.error(f"Signup failed: {e}")