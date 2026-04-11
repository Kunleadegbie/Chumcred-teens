import time
from datetime import date, timedelta
import streamlit as st
from db.supabase_client import supabase

ADMIN_EMAIL = "chumcred@gmail.com"


def sync_user_to_public_users(user_id: str, email: str, full_name: str):
    try:
        trial_start = date.today()
        trial_end = trial_start + timedelta(days=30)

        supabase.table("users").upsert(
            {
                "id": user_id,
                "email": email,
                "name": full_name,
                "age": None,
                "is_blocked": False,
                "payment_status": "trial",
                "trial_start_date": trial_start.isoformat(),
                "trial_end_date": trial_end.isoformat(),
            },
            on_conflict="id",
        ).execute()
        return True, None
    except Exception as e:
        return False, str(e)


def signup_page():
    st.subheader("Create Your Account")

    if "signup_in_progress" not in st.session_state:
        st.session_state.signup_in_progress = False

    if "last_signup_attempt" not in st.session_state:
        st.session_state.last_signup_attempt = 0.0

    if "signup_success" not in st.session_state:
        st.session_state.signup_success = False

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
        st.session_state.signup_success = False

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
                st.session_state.signup_success = True

                synced, sync_error = sync_user_to_public_users(
                    response.user.id,
                    email,
                    full_name,
                )

                st.success("✅ Account created successfully!")

                st.info(
                    "📩 Please check your email and click the confirmation link to activate your account.\n\n"
                    "⚠️ Do NOT try to sign up again.\n"
                    "After confirming your email, come back here and log in."
                )

                st.caption("If you don’t see the email, check your Spam or Promotions folder.")

                if synced:
                    st.caption("Your profile has been added to the admin user list.")
                else:
                    st.warning(f"Account created, but profile sync had an issue: {sync_error}")
            else:
                st.session_state.signup_success = True

                st.success("✅ Signup submitted successfully!")

                st.info(
                    "📩 Please check your email and click the confirmation link to activate your account.\n\n"
                    "⚠️ Do NOT try to sign up again.\n"
                    "After confirming your email, come back here and log in."
                )

                st.caption("If you don’t see the email, check your Spam or Promotions folder.")

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

    if st.session_state.signup_success:
        # ===============================
        # RESEND CONFIRMATION EMAIL
        # ===============================
        st.markdown("---")
        st.write("Didn't receive the email?")

        if st.button("📩 Resend Confirmation Email", use_container_width=True):
            if not email:
                st.error("Please enter your email above first.")
            else:
                try:
                    supabase.auth.resend(
                        {
                            "type": "signup",
                            "email": email,
                        }
                    )
                    st.success("Confirmation email sent again. Please check your inbox.")
                    st.caption("Also check Spam or Promotions folder.")
                except Exception as e:
                    error_text = str(e).lower()

                    if "rate limit" in error_text:
                        st.error("Too many requests. Please wait a few minutes before trying again.")
                    else:
                        st.error(f"Could not resend email: {e}")
