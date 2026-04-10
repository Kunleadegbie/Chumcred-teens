import streamlit as st
from core.session import init_session
from core.social import init_social, add_question, add_answer, send_message
from core.gamification import add_xp
from workflow.sidebar_menu import render_sidebar

init_session()
init_social()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🌍 Community & Peer Help")

user = st.session_state.get("user", {}).get("name", "Anonymous")

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------
# QUICK COMMUNITY CHAT
# ---------------------------
st.markdown("### 💬 Community")

quick_msg = st.text_input("Say something...", key="community_quick_msg")

if st.button("Send", key="community_quick_send"):
    if quick_msg:
        st.session_state.chat.append(quick_msg)

for m in st.session_state.chat[::-1]:
    st.write(f"🧑 {m}")

# ---------------------------
# ASK A QUESTION
# ---------------------------
st.markdown("### ❓ Ask the Community")

question = st.text_input("What do you need help with?", key="community_question")

if st.button("Ask Question", key="community_ask_question"):
    if question:
        add_question(user, question)
        add_xp(5, "Asked question")
        st.success("Question posted!")
        st.rerun()

# ---------------------------
# DISPLAY QUESTIONS
# ---------------------------
st.markdown("### 💬 Community Questions")

for i, q in enumerate(st.session_state.questions):
    st.markdown(f"**{q['user']}** ({q['time']})")
    st.write(q["question"])

    for a in q["answers"]:
        st.markdown(f"- {a['user']}: {a['answer']} ({a['time']})")

    answer = st.text_input("Your answer...", key=f"ans_{i}")

    if st.button("Reply", key=f"btn_{i}"):
        if answer:
            add_answer(i, user, answer)
            add_xp(10, "Helped peer")
            st.rerun()

    st.divider()

# ---------------------------
# LIVE CHAT
# ---------------------------
st.markdown("### 💬 Live Chat")

live_msg = st.text_input("Type a message...", key="community_live_msg")

if st.button("Send", key="community_send_btn"):
    if live_msg:
        send_message(user, live_msg)
        add_xp(2, "Chat activity")
        st.rerun()

for m in st.session_state.messages[-10:]:
    st.write(f"**{m['user']}**: {m['message']} ({m['time']})")
