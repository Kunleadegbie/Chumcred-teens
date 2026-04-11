import streamlit as st
from db.supabase_client import supabase


def _current_user():
    return st.session_state.get("user", {}) or {}


def _current_user_id():
    user = _current_user()
    return user.get("id")


def _safe_int(value, default=15):
    try:
        return int(value)
    except Exception:
        return default


def _load_profile_from_db():
    user_id = _current_user_id()
    if not user_id:
        return {}

    try:
        resp = (
            supabase.table("users")
            .select("*")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )
        rows = resp.data or []
        if not rows:
            return {}
        row = rows[0]
        return {
            "name": row.get("name", ""),
            "age": row.get("age", 15),
            "interest": row.get("interest", ""),
            "goal": row.get("goal", ""),
            "plan": row.get("plan", "freemium"),
            "credits": row.get("credits", 0),
            "referral_code": row.get("referral_code", ""),
            "selected_skill": row.get("selected_skill"),
            "active_project": row.get("active_project"),
            "skills": row.get("skills") or [],
            "projects": row.get("projects") or [],
            "xp": row.get("xp", 0),
            "level": row.get("level", 1),
            "streak": row.get("streak", 0),
            "badges": row.get("badges") or [],
        }
    except Exception:
        return {}


def _save_profile_to_db(profile: dict):
    user = _current_user()
    user_id = user.get("id")
    email = user.get("email")
    if not user_id or not email:
        return

    payload = {
        "id": user_id,
        "email": email,
        "name": profile.get("name", ""),
        "age": _safe_int(profile.get("age", 15), 15),
        "interest": profile.get("interest", ""),
        "goal": profile.get("goal", ""),
        "plan": profile.get("plan", "freemium"),
        "credits": profile.get("credits", 0),
        "referral_code": profile.get("referral_code", ""),
        "selected_skill": profile.get("selected_skill"),
        "active_project": profile.get("active_project"),
        "skills": profile.get("skills", []),
        "projects": profile.get("projects", []),
        "xp": profile.get("xp", 0),
        "level": profile.get("level", 1),
        "streak": profile.get("streak", 0),
        "badges": profile.get("badges", []),
    }

    try:
        supabase.table("users").upsert(payload, on_conflict="id").execute()
    except Exception:
        pass


def init_user_profile():
    """
    Initialize a structured user profile inside session_state.
    Safe to call on every page.
    """
    if "user_profile" not in st.session_state:
        db_profile = _load_profile_from_db()
        user = _current_user()
        st.session_state.user_profile = {
            "name": db_profile.get("name") or user.get("name") or st.session_state.get("name", ""),
            "age": db_profile.get("age") or user.get("age") or st.session_state.get("age", 15),
            "interest": db_profile.get("interest") or user.get("interest") or st.session_state.get("interest", ""),
            "goal": db_profile.get("goal") or user.get("goal") or st.session_state.get("goal", ""),
            "plan": db_profile.get("plan") or user.get("plan") or "freemium",
            "credits": db_profile.get("credits") if db_profile.get("credits") not in [None, ""] else user.get("credits", 0),
            "referral_code": db_profile.get("referral_code") or user.get("referral_code") or "",
            "selected_skill": db_profile.get("selected_skill", st.session_state.get("selected_skill", None)),
            "active_project": db_profile.get("active_project", st.session_state.get("project", None)),
            "skills": db_profile.get("skills", st.session_state.get("skills", [])),
            "projects": db_profile.get("projects", st.session_state.get("projects", [])),
            "xp": db_profile.get("xp", st.session_state.get("points", 0)),
            "level": db_profile.get("level", st.session_state.get("level", 1)),
            "streak": db_profile.get("streak", st.session_state.get("streak", 0)),
            "badges": db_profile.get("badges", st.session_state.get("badges", [])),
        }


