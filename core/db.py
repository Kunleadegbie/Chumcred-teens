from typing import Optional, Dict, Any

try:
    from db.supabase_client import supabase
except Exception:
    try:
        from core.supabase_client import supabase
    except Exception:
        supabase = None


def _safe_execute(fn):
    try:
        return fn()
    except Exception:
        return None


def save_progress(user_id: Optional[str], xp: int, level: int, streak: int):
    """
    Safe progress saver.
    Never crashes the app if a table is missing.
    """
    if not supabase or not user_id:
        return None

    payload = {
        "user_id": user_id,
        "xp": xp,
        "level": level,
        "streak": streak,
    }

    def _write_user_progress():
        return supabase.table("user_progress").upsert(payload, on_conflict="user_id").execute()

    def _write_progress():
        return supabase.table("progress").upsert(payload, on_conflict="user_id").execute()

    return _safe_execute(_write_user_progress) or _safe_execute(_write_progress)


def update_leaderboard(user_id: Optional[str], name: str, xp: int):
    """
    Safe leaderboard updater.
    Never crashes the app if the leaderboard table is missing.
    """
    if not supabase or not user_id:
        return None

    payload = {
        "user_id": user_id,
        "name": name,
        "xp": xp,
    }

    def _write_leaderboard():
        return supabase.table("leaderboard").upsert(payload, on_conflict="user_id").execute()

    return _safe_execute(_write_leaderboard)


def update_user(user_id: Optional[str], data: Dict[str, Any]):
    """
    Safe user updater used by credit/credits engine.
    Tries common table names and does not crash the app.
    """
    if not supabase or not user_id or not isinstance(data, dict) or not data:
        return None

    clean_data = {k: v for k, v in data.items()}

    def _update_users():
        return supabase.table("users").update(clean_data).eq("id", user_id).execute()

    def _update_user_profiles():
        return supabase.table("user_profiles").update(clean_data).eq("id", user_id).execute()

    def _upsert_users():
        payload = {"id": user_id, **clean_data}
        return supabase.table("users").upsert(payload, on_conflict="id").execute()

    def _upsert_user_profiles():
        payload = {"id": user_id, **clean_data}
        return supabase.table("user_profiles").upsert(payload, on_conflict="id").execute()

    return (
        _safe_execute(_update_users)
        or _safe_execute(_update_user_profiles)
        or _safe_execute(_upsert_users)
        or _safe_execute(_upsert_user_profiles)
    )
