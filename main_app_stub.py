
import streamlit as st
from modules.ops import revpah_integrity
from modules.membership import membership_segmenter

# Define all available tools with role-based access control
TOOLS = {
    "RevPAH Integrity": {
        "category": "Ops Tools",
        "roles": ["Admin", "Board", "Ops", "Finance", "Analyst", "Director"],
        "module": revpah_integrity,
    },
    "Membership Segmenter": {
        "category": "Membership Tools",
        "roles": ["Admin", "Board", "Analyst"],
        "module": membership_segmenter,
    },
}

def render_tool(tool_key, user_role):
    """Render a tool if user has proper role access"""
    tool = TOOLS[tool_key]
    if user_role not in tool["roles"]:
        st.error(f"🔒 Access Denied: You don't have permission to use this tool.")
        st.info(f"Required roles: {', '.join(tool['roles'])}")
        return
    tool["module"].run()

st.set_page_config(page_title="SportAI – Enterprise Tools", layout="wide")
st.sidebar.title("SportAI Suite")
st.sidebar.caption("Enterprise Edition v6.0.0")

role = st.sidebar.selectbox("Role", ["Admin","Board","Ops","Finance","Analyst","Director","Sponsor","Member"])
category = st.sidebar.selectbox("Category", ["Ops Tools","Sponsorship Tools","Finance Tools","Membership Tools"])

# Filter tools by selected category
available_tools = {k: v for k, v in TOOLS.items() if v["category"] == category}

st.title("SportAI – Enterprise Tool Suite")

if available_tools:
    st.markdown(f"**Category:** {category} | **Role:** {role}")
    st.divider()

    # Show available tools in category
    tool_choice = st.selectbox("Select Tool", list(available_tools.keys()))

    if tool_choice:
        st.subheader(tool_choice)
        render_tool(tool_choice, role)
else:
    st.info(f"No tools available in '{category}' category yet. More tools coming soon!")
    st.caption("Available categories: Ops Tools, Membership Tools")