def sync_profile_from_session():
    """
    Pull current known standalone session values into user_profile.
    Use this after onboarding or whenever session values change.
    """
    init_user_profile()

    profile = st.session_state.user_profile
    user = _current_user()

    profile["name"] = (
        st.session_state.get("name")
        or user.get("name")
        or user.get("full_name")
        or profile.get("name", "")
    )
    profile["age"] = (
        st.session_state.get("age")
        or user.get("age")
        or profile.get("age", 15)
    )
    profile["interest"] = (
        st.session_state.get("interest")
        or user.get("interest")
        or profile.get("interest", "")
    )
    profile["goal"] = (
        st.session_state.get("goal")
        or user.get("goal")
        or profile.get("goal", "")
    )
    profile["plan"] = user.get("plan", profile.get("plan", "freemium"))
    profile["credits"] = user.get("credits", profile.get("credits", 0))
    profile["referral_code"] = user.get("referral_code", profile.get("referral_code", ""))
    profile["selected_skill"] = st.session_state.get(
        "selected_skill", profile.get("selected_skill")
    )
    profile["active_project"] = st.session_state.get(
        "project", profile.get("active_project")
    )
    profile["skills"] = st.session_state.get("skills", profile.get("skills", []))
    profile["projects"] = st.session_state.get("projects", profile.get("projects", []))
    profile["xp"] = st.session_state.get("points", profile.get("xp", 0))
    profile["level"] = st.session_state.get("level", profile.get("level", 1))
    profile["streak"] = st.session_state.get("streak", profile.get("streak", 0))
    profile["badges"] = st.session_state.get("badges", profile.get("badges", []))

    st.session_state.user_profile = profile
    _save_profile_to_db(profile)


def sync_session_from_profile():
    """
    Push profile values back into standalone session keys so old pages
    continue working without breaking.
    """
    init_user_profile()

    profile = st.session_state.user_profile

    st.session_state.name = profile.get("name", "")
    st.session_state.age = profile.get("age", 15)
    st.session_state.interest = profile.get("interest", "")
    st.session_state.goal = profile.get("goal", "")
    st.session_state.selected_skill = profile.get("selected_skill", None)
    st.session_state.project = profile.get("active_project", None)
    st.session_state.skills = profile.get("skills", [])
    st.session_state.projects = profile.get("projects", [])
    st.session_state.points = profile.get("xp", 0)
    st.session_state.level = profile.get("level", 1)
    st.session_state.streak = profile.get("streak", 0)
    st.session_state.badges = profile.get("badges", [])

    user = _current_user()
    if user:
        user["name"] = profile.get("name", user.get("name", ""))
        user["age"] = profile.get("age", user.get("age", 15))
        user["interest"] = profile.get("interest", user.get("interest", ""))
        user["goal"] = profile.get("goal", user.get("goal", ""))
        user["plan"] = profile.get("plan", user.get("plan", "freemium"))
        user["credits"] = profile.get("credits", user.get("credits", 0))
        user["referral_code"] = profile.get("referral_code", user.get("referral_code", ""))
        st.session_state.user = user

    _save_profile_to_db(profile)


def get_user_profile():
    """
    Return the current user profile safely.
    """
    init_user_profile()
    db_profile = _load_profile_from_db()
    if db_profile:
        profile = st.session_state.user_profile
        for key, value in db_profile.items():
            if value not in [None, ""]:
                profile[key] = value
        st.session_state.user_profile = profile
        sync_session_from_profile()
    return st.session_state.user_profile


def update_profile_field(field, value):
    """
    Update any one field in the user profile.
    """
    init_user_profile()
    st.session_state.user_profile[field] = value
    sync_session_from_profile()


def add_skill(skill):
    """
    Add a skill to the profile if not already present.
    Also make it the selected skill.
    """
    if not skill:
        return

    init_user_profile()
    skill = skill.strip()

    profile = st.session_state.user_profile
    skills = profile.get("skills", [])

    if skill and skill not in skills:
        skills.append(skill)

    profile["skills"] = skills
    profile["selected_skill"] = skill
    st.session_state.user_profile = profile

    sync_session_from_profile()


def add_project(project):
    """
    Add a project to the profile if not already present.
    Also make it the active project.
    """
    if not project:
        return

    init_user_profile()
    project = project.strip()

    profile = st.session_state.user_profile
    projects = profile.get("projects", [])

    if project and project not in projects:
        projects.append(project)

    profile["projects"] = projects
    profile["active_project"] = project
    st.session_state.user_profile = profile

    sync_session_from_profile()


def set_selected_skill(skill):
    """
    Set the active/selected skill.
    """
    if not skill:
        return

    init_user_profile()
    st.session_state.user_profile["selected_skill"] = skill
    sync_session_from_profile()


def set_active_project(project):
    """
    Set the active/current project.
    """
    if not project:
        return

    init_user_profile()
    st.session_state.user_profile["active_project"] = project
    sync_session_from_profile()


def add_badge(badge):
    """
    Add a badge if it does not already exist.
    """
    if not badge:
        return

    init_user_profile()
    badges = st.session_state.user_profile.get("badges", [])

    if badge not in badges:
        badges.append(badge)

    st.session_state.user_profile["badges"] = badges
    sync_session_from_profile()
