import streamlit as st
from db.supabase_client import supabase

ADMIN_EMAIL = "chumcred@gmail.com"


def login_page():
    st.subheader("Welcome To Chumcred Teens App")

    email = st.text_input("Email Address", key="login_email").strip().lower()
    password = st.text_input("Password", type="password", key="login_password").strip()

    if st.button("Login", key="login_button", use_container_width=True):
        if not email:
            st.error("Email is required.")
            return

        if not password:
            st.error("Password is required.")
            return

        try:
            res = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )

            if res.user:
                metadata = getattr(res.user, "user_metadata", {}) or {}
                role = "super_admin" if email == ADMIN_EMAIL.lower() else metadata.get("role", "student")

                st.session_state.user = {
                    "id": res.user.id,
                    "email": getattr(res.user, "email", email),
                    "full_name": metadata.get("full_name", ""),
                    "role": role
                }

                st.session_state.just_logged_in = True
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid login credentials.")

        except Exception as e:
            st.error(f"Login failed: {e}")
