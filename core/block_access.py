import streamlit as st
from datetime import date, datetime, timedelta
from db.supabase_client import supabase

ADMIN_EMAIL = "chumcred@gmail.com"


def is_admin_email(email: str) -> bool:
    return (email or "").strip().lower() == ADMIN_EMAIL.lower()


def parse_date(value):
    if not value:
        return None
    try:
        if isinstance(value, date):
            return value
        return datetime.fromisoformat(str(value)).date()
    except Exception:
        try:
            return datetime.strptime(str(value), "%Y-%m-%d").date()
        except Exception:
            return None


def get_user_row(user_id: str):
    if not user_id:
        return None
    try:
        resp = (
            supabase.table("users")
            .select("*")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        rows = resp.data or []
        return rows[0] if rows else None
    except Exception:
        return None


def ensure_user_row(user_dict: dict):
    if not user_dict:
        return None

    user_id = user_dict.get("id")
    email = (user_dict.get("email") or "").strip().lower()
    if not user_id or not email:
        return None

    existing = get_user_row(user_id)

    base_name = (
        user_dict.get("name")
        or user_dict.get("full_name")
        or email.split("@")[0]
    )

    payload = {
        "id": user_id,
        "email": email,
        "name": base_name,
    }

    if user_dict.get("age") not in [None, ""]:
        payload["age"] = user_dict.get("age")

    if existing:
        if not existing.get("trial_start_date"):
            payload["trial_start_date"] = date.today().isoformat()
        if not existing.get("trial_end_date"):
            payload["trial_end_date"] = (date.today() + timedelta(days=14)).isoformat()
        if existing.get("payment_status") in [None, ""]:
            payload["payment_status"] = "trial"
        if existing.get("is_blocked") is None:
            payload["is_blocked"] = False
    else:
        payload.update({
            "is_blocked": False,
            "trial_start_date": date.today().isoformat(),
            "trial_end_date": (date.today() + timedelta(days=14)).isoformat(),
            "payment_status": "trial",
        })

    try:
        supabase.table("users").upsert(payload, on_conflict="id").execute()
    except Exception:
        pass

    return get_user_row(user_id)


def auto_expire_trial(user_row: dict, actor_email: str = "system"):
    if not user_row:
        return user_row

    payment_status = str(user_row.get("payment_status") or "trial").strip().lower()
    is_blocked = bool(user_row.get("is_blocked"))
    trial_end = parse_date(user_row.get("trial_end_date"))

    if payment_status == "paid":
        return user_row

    if (not is_blocked) and trial_end and trial_end < date.today():
        try:
            supabase.table("users").update({
                "is_blocked": True,
                "payment_status": "expired",
                "block_reason": "Trial expired",
                "blocked_at": datetime.utcnow().isoformat(),
                "blocked_by": actor_email,
            }).eq("id", user_row["id"]).execute()
        except Exception:
            pass

        return get_user_row(user_row["id"])

    return user_row


def logout_now():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    st.session_state.user = None
    st.session_state.onboarded = False
    st.session_state.just_logged_in = False
    st.rerun()


def enforce_block_access():
    current_user = st.session_state.get("user")
    if not current_user:
        return

    row = ensure_user_row(current_user)
    row = auto_expire_trial(row, (current_user.get("email") or "system"))

    if not row:
        return

    if bool(row.get("is_blocked")):
        st.warning("Your free trial has expired or your account has been blocked. Please complete payment or contact support.")
        st.info(
            f"Payment Status: {row.get('payment_status', 'trial')} | "
            f"Trial End Date: {row.get('trial_end_date', 'Not set')}"
        )
        if row.get("block_reason"):
            st.caption(f"Reason: {row.get('block_reason')}")
        if st.button("Logout", use_container_width=True, key="blocked_logout"):
            logout_now()
        st.stop()