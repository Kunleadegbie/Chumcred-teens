import streamlit as st


def render_sidebar(role=None):
    """
    Shared Chumcred Teens MVP sidebar.
    - Hides Streamlit default page navigation
    - Shows only MVP menu items
    - Sends user back to app.py immediately on logout
    """

    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user", {}) or {}
    email = (user.get("email") or "").strip().lower()
    name = (
        user.get("name")
        or user.get("full_name")
        or (email.split("@")[0] if email else "Student")
    )

    with st.sidebar:
        st.markdown("## Chumcred Teens")
        st.caption(name)

        st.page_link("pages/1_Home.py", label="🏠 Home")
        st.page_link("pages/2_Skill_Discovery.py", label="🎯 Skill Discovery")
        st.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")
        st.page_link("pages/4_Projects.py", label="🛠 Projects")
        st.page_link("pages/5_Learn_Anything.py", label="🌍 Learn Anything")
        st.page_link("pages/7_Community.py", label="🌍 Community")
        st.page_link("pages/8_AI_Coach.py", label="🧠 AI Coach")
        st.page_link("pages/9_Daily_Missions.py", label="🎯 Daily Missions")

        # Hidden for MVP for now:
        # pages/5_Progress.py
        # pages/6_Leaderboard.py
        # pages/10_Reward_Store.py

        if email == "chumcred@gmail.com" or role == "super_admin":
            st.page_link("pages/9_Subscription.py", label="💳 Subscription")
            st.page_link("pages/10_Admin_Payments.py", label="⚙️ Admin Payments")
            st.page_link("pages/10_Block_Unblock_Users.py", label="🚫 Block / Unblock Users")

        st.markdown("---")

        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.onboarded = False
            st.session_state.just_logged_in = False
            st.switch_page("app.py")
