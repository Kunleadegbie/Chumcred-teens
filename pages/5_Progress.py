import streamlit as st
from components.cards import metric_card, section_title

from core.session import init_session
init_session()

section_title(
    "📈 Progress Tracker",
    "See how far you’ve come."
)

col1, col2 = st.columns(2)

with col1:
    metric_card("Current Level", str(st.session_state.level), "Level up by completing projects")
with col2:
    metric_card("Total Points", str(st.session_state.points), "Every effort counts")

st.markdown("### Current Skill Path")
if st.session_state.selected_skill:
    st.success(st.session_state.selected_skill)
else:
    st.warning("You have not selected a skill path yet.")