import streamlit as st
from auth.login import login_page
from auth.signup import signup_page
from core.session import init_session
from core.user_profile import get_user_profile
from core.block_access import ensure_user_row, enforce_block_access

st.set_page_config(
    page_title="Chumcred Teens",
    page_icon="🧠",
    layout="wide"
)

init_session()

if st.session_state.get("user"):
    ensure_user_row(st.session_state.user)
    enforce_block_access()

if "user" not in st.session_state:
    st.session_state.user = None

if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False

st.markdown("""
<style>
[data-testid="stSidebar"] {display: none;}
[data-testid="stSidebarNav"] {display: none;}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
.hero-box {
    background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #38bdf8 100%);
    padding: 2.5rem 2rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
}
.feature-card {
    background: white;
    padding: 1.2rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    min-height: 170px;
}
.info-card {
    background: #f8fafc;
    padding: 1.1rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-top: 1rem;
}
.auth-wrap {
    margin-top: 1.25rem;
}
.action-card {
    background: white;
    padding: 1.2rem;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


def user_is_onboarded():
    if st.session_state.get("onboarded", False):
        return True

    try:
        profile = get_user_profile() or {}
    except Exception:
        profile = {}

    user = st.session_state.get("user", {}) or {}
    merged = dict(user)

    for key in ["name", "age", "interest", "goal", "plan", "credits", "referral_code"]:
        value = profile.get(key)
        if value not in [None, ""]:
            merged[key] = value

    st.session_state.user = merged

    ready = all(
        merged.get(key) not in [None, ""]
        for key in ["name", "age", "interest", "goal"]
    )

    st.session_state.onboarded = ready
    return ready


def route_logged_in_user():
    st.session_state.just_logged_in = False

    if user_is_onboarded():
        st.switch_page("pages/1_Home.py")
    else:
        st.switch_page("pages/0_Onboarding.py")
    st.stop()


def logout():
    st.session_state.user = None
    st.session_state.onboarded = False
    st.session_state.just_logged_in = False
    st.rerun()


def show_page():
    try:
        st.image("assets/logo.png", width=120)
    except Exception:
        pass

    st.markdown("""
    <div class="hero-box">
        <h1 style="margin-bottom:0.5rem;">Chumcred Teens</h1>
        <p style="font-size:1.15rem; margin-bottom:0.75rem;">
            A safe, smart, and inspiring learning platform for teenagers to build confidence with AI,
            digital skills, creativity, and future-ready knowledge.
        </p>
        <p style="font-size:1rem; opacity:0.95;">
            Learn. Create. Grow.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎓 Learn with Confidence</h3>
            <p>Structured teen-friendly lessons designed to make digital learning easy, practical, and exciting.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🛠️ Build Real Skills</h3>
            <p>Explore creativity, AI, productivity, and hands-on activities that prepare teens for the future.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🌟 Grow Safely</h3>
            <p>A focused platform experience designed for learning, progress, and positive digital development.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h4>How it works</h4>
        <p>
            Step 1: Read about the platform here.<br>
            Step 2: Login or sign up below.<br>
            Step 3: Complete onboarding.<br>
            Step 4: Enter Home.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ALWAYS show Login / Sign Up on landing page
    st.markdown('<div class="auth-wrap">', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        login_page()

    with tab2:
        signup_page()

    st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.user and st.session_state.just_logged_in:
    route_logged_in_user()
else:
    show_page()
