import streamlit as st
from core.supabase_client import supabase
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

# Recover user_id if missing
if "user_id" not in st.session_state:
    user = st.session_state.get("user")
    if user and "id" in user:
        st.session_state.user_id = user["id"]

st.title("💳 Upgrade to Premium")

st.markdown("""
### 🏦 Payment Details
Bank: Sterling Bank Plc  
Account Name: Chumcred Limited  
Account Number: 0087611334  

Amount: ₦5,000
""")

uploaded_file = st.file_uploader("Upload Payment Receipt")

if st.button("Submit Payment"):
    if uploaded_file:
        user = st.session_state.get("user", {})
        user_id = st.session_state.get("user_id", None)

        if not user_id:
            st.error("User session not found. Please login again.")
            st.stop()

        name = user.get("name") or user.get("full_name") or "user"
        file_path = f"{user_id}.png"

        try:
            supabase.storage.from_("receipts").upload(
                file_path,
                uploaded_file.getvalue(),
                {
                    "content-type": uploaded_file.type,
                    "upsert": True
                }
            )

            supabase.table("payments").insert({
                "user_id": user_id,
                "name": name,
                "amount": 5000,
                "status": "pending",
                "receipt_url": file_path
            }).execute()

            st.success("✅ Payment submitted. Await admin approval.")

        except Exception as e:
            st.error(f"Upload failed: {e}")

    else:
        st.warning("Upload receipt first")
