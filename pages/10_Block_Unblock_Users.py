import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
from db.supabase_client import supabase
from core.block_access import (
    ADMIN_EMAIL,
    ensure_user_row,
    auto_expire_trial,
)

st.set_page_config(
    page_title="Block / Unblock Users",
    page_icon="🚫",
    layout="wide"
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
.block-card {
    background: white;
    padding: 1rem;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please login first.")
    if st.button("Go to Welcome Page", use_container_width=True):
        st.switch_page("app.py")
    st.stop()

current_user = st.session_state.user
current_email = (current_user.get("email") or "").strip().lower()

if current_email != ADMIN_EMAIL.lower():
    st.error("Access denied.")
    st.stop()

ensure_user_row(current_user)

with st.sidebar:
    st.markdown("## Chumcred Teens")
    st.caption(st.session_state.user.get("name", "Admin"))

    st.page_link("pages/1_Home.py", label="🏠 Home")
    st.page_link("pages/2_Skill_Discovery.py", label="🎯 Skill Discovery")
    st.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")
    st.page_link("pages/4_Projects.py", label="🛠 Projects")
    st.page_link("pages/5_Learn_Anything.py", label="🌍 Learn Anything")
    st.page_link("pages/8_AI_Coach.py", label="🧠 AI Coach")
    st.page_link("pages/9_Daily_Missions.py", label="🎯 Daily Missions")
    st.page_link("pages/9_Subscription.py", label="💳 Subscription")
    st.page_link("pages/10_Admin_Payments.py", label="⚙️ Admin Payments")
    st.page_link("pages/10_Block_Unblock_Users.py", label="🚫 Block / Unblock Users")

    st.markdown("---")

    if st.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.onboarded = False
        st.session_state.just_logged_in = False
        st.switch_page("app.py")

st.title("🚫 Block / Unblock Users")
st.caption(f"Admin: {current_email}")

def load_users():
    rows = (
        supabase.table("users")
        .select("*")
        .order("trial_start_date", desc=True)
        .execute()
        .data
        or []
    )
    refreshed = []
    for row in rows:
        refreshed.append(auto_expire_trial(row, current_email) or row)
    return refreshed

def block_user(user_id: str, reason: str):
    supabase.table("users").update({
        "is_blocked": True,
        "block_reason": reason or "Blocked by admin",
        "payment_status": "blocked",
        "blocked_at": datetime.utcnow().isoformat(),
        "blocked_by": current_email,
    }).eq("id", user_id).execute()

def unblock_user(user_id: str):
    supabase.table("users").update({
        "is_blocked": False,
        "payment_status": "paid",
        "block_reason": None,
        "unblocked_at": datetime.utcnow().isoformat(),
        "unblocked_by": current_email,
    }).eq("id", user_id).execute()

def reset_trial(user_id: str, days: int):
    start = date.today()
    end = start + timedelta(days=days)
    supabase.table("users").update({
        "is_blocked": False,
        "payment_status": "trial",
        "block_reason": None,
        "trial_start_date": start.isoformat(),
        "trial_end_date": end.isoformat(),
        "unblocked_at": datetime.utcnow().isoformat(),
        "unblocked_by": current_email,
    }).eq("id", user_id).execute()

def mark_paid(user_id: str):
    supabase.table("users").update({
        "is_blocked": False,
        "payment_status": "paid",
        "block_reason": None,
        "unblocked_at": datetime.utcnow().isoformat(),
        "unblocked_by": current_email,
    }).eq("id", user_id).execute()

users = load_users()

search = st.text_input("Search by name or email").strip().lower()
status_filter = st.selectbox("Filter by status", ["All", "Active", "Blocked"])
payment_filter = st.selectbox("Filter by payment", ["All", "trial", "paid", "expired", "blocked"])

filtered = []
for row in users:
    email = str(row.get("email") or "").lower()
    name = str(row.get("name") or "").lower()
    is_blocked = bool(row.get("is_blocked"))
    payment_status = str(row.get("payment_status") or "trial").lower()

    if search and search not in email and search not in name:
        continue
    if status_filter == "Active" and is_blocked:
        continue
    if status_filter == "Blocked" and not is_blocked:
        continue
    if payment_filter != "All" and payment_status != payment_filter:
        continue

    filtered.append(row)

st.write(f"Users found: **{len(filtered)}**")

if filtered:
    table_rows = []
    for row in filtered:
        table_rows.append({
            "Name": row.get("name") or "No name",
            "Email": row.get("email") or "No email",
            "Age": row.get("age") or "N/A",
            "Blocked": "Yes" if bool(row.get("is_blocked")) else "No",
            "Payment Status": row.get("payment_status") or "trial",
            "Trial Start": row.get("trial_start_date") or "N/A",
            "Trial End": row.get("trial_end_date") or "N/A",
            "Reason": row.get("block_reason") or "",
        })

    st.markdown("### 📋 All Signed-Up Users")
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
else:
    st.info("No users found.")
    st.stop()

st.markdown("### Manage Individual Users")

for i, row in enumerate(filtered):
    user_id = row.get("id")
    email = row.get("email") or "No email"
    name = row.get("name") or "No name"
    age = row.get("age") or "N/A"
    is_blocked = bool(row.get("is_blocked"))
    payment_status = row.get("payment_status") or "trial"
    trial_start = row.get("trial_start_date") or "N/A"
    trial_end = row.get("trial_end_date") or "N/A"
    block_reason = row.get("block_reason") or ""

    st.markdown('<div class="block-card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 2, 2])

    with c1:
        st.markdown(f"### {name}")
        st.write(f"**Email:** {email}")
        st.write(f"**Age:** {age}")

    with c2:
        st.write(f"**Blocked:** {'Yes' if is_blocked else 'No'}")
        st.write(f"**Payment Status:** {payment_status}")
        st.write(f"**Trial Start:** {trial_start}")
        st.write(f"**Trial End:** {trial_end}")

    with c3:
        reason = st.text_input("Reason", value=block_reason, key=f"reason_{i}")

        if not is_blocked:
            if st.button("Block User", key=f"block_{i}", use_container_width=True):
                block_user(user_id, reason)
                st.success(f"{email} blocked.")
                st.rerun()
        else:
            if st.button("Unblock User", key=f"unblock_{i}", use_container_width=True):
                unblock_user(user_id)
                st.success(f"{email} unblocked.")
                st.rerun()

        if st.button("Mark as Paid", key=f"paid_{i}", use_container_width=True):
            mark_paid(user_id)
            st.success(f"{email} marked as paid.")
            st.rerun()

        d1, d2 = st.columns(2)
        with d1:
            if st.button("14 Days", key=f"trial14_{i}", use_container_width=True):
                reset_trial(user_id, 14)
                st.success(f"14-day trial reset for {email}.")
                st.rerun()
        with d2:
            if st.button("30 Days", key=f"trial30_{i}", use_container_width=True):
                reset_trial(user_id, 30)
                st.success(f"30-day trial reset for {email}.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
