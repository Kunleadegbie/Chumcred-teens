import os
import streamlit as st
from supabase import create_client, Client


def get_supabase_client() -> Client:
    url = None
    key = None

    # 1) Try Streamlit secrets first
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = (
            st.secrets.get("SUPABASE_ANON_KEY")
            or st.secrets.get("SUPABASE_PUBLISHABLE_KEY")
        )
    except Exception:
        pass

    # 2) Fall back to environment variables
    if not url:
        url = os.getenv("SUPABASE_URL")

    if not key:
        key = (
            os.getenv("SUPABASE_ANON_KEY")
            or os.getenv("SUPABASE_PUBLISHABLE_KEY")
        )

    if not url:
        raise ValueError(
            "Supabase URL is missing. Set SUPABASE_URL in .streamlit/secrets.toml or environment variables."
        )

    if not key:
        raise ValueError(
            "Supabase key is missing. Set SUPABASE_ANON_KEY or SUPABASE_PUBLISHABLE_KEY in .streamlit/secrets.toml or environment variables."
        )

    return create_client(url, key)


supabase = get_supabase_client()