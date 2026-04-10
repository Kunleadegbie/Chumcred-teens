import streamlit as st

def metric_card(title: str, value: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #ffffff, #f8fafc);
            padding: 20px;
            border-radius: 18px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            margin-bottom: 12px;
        ">
            <div style="font-size: 14px; color: #64748b; font-weight: 600;">{title}</div>
            <div style="font-size: 32px; font-weight: 800; color: #0f172a; margin-top: 6px;">{value}</div>
            <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(title: str, description: str, emoji: str = "🚀"):
    st.markdown(
        f"""
        <div style="
            background: white;
            padding: 22px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
            min-height: 180px;
        ">
            <div style="font-size: 34px;">{emoji}</div>
            <div style="font-size: 20px; font-weight: 800; color: #0f172a; margin-top: 10px;">
                {title}
            </div>
            <div style="font-size: 14px; color: #475569; margin-top: 8px; line-height: 1.6;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="margin-top: 8px; margin-bottom: 18px;">
            <div style="font-size: 28px; font-weight: 800; color: #0f172a;">{title}</div>
            <div style="font-size: 15px; color: #64748b; margin-top: 4px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )