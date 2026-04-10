# core/social.py

import streamlit as st
from datetime import datetime

# ---------------------------
# INIT SOCIAL SYSTEM
# ---------------------------
def init_social():
    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "messages" not in st.session_state:
        st.session_state.messages = []


# ---------------------------
# ASK QUESTION
# ---------------------------
def add_question(user, question):
    st.session_state.questions.append({
        "user": user,
        "question": question,
        "answers": [],
        "time": datetime.now().strftime("%H:%M")
    })


# ---------------------------
# ANSWER QUESTION
# ---------------------------
def add_answer(index, user, answer):
    st.session_state.questions[index]["answers"].append({
        "user": user,
        "answer": answer,
        "time": datetime.now().strftime("%H:%M")
    })


# ---------------------------
# SEND CHAT MESSAGE
# ---------------------------
def send_message(user, message):
    st.session_state.messages.append({
        "user": user,
        "message": message,
        "time": datetime.now().strftime("%H:%M")
    })