import streamlit as st


def init_user_profile():
    """
    Initialize a structured user profile inside session_state.
    Safe to call on every page.
    """
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "name": st.session_state.get("name", ""),
            "age": st.session_state.get("age", 15),
            "interest": st.session_state.get("interest", ""),
            "goal": st.session_state.get("goal", ""),
            "selected_skill": st.session_state.get("selected_skill", None),
            "active_project": st.session_state.get("project", None),
            "skills": st.session_state.get("skills", []),
            "projects": st.session_state.get("projects", []),
            "xp": st.session_state.get("points", 0),
            "level": st.session_state.get("level", 1),
            "streak": st.session_state.get("streak", 0),
            "badges": st.session_state.get("badges", []),
        }


def sync_profile_from_session():
    """
    Pull current known standalone session values into user_profile.
    Use this after onboarding or whenever session values change.
    """
    init_user_profile()

    profile = st.session_state.user_profile
    profile["name"] = st.session_state.get("name", profile.get("name", ""))
    profile["age"] = st.session_state.get("age", profile.get("age", 15))
    profile["interest"] = st.session_state.get("interest", profile.get("interest", ""))
    profile["goal"] = st.session_state.get("goal", profile.get("goal", ""))
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


def get_user_profile():
    """
    Return the current user profile safely.
    """
    init_user_profile()
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