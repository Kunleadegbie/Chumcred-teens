import streamlit as st
from core.ai_engine import teen_ai
from core.session import init_session
from core.credits import get_cost
from core.credit_engine import can_use, consume_credits
from workflow.sidebar_menu import render_sidebar

from openai import OpenAI
import tempfile

st.set_page_config(
    page_title="Chumcred Teens | Learn Anything",
    page_icon="🧠",
    layout="wide"
)

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🧠 Learn Anything")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def speak_text_native(text):
    try:
        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            f.write(response.read())
            return f.name

    except Exception as e:
        st.error(f"Speech error: {str(e)}")
        return None


tab1, tab2 = st.tabs(["📘 Learn", "🌍 Language"])

with tab1:
    st.markdown("### 💡 Ask anything you want to learn")

    topic = st.text_input(
        "What do you want to learn?",
        placeholder="e.g. What is AI? How to make money online? Football tactics?"
    )

    if st.button("Explain to Me", use_container_width=True):
        if not topic:
            st.warning("Please enter a topic")
        else:
            cost = get_cost("ask_ai")
            allowed, message = can_use(cost)

            if not allowed:
                st.error(message)
                if st.button("Upgrade Now 🚀"):
                    st.switch_page("pages/9_Subscription.py")
                st.stop()

            consume_credits(cost)

            with st.spinner("Thinking..."):
                response = teen_ai(topic, mode="learn")

            st.markdown("### 📖 Explanation")
            st.write(response)

    st.markdown("---")

    if topic:
        if st.button("Give Real-Life Example", key="example_btn"):
            cost = get_cost("ask_ai")
            allowed, message = can_use(cost)

            if not allowed:
                st.error(message)
                st.stop()

            consume_credits(cost)

            example = teen_ai(
                topic,
                mode="learn",
                extra="Give a practical real-life example a teenager can relate to."
            )
            st.write(example)

        if st.button("How can I make money with this?", key="money_btn"):
            cost = get_cost("ask_ai")
            allowed, message = can_use(cost)

            if not allowed:
                st.error(message)
                st.stop()

            consume_credits(cost)

            money = teen_ai(
                topic,
                mode="learn",
                extra="How can a teenager use this skill to make money?"
            )
            st.write(money)

with tab2:
    st.markdown("### 🌍 Translate & Learn Languages")

    col1, col2 = st.columns(2)

    with col1:
        text = st.text_input("Enter word or sentence")

    with col2:
        target_lang = st.text_input("Translate to")

    if st.button("Translate", use_container_width=True):
        if not text or not target_lang:
            st.warning("Please complete both fields")
        else:
            cost = get_cost("translate")
            allowed, message = can_use(cost)

            if not allowed:
                st.error(message)
                if st.button("Upgrade Now 🚀", key="upgrade_translate"):
                    st.switch_page("pages/9_Subscription.py")
                st.stop()

            consume_credits(cost)

            with st.spinner("Translating..."):
                translated_text = teen_ai(
                    f"Translate '{text}' to {target_lang}",
                    mode="translate"
                )

            st.session_state.translation = translated_text

            st.markdown("### 🌐 Translation")
            st.write(translated_text)

    if "translation" in st.session_state:
        if st.button("🔊 Speak", key="speak_translation"):
            cost = get_cost("speak")
            allowed, message = can_use(cost)

            if not allowed:
                st.error(message)
                if st.button("Upgrade Now 🚀", key="upgrade_speak"):
                    st.switch_page("pages/9_Subscription.py")
                st.stop()

            consume_credits(cost)

            audio_file = speak_text_native(st.session_state.translation)

            if audio_file:
                st.audio(audio_file)
