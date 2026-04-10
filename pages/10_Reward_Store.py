import streamlit as st

import streamlit as st
from core.session import init_session

init_session()

st.title("🛍 Reward Store")

st.write(f"💰 Coins: {st.session_state.coins}")

items = [
    {"name": "Unlock AI Coach Style", "cost": 50},
    {"name": "Premium Badge", "cost": 100},
]

for item in items:
    if st.button(f"Buy {item['name']} ({item['cost']} coins)"):
        if st.session_state.coins >= item["cost"]:
            st.session_state.coins -= item["cost"]
            st.success("Purchased!")
        else:
            st.error("Not enough coins")