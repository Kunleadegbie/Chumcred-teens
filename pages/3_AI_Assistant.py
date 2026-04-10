import streamlit as st
from core.ai_engine import get_ai_response
from components.cards import section_title
from core.session import init_session
from core.credit_engine import can_use, consume_credits
from core.credits import get_cost
from workflow.sidebar_menu import render_sidebar

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

section_title(
    "🤖 AI Learning Assistant",
    "Ask practical questions and get simple guidance."
)

prompt = st.text_area(
    "What would you like to learn today?",
    placeholder="Example: Teach me Canva like I am 16...",
    height=120,
)

if st.button("Ask AI"):
    if prompt:
        cost = get_cost("ask_ai")
        allowed, message = can_use(cost)

        if not allowed:
            st.error(message)
            st.stop()

        consume_credits(cost)

        response = get_ai_response(prompt)
        st.write(response)
    else:
        st.warning("Please enter a question first.")
