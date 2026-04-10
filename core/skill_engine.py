import json

def load_skills():
    with open("data/skills.json") as f:
        return json.load(f)

def recommend_skill(answers):
    """
    Simple rule-based engine (upgrade later to AI)
    """
    if answers["interest"] == "tech":
        return "AI & Data Analysis"
    elif answers["interest"] == "creative":
        return "Graphics Design"
    elif answers["interest"] == "business":
        return "Digital Marketing"
    else:
        return "General Skills"