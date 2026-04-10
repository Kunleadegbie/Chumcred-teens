import streamlit as st
from core.db import supabase
from core.session import init_session
from workflow.sidebar_menu import render_sidebar

init_session()

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

role = st.session_state.get("user", {}).get("role", "student")
render_sidebar(role)

st.title("🛠 Admin Payment Approval")

try:
    response = (
        supabase
        .table("payments")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    payments = response.data

except Exception as e:
    st.error(f"Error fetching payments: {e}")
    payments = []

if not payments:
    st.info("No payment records yet.")
    st.stop()

for p in payments:
    with st.container():
        st.markdown("---")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.write(f"👤 Name: {p.get('name')}")
            st.write(f"💰 Amount: ₦{p.get('amount')}")
            st.write(f"📌 Status: {p.get('status')}")
            st.write(f"📅 Date: {p.get('created_at')}")

            if p.get("receipt_url"):
                st.image(p.get("receipt_url"), width=200)

        with col2:
            if p.get("status") == "pending":

                if st.button("✅ Approve", key=f"approve_{p['id']}"):
                    supabase.table("payments").update({
                        "status": "approved"
                    }).eq("id", p["id"]).execute()

                    supabase.table("users").update({
                        "plan": "premium",
                        "credits": p.get("credits", 250),
                        "is_premium": True
                    }).eq("id", p["user_id"]).execute()

                    st.success("Approved + User upgraded")
                    st.rerun()

                if st.button("❌ Reject", key=f"reject_{p['id']}"):
                    supabase.table("payments").update({
                        "status": "rejected"
                    }).eq("id", p["id"]).execute()

                    st.warning("Payment rejected")
                    st.rerun()

            else:
                st.info("Processed")
