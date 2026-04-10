# core/ai_engine.py

import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def teen_ai(prompt, mode="learn", extra=""):
    """
    Core AI engine for Chumcred Teens
    Supports:
    - learn (default)
    - translate
    - general chat
    """

    system_base = """
You are a smart, friendly AI tutor for teenagers (ages 13–19).

RULES:
- Explain things simply and clearly
- Use real-life relatable examples
- Avoid complex jargon
- Be engaging and slightly conversational
"""

    if mode == "learn":
        system = system_base + """
Help the student understand the topic deeply.
Break it into simple steps.
Give examples.
"""

    elif mode == "translate":
        system = system_base + """
You are a language tutor.
Translate clearly, explain meaning, and give usage examples.
"""

    else:
        system = system_base

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": f"{prompt}\n{extra}"}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"


# ✅ THIS IS THE FIX (DO NOT REMOVE)
def get_ai_response(prompt):
    """
    Compatibility wrapper for existing imports
    Default = learning mode
    """
    return teen_ai(prompt, mode="learn")


def get_ai_coach_response(name, age, interest, goal, question):
    prompt = f"""
You are a friendly and intelligent mentor for teenagers.

User Profile:
- Name: {name}
- Age: {age}
- Interest: {interest}
- Goal: {goal}

User Question:
{question}

Your role:
- Be motivating
- Be practical
- Give clear steps
- Keep it simple and engaging

Answer like a mentor, not a teacher.
"""

    try:
        from openai import OpenAI
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    except:
        return "⚠️ AI Coach is currently unavailable. Try again."


def generate_daily_coach(name, interest, goal):
    prompt = f"""
You are a motivational AI coach for teenagers.

User:
- Name: {name}
- Interest: {interest}
- Goal: {goal}

Give a short daily motivational message + one action for today.
Keep it simple, friendly, and inspiring.
"""

    try:
        from openai import OpenAI
        client = OpenAI()

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )

        return res.choices[0].message.content

    except:
        return "🔥 Stay focused today. Small progress is still progress!"